from pathlib import Path
import hashlib,json,os
R=Path(__file__).resolve().parent
p=R/'delivery_configs/inverse_limit_semifinite.json'
current=p.read_bytes()
new=R/'delivery_configs/inverse_limit_semifinite_final.json'
assert not new.exists()
t=new.with_name(new.name+'.tmp');t.write_bytes(current);assert t.read_bytes()==current;os.replace(t,new)
s=current.decode('utf8')
s=s.replace(',"revisao_consulta_tracialidade_limite/CONSULTA_TRACIALIDADE_LIMITE"','')
addition='A consulta tracial anexa é proposta anterior a este aceite, sem prova Lean nova: localiza a compatibilidade da forma ponderada Q com a estrela e a extensão por Fatou/sanduíches. Não pedir novamente normalidade, fidelidade, escala dual ou densidade usual aqui entregues, nem receber a conclusão tracial como hipótese nova. '
assert addition in s
s=s.replace(addition,'')
original=s.encode('utf8')
checkpoint=json.loads((R/'CHECKPOINT_STATUS_20260914_232411_508207.json').read_text(encoding='utf8'))
expected=next(row for row in checkpoint['artifacts'] if row['path']==str(p))
assert len(original)==expected['bytes'] and hashlib.sha256(original).hexdigest()==expected['sha256']
t=p.with_name(p.name+'.restore_tmp');t.write_bytes(original);assert t.read_bytes()==original;os.replace(t,p)
print(json.dumps(dict(original_config_restored_to_checkpoint_pin=True,final_config_key='inverse_limit_semifinite_final',final_config_sha256=hashlib.sha256(current).hexdigest())))
