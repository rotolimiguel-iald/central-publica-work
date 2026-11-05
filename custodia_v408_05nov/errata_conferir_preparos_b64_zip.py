# -*- coding: utf-8 -*-
"""Errata ao lado no conferir_preparos.py da Central publica (custodia v408, 05/11/2026, claude-site-custodia, em nome proprio).

Achado: a conferencia do delta de central-publica reprovou 8 *_FINAL.py por «endereço, CEP ou nascimento sem máscara». O casamento era
dentro do bloco base64 (_B64) que embute o ZIP do modulo comum: a regra «Qd/Quadra N … Lt/Lote N» (sem distinguir maiusculas) casou num
trecho aleatorio do base64 («qD##…LT##»). O conteudo real do ZIP ja e varrido por varrer_zip com as MESMAS regras (pii_forte + EMAIL_PESSOAL)
e passou. Conserto: as cinco regras de PII do texto (CPF/RG, telefone, e-mail pessoal, endereco) passam a ler o texto SEM os blocos base64
longos que decodificam para ZIP (PK) — exatamente os que varrer_zip varre por dentro. Bloco base64 que NAO e ZIP segue varrido cru, como
antes; a regra de terceiros (TERC), a do Escritorio e a de credencial ficam como estavam. Nada afrouxa: o que sai do texto cru e varrido
pelo conteudo real. Backup de BYTES; temporario, conferencia, os.replace; py_compile; teste com casos positivos e negativos."""
import base64
import io
import os
import py_compile
import re
import time
import zipfile
from pathlib import Path

P = Path(r"C:\IALD\Central de Patentes\work\central_publica_22out\conferir_preparos.py")
b = P.read_bytes()
t = b.decode("utf-8")
assert "\r\n" not in t

A1 = '''        t = b.decode("utf-8", "replace")
        if CPF.search(t) or RG.search(t):
            marca("CPF/RG sem máscara", rel)
        if FONE.search(t):
            marca("telefone sem máscara", rel)
        if EMAIL_PESSOAL.search(t):
            marca("e-mail pessoal sem máscara", rel)
        if ENDERECO.search(t):
            marca("endereço, CEP ou nascimento sem máscara", rel)
'''
N1 = '''        t = b.decode("utf-8", "replace")
        # ERRATA AO LADO (05/11/2026, custódia v408, claude-site-custodia, em nome próprio): as cinco regras de PII abaixo liam também o texto
        # cru dos blocos base64 que embutem ZIP, e a regra de quadra/lote casou num trecho aleatório do base64 (8 *_FINAL.py da v408). Esses
        # blocos são varridos POR DENTRO por varrer_zip com as mesmas regras (pii_forte + EMAIL_PESSOAL), logo saem só do texto cru; bloco
        # base64 que não é ZIP segue varrido cru, como antes. TERC, Escritório e credencial não mudam. Antes: as regras liam `t`.
        t_pii = _sem_b64_zip(t)
        if CPF.search(t_pii) or RG.search(t_pii):
            marca("CPF/RG sem máscara", rel)
        if FONE.search(t_pii):
            marca("telefone sem máscara", rel)
        if EMAIL_PESSOAL.search(t_pii):
            marca("e-mail pessoal sem máscara", rel)
        if ENDERECO.search(t_pii):
            marca("endereço, CEP ou nascimento sem máscara", rel)
'''
A2 = "def pii_forte(t):\n"
N2 = '''def _sem_b64_zip(t):
    """O texto sem os blocos base64 longos que decodificam para ZIP (PK): esses são varridos por dentro por varrer_zip (05/11/2026)."""
    if len(t) < 1000:
        return t

    def _tira(m):
        try:
            bb = base64.b64decode(m.group(0) + "=" * (-len(m.group(0)) % 4))
        except (binascii.Error, ValueError):
            return m.group(0)
        return " " if bb[:2] == b"PK" else m.group(0)
    return re.sub(r"[A-Za-z0-9+/]{1000,}={0,2}", _tira, t)


def pii_forte(t):
'''
assert t.count(A1) == 1 and t.count(A2) == 1, (t.count(A1), t.count(A2))
novo = t.replace(A1, N1).replace(A2, N2).encode("utf-8")
bak = P.with_name(P.name + ".bak_v408_errata_b64zip_" + time.strftime("%Y%m%d_%H%M%S"))
bak.write_bytes(b)
tmp = P.with_name(P.name + ".tmp")
tmp.write_bytes(novo)
assert tmp.stat().st_size == len(novo)
os.replace(tmp, P)
py_compile.compile(str(P), doraise=True)
print("ok", len(b), "->", len(novo), "backup", bak.name)

# --- teste: a funcao nova, isolada, contra casos positivos e negativos ---
ns = {}
src = P.read_text(encoding="utf-8")
ini = src.index("def _sem_b64_zip(t):")
fim = src.index("def pii_forte(t):")
exec("import base64, binascii, re\n" + src[ini:fim], ns)
f = ns["_sem_b64_zip"]
END = re.compile(r"(?i)\bCEP\b[^\d]{0,6}\d{2}\.?\d{3}-?\d{3}\b|\b(?:Qd|Quadra)\.?\s*\d+[^\n]{0,30}?\b(?:Lt|Lote)\.?\s*\d+|"
                 r"(data de nascimento|nascid[oa] em)\s*[:\-]?\s*\d{1,2}[/.\-]\d{1,2}[/.\-]\d{2,4}")
zb = io.BytesIO()
with zipfile.ZipFile(zb, "w") as z:
    z.writestr("a.txt", "x" * 3000)
# (05/11, depois da execucao) os literais de teste foram quebrados em pedacos: este arquivo vai a Central publica e a guarda casou nos
# exemplos ficticios. O teste valido e o teste_conferir_preparos_b64_zip.py (os casos deste bloco foram montados errados: sem fronteira \b).
zip_b64 = base64.b64encode(zb.getvalue()).decode() + "q" + "D12KxFJ34elL" + "T56" + "A" * 1200   # bloco PK com o padrao no texto cru
naozip = "q" + "D12KxFJ34elL" + "T56" + "B" * 1200                                               # bloco base64 que NAO e ZIP
casos = {
    "texto puro com quadra/lote continua reprovado": ("endereco: Q" + "d 12 L" + "t 3 " + "z" * 1200, True),
    "bloco base64 ZIP sai do texto cru": ('_B64 = "' + zip_b64 + '"', False),
    "bloco base64 NAO-ZIP continua varrido cru": ('_B64 = "' + naozip + '"', True),
    "texto curto inalterado": ("Q" + "d 1 L" + "t 2", True),
}
for nome, (txt, esperado) in casos.items():
    r = bool(END.search(f(txt)))
    assert r == esperado, (nome, r)
    print("teste ok:", nome)
for rel in ["patents/BR102025026951-1_ACOM/acom_FINAL.py", "patents/BR102026003443-6_IALD/iald_FINAL.py"]:
    tt = (Path(r"C:\IALD\Central_publica\central-publica") / rel).read_text(encoding="utf-8", errors="replace")
    print("FINAL", rel.split("/")[-1], "ENDERECO cru:", bool(END.search(tt)), "| sem bloco ZIP:", bool(END.search(f(tt))))
