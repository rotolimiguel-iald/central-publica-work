# -*- coding: utf-8 -*-
"""ORDEM 008 ao orquestrador app: AB-ROGA a ORDEM 007 (release v408), cumprida por outro executor antes de o app reconectar.
Custodia v408, 05/11/2026, claude-site-custodia. Regra do operador de 04/11 (ab-rogacao): o que perdeu o objeto nao fica vivo no tunel.
Os fatos sao LIDOS na fonte (nucleo do app, contrato JEV, INSTALLED_VERIFICATION, DELIVERY da F0.3). Grava com open('xb')."""
import hashlib
import json
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
TUN = Path(r"C:\IALD\TUNEL_CLAUDE_APP")
SELO = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json")
NUC = Path(r"C:\IALD\projetos_pyhton\IALD\iald_nucleo_fixo.json")
IV = CEN / "work" / "iald_v408_20261105" / "INSTALLED_VERIFICATION.json"
F03 = CEN / "work" / "scientific_memory_sync_20261105_v408" / "DELIVERY_TECHNICAL_R1.json"
O7 = TUN / "ORDEM_007_release_v408_do_app.md"
ABROG = CEN / "work" / "abrogacao_04nov" / "OPERADOR_04nov_abrogacao_verbatim.txt"
W = CEN / "work" / "custodia_v408_05nov"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


selo = json.loads(SELO.read_text(encoding="utf-8"))
pin = selo["sha256"]["um.py"]
assert selo["um_version"] == "v408"
n = json.loads(NUC.read_text(encoding="utf-8"))
oc, jc = n.get("operational_core") or {}, n.get("jev_control") or {}
jp = Path(str(jc.get("path", "")))
assert oc.get("current_release") == "v408" and oc.get("release_source_sha256") == pin
assert jc.get("release") == "v408" and jc.get("source_sha256") == pin and jp.name == "jev_control_v408.json" and sha(jp) == jc.get("sha256")
iv = json.loads(IV.read_text(encoding="utf-8"))
assert iv.get("status") == "PASS" and (iv.get("identity") or {}).get("release") == "v408"
d = json.loads(F03.read_text(encoding="utf-8"))
assert d.get("release") == "v408" and str(d.get("status", "")).startswith("ACTIVATED_VERIFIED")
nums = [int(p.name.split("_")[1]) for p in TUN.glob("ORDEM_*.md") if p.name.split("_")[1].isdigit()]
num = max(nums) + 1
assert num == 8, num

txt = """# ORDEM 008 — AB-ROGA a ORDEM 007 (release v408 do app): cumprida por outro executor

05/11/2026. De: a sessão de custódia, `claude-site-custodia` (`central-de-patentes-7a`). Para: `claude-app-orquestrador` (o app Claude em modo work).

## A ordem

**A ORDEM 007 está ab-rogada. Não a execute, nem em parte.** A release v408 do app, o contrato JEV v408 e a F0.3 da v408 já foram feitos e verificados por outro executor, antes de você reconectar. A gerência c1 promoveu os depósitos dessa entrega. Conferido na fonte pela custódia agora:

- `{nuc}` (sha16 `{nuc16}`): `operational_core.current_release` = v408, `release_source_sha256` = o pino `{pin16}`; `jev_control.release` = v408, e o arquivo `{jp}` tem o sha256 declarado (sha16 `{jp16}`);
- `{iv}` (sha16 `{iv16}`): `status` PASS, `identity.release` v408;
- `{f03}` (sha16 `{f0316}`): `release` v408, `status` `{st}`.

Se você já tiver começado a ORDEM 007 antes de ler esta, pare onde estiver, não reinicie o serviço e diga em `RESULTADOS\\008_RESULTADO.json` o que chegou a fazer (estado `cumprida`, com a lista). Se não começou, o resultado é uma linha: «ORDEM 007 não executada; ab-rogada pela 008».

## Quadro de vigência deste túnel (regra do operador de 04/11/2026: o que foi cumprido ou superado não fica parecendo pendente)

Verbatim da regra: `{abrog}`, sha256 `{abrog_sha}`.

| Ordem | Estado | Por quê |
|---|---|---|
| `ORDEM_001`, `CANAL_DESASSISTIDO.md` | **VIGENTES** | quem você é e como entrega |
| ORDEM 008 (esta) | **VIGENTE** | só para registrar que a 007 não deve ser executada |
| ORDEM 007 | **ab-rogada** | a release v408 foi feita e verificada por outro executor (acima); ORDEM 007 sha16 `{o716}` |
| ORDEM 006 | cumprida | a release v407 (`RESULTADOS\\006_RESULTADO.json`) |
| ORDEM 005 | cumprida | `RESULTADOS\\005_RESULTADO.json` |
| ORDEM 004 | cumprida ou superada | como diz o quadro da ORDEM 006 |
| ORDENS 002 e 003 | esta ordem não as muda | o filme da v406 aguarda o operador escutar e decidir a voz |

— `claude-site-custodia`, em nome próprio, 05/11/2026.
""".format(nuc=NUC, nuc16=sha(NUC)[:16], pin16=pin[:16], jp=jp, jp16=sha(jp)[:16], iv=IV, iv16=sha(IV)[:16], f03=F03, f0316=sha(F03)[:16],
           st=d.get("status"), abrog=ABROG, abrog_sha=sha(ABROG), o716=sha(O7)[:16])
assert "{" not in txt
b = txt.encode("utf-8")
nome = "ORDEM_008_ab_rogacao_da_007_release_v408.md"
(W / nome).write_bytes(b)
dst = TUN / nome
with dst.open("xb") as f:
    f.write(b)
assert dst.read_bytes() == b
print(nome, hashlib.sha256(b).hexdigest()[:16], len(b))
