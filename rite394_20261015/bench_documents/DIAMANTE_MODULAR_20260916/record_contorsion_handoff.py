"""Record the reviewed conditional source map with byte-backed local memory."""
import json
from finalize_weyl_bridge import ROOT, WORK, NOW, pin, atomic, backed_replace

target = ROOT/'CONTORSION_HANDOFF_MANIFEST.json'
if target.exists():
    raise FileExistsError('Already issued')
review = '''# Revisão da passagem contorção–fonte

17/09/2026. Revisor independente Hypatia, id01a0af27-0ee6-7611-9d10-8757d9d040f0. [DERIVED — parecer escrito, não Lean].

Veredito recebido por ferramenta: “APROVADO no escopo declarado — [DERIVED], identidade geométrica e composição condicional. Não encontrei erro de índices ou sinais. A aprovação não abrange equações de movimento nem realização física da TGL.”

Leu integralmente a nota CONTORCAO_FONTE_E_CARGA_REGIONAL.md, verify_contorsion_source.py e CONTORSION_SOURCE_CHECKS.json; consultou pontualmente Atlas/índice e a proposição1 de https://arxiv.org/pdf/1807.02041. Não auditou as remissões canônicas .tex/um.py. Nenhum script reexecutado, escrita, novo agente ou promoção de gate.

Confirmou a ordem Gamma[r,mu,s], Ric[s,nu]=R[r,s,r,nu], a diferença D e a fonte B=Sym(D)−g tr(D)/2. Confirmou a compatibilidade métrica C[r,mu,s]=−C[s,mu,r] com o primeiro índice abaixado. Confirmou o sinal T_eff=Theta_sym−B/kappa e a contribuição +2pi/kappa integral xi B1 em R1. Exigiu explicitar C0=0: para C0 não nulo há termos cruzados na primeira variação. Essa precisão foi incorporada.

Reconheceu as distinções entre fonte clássica central e inserção operatorial, entre reescrita e equação da conexão, e entre conservação por equação métrica e demonstração independente por Noether. A proposição citada consome equações de matéria e torsão.

O JSON contém83true:40 comparações de Ricci,40 da aplicação linear de simetrização/traço e3 controles. A leitura não autentica sozinha sua execução; a execução pelo autor retornouPASS. A mesma função de traço é usada em ambos os lados do segundo grupo, portanto ele não detectaria coeficiente de traço errado; o −1/2 foi conferido matematicamente. dbase não é um jato geométrico completo simétrico, mas cancela na diferença. O negativo confere somente4Q≠2Q quandoQ≠0. Não há teste deEOM, conservação, integral regional, estado ou não centralidade física. Essas limitações foram acrescentadas à nota.
'''
atomic(ROOT/'REVISAO_CONTORCAO_FONTE.md', review)
receipt = json.loads((ROOT/'CONTORSION_SOURCE_CHECKS.json').read_text())
assert receipt['count'] == receipt['passed'] == 83
assert all(x['passed'] for x in receipt['checks'])
appendix = f'''
## {NOW} — fornecedor Cartan localizado e passagem para a fonte

[REAL — leitura delimitada] A Ponte Einstein Cartan Miguel.tex:530–548 escreveGamma=Gamma_LC+K_beta condicional;2223–2234 registra derivação explícita contínua deK_beta entreabertos históricos. prove_cocycle_to_einstein no um.py consultado já possui T_TGL_decomposition e geometry_stays_levi_civita, com consumidoresv361 e fontesv362 presentes. Presença não atesta rodada/selo. Não afirmar ausência deCartan porque o fornecedorEinstein-sigma usaLevi-Civita. Não confundirtorção modularmatricial comtorsãoespaço-temporal.

[DERIVED revisado — Hypatia] CONTORCAO_FONTE_E_CARGA_REGIONAL.md fornece, dadoC=K_beta, DeltaRic=∇C−∇C+C*C−C*C, B=Sym(DeltaRic)−g tr(DeltaRic)/2 e T_eff=Theta_sym−B/kappa. EmamplitudeC_e=epsilonC1, g/xi/Sigma/kappa/bordofixos, a parcela decontorção emR1 temsinal +2pi/kappa integralxiB1. C0≠0 exigeprodutoscruzados. Estado e fonteΘaindavariam; fonteclássicabIécentral.83controlesracionaispassaram, comlimitaçõesexplícitasdorevisor; nãoEOMnemmodelofísico. Proposição1 DeLorenzo/DePaoli/Speziale1807.02041usaEOMmatéria/torção paraconservação semusarEOMmétrica.

[OPEN] Ainda consumirC(psi,beta), equaçãodeconexão, inserçãorenormalizada, resposta doestado eação regionalnomesmopar. Não identificaressemapacondicionalcomderivação deK_beta. Zerooriginaleditado, zeroexecuçãoum, zeronovafunçãodemotor, zeronovogate. Evidêncianovaécomposiçãoescrita/revisadaecontrolesalgébricos; objetivoglobalincompleto.
'''
memory=[]
for name in ('MEMORIA_CENTRAL.md','REGISTRO_DAS_CONVERSAS.md','PROPOSTA_MEMORIA_ATLAS.md'):
    path=ROOT/name
    old=path.read_bytes()
    backup=backed_replace(path,old+appendix.encode('utf-8'))
    assert path.read_bytes().startswith(old)
    memory.append({'backup':backup,'after':pin(path)})
