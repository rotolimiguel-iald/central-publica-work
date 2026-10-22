# -*- coding: utf-8 -*-
"""editar_tabela_d19c.py -- DELTA 19/10 (rodada d19c): ajusta tabela_arquivos_alterados.py para a rodada final: (1) o regex dos backups aceita o sufixo _c1d19c; (2) olha tambem pos_rito\\ (so' textos_v394.py tem backup meu);
(3) arquivos CRIADOS pelo delta (delta19_v394.py, o candidato d19) entram em NOVOS e nao em «alterados» (o «antes» deles e' um estado intermediario do proprio delta); (4) a nota final diz a verdade sobre pos_rito.
Backup de BYTES antes (.bak_<STAMP>_c1d19c), temporario -> conferir -> substituir, idempotente, ancoras unicas."""
import hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ALVO = os.path.join(HERE, "tabela_arquivos_alterados.py")
raw = open(ALVO, "rb").read(); s = raw.decode("utf-8")
SUBS = [
    ('(?:blk|d19|d19b)?$")', '(?:blk|d19|d19b|d19c)?$")'),
    ('pastas = [(V, ""), (os.path.join(V, "vinculo"), "vinculo/"), (os.path.join(V, "kernel"), "kernel/")]',
     'pastas = [(V, ""), (os.path.join(V, "vinculo"), "vinculo/"), (os.path.join(V, "kernel"), "kernel/"), (os.path.join(V, "pos_rito"), "pos_rito/")]\n'
     'CRIADOS_PELO_DELTA = ("delta19_v394.py", "um_v394_candidato_d19.py")   # nascem no delta: o backup deles e\' um estado INTERMEDIARIO do proprio delta, nao um «antes»'),
    ('        if not os.path.isfile(atual):\n            continue\n',
     '        if not os.path.isfile(atual) or (pref + base) in CRIADOS_PELO_DELTA:\n            continue\n'),
    ('os.path.isfile(p) and n not in vistos and not RXB.match(n) and (os.path.getmtime(p) >= corte_t or n in COPIAS_DO_EXAME)',
     'os.path.isfile(p) and n not in vistos and not RXB.match(n) and (os.path.getmtime(p) >= corte_t or n in COPIAS_DO_EXAME or n in CRIADOS_PELO_DELTA)'),
    ('`pos_rito` aparece porque OUTRO agente escreveu nela; eu NAO escrevi em `pos_rito` (a proposta para ela esta em `delta_19out`).',
     '`pos_rito` aparece porque OUTRO agente escreveu nela (antes das 13:00) e porque, na rodada final, a gerencia AUTORIZOU a aplicacao da proposta em `pos_rito\\\\textos_v394.py` (a unica escrita minha ali, com backup de bytes `.bak_<STAMP>_c1d19c`).'),
]
if "d19c" in s and "CRIADOS_PELO_DELTA" in s:
    print("JA APLICADO (idempotente): tabela_arquivos_alterados.py"); sys.exit(0)
for a, b in SUBS:
    assert s.count(a) == 1, ("ancora nao unica", a[:70], s.count(a))
    s = s.replace(a, b)
stamp = time.strftime("%Y%m%d_%H%M%S"); bak = ALVO + ".bak_%s_c1d19c" % stamp
assert not os.path.exists(bak)
open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
tmp = ALVO + ".tmp_c1d19c"; open(tmp, "wb").write(s.encode("utf-8")); assert os.path.getsize(tmp) > 0
os.replace(tmp, ALVO)
compile(open(ALVO, encoding="utf-8").read(), ALVO, "exec")
print("OK: %s %d B -> %d B (sha16 %s -> %s); backup %s" % (os.path.basename(ALVO), len(raw), os.path.getsize(ALVO), hashlib.sha256(raw).hexdigest()[:16], hashlib.sha256(open(ALVO, "rb").read()).hexdigest()[:16], os.path.basename(bak)))
