from pathlib import Path
import datetime, hashlib, json, os, re, subprocess
R=Path(__file__).resolve().parent; K=R/'k'; CHAT=R.parent.parent
def pin(p):
    b=p.read_bytes(); return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True)
    q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
pat='fourier_shift|fourier.*translation|fourier.*characterMultiplier|shift.*fourier|regular_unitary_positive_generator'
queries=[
 ('kernel',['rg','-n',pat,str(K/'TGLExt'),'-g','*.lean']),
 ('notes',['rg','-n',pat,str(CHAT/'TETELESTAI_V350_KERNEL_20260911'),'-g','*.md','-g','!*.bak*']),
 ('deliveries',['rg','-n',pat,str(CHAT/'TUNEL/DO_CHATGPT'),'-g','*.md']),
 ('tree',['rg','-n',pat+'|gerador|traço',str(R.parent/'base_v351/A_PROVA_DA_QG_TGL_arvore.md')]),
 ('toe',['rg','-n',pat,r'C:\IALD\Artigo\BANCADA_TOE\kernel_bancada','-g','*.lean','-g','!**/.lake/**']),
 ('acervo',[r'C:\Python314\python.exe','-X','utf8','-B',r'C:\IALD\INDICE_DO_ACERVO\buscar.py',pat,'--max','20','--ctx','150']),
 ('other_workbenches',['rg','-l','fourier_shift|fourier.*characterMultiplier|shift.*fourier',str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!**/attempts/**','-g','!*.bak*'])]
A=R/'search_fourier_translation'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True)
rows=[]
for label,cmd in queries:
    p=subprocess.run(cmd,capture_output=True)
    out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt');put(out,p.stdout);put(err,p.stderr)
    rows.append(dict(label=label,command=cmd,returncode=p.returncode,stdout=pin(out),stderr=pin(err)))
    print(label,p.returncode,len(p.stdout),len(p.stderr),flush=True)
put(A/'searches.json',json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
assert all(r['returncode'] in (0,1) and r['stderr']['bytes']==0 for r in rows),'Incomplete search; preserved logs'
mathlib=K/'.lake/packages/mathlib/Mathlib'
specs=[
 (K/'TGLExt/V350L2Translation.lean','shift_ae'),
 (K/'TGLExt/V350L2CharacterMultiplier.lean','characterMultiplier_ae'),
 (K/'TGLExt/V350FourierL1L2.lean','fourier_integral_ae_eq_L2'),
 (mathlib/'Analysis/Fourier/LpSpace.lean','fourierTransformₗᵢ'),
 (mathlib/'Analysis/Fourier/LpSpace.lean','SchwartzMap.toLp_fourier_eq'),
 (mathlib/'Analysis/Distribution/SchwartzSpace/Basic.lean','compSubConstCLM'),
 (mathlib/'Analysis/Fourier/FourierTransform.lean','fourierIntegral_comp_add_right')]
providers=[]
for p,name in specs:
    s=p.read_text(encoding='utf8');m=re.search(r'^(?:def|theorem|lemma) '+re.escape(name)+r'(?:\s|\()[\s\S]*?(?= :=| where)',s,re.M)
    assert m,name
    providers.append(dict(name=name,source=pin(p),line=s[:m.start()].count('\n')+1,statement=m[0],decision='REUSAR'))
stamp=datetime.datetime.now().astimezone().isoformat()
target='forall t : Real, forall f : RegularHilbert H, Lp.fourierTransformₗᵢ Real H (shift t f) = characterMultiplier (2 * Real.pi * t) (Lp.fourierTransformₗᵢ Real H f)'
d=dict(timestamp=stamp,status='OPEN__FICHE_BEFORE_FOURIER_TRANSLATION_BRIDGE',decision='ADAPTAR',
    consumer=dict(path=str(R.parent/'LACUNAS_A1.md'),line=31,name='regular_unitary_positive_generator',route=pin(R/'ROTA_GERADOR_REGULAR_A1B.md')),
    exact_target=target,providers=providers,searches=pin(A/'searches.json'),
    scope='Existing Fourier isometry and actual L2 shift and character multiplier; Schwartz translation identity then dense extension. No new Fourier, L2, generator, or trace definition.',
    not_claimed=['positive generator','affiliation','inverse-generator trace','A1b complete','gate change'])
put(R/'REAPROVEITAMENTO_A1B_FOURIER_TRANSLACAO.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior à ligação Fourier/translação no L² existente]\n\n# A1(b): fase espectral da translação regular\n\n'+stamp+'\n\nConsumidor: LACUNAS_A1.md:31, regular_unitary_positive_generator, seguindo ROTA_GERADOR_REGULAR_A1B.\n\n```text\n'+target+'\n```\n\nADAPTAR. O sinal é o da casa: S_t f(x)=f(x−t), Fourier usa exp(−2πixξ), characterPhase(s,ξ)=exp(−isξ); s=2πt. Usar a Fourier L² da mathlib e a extensão densa de Schwartz. O fornecedor L1/L2 existente é uma alternativa; não refazer Plancherel. Lemas auxiliares só os consumidos pela igualdade acima. Nenhum novo espaço, Fourier, gerador ou traço.\n\n## Fornecedores\n\n'
for p in providers:s+=f"`{p['source']['path']}:{p['line']}` — `{p['source']['sha256']}`\n\n```lean\n{p['statement']}\n```\n\n"
s+='## Busca e aceitação\n\nSeis modalidades e outras bancadas registradas em '+str(A/'searches.json')+'. Os resultados identificam fornecedores, não uma prova de ausência em todo computador. Cada saída foi preservada, inclusive eventual erro de acesso; a ficha só é escrita se as sete leituras terminarem sem erro. A aceitação requer Lake isolado, axiomas, negativo com sinal trocado e revisão distinta. Até lá, desenvolvimento somente.\n'
put(R/'REAPROVEITAMENTO_A1B_FOURIER_TRANSLACAO.md',s.encode('utf8'));print('FICHE',len(providers))
