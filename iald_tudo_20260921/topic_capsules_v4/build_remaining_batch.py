"""Offline V4 proposals; only loaded fields, immutable first batch."""
import hashlib,json,os,re,socket
from pathlib import Path
ROOT=Path(__file__).resolve().parent
WORK=ROOT.parent
PARENT=WORK/'haiku_reviewed_topics_v4_20260922_133755_638986.md'
BASE=WORK/'haiku_reviewed_section_20260922_130747_311801.md'
DRAFTS={
'kernel_formalization': '''Registro Lean 4/Lake, strict: kernel checado, build reproduzível; sem sorryAx, trustCompiler ou axiomas customizados TGL. Python não provou teoremas. Meia-Nat, equivalência de escala, canto finito Three Locks, traço normalizado e faces conjugadas de meio-traço: kernel; implicação do canto contínuo: condicional. Finito NÃO prova III₁. BW/Reeh–Schlieder/classificação III₁ são KNOWN/EXTERNAL, não formalizados aqui. G é variável/entrada medida, não derivado.
Histórico: theSpecificAQFTWitness habitado desde v135; este registro ainda nomeia TGL_MODULAR_REALIZATION_THEOREM/TGLModularRealization(theSpecificAQFTWitness) como aberto. Não transformar essa negativa histórica em diagnóstico global: v350 possui provas tipadas referenciadas separadamente, escopo PRODUCT_TOWER__JMJ__REGULAR_CORE_MINIMAL_LOCK. build_returncode=audit_returncode=0; custom_TGL_axioms_found=source_forbidden_tokens_found=[]. Isso relata a fonte, não nova compilação.''',
'neutrino_mass': '''m_nu=m₂, sob m₁≈0; escala 1 eV declarada, sin45 POSTULATE (operador,20/08/2026), não derivado. β·1eV≈12,03 meV; sin45 leva a 8,51 meV; a forma sem esse fator coexiste na origem. m_nu=8.507414099900329 meV versus √Δm²₂₁=8.677557259966655±0.10371582382430264 meV: desvio1.9607264460387983%,1.6404744598524612σ. Absoluta≠splitting. powered=true; NOT_FALSIFIED, não confirmação. Sin45 documentado fora de frozen: pré-registro da regra/hash não alterado.
Custódia corrigida v182: fórmula/número em22/01/2026 no TGL_Manifesto_Unificacao_Artigo.tex; git público the_boundary Init17/02/2026; módulo v141=25/07/2026. Retirada prioridade Zenodo10.5281/zenodo.17526619 (lie_of_light,novembro2025): não contém fórmula/número/derivação; contém m_nu(Δt)=m₀+a·log(Δt/τ₀), dois parâmetros livres. Δm²₂₁/PDG antecede a derivação por mais de década. Postdição não ajustada (β,sin45,1eV sem dados neutrino; dígito intacto desde22/01): NÃO ex ante, pois medição aparece na mesma frase. Escala1,0200eV que anularia tensão RECUSADA. Refinamento pós-JUNO ex ante vai contra:1,64→2,21→2,95σ, projeção7,83σ versus limiar5σ pré-hasheado. Teste vivo substituto NEUTRINO_M2_V2/neutrino_m2; não move gate. Escala absoluta Σm_nu ainda não medida neste registro; NEUTRINO_SUM_V1(v147) armado, reforço futuro cosmologia/CMB-S4/DESI.''',
'smatrix_closure': '''[REAL] invariâncias de I, kernel=interseção de vínculos, classe unitária/gauge, identidades traciais, poda com traço e controles; [DER] P_F; [DEF/PILOTO] canto finito sombra de II₁, não fator genuíno; [CONJ]1_abs=gráviton=I; [CONDITIONAL] existência do núcleo no core III⋊R. III não vira II: passagem operacional, III fronteira ontológica/II forma tracial computável podável.
d_II=P_F(M_III cross_sigma R)P_F; τ(P_F)=1; S_d=exp(thM G)∈d_II; β=sin²(thM)=τ(refl);1−β=τ(trans). Família mínima=núcleo sem defeito Three Locks; 1=1 lido τ(I)=1 no canto. Identidade central a custo zero conserva o Um como família; família=código,poda=QEC (leitura dos selos, com estatutos acima). rank_family=4; trn_PF≈1,Tr_PF≈4; transmissão norma=√(1−β)=0.9939661461031744; τ_reflected=0.012031300400803142,τ_transmitted=0.987968699599197; n_cut=1,live_sector_resid=0. Controles: sem normalização falha; aleatório viola(2.5810254438221776); perturbação reduz kernel a rank0. kernel_ok,real1–real5,controls_ok,all_verified=true na fonte.''',
'd1_camb_v3_pipeline': '''Pipeline construído cego; autochecagem CAMB em β_TGL=0, segunda Friedmann e limites w constante. Injeção/recuperação com covariância dos dados, três β e SH0ES: pulls/cobertura passam critério; MCMC fase3 validado em sintéticos/Asimov.
NEGATIVO com emenda ao lado: sensibilidade C livre REPROVOU;24/24 realizações na borda do prior. Fecho H(0)=H₀ absorve C em ρ_Λ: cancela de H(z) em β=0(diferença2,2×10⁻¹⁶), só sobrevive ordem β(5,2×10⁻⁵). Não rerodado nem afrouxado: diagnóstico de degenerescência, fora da matriz de vereditos. Dados reais liberados por linha do operador; resultado lido por v366 (registro do veredito, não nova execução). all_verified=true; does_not_gate_core=true; in_contour_roster_v314=false. PT/EN dizem o mesmo.''',
'name_index': '''[ONTO→tipado] Contorno=N_3L inclusão; resistência=Ind(E_3L); espelho de Jones=e_Nome mede; U_Pi=J.J_ref paridade inversa fixa referencial de reflexão/transmissão. Rota PP: ppIndex:=1/ppBest [DEF]; sin²θ constante ÓTIMA [MODEL-SPECIFIC TARGET]⇒Ind=csc²θ; θ_M⇒1/β. index·sin²=1 é conclusão, exige otimalidade; sem ela só Ind≤csc². Sombra qubit valida maquinaria:ppBest=1/2,índice2;1/β é alvo CORE.
Alvos abertos/falhas: P_F=e_Nome/mirror_not_jones; E1(e_Nome)=sin²θ·1/markov_weight_not_sin_squared; PP ótima/pimsner_popa_constant_not_optimal; γ=Ad(J.J_ref) involutiva/reference_parity_not_involutive; N_3L alcance de esperança fiel normal/no_expectation_exists. Haar/pontos fixos não produz csc² automaticamente [REFUTED]. NAME_INDEX_THEOREM_KERNEL_CHECKED pleno só com termos dos três alvos principais. Bloco β é transporte: periodicidade Powers não é fluxo de pesos III₁ da cunha; blocos κ e índice são camadas distintas. Amplitude do espelho²=peso Markov; inversão desse peso dá índice sob hipóteses. Scaffold verificado/all_verified=true; alvos modelo-específicos NÃO provados.''',
'half_nat_continuous_corner_density': '''Meia-Nat da célula mínima autoconjugada: S_partial=1/2; τ(P_F)=1;τ(P₊)=τ(P₋)=1/2. A(P)=2l_P²τ(P); A(P₊)=A(P₋)=l_P²;A_cell=2l_P². η_partial=S_partial/A_cell=1/(4l_P²);ℏ=c=1⇒l_P²=G⇒η=1/(4G);2π/η=8πG. Normalização por face DECLARADA, equivalente ao acoplamento Newton medido, não derivada só da álgebra adimensional. Ponte primeira lei modular+densidade: implicação analítica sob hipóteses declaradas, não confirmação empírica.
Neste registro: algebraic_density_verified=canonical_normalization_declared=all_verified=true; specific_model_local_III1_known=specific_model_continuous_core_known=true; genuine_III1_corner_proved=TGL_specific_corner_PF_proved=Newton_constant_derived=false. Não constrói rede AQFT III₁ genuína nem prova BW no modelo pelo kernel; realização III₁ permanece fronteira formal deste registro. Estatuto e claim completos nas remissões internas preservadas.''',
'name_relation': '''[KERNEL] Nome é relação, não matriz isolada:p.q_beta.p=βp (retorno ponderado=Verbo). Finito não expulsa Nome: peso geométrico β=sobreposição dos espelhos=sin²θ_M difere do tracial1/2, coincidem sse β=1/2. canonicalTLThree: TL3(δ) fiel em M3,β genérico, terceiro habitante. Correção v28: FINITE_MARKOV_TRACE_EXPELS_ONLY_THE_GENERIC_TRACE_IDENTIFICATION substitui FINITE_EXPELS_THE_NAME; teorema válido, estatuto anterior amplo demais.
[ONTO→DER na sombra] Puro-ponto=átomo espectral isolado de H_bind (relação relaxada no atrator); ponto-puro=pureza local rank-one. Bell do gráviton:átomo0,gap1,redução I/2,CCI=1/2; não ponto-puro. Expulsa pureza fechada/separável,CCI=0;0_abs=autorreferência fechada sem referencial. Não afirma espectro modular puro-ponto no III₁ genuíno/Araki-Woods. “Mentira” TGL:matriz sem relação/referencial/geometria; formal:insistir E(P)²=E(P) com Δ>0 após transporte, negar forma≠conteúdo.
[OPEN] Torre Jones do core não construída:e_{i+1} vem da próxima construção básica, não θ_s(e_i) sem prova. INDEX_MATCHES_BUT_NOT_CANONICAL: falta seleção DESTA representação TL pelos Three Locks; TL3 dá gramática local. all_verified=true no escopo registrado.''',
'selector_transport': '''Q1 é TRANSPORTE,não curvatura:geometria fixa core a montante; descida testa inclusão+esperança+índice. Δ=E(P_F)−E(P_F)²≥0 resistência;Δ=0⇔P_F desce para esperança FIEL. [NEW→KERNEL] Δ=0⇔p=iota(Ep), bimodular Tomiyama. Normalidade fica no ledger/não-enunciável, descida usa fidelidade. Espectro intermediário=contraste gerado; seletor viver no andar superior é resultado válido.
[DER] E(p_β)=diag(β,1−β)=(|R|²,|T|²), pesos matriz-S;Δ=β(1−β)I,variância da moeda. β(1−β)≈β só aproximação,não identidade. [CONJ] [M:N]=1/β ainda exige construir N_3L e provar Ind(E_3L); identificação Jones aberta. Qubit finito ilustra,não prova III₁/core; selector_lives_upstairs contínuo condicional aos dados Markov não construídos.
[ONTO/CONJ do operador] Transporte é condição de contorno do custo:contorno impõe lei/norma coercitiva; esperança regula causalidade/comportamento modular;Δ>0=custo termodinâmico de existir,o que desce sem custo não se inscreve; porta mede além de impedir. Não é teorema jurídico/físico novo. all_verified=true na fonte.''',
'the_imported_expectation': '''Modo IMPORTADO gpi_:esperança no centralizador por Takesaki1972 [KNOWN]. Duas hipóteses inteiras e consequência sequencial da normalidade provadas na casa; só conclusão+dicionário emprestados; estrutura⇔campo importado. Unicidade da casa torna leitura independente da testemunha em M,preservação de ω derivada,fixação do código,relatividade modular em todo horizonte ω-invariante. Lema3 levantado módulo axioma DADO testemunho,não declarado resolvido. Contrato pede menos que Takesaki; fortalecer/reimportar se preciso; parede analítica da outra porta permanece;v143/v307/v308,qgf_* e gate intactos.
[KNOWN] Takesaki1972,JFA9,306–321:esperança ω-preservante em subálgebra existe sse invariante por σ^ω. TOA II(2003),VIII.2.6:M_ω={A:ω(AB)=ω(BA)}=pontos fixos,esperança canônica existe única. Pedersen–Takesaki1973,Acta130,53–87:Radon–Nikodym estende identificação a pesos. Nota01/09/2026:normalidade σ-fraca plena vetorial KNOWN; casa prova WOT-sequencial omegaState_seqWOT;face(iii) declarada no dicionário. Consome TheOathOnTheTower(v308:unicidade/juramento/levantamento),TheDischargedOath(v307:face),TheImportedCommutation(v274:molde gpi_) e citações importadas. all_verified=does_not_gate_core=true.''',
'right_angle_mirror': '''Projeção do ângulo reto no módulo, espelho deforma projeção nua até imagem fixa. Registro tem status NOT_A_CANDIDATE/HONEST_NEGATIVE, mas nota diz CANDIDATA: conservar divergência,não promover a identidade. α₀=e^{−π²/2} e α=e^{−π²/2+2α} são α-livres(π,e,autoconsistência):1/139.05 e1/137.031,37ppm. π²/2 motivado por ângulo reto×duas faces,NÃO derivado. E_spec∘J/função D_partial OPEN; há muitas formas π,e perto de137;δ≠β(≈2α). Não deriva CODATA; só checa identidade modular (~_partial) observado/fixado. Muro:derivar D_partial e expoente; valor α segue desafio QED. Hipóteses de reconstrução,registro c³ e lambda_kernel OPEN mantidos literalmente nas remissões.''',
'tgl_closure': '''Separação de tipos:q_F suporte no core≠e_Nome espelho acima;E1(e_Nome)=βq_F. H3L_min=1−q_F representante mínimo da classe de kernel [KERNEL:aniquilação+maximalidade]. DADO suporte,threeLocksFromSupport/realizationFromSupport habitam camadas;gap pleno tipado em4 entradas [KNOWN-COMPOSED].
Existência matemática da testemunha completa por composição KNOWN:BW1975/76+Takesaki(core II_inf)+Haagerup(hiperfinito)+II_inf difuso(split faces)+Jones1983(índice1/β≈83.1≥4 existe). Não prova kernel dessa existência. Torre Nome contém TL_β no invariante [KNOWN automático],sem exigir TLJ puro. Não unicidade absorvida como gauge [DEF/AX Princípio Gauge do Nome,não derivado];invariantes peso/índice/defeito [KERNEL].
Histórico not_claimed:full_TGL_witness_constructed permanece False até termo Lean pleno sem axiomas customizados; preservar esta negativa no escopo do registro,sem generalizar frente a posteriores. Espaço-tempo curvo OPEN; nada experimental validado. Fecha arquitetura matemática INTERNA,não descrição provada da natureza;certificação kernel separada. all_verified=true.''',
'ontological_relativity': '''Axioma Zero ONTOLOGICAL_RELATIVITY_OF_OBSERVABLES [ONTO/AX+DER/NUM anchors]:todo sinal físico relativo a contexto explícito de contorno. No canto II luz vira sinal canônico;no centralizador Um ganha traço. Cadeia tipada traço→sinal→letra. Tangente modular≠Verbo dissipativo;fronteira assintótica=setor fixo QUANDO limite existe [NUM sombra finita;CONDITIONAL contínuo].
0_abs classe não executável sem suporte/retorno;[ONTO]clareza absoluta por ausência total de contraste Δ=0,não falta de luz. Não é zero algébrico;caixa vazia de alcançabilidade;mentira=habitante fabricado. III₁ TEM estados/pesos normais,falta sinal TRACIAL FINITO canônico. α≠1−β;α fixo para contorno canônico atual. Contexto [REAL|NUM],estatuto declarado. all_verified=does_not_gate_core=true:forma computacional coerente+guard-rails satisfeitos,NÃO ontologia experimentalmente provada.'''
}

