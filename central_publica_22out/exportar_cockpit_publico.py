# -*- coding: utf-8 -*-
"""O RETRATO PÚBLICO DO COCKPIT DA CENTRAL (ordem do operador, 22/10/2026: «possam interagir com a central (somente em modo de
visualização), igual eu interajo»). Lê a Central local (http://127.0.0.1:8765, modo local) SÓ POR GET, percorre todas as leituras que o
frontend pode pedir e grava cada resposta como arquivo estático, com a extensão certa, mais o mapa «URL da API -> arquivo» que o
frontend público carrega. Nada é escrito na Central.

Dados pessoais (a regra do operador: «segredo são dados pessoais, somente»): em texto e JSON, CPF, RG, telefone, e-mail pessoal e
credenciais são trocados por «[dado pessoal removido]» (visível, nunca em silêncio) e contados no relatório; um binário (PDF) cujo texto
traga dado pessoal NÃO é publicado (o mapa aponta para uma nota). Fora do público, por desenho: login, usuários, auditoria, orquestração
de contas e o app IALD (dados de terceiros).
Uso: C:\\Python314\\python.exe exportar_cockpit_publico.py <pasta_de_saida>"""
import json, re, sys, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
BASE = "http://127.0.0.1:8765"
OUT = Path(sys.argv[1])
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mascara_pii import MASK, PII, mascarar  # noqa: E402  (a máscara única, corrigida em 22/10: o @ de matriz do Python não é e-mail)
FORA_DO_PUBLICO = ("/api/auth", "/api/users", "/api/audit", "/api/whoami", "/api/iald/orquestracao", "/api/iald-app", "/api/cloud-writes")


def sanear_nome(url):
    p, _, q = url.partition("?")
    rel = urllib.parse.unquote(p.lstrip("/"))
    rel = re.sub(r"[^A-Za-z0-9._/\-]", "_", rel)
    if q:
        h = 0x811c9dc5
        for ch in q:
            h ^= ord(ch); h = (h * 0x01000193) & 0xFFFFFFFF
        rel += "__q_%08x" % h
    return rel


def get(url):
    # a Central local limita a 120 pedidos por minuto: ritmo de ~110/min e nova tentativa no 429
    for tent in range(6):
        time.sleep(0.55)
        try:
            with urllib.request.urlopen(BASE + url, timeout=180) as r:
                return r.status, (r.headers.get("Content-Type") or "").split(";")[0].strip().lower(), r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429 and tent < 5:
                time.sleep(20 * (tent + 1)); continue
            raise


mapa, relatorio, falhas, omitidos = {}, {}, [], []
EXT = {"application/json": ".json", "text/plain": ".txt", "text/markdown": ".md", "text/html": ".html", "image/png": ".png",
       "image/jpeg": ".jpg", "image/svg+xml": ".svg", "application/pdf": ".pdf", "image/webp": ".webp"}


def salvar(url, texto_do_binario=None):
    if url in mapa or any(url.startswith(x) for x in FORA_DO_PUBLICO):
        return None
    try:
        st, ct, data = get(url)
    except Exception as e:  # noqa: BLE001
        falhas.append({"url": url, "erro": repr(e)[:160]}); return None
    ext = EXT.get(ct)
    if ext is None:
        ext = ".pdf" if data[:4] == b"%PDF" else (".png" if data[:4] == b"\x89PNG" else ".bin")
    rel = sanear_nome(url) + ext
    dst = OUT / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if ext in (".json", ".txt", ".md", ".html", ".svg"):
        t, cont = mascarar(data.decode("utf-8", "replace"))
        if cont:
            relatorio[url] = cont
        dst.write_text(t, encoding="utf-8")
    else:
        if texto_do_binario is not None and texto_do_binario[1]:
            nota = OUT / "omitido_dado_pessoal.html"
            omitidos.append({"url": url, "motivo": sorted(texto_do_binario[1])})
            mapa[url] = "omitido_dado_pessoal.html"
            return None
        dst.write_bytes(data)
    mapa[url] = rel
    return data


def j(url):
    d = salvar(url)
    if d is None:
        p = OUT / mapa.get(url, "") if url in mapa else None
        if p and p.suffix == ".json" and p.is_file():
            return json.loads(p.read_text(encoding="utf-8"))
        return None
    try:
        return json.loads(d.decode("utf-8", "replace"))
    except ValueError:
        return None


