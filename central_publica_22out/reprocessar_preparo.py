# -*- coding: utf-8 -*-
"""REPROCESSA um preparo público depois de uma correção da máscara/guarda (22/10/2026: o padrão de RG lia «RG» = Relatividade Geral e
«identidade» = termo da TGL como documento), sem reconstruir tudo. Pela MESMA esteira dos construtores:
  1. todo arquivo de texto do preparo que traz a marca «[dado pessoal removido]» é recalculado da origem com a máscara corrigida — se
     mudou, é regravado (a máscara só troca trechos; um falso positivo só pode estar onde a marca está);
  2. todo arquivo EXCLUÍDO por um motivo de dado pessoal (lista local varredura_exclusoes_<preparo>.json) é reavaliado com a guarda
     corrigida — se agora passa, entra (texto mascarado; PDF/PNG pelas regras da região; documento original do núcleo pelo texto extraído);
  3. o INDICE_PUBLICO.json, o EXCLUSOES_PUBLICAS.json e a lista local são atualizados.
Uso: reprocessar_preparo.py <nucleo|work|Chatgpt> <pasta_do_preparo>"""
import hashlib, json, os, sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
W = Path(__file__).resolve().parent
sys.path.insert(0, str(W))
from mascara_pii import mascarar, MASK  # noqa: E402
from filtro_operacional import filtrar_markdown  # noqa: E402
import guarda_publica as GP  # noqa: E402

TIPO, D = sys.argv[1], Path(sys.argv[2])
assert TIPO in ("nucleo", "work", "Chatgpt")
CENTRAL = Path(r"C:\IALD\Central de Patentes")
SRC = CENTRAL if TIPO == "nucleo" else CENTRAL / TIPO
TXT = {".py", ".lean", ".md", ".json", ".jsonl", ".txt", ".tex", ".csv", ".tsv", ".toml", ".yaml", ".yml", ".js", ".mjs", ".ts", ".tsx",
       ".jsx", ".html", ".css", ".ipynb", ".sh", ".ps1", ".bat", ".cfg", ".ini", ".sql", ".bib", ".sty", ".cls", ".xml", ".svg", ".dat",
       ".log", ".out", ".diff", ".patch", ".spec", ".gitignore", ".gitattributes", ".dockerignore", ".example", ".pysnip", ".r", ".jl", ".c",
       ".h", ".cpp", ".rs", ".go", ".java"}
SENS_PII = {"cpf", "cpf_rotulado", "rg_rotulado", "telefone"}


def lp(x):
    x = str(Path(x).resolve())
    return x if x.startswith("\\\\?\\") else "\\\\?\\" + x


def ext(rel):
    p = Path(rel)
    return p.suffix.lower() if p.suffix else ("." + p.name.lstrip(".")).lower()


def esteira_texto(rel):
    """(bytes | None, motivo_se_recusado)"""
    txt = open(lp(SRC / rel), "rb").read().decode("utf-8", "replace")
    n_cred, pii = GP.avaliar_texto(txt)
    if n_cred:
        return None, "contém credencial"
    if pii:
        return None, "carga embutida com dado pessoal"
    txt, c = mascarar(txt)
    if rel.endswith(".md"):
        txt, _n = filtrar_markdown(txt)
    # a regra do Escritório vale para o que VAI AO AR (depois da máscara e do filtro das notas): uma nota operacional omitida não conta
    if GP.toca_escritorio(txt):
        return None, "toca o acervo do Escritório (PJ separada: caminhos internos, audiências, processos)"
    return txt.encode("utf-8"), None


def gravar(rel, b):
    d = D / rel
    os.makedirs(lp(d.parent), exist_ok=True)
    t = Path(lp(d)).with_name(d.name + ".tmp_reproc")
    with open(str(t), "wb") as fh:
        fh.write(b)
    os.replace(str(t), lp(d))


IP = D / "INDICE_PUBLICO.json"
idx = json.loads(IP.read_text(encoding="utf-8"))
pos = {a["caminho"]: i for i, a in enumerate(idx["arquivos"])}
EP = D / "EXCLUSOES_PUBLICAS.json"
exc = json.loads(EP.read_text(encoding="utf-8"))
LP = W / ("varredura_exclusoes_%s.json" % D.name)
local = json.loads(LP.read_text(encoding="utf-8"))
mudados, entraram = [], Counter()
recusados_agora = []

