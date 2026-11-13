# -*- coding: utf-8 -*-
"""D195 (13/11/2026, claude-site-custodia), parte espelho: MOVE o gancho da seção das sete ressalvas no tools/gerar_estado_atual.py do
espelho, de antes de «What is NOT proved» (âncora de 12/11) para antes de «## The seal» (âncora nova), com os MESMOS bytes do gancho.
O gancho foi instalado uma vez pela E04 (patch_bytes, marca MARCA_HOOK); a G1 não o reinstala (idempotência pela marca), por isso a
migração é este script, uma vez. Bytes: o arquivo fica do mesmo tamanho (só o lugar muda). CRLF preservado. Backup; temporário; compilação.
Uso: python -X utf8 <este> [ARQUIVO_gerar_estado_atual.py] [PASTA_QUE_CONTEM_custodia_g1]"""
import os, sys, time
from pathlib import Path

ARQ = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(r"C:\IALD\Artigo\the_boundary\tools\gerar_estado_atual.py")
sys.path.insert(0, sys.argv[2] if len(sys.argv) > 2 else r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import h0dn  # noqa: E402

STAMP = time.strftime("%Y%m%d_%H%M%S")
b = ARQ.read_bytes()
crlf = b"\r\n" in b
assert (b.count(b"\r\n") == b.count(b"\n")) if crlf else True, "fim de linha misto - PARAR"
eol = (lambda s: s.replace("\n", "\r\n")) if crlf else (lambda s: s)
anc_novo, novo_mais_anc = h0dn._hook_secao()
gancho = novo_mais_anc[:-len(anc_novo)]
anc_velho = h0dn._ANC_SECAO_12NOV
assert anc_novo != anc_velho and h0dn.MARCA_HOOK in gancho
s = b.decode("utf-8")
G, AV, AN = eol(gancho), eol(anc_velho), eol(anc_novo)
assert s.count(G + AV) == 1, "o gancho não está uma vez antes de «What is NOT proved» - PARAR"
assert s.count(G) == 1, "o gancho aparece mais de uma vez - PARAR"
assert s.count(AN) == 1, "a âncora nova («## The seal») não está uma vez - PARAR"
assert s.index(AN) < s.index(G), "a âncora nova não vem antes do gancho - PARAR"
s2 = s.replace(G + AV, AV).replace(AN, G + AN)
assert s2.count(G + AN) == 1 and s2.count(G) == 1 and s2.count(AV) == 1
n2 = s2.encode("utf-8")
assert len(n2) == len(b) and n2 != b
compile(s2, str(ARQ), "exec")
bak = ARQ.with_name(ARQ.name + ".bak_%s_d195_gancho" % STAMP)
bak.write_bytes(b)
assert bak.read_bytes() == b
t = ARQ.with_name(ARQ.name + ".tmp_d195")
t.write_bytes(n2)
assert t.stat().st_size == len(n2)
os.replace(t, ARQ)
print("ok: %s movido (%d B, mesmo tamanho); gancho de %d B agora antes de «## The seal» | backup %s" % (ARQ.name, len(n2), len(G.encode("utf-8")), bak.name))
