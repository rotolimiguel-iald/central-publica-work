"""Assemble an additive, reviewed F1.REDE delivery without changing pinned work."""
from pathlib import Path
import datetime as dt
import hashlib,json,os,sys
ROOT=Path(r'C:\IALD\Central de Patentes')
OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.REDE'
WORK=ROOT/'work/rede_quantica_20261013'
def pin(p):
    p=Path(p);b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def new(name,value):
    p=OUT/name;t=p.with_name(p.name+'.tmp')
    if p.exists():raise FileExistsError(p)
    b=(value if isinstance(value,str) else json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    with t.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    assert t.read_bytes()==b;os.rename(t,p)
    return pin(p)

for name in ['RELATORIO_ENTREGA_R1.md','RESULTADO_ENTREGA_R1.json','MANIFESTO_ARQUIVOS_R1.json','MAP_ENTRY_ENTREGA_R1.json']:
    if (OUT/name).exists():raise FileExistsError(OUT/name)
review=Path(sys.argv[1])
assert review.is_relative_to(OUT/'review_modular') and review.is_file()
review_data=json.loads(review.read_text(encoding='utf-8'))
assert review_data['status']=='PASS_FORMAL_SCOPE__NO_MATERIAL_FINDING'
assert review_data['rebuilt_modules']==9 and review_data['audited_modular_declarations']==75
modular=json.loads((OUT/'modular_wedge/RESULTADO_MODULAR_R1.json').read_text(encoding='utf-8'))
assert modular['audited_declarations']==75 and modular['sorry']==0
assert all(m['exit_code']==0 for m in modular['modules'])
synthetic=json.loads((OUT/'continuum/RESULTADO_WIGNER_R1.json').read_text(encoding='utf-8'))
assert synthetic['verdict']=='PASS'
device=json.loads((OUT/'review_device_r2/REVIEW_DEVICE_R1.json').read_text(encoding='utf-8'))
assert device['all_pass'] and device['checks']==142
assert not list(OUT.rglob('__pycache__'))
at=dt.datetime.now(dt.timezone.utc).isoformat()
report='''# F1.REDE — entrega construtiva, 13/10/2026

Autor: codex-gerente-tgl. Unidade criada no evento737 e reivindicada no738.
Base de raciocínio: v392 autorizada pelo operador; isso não anuncia ratificação
nem versão implantada. Estatuto da entrega: candidata à auditoria da gerência.

## Resultado principal

**O contrato espectral D1a.3 agora tem um habitante concreto.**
`F1Rede.CanonicalWedge.spectralOutput` usa o H1 original. Foram construídos a
ponte Fubini L² vetorial, Fourier parcial, J antiunitário involutivo, T positivo
auto-adjunto, S=JT fechado de domínio denso, K=Fix(S) padrão e não nulo e a
igualdade completa dos grafos Δ=S†S. Esse avanço retira a ausência de habitante
espectral registrada na fase anterior; não promove automaticamente a rede inteira.

O arquivo CONTRATO_REDE_R2.md contém os dez blocos N0–N9 e suas obrigações.
CONSTRUCAO_CONTINUA_R1.md dá a seção de Wigner, o cociclo, a extensão antiunitária
e a rede livre de helicidades ±1 por localização modular e Fock. É uma construção
analítica [DERIVED sobre KNOWN], com revisão independente. Sua formalização
integral 4D e sua identificação com o dispositivo permanecem [OPEN].

## O que foi reaproveitado e construído

| Camada | Resultado e evidência | Alcance |
|---|---|---|
| Escritos/dispositivos | MQC, Supercondutor, Ψ-NET, TGL-Tensor, A Ponte, Q6 e Tratado, por hash e página/linha | Fonte do autor, sem inferir concessão ou hardware medido |
| Rede finita | Álgebras por fatores tensoriais; H e salto holográfico do Supercondutor | Truncamento sintético 2×2×2; geometria27sítios não é simulação de27qubits |
| Rede da reta | K_a=U(a)K_0, isotonia, translação/dilatação e não vacuidade | 39declarações locais; recompilação independente; não é rede4D |
| Fubini/Fourier | Ponte sobrejetiva canônica, seçõesAE, Fourier parcial e B0 | 31declarações locais; recompilação independente |
| Conjugação | Reflexão q→−q, conjugação e troca de helicidades | 30declarações; usada pela construção modular |
| Cunha espectral | Habitante D1a3OutputBGL + positividade adicional | 75declarações locais em5módulos; todas só no trio, zero sorry |
| Poincaré/Fock | Fórmulas explícitas e aplicação BGL; revisão analítica | [DERIVED/KNOWN], ainda não rede4D compilada |

As contagens são por componente e incluem definições/lemas; não são somadas como
um total de teoremas independentes. A revisão modular reconstitui também as
dependências novas. Comandos, toolchain, LEAN_PATH literal, início/fim, duração,
exit e axiomas estão nos recibos. Tentativas falhas foram conservadas.

A revisão modular obteve9/9EXIT0 em274,09s e conferiu169pinos antes e depois.
Na comparação binária dos cinco módulos modulares,2/5`.olean` são idênticos;
as outras diferenças estão registradas. Não se anuncia reprodução binária total.

**Precisão formal:** `ModularGroupIsBoost` comprova a fase multiplicativa
exp(itσ)=B0(−2πt) após Fourier, com σ=4π²ξ. O grafo Δ é o multiplicador expσ.
A interpretação disso como potência imaginária pelo teorema espectral é a
identificação analítica declarada; não foi usada uma API geral de cálculo
funcional para operadores ilimitados da mathlib.

## Medições sintéticas

O teste do dispositivo foi pré-registrado e passou em142/142verificações,
reproduzidas independentemente. Inclui positividade completa/traço e balanço de
energia do sistema aberto. β foi calculado da constante da fonte em runtime.
Nenhuma taxa de engenharia foi ajustada a dado; as taxas sintéticas são INPUT.

Para a representação contínua,128amostras e12famílias de identidades passaram
com tolerância1e−9; maior resíduo1,564e−13. O controle que omite a reflexão
transversal falhou como exigido: desvio0,99109. Isso verifica sinais e fórmulas em
amostras; a prova global é analítica, e não decorre dessa amostragem.

Os controles também mostram por que uma codificação não linear de amplitudes
não pode ser chamada de canal CPTP universal e por que a coerência normalizada
C=2|ρ01| não é o próprio elementoρ01. O modelo documentado de julho já continha
normalização adequada: reaproveitado, não atribuído a esta entrega.

## O contrato físico completo e suas lacunas exatas

1. **Refinamento e identificação [OPEN].** Construir a sequência de dispositivos,
   seu limite/setor físico e V unitário. Provar VU_dispositivo(g)=U_canônico(g)V
   para Poincaré completo e a reflexão, além de VK_dispositivo(W)=K_canônico(W).
   Igualdade do Hilbert abstrato ou de um boost isolado não atende esse contrato.
2. **Localização no kernel [OPEN].** Formalizar cociclo e ação4D, a igualdade do J
   espectral com a reflexão geométrica, as outras cunhas e a aplicação BGL.
3. **Certificados simultâneos [OPEN].** Construir a realização exigida pelos
   FockCertificate/MaxwellCertificate, normalização e domínios do stress tensor.
4. **Gravitação.** Reutilizar a implicação geométrica auditada da F2.3.
   H3 em todas as direções continua hipótese física nomeada; não foi derivada
   do estado, do dispositivo ou da Fundação. Takesaki segue na unidade própria.

A rede livre acima já é uma realização matemática conhecida de cinemática da
luz. Ela não constitui por si uma previsão distintiva deβ nem um modelo completo
de gravitação interagente. O ganho novo desta unidade é sua ligação explícita ao
H1 da casa e a construção formal do contrato espectral que antes não tinha termo.

## Revisão remota e processo

A autorização específica ao DeepSeek foi usada em uma única chamada, concluída
no mesmo request/job. Resposta custodiada comoDECLARADO; a revisão local separou
as sugestões úteis dos erros de unidades, β e tipos. Não houve repetição da chamada.

R1 eR2, fontes e recibos anteriores ficaram em arquivos próprios. A atualização
do Nós Vivo teve backup dos dois artefatos derivados. Nenhum original científico,
pedido de patente, um.py, kernel do Nós, Bancada produtiva, selo ou gate foi editado.
As únicas memórias atualizadas por esta etapa são as superfícies cobertas pela
reivindicação, com recibos próprios. Não há dado observado aberto nem5σ medido.

## Navegação

- CONTRATO_REDE_R2.md / .json — objetos, correspondências e falsificadores.
- CONSTRUCAO_CONTINUA_R1.md / .json — representação completa e rede livre analítica.
- modular_wedge/RESULTADO_MODULAR_R1.json — fontes congeladas, builds e axiomas.
- review_modular/ — revisão e recompilação independente da cadeia nova.
- finite_device/ e review_device_r2/ — pré-registro, teste e reprodução.
- provider/ e review_deepseek/ — resposta única e conferência crítica.
- MANIFESTO_ARQUIVOS_R1.json — hashes lidos dos artefatos desta entrega.

ENTREGUE significa submissão dessa construção e do contrato à gerência.
AUDITADA/FECHADA e eventual integração são atos dela; não foram presumidos.
'''
report_pin=new('RELATORIO_ENTREGA_R1.md',report)
files=[pin(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p.suffix not in {'.tmp'}]
work_names=['OPERADOR_REDE_VERBATIM.txt','OPERADOR_LOCALIZACAO_VERBATIM.txt','NOVA_UNIDADE.json','BOARD_NEW.json','BOARD_CLAIM.json','wigner_checks_r1.py','write_continuum_r1.py','prepare_delivery_r1.py']
manifest=new('MANIFESTO_ARQUIVOS_R1.json',{'at':at,'file_count':len(files),'files':files,'work_sources':[pin(WORK/n) for n in work_names],'scope':'Immutable delivery snapshot; excludes this manifest and later registration/memory receipts.'})
evidence=[OUT/'CONTRATO_REDE_R2.json',OUT/'CONSTRUCAO_CONTINUA_R1.json',OUT/'modular_wedge/RESULTADO_MODULAR_R1.json',review,OUT/'review_contract/REVIEW_CONTRACT_R2.json',OUT/'review_continuum/REVIEW_R1.json',OUT/'review_light_ray/REVIEW_LIGHT_RAY_R1.json',OUT/'review_fubini/20261013T213537_597067Z/REVIEW_RESULT.json',OUT/'review_device_r2/REVIEW_DEVICE_R1.json',OUT/'review_deepseek/REVIEW_DEEPSEEK_R1.json',OUT/'continuum/RESULTADO_WIGNER_R1.json']
result={'unit':'F1.REDE','at':at,'status':'ENTREGUE','verdict':'CONTRACT_AND_SPECTRAL_REALIZATION_DELIVERED__DEVICE_TO_4D_OPEN','working_basis':'v392 operator-authorized, ratification/deployment distinct','spectral_inhabitant':'F1Rede.CanonicalWedge.spectralOutput : AuditF13v31.D1a3OutputBGL','lean_scope':{'modular_local_declarations':75,'modular_modules':5,'sorry':0,'allowed_axioms':modular['allowed_axioms'],'full_4d_net':False,'independent_review':pin(review)},'synthetic_device_checks':142,'synthetic_wigner_samples':128,'full_device_refinement':'OPEN','H3_from_state':'NOT_CLAIMED','operator_confirmed_device_identity':'Location confirmed; related MQC/Supercondutor sources used, no unique device identity inferred.','report':report_pin,'manifest':manifest,'evidence':[pin(p) for p in evidence],'remote_execution':{'provider':'deepseek','request_id':'701e5bcb-cb47-4706-a9be-9b5ed10f4a35','job_id':'4d57aa1f-2d40-43df-8f82-f16593d899a2','attempts':1,'status':'completed reviewed locally no repeat'},'next_action':'Gerencia audits delivery; subsequent construction targets geometric operator identification/full Poincare and the independent device refinement contract.','gate_changed':False,'observed_data_opened':False}
result_pin=new('RESULTADO_ENTREGA_R1.json',result)
entry={'tipo':'ROTA','rota_id':'formal.f1_rede.canonical_spectral_realization','dominio':'KERNEL_FORMAL','titulo':'Rede: contrato dos dispositivos, Fubini vetorial e habitante espectral D1a.3','pergunta':'Como ligar os escritos/dispositivos do operador ao H1 canônico e construir efetivamente a saída modular antes apenas tipada?','dados':['v392 autorizada','MQC/Supercondutor/PSI-NET/TGL-Tensor e artigos pinados','BGL2002'],'metodo':'Levantamento previo; construção Lean em sandbox, testes sintéticos pré-registrados, revisão e recompilação independente; uma chamada DeepSeek autorizada.','resultado':'D1a3OutputBGL habitado com T positivo, J concreto, K padrão não nulo e Delta=S†S. 75 declarações modulares trio/zero sorry; rede da reta e Fubini construídas;142 testes reduzidos reproduzidos. Rede4D analítica por Wigner/BGL; formalização4D e ponte do dispositivo abertas.','veredito':result['verdict'],'estatuto':'DERIVED','status':'ENTREGUE','olhou_dados':False,'defeito':'Nenhum habitante Fock/Maxwell simultâneo, refinamento físico ou H3 derivado do estado é reivindicado.','nao_refazer':'Reutilizar Fubini, rede da reta, módulos positivos e conjugação geométrica; não repetir DeepSeek.','proximo_passo':result['next_action'],'onde':str(OUT),'artefatos':[result_pin['path'],report_pin['path'],str(OUT/'CONTRATO_REDE_R2.json'),str(OUT/'CONSTRUCAO_CONTINUA_R1.json'),str(OUT/'modular_wedge/RESULTADO_MODULAR_R1.json')],'refs':['formal.f1_3.reconcile_v376_mathlib_plan','formal.f1_takesaki.modular_identity_to_scaling'],'nota':'Contagens por componente não somadas; fase multiplicativa modular não é API geral de cálculo funcional da mathlib. Gerência ainda audita.'}
new('MAP_ENTRY_ENTREGA_R1.json',entry)
print(json.dumps({'result':result_pin,'manifest':manifest,'snapshot_files':len(files)},ensure_ascii=False))
