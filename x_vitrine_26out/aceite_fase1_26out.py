# -*- coding: utf-8 -*-
"""Aceite independente da Fase 1 da vitrine no X (ORDEM 026 / ADENDO A), pela gerência a7 que a ordenou; o executor foi a coordenadora
do Codex. Confere por script: o manifesto que o recibo cita é o manifesto em disco; cada arquivo usado (13) tem, no disco, o sha256 do
recibo E o do manifesto; as quatro URLs são da conta do operador e distintas; o recibo diz nome/foto/@ preservados, o fixado antigo não
apagado nem editado, nenhuma credencial lida. As capturas do perfil final e do fixado foram VISTAS pela gerência (anotado, não por
script). Grava ACEITE_FASE1_26out.json ao lado deste script; não toca no X."""
import hashlib
import json
import os
import re
import time
from pathlib import Path

B = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL")
RES = B / "DO_CHATGPT" / "ORDEM_026" / "VITRINE" / "RESULTADO_FINAL_FASE1.json"
MAN = B / "PARA_CHATGPT" / "X_VITRINE" / "MANIFEST.json"
OUT = Path(__file__).with_name("ACEITE_FASE1_26out.json")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()

R = json.loads(RES.read_text(encoding="utf-8"))
M = json.loads(MAN.read_text(encoding="utf-8"))
mm = {**M.get("arquivos", {}), **M.get("videos", {})}
man_de = lambda n: (mm[n].get("sha256") if isinstance(mm.get(n), dict) else mm.get(n))
checks = []
ck = lambda nome, ok, det="": checks.append({"check": nome, "ok": bool(ok), "detalhe": det})

ck("manifesto do recibo = manifesto em disco", R["manifest"]["sha256"] == sha(MAN), sha(MAN)[:16])
for n, f in R["files_used"].items():
    d = sha(f["path"])
    ck("arquivo %s: disco = recibo = manifesto" % n, d == f["sha256"] == man_de(n), d[:16])
urls = R["urls"]
ck("quatro URLs da conta, distintas", len(set(urls.values())) == 4 and all(re.match(r"^https://x\.com/rotolimiguel/status/\d+$", u) for u in urls.values()), ", ".join(urls))
ck("fixado novo = URL do fixado", R["pin"]["new"] == urls["fixado"] and R["pin"]["verified_first_post"])
ck("fixado antigo preservado (não apagado nem editado)", R["pin"]["old_not_edited_or_deleted"])
ck("nome L, foto e @ preservados", R["profile"]["name"] == "L" and R["profile"]["name_preserved"] and R["profile"]["photo_preserved"] and R["profile"]["handle_preserved"])
ck("uma publicação por item", all(v == 1 for v in R["publication_clicks"].values()), json.dumps(R["publication_clicks"]))
ck("Destaques: os quatro, anteriores preservados", R["highlights"]["all_four_urls_verified"] and R["highlights"]["previous_highlights_preserved"])
ck("vídeos 1080p, sem o 720p", R["media"]["fallback_720p_used"] is False)
ck("nenhuma credencial lida", R.get("credentials_read") in (False, 0, [], None, "none", "nenhuma"), repr(R.get("credentials_read"))[:80])
ck("nenhum original científico alterado", R.get("scientific_sources_modified") in (False, 0, [], None), repr(R.get("scientific_sources_modified"))[:80])
for nome in ("026x_profile_final.jpg", "026x_fixado_published.jpg"):
    p = RES.parent / nome
    ck("captura %s presente (vista pela gerência)" % nome, p.is_file(), sha(p)[:16] if p.is_file() else "ausente")

ok = all(c["ok"] for c in checks)
doc = {"schema": "iald.x-vitrine.aceite/v1", "ordem": "ORDEM 026 / ADENDO A, Fase 1", "revisor": "claude-site (gerência a7 da Central, Claude Code)",
       "executor": "codex-coordenadora", "em": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
       "recibo": {"path": str(RES), "sha256": sha(RES)}, "manifesto": {"path": str(MAN), "sha256": sha(MAN)},
       "veredito": "ACEITA" if ok else "RECUSADA", "n_checks": len(checks), "n_ok": sum(c["ok"] for c in checks), "checks": checks,
       "visto_pela_gerencia": "As capturas do perfil final (nome L, foto, bio, site e capa novos; o fixado novo no topo) e do fixado publicado "
                              "(texto igual ao fixado.txt: PROVADA como validade, CONFIRMADA como creditação recusada, z_disc 4,44 com p 4,4e-6 e o degrau de 5σ não alcançado).",
       "ressalvas": ["A legenda em inglês não entrou: a interface do X ofereceu um só espaço de legenda (pt-BR). Fica como está; o texto do post não depende dela.",
                     "O fixado antigo da ORDEM 024, ainda publicado, mostra «um.py» como link para o domínio de fora; apagá-lo é decisão do operador.",
                     "A Fase 2 (permanente) só com um manifesto novo deixado pela gerência a cada custódia."]}
t = OUT.with_name(OUT.name + ".tmp")
t.write_bytes(json.dumps(doc, ensure_ascii=False, indent=1).encode("utf-8"))
if OUT.exists():
    OUT.with_name(OUT.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(OUT.read_bytes())
os.replace(t, OUT)
print(doc["veredito"], "%d/%d" % (doc["n_ok"], doc["n_checks"]), sha(OUT)[:16])
for c in checks:
    if not c["ok"]:
        print("FALHA:", c["check"], c["detalhe"])
