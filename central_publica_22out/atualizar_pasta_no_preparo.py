# -*- coding: utf-8 -*-
"""Atualiza, no preparo do WORK, uma pasta inteira que mudou depois que o construtor passou por ela (22/10/2026: a própria pasta desta
abertura, work/central_publica_22out — o construtor copiou os scripts no meio do caminho; o público deve ver a esteira FINAL que rodou),
pela mesma esteira da região (guarda pública, regra do Escritório, máscara visível, filtro das notas nos .md). Fora, como no construtor:
as listas locais de varredura (varredura_*), backups e temporários. Atualiza/acrescenta as linhas no INDICE_PUBLICO.json e apaga do preparo o
que não existe mais na origem. Uso: atualizar_pasta_no_preparo.py <pasta_do_preparo_work> <subpasta_do_work>"""
import hashlib, json, os, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
W = Path(__file__).resolve().parent
sys.path.insert(0, str(W))
from mascara_pii import mascarar  # noqa: E402
from filtro_operacional import filtrar_markdown  # noqa: E402
import guarda_publica as GP  # noqa: E402

D, SUB = Path(sys.argv[1]), sys.argv[2].strip("/\\")
SRC = Path(r"C:\IALD\Central de Patentes\work") / SUB
TXT = {".py", ".md", ".json", ".jsonl", ".txt", ".tex", ".csv", ".yaml", ".yml", ".html", ".js", ".ts", ".log", ".out", ".xml", ".toml", ".ini",
       ".cfg", ".sh", ".ps1", ".bat", ".diff", ".patch"}
FORA = re.compile(r"(?i)(^varredura_|\.bak_|\.tmp|__pycache__|^conferencia_|^subida_|^ja_vistos_|^git_(add|rm)_)")   # subida_*: o log do envio do site traz o usuário e o caminho da hospedagem
# (22/10/2026, custódia v396) ja_vistos_*.json repete os caminhos das listas LOCAIS de exclusão (que não se publicam: os próprios nomes
# podem ser nota ou dado); git_add_/git_rm_ são listas de trabalho do envio incremental
# os scripts da própria esteira trazem os PADRÕES da regra do Escritório e exemplos FICTÍCIOS (revistos um a um em 22/10/2026): a regra do
# Escritório não os barra; credencial e dado pessoal continuam valendo para eles
ESTEIRA = {"aplicar_regra_escritorio.py", "conferir_preparos.py", "guarda_publica.py", "testar_regra_escritorio.py"}
IP = D / "INDICE_PUBLICO.json"
idx = json.loads(IP.read_text(encoding="utf-8"))
pos = {a["caminho"]: i for i, a in enumerate(idx["arquivos"])}
pref = SUB.replace("\\", "/") + "/"
vistos, novos, mudados, recusados = set(), 0, 0, []
for p in sorted(SRC.rglob("*")):
    if not p.is_file() or any(FORA.search(x) for x in p.relative_to(SRC).parts):
        continue
    rel = pref + p.relative_to(SRC).as_posix()
    if p.suffix.lower() not in TXT:
        recusados.append((rel, "formato fora da esteira de texto")); continue
    txt = p.read_bytes().decode("utf-8", "replace")
    n_cred, pii = GP.avaliar_texto(txt)
    if n_cred or pii or (GP.toca_escritorio(txt) and p.name not in ESTEIRA):
        recusados.append((rel, "guarda pública")); continue
    txt, _c = mascarar(txt)
    if rel.endswith(".md"):
        txt, _n = filtrar_markdown(txt)
    b = txt.encode("utf-8")
    d = D / rel
    os.makedirs(d.parent, exist_ok=True)
    if not d.is_file() or d.read_bytes() != b:
        t = d.with_name(d.name + ".tmp_atual")
        t.write_bytes(b)
        os.replace(t, d)
        mudados += 1
    linha = {"caminho": rel, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
    if rel in pos:
        idx["arquivos"][pos[rel]] = linha
    else:
        idx["arquivos"].append(linha); pos[rel] = len(idx["arquivos"]) - 1; novos += 1
    vistos.add(rel)
# o que está no preparo sob a pasta e já não existe (ou ficou fora) na origem sai
sobras = [a["caminho"] for a in idx["arquivos"] if a["caminho"].startswith(pref) and a["caminho"] not in vistos]
for rel in sobras:
    q = D / rel
    if q.is_file():
        q.unlink()
idx["arquivos"] = [a for a in idx["arquivos"] if a["caminho"] not in set(sobras)]
idx["n_arquivos"] = len(idx["arquivos"])
t = IP.with_name(IP.name + ".tmp_atual")
t.write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
os.replace(t, IP)
print("%s/%s: %d gravados ou atualizados (%d novos) | %d sobras tiradas | %d recusados %s | índice agora %d" % (
    D.name, SUB, mudados, novos, len(sobras), len(recusados), recusados[:6], idx["n_arquivos"]))
