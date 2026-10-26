# -*- coding: utf-8 -*-
"""acom_conferencias_v400.py -- as CONFERENCIAS da cadeia sobre a SECAO do selo pela propria tecnologia (runtime_v400.py), todas por script. Reaproveita (import por caminho) as da v399 -- C1 (o bloco embutido == o refeito das
fontes do operador, hash == manifesto == ACOM_PROVENIENCIA), C2 (os pinos das seis fontes), C3 (colisao de nomes com o um.py base) e C9 (nenhum literal de beta no codigo) -- e ACRESCENTA:
 C3' (v400, mais estreita que a da v399): a secao NAO define o nome ALPHA_FINE_CODATA_2018 (a v399 o definia, e a colisao era «permitida»; foi a v399 que a Bancada recusou);
 C10 (alfa unico): nenhuma linha da secao casa as regexes da guarda ALPHA_LINHA_UNICA da Bancada (lidas do PROPRIO esboco R3.5 pinado, nao copiadas), a secao LE o alfa do programa (SEALED_CODATA_ALPHA) e nenhum literal numerico
 igual ao alfa CODATA aparece no codigo da secao (tokenize; comentarios e prosa ficam fora);
 C11 (o bloco do operador NAO mudou): o hash do bloco embutido da secao v400 == o da v399 (a correcao e' da ADAPTACAO, que fica antes do primeiro marcador; o bloco continua sendo as fontes do operador + as 5 substituicoes declaradas).
Importado por montar_runtime_v400, gerar_candidato_v400, p00_precondicoes_v400, ensaio_a_seco_v400 e conferir_rito_v400."""
import hashlib, importlib.util, io, os, re, sys, tokenize

HERE = os.path.dirname(os.path.abspath(__file__))
V399 = os.path.join(os.path.dirname(HERE), "v399")
_spec = importlib.util.spec_from_file_location("acom_conferencias_v399", os.path.join(V399, "acom_conferencias_v399.py"))
A9 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(A9)
sha = A9.sha
lf = A9.lf
extrair_bloco = A9.extrair_bloco
proveniencia = A9.proveniencia
nomes_de_nivel_de_modulo = A9.nomes_de_nivel_de_modulo
literais_de_beta = A9.literais_de_beta
bloco_das_fontes = A9.bloco_das_fontes
ALFA_CODATA = 0.0072973525693      # o dado CODATA 2018 (so' para PROCURAR o literal na secao; nao e' usado como valor)


_ESBOCOS = {}


def esboco_da_bancada(esboco_path, esboco_sha256=None):
    """O esboco R3.5 da Bancada (sincronizar_bancada.py), IMPORTADO do arquivo pinado (nao copiado): as regexes e as funcoes da guarda sao as DELE. Confere o sha256 antes; o import so' define nomes
    (o main nao roda; a guarda de interpretador so' vale como __main__)."""
    raw = open(esboco_path, "rb").read()
    h = hashlib.sha256(raw).hexdigest()
    if esboco_sha256 is not None:
        assert h == esboco_sha256, ("o esboco em disco nao e' o pinado", h[:16], esboco_sha256[:16])
    if h not in _ESBOCOS:
        spec = importlib.util.spec_from_file_location("sincronizar_bancada_r35_" + h[:12], esboco_path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod
        spec.loader.exec_module(mod)
        _ESBOCOS[h] = mod
    return _ESBOCOS[h]


def regexes_da_bancada(esboco_path, esboco_sha256=None):
    """As regexes da guarda de alfa/versao do esboco R3.5, LIDAS do proprio esboco pinado (objetos compilados dele): a regra e' a da Bancada, nao a minha."""
    mod = esboco_da_bancada(esboco_path, esboco_sha256)
    return {n: getattr(mod, n) for n in ("RE_ALPHA_LINHAS", "RE_ALPHA_INDENTADA", "RE_VERSAO_LINHAS", "RE_VERSAO_INDENTADA", "RE_ALPHA", "RE_VERSAO")}


def conferir_alfa_unico(secao_texto, regexes):
    """C3' + C10 sobre o texto da secao (como vai para o um.py)."""
    nomes = nomes_de_nivel_de_modulo(secao_texto)
    linhas_alfa = regexes["RE_ALPHA_LINHAS"].findall(secao_texto)
    ind = regexes["RE_ALPHA_INDENTADA"].findall(secao_texto)
    ruins = []
    for tk in tokenize.generate_tokens(io.StringIO(secao_texto).readline):
        if tk.type == tokenize.NUMBER:
            try:
                v = float(tk.string.replace("_", ""))
            except ValueError:
                continue
            if abs(v - ALFA_CODATA) < 1e-15:
                ruins.append((tk.start[0], tk.string))
    usa_o_do_programa = bool(re.search(r"\bSEALED_CODATA_ALPHA\b", secao_texto))
    return {
        "C3p_a_secao_nao_define_ALPHA_FINE_CODATA_2018": {"ok": "ALPHA_FINE_CODATA_2018" not in nomes, "detalhe": {"nomes_de_nivel_de_modulo": len(nomes)}},
        "C10_alfa_unico": {"ok": (not linhas_alfa) and (not ind) and (not ruins) and usa_o_do_programa,
                           "detalhe": {"linhas_nao_indentadas_de_alfa": len(linhas_alfa), "linhas_indentadas_de_alfa": len(ind), "literais_de_alfa_no_codigo": ruins[:3], "le_SEALED_CODATA_ALPHA": usa_o_do_programa}},
    }


def conferir_secao(secao_texto, nomes_base=None, regexes=None, bloco_v399_sha256=None):
    """C1, C2, C3, C9 (da v399, sobre o texto v400) + C3', C10 e C11. Devolve {id: {ok, detalhe}}; nada levanta (o chamador decide)."""
    R = A9.conferir_secao(secao_texto, nomes_base=nomes_base)
    if regexes is not None:
        R.update(conferir_alfa_unico(secao_texto, regexes))
    if bloco_v399_sha256 is not None:
        b = extrair_bloco(secao_texto)
        R["C11_o_bloco_do_operador_nao_mudou"] = {"ok": sha(b.encode("utf-8")) == bloco_v399_sha256, "detalhe": {"sha256_do_bloco_v400": sha(b.encode("utf-8"))[:16], "sha256_do_bloco_v399": bloco_v399_sha256[:16]}}
    return R
