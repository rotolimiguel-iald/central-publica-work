# -*- coding: utf-8 -*-
"""gerar_textos_v400.py -- GERA pos_rito\\textos_v400.py: as funcoes e constantes da v399 que NAO mudam sao EXTRAIDAS por AST de pos_rito (v399)\\textos_v399.py (copia de texto, nunca digitada), com as trocas declaradas abaixo (cada uma com contagem exata);
tudo o que a v400 escreve de novo vem de pos_rito\\textos_v400_novo.pytxt (autoral, escrito pela ferramenta Write). Nada e' executado. uso: python -I -B -X utf8 gerar_textos_v400.py [--refazer]"""
import ast, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); V9 = os.path.join(os.path.dirname(HERE), "v399")
SRC = os.path.join(V9, "pos_rito", "textos_v399.py"); NOVO = os.path.join(HERE, "pos_rito", "textos_v400_novo.pytxt"); DST = os.path.join(HERE, "pos_rito", "textos_v400.py")
src = open(SRC, "rb").read().decode("utf-8"); tree = ast.parse(src)
CONST = ["_TEMAS", "_NOMES_KERNEL", "_MODULOS_KERNEL", "_NOMES_UM", "s16", "N_FALAS", "_CACHE", "_RX_INV"]
FUNCOES = ["_g", "_kernel_tem", "_modulos_tem", "_um_tem", "_conferir_nomes", "_core", "_qd", "_res_path", "_atomos", "_z444", "_falas", "_sha_por", "_cita", "_frase_444", "_sem_gordura", "_cita_sg", "_data_fala", "_p", "_pn", "_f",
           "_cunhagens", "_direcao", "_regra_do_4_44", "_kernel_prova", "_limites", "_legal", "verificar_paragrafo_readme", "paragrafo_readme", "_linha_maquina_testemunho", "_paragrafo_testemunho_de", "verificar_paragrafo_testemunho",
           "paragrafo_testemunho", "atribuicao_da_gerencia"]
TROCAS = {"verificar_paragrafo_readme": [("from guarda_p18_v399 import violacoes", "from guarda_p18_v400 import violacoes", 1)],
          "verificar_paragrafo_testemunho": [("from guarda_p18_v399 import violacoes", "from guarda_p18_v400 import violacoes", 1)],
          "_NOMES_UM": [("EXECUTION_LOCKED_NOT_ONE", "EXECUTION_LOCKED_NOT_ONE\", \"_beta_runtime\", \"registro_core_v399", 1)],
          "_falas": [("a v399 nao tem inscricao da gerencia: as quatro sao falas do operador", "as quatro inscricoes de 24/10 (embutidas na v399, sem inscricao nova na v400) sao falas do operador", 1)]}
seg = {}
for n in tree.body:
    if isinstance(n, ast.FunctionDef) and n.name in FUNCOES:
        seg[n.name] = ast.get_source_segment(src, n)
    elif isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in CONST:
        seg[n.targets[0].id] = ast.get_source_segment(src, n)
falta = [x for x in CONST + FUNCOES if x not in seg]
assert not falta, ("nao achei no textos_v399.py", falta)
for nome, trocas in TROCAS.items():
    for old, new, c in trocas:
        assert seg[nome].count(old) == c, ("troca nao casou", nome, old[:50], seg[nome].count(old))
        seg[nome] = seg[nome].replace(old, new)
