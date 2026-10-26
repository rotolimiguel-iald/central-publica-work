# -*- coding: utf-8 -*-
"""O depósito da v401 no Zenodo (25/10/2026, ato do operador: «versão 401 publicada no zenodo: https://doi.org/10.5281/zenodo.23649800 …
atualize tudo também que corresponder ao zenodo»). A FONTE DE VERDADE do depósito na casa é o CITATION.cff do espelho: gerar_portas
(PORTA.json doi_um_absoluto), a frente do README (DEP_DOI), o G1 (textos.deposito_zenodo), o quadro do organismo («Zenodo deposit holds»)
e o aplicar_selo do site (os links ao Zenodo indicam sempre a versão mais recente; o DOI anterior vira «the previous Zenodo version») leem
dele. Este script só reescreve o CITATION.cff; os geradores fazem o resto.

Nada digitado que não seja lido: o DOI e o conceito vêm da API pública do Zenodo (GET), a conferência dos 15 arquivos é por md5 contra o Nós
(13) e contra o commit da custódia no espelho (as 2 portas), o pino e os números vêm do selo e do core do Nós; os dados da v392 vêm do próprio
CITATION.cff anterior. Backup de bytes; temporário -> conferir -> substituir."""
import hashlib, json, os, re, subprocess, time, urllib.request
from pathlib import Path

TS = time.strftime("%Y%m%d_%H%M%S")
TB = Path(r"C:\IALD\Artigo\the_boundary")
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
A3 = "Um (absoluto) \u2014 Grande Atrator"
REC = "23649800"
CFF = TB / "CITATION.cff"

