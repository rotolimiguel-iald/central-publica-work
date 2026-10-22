import pathlib,json,hashlib,datetime,os
ROOT=pathlib.Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911');REV=ROOT/'revisao';RUN=REV/'reuse_contract_audit_20260913_080142_579115'
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(pathlib.Path(p).read_bytes())
def link(p,label,line=None):return f'[{label}](<{pathlib.Path(p).as_posix()}{":"+str(line) if line else ""}>)'
now=datetime.datetime.now().astimezone();stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def atomic(p,b):
 assert p.is_relative_to(REV)
 if p.exists():
  old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp);bak.write_bytes(old);assert bak.read_bytes()==old;b=old+b'\n\n'+b
 t=p.with_name(p.name+'.tmp_'+stamp);t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
d=read(RUN/'independent_verification.json');a=read(ROOT/'AUDITORIA_REUSO_GATE_20260913/gate_evidence.json');m=ROOT/'AUDITORIA_REUSO_GATE_20260913/MAPA_GATE_E_REAPROVEITAMENTO.md';ge=ROOT/'gate_extension.py'
for p,h in d['pins'].items():
 if p in [str(ROOT/'um.py'),str(ge),str(ROOT/'AUDITORIA_REUSO_GATE_20260913/gate_evidence.json')]:assert sha(p)==h
limits={
'TGLExt.qgStrongCertificate_core':'Σ de rede PhysicalNetData e fibra infinita: theTailNet.',
'TGLExt.qgStrongCertificate_corner':'Σ de Dirac genuinamente ilimitado e dimensão do núcleo positiva/finita: theGenuineDirac.',
'TGLExt.qgStrongCertificate_frame':'Σ de SmoothFrameData não constante: theCurvedFrame.',
'TGLExt.qgStrongCertificate_solder':'Σ de SolderFieldData com métrica não constante.',
'TGLExt.qgStrongCertificate_einstein':'Σ de EmergentEinsteinData, equação no ansatz, curvatura não nula, determinante negativo e métrica não constante.',
'TGLExt.qgClosureCertificateV2':'FullWitnessDataV3 := theWitnessV3; reduz à testemunha fundida e ao fator mixProfile. Não é FullTGLWitness.',
'TGLExt.qgPhysicsCertificate_massless':'Onda plana C², simetria/TT, solução de vácuo e não trivialidade ⇒ covetor nulo.',
'TGLExt.qgPhysicsCertificate_helicities':'Decomposição TT no cone padrão em duas coordenadas físicas e gauge; invariância dessas coordenadas.',
'TGLExt.qgPhysicsCertificate_ghostfree':'Cinética do representante físico ≥0, estrita sob não trivialidade.',
'TGLExt.qgPhysicsCertificate_conservation':'Bianchi no símbolo linearizado para polarização simétrica.',
'TGLExt.qgPhysicsCertificate_anomaly':'Invariância de gauge do símbolo de Ricci clássico-linear; não uma afirmação irrestrita sobre anomalias quânticas.'}
rows=[]
for x in d['entries']:
 s=x['source'];rows.append(f"| `{x['flag']}` | `{x['declaration']}` | {link(s['file'],pathlib.Path(s['file']).name,s['line'])} | True — {limits[x['declaration']]} |")
