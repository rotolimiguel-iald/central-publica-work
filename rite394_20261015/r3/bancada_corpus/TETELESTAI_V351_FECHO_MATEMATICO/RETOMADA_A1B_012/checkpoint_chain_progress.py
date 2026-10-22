from pathlib import Path
import datetime,hashlib,json,os
R=Path(__file__).resolve().parent
stamp=datetime.datetime.now().astimezone().isoformat();suffix=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b,memory=False):
 assert p.is_relative_to(R) and b
 if p.exists():
  assert memory
  old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+suffix);assert not bak.exists();bak.write_bytes(old);assert bak.read_bytes()==old
  assert len(b)>=len(old)
 t=p.with_name(p.name+'.tmp_'+suffix);t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
rows=[]
for label,audit,review in [
 ('core','AUDITORIA_ACAO_CORE_A1B','revisao_core/REVIEW_A1_CORE_FINAL'),
 ('absorption','AUDITORIA_ABSORCAO_A1B','revisao_absorcao/REVIEW_A1_ABSORPTION_FINAL'),
 ('fourier','AUDITORIA_FOURIER_TRANSLACAO_A1B','revisao_fourier/REVIEW_A1_FOURIER_FINAL'),
 ('graph','AUDITORIA_GRAFO_POSITIVO_A1B','revisao_grafo/REVIEW_A1_POSITIVE_GRAPH_FINAL'),
 ('spectral','AUDITORIA_GRAFO_ESPECTRAL_A1B','revisao_grafo_espectral/REVIEW_A1_SPECTRAL_GRAPH_FINAL'),
 ('calculus','AUDITORIA_CALCULO_MULTIPLICADOR_A1B','revisao_calculo/REVIEW_A1_MULTIPLIER_CALCULUS_FINAL'),
 ('powers','AUDITORIA_POTENCIAS_REGULARES_A1B','revisao_potencias/REVIEW_A1_REGULAR_POWERS_FINAL')]:
 ap=R/(audit+'.json');vp=R/(review+'.json');d=json.loads(ap.read_text(encoding='utf8')) if ap.exists() else None
 if d:
  assert d['all_axioms_allowed'] and d['negative_controls_rejected'] and not d['dev_objects_used']
  for m in d['modules']:
   for field in ['source','object']:assert pin(Path(m[field]['path']))==m[field]
 rows.append(dict(label=label,author=pin(ap) if d else None,new_theorems=d['new_theorems'] if d else None,new_definitions=d.get('new_definitions',0) if d else None,review=pin(vp) if vp.exists() else None,review_filename_expected_when_absent=True))
record=dict(timestamp=stamp,delta_status=rows,
    development_regular_powers=pin(R/'dev_regular_powers/20260914_193204_622512/run.json'),
    weight_trace_correction=pin(R/'ADENDO_SEMIFINITUDE_PESO_VS_TRACO.json'),
    delivery_writer_draft=pin(R/'deliver_reviewed_delta.py'),
    next_obligations=['affiliation of same positive regular graph','dual scaling of same generator','Pedersen-Takesaki inverse-generator trace'],
    warning='Do not run checkpoint_retornada.py again: it rewrites the old memory text and may drop append-only corrections. Use append-only checkpoints.',
    technique='For a LinearIsometryEquiv V use V.toLinearIsometry.toContinuousLinearMap; V.toContinuousLinearMap may resolve to a finite-dimensional LinearEquiv method.',
    full_trace_constructed=False,gate_changed=False)
rp=R/('CHECKPOINT_CHAIN_'+suffix+'.json');put(rp,json.dumps(record,ensure_ascii=False,indent=2).encode('utf8'))
table='\n'.join('| '+x['label']+' | '+('rc0 / negativo recusado' if x['author'] else 'pendente')+' | '+('arquivo disponível; ler antes de selar' if x['review'] else 'pendente')+' |' for x in rows)
text=f'''\n\n## Adendo {stamp} — cadeia regular e reprodução

| Delta | Auditoria autoral | Revisão independente |
|---|---|---|
{table}

Os scripts sequenciais antigos20318,21402,34209 encerraram rc0. A auditoria do cálculo funcional está disponível. A fila autoral das potências é60881, caso ainda não haja AUDITORIA_POTENCIAS_REGULARES_A1B. Nenhum deles deve ser repetido por memória antiga. Ler os relatórios efetivos.

Resultados novos após o checkpoint inicial: V351RegularSpectralGraph (3teoremas0defs) identifica o grafo de h com e^(-2πξ) em coordenadas V=W F^-1; V351ScalarMultiplierCalculus (3teoremas2defs) agrupa operatorFieldLift num homomorfismo para usar map_cfc, sem novo L²; V351RegularImaginaryPowers (4teoremas0defs) prova em DEVrc0 que resolventImaginaryPower do MESMO resolvente é Λ_t. A última fonte está estável no run dev_regular_powers/20260914_193204_622512, semwarnings. A aceitação exige autor e revisor, não DEV sozinho.

Fila do revisor Pasteur: core5→absorção6→Fourier3→grafo15→espectral3→cálculo5→potências4, cada relatório separado. corebuild privado começou19:02. Não duplicar ColdLake. O script deliver_reviewed_delta.py é rascunho e ainda requer ler os pareceres finais/status efetivos antes de execução; nenhuma entrega nova desses deltas foi registrada por este checkpoint. ENTREGAreprodução40 e B1–B6 permanecem seladas.

Próxima ponte de afiliação: character_commutation_local_pairing já dá igualdade pontual das formas sesquilineares para todo operador que comuta com caracteres. Pode ser consumida para provar comutação com realScalarMultiplier, conjugada por V, e então preservação do grafo por N′; não reconstruir aproximações por funções simples antes de avaliar esse fornecedor. Ainda NÃO foi codificada nesta retomada. Escala dual e traço permanecem depois disso. A propriedade de minorantes é exigida de τ, não do peso ν (ver adendo anterior).

Coerção Lean corrigida nesta rodada: para LinearIsometryEquiv V, usar V.toLinearIsometry.toContinuousLinearMap, não V.toContinuousLinearMap (pode escolher método de LinearEquiv que exige dimensão finita). Tentativas falhas preservadas. Nunca aceitar seus sorryAx automáticos.

Não rodar novamente checkpoint_retornada.py, que reescreve o texto antigo. Continuar por append com backup imediato de bytes. Snapshot estruturado: {rp.name}.
'''
md=R/'MEMORIA_RETOMADA_A1B_012.md';put(md,md.read_bytes()+text.encode('utf8'),memory=True)
jp=R/'MEMORIA_RETOMADA_A1B_012.json';data=json.loads(jp.read_text(encoding='utf8'));data.setdefault('append_only_checkpoints',[]).append(pin(rp));put(jp,json.dumps(data,ensure_ascii=False,indent=2).encode('utf8'),memory=True)
print(json.dumps(dict(checkpoint=pin(rp),memory=pin(md)),ensure_ascii=False))
