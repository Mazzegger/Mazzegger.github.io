import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timeline import T
src, dst = sys.argv[1], sys.argv[2]
open(dst, 'w').write(open(src).read().replace('__TIMELINE__', json.dumps(T)))