doc=f'''# Auditoria de escopo e reutilização — gate v350

{now.isoformat(timespec='seconds')} · AUDITORIA_REUSO_J_ORIGINAL_GATE · somente leitura e saídas em revisao.

**Conclusão:** [REAL — código e evidências existentes conferidos] as onze entradas Lean do gate principal estão verdadeiras e já ligadas aos termos consumidos. **Não identifiquei pendência matemática intrínseca ao contrato desse avaliador.** O mapa documental está correto nesse ponto. Exigir a inclusão inversa pelo J do peso regular, KMS desse peso ou outros objetivos adicionais para conservar o resultado do gate principal ampliaria o contrato implementado. A rota adicional foi suspensa, conforme ordem; não se propõe novo arco de provas.

Não há P0–P2 pendente nas ligações verificadas. A falha de escopo identificada é do processo: confundir objetivos da fronteira/rota adicional com entradas ainda não satisfeitas do avaliador principal. Isso não invalida os lemas anteriores, nem demonstra que as duas realizações matemáticas sejam iguais.

## O que foi efetivamente conferido

Li integralmente {link(m,'MAPA_GATE_E_REAPROVEITAMENTO.md')}, gate_evidence.json, gate_extension.py e o script autoral audit_existing_gate_reuse.py. Fiz extração própria do AST da cópia e dos mapas de nomes; conferi as onze fontes/linhas e seus bytes embutidos, suas hipóteses relevantes, os flags na evidência corrente e na base histórica. Reparseei o stdout corrente de Audit: **{d['current_audit_entries']} declarações**, mapa igual ao axiom_report, onze termos com apenas propext/Classical.choice/Quot.sound. Conferi rc0, fonte e binário do registro Audit e seus hashes, sem reconstruir a biblioteca.

O avaliador em {link(ROOT/'um.py','um.py',d['gate_line'])} lê exatamente seis chaves de `formal`, cinco de `physics` e quatro de `experiment`. O chamador, linhas 161541–161563, preenche os dois primeiros dicionários por qgc_/qgp_, o terceiro pelo experiment_feed, chama o avaliador e só depois anexa `kernel_frontier`. **qgf_/gpf_ não são entradas do principal.** A inspeção não executou/importou um.py nem scripts autorais.

| Entrada consumida | Termo efetivo | Fonte/linha | Valor e alcance do tipo |
|---|---|---|---|
{chr(10).join(rows)}

A ligação existente é `fonte embutida → Audit → _QG_CERTIFICATE_FLAGS/_QG_PHYSICS_FLAGS → qgc_/qgp_ → avaliador`. As leituras Python históricas usam presença do nome, build e axiomas admitidos; não provam nem reinterpretam o tipo pela grafia do flag. Nesta auditoria os fornecedores concretos foram localizados e seus enunciados conferidos. Não é necessário reconstruí-los para satisfazer essas mesmas entradas.

## Fronteira separada e literais

Em gate_extension.py, `_V350_MODULAR_CONTRACTS` relaciona somente três flags a termos e pontes Lean de tipo exato: `red_clause_JMJ_contains`, `qgf_modular_realization_constructed` e `gpf_tower_act_III_inhabitant_constructed`. Os termos `qgFrontier_modularRealization` e `qgPrice_towerActIII_inhabitantConstructed` têm tipo `ModularRealizationCertificate`; `checkedConverse`, `checkedModular` e `checkedActIII` são as pontes consumidas. Estão auditados e verdadeiros. O certificado fala de WH=TowerHilbert mixProfile, theFactorObject/commAlg, e é preenchido pelo towerJ concreto: não por uma isometria J arbitrária. Seu escopo declarado é PRODUCT_TOWER__J_M_J_EQUALS_COMMUTANT.

Os seis flags adicionais false são três qgf_ (`unconditional_continuous_corner_proved`, `continuous_modular_realization_constructed`, `full_TGL_witness_constructed`) e três gpf_ (H1/H2/H3). A mecânica histórica reserva nomes para eles; não encontrei termos desses seis nomes nem novas pontes exatas em gate_extension. `FrontierCertificate.lean` distingue o contrato modular tipado das outras reservas puras. Os tipos legados `ContinuousCoreData`, `ThreeLocksCoreData`, `TGLModularRealization` e `FullTGLWitness` existem, mas não devem ser confundidos com `FullWitnessDataV3`, já consumido pelo principal. Essa distinção **não cria uma dependência nova do principal**. KMS/original-S/UV não aparecem automaticamente como campos obrigatórios desses contratos legados; os dados e equações expressamente escritos são o contrato.

**`full_plan_complete=False` e `legacy_gate_changed=False`, no retorno de evaluate_v350_kernel_frontier, são literais.** Não são testes de novas provas, nem certificados de impossibilidade matemática. Acrescentar lemas não muda esses literais. Analogamente, `full_static_witness_exists=False` é constante do avaliador principal, não uma entrada pendente ou quinto degrau. O texto `remaining` é uma lista descritiva da fronteira, sem poder de veto sobre o veredito principal. Não se alterou nenhum desses campos nesta auditoria.

## Confronto com a auditoria autoral

Confirmei por inspeção do script e dos resultados a coerência das onze ablações individuais e das 256 combinações de oito qgf_/gpf_. **Essas execuções foram do autor; não as reexecutei.** A extração própria das chaves realmente lidas confirma, independentemente, a irrelevância dessas oito chaves extras para o avaliador. O script autoral executa apenas a definição isolada extraída por AST; isso não equivale à execução do monólito.

O inventário autoral declara 50.571 fontes externas lidas, 1.281 hashes distintos, zero falhas, 29.524 caminhos associados a 398 módulos embutidos. Conferi a aritmética dos grupos e amostras dirigidas, **não reli os 50.571 arquivos**. Dezesseis dos vinte módulos selecionados tiveram correspondência externa literal verificada; os três módulos antigos ModularPower/ModularFlowSpectrum/ModularSquare tiveram comparação adicional por cabeçalho/imports, registrada separadamente. Os onze fornecedores do gate estão em apenas cinco arquivos, também encontrados byte a byte em `C:/IALD/Central de Patentes/Chatgpt/fontes/tgl_kernel/TGLExt/`: StrongAssembly, SolderField, EmergentEinstein, TheCoinage e PhysicsCertificates. Isso é evidência positiva de reaproveitamento já realizado.

A normalização do inventário retira material anterior ao primeiro import e ajusta CRLF/espaços externos; não demonstra equivalência semântica de fontes distintas nem conta cópias como provas novas. Minha busca inicial dirigida encontrou recusas de acesso em diretórios de pacotes Python externos ao recorte Lean; seus resultados brutos foram preservados. Portanto **não afirmo busca exaustiva nem inexistência global de fornecedores equivalentes**. A investigação mais ampla sobre identidade de J/KMS ficou interrompida por ordem explícita. Os exemplos modulares examinados têm seus objetos e hipóteses próprios; não os promovo a provas sobre o J do peso escalar regular.

## Estatuto do resultado e limites

O resultado do avaliador isolado constante de gate_evidence coincide com o gate da base histórica e com gate_tests: os níveis matemático, físico e experimental internos retornam True, com `full_static_witness_exists=False` e o veredito literal `{a['gate_result']['verdict']}`. Esse é **o resultado escopado do código com os dados registrados**, não uma confirmação física independente.

Os quatro indicadores experimentais foram relidos de fontes/um_absoluto.json e são históricos; não houve novo experimento. A compilação/Audit é incremental, com dependências herdadas, não uma nova reconstrução integral. Full runtime permanece não executado. Esses limites de evidência não são novos teoremas necessários para o gate. Não é possível converter esta leitura em atestado de uma execução integral nova.

A verificação própria confirmou a preservação do original e dos 34 pins da custódia mãe. Nenhuma memória, fonte, integração, flag, recorder ou parecer selado foi modificado. O DEV14 anterior está concluído separadamente; módulos não congelados e os demais módulos DEV novos não foram compilados nem certificados por esta auditoria. Nenhuma nova integração é proposta.

## Pins e trilha verificável

- Cópia: `{d['pins'][str(ROOT/'um.py')]}`.
- Custódia mãe paired_blocks: `{d['pins'][str(ROOT/'paired_blocks_custody.json')]}`.
- Mapa documental lido: `{sha(m)}`.
- gate_extension.py: `{sha(ge)}`.
- gate_evidence.json: `{sha(ROOT/'AUDITORIA_REUSO_GATE_20260913/gate_evidence.json')}`.
- external_source_reuse.json: `{sha(ROOT/'AUDITORIA_REUSO_GATE_20260913/external_source_reuse.json')}`.
- Base experimental/fontes: `{d['pins'][str(ROOT/'fontes/um_absoluto.json')]}`.
- Audit corrente: {link(d['current_audit_log'],'log rc0')}; seu stream é o pin atual da mãe, não metadado histórico substituído por presunção.
- {link(RUN/'independent_verification.json','Verificação própria')} contém hashes, onze linhas, chaves efetivas do AST, amostras e alcance; {link(RUN/'extra_modular_source_comparison.json','comparações modulares selecionadas')} preserva os limites das amostras. Um erro inicial do parser próprio não reconhecia apóstrofo em nome Lean; corrigido, o mapa completo de 7.133 coincidiu. Não é falha das provas ou do Audit autoral.

**Encerramento:** ligação/escopo conferidos. Nenhuma obrigação matemática adicional identificada para o gate principal existente; nenhuma aprovação de objetivo mais amplo inferida. Pesquisa ampliada suspensa e não apresentada como concluída.
'''
p=REV/'AUDITORIA_REUSO_J_ORIGINAL_GATE.md';atomic(p,doc.encode('utf-8'))
pin={'timestamp':now.isoformat(),'report':str(p),'sha256':sha(p),'bytes':p.stat().st_size,'scope':'EXISTING_GATE_CONTRACT_AND_REUSE_EVIDENCE_ONLY','main_gate_missing_mathematical_input_identified':False,'additional_search_exhaustive':False,'new_compilation':False,'new_runtime':False,'author_memory_recorder_executed_by_reviewer':False,'map_sha256':sha(m),'own_verification_sha256':sha(RUN/'independent_verification.json')}
atomic(RUN/'scope_report_pin.json',json.dumps(pin,ensure_ascii=False,indent=2).encode('utf-8'));print(json.dumps(pin,ensure_ascii=False))
