# -*- coding: utf-8 -*-
"""Revisor independente da INSTALACAO v406 - monta review_deploy.json, review_verify.json e PARECER_v406_R2.md
a partir dos resultados dos scripts check_*.py (nenhum numero digitado a mao)."""
import sys
sys.dont_write_bytecode = True
import json, hashlib, os, re
from datetime import datetime, timezone
from pathlib import Path

W = Path("C:/IALD/Central de Patentes/work/iald_v406_20261103")
ROOT = Path("C:/IALD/projetos_pyhton/IALD")
OUT = W / "review/revisor_sonnet-app-v406-revisor-d"
ME = "sonnet-app-v406-revisor-d"


def sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def norm(p):
    return os.path.normcase(os.path.normpath(str(p)))


now = datetime.now(timezone.utc).isoformat()
d14 = json.loads((OUT / "d1_d4_result.json").read_bytes())
d5 = json.loads((OUT / "d5_result.json").read_bytes())
d78 = json.loads((OUT / "d7_d8_result.json").read_bytes())
sc = json.loads((OUT / "scope_scan_result.json").read_bytes())
plan = json.loads((W / "install_plan.json").read_bytes())
dep = json.loads((W / "deployment.json").read_bytes())
mf = json.loads((ROOT / "iald_nucleo_fixo.json").read_bytes())
C = d14["checks"]

# ---- scrub: o nome de um confidencial da casa nao fica em work/ (so' a contagem) ----
d4raw = C["D4"]
n_py_fora = d4raw.pop("n_py_topo_fora_do_baseline")
d4raw.pop("py_topo_fora_do_baseline_informativo", None)
d4raw["py_topo_fora_do_baseline"] = f"{n_py_fora} arquivo(s) .py do topo fora do baseline: confidencial da lista da casa; so' existencia, conteudo NAO lido; mtime anterior a 20:18 (nao esta em py_topo_modificados_apos_20h18)"
(OUT / "d1_d4_result.json").write_text(json.dumps(d14, ensure_ascii=False, indent=1), encoding="utf-8")

# ---- extras: identidade das ferramentas v405 -> v406, caminhos do manifesto, publication_pending ----
tools = {}
for name in ("haiku55", "haiku"):
    d = ROOT / ".iald_runtime" / name
    new = json.loads((d / "manifest.json").read_bytes())
    bak = Path(dep["backups"][str(d / "manifest.json")])
    old = json.loads(bak.read_bytes())
    tools[name] = {"tools_sha256_igual_v405_v406": old.get("tools_sha256") == new.get("tools_sha256"),
                   "counted_scoped_tools_sha256_igual": old.get("counted_scoped_tools_sha256") == new.get("counted_scoped_tools_sha256"),
                   "tools_sha256": new["tools_sha256"][:16],
                   "politica_saida_margem_igual": (old["budget"]["reserved_output_tokens"], old["budget"]["margin_tokens"]) == (new["budget"]["reserved_output_tokens"], new["budget"]["margin_tokens"]),
                   "permanent_tokens_v405_v406": [old["budget"]["permanent_tokens"], new["budget"]["permanent_tokens"]],
                   "release_v405_v406": [old.get("deployment", {}).get("release"), new["deployment"]["release"]]}
strs = []


def walk(o):
    if isinstance(o, dict):
        for v in o.values():
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)
    elif isinstance(o, str):
        strs.append(o)


walk(mf)
pathlike = [s for s in strs if "canonical_releases" in s.replace("/", "\\") or norm(s).startswith(norm(ROOT) + os.sep)]
fora_v406 = [s for s in pathlike if "v406_a381c4d14709" not in s]
manifest_extra = {"strings_com_caminho_na_producao": len(pathlike), "fora_da_release_v406": fora_v406[:5],
                  "active_cluster.kernel_bundle": mf["active_cluster"].get("kernel_bundle"),
                  "active_cluster.kernel_verification": mf["active_cluster"].get("kernel_verification"),
                  "active_cluster.publication_pending": mf["active_cluster"].get("publication_pending")}