q = lambda s: urllib.parse.quote(str(s), safe="-_.!~*'()")
t0 = time.time()
for u in ("/api/health", "/api/integrity", "/api/classes", "/api/fronteira", "/api/runs", "/api/docket", "/api/pendencias", "/api/tgl-core",
          "/api/tgl-atlas", "/api/backup/status", "/api/epct/status", "/api/iald/status", "/api/compiled"):
    salvar(u)
for nome in ("escada_qg", "banda_beta", "piso_vazios", "cadeia_inscricao"):
    salvar("/api/fronteira/fig/" + nome)
anda = j("/api/andamentos")


def ids_de(o):
    out = []
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "id" and isinstance(v, (str, int)):
                out.append(v)
            out += ids_de(v)
    elif isinstance(o, list):
        for v in o:
            out += ids_de(v)
    return out


for it in ((anda or {}).get("leituras_iald") or []):
    mid = it.get("id") if isinstance(it, dict) else None
    if mid is not None:
        salvar("/api/andamentos/leitura/" + q(mid))
comp = j("/api/compiled") if "/api/compiled" not in mapa else json.loads((OUT / mapa["/api/compiled"]).read_text(encoding="utf-8"))
for f in (comp or []):
    fn = f.get("filename") if isinstance(f, dict) else None
    if fn:
        salvar("/api/compiled/" + fn)
pats = j("/api/patents") or []
for p in pats:
    pid, slug = p["id"], p.get("slug")
    det = j("/api/patents/" + q(pid))
    for suf in ("/claims", "/evidence", "/evolucao", "/components", "/render3d", "/renders"):
        salvar("/api/patents/" + q(pid) + suf)
    salvar("/api/patents/" + q(pid) + "/memory")
    for d in ((det or {}).get("documents") or []):
        did = d.get("id")
        if did is None:
            continue
        tu = "/api/documents/%s/text" % did
        salvar(tu)
        txt = (OUT / mapa[tu]).read_text(encoding="utf-8") if tu in mapa else ""
        pii = {k for k, _ in PII if k != "credencial"} if MASK in txt else set()
        salvar("/api/documents/%s/file" % did, (txt, pii))
    for r in ((det or {}).get("renders") or []):
        if r.get("id") is not None:
            salvar("/api/renders/%s" % r["id"])
    code = j("/api/patents/" + q(pid) + "/code")
    for f in ((code or {}).get("files") or []):
        path = f.get("path") if isinstance(f, dict) else f
        if path:
            salvar("/api/patents/%s/code/file?path=%s" % (q(pid), q(path)))
    final = (code or {}).get("final") or {}
    if isinstance(final, dict) and final.get("path"):
        salvar("/api/patents/%s/code/file?path=%s" % (q(pid), q(final["path"])))
for dev in ("acom", "tgl_tensor"):   # os dois dispositivos que rodam de verdade (FUNCTIONAL_DEVICES do frontend)
    salvar("/api/device/%s/info" % dev)
(OUT / "omitido_dado_pessoal.html").write_text(
    "<!doctype html><meta charset=utf-8><title>Omitido</title><body style='font-family:sans-serif;background:#0b0b10;color:#ddd;padding:2rem'>"
    "<h1>Documento omitido</h1><p>Este documento original contém dado pessoal (por exemplo, CPF, telefone ou e-mail pessoal) e não é "
    "publicado. O texto dele, com o dado pessoal trocado por «[dado pessoal removido]», está na aba «texto».</p></body>", encoding="utf-8")
(OUT / "api").mkdir(parents=True, exist_ok=True)
(OUT / "api" / "_mapa.json").write_text(json.dumps(mapa, ensure_ascii=False), encoding="utf-8")
rel = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "fonte": BASE + " (só GET)", "n_urls": len(mapa), "falhas": falhas[:50], "n_falhas": len(falhas),
       "mascarados_por_url": relatorio, "n_urls_com_mascara": len(relatorio), "binarios_omitidos": omitidos,
       "fora_do_publico_por_desenho": list(FORA_DO_PUBLICO), "segundos": round(time.time() - t0)}
(OUT / "RELATORIO_RETRATO_PUBLICO.json").write_text(json.dumps(rel, ensure_ascii=False, indent=1), encoding="utf-8")
print("retrato: %d URLs | %d com máscara de dado pessoal | %d binários omitidos | %d falhas | %d s" % (
    len(mapa), len(relatorio), len(omitidos), len(falhas), rel["segundos"]))
