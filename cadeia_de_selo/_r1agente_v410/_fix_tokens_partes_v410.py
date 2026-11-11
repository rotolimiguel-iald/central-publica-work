# -*- coding: utf-8 -*-
"""_fix_tokens_partes_v410.py -- achado do PRE-VOO (F53c): o contrato do H0DN carregava os tokens proibidos e a aritmetica do agregado letra por letra (a guarda os pegaria no proprio contrato, no um.py): passam a PARTES
(montadas em runtime, como TOKENS_PROIBIDOS_V410); a F53c global fica so' com os dois tokens do veredito (o DETEC+TED so' no texto do H0DN, c8, e no trecho com H0DN, F53b: o um.py tem vereditos legados com essa palavra).
Backup de bytes; trocas exatas; ast.parse."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def troca(nome, trocas):
    P = os.path.join(HERE, nome); b0 = open(P, "rb").read(); assert b0.count(b"\r\n") == 0
    bk = P + ".bak_" + TS + "_tokens"; open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
    t = b0.decode("utf-8")
    for v, n, k in trocas:
        c = t.count(v); assert c == k, (nome, c, v[:110]); t = t.replace(v, n)
    nb = t.encode("utf-8"); ast.parse(nb); tmp = P + ".tmp_" + TS; open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb); os.replace(tmp, P)
    print(nome, len(b0), "->", len(nb), hashlib.sha256(nb).hexdigest()[:16], "| trocas", len(trocas))


troca("registros_h0dn_v410.py", [
    ('"tokens_proibidos": list(DL.TOKENS_PROIBIDOS_H0DN), "agregado_publico_nao_entra": list(DL.H0DN_AGREGADO_NAO_ENTRA),',
     '"tokens_proibidos_partes": [[t_[:-4], t_[-4:]] for t_ in DL.TOKENS_PROIBIDOS_H0DN], "agregado_publico_nao_entra_partes": [[a_[:2], a_[2:]] for a_ in DL.H0DN_AGREGADO_NAO_ENTRA],   # (em PARTES: o um.py nunca traz o token nem o numero inteiros; o runtime os monta)', 1),
])
troca("runtime_h0dn_v410.py", [
    ('    Phi_ = lambda x_: 0.5 * _m410.erfc(-float(x_) / _m410.sqrt(2.0))\n    tol_ = c_["tolerancias"]\n',
     '    Phi_ = lambda x_: 0.5 * _m410.erfc(-float(x_) / _m410.sqrt(2.0))\n    tol_ = c_["tolerancias"]\n'
     '    toks_ = ["".join(p_) for p_ in c_["tokens_proibidos_partes"]]; agreg_ = ["".join(p_) for p_ in c_["agregado_publico_nao_entra_partes"]]   # (montados aqui: o contrato os traz em partes)\n', 1),
    ('and "NOT_FALSIFIED" not in cab_ and not any(tk_ in cab_ for tk_ in c_["tokens_proibidos"])', 'and "NOT_FALSIFIED" not in cab_ and not any(tk_ in cab_ for tk_ in toks_)', 1),
    ('    c8_ok_ = (not any(tk_ in txt_json_ for tk_ in c_["tokens_proibidos"]) and not any(a_ in txt_json_ for a_ in c_["agregado_publico_nao_entra"]) and not [f_ for f_ in frases_ if f_[0].startswith(("F53", "F54", "F55"))]\n'
     '              and not any(tk_ in c_["veredito_ok"] for tk_ in c_["tokens_proibidos"]) and all(_v410_h0dn_cabeca(c_["ramos"]["vereditos"]["leitura_partes"]).find(tk_) < 0 for tk_ in c_["tokens_proibidos"]))\n',
     '    c8_ok_ = (not any(tk_ in txt_json_ for tk_ in toks_) and not any(a_ in txt_json_ for a_ in agreg_) and not [f_ for f_ in frases_ if f_[0].startswith(("F53", "F54", "F55"))]\n'
     '              and not any(tk_ in c_["veredito_ok"] for tk_ in toks_) and all(_v410_h0dn_cabeca(c_["ramos"]["vereditos"]["leitura_partes"]).find(tk_) < 0 for tk_ in toks_) and len(toks_) == 3)\n', 1),
])
troca("runtime_v410.py", [
    ('    for m_ in _re.finditer("|".join(_re.escape(x_) for x_ in (globals().get("_V410_H0DN_CONTRACT") or {}).get("tokens_proibidos", ("FIVE_SIGMA_" + "OBSERVED", "H0DN_" + "CONFIRMS"))), s_):   # F53c (D72: tokens de veredito proibidos do H0DN)\n',
     '    for m_ in _re.finditer("|".join(_re.escape(x_) for x_ in ("FIVE_SIGMA_" + "OBSERVED", "H0DN_" + "CONFIRMS")), s_):   # F53c (D72: os dois tokens de veredito proibidos do H0DN, em todo texto; o terceiro, DETEC+TED, so\' no texto do H0DN (c8) e no trecho com H0DN (F53b): o um.py tem vereditos legados com ele)\n', 1),
])
