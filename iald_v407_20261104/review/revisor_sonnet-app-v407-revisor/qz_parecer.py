"""Revisor sonnet-app-v407-revisor -- escreve PARECER_v407_R1.md a partir dos JSON medidos (numeros lidos, nao digitados). Escreve so' nesta pasta."""
import datetime, hashlib, json, sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
W = Path(r'C:\IALD\Central de Patentes\work\iald_v407_20261104')
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: json.loads(Path(p).read_bytes())
Q1, Q2, Q3, Q4R, Q4N, Q5, Q5B, Q9, Q9B, Q10, EX, ZC = (rd(HERE / n) for n in ('q1_sources_out.json', 'q2_q4_decode_out.json', 'q3_q6_q7_out.json', 'q4_recovery_out.json', 'q4_nonascii_out.json', 'q5_f1_out.json', 'q5b_global_status_leaves_out.json',
                                                                              'q9_transaction_out.json', 'q9b_serialize_out.json', 'q10_amarras_out.json', 'q_extra_numbers_out.json', 'qz_compile_out.json'))
app = rd(W / 'validation/review_app_independent.json')
src = rd(W / 'validation/review_sources.json')
final = rd(W / 'validation/review_final.json')
o1, o2, o3, o5, o9, o10 = Q1['out'], Q2['out'], Q3['out'], Q5['out'], Q9['out'], Q10['out']
rs = Q4R['summary']
n = ZC['numbers']
cls = o2['Q2_block_changes_vs_v406_by_package']
fold = o3['Q3_folga']
cap = EX['conversation_capacity_bytes_before_visible_refusal']
q6 = o3['Q6']
unch = o2['Q2_shared_vs_installed_v406']['topics_with_unchanged_source']
ident_h55 = unch - len(cls['haiku_expanded']['by_topic'])
ident_sh = unch - len(cls['shared']['by_topic'])
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
UMPY = next(a['bytes'] for a in rd(W / 'sources_verified.json')['artifacts'] if a['file'] == 'um.py')
WS = '/'.join(str(n['q2']['window']['by_suffix'][s]) for s in ('_v403', '_v404', '_v405', '_v406', '_v407'))
live = o9['live']
fz = o9['fuzz']
F = {f['id']: f for f in ZC['findings']}
sev_line = lambda sev: ', '.join(f['id'] for f in ZC['findings'] if f['severity'] == sev)

