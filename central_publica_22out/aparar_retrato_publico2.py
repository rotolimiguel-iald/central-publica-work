# -*- coding: utf-8 -*-
"""Segundo recorte do retrato público (22/10/2026): (1) os arquivos «de código» que são operacionais (docket.yaml, notas) saem do mapa;
(2) a peça consolidada sai quando a patente tem o relatório e as reivindicações em separado (a consolidada junta o protocolo e os
pagamentos), e, sem as partes em separado, fica só o texto (o PDF sai se trouxer termo de pagamento); (3) o Atlas e o TGL Core passam pelo
filtro das notas operacionais (filtro_operacional.py), com cada omissão marcada à vista. Idempotente."""
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from filtro_operacional import filtrar_markdown, TERMOS  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path(sys.argv[1])
mp = OUT / "api" / "_mapa.json"
mapa = json.loads(mp.read_text(encoding="utf-8"))
OPER_CODIGO = re.compile(r"(?i)path=(docket\.yaml|notes%2F|notas%2F|[^&]*pendenc|[^&]*prazos)")
n_cod = n_doc = 0
for url in list(mapa):
    if "/code/file?" in url and OPER_CODIGO.search(url):
        rel = mapa.pop(url)
        (OUT / rel).unlink(missing_ok=True); n_cod += 1
# a lista de arquivos de código de cada patente também perde essas entradas
for url, rel in list(mapa.items()):
    if re.match(r"^/api/patents/[^/]+/code$", url):
        p = OUT / rel
        d = json.loads(p.read_text(encoding="utf-8"))
        d["files"] = [f for f in (d.get("files") or []) if not re.search(r"(?i)^(docket\.yaml|notes/|notas/)|pendenc|prazos", str(f.get("path", "")))]
        p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
for url, rel in list(mapa.items()):
    if not re.match(r"^/api/patents/[^/]+$", url):
        continue
    p = OUT / rel
    det = json.loads(p.read_text(encoding="utf-8"))
    papeis = {d.get("doc_role") for d in det.get("documents") or []}
    separado = {"relatorio", "reivindicacoes"} <= papeis
    fica = []
    for d in det.get("documents") or []:
        if d.get("doc_role") == "peca_consolidada":
            tu, fu = "/api/documents/%s/text" % d["id"], "/api/documents/%s/file" % d["id"]
            if separado:
                for u in (tu, fu):
                    r = mapa.pop(u, None)
                    if r and r not in ("omitido_dado_pessoal.html", "fora_do_retrato.html"):
                        (OUT / r).unlink(missing_ok=True)
                n_doc += 1
                continue
            if tu in mapa:
                tp = OUT / mapa[tu]
                txt, n = filtrar_markdown(tp.read_text(encoding="utf-8"))
                tp.write_text(txt, encoding="utf-8")
                if n and fu in mapa:
                    r = mapa.pop(fu)
                    if r not in ("omitido_dado_pessoal.html", "fora_do_retrato.html"):
                        (OUT / r).unlink(missing_ok=True)
                    mapa[fu] = "fora_do_retrato.html"
        fica.append(d)
    det["documents"] = fica
    det["doc_count"] = len(fica)
    p.write_text(json.dumps(det, ensure_ascii=False), encoding="utf-8")
omit = {}
for u in ("/api/tgl-atlas", "/api/tgl-core"):
    if u in mapa:
        p = OUT / mapa[u]
        txt, n = filtrar_markdown(p.read_text(encoding="utf-8"))
        p.write_text(txt, encoding="utf-8")
        omit[u] = n
mp.write_text(json.dumps(mapa, ensure_ascii=False), encoding="utf-8")
sobras = {}
for rel in set(mapa.values()):
    p = OUT / rel
    if p.suffix in (".json", ".txt", ".md") and p.is_file():
        k = len(TERMOS.findall(p.read_text(encoding="utf-8", errors="replace")))
        if k:
            sobras[rel] = k
print("recorte 2: %d arquivos de código operacionais e %d peças consolidadas retirados | omissões no Atlas/Core: %s | leituras: %d" % (
    n_cod, n_doc, omit, len(mapa)))
print("sobras de termo operacional:", json.dumps(dict(sorted(sobras.items(), key=lambda x: -x[1])[:10]), ensure_ascii=False))
