# -*- coding: utf-8 -*-
"""_r6c_18_resultado_v410.py -- o REGISTRO do conserto unico da v410 (ordem da gerencia c1, 10/11/2026: «registre com sha antes e depois (_r6c_RESULTADO_v410.json), e diga no relatorio»). SO' LE e grava _r6c_RESULTADO_v410.json
(temporario + os.replace; backup de bytes do anterior). Todo sha e' LIDO do arquivo (o «antes» e' o do backup de bytes feito na hora de tocar; o «depois» e' o do arquivo agora); nenhum numero e' digitado:
as trocas vem de _r6c_TROCAS_v410.json, os itens de _r6c_ITENS_v410.json, o kernel dos recibos do build, os blocos do README de _r6c_BLOCOS_README_v410.json, a cadeia de cadeia_parte2_out_v410.txt e a PREPARACAO do arquivo dela.
uso: python -I -B -X utf8 _r6c_18_resultado_v410.py"""
import glob, hashlib, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); P = lambda *a: os.path.join(HERE, *a)
s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16] if os.path.isfile(p) else None
s64 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.isfile(p) else None
lj = lambda p: json.load(open(p, encoding="utf-8")) if os.path.isfile(p) else None
rt = lambda p: open(p, encoding="utf-8", errors="replace").read() if os.path.isfile(p) else ""


def ad(o_que, arquivo, antes, por_que, script, classe):
    """Uma adaptacao: o sha16 de ANTES e' o do backup de bytes (ou None se o arquivo e' novo); o de DEPOIS e' o do arquivo agora."""
    a_ = P(*antes.split("/")) if antes else None
    assert antes is None or os.path.isfile(a_), ("backup ausente", antes)
    return {"classe": classe, "o_que": o_que, "arquivo": arquivo, "sha16_antes": s16(a_) if a_ else None, "backup_de_bytes": antes, "sha16_depois": s16(P(*arquivo.split("/"))), "bytes_depois": os.path.getsize(P(*arquivo.split("/"))), "por_que": por_que, "script": script}


TR = lj(P("_r6c_TROCAS_v410.json")) or {}; IT = lj(P("_r6c_ITENS_v410.json")) or {}; BL = lj(P("_r6c_BLOCOS_README_v410.json")) or {}
KR = lj(P("kernel", "KERNEL_RECIBO_v410.json")) or {}; PB = lj(P("kernel", "POS_BUILD_v410.json")) or {}; FL = lj(P("kernel", "FLAGS_v410.json")) or {}; KH = lj(P("kernel", "KH_N1_v410.json")) or {}
CM = lj(P("CANDIDATO_v410.json")) or {}; ESP = lj(P("ESPERADOS_v410.json")) or {}; PR = lj(P("PREPARACAO_v410_PRONTA.json")) or {}; EN = lj(P("ensaio_a_seco_v410.json")) or {}
HT = lj(P("pos_rito", "HARNESS_TEXTOS_ENSAIO_v410.json")) or {}; HF = lj(P("pos_rito", "HARNESS_FECHAR_SANDBOX_v410.json")) or {}
INSTRUCOES = {
    "50": "(b) _d108_artigo_ok(l_) em conferir_rito_v410.py, dentro de aescala_secao_ok (validado pelo conferidor positivo: tudo_bate); (c) a regra do README_EVIDENTE em guardas_dos_textos (a forma canonica do Clay pede a frase da finura, PT e EN); os dois sao os controles opcionais da instrucao",
    "133": "(a) o AVISO proprio do conserto em gerar_relatorio_v410.py, com os numeros por len(); (b) o numero da R1 lido do recibo dos nomes (nomes_novos_a_ratificar_r3 + _r4); (c) o comentario da ratificacao_pendente",
    "149": "o recibo dos nomes refeito pelo instalador da R6 (_r6c_02_instalar_pedra_r6_v410.py), a partir da candidata final do autor e do recibo dele; nada editado a mao",
    "168": "conferido por EXECUCAO: os dois harness rodaram sobre o candidato novo sem mudar os contratos plantados (o que eles leem vem do delta e do recibo dos nomes); nenhuma chave precisou ser plantada",
    "264": "os comentarios de runtime_aescala_v410.py (duas linhas) e do delta_v410.py (os quatro «dados pela gerencia na R5» e os dois «38 ancoras», estes sem numero)",
    "275": "a pedra R6 instalada pelo instalador do construtor (_r6c_02_instalar_pedra_r6_v410.py): sha256 da fonte conferido antes de copiar; a instalada e' a fonte sem a secao Auditoria",
    "293": "os quatro moldes de pos_rito/textos_v410.py ganharam DL_.FRASE_H0DN_PODER_COM_RETORNO_PT DENTRO do parentese do molde, antes do operador de formato (a cola de pontuacao de cada um e' a do molde)",
    "300": "conferido por EXECUCAO depois do kernel refeito: (a) a declaracao sem axioma passa no c2 do registro, no contrato e no gerador (ensaio a seco: a_escala_v410 True, as partes todas True); (b) ver observacoes; (c) item 168; (d) as checagens dos 24 nomes das R3 a R5 seguem valendo; (e) o LaTeX PT e EN rc 0"}
