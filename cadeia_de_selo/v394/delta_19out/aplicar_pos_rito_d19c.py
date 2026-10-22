# -*- coding: utf-8 -*-
"""aplicar_pos_rito_d19c.py -- DELTA 19/10 (rodada d19c, gerencia c1): aplica em pos_rito\\textos_v394.py (1) a proposta pos_rito_PROPOSTA_delta19.diff, aprovada pela gerencia, e (2) a frase de ERRATA AO LADO sobre a palavra «teoremas»
no texto do kernel (a funcao _num). Backup de BYTES antes (.bak_<STAMP>_c1d19c, na mesma pasta), temporario -> conferir tamanho -> substituir, idempotente.
(1) so' vale se o arquivo atual e' EXATAMENTE o ORIGINAL da proposta (sha256 igual); o resultado do passo (1) tem de ser identico, byte a byte, ao arquivo PROPOSTA que a gerencia revisou.
(2) a frase vem de delta19_v394.ERRATA_TEOREMAS_PT (uma fonte so'); sem numero digitado.
uso: python -I -B -X utf8 aplicar_pos_rito_d19c.py          (aplica)        |   ... --seco   (so' mostra o que faria)"""
import hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(HERE); sys.path.insert(0, V)
import delta19_v394 as DL  # noqa: E402
ALVO = os.path.join(V, "pos_rito", "textos_v394.py")
PROP_DIR = os.path.join(HERE, "pos_rito_proposta")
ORIG = open(os.path.join(PROP_DIR, "textos_v394.py.ORIGINAL"), "rb").read()
PROP = open(os.path.join(PROP_DIR, "textos_v394.py.PROPOSTA"), "rb").read()
sha = lambda b: hashlib.sha256(b).hexdigest()
raw = open(ALVO, "rb").read()
SECO = "--seco" in sys.argv

# (2) a errata: UMA frase, dentro do texto do kernel (kern), logo depois do parentese da cobertura
OLD_KERN = ('"(%s declarações no `axiom_report`, %d fora do trio, %d nomes não lidos; a proveniência de cada declaração emitida pelo compilador cobre as mesmas %d)") % (\n').encode("utf-8")
NEW_KERN = ('"(%s declarações no `axiom_report`, %d fora do trio, %d nomes não lidos; a proveniência de cada declaração emitida pelo compilador cobre as mesmas %d); "\n'
            '            "errata ao lado (em nome próprio da gerência c1, 19/10/2026): ' + DL.ERRATA_TEOREMAS_PT + '") % (\n').encode("utf-8")
assert b"%" not in DL.ERRATA_TEOREMAS_PT.encode("utf-8"), "a frase de errata nao pode ter % (e' formato)"
assert OLD_KERN in PROP and PROP.count(OLD_KERN) == 1 and OLD_KERN in ORIG, "o ancora do texto do kernel nao e' unico"
FINAL = PROP.replace(OLD_KERN, NEW_KERN, 1)
assert len(FINAL) > len(PROP) > len(ORIG)

if raw == FINAL:
    print("JA APLICADO (idempotente): pos_rito\\textos_v394.py sha16 %s" % sha(raw)[:16]); sys.exit(0)
if raw == ORIG:
    estado = "ORIGINAL (419e...): aplica a proposta da gerencia + a errata"
elif raw == PROP:
    estado = "PROPOSTA ja aplicada: aplica so' a errata"
else:
    print("RECUSO: pos_rito\\textos_v394.py (sha16 %s) nao e' nem o ORIGINAL (%s) nem a PROPOSTA (%s) nem o FINAL (%s)" % (sha(raw)[:16], sha(ORIG)[:16], sha(PROP)[:16], sha(FINAL)[:16])); sys.exit(3)
print("estado de partida:", estado)
print("sha16 ORIGINAL %s (%d B) | PROPOSTA %s (%d B) | FINAL %s (%d B)" % (sha(ORIG)[:16], len(ORIG), sha(PROP)[:16], len(PROP), sha(FINAL)[:16], len(FINAL)))
if SECO:
    print("--seco: nada gravado"); sys.exit(0)
stamp = time.strftime("%Y%m%d_%H%M%S")
bak = ALVO + ".bak_%s_c1d19c" % stamp
assert not os.path.exists(bak)
open(bak, "wb").write(raw)
assert open(bak, "rb").read() == raw, "o backup de bytes nao confere"
tmp = ALVO + ".tmp_c1d19c"
open(tmp, "wb").write(FINAL)
assert os.path.getsize(tmp) == len(FINAL) > len(raw) - 1, "o temporario nao tem o tamanho esperado"
os.replace(tmp, ALVO)
nov = open(ALVO, "rb").read()
assert nov == FINAL and len(nov) > len(raw)
print("APLICADO: pos_rito\\textos_v394.py %d B -> %d B; sha16 %s -> %s; backup %s (sha16 %s)" % (len(raw), len(nov), sha(raw)[:16], sha(nov)[:16], os.path.basename(bak), sha(open(bak, "rb").read())[:16]))
