__version__ = "$Rev: 10 $"
import pkg_resources
try:
    version = pkg_resources.require("biomapping")[0].version
except:
    version = __version__



#:import genes
#import proteins