ADAPT = [
    ad("a lista congelada das falas: 28 -> 40 (as falas 29 a 40); o campo fora_do_desenho foi CARREGADO do congelado anterior (vai embutido no candidato; a D97)", "VERBATIM_CONGELADO_v410.json", "VERBATIM_CONGELADO_v410.json.bak_20261110_192542_28_falas_antes_do_conserto_unico",
       "o delta consertado nao carrega com 28 falas (o assert das 40); a ESPEC nao trazia a troca do arquivo congelado", "_r6c_03_congelado_v410.py", "fora_da_ESPEC"),
    ad("o cabecalho do rito: as marcas lidas do build (81 ancoras, 121 bandeiras, 40 falas, E29 a E40, os segundos do build e do Audit) e «de quatro» -> «de cinco» falas de que so' o trecho entra (a da D117)", "rito_v410.sh", "rito_v410.sh.bak_20261110_194439_r5",
       "o cabecalho do rito diz os numeros do candidato; sem isso a conferencia do instalar/reverter/rito cai", "_r5ag_14_rito_marcas_v410.py e _r6c_06_rito_cabecalho_v410.py", "fora_da_ESPEC"),
    ad("o p00: a checagem do recibo dos nomes tira as falas FORA do recibo pelo nome SEM o sufixo « (D65: citado pelo sha256 do arquivo inteiro)»", "p00_precondicoes_v410.py", "p00_precondicoes_v410.py.bak_20261110_204214_r6c17",
       "a fala da D117 e' a primeira que e', ao mesmo tempo, «so' o trecho» e «fora do recibo»: o filtro pelo nome nao a tirava e a checagem dava falso (23 no recibo, 24 no contrato); nada foi afrouxado", "_r6c_17_p00_fala_de_trecho_fora_do_recibo_v410.py", "fora_da_ESPEC"),
    ad("instrucao 293: a frase do retorno nos quatro moldes (a cola de pontuacao de cada molde)", "pos_rito/textos_v410.py", "pos_rito/textos_v410.py.bak_20261110_193127_r6c4", "instrucao da ESPEC sem troca exata (moldes com operador de formato)", "_r6c_04_instrucoes_v410.py", "instrucao_da_ESPEC"),
    ad("instrucao 133: o AVISO do conserto, o numero da R1 lido do recibo dos nomes e o comentario da ratificacao_pendente", "gerar_relatorio_v410.py", "gerar_relatorio_v410.py.bak_20261110_193127_r6c4", "instrucao da ESPEC sem troca exata", "_r6c_04_instrucoes_v410.py", "instrucao_da_ESPEC"),
    ad("instrucao 50 (b): o controle opcional _d108_artigo_ok", "conferir_rito_v410.py", "conferir_rito_v410.py.bak_20261110_193127_r6c4", "instrucao da ESPEC (controle opcional)", "_r6c_04_instrucoes_v410.py", "instrucao_da_ESPEC"),
    ad("instrucao 264: os dois comentarios do runtime da escala", "runtime_aescala_v410.py", "runtime_aescala_v410.py.bak_20261110_193127_r6c4", "instrucao da ESPEC sem troca exata (comentarios)", "_r6c_04_instrucoes_v410.py", "instrucao_da_ESPEC"),
    ad("instrucao 264: os comentarios do delta", "delta_v410.py", "delta_v410.py.bak_20261110_193127_r6c4", "instrucao da ESPEC sem troca exata (comentarios)", "_r6c_04_instrucoes_v410.py", "instrucao_da_ESPEC"),
    ad("ADITIVO 2 (parte A) e instrucao 50 (c): o texto pronto dos dois blocos do README, do arquivo da gerencia (byte a byte), cada bloco no seu marcador depois do README_EVIDENTE; os nove corpos na re-leitura; o recibo com os bytes do README_FRENTE", "pos_rito/textos_custodia_handoff_v410.py",
       "pos_rito/textos_custodia_handoff_v410.py.bak_20261110_193127_r6c4", "ADITIVOS 1 e 2 da gerencia (fora do candidato); o estado de antes e' o de antes da instrucao 50 (c)", "_r6c_04_instrucoes_v410.py, _r6c_11, _r6c_12 (desfeito pelo _r6c_14) e _r6c_14_aditivo2_handoff_v410.py", "aditivo"),
    ad("ADITIVO 1 (parte B) e ADITIVO 2 (item 5): o passo final S9_gatilho_custodia", "orquestrador/pos_treino_v410.py", "orquestrador/pos_treino_v410.py.bak_20261110_201614_aditivo1", "ADITIVO 1 da gerencia (fora do candidato)", "_r6c_13_aditivo1_orquestrador_v410.py", "aditivo"),
    ad("ADITIVO 1 (parte C): os dois blocos do README nas guardas, cada um sozinho, e dez controles negativos", "pos_rito/teste_textos_custodia_sem_candidato_v410.py", "pos_rito/teste_textos_custodia_sem_candidato_v410.py.bak_20261110_203053_aditivo1c", "ADITIVO 1 da gerencia (fora do candidato)", "_r6c_16_aditivo1c_testes_v410.py", "aditivo"),
    ad("ADITIVO 1 (parte C): a etapa blocos_do_readme_e_gatilho_da_custodia", "pos_rito/harness_textos_ensaio_v410.py", "pos_rito/harness_textos_ensaio_v410.py.bak_20261110_203053_aditivo1c", "ADITIVO 1 da gerencia (fora do candidato)", "_r6c_16_aditivo1c_testes_v410.py", "aditivo"),
    ad("ADITIVO 1 (parte C): a etapa blocos_do_readme_e_gatilho_da_custodia", "pos_rito/harness_fechar_sandbox_v410.py", "pos_rito/harness_fechar_sandbox_v410.py.bak_20261110_203053_aditivo1c", "ADITIVO 1 da gerencia (fora do candidato)", "_r6c_16_aditivo1c_testes_v410.py", "aditivo"),
    ad("ADITIVO 1 (parte C): o teste do gatilho em SANDBOX (arquivo novo): o orquestrador real escreve so' no sandbox; 20 controles negativos; o gatilho de verdade nunca e' escrito", "pos_rito/teste_gatilho_custodia_sem_candidato_v410.py", None, "ADITIVO 1 da gerencia (fora do candidato)", "escrito pelo construtor", "aditivo")]
