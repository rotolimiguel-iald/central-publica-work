# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026, claude-construtor-v411 (retomada, fork C); condicao 3(a) da gerencia c1] o topo SELADO traz o RESULTADO: a variante de recuo (fonte ausente, registro que nao selou) nunca passa como selo
"""topo_com_resultado_v411.py -- a conferencia de que o TOPO do artigo selado traz o RESULTADO (os doze marcadores preenchidos, as duas
linhas juntas), usada pelo ensaio a seco (sobre o .tex e o .txt do dry) e pelo conferidor do rito (sobre o .txt do Nos). A gerencia aceitou
(12/11) que, com a fonte de um marcador AUSENTE no core, o topo diga visivelmente que nao da' o resultado; a CONDICAO: essa variante nunca
passa como selo. Esta conferencia e' INDEPENDENTE da funcao do candidato (_v411_topo_texto): o texto e os formatos vem do arquivo
RATIFICADO (DL.TOPO_RATIFICADO_ARQ, lido aqui); a tabela de caminhos vem do candidato (o arquivo ratificado da' a fonte em prosa) e e'
conferida contra a fonte ratificada onde ela e' um caminho; os numeros vem do core. Do candidato so' se usam os dois RENDERIZADORES puros
(_v411_tex_misto, o conversor para LaTeX; _tex_to_txt, o conversor para TXT), para comparar o topo inteiro com o artigo.

O que reprova (ok False): o registro h0dn_bg1_v411 nao selou; o texto embutido no candidato != o ratificado; algum dos doze marcadores sem
fonte no core, nao numerico ou nao finito; marcador que sobra; o topo inteiro, preenchido, nao esta' no artigo (contiguo); uma das duas
frases de recuo no artigo; as duas linhas (o primario sob o modelo de erros publicado e as Cefeidas livres) fora de ordem ou fora do mesmo
paragrafo; e o numero que nao sustenta a frase do texto ratificado (o primario a n >= 5; as Cefeidas livres abaixo de 5; o z_disc abaixo do
degrau de 5). controles_negativos() roda a conferencia em sete casos que TEM de reprovar (sem a v397 no core; o registro sem selar; um
marcador nao finito; o texto do candidato diferente do ratificado; o artigo com o topo de recuo do proprio candidato; o artigo sem a linha das
Cefeidas livres; o artigo sem o resultado, so' com o prefixo) e no caso base, que TEM de passar."""
import ast, hashlib, json, math, os, re, types
import delta_v411 as DL

# A FONTE UNICA desta conferencia e' a funcao _topo_com_resultado_v411 do conferir_rito_v411.py (o conferidor do rito e' autocontido: o sandbox do harness do fechar copia uma lista explicita de arquivos, e este
# modulo nao esta' nela). Aqui a funcao e' LIDA do conferidor por AST e executada, para o ensaio a seco importar o mesmo nome de sempre; nada e' duplicado.
_HERE = os.path.dirname(os.path.abspath(__file__)); _ARQ = os.path.join(_HERE, "conferir_rito_v411.py")
_SRC = open(_ARQ, encoding="utf-8").read()
_DEFS = [n_ for n_ in ast.parse(_SRC).body if isinstance(n_, ast.FunctionDef) and n_.name == "_topo_com_resultado_v411"]
assert len(_DEFS) == 1, "a funcao _topo_com_resultado_v411 nao esta' (uma vez so') no conferir_rito_v411.py"
_SEG = ast.get_source_segment(_SRC, _DEFS[0]); FONTE_SHA16 = hashlib.sha256(_SEG.encode("utf-8")).hexdigest()[:16]
_NS = {"DL": DL, "json": json, "re": re, "math": math, "os": os, "types": types}
exec(compile(_SEG, _ARQ + "::_topo_com_resultado_v411", "exec"), _NS)
_M = _NS["_topo_com_resultado_v411"]()
N_MARCADORES = _M.N_MARCADORES
RECUO = _M.RECUO
DUAS_LINHAS = _M.DUAS_LINHAS
OBRIGACOES = _M.OBRIGACOES
ratificado = _M.ratificado
preencher = _M.preencher
confere = _M.confere
controles_negativos = _M.controles_negativos
