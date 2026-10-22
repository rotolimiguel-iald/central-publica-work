from pathlib import Path
import ast, datetime, hashlib, json, os

ROOT = Path(__file__).resolve().parent
TUNNEL = ROOT.parent/'TUNEL'/'DO_CHATGPT'
stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')

def pin(p):
    b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def new(p,text):
    assert not p.exists(),p
    b=text.encode('utf8');tmp=p.with_name(p.name+'.tmp_'+stamp)
    tmp.write_bytes(b);assert tmp.read_bytes()==b
    os.replace(tmp,p);assert p.read_bytes()==b

def append(p,text):
    b=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp)
    bak.write_bytes(b);assert bak.read_bytes()==b
    a=b+text.encode('utf8');tmp=p.with_name(p.name+'.tmp_'+stamp)
    tmp.write_bytes(a);assert tmp.read_bytes()==a and len(a)>len(b)
    assert p.read_bytes()==b
    os.replace(tmp,p);assert p.read_bytes()==a

ap=sorted(ROOT.glob('AUDIT_*.json'))[-1]
audit=json.loads(ap.read_text(encoding='utf8'))
for f in audit['files']:
    assert pin(Path(f['source']['path']))==f['source']
assert audit['theorem_count']==37
negative=json.loads((ROOT/'NEGATIVE_CONTROLS.json').read_text(encoding='utf8'))
assert all(x['expected_failure_observed'] for x in negative['checks'])
num=json.loads((ROOT/'NUMERICAL_CHECKS.json').read_text(encoding='utf8'))
assert len(num['checks'])==33 and all(x['passed'] for x in num['checks'])