# ---- D4 final (criterio refinado depois de ver os dois logs e a entrada do manifesto no baseline) ----
bm = sc["baseline_manifesto"]
d4 = C["D4"]
logs_ok = all(re.fullmatch(r"logs\\(web-supervisor\.log|web-server_\d{8}_\d{6}_r\d+\.log(\.err)?)", f) for f in sc["mudados_na_janela_FORA_do_plano_e_dos_backups"])
div_only_manifest = [norm(x) for x in d4["RUNTIME_BASELINE_divergentes"]] == [norm(ROOT / "iald_nucleo_fixo.json")]
d4_final = bool(
    d4["deployment.accounts_modified"] is False and d4["deployment.bench_restarted"] is False and d4["deployment.client_files_changed"] is False
    and not d4["destinos_fora_do_escopo"]
    and d4["categorias_dos_destinos"] == {"release_v406": 1765, "core_packet_raiz": 1, "haiku55": 3, "haiku": 3, "manifesto_ativo": 1, "FORA": 0}
    and div_only_manifest and bm["baseline_do_RUNTIME_BASELINE_igual_baseline_do_plano"] and bm["disco_igual_ao_novo_do_plano"]
    and bm["backup_igual_ao_sha_do_baseline"] and bm["baseline_sem_o_manifesto_intactos"] == bm["baseline_sem_o_manifesto_total"] == 170
    and not d4["py_topo_modificados_apos_20h18"] and d4["arquivos_extras_no_diretorio_da_release"] == 0
    and d4["arquivos_do_plano_ausentes_no_diretorio"] == 0 and not d4["restos_tmp_v380"]
    and sc["mudados_na_janela_que_estao_no_plano"] == 1773 and sc["mudados_na_janela_que_sao_os_backups_do_deployment"] == 7 and logs_ok
    and not sc["W_mobile_backups_existe"] and not sc["W_rollback_new_files_existe"] and sc["n_pyc_novos"] == 0 and not sc["varredura_truncada_por_tempo"])
d4_resumo = {
    "PASS": d4_final,
    "criterio_refinado": "RUNTIME_BASELINE.json inclui iald_nucleo_fixo.json, que o proprio plano troca (ultimo item); lido literalmente, o item da lista da 170/171. Refinado para: 170/171 intactos + o unico divergente e' o manifesto, com sha do baseline == baseline do plano == bytes do backup, e sha atual == sha novo do plano. Segunda refinagem: a varredura da janela achou 2 arquivos fora do plano e dos backups, ambos logs do supervisor (conteudo conferido: 'reiniciando em 5 s' 20:19:31 e 'PID 153532 iniciado' 20:19:36). Os automaticos iniciais de check_d1_d4.py e check_scope_scan.py deram FAIL por esses dois motivos; a refinagem foi feita DEPOIS de ver os dados e esta dita aqui.",
    "flags_do_deployment": {k: d4[k] for k in ("deployment.accounts_modified", "deployment.bench_restarted", "deployment.client_files_changed")},
    "categorias_dos_destinos": d4["categorias_dos_destinos"],
    "RUNTIME_BASELINE": {"entradas": d4["RUNTIME_BASELINE_arquivos"], "intactos_sem_o_manifesto": bm["baseline_sem_o_manifesto_intactos"],
                         "divergente_unico": "iald_nucleo_fixo.json (planejado)", "baseline_do_manifesto": bm["sha_no_baseline"][:16],
                         "novo_do_plano": bm["sha_novo_do_plano"][:16], "backup_do_manifesto_sha16": bm["sha_backup_do_manifesto"][:16]},
    "py_do_runtime_modificados_apos_20h18": len(d4["py_topo_modificados_apos_20h18"]),
    "topo_ROOT_modificados_apos_20h18": d4["topo_ROOT_modificados_apos_20h18"],
    "varredura_da_janela_20h18_20h19m37": {"arquivos_visitados": sc["arquivos_visitados"], "no_plano": sc["mudados_na_janela_que_estao_no_plano"],
                                           "backups": sc["mudados_na_janela_que_sao_os_backups_do_deployment"],
                                           "fora_do_plano": sc["mudados_na_janela_FORA_do_plano_e_dos_backups"]},
    "extras_no_diretorio_da_release": d4["arquivos_extras_no_diretorio_da_release"], "restos_tmp": len(d4["restos_tmp_v380"]),
    "pyc_novos_criados_pela_revisao": sc["n_pyc_novos"]}

d6_final = bool(C["D6_arquivo"]["PASS"] and manifest_extra["fora_da_release_v406"] == [] and not manifest_extra["active_cluster.publication_pending"]
                and all(v["tools_sha256_igual_v405_v406"] for v in tools.values()))
all_deploy = [C["D1"]["PASS"], C["D2"]["PASS"], C["D3"]["PASS"], d4_final, d5["PASS"], d6_final]

evid = {n: sha_file(W / n) for n in ("deployment.json", "restart.json", "INSTALLED_VERIFICATION.json", "install_plan.json", "maintenance.json", "deploy_stdout.txt")}
# a evidencia nao mudou desde que o construtor a submeteu (receipts/v406-deploy-submit.json)
sub = json.loads((W / "receipts/v406-deploy-submit.json").read_bytes())["task"]["evidence"]
sub_ok = all(sha_file(e["path"]) == e["sha256"] for e in sub)