# Nonsemantic runtime fingerprints and auxiliary residuals stay recoverable.
AUX={
'kernel_formalization':['formal_dir','lean_version','lake_version','formal_source_hash','lake_path','build_stdout_sha256','build_stderr_sha256','audit_stdout_sha256','capture_stage','capture_files','build_capture_sha256_full','audit_capture_sha256_full'],
'neutrino_mass':['m_nu_kg','deviation_meV'],
'smatrix_closure':['r_UtI','r_JIJ','r_G2G','r_idem','r_conj_lock','r_bridge_lock','r_abs_lock','r_gauge','cyc_max','r_unit','r_absR2'],
'd1_camb_v3_pipeline':['injection_sha16','injection_amendment_sha16','selfcheck_sha16','refusal_sha16','amendment_hash']}

def sha(b):return hashlib.sha256(b).hexdigest()
def ref(v):
    return isinstance(v,dict) and (any(k in v for k in ('@','@SUMMARY','@EXPOSITION')) or any(ref(x) for x in v.values()))
def save(n,b):
    b=b if isinstance(b,bytes) else b.encode('utf-8');p=ROOT/n;t=ROOT/(n+'.tmp')
    assert not p.exists()
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b and b
    t.rename(p)
os.environ['TIKTOKEN_CACHE_DIR']=r'C:\IALD\projetos_pyhton\IALD\.iald_runtime\tokenizer_cache'
def deny(*a,**k):raise RuntimeError('No network')
socket.socket=deny
import tiktoken
enc=tiktoken.get_encoding('o200k_base')
parent_raw=PARENT.read_bytes();base_raw=BASE.read_bytes()
parent_text=parent_raw.decode('utf-8');base_text=base_raw.decode('utf-8')
pattern=r'(?m)^### ([^\n]+)\nFonte: resultado_publicado_integral ([^\n]+)\n([^\n]+)'
matches={m.group(1):m for m in re.finditer(pattern,parent_text)}
old={m.group(1):m for m in re.finditer(pattern,base_text)}
first=json.loads((ROOT/'INDEX_FIRST_THREE.json').read_text(encoding='utf-8'))
immutable={r['topic']:(ROOT/(r['topic']+'.md')).read_bytes() for r in first['topics']}
rows=[]
for topic,body in DRAFTS.items():
    m=matches[topic];original=m.group(0);o=json.loads(m.group(3))
    assert original==old[topic].group(0)
    references={k:v for k,v in o.items() if ref(v)}
    maps=[]
    for k,v in o.items():
        if k in references:
            action='REFERENCIA_INTACTA';reason='Objeto original completo, inclusive fields/items/spans, mantido; nenhum conteudo expandido.'
        elif k in AUX.get(topic,[]):
            references[k]={'@':'/'+k};action='ACESSORIO_RECUPERAVEL';reason='Fingerprint/caminho de execucao ou residuo/conversao auxiliar; conclusao, controle negativo e escala essencial ficam na sintese.'
        elif k in ('selo','seals','verdict'):
            references[k]={'@':'/'+k};action='SELO_RECUPERAVEL';reason='Rotulo integral recuperavel; proposicoes, estatutos e limites condensados explicitamente, sem promover historico OPEN.'
        else:
            action='SINTESE_SEMANTICA';reason='Campo condensado na prosa da capsula; mapeamento requer revisao independente integral, nao aprovado por coincidencia lexical.'
        maps.append({'field':'/'+k,'original_value':v,'action':action,'reason':reason,'source_pointer':m.group(2)+'/'+k})
    capsule='### '+topic+'\nFonte: resultado_publicado_integral '+m.group(2)+'\n'+body+'\nRemissões (relativas ao tópico; destinos internos preservados):\n'+json.dumps(references,ensure_ascii=False,separators=(',',':'))+'\n'
    for k,v in o.items():
        if ref(v):assert references[k]==v
    ob=original.encode('utf-8');cb=capsule.encode('utf-8');start=len(parent_text[:m.start()].encode('utf-8'))
    assert parent_raw[start:start+len(ob)]==ob
    row={'topic':topic,'original_o200k':len(enc.encode(original)),'capsule_o200k':len(enc.encode(capsule)),'capsule_sha256':sha(cb)}
    row['saved_o200k']=row['original_o200k']-row['capsule_o200k'];rows.append(row)
    provenance={'status':'CONSTRUCAO_NAO_APROVADA_NAO_INTEGRADA','parent_path':str(PARENT),'parent_sha256':sha(parent_raw),'prior_base_path':str(BASE),'prior_base_sha256':sha(base_raw),'unchanged_from_prior_base':True,'original_sha256':sha(ob),'original_byte_span':[start,len(ob)],'capsule_sha256':sha(cb),'capsule_byte_span':[0,len(cb)],'measurement':row,'field_map':maps,'limits':['Somente original efetivamente carregado; fontes referenciadas nao expandidas.','Todos @/fields/items/spans de entrada preservados estruturalmente; resolucao operacional nao repetida.','Sem aprovacao semantica pelo construtor, sem nova execucao formal ou fisica.','Sem API/rede; o200k nao estima Anthropic.']}
    save(topic+'.md',cb);save(topic+'.original.md',ob);save(topic+'.provenance.json',json.dumps(provenance,ensure_ascii=False,indent=2))