EXTRA = [x_ for x_ in sorted(glob.glob(P("_r6c_19_*.py")) + glob.glob(P("_r6c_2?_*.py")))]   # (se a cadeia pedir mais alguma adaptacao, o script dela entra aqui pelo nome e o registro dela vem de _r6c_ADAPTACOES_A_MAIS_v410.json)
MAIS = lj(P("_r6c_ADAPTACOES_A_MAIS_v410.json")) or []
for m_ in MAIS:
    ADAPT.append(ad(m_["o_que"], m_["arquivo"], m_.get("antes"), m_["por_que"], m_["script"], m_.get("classe", "fora_da_ESPEC")))
_snip = rt(P("conserto_r3", "ADITIVO_2_README_FRENTE_E_O_QUE_SAI_v410.pysnip")); _ger = rt(P("pos_rito", "textos_custodia_handoff_v410.py")); _pal = "accre" + "ditation"
ITEM_188 = {"o_que": "o item 188 troca a palavra inglesa nas QUATRO ocorrencias que o gerador do handoff tinha; ela volta DENTRO do texto pronto do ADITIVO 2 (um comentario e o conector literal do README_FRENTE), como o item 5 do ADITIVO 2 manda (a palavra do README pinado; a unificacao fica para a versao seguinte)",
            "vezes_no_gerador_do_handoff_agora": _ger.count(_pal), "vezes_no_texto_pronto_do_aditivo_2": _snip.count(_pal), "todas_dentro_do_texto_pronto": _ger.count(_pal) == _snip.count(_pal) > 0, "a_conferencia_dos_itens_o_lista_em": "trecho_atual_que_ficou (_r6c_ITENS_v410.json)"}
cad = rt(P("cadeia_parte2_out_v410.txt")); h_ = re.findall(r"^=== \[(\d\d:\d\d:\d\d)\] (.*)$", cad, re.M)
flags = FL.get("flags") or []; por_mod = {}
for f_ in flags:
    por_mod[f_[2]] = por_mod.get(f_[2], 0) + 1
