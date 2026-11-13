# -*- coding: utf-8 -*-
"""_fix_conferidor_topo_em_linha_v411.py -- (claude-construtor-v411, fork C, 12/11/2026, cadeia REAL) UMA rodada de conserto do achado do harness do
fechar em modo de depuracao: o conferidor roda dentro de um SANDBOX que copia uma LISTA EXPLICITA de arquivos do pacote (pos_rito, da outra frente:
guarda_p18, guarda_frases, base_um_v410, runtime_h0dn, VERBATIM_CONGELADO, delta, quadro_v397, runtime_quadro_v397, conferir_rito e acom_conferencias).
O conserto da condicao 3(a) tinha posto no conferidor um `import topo_com_resultado_v411` -- um arquivo NOVO, que a lista do sandbox nao conhece: o
conferidor cairia la' com ModuleNotFoundError. A causa: eu dei ao conferidor uma dependencia de arquivo a mais. O conserto (sem tocar pos_rito\\): a
conferencia do topo passa a morar DENTRO do conferidor, numa funcao so' (_topo_com_resultado_v411, que devolve um espaco de nomes com confere,
controles_negativos, preencher, ratificado e as constantes), e o topo_com_resultado_v411.py vira um CARREGADOR: le essa funcao do conferir_rito_v411.py
por AST e a executa, para o ensaio a seco continuar importando o mesmo nome. A fonte e' UMA (o conferidor); nada e' duplicado; a interface do modulo
nao muda. O corpo e' copiado por ESTE script do modulo atual (nao redigitado). Backup de BYTES dos dois arquivos antes; ancoras unicas; ast.parse.
uso: python -B -X utf8 _fix_conferidor_topo_em_linha_v411.py"""
import ast, datetime, hashlib, os
HERE = os.path.dirname(os.path.abspath(__file__))
PC = os.path.join(HERE, "conferir_rito_v411.py"); PM = os.path.join(HERE, "topo_com_resultado_v411.py")
bc = open(PC, "rb").read(); tc = bc.decode("utf-8"); assert "\r" not in tc
bm = open(PM, "rb").read(); tm = bm.decode("utf-8").replace("\r\n", "\n")
# ---- o corpo do modulo atual: de N_MARCADORES ate' o fim (as importacoes e o docstring ficam de fora)
ini = tm.index("\nN_MARCADORES = 12\n") + 1
corpo = tm[ini:].rstrip("\n") + "\n"
assert corpo.startswith("N_MARCADORES = 12\n") and "def controles_negativos(" in corpo and "def confere(" in corpo and "def preencher(" in corpo and "def ratificado(" in corpo and '"""' in corpo
assert "import " not in corpo.replace("important", ""), "o corpo traz importacao propria: rever antes de embutir"
NOMES = ("N_MARCADORES", "RECUO", "DUAS_LINHAS", "OBRIGACOES", "ratificado", "preencher", "confere", "controles_negativos")
ident = "".join(("    " + l_ if l_.strip() else l_) for l_ in corpo.splitlines(True))
FUNC = ("def _topo_com_resultado_v411():\n"
        "    \"\"\"(condicao 3(a) da gerencia c1, 12/11) a conferencia de que o TOPO do artigo selado traz o RESULTADO, INDEPENDENTE da funcao do candidato: o texto e os formatos vem do arquivo RATIFICADO (DL.TOPO_RATIFICADO_ARQ),\n"
        "    os numeros do core; do candidato so' a tabela de caminhos (conferida contra a fonte ratificada onde ela e' um caminho) e os dois renderizadores puros. A FONTE UNICA e' esta funcao: o topo_com_resultado_v411.py a carrega\n"
        "    daqui por AST (para o ensaio a seco); o conferidor nao ganha arquivo a mais (o sandbox do harness do fechar copia uma lista explicita). Devolve o espaco de nomes (confere, controles_negativos, preencher, ratificado).\"\"\"\n"
        "    import math, types\n"
        + ident +
        "    return types.SimpleNamespace(" + ", ".join("%s=%s" % (n_, n_) for n_ in NOMES) + ")\n"
        "\n\n"
        "TR11 = _topo_com_resultado_v411()\n")
A = "import topo_com_resultado_v411 as TR11  # noqa: E402\n"
assert tc.count(A) == 1, tc.count(A)
assert "_topo_com_resultado_v411" not in tc
tc2 = tc.replace(A, FUNC)
tree = ast.parse(tc2)
defs = [n_ for n_ in tree.body if isinstance(n_, ast.FunctionDef) and n_.name == "_topo_com_resultado_v411"]; assert len(defs) == 1
seg = ast.get_source_segment(tc2, defs[0]); s16 = hashlib.sha256(seg.encode("utf-8")).hexdigest()[:16]
# ---- o carregador: o cabecalho e o docstring do modulo atual ficam; o corpo vira a carga por AST
cab = tm[:tm.index("import json, math, re\n")]
assert cab.count('"""') == 2, "o docstring do modulo nao foi achado inteiro"
CARGA = ("import ast, hashlib, json, math, os, re, types\n"
         "import delta_v411 as DL\n\n"
         "# A FONTE UNICA desta conferencia e' a funcao _topo_com_resultado_v411 do conferir_rito_v411.py (o conferidor do rito e' autocontido: o sandbox do harness do fechar copia uma lista explicita de arquivos, e este\n"
         "# modulo nao esta' nela). Aqui a funcao e' LIDA do conferidor por AST e executada, para o ensaio a seco importar o mesmo nome de sempre; nada e' duplicado.\n"
         "_HERE = os.path.dirname(os.path.abspath(__file__)); _ARQ = os.path.join(_HERE, \"conferir_rito_v411.py\")\n"
         "_SRC = open(_ARQ, encoding=\"utf-8\").read()\n"
         "_DEFS = [n_ for n_ in ast.parse(_SRC).body if isinstance(n_, ast.FunctionDef) and n_.name == \"_topo_com_resultado_v411\"]\n"
         "assert len(_DEFS) == 1, \"a funcao _topo_com_resultado_v411 nao esta' (uma vez so') no conferir_rito_v411.py\"\n"
         "_SEG = ast.get_source_segment(_SRC, _DEFS[0]); FONTE_SHA16 = hashlib.sha256(_SEG.encode(\"utf-8\")).hexdigest()[:16]\n"
         "_NS = {\"DL\": DL, \"json\": json, \"re\": re, \"math\": math, \"os\": os, \"types\": types}\n"
         "exec(compile(_SEG, _ARQ + \"::_topo_com_resultado_v411\", \"exec\"), _NS)\n"
         "_M = _NS[\"_topo_com_resultado_v411\"]()\n"
         + "".join("%s = _M.%s\n" % (n_, n_) for n_ in NOMES))
tm2 = cab + CARGA
ast.parse(tm2)
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
for p_, b_ in ((PC, bc), (PM, bm)):
    bak_ = p_ + ".bak_" + ts + "_topo_em_linha"; open(bak_, "wb").write(b_); assert open(bak_, "rb").read() == b_
for p_, t_ in ((PC, tc2), (PM, tm2)):
    nb_ = t_.encode("utf-8"); open(p_ + ".tmp", "wb").write(nb_); assert os.path.getsize(p_ + ".tmp") == len(nb_); os.replace(p_ + ".tmp", p_)
print("ok | conferidor", len(bc), "->", len(tc2.encode("utf-8")), "| modulo (carregador)", len(bm), "->", len(tm2.encode("utf-8")), "| sha16 da funcao no conferidor:", s16)
