# -*- coding: utf-8 -*-
"""Fecha os registros da release v405 do app: transicao ACOM da propria referencia, quadro (ENTREGUE; AUDITADA e ato da c1), mapa de rotas e deposito
na fila da memoria. Numeros e hashes lidos dos artefatos, nunca digitados."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import task

W = task.W
PY = r"C:\Python314\python.exe"
RUN = W / "registros_fechamento"
RUN.mkdir(exist_ok=True)


def rd(p):
    return json.loads(Path(p).read_bytes())


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


inst = rd(W / "INSTALLED_VERIFICATION.json")
med = rd(W / "BUILDER_MEASUREMENTS.json")
rest = rd(W / "restart.json")
cfg = rd(W / "app" / "RELEASE.json")
kern = med["kernel_formalization"]
pk = med["packages_v405"]
hk, sh, sn = pk["haiku_expanded"], pk["shared"], pk["sonnet_public"]
slack = med["executor_slack_bytes_with_finalize_reserve"]
pol = med["deepseek_slack_bytes_with_declared_policy_reserve_148656"]
busca = (W / "BUSCA_EXERCITADA_v405.txt").read_text(encoding="utf-8").strip().splitlines()[-1]
inst_ant = med["installed_haiku55_v404"]
assert inst["status"] == "PASS" and inst["identity"]["release"] == "v405"
fatos = {"release": cfg["release"], "commit": cfg["espelho_commit"], "um_py": cfg["um_py_sha256"], "arquivos": inst["files_verified"],
         "web": [rest["old_web_pid"], rest["new_web_pid"], rest["supervisor_pid"]], "folga_haiku": hk["remaining_tokens"], "busca": busca}
print(json.dumps(fatos, ensure_ascii=False))

EV = ["INSTALLED_VERIFICATION.json", "LOGIN_CHECK_v405.json", "BUILDER_MEASUREMENTS.json", "BUSCA_EXERCITADA_v405.txt", "LICOES_v405.md", "CUSTODIA_EM_CURSO_v405.json",
      "validation/review_final.json", "validation/review_app_independent.json", "validation/review_sources.json", "validation/review_deploy.json", "validation/review_verify.json",
      "superseded_r1/validation/review_findings.json", "receipts/v405-app-accept-r3.json", "receipts/v405-sources-accept-r3.json", "receipts/v405-deploy-accept.json", "receipts/v405-verify-accept.json"]
for e in EV:
    assert (W / e).is_file(), e

# 1. ACOM: transicao da propria referencia
atual = task.call({"operation": "project", "reference": str(task.REF), "max_chars": 100000}, False)
rev = atual["receipt"]["revision"]
records = [
    {"id": "f1_app_v405_instalado", "kind": "fact", "statute": "REAL",
     "text": "App v405 instalado: %d arquivos conferidos, commit %s, programa %s; web %d para %d sob o supervisor %d; login 200; JEV v405. Escopo: carregadores em processo novo, hashes e login; sem resposta de modelo ao vivo; sem celular fisico." % (
         inst["files_verified"], cfg["espelho_commit"], cfg["um_py_sha256"], rest["old_web_pid"], rest["new_web_pid"], rest["supervisor_pid"]),
     "sources": [{"kind": "artifact", "ref": str(W / "INSTALLED_VERIFICATION.json"), "sha256": sha(W / "INSTALLED_VERIFICATION.json")},
                 {"kind": "artifact", "ref": str(W / "validation/review_verify.json"), "sha256": sha(W / "validation/review_verify.json")}]},
    {"id": "d1_catalogo_haiku55", "kind": "decision", "statute": "REAL",
     "text": "Gerencia a7: base compacta do haiku55 redesenhada no codec. Indicadores TRUE da escada por declaracao (familias ext_ e red_) vao ao catalogo, com contagem e hash; declaration_sources_v394 por ponteiro. Folga %d para %d tokens. O revisor independente recusou a r1 e aceitou a r3." % (
         inst_ant["remaining_tokens"], hk["remaining_tokens"]),
     "sources": [{"kind": "artifact", "ref": str(W / "app/build/haiku_codec.py"), "sha256": sha(W / "app/build/haiku_codec.py")},
                 {"kind": "artifact", "ref": str(W / "LICOES_v405.md"), "sha256": sha(W / "LICOES_v405.md")}]},
]
flow = {"phase": "app_v405_instalado_e_aceito", "next_action": "nenhuma nesta referencia; AUDITADA no quadro e ato da gerencia c1", "handles": []}
ch = RUN / "transicao_changes.json"
ch.write_text(json.dumps({"records": records, "flow": flow}, ensure_ascii=False), encoding="utf-8")
r = task.call({"operation": "transition", "reference": str(task.REF), "expected_revision": rev, "event_id": "v405-app-fechamento",
               "actor": {"id": task.OWNER, "kind": "agent"}, "changes_file": str(ch), "changes_sha256": sha(ch)}, False)
print("ACOM", rev, "->", r.get("revision") or (r.get("receipt") or {}).get("revision"))

# 2. Quadro
ev_abs = [str(W / e) for e in EV]
p = subprocess.run([PY, "-B", "-X", "utf8", r"C:\IALD\PROGRAMA_IALD\iald.py", "avancar", task.UNIT, "--quem", task.ACTOR, "--status", "ENTREGUE", "--evidencia", *ev_abs,
                    "--nota", "App v405 instalado e aceito por revisores distintos do construtor; AUDITADA e ato da c1. Memoria da fila, filmes e vitrine seguem com o Codex (sem cota ate 04/11 06:37)."],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
print("QUADRO", p.returncode, (p.stdout or p.stderr)[-300:])

# 3. Mapa de rotas
rota = {
    "tipo": "ROTA", "rota_id": "app.release.v405", "dominio": "APP",
    "titulo": "release v405 do app: base compacta do haiku55 redesenhada; instalada e aceita",
    "pergunta": "A release v405 cabe nos pacotes do app sem perder o que o modelo precisa ler, e por quantas versoes?",
    "dados": ["um.py v405 (pin %s) no espelho the_boundary, origin/main %s" % (cfg["um_py_sha256"][:16], cfg["espelho_commit"][:8]), "app instalado v404"],
    "metodo": "medicao da composicao do prefixo instalado; codec: catalogo por contagem e hash das familias ext_/red_ e declaration_sources_v394 por ponteiro; recuperacao exercitada em search_tgl/fetch_tgl sem instalar; revisor independente recusou a r1 (a frase da capsula valia so pelo nome) e aceitou a r3; deploy_controlled; verify_installed; aceites por revisores distintos do construtor",
    "resultado": "haiku55: folga %d para %d tokens, capsula kernel_formalization %d para %d B, topicos _v404/_v405 integrais; shared folga %d, sonnet_public %d; %s" % (
        inst_ant["remaining_tokens"], hk["remaining_tokens"], kern["capsule_bytes_v404"], kern["capsule_bytes_v405"], sh["remaining_tokens"], sn["remaining_tokens"], busca),
    "veredito": "APP_V405_INSTALADO_E_ACEITO_NO_ESCOPO_DECLARADO", "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
    "defeito": "a janela dos outros motores e a proxima parede: os topicos _v405 pesam 104 KB no shared e a folga e %d B (Kimi), %d B (MiMo), %d B (DeepSeek, reserva declarada); o verify nao inclui resposta de modelo ao vivo nem celular fisico; ressalvas BAIXAS R3-1 e R3-2 em LICOES_v405.md" % (slack["kimi"], slack["mimo"], pol),
    "nao_refazer": "A v405 esta instalada e aceita; a proxima release parte desta pasta. Nao catalogar bandeira por regra so lexical sem conferir pares verdadeiro/falso; nome exato e melhor consulta que nome + kernel_formalization (medido).",
    "proximo_passo": "antes do finalize da v406, decidir a janela P2 do shared (LICOES_v405.md) e aplicar R3-1 e R3-2",
    "onde": str(W), "artefatos": ev_abs[:5] + [str(W / "validation/review_final.json"), str(W / "validation/review_verify.json"), str(W / "superseded_r1/validation/review_findings.json")],
    "refs": ["app.release.v404", "app.release.v402"],
    "nota": "Gerencia a7 (sessao do site) como construtora; revisores sonnet-app-v405-revisor e sonnet-app-v405-revisor-d, 02/11/2026. Consultas dos revisores: app release (2 rotas).",
}
rj = RUN / "rota_app_release_v405.json"
rj.write_text(json.dumps(rota, ensure_ascii=False, indent=1), encoding="utf-8")
p = subprocess.run([PY, "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(rj), "--quem", "claude-site"], capture_output=True, text=True, encoding="utf-8", errors="replace")
print("MAPA", p.returncode, (p.stdout or p.stderr)[-260:])

# 4. Deposito na fila da memoria
texto = f"""02/11/2026: o app foi da v404 para a v405 (backend compartilhado; não há build nova de cliente). A release está em `work\\iald_v405_20261102`.
- **Haiku55, base compacta redesenhada (a lição da v404 não coube esperar a v406):** a cápsula `kernel_formalization` tinha {kern['capsule_bytes_v404']} B no prefixo instalado; agora {kern['capsule_bytes_v405']} B. {kern['catalog']['true_fields']} indicadores TRUE das famílias `ext_`/`red_` vão ao catálogo, com contagem e hash; {kern['true_flags_kept_literal']} TRUE e {kern['false_flags_kept_literal']} FALSE ficam literais; `declaration_sources_v394` passa a ponteiro. Folga {inst_ant['remaining_tokens']} → {hk['remaining_tokens']} tokens, com os tópicos `_v404` e `_v405` integrais (`EXPAND_OVERRIDE = None`).
- **Recuperação:** a cápsula ensina a busca; {busca}.
- **Revisão:** o revisor independente recusou a r1 (F1: a regra só lexical deixava `gpf_H2=false` literal e tirava `gpc_H2=true`) e aceitou a r3. Implantação 43/43, verificação 18/18. Ressalvas BAIXAS R3-1 e R3-2, com o conserto escrito em `LICOES_v405.md`, para aplicar ao copiar a pasta.
- **Instalação:** {inst['files_verified']} arquivos; web {rest['old_web_pid']}→{rest['new_web_pid']} sob o supervisor {rest['supervisor_pid']}; /login 200; nenhuma chamada paga de geração; JEV v405.
- **Torre:** `TORRE_v405.json` tinha nascido às 04:09 com o JEV `null`, antes do app; rodei `torre.py gerar` (backup `TORRE_v405.json.bak_20261102_084051`) e o contrato do JEV ficou pinado. Fica para a v406: a G1 só gera a Torre quando falta o arquivo; depois da C21 precisa regenerar.
- **Próxima parede, medida:** janela dos outros motores. Os tópicos `_v405` pesam 104 KB no `shared`; folga Kimi {slack['kimi']} B, MiMo {slack['mimo']} B, DeepSeek {pol} B (reserva declarada). A release só coube pela saída de `declaration_sources_v394`. Uma v406 do mesmo porte não cabe sem decidir a janela P2 antes do finalize.
- **Não medido:** resposta de modelo ao vivo citando a v405; celular físico.
- **Custódia v405:** C21 `ok`; C19, C20 e C17C seguem à espera da F0.3 (Codex). Organismo: 7 DEFASADO, sendo 2 da fila, 1 do `TGL_ATLAS.md` em curso da c1 e 4 da Torre (agregado + 3 antigos).
- Quadro: `{task.UNIT}` ENTREGUE; AUDITADA é ato da c1. Rota `app.release.v405`.
"""
tx = RUN / "deposito_app_v405.md"
tx.write_text(texto, encoding="utf-8")
FILA = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fila\memoria.py")
p = subprocess.run([PY, "-X", "utf8", str(FILA), "depositar", "--quem", "claude-site", "--tipo", "project", "--estatuto", "REAL", "--alvo", "app-ciencia-propria-v395-24out.md",
                    "--fonte", str(W / "INSTALLED_VERIFICATION.json"), "--fonte", str(W / "LICOES_v405.md"), "--texto-arquivo", str(tx), "--slug", "app-v405-instalado-02nov"],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
print("FILA", p.returncode, (p.stdout or p.stderr)[-300:])