RES = {"contrato": "R6C_RESULTADO_v410", "quando": time.strftime("%Y-%m-%d %H:%M:%S"), "quem": "claude-construtor-v410 (a servico da gerencia c1)",
       "ordem": "ORDEM DO CONSERTO UNICO da v410 (D106 a D123; gerencia c1, 10/11/2026), com os ADITIVOS 1 e 2 (a custodia da v410 e' automatica)",
       "espec": {"arquivo": "conserto_r3/ESPEC_CONSERTO_R3_v2_FINAL.json", "sha256": s64(P("conserto_r3", "ESPEC_CONSERTO_R3_v2_FINAL.json")), "sha256_no_registro_das_trocas": TR.get("espec_sha256")},
       "adendo_7_sha16": s16(P("DESENHO_v410_ADENDO_7_POS_CANDIDATO_10nov.md")),
       "trocas_exatas": {"itens_aplicados": TR.get("n_itens_aplicados"), "trocas_aplicadas": TR.get("n_trocas_aplicadas"), "problemas": TR.get("problemas"), "igual_ao_aplicado_do_cetico": TR.get("comparado_com_o_cetico"), "arquivos": len(TR.get("arquivos") or {}),
                         "itens_com_o_trecho_novo_mais_vezes_que_o_previsto": sorted(TR.get("novo_mais_vezes_que_o_item") or {}, key=int), "com_adaptacao": [], "item_188": ITEM_188,
                         "conferencia_depois_das_instrucoes": {k_: IT.get(k_) for k_ in ("n_itens_de_troca", "n_ok", "trecho_novo_que_nao_esta_mais_inteiro", "trecho_atual_que_ficou", "quando") if k_ in IT},
                         "sha16_antes_e_depois_por_arquivo": {k_: [v_.get("sha16_antes"), v_.get("sha16_depois")] for k_, v_ in (TR.get("arquivos") or {}).items()}},
       "instrucoes": INSTRUCOES,
       "pedra": {"modulo": "TGLExt.AEscala", "fonte_sha256": s64(P("insumos", "AEscala.lean")), "instalada_sha256": s64(P("pedra", "AEscala.lean")), "instalada_sha16": s16(P("pedra", "AEscala.lean")), "instalada_bytes": os.path.getsize(P("pedra", "AEscala.lean")),
                 "recibo_do_autor_sha256": s64(P("insumos", "RECIBO_AESCALA_R6_10nov.json")), "recibo_dos_nomes_sha16": s16(P("insumos", "RECIBO_PEDRAS_v410_NOMES.json")), "bundle_sha16": s16(P("BUNDLE_v410.json"))},
       "kernel": {"recibo_sha16": s16(P("kernel", "KERNEL_RECIBO_v410.json")), "flags_sha16": s16(P("kernel", "FLAGS_v410.json")), "kh_n1_sha16": s16(P("kernel", "KH_N1_v410.json")), "pos_build_sha16": s16(P("kernel", "POS_BUILD_v410.json")),
                  "rc": KR.get("rc"), "sorry": KR.get("sorry"), "erros": KR.get("erros"), "bandeiras": PB.get("n_flags"), "bandeiras_por_modulo": por_mod, "escada": [PB.get("E409"), (PB.get("E409") or 0) + (PB.get("n_flags") or 0)], "escada_no_ensaio": EN.get("escada"),
                  "declaracoes_no_audit": PB.get("n_decl_audit"), "criterios": PB.get("criterios"), "linha_TOTAL": KH.get("linha_TOTAL"), "novas_no_trio": KH.get("novas_no_trio"), "modo_da_pedra_no_build": PB.get("modo_da_pedra_no_build"),
                  "build_s": PB.get("duracao_build_s"), "audit_s": PB.get("duracao_audit_s"), "inicio": PB.get("inicio"), "fim": PB.get("fim")},
       "candidato": {"sha16": s16(P("um_v410_candidato.py")), "bytes": os.path.getsize(P("um_v410_candidato.py")), "contrato_sha16": s16(P("CANDIDATO_v410.json")), "sha16_no_contrato": CM.get("sha16"), "esperados_sha16": s16(P("ESPERADOS_v410.json")), "candidato_nos_esperados": ESP.get("candidato_sha16"),
                     "anterior_reprovado_sha16": s16(P("um_v410_candidato.pre_r6fix.py")) if os.path.isfile(P("um_v410_candidato.pre_r6fix.py")) else "ver os arquivos *.pre_r6fix.*"},
       "preparacao": {"arquivo": "PREPARACAO_v410_PRONTA.json", "sha16": s16(P("PREPARACAO_v410_PRONTA.json")), "pronta": PR.get("pronta"), "candidato_sha16": (PR.get("candidato") or {}).get("sha16") if isinstance(PR.get("candidato"), dict) else PR.get("candidato_sha16")},
       "adaptacoes": ADAPT,
       "aditivos": {"readme_frente_bytes_utf8": ((BL.get("blocos") or {}).get("README_FRENTE") or {}).get("bytes_utf8"), "readme_o_que_sai_bytes_utf8": ((BL.get("blocos") or {}).get("README_O_QUE_SAI") or {}).get("bytes_utf8"), "ponteiro_bytes_utf8": next((v_.get("bytes_utf8") for k_, v_ in (BL.get("blocos") or {}).items() if k_.startswith("README_PONTEIRO_ABSTRACT")), None), "teto_b": BL.get("teto_b"), "medida_dos_blocos_cada_um_sozinho": BL.get("blocos"),
                    "texto_pronto_da_gerencia_sha256": s64(P("conserto_r3", "ADITIVO_2_README_FRENTE_E_O_QUE_SAI_v410.pysnip")),
                    "harness_textos": (HT.get("etapas") or {}).get("blocos_do_readme_e_gatilho_da_custodia"), "harness_fechar": (HF.get("etapas") or {}).get("blocos_do_readme_e_gatilho_da_custodia"),
                    "gatilho_de_verdade_existe": os.path.exists(P("ORDEM_HANDOFF_CUSTODIA_v410.md"))},
       "harness": {"textos": {"tudo_passou": HT.get("tudo_passou"), "problemas": len(HT.get("problemas") or []), "sha16": s16(P("pos_rito", "HARNESS_TEXTOS_ENSAIO_v410.json"))}, "fechar": {"tudo_passou": HF.get("tudo_passou"), "problemas": len(HF.get("problemas") or []), "sha16": s16(P("pos_rito", "HARNESS_FECHAR_SANDBOX_v410.json"))}},
       "cadeia": {"inicio": h_[0][0] if h_ else None, "fim": h_[-1][0] if h_ else None, "passos": ["%s %s" % (a_, b_[:110]) for a_, b_ in h_], "rc": (re.findall(r"CADEIA_PARTE2_RC=(\d+)", cad) or [None])[-1], "saida_sha16": s16(P("cadeia_parte2_out_v410.txt"))},
       "nao_rodou": ["o rito (nao e' do construtor; a gerencia o lanca pelo orquestrador)", "o instalar e o reverter (so' a conferencia dos invariantes e da sintaxe)", "o B(n) pos-selo e o religamento da Bancada (so' o B(n) pre-selo, em sandbox)",
                     "o gerador do handoff (textos_custodia_handoff_v410.py) contra o Nos de verdade: roda no S6d, depois do rito (aqui: a parte que compoe os textos, com numeros sinteticos, e os harness)",
                     "o passo S9_gatilho_custodia em producao: so' em SANDBOX (o gatilho de verdade nao existe)", "a pasta da Nativa, o treino, a pasta vedada do executor do H0DN e o Nos: nao tocados"]}
