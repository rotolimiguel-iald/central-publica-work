# -*- coding: utf-8 -*-
"""Recorte do retrato público do cockpit pelo critério do operador (22/10/2026):
  «não precisa se tornar público as notas de aviso pra mim, a exemplo do protocolo do MS e as leituras das patentes, não é esse o
   objetivo» e «quero que vc mostre o vínculo às patentes também, o público precisa saber que está patenteado e onde e sob qual número».
SAI do retrato: as leituras do monitor (andamentos, sinal, Sentinela), as pendências, os prazos e o docket, o status do ePCT e do backup,
os prompts compilados, a memória/leitura de cada patente e as notas; dos documentos, os de protocolo e pagamento (recibos do INPI, GRU,
Pix, formulários, petições, procurações). FICA e é dito: o número do pedido no INPI, o depósito, a prioridade, o número do PCT na OMPI
(«pedido de patente depositado», não «patente concedida»), o texto técnico (relatório, reivindicações, resumo, desenhos), o código, as
execuções, os renders, a fronteira e a TGL. Idempotente sobre a pasta do retrato."""
import json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path(sys.argv[1])
mp = OUT / "api" / "_mapa.json"
mapa = json.loads(mp.read_text(encoding="utf-8"))
FORA_PREFIXOS = ("/api/andamentos", "/api/pendencias", "/api/docket", "/api/epct", "/api/backup", "/api/compiled")
FORA_RE = re.compile(r"^/api/patents/[^/]+/memory$")
DOC_FORA_PAPEL = {"recibo_inpi", "gru", "pix"}
DOC_FORA_NOME = re.compile(r"(?i)(comprovante|recibo|\bgru\b|pix|procura[cç]|peti[cç]|formul|guia|boleto|pagamento|dep[oó]sito|protocolo|"
                           r"notifica|despacho|exig[eê]ncia|taxa|fee|receipt|invoice)")
CAMPOS_FORA_LISTA = ("alert_level", "next_due", "next_urgency", "epct_status")
CAMPOS_FORA_DETALHE = ("deadlines", "docket", "docket_path", "notes", "pendencias", "peticao", "conflict_flag", "epct_status",
                       "memory_md_path", "memory_sha256", "pasta_original")
removidos, docs_fora = [], []


def tirar(url):
    rel = mapa.pop(url, None)
    if rel and rel not in ("omitido_dado_pessoal.html", "fora_do_retrato.html"):
        p = OUT / rel
        if p.is_file():
            p.unlink()
    removidos.append(url)


for url in list(mapa):
    if url.startswith(FORA_PREFIXOS) or FORA_RE.match(url):
        tirar(url)


def ler(url):
    rel = mapa.get(url)
    return (OUT / rel, json.loads((OUT / rel).read_text(encoding="utf-8"))) if rel and rel.endswith(".json") else (None, None)


def gravar(p, d):
    p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")


p_lista, lista = ler("/api/patents")
VINCULO = {}
for row in (lista or []):
    for k in CAMPOS_FORA_LISTA:
        row.pop(k, None)
    VINCULO[row["id"]] = {"pedido_inpi": row["id"], "titulo": row.get("title_54"), "deposito": row.get("filing_date"),
                          "prioridade": row.get("priority_date"), "pct": row.get("epct_number")}
if p_lista:
    gravar(p_lista, lista)
for pid in list(VINCULO):
    p_det, det = ler("/api/patents/" + pid)
    if not det:
        continue
    for k in CAMPOS_FORA_DETALHE:
        det.pop(k, None)
    fica = []
    for d in det.get("documents") or []:
        nome = (d.get("rel_path") or "").split("/")[-1]
        if d.get("doc_role") in DOC_FORA_PAPEL or DOC_FORA_NOME.search(nome):
            docs_fora.append({"patente": pid, "papel": d.get("doc_role")})
            for suf in ("text", "file"):
                tirar("/api/documents/%s/%s" % (d.get("id"), suf))
        else:
            fica.append(d)
    det["documents"] = fica
    det["doc_count"] = len(fica)
    v = VINCULO[pid]
    v.update({"jurisdicao": det.get("jurisdiction"), "pct_data": det.get("epct_date")})
    det["vinculo_patentario"] = {
        "estatuto": "pedido de patente depositado (não é patente concedida)",
        "pedido_inpi": pid, "escritorio": "INPI — Instituto Nacional da Propriedade Industrial (Brasil)",
        "deposito": det.get("filing_date"), "prioridade": det.get("priority_date"),
        "pct": det.get("epct_number"), "pct_escritorio": "OMPI/WIPO (PCT)" if det.get("epct_number") else None,
        "pct_data": det.get("epct_date"), "titular": "IALD Ltda. — inventor Luiz Antonio Rotoli Miguel"}
    gravar(p_det, det)
p_h, h = ler("/api/health")
if h and isinstance(h.get("counts"), dict):
    for k in ("deadline", "note", "pendencia"):
        h["counts"].pop(k, None)
    gravar(p_h, h)
(OUT / "fora_do_retrato.html").write_text(
    "<!doctype html><meta charset=utf-8><title>Fora do retrato</title><body style='font-family:sans-serif;background:#0b0b10;color:#ddd;padding:2rem'>"
    "<h1>Esta leitura não faz parte do retrato público</h1><p>O modo público mostra a ciência, o código, os resultados e o vínculo às "
    "patentes. As notas operacionais do operador (prazos, leituras do monitor, protocolo) ficam na Central dele.</p></body>", encoding="utf-8")
vinc = sorted(VINCULO.values(), key=lambda v: v["pedido_inpi"])
(OUT / "api" / "vinculo_patentario.json").write_text(json.dumps(vinc, ensure_ascii=False, indent=1), encoding="utf-8")
mp.write_text(json.dumps(mapa, ensure_ascii=False), encoding="utf-8")
sobras = {}
RX = re.compile(r"(?i)(mandado de seguran|\bMS 28/10|RO/106|sentinela|\bGRU\b|\bpix\b|prazo fatal|eOwner)")
for rel in set(mapa.values()):
    p = OUT / rel
    if p.suffix in (".json", ".txt", ".md") and p.is_file():
        n = len(RX.findall(p.read_text(encoding="utf-8", errors="replace")))
        if n:
            sobras[rel] = n
print("recorte: %d leituras retiradas | %d documentos de protocolo/pagamento retirados | %d leituras ficam | vínculo de %d pedidos" % (
    len(removidos), len(docs_fora), len(mapa), len(vinc)))
print("termos operacionais que ainda aparecem (arquivo: ocorrências):", json.dumps(dict(sorted(sobras.items(), key=lambda x: -x[1])[:12]), ensure_ascii=False))
