# -*- coding: utf-8 -*-
"""guarda_p18_v392.py -- P18: a GUARDA DE TEXTO da v392 (plano, etapa 4 passo 8): a regex do molde (so' a palavra recusada e as formas PROVED_BY / TGL_PROVED) MAIS as cinco regras
das cunhagens. Aplica-se SO' ao texto NOVO dos patches (registros, erratas, artigo, md), nunca ao um.py inteiro (o token v388 que nega a palavra fica como registro, G_UMPY (r)(iv)).
 1. nenhuma ocorrencia nova da palavra recusada (nem negada); nem PROVED_BY / TGL_PROVED;
 2. nunca «Nome fixo» nem «the Name is fixed»: o fixo e' o Verbo, beta_TGL (memoria o-verbo-e-fixo-o-nome-e-posto-08out);
 3. nunca «a singularidade converge» nem «cai no atrator» (memoria singularidade-e-a-leitura-do-atrator-10out);
 4. nunca a luz ou a observacao «confirma»: o observador testemunha (memoria tgl-unidade-fundamental-e-a-luz-testemunha-10out);
 5. nunca «nao provou» nem «pos-dicao» como demerito (lei da prova de 05/10; precedente: o perielio de Mercurio).
O texto-fonte desta guarda e' embutido no runtime do um.py (GUARDA_V392_SRC) para que cada registro refaca a checagem a cada rito (fail-closed). A palavra recusada nunca e' escrita por extenso aqui:
e' montada por concatenacao, como no molde.  Uso: python -I -B -X utf8 guarda_p18_v392.py <arquivo...>   (lista violacoes; rc 1 se houver)"""
import re, sys

GUARDA_V392_SRC = r'''
def _v392_guarda_texto(txt_):
    """v392 -- P18: a guarda de texto das cinco regras (aplica-se ao texto NOVO). Devolve a lista de violacoes [(regra, trecho)]."""
    import re as _re
    banida_ = "CONF" + "IRMED"
    regras_ = [
        ("R1_palavra_recusada", _re.compile(banida_ + r"|PRO" + r"VED_BY|TGL_PRO" + r"VED")),
        ("R2_nome_fixo", _re.compile(r"Nome\s+fixo|Nome\s+(?:e|é)\s+fixo|the\s+Name\s+is\s+fixed|fixed\s+Name", _re.I)),
        ("R3_singularidade_converge", _re.compile(r"singularidade\s+converge|singularidade\s+cai\s+no\s+atrator|cai\s+no\s+atrator|singularity\s+converges|falls?\s+into\s+the\s+attractor", _re.I)),
        ("R4_luz_confirma", _re.compile(r"(?:\bluz\b|observa\w+|\blight\b|observation)[^.;\n]{0,60}\bconfirm\w*|\bconfirm\w*[^.;\n]{0,60}(?:\bluz\b|observa\w+|\blight\b|observation)", _re.I)),
        ("R5_nao_provou_posdicao", _re.compile(r"n(?:ã|a)o\s+provou|did\s+not\s+prove|has\s+not\s+proven|p(?:ó|o)s-?\s?di(?:ç|c)(?:ã|a)o|post-?diction", _re.I)),
    ]
    out_ = []
    for nome_, rx_ in regras_:
        for m_ in rx_.finditer(txt_):
            out_.append((nome_, txt_[max(0, m_.start() - 30):m_.end() + 30].replace("\n", " ")))
    return out_
'''
_ns = {}
exec(compile(GUARDA_V392_SRC, "<guarda_p18>", "exec"), _ns)
violacoes = _ns["_v392_guarda_texto"]

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    rc = 0
    for p in sys.argv[1:]:
        v = violacoes(open(p, encoding="utf-8").read())
        print(p, "->", "LIMPO" if not v else v[:10])
        rc |= bool(v)
    sys.exit(rc)