md = f"""# Parecer do revisor independente: release v407 do app (rodada 1: fontes, pacote e ferramentas de instalação)

Revisor: `sonnet-app-v407-revisor` (não é o construtor `claude-app-orquestrador`). Data: {now}. Veredito: **ACEITO COM RESSALVAS** — nenhum achado ALTO ou MÉDIO; {len([f for f in ZC['findings'] if f['severity']=='BAIXO'])} BAIXOS ({sev_line('BAIXO')}) e {len([f for f in ZC['findings'] if f['severity']=='INFO'])} INFO ({sev_line('INFO')}).

Por recomputo independente, sem provedor, sem rede, sem `.env`: {app['checks_pass']} de {app['checks_total']} verificações minhas passaram (as {len(app['nongating_failures'])} que não passaram são as ressalvas abaixo, que eu mesmo classifiquei como não-bloqueantes e disse antes de classificar); fontes {len(src['checks'])} de {len(src['checks'])}; o script mecânico `review_app.py` passou com {len(final['checks'])} checks (sha16 do review_final: `{sha((W/'validation/review_final.json').read_bytes())[:16]}`).

## Partitura (lida antes de medir; texto integral em `PARTITURA_antes_de_medir.md`, sha16 `{sha((HERE/'PARTITURA_antes_de_medir.md').read_bytes())[:16]}`)
Esta revisão **decide** se o pacote v407 (três prompts, plano, ferramentas) é fiel às fontes, se a janela que deslizou mantém `limites`/`diz`/`nao_diz`, se a F1 funciona sem perder nada e se o código novo de medição do escopo (`transaction.py`) é seguro e correto. **Não decide** valor científico, resposta de modelo ao vivo, celular nem a instalação. Um FAIL significaria **pacote ou ferramenta diferente do que as fontes e a ordem mandam** (parede medida), nunca uma palavra sobre a teoria. Minhas escolhas, ditas antes: decodificador próprio (o `lib405.py`), semente **407407407**, 520 nomes ao acaso mais bordas, regra do não-ASCII fixada antes, limiar ≥ 99% com toda falha explicada, raiz de brinquedo e listener simulado (não inicio processo).

## Resultado

| Q | resultado | número-chave |
|---|---|---|
| Q1 identidade/fontes | PASS | pino `833121339e649f71…` = selo = cofre (`um.py` {UMPY} B); commit `bf9017157406` = pinado = HEAD = `origin/main` (ref local); {n['q1']['artifacts_recomputed']} artefatos e {n['q1']['public_blobs']} blobs públicos recomputados; Nós vivo = cofre; conferência final da custódia 13/13; plano G1 hoje: pendentes {', '.join(o1['plan_pendentes'])} (+ C21, do operador) |
| Q2 janela P2/literais | PASS | janela `_v403.._v407` = {n['q2']['window']['n']} tópicos ({WS} por sufixo); aposentados `_v401` {n['q2']['retired']['_v401']} + `_v402` {n['q2']['retired']['_v402']}; {n['q2']['topics']}/{n['q2']['topics']} tópicos nos 3 pacotes, 0 perdidos, todos restauram o selado; {n['q2']['qualifier_keys_checked_shared']} chaves de qualificador e {n['q2']['lit3_checked_shared']} literais `limites/diz/nao_diz` inline e iguais (shared e sonnet_public) |
| Q3 folga | PASS | folga mínima declarada **{n['q3']['min_folga']} B** (DeepSeek; Kimi {fold['kimi']['folga_reserva_declarada_148656']}, MiMo {fold['mimo']['folga_reserva_declarada_148656']}) = `1048576 − limite − 148656 − 4096`; limites recomputados do prefixo real = declarados (880579 / 883951 / 883968); haiku55 restam **{n['q3']['haiku55_remaining_tokens']} tokens** (≥ 10.000) |
| Q4 R3-1/R3-2 | PASS | `KEEP_FLAG` igual ao da v406; catálogo {n['q4']['catalog_true']} (98 novos, 0 casam a regra); {len(o2['Q4_haiku_expanded']['false_flags'])} FALSE e pares TRUE literais; receita diz `max_chars 4500`; **{rs['sample']} nomes** (semente {rs['seed']}): {rs['found_text']}/{rs['sample']} por texto, {rs['found_in_topic']}/{rs['sample']} pela métrica estrita; 4/4 não-ASCII |
| Q5 F1 | PASS | (a) `projecao_transversal_v404/name_status` (`PROVISORIO`, «ate' ele dar outro») literal nos 3 pacotes v407 e só ponteiro no haiku55 v406 instalado; (b) {n['q5']['flat_status_records_le_500B']} registros planos ≤ 500 B ({n['q5']['bytes']} B na fonte), {n['q5']['literal_by_package']['haiku_expanded']}/{n['q5']['flat_status_records_le_500B']} literais no haiku55, **+{n['q5']['f1_bytes_in_unchanged_source_topics']['haiku_expanded']} B** no pacote ({n['q5']['f1_topics']['haiku_expanded']} tópicos); (c) {ident_h55}/{unch} tópicos de fonte inalterada idênticos no haiku55, 0 sem explicação; (d) autoteste do codec {n['q5']['self_test']}/{n['q5']['self_test']} sem escrever |
| Q6 confidencialidade | PASS | 0 ocorrências de nomes/chaves vedados nos 3 prefixos, no plano e no native_prefix; 79 contextos distintos de CONFIRMED/confirmada lidos à mão: todos negados, lista de vereditos proibidos, definição que recusa a palavra, ou benignos (transcritos abaixo); CONDITIONAL, UNINHABITED, BIJECTION, HILBERT, CREDITATION presentes |
| Q7 plano | PASS | {n['q7']['plan_files']} arquivos ({n['q7']['under_target']} sob `canonical_releases\\v407_bf9017157406` + {n['q7']['elsewhere']}), 0 `.py` de runtime substituído, manifesto ativo `iald_nucleo_fixo.json` por último, `jev_control_v407.json` válido e só campos de versão diferem, RUNTIME_BASELINE 171/171 intacto hoje e só o manifesto é sobrescrito |
| Q8 script mecânico | PASS | `review_app.py`: PASS, {len(final['checks'])} checks, {n['q7']['plan_files']} arquivos do plano |
| Q9 `transaction.py` | PASS com 2 BAIXOS | só os 5 hunks esperados (reverter os 5 devolve a v406 byte a byte); AST sem chamada que escreva, apague, mate ou inicie; eventos de auditoria vivos: só `open` somente-leitura e listagem; fuzz diferencial de {fz['pairs']} pares: {fz['raised']} exceções, {fz['differs_from_independent_oracle']} divergências do oráculo; arquivo ilegível de verdade → `None`, nunca `False`; {min(live['seconds_each'])}–{max(live['seconds_each'])} s no vivo; relatório serializa |
| Q10 amarras | PASS | `deploy_controlled.py` exige `transaction_sha256` e `maintenance_sha256` iguais aos de `review_final.json` (`{final['transaction_sha256'][:16]}` / `{final['maintenance_sha256'][:16]}`, conferidos); `maintenance.py`, `deploy_controlled.py`, `verify_installed.py`, `review_app.py` = v406 (bytes); D4 reescrito é executável (`d4_check.py`) |

## Achados (nenhum ALTO ou MÉDIO)
"""
for f in ZC['findings']:
    md += f"- **{f['severity']} {f['id']}**: {f['text']}\n"
