# -*- coding: utf-8 -*-
"""02/11/2026: MEMORY.md passou do teto (24259 B > 24000) com a linha da avaliação do site (11:37). Regra dos dois arquivos:
duas linhas vão VERBATIM ao fim do MEMORY_2.md e ficam no índice como ponteiro curto. Backup de bytes; temporário → conferir → replace."""
import datetime, os, subprocess
from pathlib import Path

M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
P1, P2 = M / "MEMORY.md", M / "MEMORY_2.md"
b1, b2 = P1.read_bytes(), P2.read_bytes()
nl1 = b"\r\n" if b"\r\n" in b1 else b"\n"
nl2 = b"\r\n" if b"\r\n" in b2 else b"\n"
lines = b1.split(nl1)

alvos = {
    "- **[AVALIAÇÃO DO SITE E DOS FILMES; o número sem procedência (02/11)](avaliacao-site-e-filmes-02nov.md)**":
        "- **[AVALIAÇÃO DO SITE E DOS FILMES (02/11)](avaliacao-site-e-filmes-02nov.md)** — guarda de procedência de número no guarda_do_selo v4 · íntegra no MEMORY_2.md (movida 02/11)",
    "- **[SESSÃO 5σ COM A IALD NATIVA v4 (02/11)](sessao-iald-nativa-5sigma-02nov.md)**":
        "- **[SESSÃO 5σ COM A IALD NATIVA v4 (02/11)](sessao-iald-nativa-5sigma-02nov.md)** · **[R-E e Landauer](rota-re-k-e-landauer-02nov.md)** · **[vazar é luzir](vazar-e-luzir-02nov.md)** · **[K é a chave da guarda](k-chave-da-guarda-02nov.md)** — N_eff 2,48σ; D8/X16 dele · íntegra no MEMORY_2.md (movida 02/11)",
}
movidas = []
novas = []
for raw in lines:
    s = raw.decode("utf-8")
    hit = next((k for k in alvos if s.startswith(k)), None)
    if hit:
        movidas.append(s)
        novas.append(alvos[hit].encode("utf-8"))
    else:
        novas.append(raw)
assert len(movidas) == 2, movidas
out1 = nl1.join(novas)
print("MEMORY.md", len(b1), "->", len(out1), "B;", len(novas), "linhas")
assert len(out1) <= 24000 and len(novas) <= 195

bloco = ("\n\n## Linhas movidas do MEMORY.md em 02/11/2026 (regra dos dois arquivos; o índice passou do teto de 24.000 B com a linha da avaliação do site)\n\n"
         + "\n".join(movidas) + "\n").replace("\n", nl2.decode())
out2 = b2.rstrip() + bloco.encode("utf-8")

for P, b, out in ((P2, b2, out2), (P1, b1, out1)):
    bak = P.with_name(P.name + ".bak_" + TS)
    with open(bak, "xb") as f:
        f.write(b)
    assert bak.read_bytes() == b
    tmp = P.with_name(P.name + ".tmp_" + TS)
    with open(tmp, "xb") as f:
        f.write(out)
    assert tmp.stat().st_size == len(out)
    os.replace(tmp, P)
    print(P.name, len(b), "->", P.stat().st_size)
assert P2.stat().st_size > len(b2)

env = dict(os.environ, MEMORIA_GERENCIA="claude-c1")
for cmd in (["pinar"], ["verificar"]):
    r = subprocess.run(["C:/Python314/python.exe", "-X", "utf8", "memoria.py", *cmd], cwd=str(M / "fila"), capture_output=True, env=env)
    print(cmd[0], "rc", r.returncode, r.stdout.decode("utf-8", "replace").replace("\n", " ")[:260])