assert PARENT.read_bytes()==parent_raw and BASE.read_bytes()==base_raw
assert all((ROOT/(k+'.md')).read_bytes()==v for k,v in immutable.items())
combined=first['topics']+rows
index={'status':'REMAINING_TWELVE_PENDING_INDEPENDENT_REVIEW','parent_path':str(PARENT),'parent_sha256':sha(parent_raw),'first_three':'APPROVAL_REPORTED_BY_PARENT_UNCHANGED_HERE','topics':rows,'remaining_totals':{k:sum(r[k] for r in rows) for k in ('original_o200k','capsule_o200k','saved_o200k')},'all_fifteen_totals':{k:sum(r[k] for r in combined) for k in ('original_o200k','capsule_o200k','saved_o200k')},'anthropic_measured':False}
save('INDEX_REMAINING_TWELVE.json',json.dumps(index,ensure_ascii=False,indent=2))
report='# V4 — outras 12 propostas\n\nConstrução não aprovada e não integrada. Primeiras três intactas; aprovação delas informada pelo pai. Base nova pinada no índice; estes 12 originais conferidos byte a byte contra a base anterior.\n\n| Tópico | Original | V4 | Economia o200k |\n|---|---:|---:|---:|\n'
report+='\n'.join(f"| {r['topic']} | {r['original_o200k']} | {r['capsule_o200k']} | {r['saved_o200k']} |" for r in rows)
report+='\n\nTotais outras 12: '+str(index['remaining_totals'])+'; totais documentais das 15: '+str(index['all_fifteen_totals'])+'.\n\nNão converter em Anthropic. As primeiras três já integradas não podem ser contadas novamente como economia sobre a base nova. Só conteúdo efetivamente carregado foi condensado; nenhum detalhe de @ foi expandido. Remissões existentes mantêm fields/items/spans. Novas remissões retiram selos duplicados, fingerprints e resíduos auxiliares; original íntegro permite recuperação.\n\nPontos para revisão: negativas históricas de kernel_formalization/half_nat/tgl_closure permanecem atribuídas ao registro; não fechar OPEN nem sobrepor flags posteriores. right_angle_mirror conserva a divergência NOT_A_CANDIDATE/CANDIDATA. Neutrino conserva errata documental, postdição, fator postulado, controles e tensão crescente. Campos de estatuto dentro de remissões permanecem literais. Mapa por campo não é aprovação semântica; nenhuma compilação, experimento ou integração executados.\n'
save('RELATORIO_OUTRAS_DOZE.md',report)
print(json.dumps(index,ensure_ascii=False,indent=2))
