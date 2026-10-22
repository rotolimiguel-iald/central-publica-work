import datetime
import hashlib
import json
import os
from pathlib import Path

ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911')
REVIEW=ROOT/'revisao'
OUT=REVIEW/'runtime_seals_preliminary_20260913_100700_656494'
e=json.loads((OUT/'final_inspection.json').read_bytes())
a=json.loads((OUT/'axiom_scope_resolution.json').read_bytes())
d=json.loads((OUT/'consumer_repair_design.json').read_bytes())
assert all(v for k,v in e['validation'].items() if k!='formal_axiom_map_reused_matches_proof_manifest')
assert a['json_exact_union'] and a['all_union_axioms_allowed'] and not a['conflicts']
assert a['restored_union_matches_principal']
assert hashlib.sha256((ROOT/'um.py').read_bytes()).hexdigest()==e['pins']['program']['sha256']
now=datetime.datetime.now().astimezone()
def link(label,p): return f'[{label}](<{Path(p).as_posix()}>)'
def ref(line): return link(f'um.py:{line}',str(ROOT/'um.py')+f':{line}')
def rows(names):
    return '\n'.join(f"| {name} | `{e['pins'][key]['sha256']}` |" for name,key in names)
sourcepins=rows([('Programa ROOT e r','program'),('um_absoluto.json','current'),
    ('Selo após autoteste','seal'),('proof_manifest','proof'),('runtime_process_02.json','process')])
