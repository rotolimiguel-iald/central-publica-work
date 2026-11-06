# -*- coding: utf-8 -*-
"""ORDEM ao orquestrador app: a release v409 do app, o contrato JEV v409 e a F0.3 da v409 (D53 em vigor).
Custodia v409, 06/11/2026, claude-site-custodia, pela ORDEM DE HANDOFF da gerencia c1 (work\\cadeia_de_selo\\v409\\ORDEM_HANDOFF_CUSTODIA_v409.md,
item 2: «pelo molde da v408 ..., rotulos 408->409, placeholders lidos do selo e do git»). A cadeia da v409 nao tem S10 (D57): a ordem e da custodia.
O molde da v408 e adaptado por substituicoes conferidas (cada trecho tem de existir uma vez) e gravado ao lado como molde da v409.
Valores LIDOS do selo e do git; grava com open('xb')."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
TUN = Path(r"C:\IALD\TUNEL_CLAUDE_APP")
SELO = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json")
TB = Path(r"C:\IALD\Artigo\the_boundary")
W = CEN / "work" / "custodia_v409_06nov"
TPL8 = CEN / "work" / "cadeia_de_selo" / "v408" / "orquestrador" / "ORDEM_RELEASE_APP_TEMPLATE.md"
HO = CEN / "work" / "cadeia_de_selo" / "v409" / "ORDEM_HANDOFF_CUSTODIA_v409.md"
ORD = CEN / "work" / "cunhagens_13out" / "OPERADOR_05nov_energia_caiu_de_novo_continue_ate_v409_publicada_verbatim.txt"
FRASE = "energia caiu de novo, continue até termos a v409 publicada"
LIC8 = CEN / "work" / "iald_v408_20261105" / "LICOES_v408.md"
ABROG = CEN / "work" / "abrogacao_04nov" / "OPERADOR_04nov_abrogacao_verbatim.txt"
PASTA_ANT = CEN / "work" / "iald_v408_20261105"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def head(repo):
    r = subprocess.run(["git", "-C", str(repo), "rev-parse", "--short=8", "HEAD"], capture_output=True, text=True, timeout=60)
    assert r.returncode == 0 and r.stdout.strip(), r.stderr
    return r.stdout.strip()


def origin(repo):
    r = subprocess.run(["git", "-C", str(repo), "rev-parse", "--short=8", "origin/main"], capture_output=True, text=True, timeout=60)
    return r.stdout.strip()


selo = json.loads(SELO.read_text(encoding="utf-8"))
assert selo["um_version"] == "v409", selo["um_version"]
pin = selo["sha256"]["um.py"]
assert FRASE in ORD.read_text(encoding="utf-8"), "a frase do operador nao esta no verbatim"
lt = LIC8.read_text(encoding="utf-8")
assert '"slack": 14757' in lt and "838165 bytes" in lt, "as licoes da v408 mudaram: reler antes de citar"
esp, cen = head(TB), head(CEN)
assert esp == origin(TB), "o espelho ainda nao foi empurrado: a ordem sai depois do E11"

t = TPL8.read_text(encoding="utf-8")
subs = [
    ("De: o orquestrador da cadeia de selo da gerência c1 (`pos_treino_{{VN}}.py`, passo S10, automático).",
     "De: a sessão de custódia (`claude-site-custodia`), pela ordem de handoff da gerência c1 (pela D57, a cadeia da {{VN}} termina no handoff e não tem S10)."),
    ("A cadeia (`pos_treino_{{VN}}.py`, passo S10) espera, por até 24 h, ao mesmo tempo:", "A custódia espera, ao mesmo tempo:"),
    ("Sem recibo em 24 h a cadeia PARA, visível, e a gerência decide; nunca marca «ok» sem a conferência.",
     "Sem recibo, o C21 da custódia fica aberto, visível; nunca se marca «ok» sem a conferência."),
    ("— O orquestrador da cadeia de selo ({{VN}}), em nome da gerência c1, {{DATA}}.",
     "— `claude-site-custodia`, pela ordem de handoff da gerência c1, {{DATA}}."),
    ("## 3. As duas tarefas agendadas (se ainda não existem)\n\n`IALD X diario` (18:00) e `IALD ronda da fila` (08:30). Se a criação for negada, diga em uma linha e não contorne.",
     "## 3. As tarefas agendadas\n\nNão se repetem por esta ordem: a criação foi negada três vezes (`RESULTADOS\\004_RESULTADO.json`) e a ORDEM 006 as tirou de vigência."),
]
for a, b in subs:
    assert t.count(a) == 1, ("trecho do molde nao encontrado uma vez", a[:80], t.count(a))
    t = t.replace(a, b)
m = re.search(r"Ordem do operador \(verbatim em `[^`]+`, sha16 `\{\{SHA16_ORDEM\}\}`\): «[^»]+»;", t)
assert m, "o trecho da ordem do operador mudou no molde"
t = t.replace(m.group(0), "Ordem do operador (verbatim em `%s`, sha16 `{{SHA16_ORDEM}}`): «%s»; e a autorização de publicar dada por ele à custódia em 06/11/2026 («Publicar tudo agora»);" % (ORD, FRASE))
tpl9 = W / "ORDEM_RELEASE_APP_TEMPLATE_v409.md"
tpl9.write_bytes(t.encode("utf-8"))

nums = [int(mm.group(1)) for p in TUN.glob("ORDEM_*.md") for mm in [re.match(r"ORDEM_(\d+)_", p.name)] if mm]
num = max(nums) + 1
vals = {"NUM": "%03d" % num, "VN": "v409", "VANT": "v408", "PIN": pin, "PIN16": pin[:16], "DATA": "06/11/2026", "SHA16_ORDEM": sha(ORD)[:16],
        "COMMIT_ESPELHO": esp, "COMMIT_CENTRAL": cen, "PASTA_ANTERIOR": "`%s`" % PASTA_ANT}
for k, v in vals.items():
    t = t.replace("{{%s}}" % k, v)
assert "{{" not in t, "placeholder sem valor"

AO_LADO = """

