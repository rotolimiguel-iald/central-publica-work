# -*- coding: utf-8 -*-
"""editar_registro_mapa_d19c.py -- DELTA 19/10 (rodada d19c): atualiza gerar_registro_mapa.py para o estado FINAL (a proposta de pos_rito foi aplicada, a errata da palavra «teoremas» entrou, o harness dos textos passa).
Backup de BYTES antes (.bak_<STAMP>_c1d19c), ancoras unicas, temporario -> conferir -> substituir, idempotente."""
import hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ALVO = os.path.join(HERE, "gerar_registro_mapa.py")
BS = chr(92)
raw = open(ALVO, "rb").read(); s = raw.decode("utf-8")
if "HARNESS_TEXTOS_ENSAIO_DEPOIS_aplicado" in s:
    print("JA APLICADO (idempotente): gerar_registro_mapa.py"); sys.exit(0)
SUBS = [
    # (1) o fim do campo «resultado»: a soma que nao fechava agora fecha (proposta aplicada)
    ("A soma que pos_rito" + BS * 2 + "textos_v394.py::_d espera NÃO fecha com a política nova (n_out_flags=%d); a proposta (n_bandeiras_por_grupo) passa.",
     "A soma que pos_rito" + BS * 2 + "textos_v394.py::_d esperava NÃO fechava com a política nova (n_out_flags=%d); a proposta (n_bandeiras_por_grupo) foi aplicada (sha16 %s) e o harness dos textos (os módulos reais contra um Nós emulado do ensaio) passa: %d + %d + %d + %d = %d."),
    ('SOMA["formula_original"]["n_out_flags"]),\n    "veredito"', 'SOMA["formula_original"]["n_out_flags"], HD["textos_sha16"], bg["tempo"], bg["quadratica"], bg["rede"], bg["outros"], sum(bg.values())),\n    "veredito"'),
    ('S = CM["sha16"]; SOMA = J(HERE, "SOMA_TEXTOS_POS_RITO.json")', 'S = CM["sha16"]; SOMA = J(HERE, "SOMA_TEXTOS_POS_RITO.json"); HD = J(HERE, "HARNESS_TEXTOS_ENSAIO_DEPOIS_aplicado.json"); bg = ESP["n_bandeiras_por_grupo"]'),
    # (2) defeito
    ("os textos do pós-rito precisam ler as bandeiras por grupo; a frase «teoremas limpos» (artigo e stdout) segue por decisão pendente; B(n)",
     "a errata da palavra «teoremas» (a escada conta bandeiras: declarações nomeadas, teoremas e definições) entrou no artigo e no texto do kernel, e o rótulo «teoremas limpos» fica como registro de máquina; o harness dos textos e o caminho positivo do conferidor são EMULAÇÃO (só o rito real os exercita); B(n)"),
    # (3) proximo passo
    ("a gerência decide a proposta de pos_rito (n_bandeiras_por_grupo) e a frase «teoremas limpos»; instalar", "instalar"),
    # (4) artefatos
    ('os.path.join(HERE, "SOMA_TEXTOS_POS_RITO.json"),', 'os.path.join(HERE, "SOMA_TEXTOS_POS_RITO.json"), os.path.join(HERE, "HARNESS_TEXTOS_ENSAIO_DEPOIS_aplicado.json"), os.path.join(HERE, "HARNESS_TEXTOS_ENSAIO_ANTES_original.json"), os.path.join(HERE, "conferencia_POSITIVO_FALSO_NOS.json"), os.path.join(V, "pos_rito", "textos_v394.py"),'),
    # (5) onde
    ("pedra em delta_19out" + BS * 2 + "TheBinaryReadingAtTheFixedPoint.lean", "pedra em delta_19out" + BS * 2 + "TheBinaryReadingAtTheFixedPoint.lean; textos em pos_rito" + BS * 2 + "textos_v394.py (proposta aplicada)"),
]
for a, b in SUBS:
    assert s.count(a) == 1, ("ancora nao unica", a[:80], s.count(a))
    s = s.replace(a, b)
stamp = time.strftime("%Y%m%d_%H%M%S"); bak = ALVO + ".bak_%s_c1d19c" % stamp
assert not os.path.exists(bak)
open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
tmp = ALVO + ".tmp_c1d19c"; open(tmp, "wb").write(s.encode("utf-8")); assert os.path.getsize(tmp) > 0
os.replace(tmp, ALVO); compile(open(ALVO, encoding="utf-8").read(), ALVO, "exec")
print("OK: %s %d B -> %d B (sha16 %s -> %s); backup %s" % (os.path.basename(ALVO), len(raw), os.path.getsize(ALVO), hashlib.sha256(raw).hexdigest()[:16], hashlib.sha256(open(ALVO, "rb").read()).hexdigest()[:16], os.path.basename(bak)))
