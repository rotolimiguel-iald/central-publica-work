# -*- coding: utf-8 -*-
"""_fix_aspas_v411.py -- conserto da CAUSA apontada por conferir_citacoes_v411.py: nos arquivos AUTORAIS da v411, toda citacao entre « » que NAO e' fala verbatim do operador (nomes de regras, frases proibidas ou
obrigatorias, titulos de quadro, frases da gerencia) passa a “ ” (regra da casa: « » so' para fala do operador). As citacoes verbatim ficam. Backup de BYTES antes; respeita o fim de linha; ast.parse depois.
uso: python -B -X utf8 _fix_aspas_v411.py"""
import ast, datetime, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
import glob
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
_nrm = lambda s_: " ".join(str(s_).replace("\r\n", "\n").split())
TEXTOS = [f_["text"] for f_ in DL.FALAS_V411] + [open(p_, "rb").read().decode("utf-8", "replace") for p_ in glob.glob(os.path.join(DL.V410, "insumos", "cunhagens", "*.txt")) + glob.glob(os.path.join(DL.CUN, "OPERADOR_*_verbatim.txt"))]
TN = [_nrm(t_) for t_ in TEXTOS]
ARQS = ["delta_v411.py", "registros_h0dn_v411.py", "registros_v411.py", "runtime_h0dn_v411.py", "quadro_v411.py", "gerar_candidato_v411.py", "guarda_frases_v411.py", "p00_precondicoes_v411.py", "guarda_material_privado_v411.py",
        "copiar_insumos_v411.py", "pos_build_kernel_v411.py", "_teste_h0dn_offline_v411.py", "_teste_quadro_v411.py"]
tot = 0
for a_ in ARQS:
    p_ = os.path.join(HERE, a_); b_ = open(p_, "rb").read(); t_ = b_.decode("utf-8")
    n_ = [0]

    def troca(m_):
        c_ = m_.group(1)
        if len(c_) >= 3 and not any(_nrm(c_) in x_ for x_ in TN):
            n_[0] += 1
            return "“" + c_ + "”"
        return m_.group(0)
    novo_ = re.sub(r"«([^«»]+)»", troca, t_)
    if n_[0]:
        ast.parse(novo_)
        open(p_ + ".bak_" + TS, "wb").write(b_)
        nb_ = novo_.encode("utf-8"); open(p_ + ".tmp", "wb").write(nb_); assert os.path.getsize(p_ + ".tmp") == len(nb_); os.replace(p_ + ".tmp", p_)
        print("%-34s %d citacao(oes) passaram a “ ”" % (a_, n_[0])); tot += n_[0]
print("total:", tot)