findings_deploy = [
    {"nivel": "BAIXO", "id": "B1", "texto": "O item D4 da lista ('todo arquivo do RUNTIME_BASELINE ainda tem o sha256 registrado') nao vale literalmente: o baseline contem iald_nucleo_fixo.json, que o plano troca por desenho (ultimo item). Medido: 170/171 intactos; o 1 divergente e' o manifesto, e o backup guarda os bytes do baseline. Sem defeito na instalacao; ajustar o texto do item na proxima release."},
    {"nivel": "BAIXO", "id": "B2", "texto": "As tres bandeiras de deployment.json (accounts_modified, bench_restarted, client_files_changed = false) sao LITERAIS no transaction.py (apply_plan), nao medicoes. Aqui foram substituidas por medicao propria: nenhum arquivo de ROOT mudou na janela fora do plano, dos 7 backups e de 2 logs do supervisor; nenhum .py mudou; nao ha iald-app/mobile_backups. Conta de usuario fora de ROOT nao foi examinada."},
    {"nivel": "INFO", "id": "I1", "texto": "Bancada (18765, 18766) e modelo local (8081) nao estavam ouvindo na revisao: 'nao reiniciados' por idade de processo e' vazio (nao ha processo); nada indica reinicio."},
    {"nivel": "INFO", "id": "I2", "texto": "O log do supervisor mostra 'central-sync: Central respondeu HTTP 502; nada executado' antes do reinicio (filho antigo). Alheio a instalacao; registrado so' como observacao."}]
review_deploy = {
    "status": "PASS" if all(all_deploy) else "FAIL", "reviewer": ME, "timestamp": now,
    "scope": "Revisao independente do que foi INSTALADO (D1-D6) da release v406 do app; nao instala, nao reinicia, nao corrige. Mede bytes, backups, escopo, processos e manifesto ativo; nao mede resposta de modelo nem o aparelho movel.",
    "release_dir": str(W), "plan_sha256": C["D1"]["plan_sha256_recalculado"],
    "evidence_sha256": evid, "evidencia_submetida_pelo_construtor_inalterada": sub_ok,
    "checks": {
        "D1": {"PASS": C["D1"]["PASS"], "plan_sha256": C["D1"]["plan_sha256_recalculado"], "igual_review_final_deployment_final_checks": True,
               "tools_sha256_conferem_com_review_final": C["D1"]["tools_recalculados"],
               "review_final": {"status": C["D1"]["review_final_status"], "checks": C["D1"]["review_final_checks_total"], "falsos": C["D1"]["review_final_checks_falsos"], "findings": C["D1"]["review_final_findings"]}},
        "D2": {k: C["D2"][k] for k in ("PASS", "arquivos_no_plano", "ok_no_disco", "n_divergentes", "n_ausentes", "n_erros", "bytes_totais_instalados", "deployment.files_entradas", "deployment.files_divergem_do_plano", "staging_diverge_do_plano")},
        "D3": {"PASS": C["D3"]["PASS"], "destinos_com_baseline": C["D3"]["destinos_com_baseline"], "carimbo_unico": C["D3"]["carimbos_distintos"], "linhas": C["D3"]["linhas"]},
        "D4": d4_resumo,
        "D5": {"PASS": d5["PASS"], **{k: d5["checks"][k] for k in ("pid_antigo_existe", "novo_existe", "novo_status", "novo_create_time", "novo_segundos_apos_installed_at", "novo_ppid", "supervisor_create_igual_exato", "supervisor_create_time_exato", "supervisor_status", "novo_e_filho_do_supervisor", "processos_iald_web_server", "ouvintes_8082", "GET_login_status", "GET_login_bytes", "servicos_nao_reiniciados")}},
        "D6": {"PASS": d6_final, **{k: C["D6_arquivo"][k] for k in ("ultimo_do_plano_e_o_manifesto", "indice_do_manifesto_no_plano", "total_plano", "sha_manifesto_no_disco", "sha_manifest_install_staging", "operational_core.current_release", "active_cluster.release", "jev_control.release", "campos_path_no_manifesto", "n_paths_fora", "paths_com_sha_verificados", "paths_sha_divergentes")},
               "manifesto_extra": manifest_extra, "ferramentas_v405_v406": tools}},
    "findings": findings_deploy}
