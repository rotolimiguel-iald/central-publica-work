from pathlib import Path
import datetime,hashlib,json,os,re
R=Path(__file__).resolve().parent;K=R/'k'
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
 assert p.is_relative_to(R) and not p.exists(),p
 t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b and b;os.replace(t,p)
specs=[('V351ScalarImaginaryRightTransport','matrixUnit_imaginaryPower_right_scaling'),
 ('V351ScalarImaginaryRightTransport','scalarTomitaImaginaryPower_regular_right_commutes'),
 ('V351ScalarTomitaImaginaryConjugation','scalarTomitaImaginaryPower_polar_commutes'),
 ('V350MatrixUnitPolarTransport','matrixUnit_polar_left_weighted'),
 ('V350ScalarRegularRightPolar','scalarTomitaPolarFactor_regular_left'),
 ('V350ScalarTomitaPolarFactor','scalarTomitaPolarFactor')]
providers=[]
for module,name in specs:
 p=K/'TGLExt'/f'{module}.lean';s=p.read_text(encoding='utf8')
 m=re.search(r'^(?:theorem|def) '+name+r'\b[\s\S]*?(?= :=| where)',s,re.M);assert m,name
 providers.append(dict(name='TGLV350.Regular.'+name,file=pin(p),line=s[:m.start()].count('\n')+1,statement=m[0],decision='REUSAR',matches='Supplies one side of the transport; no provider has the combined left-action type'))
searchfiles=[R/x for x in ['BUSCAS_A1B_ESQUERDA.json','BUSCAS_A1B_ESQUERDA_RETRY.json','BUSCA_A1B_ACERVO_REFINADA.json']]
stamp=datetime.datetime.now().astimezone().isoformat()
target='''For every SiteProfile P,N,i,j,t,x on ScalarGNSHilbert P, with U=scalarTomitaImaginaryPower P, J=scalarTomitaPolarFactor P, R=homogeneousRightGNS(matrixUnitRightData P N i j), A=star(homogeneousRightCoreElement(matrixUnitRightData P N i j)), r=localEigenvalue P N i j:
 U_t (scalarGNSRepresentation P A x)=star(modularPhase t (Real.log r)) • scalarGNSRepresentation P A (U_t x).
For A_s=star(regularRightCoreElement P s):
 U_t (scalarGNSRepresentation P A_s x)=scalarGNSRepresentation P A_s (U_t x).
No premise asserting either conclusion; use J injective, J U=U J, the existing weighted J-left/right relation and right scaling. Two theorems only, no new operator/structure.'''
doc=dict(timestamp=stamp,decision='ADAPTAR',consumer=dict(path=str(R.parent/'LACUNAS_A1.md'),line=25,name='regular_dual_weight_modular_implementation',
 next_step='same-GNS generator action, prior to extending to the full core and identifying AdLambda',final_contract='TGLV351.RegularCoreTraceData'),exact_target=target,
 providers=providers,searches=[pin(p) for p in searchfiles],
 search_result='Existing polar and right transports found; no combined left imaginary-power transport found in the inspected source/type recuts. Refined exact-name acervo search returned0of13608indexed files, not an absence claim outside that index.',
 rejected_false_match='Unbounded Imaginary.*Left matched serialized package paths; preserved then replaced by exact-name search.',
 preserved='Seven orphan sources, all old reports/notes and monolith; no duplicated GNS/J/phase/weight',
 open_after=['full modular action on every core element','positive affiliated regular generator','inverse-generator perturbation trace'])
put(R/'REAPROVEITAMENTO_A1B_ESQUERDA.json',json.dumps(doc,ensure_ascii=False,indent=2).encode('utf8'))
text='[OPEN — ficha antes dos dois lemas de transporte à esquerda]\n\n# A1(b) — mesma ação no lado esquerdo\n\n'+stamp+'\n\nADAPTAR os fornecedores existentes; duas composições tipadas, sem definir outro operador, J, GNS, raiz ou peso.\n\nConsumidor: `regular_dual_weight_modular_implementation`, LACUNAS_A1.md:25. Esta é a etapa dos geradores na mesma representação, anterior à extensão para todo o core e identificação com AdLambda. Contrato final: TGLV351.RegularCoreTraceData.\n\n## Tipo exato\n\n```text\n'+target+'\n```\n\n## Fornecedores\n\n'
for p in providers:text+=f"### {p['name']}\n\n`{p['file']['path']}:{p['line']}` · `{p['file']['sha256']}`\n```lean\n{p['statement']}\n```\nREUSAR a premissa intermediária; nenhuma recebe a conclusão nova.\n\n"
text+='## Buscas e limites\n\nAs seis modalidades e os recortes estão nos três JSONs de buscas: kernel local por nome/tipo, notasV350, entregas/outrasbancadas, árvoreA1, TOE e índiceacervo. As leituras recusadas pelo sandbox foram repetidas; o TOE não apresentou ocorrência. O padrão largo Imaginary.*Left encontrou caminhos serializados e foi corrigido; o padrão final de nomes exatos retornou zero em13608arquivos indexados. Não se afirma ausência em todo arquivo do computador.\n\nO sinal conjugado decorre da antilinearidade de J; não pode ser apagado. A comparação da frequência desse gerador com AdLambda precisa de outro lema consumidor, não de homonímia. Não se prova existência de traço nem H3. O delta não altera os sete módulos existentes ou seus resultados; suas reproduções standalone seguem em paralelo.\n'
put(R/'REAPROVEITAMENTO_A1B_ESQUERDA.md',text.encode('utf8'))
print(json.dumps(dict(fiche=True,providers=len(providers),new_theorems_planned=2)))
