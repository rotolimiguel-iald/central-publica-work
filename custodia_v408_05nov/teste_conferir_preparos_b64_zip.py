# -*- coding: utf-8 -*-
"""Teste (so leitura) da errata de 05/11 no conferir_preparos.py: _sem_b64_zip contra casos positivos e negativos.
Cada caso confere ANTES que o padrao casa no texto cru (nenhum teste passa vazio)."""
import base64
import io
import re
import zipfile
from pathlib import Path

P = Path(r"C:\IALD\Central de Patentes\work\central_publica_22out\conferir_preparos.py")
src = P.read_text(encoding="utf-8")
ns = {}
exec("import base64, binascii, re\n" + src[src.index("def _sem_b64_zip(t):"):src.index("def pii_forte(t):")], ns)
f = ns["_sem_b64_zip"]
m = re.search(r'^ENDERECO = re\.compile\((r".*?")\s*\n\s*(r".*?")\)', src, re.M)
END = re.compile(eval(m.group(1)) + eval(m.group(2)))   # a regra lida do proprio arquivo
PADRAO = "q" + "D12KxFJ34el+L" + "T56"   # literais em pedacos: o arquivo vai a Central publica e a guarda nao deve casar no proprio teste
def _zip(comentario=b""):
    zb = io.BytesIO()
    with zipfile.ZipFile(zb, "w") as z:
        z.writestr("a.txt", "x" * 3000)
        z.comment = comentario
    return zb.getvalue()
zb = _zip()
zb = _zip(b"c" * ((3 - len(zb) % 3) % 3))                    # sem '=' de preenchimento: o bloco base64 nao se corta
zip_b64 = base64.b64encode(zb).decode()
assert "=" not in zip_b64 and len(zip_b64) > 100
zip_b64 = zip_b64 + "/" + PADRAO.replace("+", "/") + "A" * 1200   # '/' e base64 e cria a fronteira \b, como no FINAL real («…V/qD##»)
naozip = "QUJD/" + PADRAO.replace("+", "/") + "B" * 1200
casos = {
    "texto puro com quadra/lote continua reprovado": ("endereco: Q" + "d 12 L" + "t 3 " + "z" * 1200, True),
    "bloco base64 ZIP sai do texto cru": ('_B64 = "' + zip_b64 + '"', False),
    "bloco base64 NAO-ZIP continua varrido cru": ('_B64 = "' + naozip + '"', True),
    "texto curto inalterado": ("Q" + "d 1 L" + "t 2", True),
    "CEP em texto continua reprovado mesmo ao lado de bloco ZIP": ("C" + "EP 74" + "000-000 " + '_B64 = "' + zip_b64 + '"', True),
}
for nome, (txt, esperado) in casos.items():
    assert END.search(txt), ("o caso nao casa nem no texto cru (teste vazio)", nome)
    r = bool(END.search(f(txt)))
    assert r == esperado, (nome, r)
    print("teste ok:", nome)
base = Path(r"C:\IALD\Central_publica\central-publica")
for rel in ["patents/BR102025026951-1_ACOM/acom_FINAL.py", "patents/BR102026003428-2_ACOM_MIRROR/acom_mirror_FINAL.py",
            "patents/BR102026003443-6_IALD/iald_FINAL.py", "patents/BR102026003450-9_SUPERCONDUTOR/supercondutor_FINAL.py",
            "patents/BR102026003453-3_PSI_NET/psi_net_FINAL.py", "patents/BR102026003456-8_FUSAO_FRIO/fusao_frio_FINAL.py",
            "patents/BR102026005477-1_APRENDIZADO_CONTINUO/aprendizado_continuo_FINAL.py",
            "patents/BR102026006129-8_KERNEL_ONTOLOGICO/kernel_ontologico_FINAL.py"]:
    tt = (base / rel).read_text(encoding="utf-8", errors="replace")
    print("FINAL", rel.split("/")[-1], "cru:", bool(END.search(tt)), "| sem bloco ZIP:", bool(END.search(f(tt))))