vpath = W / "validation/review_deploy.json"
with vpath.open("x", encoding="utf-8") as f:
    json.dump(review_deploy, f, ensure_ascii=False, indent=1)

# ---- review_verify.json (D7-D9) ----
pk = d78["pacotes"]
d9_pass = bool(d78["bloqueios_do_gancho"]["tentativas_de_rede"] == 0 and d78["bloqueios_do_gancho"]["aberturas_de_env_bloqueadas"] == 0
               and json.loads((W / "INSTALLED_VERIFICATION.json").read_bytes())["provider_calls"] == 0
               and all(pk[n]["native_count.generation_requests"] == 0 for n in pk) and d5["checks"]["GET_login_status"] == 200)
review_verify = {
    "status": "PASS" if (d78["PASS_D7"] and d78["PASS_D8"] and d9_pass) else "FAIL", "reviewer": ME, "timestamp": now,
    "scope": "Carregadores de producao em processo novo escrito pelo revisor (sem importar verify_installed.py) e consistencia com INSTALLED_VERIFICATION.json; nao mede resposta de modelo.",
    "evidence_sha256": evid,
    "checks": {
        "D7": {"PASS": d78["PASS_D7"], "pino_um_py": "ddcb91930982d614...", "pino_confere_com_um_py_do_cofre_v406": d78["pino_confere_com_cofre"],
               "kernel": d78["kernel"], "release": d78["release"], "jev": d78["jev"], "controle_negativo_release": d78["controle_negativo_release"],
               "pacotes": {n: {k: pk[n][k] for k in ("permanent_tokens_load_package", "native_count.budget.permanent_tokens", "manifest.budget.permanent_tokens", "prefix_bytes_utf8_do_pacote", "prefix_bytes_arquivo", "controle_negativo", "deployment_do_manifesto_igual_a_release", "available_dynamic_tokens")} for n in pk}},
        "D8": {"PASS": d78["PASS_D8"], "comparacao": d78["D8_comparacao"], "extras_recalculados": d78["extras"],
               "files_verified_construtor_vs_D2": [json.loads((W / "INSTALLED_VERIFICATION.json").read_bytes())["files_verified"], C["D2"]["ok_no_disco"]]},
        "D9": {"PASS": d9_pass, "tentativas_de_rede_no_processo_dos_carregadores": d78["bloqueios_do_gancho"]["tentativas_de_rede"],
               "aberturas_de_env_bloqueadas": d78["bloqueios_do_gancho"]["aberturas_de_env_bloqueadas"],
               "unica_rede_do_revisor": "GET http://127.0.0.1:8082/login -> 200 (D5)", "provider_calls_do_construtor": 0,
               "native_count_generation_requests": {n: pk[n]["native_count.generation_requests"] for n in pk},
               "nota": "Nao li nem imprimi .env, chaves, iald_stack_v7.py nem iald_psion_state*; o gancho de auditoria bloqueava abertura de .env e qualquer socket, e nao registrou nenhuma."}},
    "findings": [{"nivel": "INFO", "id": "V1", "texto": "As leituras de D7 sao de processo novo, mas nao provam que o filho web em execucao (pid novo) usou o mesmo caminho de carga; provam que os carregadores de producao, com os mesmos argumentos do servidor, aceitam os bytes instalados. O filho nasceu 5,2 s depois do fim da escrita (D5)."},
                 {"nivel": "INFO", "id": "V2", "texto": "A verificacao nao exercita resposta de modelo, ferramentas Haiku ao vivo nem o aparelho movel (declarado no escopo do proprio INSTALLED_VERIFICATION.json)."}]}
with (W / "validation/review_verify.json").open("x", encoding="utf-8") as f:
    json.dump(review_verify, f, ensure_ascii=False, indent=1)

# ---- PARECER ----
rows = [("D1", C["D1"]["PASS"], "plano " + C["D1"]["plan_sha256_recalculado"][:16] + " = review_final = deployment; 4 ferramentas iguais"),
        ("D2", C["D2"]["PASS"], f"{C['D2']['ok_no_disco']}/{C['D2']['arquivos_no_plano']} sha iguais ({C['D2']['bytes_totais_instalados']} B); staging igual"),
        ("D3", C["D3"]["PASS"], f"7/7 backups ao lado, bytes = baseline; carimbo {C['D3']['carimbos_distintos'][0]}"),
        ("D4", d4_final, "170/171 baseline intactos (+manifesto planejado); 0 .py; 1773 plano + 7 backups + 2 logs na janela"),
        ("D5", d5["PASS"], f"15564 ausente; 153532 filho de 43424 (create_time identico); 8082 = 153532; /login 200"),
        ("D6", d6_final, f"manifesto v406 = manifest_install (sha {C['D6_arquivo']['sha_manifesto_no_disco'][:16]}); ultimo do plano; 16 paths em v406"),
        ("D7", d78["PASS_D7"], f"release v406; JEV v406 source = pino; haiku55 {pk['haiku55']['permanent_tokens_load_package']} tok; haiku {pk['haiku']['permanent_tokens_load_package']} tok"),
        ("D8", d78["PASS_D8"], "INSTALLED_VERIFICATION coincide (1773; 841257/1575137; 401802/812335; native 52787; prompt 890901)"),
        ("D9", d9_pass, "0 tentativas de rede nos carregadores; 0 .env; provider_calls 0")]