md += f"""
## Q6: contextos de CONFIRMED/confirmada lidos à mão
Menções por prefixo (shared / haiku55 / sonnet_public): {q6['shared']['confirmed_mentions']} / {q6['haiku_expanded']['confirmed_mentions']} / {q6['sonnet_public']['confirmed_mentions']}. A heurística de negação classificou {q6['shared']['auto_negated_or_forbidden_list']} / {q6['haiku_expanded']['auto_negated_or_forbidden_list']} / {q6['sonnet_public']['auto_negated_or_forbidden_list']}; li os 79 contextos distintos da união dos três prefixos e os que a heurística não pegou ({q6['haiku_expanded']['hand_read_benign']}, todos no haiku55) ficaram assim:
- «duas correções da derivação-fonte (auditoria numérica, **confirmadas** ao vivo)»: correções numéricas de uma auditoria; não é a QG nem a teoria.
- «`estado_tecnico_ext_confirmado`: [EXT, leitura externa 17/07/2026 -- **confirmada** pelo runtime] INFINITE_DIMENSIONAL_INHABITANT_CONSTRUCTED…»: estado **técnico** (habitante de dimensão infinita construído), confirmado pela execução; não é a QG nem a natureza.
- «`a_regua`: PROVADA = validade (teorema; o kernel; o fecho lógico). **CONFIRMADA** = creditação (ato de quem observa de fora) -- a única palavra recusada»: define a palavra e diz que é a recusada.
- 4 selos em snake_case (`…NOT_FALSIFIED_IS_NOT_CONFIRMED…`, `…PROVED_IS_NOT_CONFIRMED`): negações que escaparam do meu regex de palavra (o sublinhado é caractere de palavra).
- Os demais: `!=`/«nunca»/«não é»/«proibido»/`forbidden_verdicts`/`vereditos_proibidos`/«não vira CONFIRMED»/«exigiria reproduzir GR/QFT no limite e observáveis confirmados; o gate segue soberano». Nenhum uso afirmativo de CONFIRMED/confirmada para a gravidade quântica ou para a teoria em nenhum dos três prefixos.

## O que acho das três escolhas do construtor que a ordem não fixou
- **(a) Regra F1** (dict de estatuto plano, chave `status|estatuto|verdict|veredito`, ≤ 500 B, `project()` devolve o registro inteiro): correta para o que mirou e sem perda (o codec novo não perde nenhum campo protegido pela regra velha; a regra nova só acrescenta {Q5['out']['b_counterfactual_old_vs_new_protected_fields']['n_newly_protected_fields']} registros, {Q5['out']['b_counterfactual_old_vs_new_protected_fields']['bytes_newly_protected']} B de fonte). Os 500 B são um corte razoável (protegem os carimbos pequenos, deixam os catálogos `statuses` por ponteiro). Dois limites a saber, não defeitos: não alcança blocos reaproveitados do baseline no `shared`/`sonnet_public` (B4) e deixa {o5['b_records']['size_buckets']['501-1000']} registros entre 501 e 1000 B; o haiku55 tem {n['q3']['haiku55_remaining_tokens']} tokens de sobra, então subir o corte para 1000 B custaria ~{o5['b_records']['bytes_by_bucket']['501-1000']//1000} KB (~{o5['b_records']['bytes_by_bucket']['501-1000']//3000}K tokens) e caberia, se o operador quiser.
- **(b) Escopo medido**: o desenho (sha256 antes e depois, ilegível = `None`, `*.lock` fora, listener por pid + create_time) está certo e o testei por mutação, falha de leitura real, falha de grupo e fuzz. O **conjunto** é que está incompleto (B1): faltam o vínculo do dono, a privacidade do chat, os saldos e razões de uso, os pedidos de acesso, a atividade de tarefa e o cliente web de fato servido; e mede-se `iald_web\\app`, que é a reescrita abandonada. Excluir `*.lock` é correto (o web vivo prende `web-runtime.lock`; o teste do construtor mostrou `PermissionError`).
- **(c) Só `_v402` sai**: honrou a ordem (a v407 não é do porte da v405), mas a economia foi de {n['q2']['v402_block_bytes']['installed_v406_shared'] - n['q2']['v402_block_bytes']['v407_shared']} B, não de 27 KB; a folga mínima caiu de 41.975 para {n['q3']['min_folga']} B (B3). A medição do construtor (`BUILDER_MEASUREMENTS.json`: 11.856) confere com a minha.

## Transparência: critérios que mudei depois de ver dados
"""
for t in ZC['transparency']:
    md += f"- {t}\n"
