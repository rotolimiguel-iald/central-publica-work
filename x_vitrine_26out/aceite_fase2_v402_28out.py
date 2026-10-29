# -*- coding: utf-8 -*-
"""Aceite da gerência c1 da Fase 2 (v402) da vitrine no X (ORDEM 026-X / ADENDO B), executada pela coordenadora do Codex em 28/10/2026
após autorização expressa do operador. Confere por script: o manifesto que o recibo cita é o manifesto em disco; cada arquivo usado tem,
no disco, o sha256 do recibo E o do manifesto; os quatro posts novos são da conta, distintos e NÃO repetem a Fase 1; o artigo foi
atualizado no MESMO id (nenhum artigo novo); o fixado antigo e o perfil (nome L, foto, @) preservados; nenhum plano comprado; recibos e
capturas presentes com os hashes do recibo; a autorização do operador está em disco. As capturas do perfil e do fixado foram VISTAS pela
gerência (anotado, não por script). Grava ACEITE_FASE2_v402_28out.json ao lado; não toca no X."""
import hashlib, json, os, re, time
from pathlib import Path
B = Path("C:/IALD/Central de Patentes/Chatgpt/TUNEL")
RES = B / "DO_CHATGPT/ORDEM_026/vitrine/RESULTADO_FASE2_v402.json"
RES1 = B / "DO_CHATGPT/ORDEM_026/VITRINE/RESULTADO_FINAL_FASE1.json"
MAN = B / "PARA_CHATGPT/X_VITRINE/MANIFEST.json"
OUT = Path(__file__).with_name("ACEITE_FASE2_v402_28out.json")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
R = json.loads(RES.read_text(encoding="utf-8")); R1 = json.loads(RES1.read_text(encoding="utf-8")); M = json.loads(MAN.read_text(encoding="utf-8"))
checks = []
ck = lambda nome, ok, det="": checks.append({"check": nome, "ok": bool(ok), "detalhe": str(det)[:200]})
ck("manifesto do recibo = manifesto em disco (6917e3dc…)", R["manifest"]["sha256"] == sha(MAN) and sha(MAN).startswith("6917e3dc"), sha(MAN)[:16])
ck("manifesto é do selo v402", M["selo"]["versao"] == "v402", M["selo"]["pin_um_py"][:16])
vid_por_caminho = {v["caminho"].replace("\\", "/"): v["sha256"] for v in M["videos"].values()}
usados = set()
for f in R["used_files"]:
    p = f["path"].replace("\\", "/"); nome = os.path.basename(p); usados.add(nome)
    d = sha(p) if Path(p).is_file() else None
    esperado_man = (M["arquivos"].get(nome) or {}).get("sha256") or vid_por_caminho.get(p)
    ck("arquivo usado %s: disco = recibo = manifesto" % nome, d is not None and d == f["sha256"] == esperado_man, (d or "ausente")[:16])
nao_usados = set(M["arquivos"]) - usados
ck("arquivos do manifesto não usados são só os justificados (bio não mudou; capa do artigo; legendas EN)",
   nao_usados <= {"bio.txt", "site.txt", "artigo_capa_1500x600.jpg", "filme1_en.srt", "filme2_en.srt"}, sorted(nao_usados))
it = R["item_receipts"]; urlre = re.compile("^https://x[.]com/rotolimiguel/status/([0-9]+)$")
novos = {k: it[k]["url"] for k in ("custodia", "filme1", "filme2", "fixado")}
ck("quatro posts novos da conta, distintos", len(set(novos.values())) == 4 and all(urlre.match(u) for u in novos.values()), json.dumps(novos))
ids1 = {urlre.match(u).group(1) for u in R1["urls"].values()}
ck("nenhum post da Fase 1 repetido (ids distintos) e o recibo diz 0 repetidos, 4 novos",
   not ({it[k]["id"] for k in novos} & ids1) and R["phase1_posts_repeated"] == 0 and R["new_posts"] == 4, sorted(ids1))
ck("artigo: atualizado no MESMO id da Fase 1, nenhum artigo novo",
   it["artigo"]["id"] == urlre.match(R1["urls"]["artigo"]).group(1) and R["new_article_created"] is False and it["artigo"]["status"].startswith("EXISTING_ARTICLE_UPDATED_SAME_ID"), it["artigo"]["id"])
for k, v in it.items():
    r = v["receipt"]; p = r["path"].replace("\\", "/")
    ck("recibo do item %s presente com o sha do recibo" % k, Path(p).is_file() and sha(p) == r["sha256"], v.get("status"))
ck("fixado: publicado uma vez e fixado; o antigo preservado (arquivo com o sha)",
   it["fixado"]["status"] == "PUBLISHED_ONCE_PINNED_VERIFIED" and sha(R["old_pin_preserved"]["path"]) == R["old_pin_preserved"]["sha256"], R["old_pin_preserved"]["sha256"][:16])
