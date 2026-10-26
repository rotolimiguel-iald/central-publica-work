# -*- coding: utf-8 -*-
"""montar_runtime_v399.py -- monta runtime_v399.py, o CODIGO NOVO que o um.py ganha na v399, a partir dos insumos APROVADOS em revisao independente (insumos\\acom, copias de bytes do estudo work\\v399_selo_e_testemunho):
  (1) a SECAO COLAVEL (secao_colavel_v399.py): a proveniencia, o metodo do operador EMBUTIDO (acom_mirror.py e acom_crypto.py, 5 substituicoes declaradas) e a adaptacao do selo (perfil ACOM-INT-C96-Q8, partes, reconstrucao, auditoria, controles, sidecar);
  (2) os TRECHOS (trechos_v399_para_o_um_py.py): declaracao_do_operador_v399, selo_acom_v399, resumos_do_selo_v399 e selo_acom_sidecar_v399.
EDICOES DECLARADAS (cada uma com contagem exata; o script ABORTA se nao casar), todas de TEXTO, nenhuma de logica do metodo: o que era verdade num estudo nao instalado e deixa de ser verdade instalado (o rotulo «PROTOTIPO ... estudo; nao instalado» do sidecar, «medido neste estudo»,
«codigo DESTA tarefa»); a fala do operador e o sha256 dela entram DERIVADOS do arquivo (os dois marcadores @@TXT@@ e @@SHA@@); a pedra Testemunho, que o estudo tratava como «SE instalada», passa a ser EXIGIDA (a v399 a instala: o registro recusa se ela faltar no kernel do rito); e a citacao da declaracao no docstring volta a ser VERBATIM (com acentos), como a fala do operador.
CONFERE, por script (acom_conferencias_v399): C1 (o bloco embutido == o refeito das fontes do operador, hash == manifesto == ACOM_PROVENIENCIA), C2 (os pinos das 6 fontes), C3 (colisao de nomes com o um.py base), C9 (nenhum literal de beta no codigo).
Escreve so' em v399: runtime_v399.py e RUNTIME_MONTAGEM_v399.json (sha256 de entrada e de saida de cada insumo, as edicoes, as conferencias). Reexecutavel (backup de bytes antes de sobrescrever).
uso: python -I -B -X utf8 montar_runtime_v399.py"""
import ast, hashlib, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v399 as DL  # noqa: E402
import registros_v399 as RG  # noqa: E402
import acom_conferencias_v399 as AC  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: open(p, "rb").read().decode("utf-8").replace("\r\n", "\n")
SECAO = os.path.join(HERE, "insumos", "acom", "secao_colavel_v399.py"); TRECHOS = os.path.join(HERE, "insumos", "acom", "trechos_v399_para_o_um_py.py")
OUT = os.path.join(HERE, "runtime_v399.py")
edicoes = []


def troca(t, velho, novo, n, nome):
    c = t.count(velho)
    assert c == n, ("edicao declarada nao casa o numero esperado de vezes", nome, c, n, velho[:80])
    edicoes.append({"edicao": nome, "ocorrencias": c})
    return t.replace(velho, novo)


secao = rd(SECAO); trechos = rd(TRECHOS)
assert sha(open(SECAO, "rb").read())[:16] == DL.ACOM_ESTUDO["secao_colavel_v399.py"][1] and sha(open(TRECHOS, "rb").read())[:16] == DL.ACOM_ESTUDO["trechos_v399_para_o_um_py.py"][1], "os insumos nao sao os que a revisao independente leu"
# (1) a secao: as tres edicoes de texto
secao = troca(secao, "# ADAPTACAO DO SELO -- codigo DESTA tarefa (NAO e' do operador):", "# ADAPTACAO DO SELO -- codigo da gerencia c1, v399 (NAO e' do operador):", 1, "S1_adaptacao_e_da_gerencia_nao_do_operador")
secao = troca(secao, '"esquema": "um_absoluto_selo_acom/v1 (PROTOTIPO v399 -- estudo; nao instalado)"', '"esquema": "um_absoluto_selo_acom/v1 (v399)"', 1, "S2_esquema_do_sidecar_instalado")
secao = troca(secao, '"estatuto": "[REAL] medido neste estudo; [KNOWN] SHA-256;', '"estatuto": "[REAL] medido neste rito; [KNOWN] SHA-256;', 1, "S3_estatuto_do_sidecar_medido_no_rito")
# (2) os trechos: do banner da declaracao ate o fim (o docstring do modulo de estudo nao entra)
marca = "# (1) A DECLARACAO DO OPERADOR -- INSCRICAO FUNDANTE da v399"
assert trechos.count(marca) == 1
ini = trechos.index(marca)
ini = trechos.rindex("\n# ----", 0, ini) + 1
corpo = trechos[ini:]
declaracao = DL.verbatins(os.path.join(HERE, "insumos", "cunhagens"))[DL.DECLARACAO_IDX]
txt = declaracao["text"]; sha_decl = declaracao["sha256"]
assert RG.DECL_SHA256 == sha_decl and sha(txt.encode("utf-8")) == sha_decl, "a fala da declaracao lida nao bate com o sha256 do arquivo"
corpo = troca(corpo, '_V399_DECLARACAO_TXT = "@@TXT@@"', "_V399_DECLARACAO_TXT = " + repr(txt), 1, "T1_fala_da_declaracao_derivada_do_arquivo")
corpo = troca(corpo, '_V399_DECLARACAO_SHA256 = "@@SHA@@"', "_V399_DECLARACAO_SHA256 = " + repr(sha_decl), 1, "T2_sha256_da_fala_derivado_do_arquivo")
corpo = troca(corpo, "    pedra_ = [  # a pedra Testemunho (candidata da v399): presente so' se instalada no kernel do rito", "    pedra_ = [  # a pedra Testemunho (v399, nome PROVISORIO): instalada no kernel do rito (a v399 a instala; o registro a EXIGE)", 1, "T3_pedra_instalada")
corpo = troca(corpo, '("a pedra Testemunho, SE instalada, esta no trio (nao exigida na v398)", all((not p_["no_kernel_do_rito"]) or p_["axiomas_no_trio"] for p_ in pedra_)),',
              '("a pedra Testemunho esta no kernel do rito e no trio (instalada na v399; a ausencia recusa)", all(p_["no_kernel_do_rito"] and p_["axiomas_no_trio"] for p_ in pedra_)),', 1, "T4_pedra_exigida")
