from pathlib import Path
import os
R=Path(__file__).resolve().parent
s=(R/'review_functional_weight_laws.py').read_text(encoding='utf-8')
changes=[
 ('functional_evaluation_independent_20260914_093032_161654','functional_laws_independent_20260914_093642_937361'),
 ("'functional_laws_independent_'","'series_normality_independent_'"),
 ("NAME='V351BaseFunctionalWeightLaws'","NAME='V351BaseSeriesNormality'"),
 ('20260914_093341_530178','20260914_093715_947928'),
 ('==12','==4'),
 ('V351BaseFunctionalEvaluation','V351BaseFunctionalWeightLaws'),
 ('==384','==385'),
 ('REAPROVEITAMENTO_A1_LEIS_FUNCIONAIS','REAPROVEITAMENTO_A1_NORMALIDADE_SERIES'),
 ("assert sha(ficha['consultation']['path'])==ficha['consultation']['sha256']\n",''),
 ('REVIEW_A1_AVALIACAO_FUNCIONAL_FINAL.md','REVIEW_A1_LEIS_FUNCIONAIS_FINAL.md'),
 ('AuditBaseFunctionalWeightLaws','AuditBaseSeriesNormality'),
 ('384 frozen own-tree inputs: 380 old inherited binaries not rebuilt; four V351 parents independently reproduced earlier (extended base, semifiniteness, Moreau, evaluation). External packages readonly reused; no author project build in LEAN_PATH. The earlier 384-entry milestone manifest contains the contract rather than the newly added evaluation and is not misidentified as this 384-object build list.',
  '385 frozen own-tree inputs: 380 old inherited binaries not rebuilt; five V351 parents independently reproduced earlier (extended base, semifiniteness, Moreau, evaluation, functional laws). External packages readonly reused; no author project build in LEAN_PATH. Earlier milestone manifest is kept distinct from this expanded list.')]
for a,b in changes:
    assert a in s,a
    s=s.replace(a,b)
assert "NAME='V351BaseSeriesNormality'" in s
dst=R/'review_series_normality.py';assert not dst.exists()
t=dst.with_name(dst.name+'.tmp');data=s.encode('utf-8')
with t.open('xb') as f:f.write(data)
assert t.read_bytes()==data;os.replace(t,dst)
print(dst)
