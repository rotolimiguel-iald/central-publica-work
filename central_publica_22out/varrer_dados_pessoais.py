# -*- coding: utf-8 -*-
"""Varredura (SÓ LEITURA) de DADOS PESSOAIS e CREDENCIAIS no universo publicável da Central (ordem do operador, 22/10/2026:
«segredo são dados pessoais, somente»). Percorre a árvore rastreada da Central, work/ e Chatgpt/ com a mesma seleção do medir_publicavel.py
e conta, por categoria, os arquivos com ocorrência. NUNCA imprime o dado: só a categoria, a contagem e exemplos MASCARADOS de caminho.
Saída: varredura_dados_pessoais.json (para a decisão excluir/mascarar)."""
import json, os, re, subprocess, sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
C = Path(r"C:\IALD\Central de Patentes")
W = C / "work" / "central_publica_22out"
TXT = {".py", ".lean", ".md", ".json", ".jsonl", ".txt", ".tex", ".csv", ".tsv", ".toml", ".yaml", ".yml", ".js", ".mjs", ".ts", ".tsx",
       ".html", ".css", ".ipynb", ".sh", ".ps1", ".bat", ".cfg", ".ini", ".sql", ".bib", ".sty", ".cls", ".r", ".jl", ".c", ".h", ".cpp",
       ".rs", ".go", ".java", ".svg", ".xml", ".dat", ".log", ".out", ".diff", ".patch", ".pysnip", ".spec"}
EXCL_DIR = {".git", ".venv", "venv", "node_modules", "__pycache__", ".lake", "tex_environment", ".wheels_ipv4", "unsloth_compiled_cache",
            "site-packages", "dist-packages", ".mypy_cache", ".pytest_cache", "build", ".cache"}
LIM = 25 * 1024 * 1024
INSTITUCIONAL = re.compile(r"@(?:[\w-]+\.)*(?:wipo\.int|inpi\.gov\.br|gov\.br|example\.(?:com|org)|anthropic\.com|openai\.com|github\.com|"
                           r"users\.noreply\.github\.com|noreply\.[\w.]+|arxiv\.org|zenodo\.org|cern\.ch|iald\.ia\.br|python\.org|localhost|test|"
                           r"teoriadagravitacaoluminodinamica\.com)\b", re.I)
PAD = {
    "cpf": re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b"),
    "cpf_rotulado": re.compile(r"(?i)\bCPF\b[^\n]{0,12}\b\d{11}\b"),
    "rg_rotulado": re.compile(r"(?i)\b(?:RG|identidade)\b[^\n]{0,15}\b\d[\d.\-]{6,12}\b"),
    "telefone": re.compile(r"(?i)(?:tel|fone|cel|whats|telefone|celular)[^\n]{0,12}(?:\+?55\s?)?\(?\d{2}\)?\s?9?\d{4}[-\s]?\d{4}"),
    "email_pessoal": re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b"),
    "credencial_token": re.compile(r"(ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|gh[osu]_[A-Za-z0-9]{30,}|sk-ant-[A-Za-z0-9_-]{20,}|"
                                   r"sk-proj-[A-Za-z0-9_-]{20,}|hf_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,}|"
                                   r"-----BEGIN [A-Z ]*PRIVATE KEY-----)"),
    "credencial_atribuida": re.compile(r"(?i)(?:password|passwd|senha|secret_key|api_key|apikey|access_token|client_secret|smtp_pass)"
                                       r"[\"']?\s*[:=]\s*[\"'][^\"'\s]{8,}[\"']"),
}


def candidatos():
    tr = subprocess.run(["git", "-C", str(C), "ls-files", "-z"], capture_output=True).stdout.decode("utf-8", "replace").split("\0")
    for t in tr:
        if t:
            yield "central", C / t
    for reg in ("work", "Chatgpt"):
        for dp, dns, fns in os.walk(C / reg):
            dns[:] = [d for d in dns if d not in EXCL_DIR]
            for f in fns:
                yield reg, Path(dp) / f


cont = defaultdict(Counter)
exemplos = defaultdict(list)
arquivos_com = defaultdict(set)
n = 0
for reg, p in candidatos():
    e = p.suffix.lower()
    if e not in TXT or ".bak_" in p.name or ".tmp" in p.name:
        continue
    try:
        s = p.stat().st_size
        if s > LIM or s == 0:
            continue
        t = p.read_bytes().decode("utf-8", "replace")
    except OSError:
        continue
    n += 1
    for k, rx in PAD.items():
        ms = rx.findall(t)
        if k == "email_pessoal":
            ms = [m for m in ms if not INSTITUCIONAL.search(m) and not m.lower().endswith((".png", ".jpg", ".py", ".json"))]
        if ms:
            cont[reg][k] += 1
            arquivos_com[k].add(str(p))
            if len(exemplos[k]) < 6:
                rel = str(p.relative_to(C))
                exemplos[k].append(re.sub(r"(?i)([a-z0-9]{3})[a-z0-9]{4,}", r"\1…", rel)[:110])
emails = Counter()
for p in list(arquivos_com["email_pessoal"])[:200000]:
    try:
        t = Path(p).read_bytes().decode("utf-8", "replace")
    except OSError:
        continue
    for m in PAD["email_pessoal"].findall(t):
        if not INSTITUCIONAL.search(m):
            dom = m.split("@")[-1].lower()
            emails[dom] += 1
out = {"arquivos_varridos": n, "por_regiao": {r: dict(c) for r, c in cont.items()},
       "arquivos_por_categoria": {k: len(v) for k, v in arquivos_com.items()}, "exemplos_mascarados": exemplos,
       "dominios_de_email_mais_frequentes": emails.most_common(25)}
(W / "varredura_dados_pessoais.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
(W / "varredura_arquivos_por_categoria.json").write_text(json.dumps({k: sorted(v) for k, v in arquivos_com.items()}, ensure_ascii=False), encoding="utf-8")
print(json.dumps({k: v for k, v in out.items() if k != "exemplos_mascarados"}, ensure_ascii=False, indent=1)[:3000])