# 1. regravar os textos com máscara indevida
for a in idx["arquivos"]:
    rel = a["caminho"]
    if ext(rel) not in TXT:
        continue
    d = D / rel
    try:
        cur = open(lp(d), "rb").read()
    except OSError:
        continue
    if MASK.encode("utf-8") not in cur:
        continue
    b, motivo = esteira_texto(rel)
    if b is None:   # a regra apertou (ex.: o Escritório): sai do preparo, com o motivo
        recusados_agora.append((rel, motivo))
        continue
    if b != cur:
        gravar(rel, b)
        mudados.append(rel)
    a["bytes"], a["sha256"] = len(b), hashlib.sha256(b).hexdigest()   # sempre: uma rodada interrompida pode ter deixado o índice velho

# 2. reavaliar os excluídos por dado pessoal
if TIPO == "nucleo":
    # o critério do núcleo para documento original: o texto extraído (vault/normalized_docs/<rel>.txt) traz CPF/RG/telefone?
    pdf_pii = set()
    for p in (CENTRAL / "vault" / "normalized_docs").rglob("*.txt"):
        _, c = mascarar(p.read_text(encoding="utf-8", errors="replace"))
        if any(k in c for k in SENS_PII):
            pdf_pii.add(p.relative_to(CENTRAL / "vault" / "normalized_docs").as_posix()[:-4])
    motivos = {"documento original com dado pessoal (o texto técnico segue nas partes separadas)": "original",
               "texto de documento com dado pessoal (formulário)": "texto_formulario",
               "documento ou compactado com dado pessoal, protocolo ou credencial": "binario",
               "carga embutida com dado pessoal": "texto"}
else:
    motivos = {"carga embutida com dado pessoal": "texto", "PDF com dado pessoal ou credencial": "pdf"}
for m, modo in motivos.items():
    ficam = []
    for rel in local.get(m, []):
        ok = None
        try:
            if modo in ("texto", "texto_formulario"):
                if modo == "texto_formulario" and rel[len("vault/normalized_docs/"):-4] in pdf_pii:
                    ficam.append(rel); continue
                ok, _ = esteira_texto(rel)
            elif modo == "original":
                if rel in pdf_pii:
                    ficam.append(rel); continue
                raw = open(lp(SRC / rel), "rb").read()
                n_cred, kk = GP.avaliar_bytes(rel.rsplit("/", 1)[-1], raw)
                ok = raw if not (n_cred or kk) else None
            elif modo in ("binario", "pdf"):
                raw = open(lp(SRC / rel), "rb").read()
                if modo == "pdf" and not GP.pdf_da_casa(raw):
                    ok = None
                else:
                    n_cred, kk = GP.avaliar_bytes(rel.rsplit("/", 1)[-1], raw)
                    ok = raw if not (n_cred or kk) else None
        except OSError:
            ok = None
        if ok is None:
            ficam.append(rel); continue
        gravar(rel, ok)
        if rel in pos:
            idx["arquivos"][pos[rel]].update({"bytes": len(ok), "sha256": hashlib.sha256(ok).hexdigest()})
        else:
            idx["arquivos"].append({"caminho": rel, "bytes": len(ok), "sha256": hashlib.sha256(ok).hexdigest()})
            pos[rel] = len(idx["arquivos"]) - 1
        entraram[m] += 1
    local[m] = ficam
    if entraram[m]:
        exc["por_motivo"][m] = exc["por_motivo"].get(m, 0) - entraram[m]
        if not exc["por_motivo"][m]:
            del exc["por_motivo"][m]
if recusados_agora:   # tira do preparo e do índice os que a regra apertada recusou
    fora_ids = {r for r, _ in recusados_agora}
    for r in fora_ids:
        q = "\\\\?\\" + str((D / r).resolve())
        if os.path.exists(q):
            os.remove(q)
    idx["arquivos"] = [x for x in idx["arquivos"] if x["caminho"] not in fora_ids]
    for r, m in recusados_agora:
        exc["por_motivo"][m] = exc["por_motivo"].get(m, 0) + 1
        local.setdefault(m, []).append(r)
idx["n_arquivos"] = len(idx["arquivos"])
exc["reprocessado_em_22out"] = {"recusados_pela_regra_apertada": len(recusados_agora),"textos_regravados": len(mudados), "excluidos_que_entraram": dict(entraram),
                                "motivo": "o padrão de RG lia «RG» (Relatividade Geral) e «identidade» (termo da TGL) como documento"}
for p, obj in ((IP, idx), (EP, exc), (LP, local)):
    t = p.with_name(p.name + ".tmp_reproc")
    t.write_text(json.dumps(obj, ensure_ascii=False, indent=(None if p == IP else 1)), encoding="utf-8")
    os.replace(t, p)
print("%s: %d textos regravados | recusados agora: %d | entraram: %s | índice agora %d" % (D.name, len(mudados), len(recusados_agora), dict(entraram), idx["n_arquivos"]))
for r in mudados[:12]:
    print("   regravado:", r)