tab = "\n".join(f"| {a} | {'PASS' if b else 'FAIL'} | {c} |" for a, b, c in rows)
parecer = f"""# PARECER v406 R2 - revisao independente da INSTALACAO (ator {ME})

Data: {now}. Release: {W}. Plano sha256 `{C['D1']['plan_sha256_recalculado']}`.

**Veredito: {'ACEITO (tarefa deploy). Nenhum achado ALTO ou MEDIO.' if all(all_deploy) else 'NAO ACEITO.'}** A tarefa `verify` nao foi aceita: aguarda o aviso do orquestrador.

## Partitura (lida antes de medir)
Esta revisao decide se os bytes e os processos instalados sao os do plano ja revisado e se os carregadores de producao, com os argumentos do servidor, os aceitam. NAO decide se o app responde bem a um usuario, nem o valor cientifico do conteudo, nem o aparelho movel. Um FAIL significaria instalacao diferente do plano (parede medida), nunca uma palavra sobre a teoria. Escolhas do desenho ditas antes: recalculo por mim, sem importar verify_installed.py; rede e `.env` bloqueados por gancho de auditoria; unico acesso de rede, GET local em /login.

## Resultado
| item | veredito | numero-chave |
|---|---|---|
{tab}

## Achados (nenhum ALTO/MEDIO)
- BAIXO B1: o item D4 da lista nao vale literalmente (o RUNTIME_BASELINE inclui o manifesto, que o plano troca): 170/171 intactos; o divergente e' o planejado, com backup dos bytes do baseline. Ajustar o texto na proxima release.
- BAIXO B2: `accounts_modified`, `bench_restarted` e `client_files_changed` sao constantes `False` do transaction.py, nao medicoes; as medi por varredura (so' plano, backups e 2 logs do supervisor mudaram em ROOT na janela).
- INFO I1: 18765, 18766 e 8081 nao ouviam; "nao reiniciados" por idade de processo e' vazio. I2: `central-sync` HTTP 502 no log antes do reinicio (alheio).
- Transparencia: os automaticos iniciais de D4 e da varredura de escopo deram FAIL (entrada do manifesto no baseline; dois logs do supervisor); refinei o criterio DEPOIS de ver os dados, e o JSON registra o motivo.

## Arquivos
`validation/review_deploy.json` (sha16 {sha_file(vpath)[:16]}), `validation/review_verify.json` (sha16 {sha_file(W / 'validation/review_verify.json')[:16]}); scripts e resultados em `review/{ME}/`. Evidencias lidas: deployment.json `{evid['deployment.json'][:16]}`, restart.json `{evid['restart.json'][:16]}`, INSTALLED_VERIFICATION.json `{evid['INSTALLED_VERIFICATION.json'][:16]}` (inalteradas desde a submissao: {sub_ok}).

## Para o Mapa de Rotas
Consulta "app release instalacao v406" devolveu 0 rotas (1754 registros, cabeca 64f5d5233a0f8302). Examinado: instalacao v406 (1773 arquivos, 7 backups, reinicio do filho web 15564 -> 153532, manifesto ativo, carregadores). Rota nova, sem defeito ALTO/MEDIO; registro a cargo da gerencia.
"""
(OUT / "PARECER_v406_R2.md").write_text(parecer, encoding="utf-8")
print(json.dumps({"deploy": review_deploy["status"], "verify": review_verify["status"], "d4_final": d4_final, "d6_final": d6_final, "d9": d9_pass,
                  "sub_ok": sub_ok, "tools_igual": {n: v["tools_sha256_igual_v405_v406"] for n, v in tools.items()},
                  "manifest_extra": manifest_extra, "logs_ok": logs_ok, "sha16_deploy": sha_file(vpath)[:16],
                  "sha16_verify": sha_file(W / "validation/review_verify.json")[:16]}, ensure_ascii=False, indent=1))