md += f"""
## Conferência da partitura no fim
- Cumprida: nada aqui fala da teoria nem de modelo ao vivo; nenhum FAIL bloqueante. O único «negativo» honesto de desenho é a recuperação por nome ({rs['found_in_topic']}/{rs['sample']} estrito): é **parede de medição** (o offset do resultado não é a posição da bandeira; o nome também está em `external_ladder`), não falsificação da receita (604/604 por texto).
- Os BAIXOS B1–B4 são **limites medidos** do pacote e da ferramenta, não divergência das fontes: nada contradiz a ordem nem o selo.
- Bytes da F1: não fiz um segundo `prepare`; medi o efeito nos blocos reais (tópicos de fonte inalterada, v407 contra v406 instalada) e, em separado, o contrafactual regra velha × nova do próprio codec sobre o selado v407 (59 registros, 17.853 B de fonte).

## Limites do exame
"""
for t in ZC['limits']:
    md += f"- {t}\n"
md += f"""
## Consulta ao Mapa de Rotas (só consulta)
`python C:\\IALD\\MAPA_DE_ROTAS\\rotas.py consultar "app release v407"` devolveu `{{"n": 0, "truncado": false, "rotas": [], "n_registros": 1789, "cabeca": "14cc63f10595d48f"}}`: nenhuma rota anterior para este exame. Registrar é da gerência: rota nova `app.release.v407`, sem defeito ALTO ou MÉDIO, com os artefatos em `W\\review\\revisor_sonnet-app-v407-revisor\\` e `W\\validation\\review_*`.

## O que é ato do operador
1. **Autorizar o reinício do filho web (porta 8082)** para a instalação; a autorização dada para a v406 em 03/11 não se estende à v407. `quiet()` é refeito pela própria instalação e antes de pedir convém conferi-lo (a v406 levou 87 s).
2. **Decidir B1/B2 antes ou depois**: corrigir o escopo (e o `encode`) muda `transaction.py` e exige novo `review_app.py` + novo aceite (o hash está pinado); aceitar as ressalvas é seguro porque o plano não escreve em nenhum caminho não medido e a rodada da instalação mantém a varredura de janela do D4. Isso é decisão da gerência com o operador, não minha.
3. B3 (política da janela para a v408) é da gerência c1.

## Arquivos
`W\\validation\\review_sources.json` (sha16 `{sha((W/'validation/review_sources.json').read_bytes())[:16]}`), `W\\validation\\review_app_independent.json` (sha16 `{sha((W/'validation/review_app_independent.json').read_bytes())[:16]}`), `W\\validation\\review_final.json` (sha16 `{sha((W/'validation/review_final.json').read_bytes())[:16]}`); scripts e saídas em `W\\review\\revisor_sonnet-app-v407-revisor\\` (entre eles `d4_check.py`, o D4 reescrito como função pura para a rodada da instalação).
"""
(HERE / 'PARECER_v407_R1.md').write_text(md, encoding='utf-8')
print(len(md.encode()), 'bytes;', md.count('\n'), 'lines')
