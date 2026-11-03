# -*- coding: utf-8 -*-
"""02/11/2026: compactação do MEMORY.md para a pré-condição p00 da v406 (bytes + 900 < 24000 e linhas + 1 <= 195).
Regra dos dois arquivos: as linhas vão ÍNTEGRAS ao fim do MEMORY_2.md e ficam no índice como ponteiro curto. Backup de bytes;
temporário → conferir → replace; pinar + verificar. Modelo: cadeia_de_selo\\v404\\compactar_indice_memoria_v404.py."""
import datetime, os, subprocess
from pathlib import Path
M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
P1, P2 = M / "MEMORY.md", M / "MEMORY_2.md"
b1, b2 = P1.read_bytes(), P2.read_bytes()
nl1 = b"\r\n" if b"\r\n" in b1 else b"\n"
nl2 = b"\r\n" if b2.rstrip(b"\n").endswith(b"\r") else b"\n"   # estilo da última linha (fim de linha misto)
lines = b1.split(nl1)
alvos = {
 "- **[O ORGANISMO — a torre de comando única (23/10)]": "- **[O ORGANISMO — a torre de comando única (23/10)](organismo-torre-de-comando-23out.md)** — íntegra no MEMORY_2.md (movida 02/11)",
 "- **[G1 — custodiar.py: a custódia numa só ordem (24/10)]": "- **[G1 — custodiar.py (24/10)](custodiar-g1-24out.md)** · [v403](licoes-cadeia-v403-28out.md) · [v404](licoes-cadeia-v404-28out.md) · [v405](licoes-custodia-v405-02nov.md) — íntegra no MEMORY_2.md (movida 02/11)",
 "- [A CENTRAL ABERTA (22/10)]": "- [A CENTRAL ABERTA (22/10)](central-publica-22out.md) — 3 repositórios públicos + /central/ + um.acom · íntegra no MEMORY_2.md (movida 02/11) <!-- central_publica_22out -->",
 "- **[5σ FORA DA COSMOLOGIA (27/10)]": "- **[5σ FORA DA COSMOLOGIA (27/10)](cinco-sigma-fora-da-cosmologia-27out.md)** — íntegra no MEMORY_2.md (movida 02/11)",
 "- **[E₀: Kimi conferido, no-go tipado, fórmula da massa (31/10)]": "- **[E₀: Kimi conferido, no-go tipado, fórmula da massa (31/10)](e0-cadeia-conferencia-kimi-e-no-go-31out.md)** · [28/10](transicao-para-a-massa-28out.md) — íntegra no MEMORY_2.md (movida 02/11)",
 "- **[HANDOFF v405 (30/10)]": "- **[HANDOFF v405 (30/10)](handoff-v405-pontes-da-massa-e-espelho-30out.md)** · [ObservadorTerminal (31/10)](observador-terminal-pedra-candidata-31out.md) — íntegra no MEMORY_2.md (movida 02/11)",
 "- **[A TORRE IALD — o JEV como chão da memória (31/10)]": "- **[A TORRE IALD — o JEV como chão da memória (31/10)](torre-iald-jev-memoria-31out.md)** — íntegra no MEMORY_2.md (movida 02/11)",
 "- **[A VITRINE DA TGL NO X (26/10)]": "- **[A VITRINE DA TGL NO X (26/10)](x-vitrine-da-tgl-26out.md)** — íntegra no MEMORY_2.md (movida 02/11)",
}
movidas, novas = [], []
for raw in lines:
    s = raw.decode("utf-8")
    hit = next((k for k in alvos if s.startswith(k)), None)
    if hit:
        movidas.append(s); novas.append(alvos[hit].encode("utf-8"))
    else:
        novas.append(raw)
assert len(movidas) == len(alvos), (len(movidas), [m[:50] for m in movidas])
out1 = nl1.join(novas)
print("MEMORY.md", len(b1), "->", len(out1), "B;", len(novas), "linhas")
assert len(out1) + 900 < 24000 and len(novas) + 1 <= 195, (len(out1), len(novas))
bloco = ("\n\n## Linhas movidas do MEMORY.md em 02/11/2026 (regra dos dois arquivos; pré-condição p00 da v406: bytes + 900 < 24000)\n\n" + "\n".join(movidas) + "\n").replace("\n", nl2.decode())
out2 = b2.rstrip(b"\r\n") + bloco.encode("utf-8")
assert out2.startswith(b2.rstrip(b"\r\n"))
for P, b, out in ((P2, b2, out2), (P1, b1, out1)):
    bak = P.with_name(P.name + ".bak_" + TS)
    with open(bak, "xb") as f: f.write(b)
    assert bak.read_bytes() == b
    tmp = P.with_name(P.name + ".tmp_" + TS)
    with open(tmp, "xb") as f: f.write(out)
    assert tmp.stat().st_size == len(out)
    os.replace(tmp, P); print(P.name, len(b), "->", P.stat().st_size)
env = dict(os.environ, MEMORIA_GERENCIA="claude-c1")
for cmd in (["pinar", "--motivo", "compactacao pre-v406 (p00: bytes+900<24000)"], ["verificar"]):
    r = subprocess.run(["C:/Python314/python.exe", "-X", "utf8", "memoria.py", *cmd], cwd=str(M / "fila"), capture_output=True, env=env)
    print(cmd[0], "rc", r.returncode, r.stdout.decode("utf-8", "replace").replace("\n", " ")[:160])
