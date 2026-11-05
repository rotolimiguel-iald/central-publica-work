"""Revisor sonnet-app-v407-revisor -- RODADA 2: compila os resultados MEDIDOS (r2_*.py) em validation/review_deploy.json e no PARECER_v407_R2.md. Numeros LIDOS dos JSON de saida.
Escreve so' em validation/review_deploy.json (modo 'x') e nesta pasta."""
import datetime, hashlib, json, sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
W = Path(r'C:\IALD\Central de Patentes\work\iald_v407_20261104')
ACTOR = 'sonnet-app-v407-revisor'
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: json.loads(Path(p).read_bytes())
now = datetime.datetime.now(datetime.timezone.utc)
D16, SC, D5, D9, EX, D4F = (rd(HERE / n) for n in ('r2_d1_d6_out.json', 'r2_d4_scope_out.json', 'r2_d5_out.json', 'r2_d9_out.json', 'r2_extra_out.json', 'r2_d4_function_out.json'))
c = D16['checks']
dep = rd(W / 'deployment.json')
sm = dep['scope_measurement']
rf = rd(W / 'validation/review_final.json')
T = SC['tempos']
rm = SC['re_medicao']
jan = SC['janela_estrita_resultado']
pos = SC['mudancas']['pos_janela (depois de restart.json)']
b1 = SC['B1_19_caminhos']
n5 = D5['checks']
srv = n5['servicos_nao_reiniciados']
ev_hash = D16['hashes_das_evidencias']
submit = rd(W / 'receipts/v407-deploy-submit.json')['task']['evidence']
unchanged_submitted = all(sha((Path(e['path'])).read_bytes()) == e['sha256'] for e in submit)

# ------------------------------------------------------------------ D4 composto
d4b_ok = (not jan['outros_(achados)'] and jan['no_plano'] == 1782 and jan['backups'] == 7 and jan['n_logs'] == 3 and SC['plano_mtimes']['todos_dentro_da_janela_estrita'] and not SC['backups_orfaos_com_o_carimbo_da_instalacao']
          and SC['mudancas']['pre_janela (deploy_stderr..maintenance.json)']['total'] == 0 and not SC['varredura']['truncada_por_tempo'] and not SC['varredura']['podou_algo']
          and all(v['posicao'] == 'FORA, ANTES (inalterado)' and v['mesma_contagem_da_rodada_1'] and v['plano_escreve_dentro'] is False for v in b1.values()) and len(b1) == 19 and D4F['PASS'])
d4c_ok = (dep['accounts_modified'] is False and dep['bench_restarted'] is False and dep['client_files_changed'] is False and not sm['errors'] and sm['state_aggregate_before'] == sm['state_aggregate_after'] and sm['client_aggregate_before'] == sm['client_aggregate_after']
          and not sm['bench_changed'] and not sm['state_changed'] and not sm['client_changed'] and not sm['state_unreadable'] and not sm['client_unreadable'] and not sm['plan_overlap_before'] and not sm['plan_overlap_after']
          and rm['cliente']['igual_ao_after'] and rm['estado']['igual_ao_after'] and rm['estado_por_posicao'] == {'antes': 120, 'pre_janela': 0, 'dentro': 0, 'depois': 0} and not rm['cliente_modificados_desde_o_inicio_do_deploy'])
D4 = {'PASS': bool(c['D4a']['PASS'] and d4b_ok and d4c_ok), 'a_baseline_e_manifesto': c['D4a'], 'b_varredura_de_janela': {'PASS': bool(d4b_ok), 'tempos': T, 'varredura': SC['varredura'], 'janela_estrita': jan, 'pos_janela': {'total': pos['total'], 'arquivos': pos['logs']}, 'plano_mtimes': SC['plano_mtimes'], 'funcao_d4_check_da_rodada_1_na_producao': D4F},
      'c_escopo_medido': {'PASS': bool(d4c_ok), 'deployment_json': {k: dep[k] for k in ('accounts_modified', 'bench_restarted', 'client_files_changed')}, 'scope_measurement_resumo': {k: sm[k] for k in ('state_files', 'state_bytes', 'state_aggregate_before', 'state_aggregate_after', 'client_files', 'client_bytes', 'client_aggregate_before', 'client_aggregate_after', 'bench_changed', 'errors', 'seconds_before', 'seconds_after')},
                          'remedicao_propria': rm}}
checks = {'D1': c['D1'], 'D2': c['D2'], 'D3': c['D3'], 'D4': D4, 'D5': D5, 'D6': c['D6'], 'D9_parcial': D9, 'extra_ordem_e_tempo': EX}
all_pass = all(v['PASS'] for v in checks.values())

