import sys
keys=tuple(sys.modules.keys())
for key in keys:
    if "percolation" in key:
        del sys.modules[key]
import percolation as P
P.start()
#P.close()