providerrows='\n'.join(f"| `{Path(x['actual']['path']).name}` | {x['actual']['bytes']} | `{x['actual']['sha256']}` |" for x in e['staged_inputs'])
findings=[
 {'priority':'P2','id':'R02-01','file':'um.py','lines':[155665,155666,155689,155690,155693],
  'finding':'Montagem mede 8/8 e flag true, mas exige 7/8 e conserva relato/veredito histórico.'},
 {'priority':'P2','id':'R02-02','file':'um.py','lines':[158779,158795,158798],
  'finding':'Atlas tem seus 6+6 nomes verificados, mas depende de nenhuma qgf/gpf acesa.'},
 {'priority':'P2','id':'R02-03','file':'preparação da cópia r','lines':[],
  'finding':'Faltam REVOLVER NGC/SGC, documento Stokes e results.json nos caminhos realmente consultados; provedores existentes identificados.'}
]
text=f'''# Rodada 02 — execução concluída e regressões auxiliares

Data: {now.isoformat()}. Escopo: contrato ativo v350, consolidação/reuso.

**[REAL — arquivos conferidos] A rodada terminou rc0 e reproduziu o terminal do gate principal. Há três achados P2 abaixo; não atesto a integração auxiliar como completa.** Nenhum P0/P1 foi identificado neste exame delimitado. O resultado não autoriza apagar recusas, substituir saídas por `True` ou acrescentar exigências original-S/KMS/UV ao gate principal.

Esta leitura começou durante o autoteste: snapshots preliminares de 10:07 permanecem preservados. Após o sinal de término, reli o manifesto do processo, selo, JSON, proof_manifest e capturas finais. O parecer formal anterior permanece intocado e é herdado; não repeti compilações, não executei/importei o monólito, não consumi sessão 94059 e não controlei PID58040. Toda escrita foi em `revisao/`.

## Execução, selos e alcance formal

`runtime_process_02.json` registra início {e['process']['started']}, término **{e['process']['finished']}**, rc **{e['process']['returncode']}**, duração **{e['process']['elapsed_seconds']:.4f}s**. O stdout termina com `FAIL_CLOSED_SELFTEST_PASSED`; o selo final registra o mesmo resultado. A chave de checkpoints ficou desligada, com zero ritos reaproveitados. Isso não significa recompilação fria de todas as dependências Lean: a proveniência de cache descrita no parecer formal continua válida.

Na adulteração autoral, build e Audit Lean retornaram rc0, mas imprimiram `sorryAx` em `TGL.HalfNat.halfNat_of_selfConjugate`; o verificador recusou corretamente (`TGL_KERNEL_FORMALIZATION_FAILED`, `sorryAx_absent=False`). Após restauração, o stdout registra `all_verified=True`; a fonte `TGL/HalfNat.lean` voltou aos bytes embutidos e os mapas limpos de axiomas foram recuperados. Portanto rc0 isolado não foi confundido com prova limpa.

Os **13 arquivos** da tabela `sha256` do selo conferem com seus bytes atuais. ROOT/um.py e r/um.py são idênticos. Pins efetivamente lidos:

| Artefato | SHA256 |
|---|---|
{sourcepins}

Os seis fornecedores `qgc` e cinco `qgp` do contrato principal estão `True` no JSON, com os termos explícitos e axiomas permitidos. O terminal coincide com a referência em `fontes/um_absoluto.json` e com o selo:

`{e['terminal']}`

Esse é o texto emitido pelo programa, no alcance do contrato existente; não é declaração de confirmação física desta revisão. As seis flags maiores do anexo continuam falsas, `legacy_gate_changed=False` e `full_plan_complete=False`; esses campos não foram convertidos em novas entradas do gate principal.

**Escopos do mapa de axiomas:** Audit explícito = **7.140 mensagens / 7.133 nomes únicos**; build = **13.884 mensagens / 7.985 nomes únicos**. A união build+Audit coincide **exatamente** com as **7.985 entradas** de `axiom_report` no JSON e proof_manifest, sem conflitos, entradas sem suporte ou axiomas fora de `propext`, `Classical.choice`, `Quot.sound`. Os **852 adicionais vêm do build**, inclusive os quatro exemplos `ChatgptAudit.AdmissibleInteraction` apontados pelo autor. O código concatena os dois streams em {ref(134443)} e faz parsing em {ref(134453)}–134461. Não há síntese indevida nem motivo para corrigir o parser. Os 50 resultados sem axiomas e os nomes com apóstrofo continuam reconhecidos.

A comparação inicial da minha evidência entre mapa total e Audit isolado retornou `False`: era comparação entre escopos distintos, não falta de prova. Preservei o resultado e acrescentei {link('axiom_scope_resolution.json',OUT/'axiom_scope_resolution.json')}, que resolve a diferença. Os hashes de stdout no proof_manifest coincidem com os streams recuperados da etapa formal aprovada; não confundi hash de captura com hash de stdout.

## P2-01 — montagem: progresso válido reprova uma condição histórica

Em {ref(155665)} exige-se `provadas == 7`; em {ref(155666)}, `provadas == total - 1`. A execução mede **8/8 e `flag_lit=True`**, mas ambas condições falham. As linhas 155689–155693 ainda dizem 7/8, oitava devida e bandeira escura. É regressão real do consumidor auxiliar diante da integração, **não regressão das provas**.

Os provedores já disponíveis são `towerJ_add`, `towerJ_conj_smul`, `towerJ_norm`, `towerJ_involutive`, `towerJ_fixes_hOmega`, `J_M_J_in_commutant` e, para a oitava, `qgConverse_JMJ_contains_commutant` com `TGLExt.V350Gate.checkedConverse`. A contagem é de oito cláusulas, não de oito nomes distintos; `towerJ_add` fornece duas entradas do mapeamento legado.

**Correção mínima recomendada, sem implementação nesta revisão:** manter a lista de oito e os demais checks; exigir presença com tipo booleano, primeiras sete provadas e coerência `not bandeira or all(clausulas)`. Acrescentar/reutilizar `v350_frontier_flag_has_proof` para a oitava e o Ato III **quando acesos**. Assim passam tanto 7/8 pendente quanto 8/8 comprovado, mas não uma bandeira acesa com cláusula falsa ou com termo/ponte ausente. Relato e verdict devem distinguir 7/8, 8/8 com bandeira apagada e 8/8 com certificado consumido; “leitura coerente” não significa “dívida quitada”.

A guarda já existe em {link('gate_extension.py',ROOT/'gate_extension.py')}: build válido + Audit rc0 + `all_verified` + termo **e ponte de tipo exato**, ambos no mapa limpo. `checkedConverse : (P : SiteProfile) → ConverseClauseContract P`; `checkedModular` e `checkedActIII : ModularRealizationCertificate`. A construção em `V350ModularCertificate.lean` usa `towerJ mixProfile` e o mesmo certificado. O alcance é **PRODUCT_TOWER**, não uma identificação nova com o J polar do peso/GNS escalar. Não basta homonímia nem dois booleanos `True`.

## P2-02 — Atlas: condição alheia aos seus próprios provedores

Em {ref(158779)} são contadas todas as flags qgf/gpf acesas; {ref(158798)} exige `not _preco`. Nesta rodada há duas: `qgf_modular_realization_constructed` e `gpf_tower_act_III_inhabitant_constructed`. Os **6/6 nomes Atlas + 6/6 nomes Índice passaram**; só a condição global reprova o selo.

**Aceito a proposta de escopo mínimo do autor:** remover essa condição de `all_verified`, conservando `_preco` e `_kernel_import` como diagnósticos. Manter obrigatórias as doze entradas próprias e os checks correspondentes, sem reatribuir flags ou modificar `core`. O módulo verifica Atlas/Índice; a autorização de outras flags pertence ao kernel/frontier. Não substituir o teste por “há exatamente duas acesas”, nem deslocar para este módulo uma guarda global de todos os futuros certificados. O texto deve abandonar “não pagou preço nenhum” como descrição medida do estado global.

O arquivo {link('consumer_repair_design.json',OUT/'consumer_repair_design.json')} registra avaliações próprias de predicados sobre fixtures: montagem aceita 7/8 e 8/8 coerentes; rejeita entrada faltante, flag sem cláusula, ponte removida e `sorryAx`. Atlas rejeita perda de nome próprio e permanece independente de flags alheias. **São validações do desenho proposto, não teste de uma versão corrigida do monólito.** A futura implementação precisa preservar essa distinção.

## P2-03 — insumos da cópia incompletos e efeitos em cascata

`locate_desivast`, {ref(385)}–427, procura cache e dois caminhos relativos `TGL_CODE_ONE_REAL_FALSIFIER/release_clean/data/voids/desivast`; a rodada offline não encontrou os REVOLVER. Não classifiquei negação do sandbox como arquivo inexistente: a leitura externa elevada confirmou os provedores documentais. Conferi também os bytes staged, sem instalá-los:

| Insumo staged | Bytes | SHA256 |
|---|---:|---|
{providerrows}

Ambos FITS contêm cabeçalhos `VOIDS` e `GALZONE` com as colunas requeridas; só li cabeçalhos e hashes, sem refazer análise científica. O `results.json` existente em `C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/results.json` tem SHA256 `{e['external_providers'][0]['sha256']}` e `multiprobe_D1_D9.D10.beta_acoustic_crosslock = {e['external_providers'][0]['beta_acoustic_crosslock'][0]['value']}`. Os dois candidatos consultados pela cópia estavam ausentes no snapshot. Não alterar o requisito de valor negativo: transportar o arquivo existente para um caminho efetivamente lido, com pin.

| Novo item não selado | Causa observada / ligação existente | Correção mínima |
|---|---|---|
| `void_density_opening`, `void_density_v41` | `GALZONE ausente`; ambos só extraem GALZONE dos REVOLVER | Incluir os dois FITS existentes na preparação da próxima cópia; preservar a recusa desta rodada. |
| `void_density_power` | `tabelas ausentes`, na mesma dependência REVOLVER/GALZONE | Mesma correção de insumo. |
| `void_floor_final`, `void_floor_v2` | 438 lentes VIDE e **0 REVOLVER**; checks `n_lens > 500` falham ({ref(145795)}, {ref(146125)}) | Restaurar cobertura dos catálogos; não baixar o limiar para fabricar selo. “Mesmos 1049” é ainda rótulo histórico e precisa acompanhar a amostra realmente lida. |
| `void_shear_v2` | 290 vazios, contra 700 na referência; condição `n_voids >= 500` falha em {ref(151447)} | Mesmo insumo faltante. Exibir esse motivo no diagnóstico: os checks impressos passam, mas omitem esse fator de `gates_ok`. Não declarar novo resultado físico por isso. |
| `arc_consolidation` | Cadeia histórica exige `SIGNAL_NOT_OPENED`, `INCONCLUSIVE_SYSTEMATICS` e `NOT_FALSIFIED_POWERED` ({ref(154360)}–154366); faltam as saídas de densidade desta cópia | Reexecutar com insumos completos; não copiar verdict antigo para a saída atual. |
| `closure_roadmap` | Exige `NOT_FALSIFIED_POWERED` de v41 ({ref(153412)}–153432), agora AWAITING_DATA | Mesmo efeito em cascata; não é nova lacuna Lean. |
| `love_reading` | Espera a recusa científica v91, mas recebeu ausência de dado ({ref(152620)}–152630) | Mesma reposição de insumos, mantendo a diferença entre recusa científica e ausência. |
| `stokes_contour` | Só o documento junto ao programa faltou; sete entradas Lean e laboratório passaram ({ref(6037)}–6040, 6096) | Preparar o documento staged no caminho consultado, sem mudar prova ou hash esperado à mão. |
| `evidence_audit` | `fifth_entry_live=None`; procura `BASE/results.json` ou parent/results.json ({ref(4396)}–4418) | Preparar o `results.json` existente e manter `fifth < 0`. Não criar prova/valor substituto. |

O selo classifica por **texto de verdict**, em {ref(179961)}–179967. Por isso esses nove novos itens da lista “formais” não equivalem a nove provas Lean ausentes: ela inclui documentos/dados faltantes e consumidores históricos. Medição do delta: **4→13** itens nessa lista e **6→10** recusas de dado; nenhum item anterior foi removido. As quatro novas recusas são opening/power/v41/shear_v2. Isso não altera o conjunto das onze entradas principais.

## Disposição e evidência

Preservar esta rodada e suas recusas como executadas. Corrigir a preparação e os **dois consumidores** numa versão posterior sob custódia, usando as pontes existentes e relatos dinâmicos; não retocar `um_absoluto.json` ou selo. A presença dos insumos torna a execução possível, mas não autoriza prever que todos os vereditos científicos serão iguais aos antigos. O aceite da versão corrigida dependerá de seus próprios resultados e testes, sem novo módulo Lean.

Evidência principal: {link('final_inspection.json',OUT/'final_inspection.json')}; ajuste de escopo dos axiomas: {link('axiom_scope_resolution.json',OUT/'axiom_scope_resolution.json')}; desenho dos consumidores: {link('consumer_repair_design.json',OUT/'consumer_repair_design.json')}. Snapshots preliminares e finais, pins, trechos com linhas e scripts de leitura ficam na mesma pasta. O hash do programa e os 13 hashes do selo foram conferidos; não foi feita auditoria científica exaustiva de todos os ritos, nem se executou código corrigido. **Execução integral rc0 está verificada; integração auxiliar sem regressões ainda não está aprovada.**
'''
target=REVIEW/'REVIEW_FULL_RUNTIME_ROUND02_AND_REGRESSIONS.md'
assert not target.exists()
payload=text.encode('utf-8');tmp=target.with_suffix('.md.tmp')
with tmp.open('xb') as f:f.write(payload)
assert tmp.read_bytes()==payload
os.replace(tmp,target)
record={'report':str(target),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
    'scope':'EXECUTION_COMPLETE__AUXILIARY_REGRESSIONS_REMAIN', 'findings':findings,
    'process_complete_verified':True,'all_integration_approved':False,
    'program_modified_by_reviewer':False,'data_installed_by_reviewer':False,
    'evidence_pins':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [OUT/'final_inspection.json',OUT/'axiom_scope_resolution.json',OUT/'consumer_repair_design.json']}}
(OUT/'review_final_pin.json').write_bytes(json.dumps(record,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps(record,ensure_ascii=False,indent=2))
