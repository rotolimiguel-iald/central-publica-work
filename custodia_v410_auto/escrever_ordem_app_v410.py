# -*- coding: utf-8 -*-
"""ORDEM ao executor do app no tunel: a release v410 do app, o contrato JEV v410 e a F0.3 da v410 (D53 em vigor: literal completo so v410 e v409).
Custodia v410, claude-site-custodia, pela ordem do operador de 10/11/2026 (verbatim abaixo; tudo desassistido). Molde: o da v408 com as substituicoes
conferidas da v409 (escrever_ordem_009_app.py). Valores LIDOS do selo e do git; so roda depois do push do espelho (E11). Grava com open('xb').
Se existir um verbatim do operador autorizando o reinicio da v410 (work\\cunhagens_13out\\OPERADOR_*reinicio*v410*verbatim.txt), a ordem o cita."""
import glob
import hashlib
import json
import re
import subprocess
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
TUN = Path(r"C:\IALD\TUNEL_CLAUDE_APP")
SELO = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json")
TB = Path(r"C:\IALD\Artigo\the_boundary")
W = CEN / "work" / "custodia_v410_auto"
TPL8 = CEN / "work" / "cadeia_de_selo" / "v408" / "orquestrador" / "ORDEM_RELEASE_APP_TEMPLATE.md"
ORD = CEN / "work" / "cunhagens_13out" / "OPERADOR_10nov_v410_atualize_e_publique_tudo_desassistido_verbatim.txt"
FRASE = "quando isso acontecer quero que vc atualize tudo e publique tudo"
ANT = CEN / "work" / "iald_v409_20261106"
LICS = [ANT / "LICOES_v409.md", ANT / "LICOES_v409_COMPLEMENTO.md"]
ABROG = CEN / "work" / "abrogacao_04nov" / "OPERADOR_04nov_abrogacao_verbatim.txt"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git(repo, *a):
    r = subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


selo = json.loads(SELO.read_text(encoding="utf-8"))
assert selo["um_version"] == "v410", selo["um_version"]
pin = selo["sha256"]["um.py"]
assert FRASE in ORD.read_text(encoding="utf-8")
esp, cen = git(TB, "rev-parse", "--short=8", "HEAD"), git(CEN, "rev-parse", "--short=8", "HEAD")
assert esp == git(TB, "rev-parse", "--short=8", "origin/main"), "o espelho ainda nao foi empurrado: a ordem sai depois do E11"
for p in LICS:
    assert p.is_file(), p
reinicio = sorted(glob.glob(str(CEN / "work" / "cunhagens_13out" / "OPERADOR_*reinicio*v410*verbatim.txt")))

t = TPL8.read_text(encoding="utf-8")
subs = [
    ("De: o orquestrador da cadeia de selo da gerência c1 (`pos_treino_{{VN}}.py`, passo S10, automático).",
     "De: a sessão de custódia (`claude-site-custodia`), pela ordem de handoff da gerência c1 (a cadeia da {{VN}} termina no handoff e não tem S10)."),
    ("A cadeia (`pos_treino_{{VN}}.py`, passo S10) espera, por até 24 h, ao mesmo tempo:", "A custódia espera, ao mesmo tempo:"),
    ("Sem recibo em 24 h a cadeia PARA, visível, e a gerência decide; nunca marca «ok» sem a conferência.",
     "Sem recibo, o C21 da custódia fica aberto, visível; nunca se marca «ok» sem a conferência."),
    ("— O orquestrador da cadeia de selo ({{VN}}), em nome da gerência c1, {{DATA}}.", "— `claude-site-custodia`, pela ordem de handoff da gerência c1, {{DATA}}."),
    ("## 3. As duas tarefas agendadas (se ainda não existem)\n\n`IALD X diario` (18:00) e `IALD ronda da fila` (08:30). Se a criação for negada, diga em uma linha e não contorne.",
     "## 3. As tarefas agendadas\n\nNão se repetem por esta ordem: a criação foi negada três vezes (`RESULTADOS\\004_RESULTADO.json`) e a ORDEM 006 as tirou de vigência."),
]
for a, b in subs:
    assert t.count(a) == 1, ("trecho do molde nao encontrado uma vez", a[:80])
    t = t.replace(a, b)
