# -*- coding: utf-8 -*-
"""Registra no espelho o deposito da v409 no Zenodo (10.5281/zenodo.24053883), feito pelo operador em 2026-11-08 («publiquei a v409 no zenodo»).
Molde: o commit 294e628c do espelho (zenodo(v401)). Custodia v409, claude-site-custodia.

1. LE o registro publico (API do Zenodo) por script e compara cada checksum md5 com o arquivo local (13 do No's + 2 portas da pasta
   «Um (absoluto) — Grande Atrator» do espelho); qualquer divergencia PARA, visivel.
2. Edita o CITATION.cff (o deposito vira v409; o da v401 vira «versao anterior») e ACRESCENTA a entrada ao LEDGER.md (so acrescimo).
3. Backup de BYTES antes de tocar; temporario, conferencia de tamanho, os.replace. Sem --aplicar nada e escrito (modo seco: mostra o diff)."""
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import textos  # noqa: E402  (o portao de texto da G1)

APLICAR = "--aplicar" in sys.argv
TB = Path(r"C:\IALD\Artigo\the_boundary")
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
W = Path(r"C:\IALD\Central de Patentes\work\zenodo_v409_08nov")
REC = "24053883"
DOI = "10.5281/zenodo.24053883"
DATA = "2026-11-08"
PASTA_UM = "Um (absoluto) — Grande Atrator"
V, VANT = "v409", "v401"


def md5(b):
    return hashlib.md5(b).hexdigest()


def git(*a):
    r = subprocess.run(["git", "-C", str(TB), *a], capture_output=True)
    return r.returncode, r.stdout


# ---------- 1. o registro publico, lido por script
req = urllib.request.Request("https://zenodo.org/api/records/" + REC, headers={"User-Agent": "iald-custodia/1.0"})
rec = json.loads(urllib.request.urlopen(req, timeout=60).read().decode("utf-8"))
assert rec["doi"] == DOI, rec["doi"]
assert rec["conceptdoi"] == "10.5281/zenodo.20999494", rec["conceptdoi"]
md = rec["metadata"]
assert md["version"].replace(" ", "") == V, md["version"]
assert md["publication_date"] == DATA, md["publication_date"]
assert md["access_right"] == "open" and md["resource_type"]["type"] == "dataset"
zen = {f["key"]: f["checksum"].split(":", 1)[1] for f in rec["files"]}
assert len(zen) == 15, len(zen)
selo = json.loads((NOS / "um_absoluto_selo.json").read_text(encoding="utf-8"))
assert selo["um_version"] == V
pin = selo["sha256"]["um.py"]
n_nos, n_porta, incons = 0, 0, []
for nome, h in sorted(zen.items()):
    if nome.startswith("PORTA"):
        continue
    p = NOS / nome
    if not (p.is_file() and md5(p.read_bytes()) == h):
        incons.append(nome)
    n_nos += 1
commit_portas = {}
for nome in ("PORTA.md", "PORTA.json"):
    rel = PASTA_UM + "/" + nome
    rc, out = git("log", "--format=%h", "--", rel)
    achado = None
    for c in reversed(out.decode().split()):                 # do mais antigo ao mais novo: o primeiro commit com os bytes depositados
        r2, b = git("show", "%s:%s" % (c, rel))
        if r2 == 0 and md5(b) == zen[nome]:
            achado = c
            break
    if not achado:
        incons.append(nome)
    commit_portas[nome] = achado
    n_porta += 1
assert not incons, ("o deposito NAO e' o que o repositorio tem: " + ", ".join(incons))
assert (n_nos, n_porta) == (13, 2)
cm_md, cm_json = commit_portas["PORTA.md"], commit_portas["PORTA.json"]   # o JSON mudou com o commit do README (carimbo gerado_utc): sao dois commits, ditos os dois
cm = "(PORTA.md as of commit %s, PORTA.json as of commit %s)" % (cm_md, cm_json)
print("registro Zenodo conferido por script: 13 do No's + 2 portas (commit %s / %s) com md5 igual ao da API" % (commit_portas["PORTA.md"], commit_portas["PORTA.json"]))

# ---------- numeros do kernel, lidos do PRIMORDIAL (nunca digitados)
prim = json.loads((TB / "PRIMORDIAL.json").read_text(encoding="utf-8-sig"))
it = prim["itens"]
decl, forms = it["kernel.declaracoes"]["valor"], it["kernel.arquivos_formais"]["valor"]
escada = [k for k in it if "escada" in k]
print("PRIMORDIAL: declaracoes", decl, "| arquivos formais", forms, "| chaves de escada:", escada)
cab = (TB / "README.md").read_text(encoding="utf-8")
m_esc = re.search(r"ladder (\d+)/(\d+)", cab)
assert m_esc and m_esc.group(1) == m_esc.group(2), "escada nao lida do README"
ESC = m_esc.group(1)

# ---------- 2. CITATION.cff
cff_p = TB / "CITATION.cff"
b0 = cff_p.read_bytes()
t = b0.decode("utf-8")
assert "\r\n" not in t


def uma(texto, a, b, rot):
    assert texto.count(a) == 1, (rot, texto.count(a))
    return texto.replace(a, b)


