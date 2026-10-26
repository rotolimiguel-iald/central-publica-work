# -*- coding: utf-8 -*-
"""O depósito da v401 no Zenodo nas superfícies (25/10/2026, gerência a7). Lê o depósito do CITATION.cff (já reescrito por zenodo_v401_citation.py):
 1. a nota de estado da v401 no gerador do ESTADO_ATUAL (a custódia corrente: «The Zenodo deposit holds v392 (…)» vira o depósito novo);
 2. o LEDGER (só acréscimo): uma entrada datada, ao lado da seção da v401, com o depósito e a conferência por md5;
 3. o ESTADO_ATUAL regerado pelo gerador; 4. o laço E08 do G1 (portas, README, read-brief, llms) pela própria função;
 5. o site: aplicar_selo.py (os links ao Zenodo vão à versão mais recente), index.md, llms-full e o cartão de estado.
Backup de bytes; trocas contadas."""
import json, os, re, subprocess, time
from pathlib import Path

TS = time.strftime("%Y%m%d_%H%M%S")
PY = r"C:\Python314\python.exe"
TB = Path(r"C:\IALD\Artigo\the_boundary")
BANC = Path(r"C:\IALD\Site\tgl\v3.0_bancada")
W = Path(r"C:\IALD\Central de Patentes\work\custodia_v401_25out")
cff = (TB / "CITATION.cff").read_text(encoding="utf-8")
doi = re.search(r'^doi: "(10\.5281/zenodo\.\d+)"', cff, re.M).group(1)
m = re.search(r'Zenodo deposit of (v\d+), deposited ([0-9-]{10}) \(byte-identical to the seal: um\.py sha256 ([0-9a-f]{16})…; the (\d+) deposited files matched by md5: (\d+) to the Nós and (\d+) doors', cff)
ver, data, pin16, nf, nn, ne = m.groups()
ma = re.search(r'value: "(10\.5281/zenodo\.\d+)"\n    description: "the previous Zenodo version: (v\d+)', cff)
doi_ant, ver_ant = ma.groups()


def trocar(p, a, b):
    raw = p.read_bytes(); s = raw.decode("utf-8")
    assert s.count(a) == 1, (p.name, a[:70], s.count(a))
    p.with_name(p.name + ".bak_" + TS).write_bytes(raw)
    t = p.with_name(p.name + ".tmp"); t.write_bytes(s.replace(a, b).encode("utf-8"))
    if p.suffix == ".py":
        import py_compile; py_compile.compile(str(t), doraise=True)
    os.replace(t, p)
    print("  %s: %d -> %d" % (p.name, len(raw), p.stat().st_size))


def rodar(args, cwd):
    r = subprocess.run([PY, "-X", "utf8"] + args, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(cwd))
    linhas = [l for l in (r.stdout or "").splitlines() if l.strip()]
    print("  [%s] rc=%d | %s" % (Path(args[0]).name, r.returncode, (linhas[-1] if linhas else (r.stderr or "")[-300:])[:220]))
    assert r.returncode == 0, "falhou: " + args[0]


# 1) a nota de estado da v401
G = TB / "tools" / "gerar_estado_atual.py"
velho = "the B(n) receipts of the Bancada are in `recibos_bancada_v401/`. The Zenodo deposit holds %s (%s). Not falsified" % (ver_ant, doi_ant)
novo = ("the B(n) receipts of the Bancada are in `recibos_bancada_v401/`. The Zenodo deposit holds %s (%s), deposited by the operator on %s after this "
        "custody; the %s deposited files are byte-identical by md5 (%s to the Nós, %s doors to the custody commit); the previous deposit holds %s (%s). Not falsified"
        % (ver, doi, data, nf, nn, ne, ver_ant, doi_ant))
if ("The Zenodo deposit holds %s (%s), deposited by the operator" % (ver, doi)) not in G.read_text(encoding="utf-8"):
    trocar(G, velho, novo)
# 2) o LEDGER: só acréscimo
L = TB / "LEDGER.md"
marca = "### The Zenodo deposit of %s (%s)" % (ver, data)
lt = L.read_bytes()
if marca.encode("utf-8") not in lt:
    nl = b"\r\n" if b"\r\n" in lt else b"\n"
    ent = ("\n%s\n\nBeside the custody of %s (written on %s by the session a7 of the Central, after the operator’s deposit): the operator deposited %s on Zenodo, "
           "**[%s](https://doi.org/%s)** (concept DOI 10.5281/zenodo.20999494, all versions). The %s deposited files are byte-identical by md5, read from the public "
           "record: %s to the Nós (`um.py` sha256 `%s…`, the seal, the core, the articles PT/EN, the canonical form, the manifest, the quantum pillar, the lineage diary, "
           "the design and the proof tree) and %s doors (`PORTA.md`, `PORTA.json`) to the custody commit of this repository. The previous deposit holds %s (%s). "
           "`CITATION.cff` now cites %s; the site links to the latest version. A deposit is an archive, not accreditation; the gate did not move.\n"
           % (marca, ver, data, ver, doi, doi, nf, nn, pin16, ne, ver_ant, doi_ant, ver)).replace("\n", nl.decode())
    L.with_name(L.name + ".bak_" + TS).write_bytes(lt)
    t = L.with_name(L.name + ".tmp"); t.write_bytes(lt + ent.encode("utf-8")); os.replace(t, L)
    assert L.stat().st_size > len(lt)
    print("  LEDGER.md: + %s (%d -> %d)" % (marca, len(lt), L.stat().st_size))
# 3) o ESTADO_ATUAL pelo gerador
rodar([str(G)], TB)
# 4) o laço E08 do G1
rodar([str(W / "rodar_e08_forcado.py")], W)
# 5) o site
rodar([str(BANC / "tools" / "aplicar_selo.py")], BANC)
for g in ("gerar_index_md.py", "gerar_llms_full.py", "gerar_cartao_estado.py"):
    rodar([str(BANC / "tools" / g)], BANC)
# conferência: o DOI novo nas superfícies; o antigo só como «anterior»
for p in [TB / "README.md", TB / "PORTA.json", TB / "ESTADO_ATUAL.md", TB / "read-brief.md", TB / "llms.txt", Path(r"C:\IALD\Site\tgl\v3.0\index.html"),
          Path(r"C:\IALD\Site\tgl\v3.0\llms.txt"), Path(r"C:\IALD\Site\tgl\v3.0\read-brief.md"), Path(r"C:\IALD\Site\tgl\v3.0\index.md"), Path(r"C:\IALD\Site\tgl\v3.0\estado.json")]:
    s = p.read_text(encoding="utf-8")
    print("  %-14s novo %2d | anterior %2d" % (p.name, s.count(doi.rsplit(".", 1)[1]), s.count(doi_ant.rsplit(".", 1)[1])))
