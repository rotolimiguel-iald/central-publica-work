# -*- coding: utf-8 -*-
"""_medir_a2_v411.py -- o A2 da revisao de terceiro da v410 (61 expoentes sem agrupar no TXT do artigo, PT e EN, em linhas herdadas): mede ANTES e DEPOIS de uma mudanca CONTIDA no conversor _tex_to_txt (o do um.py da v410
selada, lido por trecho), rodando os dois conversores sobre os .tex que o rito da v410 gravou no Nos (so' leitura). A mudanca: antes de dissolver as chaves, todo expoente agrupado de mais de um caractere, ^{X}, vira ^(X) (o
agrupamento que o PDF mostra passa a aparecer no TXT). Criterio do achado (o do revisor: `e^-s c(x)`, `e^-t`, `P^k+1=P`): expoente que comeca por sinal ou que traz operador logo apos o primeiro termo, sem parenteses.
Grava A2_MEDIDA_v411.json; nada mais e' escrito. uso: python -B -X utf8 _medir_a2_v411.py"""
import json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import base_um_v410 as B  # noqa: E402
import delta_v411 as DL  # noqa: E402
ANCORA = '    t = t.replace("~", " ").replace("{", "").replace("}", "")\n'
NOVA = ('    t = _re.sub(r"\\^\\{([^{}]{2,})\\}", r"^(\\1)", t)   # v411 (A2 da revisao de terceiro da v410): o expoente agrupado de mais de um caractere fica agrupado no TXT, como no PDF\n')
src0 = B.trecho("_tex_to_txt")
assert src0.count(ANCORA) == 1, "a ancora do A2 nao e' unica no conversor"
src1 = src0.replace(ANCORA, NOVA + ANCORA)
ns0, ns1 = {}, {}
exec(compile(src0, "<base:_tex_to_txt>", "exec"), ns0); exec(compile(src1, "<v411:_tex_to_txt>", "exec"), ns1)
RX = re.compile(r"\^(?![(])(?:[-−+][^\s$]|[A-Za-z0-9.]+[+\-−/·*][^\s$])")
out = {"contrato": "A2_MEDIDA_v411", "ancora": ANCORA.strip(), "linha_nova": NOVA.strip(), "criterio": RX.pattern, "linguas": {}}
for lg in ("pt", "en"):
    tex = open(os.path.join(DL.NOS, "um_absoluto_%s.tex" % lg), encoding="utf-8").read()
    t0, t1 = ns0["_tex_to_txt"](tex), ns1["_tex_to_txt"](tex)
    txt_nos = open(os.path.join(DL.NOS, "um_absoluto_%s.txt" % lg), encoding="utf-8").read()
    a0, a1 = RX.findall(t0), RX.findall(t1)
    g_ = re.findall(r"\^\{[^{}]{2,}\}", tex)
    out["linguas"][lg] = {"grupos_de_expoente_de_2_ou_mais_caracteres_no_tex": len(g_), "dissolvidos_no_txt_antes": len(g_) - t0.count("^("), "dissolvidos_no_txt_depois": len(g_) - (t1.count("^(") - t0.count("^(")) - (len(g_) - (t1.count("^(") - t0.count("^("))) if False else max(0, len(g_) - (t1.count("^(") - t0.count("^("))),
                          "criterio_largo_antes": len(a0), "criterio_largo_depois": len(a1), "nota_do_criterio_largo": "o criterio largo (sinal ou operador logo apos o primeiro termo) inclui casos nao ambiguos como q^2+alfa^2 e P^+; o do revisor (61) e' o dos expoentes de grupo dissolvido", "o_base_reproduz_o_txt_do_nos": t0 == txt_nos, "amostra_antes": sorted(set(a0))[:12], "amostra_depois": sorted(set(a1))[:12],
                          "linhas_que_mudam": sum(1 for x_, y_ in zip(t0.splitlines(), t1.splitlines()) if x_ != y_), "n_linhas_igual": len(t0.splitlines()) == len(t1.splitlines())}
out["mudanca_contida_no_conversor"] = True
p = os.path.join(HERE, "A2_MEDIDA_v411.json"); open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1)); os.replace(p + ".tmp", p)
print(json.dumps(out["linguas"], ensure_ascii=False, indent=1)[:2500])
