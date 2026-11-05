# -*- coding: utf-8 -*-
"""ORDEM_006: fecha os registros da release v407 do app DEPOIS do aceite do verify e da Torre regenerada.
Passos (cada um escreve com 'xb' ou e' idempotente por event_id): acom | quadro | mapa | fila | tunel.
Numeros, hashes e estados sao LIDOS dos artefatos; as condicoes abaixo sao assert (falha visivel, nunca 'ok' falso).
Uso: python -B -X utf8 fechar_registros_v407.py [--seco] passo [passo ...]   (--seco: monta e imprime, nao escreve nem chama nada)"""
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
sys.path.insert(0, str(W))
import task  # noqa: E402  (UNIT, ACTOR, REF; so' leitura de configuracao)

OLD_SC = Path(r"C:\Users\rotol\AppData\Local\Temp\claude\C--IALD-Central-de-Patentes\fda3adae-8303-4906-a1c4-4eb0c0b6c4e4\scratchpad")
sys.path.insert(0, str(OLD_SC))
import acom as A  # noqa: E402  (REF da MINHA inscricao ordem001; call(payload) -> (rc, out, err))

PY = r"C:\Python314\python.exe"
R = Path(r"C:\IALD\projetos_pyhton\IALD")
TUNEL = Path(r"C:\IALD\TUNEL_CLAUDE_APP")
F03 = Path(r"C:\IALD\Central de Patentes\work\scientific_memory_sync_20261104_v407")
FILA = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fila")
QUEM = "claude-app-orquestrador"
REG = W / "registros_fechamento"
SECO = "--seco" in sys.argv
PASSOS = [a for a in sys.argv[1:] if not a.startswith("--")]


