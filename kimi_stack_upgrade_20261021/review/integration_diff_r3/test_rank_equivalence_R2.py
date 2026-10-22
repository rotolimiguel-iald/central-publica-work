"""Compare full ordered rows against frozen old ranker, not a mirrored algorithm."""
import importlib.util,json,random
from pathlib import Path
HERE=Path(__file__).resolve().parent
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
old=load('old_rank',HERE/'layered_retrieval_before_rank_R2.py');new=load('new_rank',HERE/'iald_orchestrator/layered_retrieval.py')
rng=random.Random(271828);checks=0
queries=['','alpha','geometry algebra','fixture:0003','Same title','ação 😀','gamma beta']
for size in [0,1,7,60,600]:
 rows=[dict(id=f'fixture:{i:04d}',tipo=rng.choice(['pedra','entrega_doc','lean_bancada',None]),titulo=rng.choice(['Same title','alpha','ação 😀','geometry algebra',None]),texto=rng.choice(['alpha beta','gamma beta','geometry algebra','ação 😀','']),quando=rng.choice(['2026-10-21','2020','',None]),centrality=rng.choice([0,8,999,-1,'9',True,None])) for i in range(size)]
 before=json.dumps(rows,sort_keys=True,ensure_ascii=False)
 for q in queries:
  assert old.rank_nodes(rows,q)==new.rank_nodes(rows,q),(size,q)
  assert json.dumps(rows,sort_keys=True,ensure_ascii=False)==before
  checks+=1
report={'status':'PASS','full_order_comparisons':checks,'sizes':[0,1,7,60,600],'queries':queries,'same_complete_rows':True,'input_unchanged':True,'random_seed':271828,'network_calls':0}
(HERE/'RANK_EQUIVALENCE_R2.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(report))