# ------------------------------------------------------------------ achados
F = []
add = lambda sev, ident, text: F.append({'severity': sev, 'id': ident, 'text': text})
add('INFO', 'R2-I1', f"Os três campos medidos (accounts_modified, bench_restarted, client_files_changed = false, errors vazio, agregados antes = depois) valem SÓ para os arquivos que o código mediu: {sm['state_files']} de estado ({sm['state_bytes']} B), {sm['client_files']} de cliente ({sm['client_bytes']} B) e os listeners das portas 18765, 18766 e 8081. A cobertura do resto é a minha varredura de mtime: {SC['varredura']['arquivos_visitados']} arquivos de C:\\IALD\\projetos_pyhton\\IALD, nada podado, mtime ≥ início do deploy ({T['deploy_stderr_mtime (inicio do deploy)']}): só o plano ({jan['no_plano']}), os backups ({jan['backups']}), {jan['n_logs']} logs do supervisor/web na janela e {pos['total']} telemetrias depois dela. Os 19 caminhos do B1 ficam todos antes do deploy e com a mesma contagem de arquivos da rodada 1.")
add('INFO', 'R2-I2', "O web novo não escreveu estado medido depois da janela: os 120 arquivos de estado têm mtime anterior ao deploy e o meu agregado de agora é igual ao state_aggregate_after (o do cliente também). Mudaram depois da janela só dois arquivos de telemetria em logs\\: gpu_20261104_072914.csv (logger de GPU que acrescenta uma linha a cada 15 s desde 07:29, iniciado antes da instalação) e iald_heartbeat_telemetry.jsonl (telemetria do heartbeat: o log do web novo diz 'Heartbeat Iniciado' e a linha das 14:53:54 é do tipo 'beat'). Não são estado nem são do plano; achei diferença em zero arquivos de estado.")
add('INFO', 'R2-I3', "Limite do método: o mtime só mostra a última escrita e não vê remoção. Fica coberto porque nada fora da telemetria tem mtime posterior à janela, as contagens dos 19 caminhos são as da rodada 1, os agregados dos conjuntos medidos são iguais e o plano não remove nada.")
add('INFO', 'R2-I4', "deployment.json grava status INSTALLED_RESTART_REQUIRED mesmo com o reinício feito: o reinício está em restart.json (PASS; pid 14740 para 66348). A string descreve a aplicação do plano (lição 2 da v406).")
add('INFO', 'R2-I5', f"O log do supervisor traz '*** WEB SERVER MORREU | exit code =' às 14:52:05 e 'reiniciando em 5 s': é o supervisor, suspenso durante a janela, vendo o filho encerrado de forma controlada; 'PID 66348 iniciado' às 14:52:10. O novo filho nasceu {n5['novo']['create_time']}, {EX['tempo']['web_novo_nasceu_depois_da_ultima_escrita_s']} s depois da última escrita do plano; o stdout do web novo não tem sinal de erro e o .err tem 0 B.")
add('INFO', 'R2-I6', f"Janela de manutenção {EX['tempo']['janela_manutencao_s']} s (v406: 87 s); escrita do plano {EX['ordem_de_escrita']['escrita_levou_s']} s ({EX['ordem_de_escrita']['primeiro']} a {EX['ordem_de_escrita']['ultimo']}), mtimes não decrescentes na ordem do plano e o manifesto ativo por último; os 7 backups são anteriores às escritas dos seus destinos.")
add('INFO', 'R2-I7', "B2 da rodada 1 (nome de arquivo com substituto Unicode solitário derruba scope_compare) não se manifestou: o deployment.json foi gravado. B1 continua sem correção de código; a evidência desta instalação é a varredura acima.")
add('INFO', 'R2-I8', "D9 desta rodada é parcial: meu rastro (1 connect permitido a 127.0.0.1:8082, 0 abertura de .env, 0 subprocesso, 0 escrita fora da pasta) e a trilha do deploy (código sem rede externa nem provedor; evidências sem pista de provedor ou segredo). A parte dos carregadores de produção (0 rede, 0 .env e provider_calls 0 no INSTALLED_VERIFICATION.json) fica para o D7/D9 da segunda mensagem.")
transparency = ["Dois defeitos do MEU script: r2_extra.py indexava os backups por nome de arquivo e colidia (4 de 7 conferidos); percebi pelo número de linhas da saída, passei a indexar por caminho relativo (7 de 7) e reexecutei, e o veredito não mudou. r2_d9.py tinha um apóstrofo dentro de um literal (erro de sintaxe, sem veredito).",
                "Rotulagem: a classe 'log do supervisor ou web' do meu script reunia tudo sob logs\\; depois de ver os dois arquivos que mudaram depois da janela, passei a nomeá-los como telemetria (não são logs do supervisor). Não mudei critério: a janela estrita continua sem nenhum 'outro'.",
                "Nenhum critério de PASS/FAIL foi alterado depois de ver dados nesta rodada; a partitura da rodada (PARTITURA_R2_antes_de_medir.md) foi escrita antes das medições."]
