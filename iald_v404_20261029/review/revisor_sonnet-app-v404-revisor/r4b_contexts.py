"""Reviewer: print each strict old-wording hit with its enclosing, decoded context (RAW view of the model's text) for shared and haiku55."""
import re,sys,json
from pathlib import Path
W=Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029')
SEP=r'[\s\W_]{1,12}'
rx=re.compile(r'15'+SEP+r'(?:as'+SEP+r')?(?:calculad\w*|computad\w*|computed|calculated)'+SEP+r'(?:e|and|plus|\+|mais|com)?'+SEP+r'3'+SEP+r'(?:as'+SEP+r')?liter\w*',re.I)
for pkg in sys.argv[1:]:
    t=(W/'app/packages'/pkg/'prefix.md').read_text('utf-8')
    print('=================',pkg)
    for m in rx.finditer(t):
        a=max(0,m.start()-420);b=min(len(t),m.end()+420)
        print('--- at',m.start(),'/',len(t));print(t[a:b].replace('\n','\\n'));print()
