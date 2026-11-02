# -*- coding: utf-8 -*-
"""Aceite da gerência c1 da Fase 2 (v404) da vitrine no X (ORDEM 026-X / ADENDO C), executada pela coordenadora do Codex em 29/10/2026
sob a ordem permanente da casa (a cada custódia: post da versão, filmes do selo corrente, fixado, capa, artigo) e a autorização do operador
de 27/10 para integrar e publicar os filmes (recibo do ADENDO E da ORDEM 022). Confere por script, contra o recibo RESULTADO_FASE2_v404.json
(esquema novo da coordenadora: `items[]` com `source`/`video`/`captions`/`evidence`): o manifesto citado é o manifesto em disco e é do selo
v404 (pin = sha256 do um.py do Nós, lido agora); cada arquivo usado tem, no disco, o sha256 do recibo E o do manifesto; os quatro posts novos
são da conta, distintos e NÃO repetem a Fase 1 nem a Fase 2 da v402; o artigo foi atualizado no MESMO id (nenhum artigo novo); o fixado
anterior (v402) preservado e o novo fixado fixado; perfil (nome L, bio, foto, @) preservado e capa trocada; nenhuma compra/TTS/render;
recibos e capturas presentes com os hashes do recibo; os textos publicados (custódia, filmes, fixado, artigo) iguais à fonte a menos de
espaço em branco e da exibição padrão de URL do X; o depósito na fila da memória existe com o hash do recibo. Grava
ACEITE_FASE2_v404_29out.json ao lado (temporário → substituir; backup se existir); não toca no X."""
import hashlib, json, os, re, time
from pathlib import Path

B = Path("C:/IALD/Central de Patentes/Chatgpt/TUNEL")
RES = B / "DO_CHATGPT/ORDEM_026/VITRINE/RESULTADO_FASE2_v404.json"
RES1 = B / "DO_CHATGPT/ORDEM_026/VITRINE/RESULTADO_FINAL_FASE1.json"
RES2 = B / "DO_CHATGPT/ORDEM_026/VITRINE/RESULTADO_FASE2_v402.json"
MAN = B / "PARA_CHATGPT/X_VITRINE/MANIFEST.json"
ADENDO = B / "PARA_CHATGPT/ORDEM_026_ADENDO_C_fase2_v404.md"
AUT_OP = B / "DO_CHATGPT/ORDEM_022/ADENDO_E/AUTORIZACAO_OPERADOR_INTEGRAR_PUBLICAR_20261027.json"
UMPY = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um.py")
SELO = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um_absoluto_selo.json")
OUT = Path(__file__).with_name("ACEITE_FASE2_v404_29out.json")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
P = lambda s: Path(str(s).replace("\\", "/"))
R = json.loads(RES.read_text(encoding="utf-8")); R1 = json.loads(RES1.read_text(encoding="utf-8")); R2 = json.loads(RES2.read_text(encoding="utf-8"))
M = json.loads(MAN.read_text(encoding="utf-8"))
checks = []
ck = lambda nome, ok, det="": checks.append({"check": nome, "ok": bool(ok), "detalhe": str(det)[:220]})

# 1. ordem, manifesto, selo
ck("recibo é da ORDEM 026-X ADENDO C, versão v404, status COMPLETED_VERIFIED_AWAITING_MANAGEMENT_ACCEPTANCE",
   R["order"] == "ORDEM026-X ADENDO C" and R["version"] == "v404" and R["status"] == "COMPLETED_VERIFIED_AWAITING_MANAGEMENT_ACCEPTANCE", R["status"])
ck("autoridade do recibo = o adendo C em disco (sha256)", P(R["authority"]["path"]) == ADENDO and ADENDO.is_file() and sha(ADENDO) == R["authority"]["sha256"], R["authority"]["sha256"][:16])
ck("manifesto do recibo = manifesto em disco (cd748ab5…)", P(R["manifest"]["path"]) == MAN and R["manifest"]["sha256"] == sha(MAN) and sha(MAN).startswith("cd748ab5"), sha(MAN)[:16])
pin = sha(UMPY)
ck("manifesto é do selo v404 e o pin é o sha256 do um.py do Nós (lido agora)", M["selo"]["versao"] == "v404" and M["selo"]["pin_um_py"] == pin, pin[:16])
ck("selo reconferido pela coordenadora = selo em disco (sha256)", P(R["sealed_source_rechecked"]["path"]) == SELO and sha(SELO) == R["sealed_source_rechecked"]["sha256"], R["sealed_source_rechecked"]["sha256"][:16])
pre = P(R["precheck"]["path"])
ck("precheck presente com o sha do recibo e PASS", pre.is_file() and sha(pre) == R["precheck"]["sha256"] and json.loads(pre.read_text(encoding="utf-8"))["status"] == "PASS", R["precheck"]["sha256"][:16])