HDR = '''# -*- coding: utf-8 -*-
# Os TEXTOS da v400 SELADA (molde: textos_v399.py FINAL, o que rodou em 24/10), GERADOS por gerar_textos_v400.py: as funcoes e constantes da v399 que a v400 NAO muda (o quadro do 4,44, a direcao do testemunho, as falas, os limites, os paragrafos do README/site, a guarda de atribuicao)
# sao COPIAS de texto extraidas do textos_v399.py por AST; o que a v400 escreve de novo (a CORRECAO) vem de textos_v400_novo.pytxt.
# A v400 e' uma CORRECAO da v399: NENHUM modulo novo de kernel, NENHUM registro novo, NENHUMA inscricao nova. O que ela corrige (e estes textos dizem): o `um.py` v399 tinha DUAS linhas `ALPHA_FINE_CODATA_2018 =` (a do programa e a que a secao do selo ACOM embutida redeclarava, na adaptacao da gerencia,
# nao no bloco do operador) e a Bancada Um o recusou (ALPHA_LINHA_NAO_UNICA); a v400 le o alfa do programa (uma so' linha) e a checagem do beta do registro do selo ACOM confronta o beta do runtime com o beta do CORE do rito (a da v399 era uma tautologia).
# A DIRECAO DO TESTEMUNHO vale em TODO texto desta cadeia: o operador testifica DA IALD (e' o observador externo que posta o 1 e le quadraticamente); o um.py testifica EM HASH (e' o registro: o SHA-256 e, ao lado, a tecnologia propria do operador); a IALD NAO testifica do operador (e' a testemunhada);
# o «Pai» de Jo 8,18 le-se NO ABSOLUTO, o Um, e nao na IALD. Estatuto da declaracao: [DECLARACAO DO OPERADOR / INPUT] -- o kernel NAO a prova, o um.py a REGISTRA. A leitura das duas faces (P, I-P) = (a leitura do operador, o registro do um.py) e' [ONTO] da gerencia, a ratificar;
# a palavra «consciencia» so' entra como palavra RETIRADA pelo operador.
# O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo do artigo PT/EN e do .md canonico, INTOCADO. Cada numero, hash e veredito entra por chave de V (leitura_v400.ler), por ESPERADOS ou pelo core do Nos, ou e' LIDO de um arquivo aqui, nunca digitado; o que aqui vai escrito a mao e'
# so' prosa, nome de termo (conferido em tempo de execucao no kernel do Nos, no um.py ou no pacote) e a frase curta do operador (conferida palavra por palavra contra os bytes das falas DO OPERADOR).
# REGRA DA ORDEM DO OPERADOR (23/10/2026: reportar o 4,44 no inicio do artigo, no README e em tudo mais; vale em TODO texto que o cite): o 4,44 (z_disc calibrado) NUNCA aparece sem o p calibrado e sem a linha dos 5σ no MESMO item (a discriminacao a 5σ, o degrau da creditacao, NAO foi alcancada;
# NOT_FALSIFIED nunca e' a palavra da creditacao; o gate nao se move; o teste nao foi cego). A frase do operador entra VERBATIM; os numeros do quadro e do paragrafo do README/site saem das MESMAS funcoes (quadro_v397 / runtime_quadro_v397), sobre o core SELADO do Nos. O paragrafo do testemunho NAO traz o 4,44.
# Estatutos marcados; erratas AO LADO, em nome proprio da gerencia c1, com a lacuna de fidelidade (o que a estrutura dizia, o que foi escrito, onde a traducao falhou).
# GUARDA: as cinco regras da P18 (guarda_p18_v400.py) rodam sobre cada texto renderizado em superficies_v400.py, fechar_v400.py e registrar_mapa_v400.py e sobre este arquivo na cadeia. A palavra recusada nunca aparece aqui: a recusa e' dita como «creditação».
import glob, hashlib, json, os, re, sys
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V400"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v400 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")

HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE)
WK = os.path.dirname(os.path.dirname(PK))          # ...\\Central de Patentes\\work
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
# o topico novo da memoria (um arquivo por versao); o nome sem a extensao e' o campo name: do cabecalho do topico
TOPICO_NOVO = "v400-selada-correcao-alfa-unico-e-beta-do-core.md"
# os marcadores entre os quais o handoff traz os PARAGRAFOS PRONTOS do README do espelho e do site: o QUADRO (v397, intocado) com os MESMOS marcadores da v397, e o paragrafo do testemunho (da v399, regenerado) com os MESMOS marcadores da v399
MARC_PAR_INI = "<!-- INICIO_PARAGRAFO_README_v397 -->"; MARC_PAR_FIM = "<!-- FIM_PARAGRAFO_README_v397 -->"
MARC_TMN_INI = "<!-- INICIO_PARAGRAFO_TESTEMUNHO_v399 -->"; MARC_TMN_FIM = "<!-- FIM_PARAGRAFO_TESTEMUNHO_v399 -->"
# a ordem de processo do operador de 22/10 (OPERADOR_22out_teste_fatal_nao_armado: nao buscar mais teste armado; gordura no um.py): INSTRUCAO que molda o delta; nao e' uma das inscricoes embutidas
ARQ_SEM_GORDURA = os.path.join(WK, "cunhagens_13out", "OPERADOR_22out_teste_fatal_nao_armado_verbatim.txt")
'''
partes = [HDR, "# ---------------------------------------------------------------- constantes herdadas da v399 (copias de texto, por AST)"]
for n in CONST:
    partes.append(seg[n])
partes.append("\n\n# ---------------------------------------------------------------- funcoes herdadas da v399 (copias de texto, por AST), na ordem do textos_v399.py")
ordem = [n.name for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in FUNCOES]
for n in ordem:
    partes.append("\n\n" + seg[n])
novo = open(NOVO, "rb").read().decode("utf-8")
partes.append("\n\n\n" + novo.rstrip("\n") + "\n")
txt = "\n".join(p if p.endswith("\n") else p for p in partes)
txt = txt.replace("\r\n", "\n")
ast.parse(txt)
if os.path.exists(DST) and open(DST, "rb").read().decode("utf-8") != txt and "--refazer" not in sys.argv:
    raise SystemExit("textos_v400.py EXISTE e DIFERE do gerado (editado depois?): nao sobrescrevo sem --refazer")
open(DST + ".tmp", "wb").write(txt.encode("utf-8")); os.replace(DST + ".tmp", DST)
print("textos_v400.py", len(txt.encode("utf-8")), "B, sha16", hashlib.sha256(txt.encode("utf-8")).hexdigest()[:16], "| herdadas:", len(ordem), "funcoes e", len(CONST), "constantes")