api = json.load(urllib.request.urlopen("https://zenodo.org/api/records/" + REC, timeout=60))
doi, conceito = api["doi"], api["conceptdoi"]
assert doi == "10.5281/zenodo." + REC and api["metadata"]["title"] == "Um: Absoluto", (doi, api["metadata"]["title"])
pub = api["metadata"]["publication_date"]
files = api["files"] if isinstance(api["files"], list) else list(api["files"]["entries"].values())
head = subprocess.run(["git", "-C", str(TB), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
ok_nos = ok_esp = 0
for e in files:
    nome = e.get("key") or e.get("filename")
    z = e["checksum"].split(":", 1)[-1]
    p = NOS / nome
    if p.is_file() and hashlib.md5(p.read_bytes()).hexdigest() == z:
        ok_nos += 1; continue
    b = subprocess.run(["git", "-C", str(TB), "show", "%s:%s/%s" % (head, A3, nome)], capture_output=True).stdout
    assert b and hashlib.md5(b).hexdigest() == z, "arquivo do depósito não confere com o Nós nem com o espelho: " + nome
    ok_esp += 1
assert ok_nos + ok_esp == len(files), (ok_nos, ok_esp, len(files))
selo = json.loads((NOS / "um_absoluto_selo.json").read_text(encoding="utf-8"))
versao, pin = selo["um_version"], selo["sha256"]["um.py"]
assert any((e.get("key") or e.get("filename")) == "um.py" and e["checksum"].split(":", 1)[-1] == hashlib.md5((NOS / "um.py").read_bytes()).hexdigest() for e in files)
core = json.loads((NOS / "um_absoluto.json").read_text(encoding="utf-8"))["core"]
p1 = core["estatuto_da_prova_v391"]["prova_1_kernel"]
man = json.loads((NOS / "tgl_kernel_proof_manifest.json").read_text(encoding="utf-8"))
n_arq, n_decl = len(man["formal_files_sha256"]), len(man["axiom_report"])

raw = CFF.read_bytes(); s = raw.decode("utf-8")
m_dep = re.search(r'  - type: doi\n    value: "(10\.5281/zenodo\.\d+)"\n    description: "Zenodo deposit of (v\d+), deposited (\d{4}-\d\d-\d\d) \(byte-identical to the seal: um\.py sha256 ([0-9a-f]{16})…[^"]*"\n', s)
assert m_dep, "CITATION.cff sem a linha do depósito corrente — PARAR"
doi_ant, ver_ant, data_ant, pin_ant = m_dep.groups()
assert doi_ant != doi, "o CITATION.cff já registra este depósito"
m_abs = re.search(r"\(at (v\d+): ladder of\n  (\d+)/(\d+) theorems clean, (\d+) audited declarations", s)
assert m_abs and m_abs.group(1) == ver_ant, "o abstract não traz os números da versão depositada anterior — PARAR"
lad_ant, decl_ant = "%s/%s" % (m_abs.group(2), m_abs.group(3)), m_abs.group(4)

n = s
n = n.replace("The DOI below resolves to the deposited %s, byte-identical to the %s seal;" % (ver_ant, ver_ant),
              "The DOI below resolves to the deposited %s, byte-identical to the %s seal;" % (versao, versao), 1)
n = re.sub(r'^version: "v\d+"$', 'version: "%s"' % versao, n, count=1, flags=re.M)
n = re.sub(r'^date-released: "[0-9-]+"$', 'date-released: "%s"' % pub, n, count=1, flags=re.M)
n = re.sub(r'^doi: "10\.5281/zenodo\.\d+"$', 'doi: "%s"' % doi, n, count=1, flags=re.M)
novo_dep = ('  - type: doi\n    value: "%s"\n    description: "Zenodo deposit of %s, deposited %s (byte-identical to the seal: um.py sha256 %s…; '
            'the %d deposited files matched by md5: %d to the Nós and %d doors to the custody commit of the repository)"\n'
            % (doi, versao, pub, pin[:16], len(files), ok_nos, ok_esp))
ant_dep = ('  - type: doi\n    value: "%s"\n    description: "the previous Zenodo version: %s, deposited %s (um.py sha256 %s…)"\n'
           % (doi_ant, ver_ant, data_ant, pin_ant))
n = n.replace(m_dep.group(0), novo_dep, 1)
# a anterior entra logo depois do conceito; a que era «the previous» vira «an earlier»
n = n.replace('description: "the previous Zenodo version:', 'description: "an earlier Zenodo version:')
m_con = re.search(r'  - type: doi\n    value: "%s"\n    description: "[^"]*"\n' % re.escape(conceito), n)
assert m_con, "conceito ausente no CITATION.cff — PARAR"
n = n[:m_con.end()] + ant_dep + n[m_con.end():]
n = re.sub(r'(regenerated at every custody \(v\d+ on [0-9-]{10}; the Zenodo deposit holds )v\d+\)', r'\g<1>%s)' % versao, n, count=1)
n = re.sub(r'(the repository head \([\d,]+ bytes; sealed [0-9: -]+\); the Zenodo deposit )10\.5281/zenodo\.\d+ holds v\d+ \([0-9a-f]{16}…\)',
           r'\g<1>%s holds %s (%s…)' % (doi, versao, pin[:16]), n, count=1)
n = n.replace(m_abs.group(0), "(at %s: ladder of\n  %d/%d theorems clean, %d audited declarations" % (versao, p1["n_theorems_clean"], p1["n_theorems_expected"], n_decl), 1)
n = re.sub(r"the\n  previous deposit, v\d+, had [^)]*\)", "the\n  previous deposit, %s, had a ladder of %s and %s audited declarations)" % (ver_ant, lad_ant, decl_ant), n, count=1)
for k in (doi, versao + ", deposited " + pub, "the previous Zenodo version: " + ver_ant, "the Zenodo deposit holds " + versao):
    assert k in n, "faltou no CITATION.cff novo: " + k
assert n.count('doi: "%s"' % doi) == 1 and "Zenodo deposit holds %s" % ver_ant not in n
CFF.with_name(CFF.name + ".bak_" + TS).write_bytes(raw)
t = CFF.with_name(CFF.name + ".tmp"); t.write_bytes(n.encode("utf-8"))
assert t.stat().st_size > 0
os.replace(t, CFF)
print("CITATION.cff: %s depositada (%s, %s); %d/%d arquivos por md5 (%d Nós, %d portas do commit %s); anterior %s (%s) | %d -> %d bytes"
      % (versao, doi, pub, ok_nos + ok_esp, len(files), ok_nos, ok_esp, head[:8], ver_ant, doi_ant, len(raw), CFF.stat().st_size))