---

## Ao lado (06/11/2026): o que mudou desde o molde da v408

**1. As lições da v408** estão em `{lic}` (sha16 `{lic16}`). Com só v408 e v407 em literal, o pacote do `shared` ficou em 838.165 B, e a folga mínima declarada foi 14.757 B (DeepSeek; Kimi 18.146; MiMo 14.774). Pela D53, agora ficam v409 e v408 em literal, e a v407 vira tópico regenerado. Meça antes do `finalize` e escreva no `LICOES_v409.md` os bytes por versão e a folga. Se não couber, proponha o teto com os números, sem deslizar por adivinhação.
**2. Lição da F0.3 da v408:** antes do CAS, confira as coordenadas de todos os trechos e a igualdade dos hashes nos caminhos definitivos. Entregue o `DELIVERY_TECHNICAL_R1.json` direto no esquema da fila.
**3. O reinício do filho web (porta 8082)** é do operador, por versão, em uma linha, com `quiet()` conferido.
**4. Os instantâneos da ACOM** (lição da v408) já foram reconciliados em 05/11: 3 locais, os mais velhos no arquivo `D:\\`, restauração isolada verificada (`work\\custodia_v408_05nov\\RESTAURACAO_SNAPSHOT_ACOM_v408.json`). Nada a fazer.

## Quadro de vigência deste túnel (regra do operador de 04/11/2026)

Verbatim da regra: `{abrog}`, sha256 `{abrog_sha}`.

| Ordem | Estado | Por quê |
|---|---|---|
| `ORDEM_001`, `CANAL_DESASSISTIDO.md` | **VIGENTES** | quem você é e como entrega |
| ORDEM {num} (esta) | **VIGENTE** | a release v409 do app, o contrato JEV v409 e a F0.3 da v409 |
| ORDEM 007 | cumprida | a release v408 (`RESULTADOS\\007_RESULTADO.json`, estado cumprida) |
| ORDEM 008 | sem objeto | ab-rogava a 007, mas a 007 já tinha sido cumprida quando a 008 foi escrita |
| ORDENS 004, 005 e 006 | cumpridas ou superadas | como dizem os quadros da 006 e da 007 |
| ORDENS 002 e 003 | esta ordem não as muda | o filme da v406 aguarda o operador escutar e decidir a voz |
""".format(lic=LIC8, lic16=sha(LIC8)[:16], abrog=ABROG, abrog_sha=sha(ABROG), num="%03d" % num)
assert "{" not in AO_LADO.replace("{{", "")
full = (t.rstrip("\n") + AO_LADO).encode("utf-8")
s = full.decode("utf-8")
assert pin in s and "v409" in s and "D53" in s and "v408" in s
nome = "ORDEM_%03d_release_v409_do_app.md" % num
(W / nome).write_bytes(full)
dst = TUN / nome
with dst.open("xb") as f:
    f.write(full)
assert dst.read_bytes() == full
print(nome, hashlib.sha256(full).hexdigest()[:16], len(full), "pino", pin[:16], "espelho", esp, "central", cen)
