"""Use complete AX captures; preserve the earlier partial captures unchanged."""
from pathlib import Path
W=Path(__file__).resolve().parent
text=(W/'record_ios35_distribution.py').read_text(encoding='utf-8')
for stem in ('IOS35_EQUIPE','IOS35_PILOTO','IOS35_OPERATOR_PARTICIPATION'):
    text=text.replace(stem+'.txt',stem+'_FULL.txt')
exec(compile(text,str(W/'record_ios35_distribution.py'),'exec'),{'__file__':__file__})
