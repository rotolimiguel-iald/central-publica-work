"""Troca o bloco '# 4) fila' do entrega_f03_v407.py: o deposito passa a ser feito SEMPRE pela ferramenta memoria.py depositar (regra da c1, 04/11), nunca a mao."""
from pathlib import Path

p = Path(r"C:\IALD\Central de Patentes\work\scientific_memory_sync_20261104_v407\entrega_f03_v407.py")
s = p.read_text(encoding="utf-8")
ini = s.index("# 4) fila")
fim = s.index("# 5) 004_RESULTADO")
novo = r'''# 4) fila: SEMPRE pela ferramenta memoria.py depositar (regra da c1, 04/11), nunca a mao
texto = (f"[REAL] 04/11/2026 08:02: a memoria cientifica sincronizada da fila (F0.3) foi ATIVADA para a v407 pela API existente com CAS, por escrita unica autorizada pelo operador no chat "
         f"(Autorizo a escrita; Vale para a v407) e chamada pela gerencia c1 depois do selo completo do Nos. Release {EPOCH}: 13 documentos, {prep['chunks']} trechos, manifest {prep['manifest']['sha256'][:16]}; "
         f"ACTIVE.json v404 -> v407; check em processo novo = CURRENT; revisao independente PODE ATIVAR. Em Chatgpt so' mudaram o release novo (17 arquivos), o ACTIVE.json e o backup do ponteiro; "
         f"a autorizacao se esgotou com a ativacao (a v408 pede outra). A unidade nao foi movida para AUDITADA/FECHADA (ato da gerencia). Mapa: memoria.cientifica_sync.v406_gate_chatgpt (RESULTADO).")
tf = W / "DEPOSITO_F03_v407.md"
with tf.open("xb") as f:
    f.write(texto.encode("utf-8"))
FILA_DIR = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fila")
r = subprocess.run([PY, "-X", "utf8", "memoria.py", "depositar", "--quem", QUEM, "--tipo", "project", "--estatuto", "REAL", "--alvo", "missao-ultima-flag-um-py.md",
                    "--fonte", str(dp), "--fonte", str(parecer), "--slug", "f03-v407-ativada-04nov", "--texto-arquivo", str(tf)], cwd=str(FILA_DIR), capture_output=True)
print("fila rc", r.returncode, " ".join(r.stdout.decode("utf-8", "replace").split())[:300], r.stderr.decode("utf-8", "replace")[:400])

'''
s = s[:ini] + novo + s[fim:]
p.write_text(s, encoding="utf-8")
print("script atualizado:", p.stat().st_size, "bytes")