# 2. arquivos usados: disco = recibo = manifesto
vid_por_caminho = {v["caminho"].replace("\\", "/"): v["sha256"] for v in M["videos"].values()}
items = {it["item"]: it for it in R["items"]}
ck("seis itens, todos COMPLETED_VERIFIED; items_complete = 6",
   set(items) == {"custodia", "filme1", "filme2", "fixado", "capa_perfil", "artigo"} and all(it["status"] == "COMPLETED_VERIFIED" for it in items.values()) and R["items_complete"] == 6 == len(R["items"]),
   sorted(items))
usados = set()
def arq(nome_item, chave, f):
    p = P(f["path"]); nome = p.name; usados.add(nome)
    d = sha(p) if p.is_file() else None
    esperado_man = (M["arquivos"].get(nome) or {}).get("sha256") or vid_por_caminho.get(str(p).replace("\\", "/"))
    ck("arquivo usado (%s/%s) %s: disco = recibo = manifesto" % (nome_item, chave, nome), d is not None and d == f["sha256"] == esperado_man and (f.get("bytes") is None or p.stat().st_size == f["bytes"]), (d or "ausente")[:16])
for k in ("custodia", "filme1", "filme2", "fixado", "capa_perfil"):
    arq(k, "source", items[k]["source"])
for k in ("filme1", "filme2"):
    arq(k, "video", items[k]["video"]); arq(k, "captions_pt_br", items[k]["captions_pt_br"])
    ck("%s: duração do vídeo no recibo = manifesto" % k, items[k]["duration_seconds"] == M["videos"][k]["duracao_s"], items[k]["duration_seconds"])
    ck("%s: legenda EN declarada como não oferecida (um só espaço de legenda)" % k, items[k]["captions_en"] == "NOT_OFFERED_SECOND_SLOT", items[k]["captions_en"])
arq("artigo", "body", items["artigo"]["body"]); arq("artigo", "cover", items["artigo"]["cover"])
nao_usados = set(M["arquivos"]) - usados
ck("arquivos do manifesto não usados são só os justificados (bio não mudou; título do artigo não mudou; legendas EN sem espaço; site.txt é referência)",
   nao_usados <= {"bio.txt", "site.txt", "artigo_titulo.txt", "filme1_en.srt", "filme2_en.srt"}, sorted(nao_usados))

# 3. posts: quatro novos, distintos, da conta; nada repetido; artigo no mesmo id
urlre = re.compile("^https://x[.]com/rotolimiguel/status/([0-9]+)$")
novos = {k: items[k]["url"] for k in ("custodia", "filme1", "filme2", "fixado")}
ck("quatro posts novos da conta, distintos, id da URL = post_id, new_posts = 1 cada",
   len(set(novos.values())) == 4 and all(urlre.match(u) and urlre.match(u).group(1) == str(items[k]["post_id"]) and items[k]["new_posts"] == 1 for k, u in novos.items()), json.dumps(novos))
ids1 = {urlre.match(u).group(1) for u in R1["urls"].values()}
ids2 = {urlre.match(v["url"]).group(1) for v in R2["item_receipts"].values() if v.get("url")}
ids_novos = {str(items[k]["post_id"]) for k in novos}
ck("nenhum post da Fase 1 nem da Fase 2 (v402) repetido; recibo diz 4 posts novos e a conta foi de %d a %d" % (R["profile_post_count_before"], R["profile_post_count_after"]),
   not (ids_novos & (ids1 | ids2)) and R["new_posts"] == 4 and R["profile_post_count_after"] - R["profile_post_count_before"] == 4, sorted(ids1 | ids2))
art = items["artigo"]
ck("artigo: atualizado no MESMO id da Fase 1, nenhum artigo novo, título inalterado, destaque preservado",
   str(art["same_id"]) == urlre.match(R1["urls"]["artigo"]).group(1) and art["new_article_created"] is False and art["title_unchanged"] is True and art["highlight_preserved"] is True and art["url"].endswith(str(art["same_id"])), art["same_id"])

# 4. evidências com hash
def ev(nome, e):
    p = P(e["path"]); ck("evidência %s presente com o sha do recibo" % nome, p.is_file() and sha(p) == e["sha256"] and p.stat().st_size == e["bytes"], e["sha256"][:16])
for k in ("custodia", "filme1", "filme2", "fixado", "capa_perfil"):
    ev("%s/evidence" % k, items[k]["evidence"])
