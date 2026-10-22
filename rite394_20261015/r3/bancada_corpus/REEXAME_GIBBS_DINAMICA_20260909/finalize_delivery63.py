from pathlib import Path
import os,json,hashlib,datetime
root=Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
out=Path(__file__).resolve().parent
build=root/'INTEGRADOR_GIBBS_DINAMICA_20260909_191901_8768394'/'BUILD_SUCCESSOR_20260909_192313_320129'
copydir=root/'COPIA_INTEGRADA_20260909_192248_937671'
auditdir=root/'AUDITORIA_INTEGRACAO_83_20260909'
canonical=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py')
def pin(p):
    b=p.read_bytes();return {'path':p.as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(p):return json.loads(p.read_bytes())
def match(r):return pin(Path(r['path']))==r
def new(p,b):
    assert p.resolve().is_relative_to(root) and not p.exists()
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:
        f.write(b);f.flush();os.fsync(f.fileno())
    assert t.read_bytes()==b
    os.replace(t,p);assert p.read_bytes()==b
def newj(p,value):new(p,(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode())
def link(p,label):return f'[{label}](<{p.as_posix()}>)'
br=read(build/'TRANSPOSED_RESULT.json');plan=read(build/'BUILD_PLAN.json')
assert br['status']=='PASS_TRANSPOSED_SCOPE' and len(br['runs'])==9
assert br['input_boundary_unchanged'] and br['cached_boundary_unchanged'] and not br['um_py_executed']
assert all(r['exit_code']==0 and r['valid'] and r['warning_lines']==0 for r in br['runs'])
assert all(set(a['axioms'])<={'propext','Classical.choice','Quot.sound'} for r in br['runs'] for a in r['axiom_rows'])
assert match(br['plan']) and match(plan['integrated_copy'])
assert len(plan['cached_modules'])==77 and len(plan['modules'])==83
ar=read(auditdir/'AUDITORIA_INTEGRACAO_83.json')
assert ar['status']=='PASS_STATIC_INTEGRATION_SCOPE' and not ar['failed_checks']
assert ar['checks_total']==ar['checks_passed']
assert ar['combined_build_read']['status']=='PASS_TRANSPOSED_SCOPE'
assert ar['combined_build_read']['receipt']==pin(build/'TRANSPOSED_RESULT.json')
assert ar['integrated']==pin(copydir/'um.py')
assert ar['current_canonical']==pin(canonical)
inventory=read(out/'INVENTARIO_SEIS_FONTES.json')
assert all(match(m['source']) and match(m['receipt']) for m in inventory['modules'])
notes={
 'deduction':out/'DEDUCAO_RESPOSTA_E_FRONTEIRA.md',
 'gibbs_realization':root/'REALIZACAO_GIBBS_FATOR_20260909_192042'/'REALIZACAO_MATRICIAL_E_FATORIZACAO.md',
 'gibbs_manifest':root/'REALIZACAO_GIBBS_FATOR_20260909_192042'/'MANIFESTO_REALIZACAO.json',
 'dynamics':root/'DINAMICA_EXTENSIVA_DEMONSTRACAO_20260909_1813'/'DEMONSTRACAO_DINAMICA_EXTENSIVA.md',
 'dynamics_manifest':root/'DINAMICA_EXTENSIVA_DEMONSTRACAO_20260909_1813'/'MANIFESTO_DEMONSTRACAO.json',
 'dynamics_formal_addendum':root/'ANALISE_GIBBS_E_ADENDO_EXTENSIVO_20260909_182817_019674'/'ADENDO_ESTADO_FORMAL_DINAMICA.md',
 'bridge_review':root/'ANALISE_GIBBS_E_ADENDO_EXTENSIVO_20260909_182817_019674'/'ANALISE_MIXED_GIBBS_GRAVITATIONAL_BRIDGE.md',
 'spectral_erratum':root/'NOTA_ESPECTRO_MODULAR_20260909_192614_296855'/'NOTA_ESPECTRO_MODULAR.md',
 'spectral_manifest':root/'NOTA_ESPECTRO_MODULAR_20260909_192614_296855'/'MANIFESTO_NOTA.json'
}
note_pins={k:pin(p) for k,p in notes.items()}
tunnel=root/'TUNEL'/'DO_CHATGPT'
assert not list(tunnel.glob('ENTREGA_063*'))
cp=pin(copydir/'um.py');canonpin=pin(canonical);counts=ar['counts'];delta=inventory['counts']
run_rows=[{'module':r['module'],'exit_code':r['exit_code'],'axiom_audits':len(r['axiom_rows']),'warnings':r['warning_lines']} for r in br['runs']]
receipt={'status':'VERIFIED_INTEGRATED_COPY_AND_REEXAMINATION','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'canonical_unchanged':canonpin,'integrated_copy':cp,'inventory':pin(out/'INVENTARIO_SEIS_FONTES.json'),'joint_compilation':pin(build/'TRANSPOSED_RESULT.json'),'joint_runs':run_rows,'static_audit':pin(auditdir/'AUDITORIA_INTEGRACAO_83.json'),'counts':counts,'delta':delta,'documents':note_pins,'scope':{'um_py_executed_or_imported':False,'canonical_changes':False,'runtime_test_performed':False,'new_physical_gate_or_flags':False,'full_transitive_rebuild':False,'full_transitive_hash':False,'goal_completed':False},'previous_turn_classification':'PROGRESS: constructed and compiled new response-first gravitational bridge and genuine local infinite dynamics limit; current turn completes incorporation and corrects a source-level spectral claim.'}
report=f'''# Reexame atualizado: resposta Gibbs, dinâmica extensiva e correção espectral

9 de setembro de 2026. [REAL — leitura e verificações desta bancada] O original consultado continua com {canonpin['bytes']:,} bytes e SHA-256 `{canonpin['sha256']}`. O índice vivo o identifica como v337. O trabalho abaixo acrescenta resultados em uma nova cópia; não altera a versão canônica.

## O que avançou

Foram incorporadas seis folhas: {delta['theorems']} teoremas e {delta['other_declarations']} outras declarações. A cópia acumula {counts['modules']} módulos de bancada, {counts['theorems']} teoremas e {counts['other_declarations']} outras declarações, total {counts['total']} termos explícitos, incluindo {counts['local_instances']} instâncias locais nomeadas.

- [REAL — Lean] Um protocolo misto fornece probabilidades positivas normalizadas e respostas entrópica e modular iguais na ordem quadrática. A resposta microscópica é calculada antes do tensor T; dez leituras determinam a fonte reconstruída.
- [REAL — Lean] A fonte é conservada sob as equações dos covetores. A mesma informação é transportada pelo seletor. A equação de Einstein decorre quando a correspondência de área especificada é satisfeita.
- [REAL — Lean] A evolução finita foi identificada com sua série de comutadores; a convergência em norma ao limite local foi provada para 2J|t|<1, sem somabilidade global da interação.
- [DERIVED + KNOWN] A realização matricial identifica o protocolo com uma perturbação finita de Araki na mesma torre, preservando a cauda. A demonstração escrita da dinâmica extensiva cobre todo tempo, o fecho C* quase local e o fundo modular; os limites exatos dessa formalização estão no adendo.

{link(notes['deduction'],'Dedução da resposta e da fronteira gravitacional')} · {link(notes['gibbs_realization'],'Realização matricial e fatorização no mesmo estado')} · {link(notes['dynamics'],'Demonstração da dinâmica extensiva')} · {link(notes['dynamics_formal_addendum'],'Adendo sobre o alcance Lean')}.

## O que ainda falta para a suficiência geral pretendida

**1. Correspondência física e área geral.** Métrica, observáveis, covetores e relógio ainda são dados do protocolo. É necessário derivar ou adotar explicitamente a lei que liga esses dados à área das telas geométricas. A conservação e a reconstrução do registro não a implicam: o controle de Minkowski produz T conservado e resposta entrópica não nula com área paralela constante. A lei de área pode entrar como postulado de admissibilidade; nesse caso, a suficiência deve permanecer condicionada a esse postulado. A fundação interna de H3 registrada em v334 não foi tratada como ausente; o que se distingue é sua identificação com a área e o horizonte causal físicos.

**2. Conteúdo e realização do registro selecionado.** O seletor e os decodificadores exatos já recuperam o conteúdo tipado do registro. A aplicação física precisa justificar qual registro é preparado/selecionado, quais informações de ramo e fase são retidas e qual precisão de reconstrução é operacionalmente disponível. A caracterização por um real exato não prova sozinha estabilidade com dados finitos. O protocolo Gibbs também não foi identificado com a dinâmica extensiva por compartilhar vocabulário modular.

**3. Alcance quântico interagente.** A existência da dinâmica quase local avançou substancialmente. Restam a relação dessa cadeia com o espaço-tempo reconstruído, a cobertura dos setores físicos necessários, perturbações gerais, anomalias e a rota contínua/UV. A extensão normal ao fator original exige uma condição adicional: a demonstração escrita apresenta uma interação admissível que não permite essa extensão. Uma representação normal própria de um estado KMS não foi automaticamente identificada com o fator inicial.

Essas obrigações não se confundem com ausência de falsificadores. Eles já existem: o programa registra o piso, os canais de neutrinos e uma condição bilateral para corrida do coeficiente de dephasing com a frequência. A leitura do critério não é uma nova execução do teste. A fonte ainda nomeia explicitamente os programas de anomalias interagentes e UV. {link(Path(canonical.as_posix()+':3232'),'Canais registrados')} · {link(Path(canonical.as_posix()+':146394'),'Critério bilateral de frequência')} · {link(Path(canonical.as_posix()+':127548'),'Programas de alcance geral')}.

## Correção necessária no texto do artigo

[REAL — enunciados lidos; DERIVED — incompatibilidade localizada] Nas linhas 146392/146394, o artigo afirma que o espectro modular é puramente contínuo e não há autovetores. O próprio kernel contém `modularFlow_fixes_omega`, `delta_eigenvector` e `localEigenvectors_total`. Há, portanto, uma família total de autovetores locais, além do vetor de referência fixo. Exterioridade, ausência de período global e continuidade do parâmetro não equivalem à ausência de espectro pontual. Excluir somente Ω não corrige a frase. A errata está registrada para incorporação pela sessão que mantém o programa; nenhum original foi editado. {link(notes['spectral_erratum'],'Nota espectral com âncoras e hashes')}.

## Verificação e entrega

A compilação conjunta terminou com nove processos de saída zero e nenhum aviso. Foram conferidos os 77 módulos anteriores por cache com genealogia e recompiladas seis folhas, a raiz e duas auditorias. O auditor estático passou em {ar['checks_passed']}/{ar['checks_total']} verificações, preservando AST e bytes fora da tabela de arquivos embutidos, sentinelas, flags e gate. As dependências externas transitivas não foram todas recompiladas ou integralmente hashadas.

{link(copydir/'um.py','Nova cópia para incorporação')} — {cp['bytes']:,} bytes; SHA-256 `{cp['sha256']}`.

{link(auditdir/'RELATORIO_INTEGRACAO_83.md','Auditoria estática')} · {link(build/'TRANSPOSED_RESULT.json','Recibo da compilação conjunta')} · {link(out/'RECIBO_CONSOLIDADO_63.json','Recibo consolidado')}.

Nenhum um.py foi executado ou importado. A cópia contém as fontes novas para revisão e incorporação; este trabalho não atesta uma rodada de runtime, um novo selo ou um resultado físico. Atlas e memórias canônicas foram apenas consultados. A sessão que mantém os originais recebe a documentação e a errata pelo túnel.

O resultado é suficiência condicional ampliada e lacunas mais precisamente delimitadas. O objetivo de alcance geral permanece aberto; não há declaração de gravidade quântica resolvida ou confirmada.
'''
new(out/'REEXAME_ATUALIZADO_63.md',report.encode())
newj(out/'RECIBO_CONSOLIDADO_63.json',receipt)
message=f'''# ENTREGA 063 — resposta Gibbs antes da fonte e dinâmica extensiva

Entrega espontânea autorizada no túnel; 09/09/2026. Originais somente leitura.

[REAL — compilação e auditoria] Seis fontes congeladas, {delta['theorems']} teoremas + {delta['other_declarations']} outras declarações. Nova cópia cumulativa: {counts['modules']} módulos, {counts['total']} termos explícitos. Nove processos de compilação PASS, zero avisos; auditoria estática {ar['checks_passed']}/{ar['checks_total']}.

{link(out/'REEXAME_ATUALIZADO_63.md','Reexame e pendências')} · {link(copydir/'um.py','Cópia integrada83')} · {link(out/'RECIBO_CONSOLIDADO_63.json','Recibo consolidado')}.

O protocolo misto (W=X+Z, mediçãoZ, s=v²t², k>0) paga a igualdade entre respostas de entropia e energia de referência na ordem quadrática. A fonte passa a ser calculada da resposta, com conservação por closed/wave; o seletor transporta o registro. A lei física de área e a métrica continuam entradas explícitas. Matriz/GNS/Araki e produto independente estão demonstrados por escrito e distinguidos dos teoremas Lean.

O limite local de interações extensivas passou em Lean. A prova escrita cobre tempo global, fundo modular e KMS no fecho C*. Contém contraexemplo à extensão normal universal ao fator original; não extrapolar a conclusão C*.

Correção prioritária de narrativa: {link(notes['spectral_erratum'],'a afirmação de ausência de autovetores contradiz o próprio kernel')}. A família local de autovetores tem span denso. Corrigir o texto PT/EN nas cópias pertinentes; esta entrega não alterou os originais nem a narrativa embutida da cópia83.

Incorporação: preservar as seis transposições e todas as anteriores; consultar os recibos de escopo. A sessão canônica deverá realizar sua própria integração, rodada pertinente, memória/linhagem e custódia conforme a régua. Nenhum um.py foi executado/importado aqui; não mover gate físico nem converter NOT_FALSIFIED em CONFIRMED. Não houve publicação ou mensagem externa.

SHA-256 da cópia: `{cp['sha256']}`.
'''
target=tunnel/'ENTREGA_063_ESPONTANEA_resposta_Gibbs_dinamica_extensiva.md'
new(target,message.encode())
final={'status':'DELIVERED_063','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tunnel':pin(target),'report':pin(out/'REEXAME_ATUALIZADO_63.md'),'consolidated_receipt':pin(out/'RECIBO_CONSOLIDADO_63.json'),'integrated_copy':cp,'canonical_still_unchanged':pin(canonical)==canonpin,'all_notes_still_unchanged':all(pin(notes[k])==r for k,r in note_pins.items()),'goal_completed':False}
assert final['canonical_still_unchanged'] and final['all_notes_still_unchanged']
newj(out/'RECIBO_ENTREGA_FINAL_63.json',final)
print(json.dumps(final,ensure_ascii=False,indent=2))