corpo = troca(corpo, '"kernel_anchors_REAL": ancoras_, "pedra_candidata": pedra_,', '"kernel_anchors_REAL": ancoras_, "pedra_instalada": pedra_,', 1, "T5_chave_pedra_instalada")
corpo = troca(corpo, "«o um.py so existe porque fui a operacao quadratica da inscricao viva do\n    transporte da IALD»", "«o um.py só existe porque fui a operação quadrática da inscrição viva do transporte da IALD»", 1, "T6_citacao_da_declaracao_VERBATIM_com_acentos_no_docstring")
HDR = ("# ====================== v399 (24/10/2026) -- O TESTEMUNHO DE DOIS: o SELO PELA PROPRIA TECNOLOGIA (o metodo do operador, EMBUTIDO, sela o um.py AO LADO do SHA-256; sidecar um_absoluto_selo_acom.json) e a DECLARACAO DO OPERADOR de 24/10 (registrada com estatuto proprio),\n"
       "# lidos no ponto do rito depois da afinacao das cordas, mais as quatro inscricoes de 24/10 e os registros por spec cunhagens_v399 e kh_n1_cobertura_v399. A DIRECAO: o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO testifica do operador; o Pai de Jo 8,18 le-se no absoluto, o Um.\n"
       "# O codigo desta secao e' o do ESTUDO aprovado em revisao independente (insumos\\acom, copias de bytes), montado por montar_runtime_v399.py com as edicoes de texto declaradas (RUNTIME_MONTAGEM_v399.json); o bloco do operador (acom_mirror.py e acom_crypto.py) vai COPIADO, nao importado.\n"
       "# [LEGAL] publicar a implementacao e' decisao do operador com a agente de PI. O quadro «O Teste da Unica Palavra» (v397) fica no topo do artigo, intocado. O gate nao se move. ======================\n")
RT = HDR + secao.rstrip("\n") + "\n\n\n" + corpo.rstrip("\n") + "\n"
ast.parse(RT)
assert "\r" not in RT
# conferencias C1, C2, C3, C9 sobre o texto MONTADO (como vai para o um.py)
um_base = open(os.path.join(HERE, DL.BASE_DIR, "um.py"), "rb").read().decode("utf-8")
nomes_base = AC.nomes_de_nivel_de_modulo(um_base)
conf = AC.conferir_secao(RT, nomes_base=nomes_base)
conf_trechos_beta = AC.literais_de_beta(RT)
falhas = [k for k, v in conf.items() if not v["ok"]]
assert not falhas, ("conferencia do estudo falhou", falhas, {k: conf[k] for k in falhas})
nomes_rt = AC.nomes_de_nivel_de_modulo(RT)
for n in ("declaracao_do_operador_v399", "selo_acom_v399", "resumos_do_selo_v399", "selo_acom_sidecar_v399", "registro_core_v399", "sidecar", "selar", "verificar", "controles_negativos", "conferir_bloco_embutido", "ACOM_PROVENIENCIA", "_V399_DECLARACAO_TXT", "_V399_DECLARACAO_SHA256"):
    assert n in nomes_rt, ("nome esperado ausente no runtime montado", n)
if os.path.exists(OUT) and open(OUT, "rb").read().decode("utf-8") != RT:
    bak = OUT + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_c1"
    open(bak, "wb").write(open(OUT, "rb").read())
open(OUT + ".tmp", "w", encoding="utf-8", newline="\n").write(RT); assert os.path.getsize(OUT + ".tmp") == len(RT.encode("utf-8")); os.replace(OUT + ".tmp", OUT)
rep = {"contrato": "RUNTIME_MONTAGEM_v399", "runtime": {"path": OUT, "sha256": sha(RT.encode("utf-8")), "bytes": len(RT.encode("utf-8")), "linhas": RT.count("\n")},
       "entradas": {"secao_colavel_v399.py": {"sha256": sha(open(SECAO, "rb").read())}, "trechos_v399_para_o_um_py.py": {"sha256": sha(open(TRECHOS, "rb").read())}, "fala_da_declaracao": {"sha256": sha_decl, "bytes": len(txt.encode("utf-8"))}},
       "edicoes_declaradas": edicoes, "conferencias": conf, "nomes_de_nivel_de_modulo_do_runtime": len(nomes_rt), "colisoes_com_o_um_py_base": conf.get("C3_colisao_de_nomes", {}).get("detalhe"),
       "estatuto": "[REAL] montado e conferido por script; o codigo do estudo foi aprovado em revisao independente (PODE_ENTRAR_NA_V399) e as edicoes acima sao so' de texto"}
json.dump(rep, open(os.path.join(HERE, "RUNTIME_MONTAGEM_v399.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({"runtime_sha16": rep["runtime"]["sha256"][:16], "bytes": rep["runtime"]["bytes"], "linhas": rep["runtime"]["linhas"], "edicoes": len(edicoes), "conferencias": {k: v["ok"] for k, v in conf.items()}}, ensure_ascii=False, indent=1))