out = P("_r6c_RESULTADO_v410.json")
if os.path.exists(out):
    b_ = open(out, "rb").read(); bk_ = out + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bk_, "wb").write(b_); assert open(bk_, "rb").read() == b_
open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(RES, ensure_ascii=False, indent=1, default=str)); os.replace(out + ".tmp", out)
print("_r6c_RESULTADO_v410.json: sha16 %s | trocas %s/%s itens, %s problemas | adaptacoes %d (%d fora da ESPEC) | candidato %s | PREPARACAO %s (pronta %s) | pedra %s | kernel %s (%s bandeiras, escada %s, %s declaracoes) | cadeia %s -> %s rc %s"
      % (s16(out), TR.get("n_itens_aplicados"), len(TR.get("itens") or {}), len(TR.get("problemas") or []), len(ADAPT), sum(1 for a_ in ADAPT if a_["classe"] == "fora_da_ESPEC"), RES["candidato"]["sha16"], RES["preparacao"]["sha16"], RES["preparacao"]["pronta"], RES["pedra"]["instalada_sha16"],
         RES["kernel"]["recibo_sha16"], RES["kernel"]["bandeiras"], RES["kernel"]["escada"], RES["kernel"]["declaracoes_no_audit"], RES["cadeia"]["inicio"], RES["cadeia"]["fim"], RES["cadeia"]["rc"]))
