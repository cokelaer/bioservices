from bioservices import Biocontainers

def test_biocontainers():

    b = Biocontainers()
    stats = b.get_stats()
    b.get_tools(limit=10)
    b.get_versions_one_tool("bioservices")

