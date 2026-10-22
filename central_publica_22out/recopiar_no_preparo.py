# -*- coding: utf-8 -*-
"""Recopia para um preparo público arquivos de texto que mudaram (na origem ou na máscara) depois que o construtor passou por eles —
22/10/2026: as erratas do titular nas memórias; a máscara dos identificadores de terceiros — pela MESMA esteira dos construtores: guarda
pública (credencial, carga embutida), máscara visível, filtro das notas nos .md, regra do Escritório no que vai ao ar. Atualiza a linha de
cada um no INDICE_PUBLICO.json. Só arquivos já presentes no índice; recusa o resto.
Uso: recopiar_no_preparo.py <pasta_do_preparo> [--origem <pasta_de_origem>] (<caminho> ... | @<lista.txt>)
     (origem padrão: a raiz da Central — o núcleo; para as regiões, C:\\IALD\\Central de Patentes\\work ou ...\\Chatgpt)"""
import hashlib, json, os, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mascara_pii import mascarar  # noqa: E402
from filtro_operacional import filtrar_markdown  # noqa: E402
import guarda_publica as GP  # noqa: E402

args = sys.argv[1:]
D = Path(args.pop(0))
SRC = Path(r"C:\IALD\Central de Patentes")
if args and args[0] == "--origem":
    args.pop(0)
    SRC = Path(args.pop(0))
rels = []
for a in args:
    if a.startswith("@"):
        rels += [x.strip() for x in Path(a[1:]).read_text(encoding="utf-8").splitlines() if x.strip()]
    else:
        rels.append(a)
IP = D / "INDICE_PUBLICO.json"
idx = json.loads(IP.read_text(encoding="utf-8"))
pos = {a["caminho"]: i for i, a in enumerate(idx["arquivos"])}
TXT = (".md", ".txt", ".json", ".jsonl", ".py", ".yaml", ".yml", ".html", ".js", ".ts", ".tsx", ".log", ".csv", ".tex", ".lean", ".ps1", ".sh",
       ".toml", ".ini", ".cfg", ".xml", ".out")
ESTEIRA = {"aplicar_regra_escritorio.py", "conferir_preparos.py", "guarda_publica.py", "testar_regra_escritorio.py"}
recusados, feitos = [], 0
for t in rels:
    if t not in pos:
        recusados.append((t, "fora do índice")); continue
    if not t.lower().endswith(TXT):
        recusados.append((t, "não é texto")); continue
    txt = open("\\\\?\\" + str((SRC / t).resolve()), "rb").read().decode("utf-8", "replace")
    n_cred, pii = GP.avaliar_texto(txt)
    if n_cred or pii:
        recusados.append((t, "a guarda recusa")); continue
    txt, c = mascarar(txt)
    if t.endswith(".md"):
        txt, n = filtrar_markdown(txt)
    if GP.toca_escritorio(txt) and t.rsplit("/", 1)[-1] not in ESTEIRA:
        recusados.append((t, "Escritório")); continue
    b = txt.encode("utf-8")
    dst = "\\\\?\\" + str((D / t).resolve())
    tmp = dst + ".tmp_recopia"
    with open(tmp, "wb") as fh:
        fh.write(b)
    os.replace(tmp, dst)
    idx["arquivos"][pos[t]] = {"caminho": t, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
    feitos += 1
tmp = IP.with_name(IP.name + ".tmp_recopia")
tmp.write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
os.replace(tmp, IP)
print("%s: %d recopiados | %d recusados %s | índice %d" % (D.name, feitos, len(recusados), recusados[:8], idx["n_arquivos"]))
