# -*- coding: utf-8 -*-
"""ORDEM ao orquestrador app: a release v408 do app, o contrato JEV v408 e a F0.3 (com a decisao D53 da gerencia sobre a janela P2 do shared).

Custodia v408, 05/11/2026, claude-site-custodia, pela ORDEM DE HANDOFF da gerencia c1 (work\\cadeia_de_selo\\v408\\ORDEM_HANDOFF_CUSTODIA_v408.md,
item 2: «A release v408 do app (C21): a ORDEM ao app no tunel ... pelo molde ... com a decisao D53»). O orquestrador da c1 foi PARADO antes do S10.
Reaproveita renderizar_ordem do proprio pos_treino_v408.py (importado; o main e guardado por __name__): versao, pino, commits e pasta anterior LIDOS.
Acrescenta, ao lado, o que mudou desde o molde. Grava com open('xb'): nunca sobrescreve ordem entregue."""
import hashlib
import importlib.util
import json
import re
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
ORQ = CEN / "work" / "cadeia_de_selo" / "v408" / "orquestrador"
TUN = Path(r"C:\IALD\TUNEL_CLAUDE_APP")
SELO = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json")
W = CEN / "work" / "custodia_v408_05nov"
HANDOFF = CEN / "work" / "cadeia_de_selo" / "v408" / "ORDEM_HANDOFF_CUSTODIA_v408.md"
ABROG = CEN / "work" / "abrogacao_04nov" / "OPERADOR_04nov_abrogacao_verbatim.txt"

spec = importlib.util.spec_from_file_location("pos_treino_v408", ORQ / "pos_treino_v408.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

selo = json.loads(SELO.read_text(encoding="utf-8"))
assert selo["um_version"] == "v408", selo["um_version"]
pin = selo["sha256"]["um.py"]
num = m._proximo_num_ordem(TUN)
txt = m.renderizar_ordem(num, selo, hoje="05/11/2026")


def s16(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]


lic = CEN / "work" / "iald_v407_20261104" / "LICOES_v407.md"
lt = lic.read_text(encoding="utf-8")
assert "34,26 s" in lt and "+29.323 B" in lt and "106.216 B" in lt, "as licoes da v407 mudaram: reler antes de citar"
dlv = CEN / "work" / "scientific_memory_sync_20261104_v407" / "DELIVERY_TECHNICAL_R1.json"
dj = json.loads(dlv.read_text(encoding="utf-8"))
assert dj.get("release") == "v407" and "v408 pede outra" in str(dj.get("authorization", "")), "o recibo da F0.3 da v407 mudou: reler"
ho = HANDOFF.read_text(encoding="utf-8")
assert "D53" in ho and "11.856 B" in ho
r006 = TUN / "RESULTADOS" / "006_RESULTADO.json"
assert json.loads(r006.read_text(encoding="utf-8")).get("estado") == "cumprida"

AO_LADO = """

---

## Ao lado (05/11/2026): o que mudou desde o molde. Escrito pela sessão de custódia, `claude-site-custodia`, pela ordem de handoff da gerência c1.

O orquestrador da c1 foi parado antes do S7 e do S10, porque os dois são da custódia (`{ho}`, sha16 `{ho16}`, item 2). Por isso esta ordem foi escrita pela custódia, com a função `renderizar_ordem` do próprio `pos_treino_v408.py`. Versão, pino e commits acima foram lidos do selo e do git. O espelho já está em v408; a Central pública (C18) e a medida final do organismo (C19) seguem com a custódia e não precisam esperar você.

**1. A janela P2 (D53) e os números da v407.** Em `{lic}` (sha16 `{lic16}`), item 1 e «para a próxima» item 1: o `shared` cresceu +29.323 B na v407, a folga ficou em 11.856 B, e o maior bloco é `_v405` (106.216 B). A D53 acima é a resposta da gerência: só v408 e v407 em literal completo; `_v403` a `_v406` viram tópicos regenerados. Meça antes do `finalize` e escreva no `LICOES_v408.md` os bytes por versão e a folga que sobrou.

**2. A F0.3 da v408 precisa de autorização nova do operador.** O recibo da v407 (`{dlv}`, sha16 `{dlv16}`) diz: «uma escrita única autorizada pelo operador … esgotada com a ativação; a v408 pede outra». Peça-lhe em uma linha, junto com o pedido de reinício, se houver. Sem a autorização, pare a seção 2 e diga isso no resultado. Ao entregar, escreva direto o `DELIVERY_TECHNICAL_R1.json` no esquema da fila (`release`, `status ACTIVATED_VERIFIED_…`, `epoch`, `generation`, `receipts` com sha256): é o que o quadro do organismo (C19/C20) lê.

**3. O reinício do filho web (porta 8082)** continua sendo do operador, por versão, em uma linha, com `quiet()` conferido e a janela medida da v407 (34,26 s; v406: 87 s). A autorização da v407 não vale para a v408.

**4. A seção 3 do molde (tarefas agendadas) não se repete.** Foi negada três vezes (`RESULTADOS\\004_RESULTADO.json`) e a ORDEM 006 já a tirou de vigência. Não contorne.

**5. Depois de você.** A custódia confere na fonte os quatro elos da seção 4 e roda de novo `custodiar.py executar --versao v408 --publicar` para fechar C21, C19, C20 e C17C. Entregue como manda a `ORDEM_001`, seção 6: `RESULTADOS\\{num}_RESULTADO.json` com `estado: cumprida` e aviso de até 15 linhas.

## Quadro de vigência deste túnel (regra do operador de 04/11/2026: o que foi cumprido ou superado não fica parecendo pendente)

Verbatim da regra: `{abrog}`, sha256 `{abrog_sha}`.

| Ordem | Estado | Por quê |
|---|---|---|
| `ORDEM_001`, `CANAL_DESASSISTIDO.md` | **VIGENTES** | quem você é e como entrega |
| ORDEM {num} (esta) | **VIGENTE** | a release v408 do app, o contrato JEV v408 e a F0.3 da v408 |
| ORDEM 006 | cumprida | a release v407 foi instalada em 04/11, de 14:51 a 14:52 (`RESULTADOS\\006_RESULTADO.json`) |
| ORDEM 005 | cumprida | `RESULTADOS\\005_RESULTADO.json` |
| ORDEM 004 | cumprida ou superada | como diz o quadro da ORDEM 006; a §3 não se repete |
| ORDENS 002 e 003 | esta ordem não as muda | o filme da v406 aguarda o operador escutar e decidir a voz |

— `claude-site-custodia`, em nome próprio, pela ordem de handoff da gerência c1, 05/11/2026.
""".format(ho=HANDOFF, ho16=s16(HANDOFF), lic=lic, lic16=s16(lic), dlv=dlv, dlv16=s16(dlv), num="%03d" % num,
           abrog=ABROG, abrog_sha=hashlib.sha256(ABROG.read_bytes()).hexdigest())
assert "{" not in AO_LADO, "chave sem valor"
full = (txt.rstrip("\n") + AO_LADO).encode("utf-8")
s = full.decode("utf-8")
assert pin in s and "v408" in s and "D53" in s
assert not re.search(r"\bindisponivel\b", s), "commit do git nao lido"
nome = "ORDEM_%03d_release_v408_do_app.md" % num
(W / nome).write_bytes(full)                # copia de trabalho
dst = TUN / nome
with dst.open("xb") as f:
    f.write(full)
assert dst.read_bytes() == full
print(nome, hashlib.sha256(full).hexdigest()[:16], len(full), "pino", pin[:16])
print([l for l in s.splitlines() if "commit" in l.lower()][:1][0][:420])
