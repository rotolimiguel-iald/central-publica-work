# -*- coding: utf-8 -*-
"""Testes da guarda pública (22/10/2026), antes de reconstruir os preparos: positivos e negativos sintéticos, os 3 falsos positivos
medidos, os 16 FINAL.py (a carga embutida decodificada) e os compactados do INPI/ePCT (devem barrar)."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import guarda_publica as GP  # noqa: E402

SRC = Path(r"C:\IALD\Central de Patentes")
falhas = []


def conf(nome, cond):
    print(("ok   " if cond else "FALHA"), nome)
    if not cond:
        falhas.append(nome)


# sintéticos (montados em tempo de execução para que este arquivo não contenha um padrão de credencial literal)
chave = "api_" + "key = '" + "q7Z" * 6 + "'"
conf("credencial atribuída sintética barra", GP.avaliar_texto(chave)[0] > 0)
conf("senha errada de teste não barra", GP.avaliar_texto("x(password=\"senha-errada-999\")")[0] == 0)
conf("canário sintético não barra", GP.avaliar_texto("password = 'FAKE_SYNTHETIC_CANARY_NOT_A_SECRET'")[0] == 0)
tok = "gh" + "p_" + "A1b2C3d4" * 5
conf("token do GitHub sintético barra", GP.avaliar_texto("t = '%s'" % tok)[0] > 0)
import base64, io, zipfile
buf = io.BytesIO()
with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_STORED) as z:
    z.writestr("a.txt", "CPF: [dado pessoal removido] e " + tok)
    z.writestr("enchimento.bin", bytes(range(256)) * 8)
blob = base64.b64encode(buf.getvalue()).decode()
n, k = GP.avaliar_texto("_B64 = '" + blob + "'")
conf("carga base64 com zip: credencial e CPF achados dentro", n > 0 and "cpf_rotulado" in k)
conf("arquivo de credencial pelo nome", GP.arquivo_de_credencial(".env") and GP.arquivo_de_credencial("deepseek_authorization.json"))
conf("nome comum não é credencial", not GP.arquivo_de_credencial("um_absoluto.json"))
# os três falsos positivos medidos
for rel in ("patents/BR102025026951-1_ACOM/dispositivo/acom_archive.py", "patents/BR102026003428-2_ACOM_MIRROR/acom_mirror_FINAL.py",
            "patents/BR102026004849-6_CELULA_REVERSAO/celula_reversao_FINAL.py"):
    n, k = GP.avaliar_texto((SRC / rel).read_bytes().decode("utf-8", "replace"))
    conf("falso positivo liberado: %s (cred=%d pii=%s)" % (rel.rsplit("/", 1)[-1], n, sorted(k)), n == 0 and not k)
# os 16 FINAL.py: a carga embutida
for p in sorted(SRC.glob("patents/*/*_FINAL.py")):
    n, k = GP.avaliar_texto(p.read_bytes().decode("utf-8", "replace"))
    conf("FINAL limpo: %s (cred=%d pii=%s)" % (p.name, n, sorted(k)), n == 0 and not k)
# os compactados do INPI/ePCT devem barrar
for rel in ("Patentes/Acervo de Patentes/Acervos de Patentes INPI.zip", "vault/originals_copy/zips/Acervos de Patentes INPI.zip",
            "vault/originals_copy/zips/Depósito 1 no epct.zip"):
    p = SRC / rel
    if p.is_file():
        n, k = GP.avaliar_bytes(p.name, p.read_bytes())
        conf("compactado barrado: %s (pii=%s)" % (p.name, sorted(k)), bool(k & set(GP.SENS)) or "documento_de_protocolo_no_compactado" in k)
for p in sorted(SRC.glob("Patentes/**/*.docx")):
    n, k = GP.avaliar_bytes(p.name, p.read_bytes())
    print("     docx:", p.name, "cred=%d" % n, sorted(k))
import time
bomba = Path(r"C:\IALD\Central de Patentes\work\acom_signal_transport_20261021\client_server_stage\fixtures\bad_bomb.json")
if bomba.is_file():
    t0 = time.perf_counter()
    n, k = GP.avaliar_texto(bomba.read_bytes().decode("utf-8", "replace"))
    dt = time.perf_counter() - t0
    conf("fixture bad_bomb.json (2 MB de «a» após zlib) atravessa em tempo linear (%.2f s, %s)" % (dt, sorted(k)), dt < 30)
import zlib
grande = zlib.compress(b"\0" * (100 * 1024 * 1024), 9)
t0 = time.perf_counter()
n, k = GP.avaliar_bytes("bomba.bin", grande)
conf("bomba de verdade (100 MB) recusada no teto, sem expandir (%.2f s, %s)" % (time.perf_counter() - t0, sorted(k)), "carga_grande_demais" in k)
del grande
from mascara_pii import mascarar
t0 = time.perf_counter()
mascarar("x " + "a" * 2_000_000)
conf("máscara de e-mail linear num trecho de 2 MB sem @ (%.2f s)" % (time.perf_counter() - t0), time.perf_counter() - t0 < 5)
print("FALHAS:", falhas if falhas else "nenhuma")