limits = ["Não instalei, não reiniciei, não matei nem iniciei processo; não rodei deploy_controlled.py, verify_installed.py nem teste_escopo_v407.py; a única rede foi o GET http://127.0.0.1:8082/login.",
          "Não tenho o hash por arquivo de estado do instante da instalação (só o agregado); por isso a explicação de qualquer diferença seria por mtime e pasta. Não houve diferença para explicar.",
          "D7 e D8 (carregadores de produção e INSTALLED_VERIFICATION.json) não foram feitos nesta rodada, por ordem do coordenador; a parte dos carregadores do D9 também fica para lá.",
          "Não avalio resposta ao vivo do app, celular físico nem valor científico; o GET /login prova que o web novo responde, não que responde bem."]
scripts = {p.name: sha(p.read_bytes())[:16] for p in sorted(HERE.glob('r2*.py'))}
reused = ['check_d1_d4.py (v406 -d) adaptado em r2_d1_d6.py', 'check_scope_scan.py (v406 -d) adaptado em r2_d4_scope.py (agora com re-medição própria dos agregados e os 19 caminhos nomeados)', 'check_d5.py (v406 -d) adaptado em r2_d5.py',
          'novos, meus: r2lib.py (gancho de auditoria que conta e bloqueia), r2_extra.py, r2_d9.py, r2_d4_function.py (roda o d4_check.py da rodada 1 na produção), r2_compile.py']

rdep = {'status': 'PASS' if all_pass else 'FAIL', 'reviewer': ACTOR, 'timestamp': now.isoformat(), 'task': 'deploy', 'release': 'v407',
        'scope': 'Revisão independente do que foi INSTALADO (D1-D6 e D9 parcial) da release v407 do app; não instala, não reinicia, não corrige. Mede bytes, backups, escopo, processos e manifesto ativo; não mede resposta de modelo nem celular. D7-D8 em review_verify.json, em outra mensagem.',
        'release_dir': str(W), 'plan_sha256': D16['checks']['D1']['plan_sha256_recalculado'], 'evidence_sha256': ev_hash,
        'evidencia_submetida_pelo_construtor_inalterada': unchanged_submitted, 'checks': checks, 'b1_19_caminhos': b1, 'findings': F, 'findings_alto_medio': [], 'transparency': transparency, 'reused_from_mould': reused, 'limits': limits, 'scripts_sha16': scripts,
        'partitura_antes_de_medir_sha256': sha((HERE / 'PARTITURA_R2_antes_de_medir.md').read_bytes()), 'review_final_sha256': sha((W / 'validation/review_final.json').read_bytes())}
with (W / 'validation/review_deploy.json').open('x', encoding='utf8') as f:
    json.dump(rdep, f, ensure_ascii=False, indent=2, default=str)
rd_sha = sha((W / 'validation/review_deploy.json').read_bytes())

