# -*- coding: utf-8 -*-
"""O cartão de estado do site ganha o depósito citável do Zenodo, lido do CITATION.cff do espelho (a fonte de verdade da casa): versão
depositada, DOI da versão e DOI do conceito. Nada digitado. Backup de bytes; py_compile."""
import os, py_compile, time
from pathlib import Path

P = Path(r"C:\IALD\Site\tgl\v3.0_bancada\tools\gerar_cartao_estado.py")
raw = P.read_bytes(); s = raw.decode("utf-8")
if "'zenodo':" in s:
    raise SystemExit("já aplicado")
pares = [
    ("site = PORTA['site'].rstrip('/') + '/'\n",
     "site = PORTA['site'].rstrip('/') + '/'\n"
     "# 25/10/2026: o depósito citável do Zenodo, lido do CITATION.cff do espelho (a fonte de verdade da casa; nada digitado)\n"
     "_cff = open(os.path.join(ESP, 'CITATION.cff'), encoding='utf-8').read()\n"
     "_mz = re.search(r'^doi: \"(10\\.5281/zenodo\\.[0-9]+)\"', _cff, re.M)\n"
     "_mv = re.search(r'Zenodo deposit of (v[0-9]+), deposited ([0-9-]{10})', _cff)\n"
     "_mc = re.search(r'value: \"(10\\.5281/zenodo\\.[0-9]+)\"\\n    description: \"Zenodo concept DOI', _cff)\n"
     "if not (_mz and _mv and _mc):\n"
     "    falha('CITATION.cff sem o depósito do Zenodo (doi, «Zenodo deposit of vN», conceito)')\n"
     "zen = {'versao_depositada': _mv.group(1), 'depositada_em': _mv.group(2), 'doi': 'https://doi.org/' + _mz.group(1),\n"
     "       'conceito': 'https://doi.org/' + _mc.group(1), 'igual_ao_selo': _mv.group(1) == versao}\n"),
    ("    'gate': E['gate'],\n",
     "    'gate': E['gate'],\n    'zenodo': zen,\n"),
    ("    'reproduce: echo 1 | python um.py',\n",
     "    'reproduce: echo 1 | python um.py',\n"
     "    'cite: Zenodo %s (deposited %s) %s; all versions %s' % (zen['versao_depositada'], zen['depositada_em'], zen['doi'], zen['conceito']),\n"),
]
for a, b in pares:
    n = s.count(a)
    assert n == 1, (a[:60], n)
    s = s.replace(a, b)
P.with_name(P.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(raw)
t = P.with_name(P.name + ".tmp"); t.write_bytes(s.encode("utf-8")); py_compile.compile(str(t), doraise=True); os.replace(t, P)
print("gerar_cartao_estado.py: + depósito do Zenodo | %d -> %d" % (len(raw), P.stat().st_size))