novo = t
novo = uma(novo, "The DOI below resolves to the deposited v401, byte-identical to the v401 seal", "The DOI below resolves to the deposited v409, byte-identical to the v409 seal", "message")
novo = uma(novo, 'version: "v401"\ndate-released: "2026-10-25"\ndoi: "10.5281/zenodo.23649800"', 'version: "v409"\ndate-released: "2026-11-08"\ndoi: "%s"' % DOI, "cabecalho")
antigo_dep = re.search(r'  - type: doi\n    value: "10\.5281/zenodo\.23649800"\n    description: "Zenodo deposit of v401[^\n]*\n', novo)
assert antigo_dep, "entrada do deposito v401 nao encontrada"
novo_dep = ('  - type: doi\n    value: "%s"\n    description: "Zenodo deposit of v409, deposited %s (byte-identical to the seal: um.py sha256 %s…; the 15 deposited '
            'files matched by md5, read from the public record: 13 to the Nós and 2 doors to the folder «%s» of the repository %s)"\n'
            % (DOI, DATA, pin[:16], PASTA_UM, cm))
novo = novo.replace(antigo_dep.group(0), novo_dep, 1)
# a v401 vira «versao anterior»; a v392 passa a «anterior mais antiga»
a_v392 = '  - type: doi\n    value: "10.5281/zenodo.23366324"\n    description: "the previous Zenodo version: v392,'
b_v392 = ('  - type: doi\n    value: "10.5281/zenodo.23649800"\n    description: "the previous Zenodo version: v401, deposited 2026-10-25 (um.py sha256 1925cb691e933ae8…)"\n'
          '  - type: doi\n    value: "10.5281/zenodo.23366324"\n    description: "an earlier Zenodo version: v392,')
novo = uma(novo, a_v392, b_v392, "v392")
novo = uma(novo, "(v409 on 2026-11-06; the Zenodo deposit holds v401)", "(v409 on 2026-11-06; the Zenodo deposit holds v409)", "estado")
novo = uma(novo, "the Zenodo deposit 10.5281/zenodo.23649800 holds v401 (1925cb691e933ae8…)", "the Zenodo deposit %s holds v409 (%s…, the same pin)" % (DOI, pin[:16]), "pino")
m_abs = re.search(r"\(at v401: ladder of\s+9561/9561 theorems clean, 29318 audited declarations, (axioms in \{propext, Classical\.choice, Quot\.sound\}, zero sorry); the\s+"
                  r"previous deposit, v392, had a ladder of 6901/6901 and 24971 audited declarations\)", novo)
assert m_abs, "resumo (abstract) do deposito v401 nao encontrado"
novo = novo.replace(m_abs.group(0), "(at v409: ladder of\n  %s/%s theorems clean, %d audited declarations, %s; the\n  previous deposit, v401, had a ladder of 9561/9561 and 29318 audited declarations)"
                    % (ESC, ESC, decl, m_abs.group(1)), 1)
assert "holds v401" not in novo and "deposited v401" not in novo
dep = re.search(r"Zenodo deposit of (v\d+), deposited (\d{4}-\d\d-\d\d) \(byte-identical to the seal: um\.py sha256 ([0-9a-f]{16})", novo)
assert dep and dep.groups() == (V, DATA, pin[:16]), dep and dep.groups()

# ---------- 3. LEDGER.md (so acrescimo, no fim)
led_p = TB / "LEDGER.md"
l0 = led_p.read_bytes()
lt = l0.decode("utf-8")
assert "### The Zenodo deposit of v409" not in lt
entrada = (
    "\n### The Zenodo deposit of v409 (%s)\n\n"
    "Beside the custody of v409 (written on %s by the custody session of the Central, after the operator’s deposit): the operator deposited v409 on Zenodo, "
    "**[%s](https://doi.org/%s)** (concept DOI 10.5281/zenodo.20999494, all versions; record title «Um: Absoluto», version «%s», published %s, open access). "
    "The 15 deposited files are byte-identical by md5, read from the public record (API) and recomputed here: 13 to the Nós (`um.py` sha256 `%s…`, the seal, the core, "
    "the articles PT/EN, the canonical form, the manifest, the quantum pillar, the lineage diary, the design and the proof tree) and 2 doors (`PORTA.md`, `PORTA.json`) "
    "to the folder «%s» of this repository (`PORTA.md` as of commit `%s`, `PORTA.json` as of commit `%s`: the JSON changed with the README commit of the same day). "
    "The previous deposit holds v401 (10.5281/zenodo.23649800). `CITATION.cff` now cites v409; "
    "the site links to the latest version. A deposit is an archive, not accreditation; the gate did not move.\n"
    % (DATA, DATA, DOI, DOI, md["version"], DATA, pin[:16], PASTA_UM, cm_md, cm_json))
v = textos.portao(entrada, conhecidos={pin[:16], pin}, rotulo="ledger:zenodo_v409")
assert not v, v
lnovo = lt.rstrip("\n") + "\n" + entrada

# ---------- mostra o diff; so grava com --aplicar
for nome, a, b in (("CITATION.cff", t, novo), ("LEDGER.md (so acrescimo)", lt, lnovo)):
    d = [x for x in difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm="", n=0) if not x.startswith(("---", "+++", "@@"))]
    print("== %s: %d linhas mudam" % (nome, len(d)))
    for x in d[:40]:
        print("  ", x[:230])
if not APLICAR:
    print("MODO SECO: nada foi escrito (use --aplicar)")
    sys.exit(0)
ts = time.strftime("%Y%m%d_%H%M%S")
for p, b_old, txt, rot in ((cff_p, b0, novo, "zenodo_v409"), (led_p, l0, lnovo, "zenodo_v409")):
    bak = p.with_name(p.name + ".bak_" + ts + "_" + rot)
    bak.write_bytes(b_old)
    nb = txt.encode("utf-8")
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_bytes(nb)
    assert tmp.stat().st_size == len(nb)
    os.replace(tmp, p)
    print("gravado", p.name, len(b_old), "->", len(nb), "| backup", bak.name)