# ------------------------------------------------------------------ parecer
d1, d2, d3, d4a, d6 = c['D1'], c['D2'], c['D3'], c['D4a'], c['D6']
m = lambda a: a['PASS']
md = f"""# PARECER v407 R2 — revisão independente da INSTALAÇÃO (ator `{ACTOR}`)

Data: {now.strftime('%Y-%m-%dT%H:%MZ')}. Release: `{W}`. Plano sha256 `{d1['plan_sha256_recalculado']}`.

**Veredito: {'ACEITO (tarefa `deploy`)' if all_pass else 'RECUSADO'}. Nenhum achado ALTO ou MÉDIO.** Esta rodada cobre D1–D6 e D9 (parcial); D7–D8 (`verify`) ficam para a segunda mensagem do orquestrador e a tarefa `verify` não é tocada aqui.

## Partitura (dita antes de medir; texto integral em `PARTITURA_R2_antes_de_medir.md`, sha16 `{sha((HERE/'PARTITURA_R2_antes_de_medir.md').read_bytes())[:16]}`)
Decide se o que está instalado em `C:\\IALD\\projetos_pyhton\\IALD` é o plano que eu revisei, se o escopo medido pelo código bate com a minha varredura própria e se o processo web novo é o esperado; **não** decide valor científico nem resposta ao vivo; um FAIL seria **parede medida** (instalado diferente do plano), nunca uma palavra sobre a teoria. Escolhas ditas antes: recálculo próprio dos bytes (não importo `verify_installed.py`), três visões de tempo, varredura de mtime da árvore inteira sem podar, re-medição própria dos agregados, só leitura de processos e o único GET permitido.

## Resultado
| item | veredito | número-chave |
|---|---|---|
| D1 | {'PASS' if m(d1) else 'FAIL'} | plano `{d1['plan_sha256_recalculado'][:16]}` = `review_final` = `deployment` = `final_checks`; as 4 ferramentas têm o sha que o `review_final` pinou (`transaction.py` `{d1['tools_recalculados']['transaction.py']}`); `review_final.json` inalterado desde o meu aceite (`33dd393f24d01f6f`) |
| D2 | {'PASS' if m(d2) else 'FAIL'} | {d2['ok_no_disco']}/{d2['arquivos_no_plano']} destinos com o sha do plano ({d2['bytes_totais_instalados']} B); origem (staging) {d2['arquivos_no_plano'] - d2['staging_diverge_do_plano']}/{d2['arquivos_no_plano']}; `deployment.files` {d2['deployment.files_entradas']} entradas, 0 divergentes |
| D3 | {'PASS' if m(d3) else 'FAIL'} | {d3['backups_no_deployment']} backups `.bak_{d3['carimbos'][0]}` ao lado dos destinos, bytes = baseline do plano, todos anteriores à escrita do destino; sem `mobile_backups` nem `rollback_new_files` |
| D4(a) | {'PASS' if m(d4a) else 'FAIL'} | RUNTIME_BASELINE {d4a['RUNTIME_BASELINE_intactos_sem_o_manifesto']}/{d4a['RUNTIME_BASELINE_entradas'] - 1} intactos + manifesto: backup `{d4a['manifesto']['backup_bytes_sha']}` = baseline, novo `{d4a['manifesto']['novo_no_disco']}` = plano; 0 `.py` de runtime mudado; 0 extra/ausente/tmp no alvo |
| D4(b) | {'PASS' if d4b_ok else 'FAIL'} | janela estrita `{T['maintenance.json mtime (inicio da janela)']}`–`{T['restart.json mtime (fim da janela)']}` ({T['janela_estrita_segundos']} s): **{jan['no_plano']} plano + {jan['backups']} backups + {jan['n_logs']} logs do supervisor/web, 0 outros**; {SC['varredura']['arquivos_visitados']} arquivos varridos sem podar; depois da janela só {pos['total']} telemetrias; os 19 caminhos do B1 nomeados abaixo |
| D4(c) | {'PASS' if d4c_ok else 'FAIL'} | `accounts_modified`, `bench_restarted`, `client_files_changed` = `false` (booleanos, não `null`), `errors` vazio, `bench_changed` vazio; agregados antes = depois; **re-medição minha**: cliente {rm['cliente']['arquivos']} arquivos/{rm['cliente']['bytes']} B e estado {rm['estado']['arquivos']}/{rm['estado']['bytes']} B com agregado igual ao `*_after` |
| D5 | {'PASS' if D5['PASS'] else 'FAIL'} | pid antigo {n5['restart_json']['old_web_pid']} ausente; novo {n5['restart_json']['new_web_pid']} filho do supervisor {n5['restart_json']['supervisor_pid']} (create_time exato `{n5['supervisor']['create_time_exato']}` = `maintenance.json`); `8082` ouve só o pid novo; `GET /login` = {n5['GET_login']['status']} ({n5['GET_login']['bytes']} B); 18765/18766 sem ouvir antes, depois e agora; 8081 = llama-server pid {srv['8081']['agora'][0]['pid']}, mesmo create_time |
| D6 | {'PASS' if m(d6) else 'FAIL'} | `iald_nucleo_fixo.json` sha `{d6['sha_manifesto_no_disco'][:16]}` = `manifest_install.json` = plano, último item ({d6['indice_no_plano'] + 1} de {d6['total_plano']}); release `v407` nos três campos; pino e commit certos; {d6['arquivos_no_disco_sob_o_alvo']} arquivos sob `canonical_releases\\v407_bf9017157406` = {d6['caminhos_sob_canonical_releases_v407_bf9017157406_no_plano']} do plano |
| D9 (parcial) | {'PASS' if D9['PASS'] else 'FAIL'} | meu rastro: 1 connect permitido (127.0.0.1:8082), 0 `.env`, 0 subprocesso, 0 escrita fora da pasta; código do deploy sem rede externa nem provedor; evidências sem pista de provedor ou segredo. **Os carregadores (D7) ficam para a segunda mensagem.** |

Evidência submetida pelo construtor (`deployment.json` `{ev_hash['deployment.json'][:16]}`, `maintenance.json` `{ev_hash['maintenance.json'][:16]}`, `restart.json` `{ev_hash['restart.json'][:16]}`, `deploy_stdout.txt`): inalterada desde a submissão: {'sim' if unchanged_submitted else 'NÃO'}.

## O que os três campos medidos valem (declaração pedida)
`accounts_modified`, `bench_restarted` e `client_files_changed` valem **só para os arquivos que o código mediu**: {sm['state_files']} de estado, {sm['client_files']} de cliente e os listeners 18765, 18766 e 8081. **A cobertura do resto é a minha varredura de mtime**, que visitou {SC['varredura']['arquivos_visitados']} arquivos de `C:\\IALD\\projetos_pyhton\\IALD` (nada podado) e não achou nenhuma mudança fora do plano, dos backups e dos logs. O B1 da rodada 1 segue sem correção de código; para esta instalação o resíduo está fechado por evidência, não por código.

## D4(b): os 19 caminhos do B1, com mtime, frente à janela estrita {T['maintenance.json mtime (inicio da janela)']}–{T['restart.json mtime (fim da janela)']} de 04/11/2026
| caminho | arquivos (agora / rodada 1) | mtime mais novo | dentro da janela? |
|---|---|---|---|
"""
for k, v in b1.items():
    md += f"| `{v['path']}` | {v['arquivos']} / {v['arquivos_rodada_1']} | {v['mtime_mais_novo']} | **fora, antes** (0 dentro, 0 depois) |\n"
