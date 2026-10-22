from pathlib import Path
import sys,json,difflib,re
OUT=Path(__file__).resolve().parent;R=OUT.parent
sys.path.insert(0,str(OUT))
from build_delta import pin,fresh,save,now,ck,load,uncomment

history=[]
for p in sorted((R/'dev_sine_resolvent').glob('*/run.json')):
 j=load(p);snapshot=p.parent/'V351SineResolventApprox.lean';sp=pin(snapshot)
 assert sp['sha256']==j['source']['sha256'] and sp['bytes']==j['source']['bytes']
 msgs=[]
 for f in ['stdout','stderr']:
  ck(j[f]);t=Path(j[f]['path']).read_text(encoding='utf8')
  msgs += [line for line in t.splitlines() if ': error:' in line or ': warning:' in line]
 history.append(dict(run=pin(p),snapshot=sp,recorded_source_pin=j['source'],returncode=j['returncode'],diagnostics=msgs,stdout=j['stdout'],stderr=j['stderr'],accepted_for_current_source=False))
p=R/'dev_sine_resolvent/20260914_211359_468646/V351SineResolventApprox.lean'
b=p.read_bytes();current=(R/'k/TGLExt/V351SineResolventApprox.lean').read_bytes()
removed=[l for l in b.splitlines(keepends=True) if l.strip()=='change ‖M n u x-M0 u x‖^2 = _'.encode()]
assert len(removed)==1 and b.replace(removed[0],b'')==current
cleanup=dict(previous=pin(p),current=pin(R/'k/TGLExt/V351SineResolventApprox.lean'),exact_only_removed_line=removed[0].decode(),unified_diff=''.join(difflib.unified_diff(b.decode().splitlines(keepends=True),current.decode().splitlines(keepends=True))),effect='Redundant change removed before final Lake; current source validated by author cold Lake and own Lake, not by treating the prior DEV pin as current')
hd=dict(timestamp=now(),attempts=history,rc1_count=sum(x['returncode']!=0 for x in history),historical_rc0_count=sum(x['returncode']==0 for x in history),final_cleanup=cleanup)
save(OUT/'history_read.json',hd)
private=[dict(kind=m[0],name=m[1]) for m in re.findall(r'^private (def|theorem) (\S+)',uncomment(current.decode()),re.M)]
assert len(private)==7 and sum(x['kind']=='theorem' for x in private)==6
save(OUT/'private_declarations.json',dict(source=pin(R/'k/TGLExt/V351SineResolventApprox.lean'),declarations=private,private_theorems=6,private_definitions=1,public_target_count=11,axiom_scope='Whole source compiled; private proofs covered transitively by public axioms, not 7 additional standalone prints',consumers={'sineWindow_character':'sineWindow_multiplier -> regularSineWindowCore_spectral','sineWindow_multiplier':'regularSineWindowCore_spectral','scalarMultiplier_sequence_tendsto':'regularSineResolvent_tendsto -> regularSpectralResolvent_right','sineWindow_continuous':'regularSineWindowCore_spectral / CFC','sineWindow_nonneg':'regularSineWindowCore_spectral / CFC','sineWindow_le_one':'regularSineWindowCore_spectral / CFC'}))
notes=dict(review_complete=True,findings=[],status='A1_SINE_RESOLVENT_REVIEW_ACCEPTED__CUTOFF_RIGHT_ACTION_TRACE_OPEN',report_name='REVIEW_A1_SINE_RESOLVENT_FINAL',title='Revisão independente — aproximantes seno e ação direita do resolvente',paragraphs=[
'[REAL] A ficha REAPROVEITAMENTO_A1B_APROXIMANTES_SENO MD/JSON e o ADENDO_FICHA_SENO_DCT MD/JSON foram lidos inteiros e seus fornecedores confrontados aos bytes. A ficha antecede a implementação dos aproximantes; o adendo antecede o adaptador DCT. O consumidor prometido é realizado por regularSpectralResolvent_right, não acrescentado como hipótese. As buscas anteriores continuam consultas delimitadas, não prova de exaustividade do acervo.',
'[REAL] Contagem separada: 11 declarações públicas (9 teoremas + 2 definições) têm #check com universos e #print axioms próprios. Além delas, há 6 teoremas privados e 1 definição privada: sineWindow; sineWindow_continuous, sineWindow_nonneg, sineWindow_le_one, sineWindow_character, sineWindow_multiplier e scalarMultiplier_sequence_tendsto. Foram lidos integralmente e compilados no mesmo módulo; seus axiomas são cobertos transitivamente pelos alvos públicos consumidores. Não se alegam sete prints privados adicionais. Inventário em private_declarations.json.',
'[REAL] O sinal está correto para characterPhase=e^(-isξ): X_m=I/2+(Λ_(-1/m)−Λ_(1/m))/(4i) tem símbolo (1+sin(2πξ/m))/2. regularSineWindowCore_right reutiliza a álgebra da ação direita e os dois geradores regulares. regularSineWindowCore_spectral usa o MESMO V=regularSpectralCoordinates e a igualdade já paga com regularUnitary. As fórmulas para m real não exigem m>0; no limite usa-se exclusivamente m=n+1>0.',
'[REAL] regularSineResolvent_cfc identifica o aproximante espectral com CFC de X_m: f_m(z)=ofReal(sigmoid(m(2 Re z−1))). A função é globalmente contínua; o multiplicador de X_m está efetivamente em [0,1] e a normalidade usada em map_cfc decorre da positividade. Não se aplica a interface contratante diretamente ao símbolo assinado m sin. A pertinência ao core e à álgebra direita resulta de scalarRightAction_cfc; não foi postulada.',
'[REAL] sine_rescaled_tendsto usa sinc contínua em zero. O adaptador DCT é sequencial e vale no L² vetorial original: φ_n=(g_n−g)^2‖u‖², dominante integrável ‖u‖² por Lp.memLp. MemLp, a identidade L2_integral_norm_sq e a raiz quadrada transportam o limite da integral para a norma. Os eventos a.e. usados em cada igualdade são finitos para um n e vetor fixos. Não se exige medida finita de ℝ, separabilidade de H, continuidade do representante u ou evento comum a todos os vetores.',
'[REAL] regularSineResolvent_nonneg e norm_le dão operadores positivos de norma ≤1. A autoadjunção de cada aproximante e de R produz a convergência dos adjuntos a partir da convergência forte demonstrada. regularSpectralResolvent_right aplica scalarRightAction_closed_of_bounded_strongStar com cota 1 e todas as hipóteses descarregadas; conclusão para todo P, sem família aproximante residual. A definição herdada de ScalarPolarRight quantifica TODO A∈nν e usa o MESMO scalarWeightGNSEmbedding, scalarGNSRepresentation e scalarTomitaPolarFactor original. Como R*=R, a conclusão pertence à álgebra com as duas propriedades, não só à propriedade unilateral.',
'[REAL] Histórico preservado em history_read.json: cinco DEV [rc1, rc0, rc1, rc1, rc0], três falhas excluídas. O rc0 intermediário das 21:09 não é certificado deste delta completo. O DEV de 21:13 ainda tinha um change redundante e um aviso; seus bytes não são apresentados como finais. A comparação byte a byte verificou exclusivamente a remoção dessa linha antes do Lake autoral final, cujos bytes coincidem com o snapshot próprio e cuja compilação não tem avisos de alvo. Nenhum print parcial de rc1 foi aceito.',
'[REAL] AUDITORIA_APROXIMANTES_SENO_A1B.json e seus streams foram lidos e pinados. O negativo BadSineResolventLimit usa imports funcionais e é recusado por Type mismatch ao trocar o limite R por I−R; não é falha de ambiente. Trata-se de execução autoral relida, sem nova execução do negativo nesta revisão.'
],limits=[
'A ação direita do MESMO R está paga neste delta. A igualdade CFC do corte inverso existente e a ação da sua raiz ainda são passos separados; a consulta por equação de grafo não é uma prova Lean aceita neste relatório.',
'Não se prova convergência em norma de operador, monotonicidade dos aproximantes ou DCT para redes arbitrárias. Não se constrói novo GNS/J/h, não se identifica h regular com Δν por homonímia, não se obtém tracialidade nem se altera gate/memórias/custódias.'
])
save(OUT/'semantic_notes.json',notes)
# Fresh finalizer variant. Preserve the copied parent finalizer.
s=(OUT/'finish_delta.py').read_text()
old="dp=R/rel;dj=load(dp);assert dj['returncode']==0;ck(dj['source'])\n  match=[x for x in s['sources'] if x['target'] and x['original']==dj['source']];assert len(match)==1,dp"
new="""dp=R/rel;dj=load(dp);assert dj['returncode']==0
  historical=dp.parent/'V351SineResolventApprox.lean';hp=pin(historical)
  assert hp['sha256']==dj['source']['sha256'] and hp['bytes']==dj['source']['bytes']
  history=load(out/'history_read.json');cleanup=history['final_cleanup'];ck(cleanup['previous']);ck(cleanup['current'])
  assert historical.read_bytes().replace(cleanup['exact_only_removed_line'].encode(),b'')==Path(cleanup['current']['path']).read_bytes()
  match=[x for x in s['sources'] if x['target'] and x['original']==cleanup['current']];assert len(match)==1,dp"""
