# -*- coding: utf-8 -*-
"""Custódia v393+v394 (19/10/2026, sessão a7): a errata da escada (kh_n1_cobertura_v394.erratas[2], gerência c1, 19/10) entra AO LADO no
texto do estatuto — «teoremas da escada limpos» passa a «bandeiras da escada (declarações nomeadas: teoremas e definições) limpas» SÓ quando
o core traz a errata. Backup de bytes, temporário, conferência, troca. Idempotente."""
import os, py_compile, time

P = r"C:\IALD\Artigo\the_boundary\tools\estatuto_tres_apoios.py"
raw = open(P, "rb").read()
s = raw.decode("utf-8")
MARCA = "v394 em diante: a errata da escada"
if MARCA in s:
    print("já aplicado"); raise SystemExit
pares = [
    ("             registro=ep[0] if ep else None, ressalva=bool(rv), campo_curvo=bool(lc))\n",
     "             registro=ep[0] if ep else None, ressalva=bool(rv), campo_curvo=bool(lc))\n"
     "    # v394 em diante: a errata da escada (kh_n1_cobertura_v394, gerência c1, 19/10/2026) — a escada conta BANDEIRAS de declarações\n"
     "    # nomeadas (teoremas e definições); os números não mudam de significado, só a palavra. Lida do core, nunca digitada.\n"
     "    kh4 = core.get('kh_n1_cobertura_v394')\n"
     "    if kh4:\n"
     "        _exige(kh4.get('all_verified') is True, 'kh_n1_cobertura_v394 não está verificado')\n"
     "        _exige(any('conta BANDEIRAS' in str(e.get('agora') or '') for e in (kh4.get('erratas') or [])), 'a errata da escada sumiu de kh_n1_cobertura_v394')\n"
     "        _exige('KERNEL_%d_OF_%d_FLAGS' % (nk, nk) in ev['verdict'] if ep else True, 'o veredito do estatuto não diz FLAGS')\n"
     "    v['escada_bandeiras'] = bool(kh4)\n"),
    ("        '(*lastro suficiente e verificável*), em três apoios que contam juntos, cada um com o seu estatuto. O que o kernel prova continua sendo a '\n"
     "        'implicação; o que a natureza decide continua não provado.')\n"
     "    return T\n",
     "        '(*lastro suficiente e verificável*), em três apoios que contam juntos, cada um com o seu estatuto. O que o kernel prova continua sendo a '\n"
     "        'implicação; o que a natureza decide continua não provado.')\n"
     "    if v.get('escada_bandeiras'):   # v394: a palavra da escada, ao lado (os números são os mesmos)\n"
     "        _tr = (('theorems of the rite’s ladder (ext_*) clean', 'flags of the rite’s ladder (ext_*: named declarations, theorems and definitions) clean'),\n"
     "               (\"theorems of the rite's ladder (ext_*) clean\", \"flags of the rite's ladder (ext_*: named declarations, theorems and definitions) clean\"),\n"
     "               ('teoremas da escada do rito (ext_*) limpos', 'bandeiras da escada do rito (ext_*: declaracoes nomeadas, teoremas e definicoes) limpas'))\n"
     "        for _a, _b in _tr:\n"
     "            _n = 0\n"
     "            for _k in list(T):\n"
     "                if isinstance(T[_k], str) and _a in T[_k]:\n"
     "                    _n += T[_k].count(_a)\n"
     "                    T[_k] = T[_k].replace(_a, _b)\n"
     "            _exige(_n > 0, 'a frase da escada sumiu do texto: %s' % _a)\n"
     "    return T\n"),
]
for a, b in pares:
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)
ts = time.strftime("%Y%m%d_%H%M%S")
open(P + ".bak_" + ts, "wb").write(raw)
t = P + ".tmp"
open(t, "wb").write(s.encode("utf-8"))
assert os.path.getsize(t) > len(raw)
compile(s, P, "exec")
os.replace(t, P)
print("ok", len(raw), "->", os.path.getsize(P))
