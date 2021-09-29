# imports - standard imports
import sys

PYTHON_VERSION = sys.version_info


def _is_python_version(*args, **kwargs):
    major = kwargs.get("major", None)
    minor = kwargs.get("minor", None)
    patch = kwargs.get("patch", None)

    result = True

    if major:
        result = result and major == PYTHON_VERSION.major
    if minor:
        result = result and minor == PYTHON_VERSION.minor
    if patch:
        result = result and patch == PYTHON_VERSION.micro

    return result


PY2 = _is_python_version(major=2)


def iteritems(dict_, **kwargs):
    if PY2:
        iterator = dict_.iteritems()
    else:
        iterator = iter(dict_.items(), **kwargs)
    return iterator


if PY2:
    string_types = basestring
else:
    string_types = str