assert s.count(old)==1;s=s.replace(old,new)
s=s.replace("role='Historical author DEV evidence only; no object imported'","role='Historical pre-cleanup DEV rc0 with warning, retained source snapshot; final source validated separately by author Lake and own Lake',historical_snapshot=hp,cleanup=cleanup")
old="comp['author_dev_evidence_read_only']=devread"
new="""comp['author_dev_evidence_read_only']=devread
 comp['history']=pin(out/'history_read.json')
 comp['private_declarations']=pin(out/'private_declarations.json')
 comp['private_theorems']=6;comp['private_definitions']=1
 comp['public_new_theorems']=comp['new_theorems'];comp['public_new_definitions']=comp['new_definitions']
 comp['total_source_theorems_including_private']=15;comp['total_source_definitions_including_private']=3
 comp['count_scope']='11 public targets, with 6 private theorems and 1 private definition compiled transitively'
 comp['helper_provenance']=pin(out/'finalizer_provenance.json')"""
assert s.count(old)==1;s=s.replace(old,new)
fresh(OUT/'finish_sine.py',s.encode())
save(OUT/'finalizer_provenance.json',dict(parent=pin(OUT/'finish_delta.py'),variant=pin(OUT/'finish_sine.py'),reason='Disclosed redundant-change cleanup: validate historical snapshot plus exact deletion and both final Lake builds',notes=pin(OUT/'semantic_notes.json'),history=pin(OUT/'history_read.json'),private=pin(OUT/'private_declarations.json'),initial_helper_provenance=pin(OUT/'helper_provenance.json'),preparer=pin(Path(__file__))))
save(OUT/'preparation_history.json',dict(failed_stdin_preparation='SyntaxError unmatched closing parenthesis; parse failed before any write or Lean execution',corrected_preparer=pin(Path(__file__)),lean_build_repeated=False))
print(json.dumps(dict(history=pin(OUT/'history_read.json'),private=pin(OUT/'private_declarations.json'),notes=pin(OUT/'semantic_notes.json'),diff=cleanup['unified_diff']),ensure_ascii=False))