for k in ("custodia", "filme1", "filme2"):
    ck("%s nos Destaques (highlight_verified)" % k, items[k]["highlight_verified"] is True); ev("%s/highlight" % k, items[k]["highlight_evidence"])
for k in ("filme1", "filme2"):
    ev("%s/caption_upload" % k, items[k]["caption_upload_evidence"])
for i, e in enumerate(art["evidence"]):
    ev("artigo/%d" % i, e)
ev("fixado/pin", items["fixado"]["pin_evidence"])
n_ui_ok = sum(1 for e in R["ui_evidence"] if P(e["path"]).is_file() and sha(P(e["path"])) == e["sha256"])
ck("as %d evidências de UI presentes com o sha do recibo" % len(R["ui_evidence"]), n_ui_ok == len(R["ui_evidence"]), n_ui_ok)
for nome, chave in (("recibo técnico", "technical_receipt"), ("recibo do depósito na fila", "memory_deposit_receipt")):
    e = R[chave]; p = P(e["path"]); ck("%s presente com o sha do recibo" % nome, p.is_file() and sha(p) == e["sha256"], e["sha256"][:16])
dep = R["memory_deposit"]; dp = P(dep["arquivo"])
ck("depósito na fila da memória existe (codex-coordenadora, seq %s) com o sha256 do recibo" % dep.get("seq"), dep["ok"] is True and dp.is_file() and sha(dp) == dep["sha256_deposito"], dp.name)

# 5. fixado e perfil
ck("fixado: fixado e conferido; o fixado anterior (Fase 2 da v402) preservado",
   items["fixado"]["pinned_verified"] is True and str(items["fixado"]["previous_pin_preserved"]) == urlre.match(R2["item_receipts"]["fixado"]["url"]).group(1), items["fixado"]["previous_pin_preserved"])
perfil = json.loads(P(items["fixado"]["pin_evidence"]["path"]).read_text(encoding="utf-8"))
bio = (B / "PARA_CHATGPT/X_VITRINE/bio.txt").read_text(encoding="utf-8")
norm = lambda s: re.sub("[ \t\r\n]+", " ", s).strip()
ptxt = perfil.get("profile", "")
ck("perfil final: nome L, @rotolimiguel, a bio em disco (não mudou) e o fixado novo no topo com «selo v404»",
   ptxt.startswith("L\n") and "@rotolimiguel" in ptxt and norm(bio) in norm(ptxt) and perfil.get("firstArticle", "").startswith("Fixado") and "selo v404" in perfil.get("firstArticle", "")
   and any(str(items["fixado"]["post_id"]) in l for l in perfil.get("firstLinks", [])), perfil.get("firstArticle", "")[:60])
antes = json.loads((P(items["fixado"]["pin_evidence"]["path"]).parent / "v404_perfil_antes_capa.json").read_text(encoding="utf-8")) if (P(items["fixado"]["pin_evidence"]["path"]).parent / "v404_perfil_antes_capa.json").is_file() else {}
hdr_antes = antes.get("header") if isinstance(antes, dict) else None
ck("capa do perfil: campos preservados (recibo) e a capa final difere da anterior",
   items["capa_perfil"]["profile_fields_preserved"] is True and perfil.get("header") and (hdr_antes is None or hdr_antes != perfil.get("header")), (perfil.get("header") or "")[-40:])
ck("preservados: nome L, bio, avatar, @, fases anteriores, artigo no mesmo id", {"nome L", "bio", "avatar", "@rotolimiguel"} <= set(R["preserved"]))
ck("nenhuma compra, TTS ou render novos; nenhuma condição de parada", R["purchases"] == 0 and R["new_tts"] == 0 and R["new_render"] == 0 and R["stop_conditions_observed"] == [])
ck("escopo: publicação; sem validação científica; aceite separado da gerência", R["independent_scientific_validation"].startswith("NOT_PERFORMED") and R["management_acceptance"].startswith("SEPARATE_PENDING"))
ck("autorização do operador (27/10) para integrar e publicar os filmes, citada no adendo, existe em disco", AUT_OP.is_file(), sha(AUT_OP)[:16] if AUT_OP.is_file() else "ausente")

# 6. textos publicados = fonte (sem URLs; espaço em branco normalizado)
sem_url = lambda s: re.sub("https?://[^ \t\r\n]+", " ", s)
def texto_pub(e):
    p = P(e["path"]); j = json.loads(p.read_text(encoding="utf-8", errors="replace"))
    return j.get("text") or j.get("body") or ""
