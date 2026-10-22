# -*- coding: utf-8 -*-
"""Marco fixo de 26/11/2026 (publicação internacional do ACOM, IB/345 [42]) no andamentos/marcos_fixos.json — pendência «CONTROLE» da
ENTREGA_009 de 19/10 do Codex («26/11 está no alerta e JSONL de 13/10 e agora no PDF original, mas não em marcos_fixos.json»). Sessão a7,
19/10/2026. Backup de BYTES; temporário; conferência; troca. Idempotente. A fonte vai por sha256 lido do arquivo."""
import hashlib, json, os, time
from pathlib import Path

P = Path(r"C:\IALD\Central de Patentes\andamentos\marcos_fixos.json")
PDF = Path(r"C:\IALD\Central de Patentes\EPCT\_EPCT_ACOM_PCT_BR2025_050558\RECIBOS_WIPO\PCTBR2025050558-ib345-000042-en-20261012_CUSTODIA_20261019_2b6b83ec37ee.pdf")
ENT = Path(r"C:\TUNEL_PCT\DO_CODEX\ENTREGA_009_ATUALIZACAO_EMAILS_PENDENCIAS_20261019_132121Z.md")
raw = P.read_bytes()
m = json.loads(raw.decode("utf-8"))
if any(x.get("id") == "acom_wo_publicacao_26nov" for x in m["marcos"]):
    print("já aplicado"); raise SystemExit
sh_pdf = hashlib.sha256(PDF.read_bytes()).hexdigest()
sh_ent = hashlib.sha256(ENT.read_bytes()).hexdigest()
m["marcos"].append({
    "id": "acom_wo_publicacao_26nov", "data": "2026-11-26", "cor": "vermelho",
    "processos": ["BR102025026951-1", "BR112026025335-5"],
    "titulo": ("PUBLICAÇÃO INTERNACIONAL do PCT/BR2025/050558 (ACOM) programada pelo IB/345 [42] de 12/10/2026 — data de publicação, não "
               "prazo de resposta. A 2ª geração do ACOM e qualquer matéria nova têm de ser depositadas ANTES dela: o WO vira estado da técnica "
               "sem carência contra o que vier depois. Não esperar a meta de 04/12 (decisão do operador com o advogado)."),
    "fonte": ("IB/345 [42], PDF original extraído do e-mail e custodiado pelo Codex em 19/10: %s (sha256 %s); ENTREGA_009_ATUALIZACAO_EMAILS_"
              "PENDENCIAS de 19/10 (sha256 %s); ENTREGA_009_ALERTA_WO de 13/10 [LEGAL]" % (PDF, sh_pdf, sh_ent)),
})
m["_registro"].append("19/10/2026 (Central, sessão a7): 1 marco novo — a publicação internacional do ACOM em 26/11/2026 (IB/345 [42], vermelho), "
                      "pendência «CONTROLE» da ENTREGA_009 de 19/10 do Codex. Origem: work/custodia_v394_19out/marco_26nov_acom.py.")
novo = json.dumps(m, ensure_ascii=False, indent=2).encode("utf-8")
P.with_name(P.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(raw)
t = P.with_suffix(".json.tmp")
t.write_bytes(novo)
json.loads(t.read_text(encoding="utf-8"))
assert t.stat().st_size > len(raw)
os.replace(t, P)
print("ok marcos:", len(m["marcos"]), "| bytes", len(raw), "->", P.stat().st_size, "| pdf", sh_pdf[:16])