ck("custódia e filmes nos Destaques (status)", all(it[k]["status"] == "PUBLISHED_ONCE_HIGHLIGHT_VERIFIED" for k in ("custodia", "filme1", "filme2")))
ck("capa salva e conferida", it["capa"]["status"] == "HEADER_SAVED_VISUALLY_VERIFIED")
ck("bio, nome L, foto e @ preservados; nenhum plano comprado", R["bio_name_avatar_handle_preserved"] is True and R["plans_bought"] == 0)
for k, s in R["screenshots"].items():
    ck("captura %s presente com o sha do recibo" % k, Path(s["path"]).is_file() and sha(s["path"]) == s["sha256"], s["sha256"][:16])
oa = R["operator_authorization"]; txt_oa = Path(oa["path"]).read_text(encoding="utf-8", errors="replace") if Path(oa["path"]).is_file() else ""
ck("autorização expressa do operador em disco, com o sha do recibo", sha(oa["path"]) == oa["sha256"] and "Autorizo expressamente" in txt_oa, txt_oa[:80])
ck("escopo: publicação de material autenticado; sem execução científica, sem gate", "No um.py/Lean execution" in R["scientific_scope"] and "gate" in R["scientific_scope"])
art_pub = Path(B / "DO_CHATGPT/ORDEM_026/vitrine/fase2_v402/fase2_v402_artigo_atualizado.txt").read_text(encoding="utf-8", errors="replace")
art_src = Path(B / "PARA_CHATGPT/X_VITRINE/artigo.txt").read_text(encoding="utf-8")
norm = lambda s: re.sub("[ \t\r\n]+", " ", s).strip()
sem_url = lambda s: re.sub("https?://[^ \t\r\n]+", " ", s)
pub_norm = norm(sem_url(art_pub))
frases = [norm(sem_url(l)) for l in art_src.split("\n") if norm(sem_url(l))]
faltam = [f[:60] for f in frases if f not in pub_norm]
ck("artigo publicado contém as %d linhas de texto do artigo.txt (sem as URLs, que a captura separa em nós link)" % len(frases), not faltam, faltam[:3])
urls = re.findall("https?://[^ \t\r\n]+", art_src)
faltam_u = [u for u in urls if ("Description: " + u) not in art_pub and u not in art_pub]
ck("artigo publicado contém as %d URLs do artigo.txt" % len(urls), not faltam_u, faltam_u[:3])
ck("não feito, declarado: só a legenda EN (um só espaço de legenda)", len(R["not_done"]) == 1 and "English" in R["not_done"][0]["item"])
ok = all(c["ok"] for c in checks)
doc = {"schema": "iald.x-vitrine.aceite/v1", "ordem": "ORDEM 026-X / ADENDO B, Fase 2 (v402)",
       "revisor": "claude-c1 (gerência da Central, Claude Code), que ordenou; distinto do executor", "executor": "codex-coordenadora",
       "em": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "recibo": {"path": str(RES), "sha256": sha(RES)}, "manifesto": {"path": str(MAN), "sha256": sha(MAN)},
       "veredito": "ACEITA" if ok else "RECUSADA", "n_checks": len(checks), "n_ok": sum(c["ok"] for c in checks), "checks": checks,
       "visto_pela_gerencia": os.environ.get("VISTO_PELA_GERENCIA", "NAO_ANOTADO"),
       "ressalvas": ["A legenda em inglês não entrou (um só espaço de legenda por vídeo); fica como está.",
                     "O fixado antigo da ORDEM 024 (com «um.py» virado link externo) continua publicado; apagá-lo é decisão do operador.",
                     "A capa do artigo não mudou (o adendo pediu a capa do perfil e o texto do artigo).",
                     "O requisito ACOM x-vitrine-v402-phase2 (sessão da coordenadora, revisão 144, review_pending) não é mutado por esta sessão: o aceite da gerência é este arquivo e o avanço da unidade no quadro."],
       "nao_prova": "Este aceite não executa um.py, não valida ciência e não move o gate; só confere a publicação contra o manifesto."}
t = OUT.with_name(OUT.name + ".tmp"); t.write_bytes(json.dumps(doc, ensure_ascii=False, indent=1).encode("utf-8"))
if OUT.exists():
    OUT.with_name(OUT.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(OUT.read_bytes())
os.replace(t, OUT)
print(doc["veredito"], "%d/%d" % (doc["n_ok"], doc["n_checks"]), sha(OUT)[:16])
for c in checks:
    if not c["ok"]:
        print("FALHA:", c["check"], c["detalhe"])