for k, fonte in (("custodia", "CUSTODIA_v404.txt"), ("filme1", "filme1_post.txt"), ("filme2", "filme2_post.txt"), ("fixado", "fixado.txt")):
    src = (B / "PARA_CHATGPT/X_VITRINE" / fonte).read_text(encoding="utf-8")
    pub = texto_pub(items[k]["evidence"])
    ck("%s: texto publicado = %s (sem as URLs; espaço em branco normalizado)" % (k, fonte), pub and norm(sem_url(pub)) == norm(sem_url(src)), "%d/%d c" % (len(pub), len(src)))
    urls = re.findall("https?://[^ \t\r\n]+", src)
    faltam_u = [u for u in urls if u.rstrip("/") not in pub.replace("…", "")]
    ck("%s: as %d URLs da fonte aparecem no publicado (a menos da barra final e da elipse visual do X)" % (k, len(urls)), not faltam_u, faltam_u[:2])
art_pub = json.loads(P(art["evidence"][0]["path"]).read_text(encoding="utf-8", errors="replace"))
art_src = (B / "PARA_CHATGPT/X_VITRINE/artigo.txt").read_text(encoding="utf-8")
body = art_pub.get("body", "")
frases = [norm(sem_url(l)) for l in art_src.splitlines() if norm(sem_url(l))]
faltam = [f[:60] for f in frases if f not in norm(sem_url(body))]
ck("artigo publicado (body) contém as %d linhas de texto do artigo.txt (sem URLs)" % len(frases), not faltam and art_pub.get("body_whitespace_normalized_equal") is True, faltam[:3])
urls_a = re.findall("https?://[^ \t\r\n]+", art_src)
tudo = body + " " + json.dumps(art_pub, ensure_ascii=False)
faltam_ua = [u for u in urls_a if u.rstrip("/") not in tudo.replace("…", "")]
ck("artigo publicado contém as %d URLs do artigo.txt" % len(urls_a), not faltam_ua, faltam_ua[:3])
titulo = (B / "PARA_CHATGPT/X_VITRINE/artigo_titulo.txt").read_text(encoding="utf-8").strip()
ck("título do artigo publicado = artigo_titulo.txt", art_pub.get("articleText", "").startswith(titulo), titulo)
ck("artigo publicado diz «Selo corrente: v404» e a ressalva do gate na forma da v403 (18 calculadas, 0 literais, veredito lê 15)",
   "Selo corrente: v404" in body and "18" in body and "0 literais" in body.replace("zero literais", "0 literais") and "15" in body, "")

ok = all(c["ok"] for c in checks)
doc = {"schema": "iald.x-vitrine.aceite/v1", "ordem": "ORDEM 026-X / ADENDO C, Fase 2 (v404)",
       "revisor": "claude-c1 (gerência da Central, Claude Code), que ordenou; distinto do executor", "executor": "codex-coordenadora",
       "em": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "recibo": {"path": str(RES), "sha256": sha(RES)}, "manifesto": {"path": str(MAN), "sha256": sha(MAN)},
       "veredito": "ACEITA" if ok else "RECUSADA", "n_checks": len(checks), "n_ok": sum(c["ok"] for c in checks), "checks": checks,
       "visto_pela_gerencia": os.environ.get("VISTO_PELA_GERENCIA", "NAO_ANOTADO"),
       "ressalvas": ["A legenda em inglês não entrou (um só espaço de legenda por vídeo); fica como está, como na v402.",
                     "O título do artigo não mudou (artigo_titulo.txt não usado por isso); a capa do artigo mudou.",
                     "Os posts e fixados das fases anteriores (Fase 1, Fase 2 da v402, o fixado antigo da ORDEM 024) continuam publicados; apagar é decisão do operador.",
                     "O requisito ACOM x-vitrine-v404-phase2 (sessão da coordenadora) não é mutado por esta sessão: o aceite da gerência é este arquivo e o avanço da unidade no quadro.",
                     "A conferência dos textos publicados é contra a evidência de UI que a coordenadora gravou (texto de acessibilidade), não contra o X ao vivo."],
       "nao_prova": "Este aceite não executa um.py, não valida ciência e não move o gate; só confere a publicação contra o manifesto e o recibo."}
t = OUT.with_name(OUT.name + ".tmp"); t.write_bytes(json.dumps(doc, ensure_ascii=False, indent=1).encode("utf-8"))
if OUT.exists():
    OUT.with_name(OUT.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(OUT.read_bytes())
os.replace(t, OUT)
print(doc["veredito"], "%d/%d" % (doc["n_ok"], doc["n_checks"]), sha(OUT)[:16])
for c in checks:
    if not c["ok"]:
        print("FALHA:", c["check"], "|", c["detalhe"])
