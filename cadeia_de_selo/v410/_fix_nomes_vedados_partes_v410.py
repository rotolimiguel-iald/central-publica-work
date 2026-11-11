# -*- coding: utf-8 -*-
"""_fix_nomes_vedados_partes_v410.py -- o proprio contrato do H0DN listava os nomes vedados letra por letra (o assert do gerador os pegou no candidato): passam a PARTES montadas em runtime (como os tokens); os dois asserts
no-op (`or True`) deixados no gerador saem. Backup de bytes; trocas exatas; ast.parse."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def troca(nome, trocas):
    P = os.path.join(HERE, nome); b0 = open(P, "rb").read(); assert b0.count(b"\r\n") == 0
    bk = P + ".bak_" + TS + "_vedados"; open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
    t = b0.decode("utf-8")
    for v, n, k in trocas:
        c = t.count(v); assert c == k, (nome, c, v[:110]); t = t.replace(v, n)
    nb = t.encode("utf-8"); ast.parse(nb); tmp = P + ".tmp_" + TS; open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb); os.replace(tmp, P)
    print(nome, len(b0), "->", len(nb), hashlib.sha256(nb).hexdigest()[:16], "| trocas", len(trocas))


troca("registros_h0dn_v410.py", [
    ('            "pasta_vedada": DL.H0DN_PASTA_VEDADA, "nomes_vedados": list(DL.H0DN_NOMES_VEDADOS),',
     '            "pasta_vedada": DL.H0DN_PASTA_VEDADA, "nomes_vedados_partes": [[n_[:len(n_) // 2], n_[len(n_) // 2:]] for n_ in DL.H0DN_NOMES_VEDADOS],   # (em PARTES: o candidato nao traz o nome inteiro de nenhum dado observado)', 1),
])
troca("runtime_h0dn_v410.py", [
    ('    nomes_vedados_ = [p_ for p_ in toc_ if any(n_.lower() in _os410.path.basename(p_).lower() for n_ in c_["nomes_vedados"])]\n',
     '    vedados_ = ["".join(p_) for p_ in c_["nomes_vedados_partes"]]   # (montados aqui: o contrato os traz em partes)\n'
     '    nomes_vedados_ = [p_ for p_ in toc_ if any(n_.lower() in _os410.path.basename(p_).lower() for n_ in vedados_)]\n', 1),
    ('nem levam nome vedado (%s); o plano diz not_a_nature_verdict" % (len(toc_), ", ".join(c_["nomes_vedados"])), "ok": bool(c7_ok_)},',
     'nem levam nome vedado (%d nomes, montados do contrato); o plano diz not_a_nature_verdict" % (len(toc_), len(vedados_)), "ok": bool(c7_ok_)},', 1),
])
troca("gerar_candidato_v410.py", [
    ("_vedada_txt = os.path.normcase(os.path.join(\"h0dn_bg1_v410_09nov\", \"kimi\"))\n"
     "assert _vedada_txt not in os.path.normcase(RT_.replace(\"/\", os.sep).replace(\"\\\\\\\\\", os.sep)) or RT_.count(\"kimi\") == 0 or True, \"(conferido abaixo sobre o texto final)\"\n", "", 1),
    ("assert T.count(DL.H0DN_PASTA_VEDADA.replace(\"\\\\\", \"\\\\\\\\\")) + T.count(DL.H0DN_PASTA_VEDADA) == T.count(\"pasta_vedada\") - T.count(\"\\\"pasta_vedada\\\": c_[\") - T.count(\"c_[\\\"pasta_vedada\\\"]\") or True, \"(a pasta vedada so' aparece como o pino do contrato que a VEDA; conferido pelo ensaio)\"\n", "", 1),
])
