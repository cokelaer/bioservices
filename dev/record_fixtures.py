#!/usr/bin/env python
"""Record real web-service responses into test/fixtures/.

The recorded payloads serve two purposes:

1. they let unit tests replay a realistic response without touching the
   network, which is what makes the per-PR suite fast and deterministic;
2. they are the source of truth for validating the pydantic models of
   BioServices v2 — a model that cannot parse the recorded payload is wrong.

They are deliberately stored as transport-agnostic JSON (method, url, params,
status, headers, body) rather than as ``requests`` or ``httpx`` objects, so the
same files keep working across the httpx migration.

Usage::

    python dev/record_fixtures.py               # record everything
    python dev/record_fixtures.py uniprot       # only names starting with uniprot
    python dev/record_fixtures.py --list        # show what is defined

Recording hits live services, so it is a developer action, never part of a test
run. Re-record only when an API changes; a fixture that silently drifts is worse
than no fixture at all.
"""
import argparse
import json
import sys
from pathlib import Path

import requests

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "test" / "fixtures"

#: Headers worth keeping: they drive content negotiation and rate limiting, and
#: replaying the rest (cookies, request ids, dates) would only add churn.
KEPT_HEADERS = {"content-type", "retry-after", "x-ratelimit-limit", "x-ratelimit-remaining"}

#: Cap on a recorded body. Fixtures are read by humans in diffs; a 10 MB blob is
#: not a fixture, it is a liability.
MAX_BODY = 200_000


# name -> (method, url, params)
EXCHANGES = {
    # -- UniProt: WS-3 tier 1, and the most used service in the package -------
    "uniprot/search_zap70": (
        "GET",
        "https://rest.uniprot.org/uniprotkb/search",
        {"query": "ZAP70 AND organism_id:9606", "format": "json", "size": 2},
    ),
    "uniprot/entry_P43403": (
        "GET",
        "https://rest.uniprot.org/uniprotkb/P43403.json",
        None,
    ),
    "uniprot/fasta_P43403": (
        "GET",
        "https://rest.uniprot.org/uniprotkb/P43403.fasta",
        None,
    ),
    # error shapes, so the error path can be tested against real bodies.
    # A well-formed but non-existent accession gives a genuine 404 ...
    "uniprot/entry_missing_404": (
        "GET",
        "https://rest.uniprot.org/uniprotkb/A0A000A0A9.json",
        None,
    ),
    # ... whereas a malformed one is rejected as a 400. Both are worth pinning:
    # they are the two failure modes a caller passing a bad id will hit.
    "uniprot/entry_bad_accession_400": (
        "GET",
        "https://rest.uniprot.org/uniprotkb/NOTAREALACCESSION.json",
        None,
    ),
    "uniprot/search_bad_query_400": (
        "GET",
        "https://rest.uniprot.org/uniprotkb/search",
        {"format": "json"},  # missing the required 'query'
    ),
    # -- KEGG: plain text, a completely different response shape -------------
    "kegg/get_hsa10458": ("GET", "https://rest.kegg.jp/get/hsa:10458", None),
    "kegg/list_pathway_hsa": ("GET", "https://rest.kegg.jp/list/pathway/hsa", None),
    # KEGG withdrew /list/organism: it now answers 400 with an empty body, which
    # breaks KEGG.list("organism") and KEGG.organismIds. Recorded so the fix and
    # its regression test can be written offline.
    "kegg/list_organism_400": ("GET", "https://rest.kegg.jp/list/organism", None),
    # -- ChEMBL: json, tier 1 ------------------------------------------------
    "chembl/molecule_CHEMBL25": (
        "GET",
        "https://www.ebi.ac.uk/chembl/api/data/molecule/CHEMBL25.json",
        None,
    ),
    # -- UniChem: pins the documented oddity that an unknown identifier is
    #    answered with 500 rather than 404 (see UniChem._get_or_empty) --------
    "unichem/sources": ("GET", "https://www.ebi.ac.uk/unichem/api/v1/sources", None),
    "unichem/inchi_unknown_500": (
        "GET",
        "https://www.ebi.ac.uk/unichem/rest/inchi/NOTAREALINCHIKEY",
        None,
    ),
}


def record(name, method, url, params, timeout=30):
    """Perform one request and write it to ``test/fixtures/<name>.json``."""
    response = requests.request(
        method,
        url,
        params=params,
        timeout=timeout,
        headers={"User-Agent": "bioservices-fixture-recorder"},
    )

    text = response.text
    truncated = len(text) > MAX_BODY
    if truncated:
        text = text[:MAX_BODY]

    body = text
    content_type = response.headers.get("content-type", "")
    if "json" in content_type and not truncated:
        try:
            body = response.json()
        except ValueError:
            pass  # keep the raw text; a malformed body is itself worth recording

    payload = {
        "request": {"method": method, "url": url, "params": params},
        "response": {
            "status_code": response.status_code,
            "reason": response.reason,
            "headers": {k.lower(): v for k, v in response.headers.items() if k.lower() in KEPT_HEADERS},
            "body": body,
            "truncated": truncated,
        },
    }

    path = FIXTURES_DIR / f"{name}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return response.status_code, path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("prefix", nargs="*", help="only record fixtures whose name starts with one of these")
    parser.add_argument("--list", action="store_true", help="list the defined fixtures and exit")
    args = parser.parse_args(argv)

    if args.list:
        for name in sorted(EXCHANGES):
            print(name)
        return 0

    selected = sorted(name for name in EXCHANGES if not args.prefix or any(name.startswith(p) for p in args.prefix))
    if not selected:
        print("Nothing matched.", file=sys.stderr)
        return 1

    failures = 0
    for name in selected:
        method, url, params = EXCHANGES[name]
        try:
            status, path = record(name, method, url, params)
        except Exception as err:  # network problems must not abort the whole run
            print(f"FAIL {name}: {type(err).__name__}: {err}", file=sys.stderr)
            failures += 1
            continue
        print(f"  {status}  {name}  ->  {path.relative_to(FIXTURES_DIR.parent.parent)}")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
