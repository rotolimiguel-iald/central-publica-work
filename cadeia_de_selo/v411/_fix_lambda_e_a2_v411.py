# -*- coding: utf-8 -*-
"""_fix_lambda_e_a2_v411.py -- (claude-construtor-v411, fork C, 12/11/2026) UMA rodada de conserto por achado do ensaio a seco da v411:
 (1) [achado: o pdflatex do artefato PARA em «Unicode character Λ (U+039B)» -- o texto do topo diz «(ΛCDM)»] quadro_v411._v411_tex_misto passa a converter Λ (fora do modo matematico: $\\Lambda$; dentro: \\Lambda), e a guarda do
     gerador sobre o texto RENDERIZADO passa a recusar QUALQUER letra do bloco grego (U+0370 a U+03FF), nao so' beta/alfa/sigma (a causa: a guarda era estreita demais);
 (2) [achado: a regra da ordem do quadro da v397 (quadro_v397.confere_txt) deixou de achar o p calibrado no TXT, porque o A2 agrupa o expoente: 4,4×10^(-6)] quadro_v397.normaliza passa a ler o expoente agrupado
     (×10^(-6)) como ×10^-6: o A2 e' mudanca CONTIDA no conversor para TXT, e quem le o TXT tem de ler a forma nova.
Backup de BYTES antes de cada arquivo; ancoras unicas; ast.parse depois. uso: python -B -X utf8 _fix_lambda_e_a2_v411.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def troca(arq_, pares_):
    p_ = os.path.join(HERE, arq_); b_ = open(p_, "rb").read(); t_ = b_.decode("utf-8"); assert "\r" not in t_, arq_
    for a_, n_ in pares_:
        assert t_.count(a_) == 1, (arq_, a_[:100], t_.count(a_))
        t_ = t_.replace(a_, n_)
    ast.parse(t_)
    bak_ = p_ + ".bak_" + TS + "_forkc"; open(bak_, "wb").write(b_); assert open(bak_, "rb").read() == b_
    nb_ = t_.encode("utf-8"); open(p_ + ".tmp", "wb").write(nb_); assert os.path.getsize(p_ + ".tmp") == len(nb_); os.replace(p_ + ".tmp", p_)
    print("ok", arq_, len(b_), "->", len(nb_))


troca("quadro_v411.py", [
    ('    fora_ = {"β": r"$\\beta$", "α": r"$\\alpha$", "σ": r"$\\sigma$", "√": r"$\\surd$", "×": r"$\\times$", "−": r"$-$", "%": r"\\%"}\n',
     '    fora_ = {"β": r"$\\beta$", "α": r"$\\alpha$", "σ": r"$\\sigma$", "Λ": r"$\\Lambda$", "√": r"$\\surd$", "×": r"$\\times$", "−": r"$-$", "%": r"\\%"}   # (v411: o Λ do ΛCDM, achado do ensaio a seco)\n'),
    ('    dentro_ = {"β": r"\\beta ", "α": r"\\alpha ", "σ": r"\\sigma ", "√e": r"\\sqrt e", "√": r"\\sqrt ", "×": r"\\times ", "−": "-"}\n',
     '    dentro_ = {"β": r"\\beta ", "α": r"\\alpha ", "σ": r"\\sigma ", "Λ": r"\\Lambda ", "√e": r"\\sqrt e", "√": r"\\sqrt ", "×": r"\\times ", "−": "-"}\n'),
])
troca("gerar_candidato_v411.py", [
    ('        assert not any(("β" in l_ or "α" in l_ or "σ" in l_) for l_ in _ls), ("unicode de beta/alfa/sigma no LaTeX renderizado (licao da v408)", _k)\n',
     '        assert not any(any(0x370 <= ord(ch_) <= 0x3FF for ch_ in l_) for l_ in _ls), ("letra grega Unicode no LaTeX renderizado (licao da v408; na v411 o Λ do ΛCDM, achado do ensaio a seco)", _k, sorted({ch_ for l_ in _ls for ch_ in l_ if 0x370 <= ord(ch_) <= 0x3FF}))\n'),
])
troca("quadro_v397.py", [
    ('    t = re.sub(r"[×x]\\s*10\\^\\s*-?\\s*(\\d+)", lambda m: "e-" + m.group(1), t)\n',
     '    t = re.sub(r"[×x]\\s*10\\^\\s*\\(?\\s*-?\\s*(\\d+)\\s*\\)?", lambda m: "e-" + m.group(1), t)   # (v411: o A2 agrupa o expoente no TXT, ×10^(-6); a leitura aceita as duas formas)\n'),
])
print("FEITO")
