# -*- coding: utf-8 -*-
"""O NÚCLEO PÚBLICO da Central (repositório github.com/rotolimiguel-iald/central-publica) — ordem do operador, 22/10/2026:
«Quero que o projeto inteiro esteja indexado no github de forma pública e vinculado à minha pasta do the_boundary ... quero liberar todos
os códigos e todos os resultados de tudo, sem exceção» + «segredo são dados pessoais, somente» + «não precisa se tornar público as notas de
aviso pra mim, a exemplo do protocolo do MS e as leituras das patentes» + «mostre o vínculo às patentes».
Copia a árvore RASTREADA da Central privada para uma pasta NOVA (o repositório privado não é tocado), com:
  - FORA: as notas operacionais do operador (andamentos/monitor, pendências, prazos, docket, notas e leituras de patente, prompts
    compilados, protocolo do PCT/EPCT, segurança e deploy da nuvem), a pesquisa jurídica do Escritório, documentos de protocolo e de
    pagamento, PDFs originais cujo texto traga dado pessoal, arquivos que batam nos marcadores privados da casa, > 95 MB;
  - DENTRO: todo o código e todo resultado, com dado pessoal trocado à vista por «[dado pessoal removido]» e, nos .md, as notas
    operacionais omitidas à vista; o vínculo patentário (PATENTES.md); o índice público (INDICE_PUBLICO.json, sha256 de cada arquivo).
Uso: C:\\Python314\\python.exe construir_nucleo_publico.py <pasta_destino_nova>"""
import hashlib, json, os, re, shutil, subprocess, sys, time
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
W = Path(__file__).resolve().parent
sys.path.insert(0, str(W))
sys.path.insert(0, r"C:\IALD\Site\tgl\v3.0_bancada\tools")
from mascara_pii import mascarar            # noqa: E402
from filtro_operacional import filtrar_markdown  # noqa: E402
import guarda_publica as GP                 # noqa: E402  (22/10/2026: barra só CREDENCIAL e dado pessoal forte onde a máscara não alcança)

SRC = Path(r"C:\IALD\Central de Patentes")
DST = Path(sys.argv[1])
assert not DST.exists() or not any(DST.iterdir()), "a pasta de destino precisa ser nova ou vazia — PARAR"
DST.mkdir(parents=True, exist_ok=True)
TXT = {".py", ".lean", ".md", ".json", ".jsonl", ".txt", ".tex", ".csv", ".tsv", ".toml", ".yaml", ".yml", ".js", ".mjs", ".ts", ".tsx",
       ".jsx", ".html", ".css", ".ipynb", ".sh", ".ps1", ".bat", ".cfg", ".ini", ".sql", ".bib", ".sty", ".cls", ".xml", ".svg", ".dat",
       ".log", ".out", ".diff", ".patch", ".spec", ".gitignore", ".gitattributes", ".dockerignore", ".example"}
LIM = 95 * 1024 * 1024
EXT_FORA = {".db", ".sqlite", ".sqlite3", ".db-wal", ".db-shm", ".eml", ".msg", ".mbox", ".pst", ".ost", ".vcf", ".ics", ".kdbx",
            ".har"}
FORA_PREFIXO = {"andamentos/": "notas operacionais (monitor, andamentos, sinal)", "EPCT/": "protocolo do PCT/EPCT",
                "compiled_prompts/": "prompts compilados (operacional)", "memory/patents/": "leituras/memórias das patentes (notas ao operador)",
                "backend/data/": "dados vivos (banco, auditoria)", "logs/": "logs", "backups/": "backups"}
FORA_EXATO = {"PENDENCIAS.md": "pendências (notas ao operador)", "SEGURANCA_REMOTA.md": "segurança da nuvem (operacional)",
              "DEPLOY_NUVEM.md": "deploy da nuvem (operacional)", "pjedocs_sm.xml": "pesquisa jurídica do Escritório"}
FORA_RE = [(re.compile(r"^patents/[^/]+/docket\.yaml$"), "docket (prazos e protocolo)"),
           (re.compile(r"^patents/[^/]+/notes/"), "notas de patente (ao operador)"),
           (re.compile(r"(?i)(^|/)[^/]*pendenc"), "pendências (notas ao operador)"),
           (re.compile(r"(?i)(^|/)prazos"), "prazos (notas ao operador)"),
           (re.compile(r"Informações sobre o Depósito Internacional PCT/"), "protocolo do PCT/EPCT")]
DOC_FORA_NOME = re.compile(r"(?i)(comprovante|recibo|\bgru\b|\bpix\b|procura[cç]|peti[cç]|formul|guia|boleto|pagamento|dep[oó]sito|protocolo|"
                           r"notifica|despacho|exig[eê]ncia|\btaxa|\bfee\b|receipt|invoice|epct)")


def sha(b):
    return hashlib.sha256(b).hexdigest()


tr = subprocess.run(["git", "-C", str(SRC), "ls-files", "-z"], capture_output=True).stdout.decode("utf-8", "replace").split("\0")
tr = [t for t in tr if t]
fora = Counter(); fora_lista = {}
indice = []
masc_total = Counter(); n_md_filtrados = 0
pdf_pii = set()
# os PDFs originais com dado pessoal: decididos pelo texto extraído do próprio documento (vault/normalized_docs/<rel>.txt)
for t in tr:
    if t.startswith("vault/normalized_docs/") and t.endswith(".txt"):
        _, c = mascarar((SRC / t).read_text(encoding="utf-8", errors="replace"))
        if any(k in c for k in ("cpf", "cpf_rotulado", "rg_rotulado", "telefone")):
            pdf_pii.add(t[len("vault/normalized_docs/"):-4])