md += f"""
Os 19 ficam fora e antes do deploy (o mais novo é `.iald_runtime\\task_runs`, 30/10/2026 20:14:10; `iald_deadlines.json` é de 23/10/2026 14:51:06, a data é outra apesar de a hora lembrar a janela). Nenhum deles é destino do plano.

## Mudanças depois da janela (web novo e outros serviços)
{pos['total']} arquivos, ambos telemetria em `logs\\`: {', '.join('`%s` (%s)' % (a, b) for a, b in pos['logs'])}. Nenhum arquivo de estado: os {rm['estado']['arquivos']} de estado têm mtime anterior ao deploy ({rm['estado_por_posicao']['antes']} antes, {rm['estado_por_posicao']['pre_janela']} na pré-janela, {rm['estado_por_posicao']['dentro']} dentro, {rm['estado_por_posicao']['depois']} depois) e o agregado de agora é igual ao `state_aggregate_after`; não achei diferença, então não há arquivo a explicar. Na janela, os {jan['n_logs']} logs são {', '.join('`%s`' % a for a, b in jan['logs_do_supervisor'])}.

## Achados (nenhum ALTO ou MÉDIO)
"""
for f in F:
    md += f"- **{f['severity']} {f['id']}**: {f['text']}\n"
md += "\n## Transparência\n" + ''.join(f"- {t}\n" for t in transparency)
md += f"""
## Conferência da partitura no fim
Cumprida: nada aqui fala da teoria; nenhum FAIL; os dois pontos que poderiam virar achado (estado escrito pelo web novo; contas e carteira fora da medição) foram medidos e deram vazio (estado idêntico ao agregado da instalação; os 19 caminhos inalterados desde antes do deploy). Reaproveitei e adaptei `check_d1_d4.py`, `check_scope_scan.py` e `check_d5.py` do revisor da v406 (-d); são novos `r2lib.py`, `r2_extra.py`, `r2_d9.py`, `r2_d4_function.py` e a re-medição própria dos agregados.

## Limites do exame
""" + ''.join(f"- {t}\n" for t in limits)
md += f"""
## Arquivos
`W\\validation\\review_deploy.json` (sha16 `{rd_sha[:16]}`); scripts e saídas em `W\\review\\revisor_sonnet-app-v407-revisor\\` (`r2_*.py`, `r2_*_out.json`).
"""
(HERE / 'PARECER_v407_R2.md').write_text(md, encoding='utf-8')
print(json.dumps({'status': rdep['status'], 'all_pass': all_pass, 'sha256_review_deploy': rd_sha, 'parecer_bytes': len(md.encode()), 'unchanged_submitted': unchanged_submitted, 'D4b': d4b_ok, 'D4c': d4c_ok}, indent=1))
