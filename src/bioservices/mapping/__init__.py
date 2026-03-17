__version__ = "$Rev: 10 $"

try:
    from importlib.metadata import version

    version = version("biomapping")
except Exception:
    version = __version__


#:import genes
# import proteins