LOCAL_EXCL = {}


def fora_(m, x):
    fora[m] += 1
    LOCAL_EXCL.setdefault(m, []).append(x)


def motivo(t):
    for pre, m in FORA_PREFIXO.items():
        if t.startswith(pre):
            return m
    if t in FORA_EXATO:
        return FORA_EXATO[t]
    for rx, m in FORA_RE:
        if rx.search(t):
            return m
    nome = t.rsplit("/", 1)[-1]
    if (t.startswith("Patentes/") or t.startswith("vault/normalized_docs/") or t.startswith("vault/originals_copy/zips/")) and DOC_FORA_NOME.search(nome):
        return "documento de protocolo ou pagamento"
    if t.startswith("Patentes/") and t in pdf_pii:
        return "documento original com dado pessoal (o texto técnico segue nas partes separadas)"
    if t.startswith("vault/normalized_docs/") and t[len("vault/normalized_docs/"):-4] in pdf_pii:
        return "texto de documento com dado pessoal (formulário)"
    if ".bak_" in nome or nome.endswith(".tmp"):
        return "backup de sessão"
    return None


t0 = time.time()
for i, t in enumerate(tr):
    p = SRC / t
    if not p.is_file():
        continue
    m = motivo(t)
    if m:
        fora_(m, t); fora_lista.setdefault(m, []).append(t); continue
    if GP.arquivo_de_credencial(t.rsplit("/", 1)[-1]):
        fora_("arquivo de credencial", t); continue
    try:
        s = p.stat().st_size
        raw = p.read_bytes() if s <= LIM else b""
    except OSError:
        fora_("ilegível no disco", t); continue
    if s > LIM:
        fora_("acima de 95 MB (índice apenas)", t); fora_lista.setdefault("acima de 95 MB (índice apenas)", []).append(t); continue
    ext = p.suffix.lower() if p.suffix else ("." + p.name.lstrip(".")).lower()
    if ext in EXT_FORA:
        fora_("correio, banco de dados ou contatos (podem conter dado pessoal)", t); continue
    dst = DST / t
    dst.parent.mkdir(parents=True, exist_ok=True)
    if ext in TXT:
        txt = raw.decode("utf-8", "replace")
        n_cred, pii_blob = GP.avaliar_texto(txt)
        if n_cred:
            fora_("contém credencial", t); continue
        if pii_blob:
            fora_("carga embutida com dado pessoal", t); continue
        txt, c = mascarar(txt)
        if ext == ".md":
            txt, n = filtrar_markdown(txt)
            if n:
                c["notas_operacionais_omitidas"] = n; n_md_filtrados += 1
        # (22/10/2026) a regra do Escritório vale para o que VAI AO AR (depois da máscara e do filtro): o acervo do Escritório,
        # PJ separada, nunca entra; uma nota operacional já omitida não conta
        if GP.toca_escritorio(txt):
            fora_("toca o acervo do Escritório (PJ separada: caminhos internos, audiências, processos)", t); continue
        dst.write_text(txt, encoding="utf-8", newline="")
        for k, v in c.items():
            masc_total[k] += v
        b = txt.encode("utf-8")
    else:
        n_cred, kk = GP.avaliar_bytes(t.rsplit("/", 1)[-1], raw)
        if n_cred or kk:
            m = "documento ou compactado com dado pessoal, protocolo ou credencial"
            fora_(m, t); fora_lista.setdefault(m, []).append(t); continue
        dst.write_bytes(raw)
        b = raw
    indice.append({"caminho": t, "bytes": len(b), "sha256": sha(b)})
    if i % 5000 == 0:
        print("  ... %d/%d (%.0f s)" % (i, len(tr), time.time() - t0), flush=True)
LISTAVEIS = {"documento de protocolo ou pagamento", "acima de 95 MB (índice apenas)", "backup de sessão"}
exclusoes = {"criterio": "dados pessoais e notas operacionais do operador ficam fora; todo o código e todo resultado ficam",
             "por_motivo": dict(fora), "caminhos_listados_por_motivo": {k: v for k, v in fora_lista.items() if k in LISTAVEIS},
             "nota": "os caminhos dos motivos de dado pessoal, marcador privado e notas operacionais não são listados (os próprios nomes podem ser nota ou dado)",
             "mascaras_de_dado_pessoal": dict(masc_total), "md_com_notas_operacionais_omitidas": n_md_filtrados}
(DST / "INDICE_PUBLICO.json").write_text(json.dumps({"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "n_arquivos": len(indice),
                                                      "arquivos": indice}, ensure_ascii=False), encoding="utf-8")
(DST / "EXCLUSOES_PUBLICAS.json").write_text(json.dumps(exclusoes, ensure_ascii=False, indent=1), encoding="utf-8")
print("núcleo público: %d arquivos copiados | fora: %s | máscaras: %s | %d .md com notas omitidas | %.0f s" % (
    len(indice), dict(fora), dict(masc_total), n_md_filtrados, time.time() - t0))
(W / ("varredura_exclusoes_%s.json" % DST.name)).write_text(json.dumps(LOCAL_EXCL, ensure_ascii=False, indent=0), encoding="utf-8")
