# -*- coding: utf-8 -*-
"""_adapt_d74_ratificacao_v410.py -- RETOMADA de 09/11/2026 (claude-construtor-v410): a VARREDURA da D74 (licao da v409: varrer, nao remendar) nos textos da gerencia desta cadeia: onde dizia «[DECLARADO] ate a ratificacao (D63)»
passa a dizer que os nomes das declaracoes foram RATIFICADOS pelo operador em 09/11/2026 (D74); as docstrings da PEDRA nao mudam (dizem [DECLARADO] ate a ratificacao, verdade da epoca). Arquivos: runtime_v410.py, registros_v410.py,
artigo_pt_v410.pysnip, artigo_en_v410.pysnip (o gerador e' adaptado por _adapt_h0dn_gerador_v410.py; o pos-rito, pelo agente dos textos). Backup de bytes; cada troca com a contagem conferida; ast.parse."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def troca(nome, trocas, parse="py"):
    P = os.path.join(HERE, nome); b0 = open(P, "rb").read(); assert b0.count(b"\r\n") == 0
    bk = P + ".bak_" + TS + "_d74"; open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
    t = b0.decode("utf-8")
    for v, n, k in trocas:
        c = t.count(v); assert c == k, (nome, c, v[:110]); t = t.replace(v, n)
    nb = t.encode("utf-8")
    ast.parse(nb) if parse == "py" else ast.parse(b"def _f(core, verdict, data_path, s):\n" + nb)
    tmp = P + ".tmp_" + TS; open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb); os.replace(tmp, P)
    print(nome, "(D74):", len(b0), "->", len(nb), hashlib.sha256(nb).hexdigest()[:16], "| trocas", len(trocas))


RAT = "RATIFICADOS pelo operador em 09/11/2026 (D74; as docstrings da pedra, da epoca, dizem [DECLARADO] ate a ratificacao)"
troca("runtime_v410.py", [
    ("o NOME do modulo e' do operador, 06/11; os nomes das declaracoes sao da gerencia, [DECLARADO] ate a ratificacao, D63)",
     "o NOME do modulo e' do operador, 06/11; os nomes das declaracoes sao da gerencia, " + RAT + ")", 1),
])
troca("registros_v410.py", [
    ("(gerencia c1, 06/11/2026; o NOME do modulo e' do operador; os nomes das declaracoes sao da gerencia, [DECLARADO] ate a ratificacao, D63):",
     "(gerencia c1, 06/11/2026; o NOME do modulo e' do operador; os nomes das declaracoes sao da gerencia, " + RAT + "):", 1),
    ("\"[DECLARADO] os nomes das declaracoes (da gerencia, ate a ratificacao) e os recibos de compilacao;",
     "\"[INPUT] os nomes das declaracoes, da gerencia, " + RAT + "; [DECLARADO] os recibos de compilacao;", 1),
    ("IALD2 (o NOME do modulo e' do operador, 06/11/2026; os nomes das declaracoes sao da gerencia, [DECLARADO] ate a ratificacao, D63). \"",
     "IALD2 (o NOME do modulo e' do operador, 06/11/2026; os nomes das declaracoes sao da gerencia, " + RAT + "). \"", 1),
    ("o NOME do modulo e' do operador e os nomes das declaracoes sao da gerencia, [DECLARADO] ate a ratificacao (D63)\",",
     "o NOME do modulo e' do operador e os nomes das declaracoes sao da gerencia, " + RAT + "\",", 1),
    ("THE_MODULE_NAME_IALD2_GIVEN_BY_THE_OPERATOR__THE_DECLARATION_NAMES_DECLARED_UNTIL_RATIFICATION__DECISIONS_D63_TO_D71__",
     "THE_MODULE_NAME_IALD2_GIVEN_BY_THE_OPERATOR__THE_DECLARATION_NAMES_RATIFIED_BY_THE_OPERATOR_ON_09_NOV__DECISIONS_D63_TO_D76__ERRATUM_E30_BESIDE__", 1),
    ("a IALD e o seletor; o atrator, 07/11; a ORDEM da retomada, 09/11, so' o trecho); DECLARADO os nomes das declaracoes e os recibos de compilacao; KNOWN as referencias do alcance]\",",
     "a IALD e o seletor; o atrator, 07/11; a ORDEM da retomada, 09/11, so' o trecho; as decisoes de 09/11 e a ratificacao dos nomes, D74; as tres copias do ACOM, 08/11, so' o trecho; a leitura do 5 sigma e o selo, 09/11; "
     "os nomes das declaracoes RATIFICADOS em 09/11, D74); DECLARADO os recibos de compilacao; KNOWN as referencias do alcance]\",", 1),
    ("                    \"[INPUT] \" + DL.NOMES_DAS_PEDRAS[\"IALD2\"] + \" (D63)\",",
     "                    \"[INPUT] \" + DL.NOMES_DAS_PEDRAS[\"IALD2\"] + \" (D63; D74)\",", 1),
])
troca("artigo_pt_v410.pysnip", [
    ("(IALD2; o NOME do módulo é do operador, 06/11; os nomes das declarações são da gerência, [DECLARADO] até a ratificação, D63);",
     "(IALD2; o NOME do módulo é do operador, 06/11; os nomes das declarações são da gerência, ratificados pelo operador em 09/11/2026, D74);", 1),
    ("(o nome do módulo é do operador; os nomes das declarações são da gerência e ficam \\textsf{[DECLARADO]} até a ratificação), com ",
     "(o nome do módulo é do operador; os nomes das declarações são da gerência, ratificados pelo operador em 09/11/2026: «os nomes dos teoremas ratifico-os todos», D74; as docstrings da pedra, da época, dizem \\textsf{[DECLARADO]} até a ratificação), com ", 1),
], parse="snip")
troca("artigo_en_v410.pysnip", [
    ("(IALD2; the NAME of the module is the operator's, 06/11; the names of the declarations are the management's, [DECLARADO] until ratification, D63);",
     "(IALD2; the NAME of the module is the operator's, 06/11; the names of the declarations are the management's, ratified by the operator on 09/11/2026, D74);", 1),
    ("(the name of the module is the operator's; the names of the declarations are the management's and stay \\textsf{[DECLARADO]} until ratification), with ",
     "(the name of the module is the operator's; the names of the declarations are the management's, ratified by the operator on 09/11/2026 (our translation: the names of the theorems, I ratify them all; D74); the docstrings of the stone, of their time, say \\textsf{[DECLARADO]} until ratification), with ", 1),
], parse="snip")
