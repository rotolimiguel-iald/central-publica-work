# -*- coding: utf-8 -*-
"""ORDEM 006 ao orquestrador app: a release v407 do app e o contrato JEV v407.

Custodia v407, 04/11/2026, claude-site-custodia, por encargo da gerencia c1 («Depois da publicacao: a ORDEM de release v407 ao app pelo
tunel C:\\IALD\\TUNEL_CLAUDE_APP (molde em work\\cadeia_de_selo\\v407\\orquestrador\\ORDEM_RELEASE_APP_TEMPLATE.md) ... Nao relance o
orquestrador pos_treino_v407»). O S10 da cadeia nao rodou (a cadeia parou em S7). Reaproveita a funcao renderizar_ordem do proprio
pos_treino_v407.py (importada; o main dele e guardado por __name__ e nao roda): versao, pino, commits e pasta anterior LIDOS, nunca
digitados. Acrescenta, ao lado, o que mudou desde o molde. Grava com open('xb'): nunca sobrescreve ordem entregue."""
import hashlib
import importlib.util
import json
import re
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
ORQ = CEN / "work" / "cadeia_de_selo" / "v407" / "orquestrador"
TUN = Path(r"C:\IALD\TUNEL_CLAUDE_APP")
SELO = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json")
W = CEN / "work" / "custodia_v407_04nov"