m = re.search(r"Ordem do operador \(verbatim em `[^`]+`, sha16 `\{\{SHA16_ORDEM\}\}`\): «[^»]+»;", t)
assert m
t = t.replace(m.group(0), "Ordem do operador (verbatim em `%s`, sha16 `{{SHA16_ORDEM}}`): «%s»;" % (ORD, FRASE))
nums = [int(mm.group(1)) for p in TUN.glob("ORDEM_*.md") for mm in [re.match(r"ORDEM_(\d+)_", p.name)] if mm]
num = max(nums) + 1
for k, v in {"NUM": "%03d" % num, "VN": "v410", "VANT": "v409", "PIN": pin, "PIN16": pin[:16], "DATA": __import__("time").strftime("%d/%m/%Y"),
             "SHA16_ORDEM": sha(ORD)[:16], "COMMIT_ESPELHO": esp, "COMMIT_CENTRAL": cen, "PASTA_ANTERIOR": "`%s`" % ANT}.items():
    t = t.replace("{{%s}}" % k, v)
assert "{{" not in t

reinicio_txt = ("**3. O reinício do filho web (porta 8082):** autorizado pelo operador para a v410 (verbatim em `%s`, sha16 `%s`). Confira `quiet()` antes e meça a janela."
                % (reinicio[-1], sha(reinicio[-1])[:16])) if reinicio else \
               "**3. O reinício do filho web (porta 8082)** é do operador, por versão, em uma linha, com `quiet()` conferido."
AO_LADO = """

---

## Ao lado: o que mudou desde o molde

**1. As lições da v409** estão em {lics}. Leia as duas inteiras antes de construir; aplique a D53 (só v410 e v409 em literal completo) e meça a folga antes do `finalize`.
**2. A F0.3:** confira as coordenadas de todos os trechos e a igualdade dos hashes nos caminhos definitivos antes do CAS; entregue o `DELIVERY_TECHNICAL_R1.json` no esquema da fila.
{reinicio}
**4. As cópias da memória ACOM:** regra do operador de 08/11 — só as três mais recentes; nada vai para o arquivo do D:.

## Quadro de vigência deste túnel (regra do operador de 04/11/2026)

Verbatim da regra: `{abrog}`, sha256 `{abrog_sha}`.

| Ordem | Estado | Por quê |
|---|---|---|
| `ORDEM_001`, `CANAL_DESASSISTIDO.md` | **VIGENTES** | quem você é e como entrega |
| ORDEM {num} (esta) | **VIGENTE** | a release v410 do app, o contrato JEV v410 e a F0.3 da v410 |
| ORDEM 009 | cumprida | a release v409 (`RESULTADOS\\009_RESULTADO.json`) |
| ORDENS 004 a 008 | cumpridas, superadas ou sem objeto | como dizem os quadros da 006, da 007 e da 009 |
| ORDENS 002 e 003 | esta ordem não as muda | o filme da v406 aguarda o operador escutar e decidir a voz |
""".format(lics=" e ".join("`%s` (sha16 `%s`)" % (p, sha(p)[:16]) for p in LICS), reinicio=reinicio_txt, abrog=ABROG, abrog_sha=sha(ABROG), num="%03d" % num)
full = (t.rstrip("\n") + AO_LADO).encode("utf-8")
s = full.decode("utf-8")
assert pin in s and "v410" in s and "D53" in s
nome = "ORDEM_%03d_release_v410_do_app.md" % num
W.mkdir(parents=True, exist_ok=True)
(W / nome).write_bytes(full)
with (TUN / nome).open("xb") as f:
    f.write(full)
print(nome, hashlib.sha256(full).hexdigest()[:16], len(full), "pino", pin[:16], "espelho", esp, "central", cen, "| reinicio autorizado:", bool(reinicio))
