from wbuild.scanFiles import *
from wbuild.utils import *
print('Processing file',sys.argv[1])
writeWBParseDependencyFile(sys.argv[1])