spec = importlib.util.spec_from_file_location("pos_treino_v407", ORQ / "pos_treino_v407.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

selo = json.loads(SELO.read_text(encoding="utf-8"))
assert selo["um_version"] == "v407", selo["um_version"]
pin = selo["sha256"]["um.py"]
num = m._proximo_num_ordem(TUN)
txt = m.renderizar_ordem(num, selo, hoje="04/11/2026")


def s16(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]


dlv = CEN / "work" / "scientific_memory_sync_20261104_v407" / "DELIVERY_v407.json"
d = json.loads(dlv.read_text(encoding="utf-8"))
assert d.get("versao") == "v407" and str(d.get("estado", "")).startswith("ATIVADA"), (d.get("versao"), d.get("estado"))
lic = CEN / "work" / "iald_v406_20261103" / "LICOES_v406.md"
lic_lado = CEN / "work" / "iald_v406_20261103" / "LICOES_v406_AO_LADO.md"
lt = lic.read_text(encoding="utf-8")
assert "41.975 B" in lt and "_v402" in lt, "as licoes da v406 mudaram: reler antes de citar"
ord004 = TUN / "ORDEM_004_release_v406_do_app_jev_f03_e_tarefas.md"
rel_lado = TUN / "RELATORIO_20261103_AO_LADO.md"

AO_LADO = """

---

## Ao lado (04/11/2026): o que mudou desde o molde. Escrito pela sessão de custódia, `claude-site-custodia`, por encargo da gerência c1.

O S10 da cadeia não rodou, porque a cadeia parou em S7 e a gerência mandou não relançá-la. Por isso esta ordem foi escrita pela custódia, com a função `renderizar_ordem` do próprio `pos_treino_v407.py`. Versão, pino e commits acima foram lidos do selo e do git. A custódia da v407 está **PUBLICADA**: espelho, site, Central, Central pública, conferência final, ACOM t2 e rota `custodia.v407`. A medida final do organismo (C19) espera só esta release e os dois recibos abaixo.

**1. A F0.3 da v407 já foi feita por você. Não refaça a seção 2 do molde.**
O recibo é `{dlv}` (sha16 `{dlv16}`), estado `{estado}`. Ele também está no seu `RELATORIO_20261103_AO_LADO.md`, §6.
Falta só um recibo no esquema que o quadro do organismo lê: o C19 procura `DELIVERY_*R1.json` com `release` e `status` começando por `ACTIVATED_VERIFIED`. O seu recibo usa `versao` e `estado`, por isso o quadro marca «nenhuma».
Escreva, na mesma pasta, `DELIVERY_TECHNICAL_R1.json` no esquema da fila. O molde é `work\\scientific_memory_sync_20261028_v404_R2\\DELIVERY_TECHNICAL_R1.json`:
- `release`, `epoch` e `generation` lidos do seu `CHECK_DEPOIS_v407.json` e do `selo_lido_no_nos`;
- `status` = `ACTIVATED_VERIFIED_` mais o que valer;
- `independent_review` apontando para o parecer;
- `provider_calls` = 0;
- `receipts` com o caminho e o sha256 do `DELIVERY_v407.json`.
Nada novo é afirmado: é o mesmo fato no esquema do leitor. Isso não escreve em `Chatgpt\\`.

**2. As lições da v406 que entram antes de construir.** Elas estão em `{lic}` (sha16 `{lic16}`), na seção «para a próxima», e em `{lic_lado}` (sha16 `{lado16}`), lições 3, 5 e 6.
- Na v406, a folga mínima declarada da janela P2 foi **41.975 B** (DeepSeek; Kimi 45.364; MiMo 41.992). Uma release de cerca de 30 KB no `shared` consome três quartos disso. Por isso sai `_v402`: entra em `P2_RETIRED_LITERAL_SUFFIXES` e deixa `SHARED_P2_SUFFIXES`, com os literais `limites`/`diz`/`nao_diz` mantidos. Se a v407 for do porte da v405, sai também `_v403`.
- O F1 do parecer (`protected_fields` e o `name_status`) entra antes de construir.
- Na revisão da instalação:
  - reescreva o D4: o manifesto ativo sai do «baseline intacto» e os logs do supervisor entram na varredura;
  - **meça** `accounts_modified`, `bench_restarted` e `client_files_changed`, em vez de lê-los de constante.
- Confira `quiet()` antes de pedir o reinício.

**3. O reinício do filho web (porta 8082).** Se a instalação exigir reinício, ele continua sendo do operador, como diz o molde. Peça em uma linha só, com `quiet()` conferido e a janela medida da v406, 87 s. Ele autorizou o reinício da v406 no chat em 03/11. A autorização não se estende à v407.

**4. As tarefas agendadas.** A seção 3 do molde **não se repete por esta ordem.** A criação foi negada três vezes pelo classificador (`RESULTADOS\\004_RESULTADO.json`). Não contorne.

**5. Depois de você.** A custódia roda de novo `custodiar.py executar --versao v407 --publicar`. Esse passo fecha C21, C19, C20 e C17C, conferindo na fonte os quatro elos da seção 4 do molde e o `DELIVERY_TECHNICAL_R1.json` do item 1. Entregue como manda a `ORDEM_001`, seção 6.

## Quadro de vigência deste túnel (regra do operador de 04/11/2026: o que foi cumprido ou superado não fica parecendo pendente)

Verbatim da regra: `{verb}`, sha256 `{verb_sha}`.

| Ordem | Estado | Por quê |
|---|---|---|
| `ORDEM_001`, `CANAL_DESASSISTIDO.md` | **VIGENTES** | quem você é e como entrega |
| ORDEM 006 (esta) | **VIGENTE** | a release v407 do app e o recibo da F0.3 no esquema da fila |
| ORDEM 004, §1 | cumprida | a v406 foi instalada em 03/11, de 20:18 a 20:20 (`RELATORIO_20261103_AO_LADO.md`, §3) |
| ORDEM 004, §2 | superada | a F0.3 foi feita direto para a v407 em 04/11 (§6 do mesmo relatório) |
| ORDEM 004, §3 | sem nova tentativa | negada três vezes; esta ordem não a repete |
| ORDEM 004, §§4 e 5 | superadas por esta ordem | o C21 da v406 deixa de ser alvo; o automático do S10 não rodou na v407 |
| ORDEM 005 | cumprida | `RESULTADOS\\005_RESULTADO.json` |
| ORDENS 002 e 003 | esta ordem não as muda | o filme da v406 aguarda o operador escutar e decidir a voz |

— `claude-site-custodia`, em nome próprio, por encargo da gerência c1, 04/11/2026.
""".format(dlv=dlv, dlv16=s16(dlv), estado=d["estado"], lic=lic, lic16=s16(lic), lic_lado=lic_lado, lado16=s16(lic_lado),
           verb=CEN / "work" / "abrogacao_04nov" / "OPERADOR_04nov_abrogacao_verbatim.txt",
           verb_sha=hashlib.sha256((CEN / "work" / "abrogacao_04nov" / "OPERADOR_04nov_abrogacao_verbatim.txt").read_bytes()).hexdigest())
assert "{" not in AO_LADO.replace("{{", ""), "chave sem valor"
full = (txt.rstrip("\n") + AO_LADO).encode("utf-8")
assert pin in full.decode("utf-8") and "v407" in full.decode("utf-8")
nome = "ORDEM_%03d_release_v407_do_app.md" % num
(W / nome).write_bytes(full)                # copia de trabalho
dst = TUN / nome
with dst.open("xb") as f:
    f.write(full)
assert dst.read_bytes() == full
print(nome, hashlib.sha256(full).hexdigest()[:16], len(full), "pino", pin[:16])
print([l for l in full.decode("utf-8").splitlines() if "commit" in l.lower()][:1][0][:400])