tunnel=WORK/'TUNEL/DO_CHATGPT/ENTREGA_CONTORCAO_FONTE_REGIONAL_20260917.md'
atomic(tunnel, '''# Passagem condicional da contorção à fonte regional

[DERIVED revisado] Dado o fornecedorC=K_beta, a nota explicita o tensorB e T_eff=Theta_sym−B/kappa, além da parcela correspondente no coeficienteR1. A Ponte e o cociclo existentes foram localizados: não há pedido de trocarLevi-Civita poroutrateoria. Ainda falta consumir a contorçãofísica e sua equaçãodeconexão, o estado e as inserçõesrenormalizadas.

- [Nota e escopo](../../DIAMANTE_MODULAR_20260916/CONTORCAO_FONTE_E_CARGA_REGIONAL.md)
- [Revisão](../../DIAMANTE_MODULAR_20260916/REVISAO_CONTORCAO_FONTE.md)
- [83 controles racionais](../../DIAMANTE_MODULAR_20260916/CONTORSION_SOURCE_CHECKS.json)
- [Manifesto](../../DIAMANTE_MODULAR_20260916/CONTORSION_HANDOFF_MANIFEST.json)

Não criar gate nem nova função por remissão. O resultado é geométrico condicional, não coeficiente físico universal medido. Memórias locais atualizadas combackup; proposta às canônicas vai pela gerência.
''')
artifacts=[pin(ROOT/name) for name in ('CONTORCAO_FONTE_E_CARGA_REGIONAL.md','REVISAO_CONTORCAO_FONTE.md','verify_contorsion_source.py','CONTORSION_SOURCE_CHECKS.json','record_contorsion_handoff.py')]+[pin(tunnel)]
manifest={'timestamp':NOW,'status':'REVIEWED_CONDITIONAL_GEOMETRIC_SOURCE_MAP',
          'artifacts':artifacts,'memory_appends':memory,'checks':83,
          'canonical_read_scope':'Targeted lines and searches only; no whole-source audit or execution.',
          'new_lean_compilations':0,'canonical_modified':False,'physical_K_beta_derived':False,
          'modular_R1_physical_value_computed':False,'quantum_gravity_solved':False}
atomic(target,json.dumps(manifest,ensure_ascii=False,indent=2))
assert artifacts==[pin(__import__('pathlib').Path(x['path'])) for x in artifacts]
print(json.dumps({'status':'PASS','artifacts':len(artifacts),'memory_backups':len(memory),'checks':83}))