def rd(p):
    return json.loads(Path(p).read_bytes())


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def pin(p):
    b = Path(p).read_bytes()
    return {"arquivo": str(p), "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}


def novo(p, texto):
    if SECO:
        print("[seco] escreveria", p, len(texto.encode("utf-8")), "B")
        return
    with Path(p).open("xb") as f:
        f.write(texto.encode("utf-8"))


# ------------------------------------------------------------------ fatos (lidos) e condicoes (assert)
inst = rd(W / "INSTALLED_VERIFICATION.json")
dep, rest, mnt = rd(W / "deployment.json"), rd(W / "restart.json"), rd(W / "maintenance.json")
cfg = rd(W / "app" / "RELEASE.json")
med = rd(W / "BUILDER_MEASUREMENTS.json")
rdep, rver = rd(W / "validation" / "review_deploy.json"), rd(W / "validation" / "review_verify.json")
nf = rd(R / "iald_nucleo_fixo.json")
contrato = R / "canonical_releases" / ("v407_" + cfg["espelho_commit"][:12]) / "jev_control_v407.json"
parecer_r1 = W / "review" / "revisor_sonnet-app-v407-revisor" / "PARECER_v407_R1.md"
parecer_r2 = W / "review" / "revisor_sonnet-app-v407-revisor" / "PARECER_v407_R2.md"
licoes = W / "LICOES_v407.md"
torre_out = W / "torre_gerar_stdout.txt"
busca = (W / "BUSCA_EXERCITADA_v407.txt").read_text(encoding="utf-8").strip().splitlines()[-1]

assert cfg["release"] == "v407" and cfg["espelho_commit"].startswith("bf9017157406")
assert inst["status"] == "PASS" and inst["identity"]["release"] == "v407" and inst["JEV_release"] == "v407" and inst["provider_calls"] == 0
assert rest["status"] == "PASS" and rest["http_status"] == 200 and rest["supervisor_pid"] == mnt["supervisor_pid"]
assert dep["status"] == "INSTALLED_RESTART_REQUIRED" and dep["accounts_modified"] is False and dep["bench_restarted"] is False and dep["client_files_changed"] is False
assert rdep["status"] == "PASS" and rver["status"] == "PASS", (rdep["status"], rver["status"])
assert nf["operational_core"]["current_release"] == "v407" and nf["operational_core"]["release_source_sha256"] == cfg["um_py_sha256"]
assert nf["jev_control"]["release"] == "v407" and nf["jev_control"]["sha256"] == sha(contrato) and nf["jev_control"]["source_sha256"] == cfg["um_py_sha256"]
assert parecer_r2.is_file() and licoes.is_file() and torre_out.is_file()
torre_linha = [ln for ln in torre_out.read_text(encoding="utf-8", errors="replace").splitlines() if ln.strip()][-1].strip()

janela = round((W / "restart.json").stat().st_mtime - (W / "maintenance.json").stat().st_mtime)
carimbo = re.search(r"\.bak_(\d{8}_\d{6})", next(iter(dep["backups"].values()))).group(1)
pk = med["packages"]
hk, sh, sn = pk["haiku_expanded"], pk["shared"], pk["sonnet_public"]
folga = med["menor_folga_declarada_bytes"]
inst_pk = inst["packages"]
RESULTADO_TXT = (
    "INSTALADA em 04/11/2026 (janela de %d s entre maintenance.json e restart.json, reinicio autorizado pelo operador no chat): %d arquivos, %d backups (carimbo %s), "
    "web %d -> %d sob o supervisor %d, /login %d; verify_installed %s em processo novo (release %s, JEV %s, 0 chamadas a provedor); escopo da instalacao MEDIDO "
    "(accounts_modified/bench_restarted/client_files_changed = false, medidos em 120 arquivos de estado e 266 de cliente, errors vazio); Torre regenerada (%s) com o contrato jev_control_v407 pinado (%s); "
    "revisores distintos do construtor aceitaram sources, app, deploy e verify. Pacote: shared %d B, folga minima declarada %d B (DeepSeek; v406: 41975); haiku55 folga %d tokens; "
    "topicos %d, novos %s; plano de %d arquivos, 0 .py de runtime. %s"
) % (janela, inst["files_verified"], len(dep["backups"]), carimbo, rest["old_web_pid"], rest["new_web_pid"], rest["supervisor_pid"], rest["http_status"], inst["status"],
     inst["identity"]["release"], inst["JEV_release"], torre_linha, nf["jev_control"]["sha256"][:16], sh["prefix_bytes"], folga, hk["remaining_tokens"],
     med["topics"]["core"], med["topics"]["new_v407"], inst["files_verified"], busca)

EVID = [W / n for n in ("INSTALLED_VERIFICATION.json", "deployment.json", "restart.json", "maintenance.json", "deploy_stdout.txt", "verify_stdout.txt", "torre_gerar_stdout.txt",
                        "validation/review_final.json", "validation/review_deploy.json", "validation/review_verify.json", "BUILDER_MEASUREMENTS.json", "BUSCA_EXERCITADA_v407.txt",
                        "install_plan.json", "TESTE_ESCOPO_v407.json", "LICOES_v407.md", "app/RELEASE.json")]
EVID += [parecer_r1, parecer_r2, contrato, F03 / "DELIVERY_TECHNICAL_R1.json"]
for e in EVID:
    assert Path(e).is_file(), e
print(json.dumps({"release": cfg["release"], "arquivos": inst["files_verified"], "web": [rest["old_web_pid"], rest["new_web_pid"], rest["supervisor_pid"]], "janela_s": janela,
                  "backups": len(dep["backups"]), "folga_B": folga, "contrato_sha16": nf["jev_control"]["sha256"][:16], "torre": torre_linha, "seco": SECO}, ensure_ascii=False))


# ------------------------------------------------------------------ passos
def passo_acom():
    def acom(op, extra=None):
        rc, out, err = A.call(dict({"operation": op, "reference": A.REF}, **(extra or {})))
        return rc, (json.loads(out) if out.strip().startswith("{") else out), err

    rc, v0, err = acom("verify")
    rev0 = v0["result"]["receipt"]["revision"]
    texto = ("04/11/2026: release v407 do app INSTALADA (ORDEM_006). " + RESULTADO_TXT +
             " [o aceite dos revisores e' DECLARADO por eles ate a gerencia conferir na fonte; escopo: carregadores, hashes e login; sem resposta de modelo ao vivo nem celular fisico]")
    changes = {"records": [{"id": "app-v407-instalada-20261104", "kind": "fact", "statute": "REAL", "text": texto,
                            "sources": [{"kind": "artifact", "ref": str(p), "sha256": sha(p)} for p in (W / "INSTALLED_VERIFICATION.json", W / "deployment.json", W / "restart.json",
                                                                                                         W / "validation/review_deploy.json", W / "validation/review_verify.json", licoes)]}],
               "flow": {"phase": "app_v407_instalada_e_aceita; registros_fechados; aguarda_custodia_c21_c19_c20_c17c_e_auditada_da_gerencia",
                        "next_action": "nenhuma nesta referencia; a gerencia/custodia roda custodiar.py executar --versao v407 --publicar; AUDITADA/FECHADA no quadro sao atos da gerencia", "handles": []}}
    if SECO:
        print("[seco] ACOM transition rev", rev0, "->", json.dumps(changes, ensure_ascii=False)[:300])
        return
    rc, res, err = acom("transition", {"expected_revision": rev0, "event_id": "claude-app-orq-20261104-app-v407-instalada", "actor": {"id": QUEM, "kind": "agent"}, "changes": changes})
    print("ACOM transition rc", rc, (json.dumps(res, ensure_ascii=False)[:200] if not isinstance(res, str) else res[:300]), err[:200])
    rc, v1, err = acom("verify")
    print("ACOM verify rc", rc, "ok", v1["result"]["ok"], "revisao", v1["result"]["receipt"]["revision"])


def passo_quadro():
    ev = [str(p) for p in EVID]
    nota = ("App v407 instalado e aceito por revisores distintos do construtor (ORDEM_006); AUDITADA e FECHADA sao atos da gerencia. "
            "A F0.3 da v407 ja estava ativada; DELIVERY_TECHNICAL_R1.json escrito no esquema da fila.")
    cmd = [PY, "-B", "-X", "utf8", r"C:\IALD\PROGRAMA_IALD\iald.py", "avancar", task.UNIT, "--quem", QUEM, "--status", "ENTREGUE", "--evidencia", *ev, "--nota", nota]
    if SECO:
        print("[seco] quadro:", task.UNIT, "ENTREGUE", len(ev), "evidencias")
        return
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("QUADRO rc", p.returncode, (p.stdout or p.stderr)[-300:])


def passo_mapa():
    REG.mkdir(exist_ok=True)
    arte = [str(p) for p in EVID]
    base = {
        "rota_id": "app.release.v407", "dominio": "APP",
        "titulo": "release v407 do app: janela P2 deslizada de novo (sai _v402), F1 em registros de estatuto planos e escopo da instalacao MEDIDO; instalada e aceita",
        "pergunta": "A release v407 cabe nos pacotes do app com a janela P2 deslizada pela segunda vez, as lembrancas da v406 aplicadas (F1, escopo medido, D4 reescrito) e o que sobra da janela?",
        "dados": ["um.py v407 (pin %s) no espelho the_boundary, commit %s" % (cfg["um_py_sha256"][:16], cfg["espelho_commit"][:8]), "app instalado v406"],
        "metodo": "so' as ferramentas da v406 (28 arquivos, COPIA_DA_V406.json); SHARED_P2_SUFFIXES _v403.._v407 (_v402 aposentado com limites/diz/nao_diz mantidos); status_record() no codec (F1); "
                  "scope_snapshot/scope_compare em transaction.py (escopo medido); prepare e finalize offline; contagem nativa (6 pedidos, 0 geracao); validate_plan; busca exercitada; "
                  "revisor independente sonnet-app-v407-revisor (rodada 1: fontes e pacote; rodada 2: instalacao e verify); deploy_controlled; verify_installed",
        "nao_refazer": "A v407 esta instalada e aceita; nao reinstalar (deployment.json existente faz o deploy_controlled recusar). A v408 parte de work\\iald_v407_20261104 (LICOES_v407.md): "
                       "a janela P2 por deslize quase esgotou (folga minima %d B; tirar _v403 poupa ~3 KB), exige decisao de projeto da gerencia antes do finalize." % folga,
        "proximo_passo": "a gerencia/custodia roda custodiar.py executar --versao v407 --publicar (C21, C19, C20, C17C); v408: decidir a janela (LICOES_v407.md), estender o escopo medido aos 19 caminhos do B1 e ao cliente servido, surrogatepass (B2)",
        "onde": str(W), "artefatos": arte, "refs": ["app.release.v406", "app.release.v405"],
        "nota": "Construtora: claude-app-orquestrador (ORDEM_006); revisor sonnet-app-v407-revisor, 04/11/2026. Consulta ao mapa antes: 0 rotas app.release.v407. Nada tocou um.py, selo, kernel, gate, cofre nem Chatgpt\\.",
        "estatuto": "REAL", "olhou_dados": False,
    }
    rota = dict(base, tipo="ROTA", veredito="ROTA_ABERTA_ORDEM_006_APP_RELEASE_V407", status="EM_CURSO",
                resultado="rota aberta nesta etapa; o resultado entra no registro seguinte", defeito="ver o registro de resultado")
    resultado = dict(base, tipo="RESULTADO", resultado=RESULTADO_TXT, veredito="APP_V407_INSTALADO_E_ACEITO_NO_ESCOPO_DECLARADO", status="EXAMINADA",
                     defeito="sem resposta de modelo ao vivo nem celular fisico; BAIXOS B1 (escopo medido cobre 120+266 arquivos; 19 caminhos fora), B2 (nome de arquivo com substituto Unicode solitario), "
                             "B3 (a janela do shared quase esgotada: folga %d B), B4 (F1 chega ao haiku55 por inteiro, ao shared e ao sonnet_public so' nos topicos regenerados) e os da rodada 2 em PARECER_v407_R2.md" % folga)
    for nome, obj in (("rota_aberta_app.release.v407", rota), ("rota_resultado_app.release.v407", resultado)):
        p = REG / (nome + ".json")
        txt = json.dumps(obj, ensure_ascii=False, indent=1)
        if SECO:
            print("[seco] mapa", nome, len(txt), "B")
            continue
        novo(p, txt)
        r = subprocess.run([PY, "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(p), "--quem", QUEM], capture_output=True)
        print(nome, "rc", r.returncode, " ".join(r.stdout.decode("utf-8", "replace").split())[:230], r.stderr.decode("utf-8", "replace")[:300])


def passo_fila():
    REG.mkdir(exist_ok=True)
    texto = (
        "[REAL] 04/11/2026: app v407 INSTALADO (ORDEM_006), com o reinicio do filho web autorizado pelo operador no chat (a autorizacao da v406 nao valeu para a v407). "
        "%d arquivos, %d backups; web %d -> %d sob o mesmo supervisor %d em %d s; /login %d. O escopo da instalacao foi MEDIDO pela primeira vez (accounts_modified, bench_restarted e "
        "client_files_changed = false sobre 120 arquivos de estado e 266 de cliente; a cobertura do resto e' a varredura do revisor). verify_installed PASS em processo novo "
        "(release v407, JEV v407, 0 chamadas a provedor). Torre regenerada (%s) com o contrato jev_control_v407 pinado (sha256 %s). Revisores distintos do construtor aceitaram sources, app, deploy e verify.\n"
        "[REAL] Pacote: shared %d B; folga minima declarada %d B (DeepSeek; era 41975 na v406): a janela P2 por deslize esta quase esgotada (tirar _v402 poupou 2,7 KB, nao 27 KB); "
        "uma v408 do mesmo porte nao cabe sem decisao de projeto da gerencia. F1 (registros de estatuto planos) literal por inteiro no haiku55; so' nos topicos regenerados no shared e no sonnet_public.\n"
        "[REAL] Falta (da gerencia): custodiar.py executar --versao v407 --publicar (C21, C19, C20, C17C); AUDITADA/FECHADA da unidade %s. Continuam do operador: publicar, render final do filme, voz. "
        "Escopo: carregadores, hashes e login; sem resposta de modelo ao vivo nem celular fisico. Mapa: app.release.v407. Nada aqui e' selo nem move gate."
    ) % (inst["files_verified"], len(dep["backups"]), rest["old_web_pid"], rest["new_web_pid"], rest["supervisor_pid"], janela, rest["http_status"], torre_linha, nf["jev_control"]["sha256"][:16],
         sh["prefix_bytes"], folga, task.UNIT)
    tx = REG / "deposito_app_v407.md"
    novo(tx, texto)
    cmd = [PY, "-X", "utf8", str(FILA / "memoria.py"), "depositar", "--quem", QUEM, "--tipo", "project", "--estatuto", "REAL", "--alvo", "app-ciencia-propria-v395-24out.md",
           "--fonte", str(W / "INSTALLED_VERIFICATION.json"), "--fonte", str(W / "deployment.json"), "--fonte", str(licoes), "--texto-arquivo", str(tx), "--slug", "app-v407-instalado-04nov"]
    if SECO:
        print("[seco] fila:", " ".join(cmd[:8]), "...")
        return
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(FILA))
    print("FILA rc", p.returncode, (p.stdout or p.stderr)[-300:])


def passo_tunel():
    agora = datetime.now().astimezone().isoformat(timespec="seconds")
    arquivos = [pin(p) for p in (W / "RELEASE.json" if (W / "RELEASE.json").is_file() else W / "app" / "RELEASE.json", W / "deployment.json", W / "INSTALLED_VERIFICATION.json", licoes, contrato,
                                 F03 / "DELIVERY_TECHNICAL_R1.json", W / "validation/review_deploy.json", W / "validation/review_verify.json", parecer_r2)]
    res = {
        "ordem": "006 - release v407 do app, contrato JEV v407 e recibo da F0.3 no esquema da fila",
        "de": QUEM, "quando": agora, "estado": "cumprida",
        "escopo": "secoes 1 e 4 da ORDEM_006 e o item 1 do 'Ao lado' (DELIVERY_TECHNICAL_R1.json); a secao 2 (F0.3) ja estava feita e nao foi refeita; a secao 3 (tarefas agendadas) nao se repete, por ordem",
        "feito": {
            "release_v407": "instalada (%d arquivos, %d backups, 0 .py de runtime), reinicio do filho web autorizado pelo operador no chat; web %d -> %d, /login %d, janela %d s" % (
                inst["files_verified"], len(dep["backups"]), rest["old_web_pid"], rest["new_web_pid"], rest["http_status"], janela),
            "verify": "INSTALLED_VERIFICATION.json PASS, identity.release v407, JEV v407, 0 chamadas a provedor (carregadores em processo novo; sem resposta de modelo ao vivo nem celular fisico)",
            "nucleo_fixo": "iald_nucleo_fixo.json lido na fonte: operational_core.current_release v407; release_source_sha256 = pino do um.py (%s); jev_control.release v407; jev_control.sha256 = sha256 do arquivo do contrato (%s)" % (
                cfg["um_py_sha256"][:16], nf["jev_control"]["sha256"][:16]),
            "torre": torre_linha,
            "revisao": "sonnet-app-v407-revisor: sources e app (rodada 1); deploy e verify (rodada 2); 0 ALTO, 0 MEDIO; BAIXOS escritos em LICOES_v407.md",
            "f03": "DELIVERY_TECHNICAL_R1.json escrito no esquema da fila (release v407, status ACTIVATED_VERIFIED_...); a F0.3 nao foi refeita; nada foi escrito em Chatgpt\\",
        },
        "nao_feito": ["tarefas agendadas (nao repetidas, por ordem)", "publicar, render final do filme e voz (atos do operador)", "AUDITADA/FECHADA da unidade e custodiar.py --publicar (atos da gerencia/custodia)"],
        "aviso_para_a_v408": "a janela P2 do shared por deslize quase esgotou: folga minima declarada %d B (v406: 41975); uma v408 do mesmo porte exige decisao de projeto da gerencia antes do finalize (LICOES_v407.md)" % folga,
        "declarado": "o que este resultado traz e' DECLARADO ate a gerencia conferir na fonte (nucleo_fixo, INSTALLED_VERIFICATION, deployment); o escopo medido vale so' para os arquivos medidos",
        "arquivos": arquivos,
    }
    rp = TUNEL / "RESULTADOS" / "006_RESULTADO.json"
    novo(rp, json.dumps(res, ensure_ascii=False, indent=1))
    linhas = [
        "# Relatorio de %s - ORDEM_006 (release v407 do app)" % datetime.now().strftime("%d/%m/%Y"),
        "",
        "De: `claude-app-orquestrador`. Cumpre a ORDEM_006, secoes 1 e 4 e o item 1 do 'Ao lado'. Estado: **cumprida** (DECLARADO ate a gerencia conferir na fonte).",
        "",
        "1. **Release**: v407 instalada. %d arquivos, %d backups (carimbo `%s`), 0 `.py` de runtime. Reinicio do filho web autorizado pelo operador no chat (a autorizacao da v406 nao valeu para a v407)."
        % (inst["files_verified"], len(dep["backups"]), carimbo),
        "2. **Processos**: web %d -> %d sob o mesmo supervisor %d; `/login` %d; janela de %d s (mtime de `maintenance.json` a `restart.json`). Bancada (18765/18766) e modelo local (8081) nao tocados."
        % (rest["old_web_pid"], rest["new_web_pid"], rest["supervisor_pid"], rest["http_status"], janela),
        "3. **Escopo medido** (novo na v407): `accounts_modified`, `bench_restarted` e `client_files_changed` = false, medidos sobre 120 arquivos de estado e 266 de cliente (`errors` vazio). "
        "Valem so' para os arquivos medidos; a cobertura do resto (19 caminhos, B1) e' a varredura do revisor.",
        "4. **Verify**: `INSTALLED_VERIFICATION.json` PASS, `identity.release` v407, JEV v407, 0 chamadas a provedor. Escopo: carregadores, hashes e login; sem resposta de modelo ao vivo nem celular fisico.",
        "5. **Nucleo fixo lido na fonte**: `operational_core.current_release` v407; `release_source_sha256` = pino do `um.py` (`%s`); `jev_control.release` v407; `jev_control.sha256` = sha256 do arquivo do contrato (`%s`)."
        % (cfg["um_py_sha256"][:16], nf["jev_control"]["sha256"][:16]),
        "6. **Torre**: `torre.py gerar` rodado depois (%s)." % torre_linha,
        "7. **Revisao**: `sonnet-app-v407-revisor` (distinto do construtor) aceitou sources, app (rodada 1), deploy e verify (rodada 2). 0 ALTO, 0 MEDIO. BAIXOS: ver `LICOES_v407.md` e `PARECER_v407_R2.md`.",
        "8. **F0.3**: ja estava feita; escrito `DELIVERY_TECHNICAL_R1.json` no esquema da fila (mesmo fato, esquema do leitor). Nada escrito em `Chatgpt\\`.",
        "9. **Aviso para a v408**: a janela P2 do `shared` por deslize quase esgotou (folga minima declarada %d B; era 41975 na v406). Uma v408 do mesmo porte nao cabe sem decisao de projeto da gerencia (LICOES_v407.md)." % folga,
        "10. **Nao feito (por ordem ou por ser de outro)**: tarefas agendadas; publicar, render final e voz do filme (operador); AUDITADA/FECHADA e `custodiar.py executar --versao v407 --publicar` (gerencia/custodia).",
        "",
        "Resultado em `RESULTADOS\\006_RESULTADO.json`. Mapa: `app.release.v407`. Deposito: `memory\\fila\\depositos\\%s\\`. Quadro: `%s` ENTREGUE." % (QUEM, task.UNIT),
    ]
    rel = TUNEL / ("RELATORIO_%s.md" % datetime.now().strftime("%Y%m%d"))
    novo(rel, "\n".join(linhas) + "\n")
    print("TUNEL", rp, rel)


TODOS = {"acom": passo_acom, "quadro": passo_quadro, "mapa": passo_mapa, "fila": passo_fila, "tunel": passo_tunel}
if not PASSOS:
    sys.exit("passos: " + " ".join(TODOS))
for nome in PASSOS:
    assert nome in TODOS, nome
    TODOS[nome]()