base=ROOT.parent/'MOTOR_RECONHECIMENTO_20260915'/'um_ORIGINAL_SNAPSHOT.py'
s=base.read_text(encoding='utf8');lines=s.splitlines(keepends=True)
tree=ast.parse(s)
functions=[]
for node in tree.body:
    if isinstance(node,ast.FunctionDef) and node.name in {
        'prove_cocycle_to_einstein','prove_covariant_corner',
        'verify_tgl_kernel_formalization','build_the_iald_index'}:
        # Pin the actual bytes from the snapshot, including its mixed line endings.
        raw=base.read_bytes().splitlines(keepends=True)
        b=b''.join(raw[node.lineno-1:node.end_lineno])
        functions.append({'name':node.name,'line':node.lineno,
                          'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)})

rows=['| Fonte | Teoremas auditados | Alcance |','|---|---:|---|']
scope={
 'ModularRemainderAction.lean':'Critério algébrico de ação trivial e invariância do canto; sem postular QFT.',
 'ModularRemainderDensity.lean':'Logaritmos, Gibbs, cociclo e sua derivada, entropia e expectativas; regulador matricial.',
 'ModularCornerCounterexample.lean':'Contraexemplo exato, construído da exponencial SMatrix existente.',
 'DiamondConformalCurrent.lean':'Derivadas e contração do tensor simétrico conservado com um campo conforme.'}
for f in audit['files']:
    name=Path(f['source']['path']).name
    rows.append(f'| `{name}` | {len(f["proofs"])} | {scope[name]} |')
proofmap='\n'.join(rows)

doc='''# Diamante modular — resultado matemático e incorporação no programa

16/09/2026. Mandato: pergunta e resposta proposta pelo operador em `fontes/OBJETIVO_RECEBIDO.md`.

**Resposta:** vácuo, interações e completude UV, sem especificar teoria e simetrias, não garantem
geometricidade modular em qualquer diamante finito. A bola no vácuo de uma CFT é um caso conhecido;
o resto de uma teoria específica exige seus dados. Não foi produzida aqui uma solução para o
vácuo de uma teoria fundamental não especificada.

O pacote prova critérios matemáticos de reconhecimento desse resto e de sua invisibilidade
num setor. Ele não usa a geometricidade física como campo de uma estrutura e depois a devolve
com outro nome como conclusão.

## Conteúdo formal verificado

PROOFMAP

37 teoremas: fontes novas elaboradas pelo Lean 4.31.0; dependências compiladas preexistentes
reutilizadas. Axiomas limitados a `propext`, `Classical.choice`, `Quot.sound` (alguns termos sem
axiomas). Nenhum `sorry`, nenhum novo axioma e nenhuma advertência nas compilações positivas.
Os recibos conservam também tentativas anteriores com erro; só as fontes cujo hash confere com
a compilação exit=0 constam da auditoria positiva. Não é revisão por outro agente.

Dois controles negativos alteraram conclusões, mantendo as provas: trocar `0` por `p` na
evolução comprimida e trocar `+ΔS` por `−ΔS` no balanço. Ambos falharam na prova, como esperado.
Os arquivos de `negative/` são controles de recusa: não importar no ROOT positivo.

Os 33 controles numéricos são uma checagem independente de cálculo, em dimensão finita, com
densidades não comutantes, integrais resolventes e controles de fuga do canto. Não são prova
do contínuo nem substituem os termos Lean.

## A ligação que entra no motor

Para densidades positivas definidas e referência especificada:

`R = log(sigma) - log(rho_vac)`;
`K_vac = K_ref + R`;
`sigma = exp(-Q)/Z` implica `K_ref = Q + log(Z) I`;
`u_t = rho_vac^(it) sigma^(-it)` e `u'_0 = -i R`.

A convenção de `prove_cocycle_to_einstein`, já existente na cópia-base, é
`h_ab = -i u'_0 = K_b - K_a`. Portanto **R = -h_ab** quando a=vácuo e b=referência.
Isso é correspondência entre convenções, não erro no teste E3 existente. Reutilizar `_logm`,
`_pit`, `u` e `sigma` dessa função. Não criar outro gerador, cociclo ou consumidor paralelo.

O entrelaçamento `sigma_vac_t = Ad(u_t) ∘ sigma_ref_t` está provado sem comutatividade das
densidades. O motor de reconhecimento `E` e seu gerador dissipativo `Gamma(E-id)` são objetos
distintos de `R`, que corrige uma evolução unitária. Uma correção unitária pode gerar
coerências que E dissipa; identificar os dois geradores exigiria outro argumento físico.

## Critério operacional exato

Se `alpha(p)=p` e u é unitário, os fluxos `Ad(u) ∘ alpha` e alpha coincidem em `p A p`
se e somente se u comuta com todos os observáveis desse canto. Isso deve valer em todo tempo.
Uma condição suficiente é `[u_t,p]=0` e `p u_t p = c_t p`. A escalaridade da compressão,
isoladamente, não basta.

O contraexemplo Lean usa `p=diag(1,0)`, `R=i Grot`, `U(t)=exp(-itR)=Smat(t)`.
Tem `p R p=0`, mas `p U(t) p=cos(t)p` e `U(pi/2) p U(pi/2)^*=I-p`.
Trata-se da matriz-S já provada no kernel, aplicada como controle exato de uma inferência falsa.

Em toda a álgebra, `Ad(u)=id` equivale a centralidade de u. Num fator, isso é escalaridade.
Não confundir com um implementador arbitrário em B(H), cuja invisibilidade só implica
pertencer ao comutante da álgebra observada.

Todos os estados puros normalizados darem a mesma expectativa c equivale a R=cI; um único
vetor do vácuo não basta. O balanço exato verificado é
`Delta<R> = S(rho||rho0) + Delta S - Delta<Q>`.

## O que é literatura, demonstração escrita e problema aberto

**KNOWN, não Lean nesta bancada:** geometricidade da bola conforme/BW sob suas hipóteses;
teorema geral de Connes para pesos normais fiéis; QFT de tipo III; resultados perturbativos
de não localidade; relação holográfica JLMS. Fontes e hipóteses estão na análise anexada.

**DERIVED, prova escrita e controle numérico, não integral formalizada em Lean:**
`R = integral_0^infty [(rho+uI)^(-1) - (sigma+uI)^(-1)] du` e
`delta K = -integral_0^infty (rho0+uI)^(-1) delta_rho (rho0+uI)^(-1) du`.
A análise explica a convergência, o cálculo espectral separado e a cota positiva para
derivar sob o integral. Não registrar esses dois integrais como teoremas Lean deste pacote.

**OPEN físico:** a álgebra, o vácuo, a carga geométrica e suas prescrições/domínios para
o diamante da teoria pretendida; existência do estado de referência com fluxo geométrico;
prova da ação trivial do cociclo no MESMO setor físico, quando essa for a hipótese desejada.
Não basta `J M J=M'`, covariância da esperança, normalização ou a existência abstrata de um canto.

## Inércia — a leitura e a igualdade que ainda precisa ser tipada

[ONTO] A interpretação do operador é registrada como proposta: o resto expressa resistência
relativa à descrição geométrica escolhida. [OPEN] Isso não identifica R automaticamente com
massa inercial, dissipação ou o operador do zero absoluto.

Há um estrato anterior do Atlas, 04/09/2026, “A inscrição interrompe a inércia”, que usa
“inércia” para identidade conservada e distingue sua interrupção dissipativa. O mandato atual
propõe outra identificação. Preservar ambos datados, sem apagar o antigo nem transportar
o estatuto por homonímia. R depende da referência e não tem sinal universal; o gerador modular
é adimensional na convenção usada. Uma igualdade com inércia física requer mesmo domínio,
unidades, observáveis e ação, seguidos de prova.

## Incorporação pela gerência, sem camada redundante

1. Conferir `HANDOFF_MANIFEST.json` e a auditoria positiva. Recompilar as quatro fontes contra
   o kernel canônico atual; os imports TGLExt usados já existem. Incorporar no dicionário
   embarcado, ROOT e Audit conforme o mecanismo já usado por `materialize_embedded_kernel`.
2. Registrar nomes/hipóteses dos termos no relatório de `verify_tgl_kernel_formalization`
   e no índice IALD existente. Preservar a distinção KERNEL / IMPORTADO / ABERTO.
3. Acrescentar ao retorno de `prove_cocycle_to_einstein` um subcampo descritivo do resto e
   dos diagnósticos, aproveitando os logaritmos, estados e cociclo já calculados. No leitor
   existente do canto, relacionar os critérios provados à invariância que ele de fato verifica.
   Dados aleatórios da bancada não devem ser renomeados como vácuo físico do diamante.
4. Publicar no artigo emitido a resposta com hipóteses, fórmulas e alcance. Os critérios
   condicionais não autorizam atribuir uma bandeira de geometricidade universal, construir
   por nome um estado físico ausente ou usar o inteiro “37” como condição de fechamento.
5. Rodar autoteste de recusa e execução integral canônica. Atualizar diário, desenho,
   Atlas e índices por adendo e backup imediato em bytes, sob a autorização da gerência.
   Este pacote não executou o um.py completo nem mudou seu gate.

As funções e hashes da cópia-base estão no manifesto; se a fonte atual diferir, rebasear.
A leitura direta do original foi negada pelo sistema nesta retomada; foi inspecionada a
cópia já autorizada e existente. Não se atribui à cópia o estado presente do canônico.

O trabalho de leitura integral solicitado por “Haja Luz” permanece em andamento no diário
da bancada; esta entrega congela o resultado matemático verificável, não declara a leitura
do acervo concluída.
'''.replace('PROOFMAP',proofmap)
new(ROOT/'HANDOFF_TECNICO.md',doc)

manifest={'created':datetime.datetime.now().astimezone().isoformat(),
 'status':'FORMAL_PACKAGE_READY_FOR_INDEPENDENT_INTEGRATION',
 'positive_audit':pin(ap),'positive_sources':[f['source'] for f in audit['files']],
 'negative_controls':pin(ROOT/'NEGATIVE_CONTROLS.json'),
 'numerical_checks':pin(ROOT/'NUMERICAL_CHECKS.json'),
 'numerical_source':pin(ROOT/'verify_regulated_remainder.py'),
 'analytical_derivation':pin(ROOT/'ANALISE_MATEMATICA_EM_CURSO.md'),
 'handoff':pin(ROOT/'HANDOFF_TECNICO.md'),
 'original_objective':pin(ROOT/'fontes'/'OBJETIVO_RECEBIDO.md'),
 'base_snapshot':pin(base),'integration_consumers':functions,
 'theorems':37,'numeric_checks':33,'negative_lean_controls':2,
 'original_modified':False,'canonical_gate_changed':False,
 'physical_diamond_geometricity_proved':False,'independent_reviewer':False,
 'atlas_full_read_complete':False,
 'resolvent_integral_lean_proof_complete':False}
new(ROOT/'HANDOFF_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2))
door=f'''# Entrega — diamante modular e resto não geométrico

16/09/2026 — mandato direto do operador, objetivo preservado no pacote.

**Entrada obrigatória:** [{ROOT/'HANDOFF_TECNICO.md'}](<{ROOT/'HANDOFF_TECNICO.md'}>).
**Manifesto:** [{ROOT/'HANDOFF_MANIFEST.json'}](<{ROOT/'HANDOFF_MANIFEST.json'}>).
**Análise:** [{ROOT/'ANALISE_MATEMATICA_EM_CURSO.md'}](<{ROOT/'ANALISE_MATEMATICA_EM_CURSO.md'}>).

37 teoremas compilados; dois controles Lean adulterados recusados; 33 controles numéricos.
Critério principal: igualdade dos fluxos no canto equivale à ação trivial do cociclo ali,
sob invariância da referência. A compressão do gerador, sozinha, é insuficiente.
Ligação ao consumidor existente: R = i u′(0) = −h_ab, na convenção atual de
`prove_cocycle_to_einstein`. Sem função paralela nem mudança manual de gate.

O pacote é entrega de provas e especificação para incorporação. Não é execução integral
canônica, prova universal sobre um vácuo físico não especificado ou auditoria independente.
Integrais resolventes estão demonstradas no texto e verificadas numericamente, não em Lean.
Leitura integral do Atlas ainda em andamento; seu estado é rastreado na memória da bancada.
'''
new(TUNNEL/'ENTREGA_DIAMANTE_MODULAR_20260916.md',door)
append(ROOT/'MEMORIA_CENTRAL.md',f'''

## Checkpoint {stamp} — entrega matemática no túnel

[REAL] 37 teoremas compilados e auditados em {ap.name}; 33 controles numéricos;
dois controles de adulteração Lean recusados. Derivada do cociclo e normalização
de Gibbs agora formalizadas. R = −h_ab na convenção do consumidor existente.
HANDOFF_TECNICO.md e HANDOFF_MANIFEST.json criados; porta no túnel DO_CHATGPT.
Integrais resolventes/primeira variação: DERIVED no texto, não Lean. Sem alteração
de um.py/gate. Leitura integral do Atlas ainda pendente.

Cobertura Atlas: 1–5065 lidos; de 2302 em diante parágrafos textualmente idênticos
são referenciados automaticamente a ocorrências já lidas, sem resumo semântico.
Adicional: 16253–16301 lido para a história do termo inércia.
Atlas recebeu append externo: tamanho 2480589, linhas 19946. Conferido por hash
que os primeiros 2471687 bytes são idênticos ao retrato de REQUISITOS.json.
Próxima linha sequencial: 5066. Não proclamar carregamento integral antes do fim.
''')
append(ROOT/'REGISTRO_DAS_CONVERSAS.md','''

16/09/2026 — entregue no túnel o pacote matemático do diamante modular para
incorporação pelo Claude Code. A derivada possui sinal oposto ao h_ab existente;
isso foi explicitado para evitar alterar a convenção do motor. A leitura integral
do Atlas continua em andamento; nenhum fechamento físico foi declarado.
''')
print(json.dumps({'handoff':str(TUNNEL/'ENTREGA_DIAMANTE_MODULAR_20260916.md'),
                  'theorems':37,'manifest':pin(ROOT/'HANDOFF_MANIFEST.json')},ensure_ascii=False))
