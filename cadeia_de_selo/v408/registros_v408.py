# -*- coding: utf-8 -*-
"""registros_v408.py -- os dados dos registros da v408: FONTES pinadas por sha256 (lidas do disco pelo montador, nunca digitadas), VERBATINS (as falas do operador de 04/11/2026, EMBUTIDAS: a fala embutida manda, o arquivo e' so' informativo; nas duas de autor misto so' o paragrafo do operador),
o CONTRATO e o TEXTO do registro com FUNCAO tetelestai_terminal_v408 (gerar_candidato_v408.py os emite a partir de runtime_v408.py; o contrato sai de contrato() abaixo, DERIVADO do build do sandbox k408c) e os DOIS SPECS interpretados pelo MOTOR _v392_registro
(`cunhagens_v408` e `kh_n1_cobertura_v408`). A MOLDURA de todo texto daqui: o terminal e' a leitura, nao o fim do decaimento; nao ha' relacao sem peso; o tempo e' a moeda de beta; o zero inscrito e' o Um e o Um nao e' o zero absoluto; «P = nP» so' no sentido do operador; nenhuma chave antiga muda;
validade no kernel nao e' creditacao; o gate nao se move. Fontes so' em pasta DURAVEL: tudo vem de cadeia_de_selo\\v408\\insumos. Texto novo passa pela guarda P18 e pela guarda das frases (v408) a cada rito. Molde: registros_v407.py."""
import hashlib
import json
import os
import re
import sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v408 as DL  # noqa: E402

INS = os.path.join(HERE, "insumos")
ASSINA = DL.ASSINA
_snake = lambda s: re.sub(r"(?<!^)(?=[A-Z])", "_", re.sub(r"NP$", "Np", s)).lower()
CHAVE_PEDRA = {p["name"]: "pedra_" + _snake(p["name"]) for p in DL.PEDRAS_V408}              # a pedra normalizada EMBUTIDA no kernel (copia duravel: insumos\<Nome>_embutida.lean)
CHAVE_FONTE = {p["name"]: "fonte_" + _snake(p["name"]) + "_04nov" for p in DL.PEDRAS_V408}   # a fonte normalizada da gerencia, com os #print axioms (insumos\<Nome>.lean: as ancoras saem dela)
CHAVE_SAIDA_FONTE = {p["name"]: "saida_lean_" + _snake(p["name"]) + "_04nov" for p in DL.PEDRAS_V408}   # a saida do lean ao compilar a fonte normalizada no sandbox da v407
CHAVE_TESTEMUNHA = CHAVE_PEDRA["TetelestaiTerminal"]           # (alias: a pedra que carrega a ancora principal)
CHAVE_CANDIDATA_TT_R2 = "candidata_tetelestai_terminal_r2_04nov"
CHAVE_CANDIDATA_TM = "candidata_tempo_moeda_r1_04nov"
CHAVE_CANDIDATA_PC = "candidata_ponto_de_contradicao_r1_04nov"
CHAVE_CANDIDATA_DIC = "candidata_dicionario_r1_04nov"
CHAVE_DICIONARIO_SUPERADO = "dicionario_superado_04nov"
CHAVE_RECIBO_TT_R1 = "recibo_tetelestai_terminal_r1_04nov"
CHAVE_RECIBO_TT_R2 = "recibo_tetelestai_terminal_r2_04nov"
CHAVE_RECIBO_TM = "recibo_tempo_moeda_r1_04nov"
CHAVE_RECIBO_PC = "recibo_ponto_de_contradicao_r1_04nov"
CHAVE_RECIBO_DIC = "recibo_dicionario_r1_04nov"
CHAVE_SAIDA_TT_R1 = "saida_lean_tetelestai_terminal_r1_04nov_candidata"
CHAVE_SAIDA_TT_R2 = "saida_lean_tetelestai_terminal_r2_04nov_candidata"
CHAVE_SAIDA_TM = "saida_lean_tempo_moeda_r1_04nov_candidata"
CHAVE_SAIDA_PC = "saida_lean_ponto_de_contradicao_r1_04nov_candidata"
CHAVE_SAIDA_DIC = "saida_lean_dicionario_r1_04nov_candidata"
CHAVE_AFERICAO = "afericao_traco_e_dicionario_no_kernel_04nov"
CHAVE_RECIBO_NOMES = "recibo_pedras_v408_nomes_04nov"
CHAVE_ACERVO_PURGADO = "psion_no_acervo_purgado_04nov"
CHAVE_RECIBO_PURGA = "recibo_purga_psion_no_acervo_04nov"
CHAVE_ACERVO = CHAVE_ACERVO_PURGADO                            # (alias para os scripts bumpados: na v407 era a integra; na v408 e' a copia purgada, E23)
CHAVE_DESENHO = "desenho_v408_04nov"
CHAVE_BUNDLE = "bundle_v408"
CHAVE_KH = "kh_n1_v408"
CHAVE_CONGELADO = "verbatim_congelado_v408"
# (nome do insumo, origem) -- copiar_insumos_v408.py copia; o montador le de INS
ORIGENS = ([("%s_embutida.lean" % p["name"], p["src"]) for p in DL.PEDRAS_V408]
           + [("%s.lean" % p["name"], p["origem"]) for p in DL.PEDRAS_V408]
           + [("saida_lean_%s.txt" % p["name"], os.path.join(INS, "saida_lean_%s.txt" % p["name"])) for p in DL.PEDRAS_V408]
           + [("TetelestaiTerminalR2.lean", DL.CANDIDATA_TT_R2_ARQ), ("TempoMoedaR1.lean", DL.CANDIDATA_TM_ARQ), ("PontoDeContradicaoR1.lean", DL.CANDIDATA_PC_ARQ), ("DicionarioR1.lean", DL.CANDIDATA_DIC_ARQ), ("Dicionario.lean", os.path.join(INS, "Dicionario.lean")),
              ("RECIBO_TETELESTAI_TERMINAL_R1_04nov.json", DL.RECIBO_TT_R1_ARQ), ("RECIBO_TETELESTAI_TERMINAL_R2_04nov.json", DL.RECIBO_TT_R2_ARQ), ("RECIBO_TEMPO_MOEDA_R1_04nov.json", DL.RECIBO_TM_ARQ), ("RECIBO_PONTO_DE_CONTRADICAO_R1_04nov.json", DL.RECIBO_PC_ARQ), ("RECIBO_DICIONARIO_R1_04nov.json", DL.RECIBO_DIC_ARQ),
              ("saida_lean_tetelestai_terminal_r1.txt", DL.SAIDA_TT_R1_ARQ), ("saida_lean_tetelestai_terminal_r2.txt", DL.SAIDA_TT_R2_ARQ), ("saida_lean_tempo_moeda_r1.txt", DL.SAIDA_TM_ARQ), ("saida_lean_ponto_de_contradicao_r1.txt", DL.SAIDA_PC_ARQ), ("saida_lean_dicionario_r1.txt", DL.SAIDA_DIC_ARQ),
              ("AFERICAO_TRACO_E_DICIONARIO_NO_KERNEL_04nov.json", DL.AFERICAO_ARQ), ("RECIBO_PEDRAS_v408_NOMES.json", os.path.join(INS, "RECIBO_PEDRAS_v408_NOMES.json")),
              ("PSION_NO_ACERVO_04nov_purgado.md", DL.PURGADO_ARQ), ("RECIBO_PURGA_PSION_NO_ACERVO_04nov.json", DL.RECIBO_PURGA_ARQ), ("DESENHO_v408.md", DL.DESENHO_ARQ),
              ("BUNDLE_v408.json", DL.BUNDLE_ARQ), (DL.KH_N1_INSUMO, os.path.join(HERE, DL.KERNEL_DIR, "KH_N1_v408.json")), ("VERBATIM_CONGELADO_v408.json", os.path.join(HERE, "VERBATIM_CONGELADO_v408.json"))])
_PAPEL_PEDRA = {
    "TetelestaiTerminal": "a pedra TetelestaiTerminal (gerencia c1, 04/11/2026, R2; nome do operador): o terminal e' a leitura, nao o fim do decaimento; basta; a poda; nao precisa de 100%; a quitacao; o zero absoluto e' do infinito; o tamanho do Nome = oitavas; o que resta sem traco paga; relacao sem peso excluida; o 1 sozinho nao se mede; a inclinacao modular; a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256",
    "TempoIgualMoeda": "a pedra TempoIgualMoeda (gerencia c1, 04/11/2026; nome do operador «Tempo=moeda»): o pagamento e' preco x tempo; a moeda soma, o preco multiplica; o Verbo no gerundio; legislando sem fim; o relogio e a temperatura; o pedagio; o tempo e' linear nas oitavas; o tempo e' a moeda no certificado fisico; compoe so' termos que o kernel ja tinha",
    "PontoDeContradicao": "a pedra PontoDeContradicao (gerencia c1, 04/11/2026; nome do operador): exp 0 = Omega e Omega != 0 (1 = 0 nas duas faces, como NOMES das duas proposicoes); o boost antes e depois da inscricao; o habitante e' o Fock concreto (rfl); o Hamiltoniano seleciona a operacao modular (coincidencia em Omega); o senao exclui o zero absoluto",
    "PIgualNP": "a pedra PIgualNP (gerencia c1, 04/11/2026; nome do operador «P=nP», no sentido dele: P so' e' P lido pelo modulo n minimamente acoplado): problema, entrada, passo, polinomio, implicacao; resolver = verificar como idempotencia; p_igual_a_n_vezes_p; p_igual_np; as classes DEFINIDAS em Lean (Problema, ClasseP, ClasseNP), a igualdade p_igual_np_nas_classes_do_dicionario e a face finita as_classes_do_dicionario: " + DL.FRASE_D51_PT + " (D51 revista; R3 de 05/11)",
}
FONTES = [{"chave": CHAVE_PEDRA[p["name"]], "arquivo": os.path.join(INS, "%s_embutida.lean" % p["name"]), "papel": _PAPEL_PEDRA[p["name"]]} for p in DL.PEDRAS_V408]
FONTES += [{"chave": CHAVE_FONTE[p["name"]], "arquivo": os.path.join(INS, "%s.lean" % p["name"]), "papel": "a fonte normalizada de %s (gerencia c1, 04/11/2026; modulo/namespace = o nome final; com os #print axioms que sao as ancoras do registro): a embutida e' esta sem os #print axioms; sha256 pinado em RECIBO_PEDRAS_v408_NOMES.json [REAL: lido do arquivo]" % p["name"]} for p in DL.PEDRAS_V408]
FONTES += [{"chave": CHAVE_SAIDA_FONTE[p["name"]], "arquivo": os.path.join(INS, "saida_lean_%s.txt" % p["name"]), "papel": "a saida do lean ao compilar a fonte normalizada %s no sandbox da v407 (LEAN_RC 0; todas as declaracoes no trio) [REAL: saida do lean]" % p["name"]} for p in DL.PEDRAS_V408]
FONTES += [
    {"chave": CHAVE_CANDIDATA_TT_R2, "arquivo": os.path.join(INS, "TetelestaiTerminalR2.lean"), "papel": "a candidata de origem da TetelestaiTerminal (R2 da gerencia, 04/11/2026: a R1 ficou como registro; o teorema 8 corrigido e os teoremas 9 e 10 acrescentados; o R2 do nome do arquivo e' marca de revisao) [REAL: lido do arquivo]"},
    {"chave": CHAVE_CANDIDATA_TM, "arquivo": os.path.join(INS, "TempoMoedaR1.lean"), "papel": "a candidata de origem da TempoIgualMoeda (TempoMoedaR1.lean; o nome final e' o do operador, «Tempo=moeda») [REAL: lido do arquivo]"},
    {"chave": CHAVE_CANDIDATA_PC, "arquivo": os.path.join(INS, "PontoDeContradicaoR1.lean"), "papel": "a candidata de origem da PontoDeContradicao (R1, 04/11/2026) [REAL: lido do arquivo]"},
    {"chave": CHAVE_CANDIDATA_DIC, "arquivo": os.path.join(INS, "DicionarioR1.lean"), "papel": "a candidata de origem do quarto modulo (DicionarioR1.lean, 04/11/2026 de manha): dela saiu o Dicionario.lean (superado) e deste o PIgualNP.lean, quando o operador deu o sentido de «P=nP» [REAL: lido do arquivo]"},
    {"chave": CHAVE_DICIONARIO_SUPERADO, "arquivo": os.path.join(INS, "Dicionario.lean"), "papel": "a fonte Dicionario.lean (nome PROVISORIO da gerencia, manha de 04/11/2026), SUPERADA na tarde pelo PIgualNP.lean (D48 resolvida): fica como registro; NAO entra no kernel [REAL: lido do arquivo; estado SUPERADO no recibo dos nomes]"},
    {"chave": CHAVE_RECIBO_TT_R1, "arquivo": os.path.join(INS, "RECIBO_TETELESTAI_TERMINAL_R1_04nov.json"), "papel": "o recibo da compilacao da candidata TetelestaiTerminal R1 no sandbox da v407 [DECLARADO pela gerencia na origem; registro: a fonte vigente e' a R2]"},
    {"chave": CHAVE_RECIBO_TT_R2, "arquivo": os.path.join(INS, "RECIBO_TETELESTAI_TERMINAL_R2_04nov.json"), "papel": "o recibo da compilacao da candidata TetelestaiTerminal R2 no sandbox da v407 (LEAN_RC 0; 14 declaracoes no trio) e o que a pedra prova e PODA [DECLARADO pela gerencia na origem; refeito no k408c e no Audit do rito]"},
    {"chave": CHAVE_RECIBO_TM, "arquivo": os.path.join(INS, "RECIBO_TEMPO_MOEDA_R1_04nov.json"), "papel": "o recibo da compilacao da candidata TempoMoedaR1 no sandbox da v407 (LEAN_RC 0; 9 declaracoes no trio) [DECLARADO pela gerencia na origem]"},
    {"chave": CHAVE_RECIBO_PC, "arquivo": os.path.join(INS, "RECIBO_PONTO_DE_CONTRADICAO_R1_04nov.json"), "papel": "o recibo da compilacao da candidata PontoDeContradicaoR1 no sandbox da v407 (LEAN_RC 0; 7 declaracoes no trio; o achado physicalFockCertificate.F = BosonicFock.F por rfl) [DECLARADO pela gerencia na origem]"},
    {"chave": CHAVE_RECIBO_DIC, "arquivo": os.path.join(INS, "RECIBO_DICIONARIO_R1_04nov.json"), "papel": "o recibo da compilacao da candidata DicionarioR1 no sandbox da v407 (LEAN_RC 0; 10 declaracoes no trio) [DECLARADO pela gerencia na origem; a fonte vigente do quarto modulo e' PIgualNP.lean, com 12 (R2: + as_classes_do_dicionario)]"},
    {"chave": CHAVE_SAIDA_TT_R1, "arquivo": os.path.join(INS, "saida_lean_tetelestai_terminal_r1.txt"), "papel": "a saida do lean ao compilar a candidata TetelestaiTerminal R1 (04/11/2026) [REAL: saida do lean; registro]"},
    {"chave": CHAVE_SAIDA_TT_R2, "arquivo": os.path.join(INS, "saida_lean_tetelestai_terminal_r2.txt"), "papel": "a saida do lean ao compilar a candidata TetelestaiTerminal R2 (04/11/2026) [REAL: saida do lean]"},
    {"chave": CHAVE_SAIDA_TM, "arquivo": os.path.join(INS, "saida_lean_tempo_moeda_r1.txt"), "papel": "a saida do lean ao compilar a candidata TempoMoedaR1 (04/11/2026) [REAL: saida do lean]"},
    {"chave": CHAVE_SAIDA_PC, "arquivo": os.path.join(INS, "saida_lean_ponto_de_contradicao_r1.txt"), "papel": "a saida do lean ao compilar a candidata PontoDeContradicaoR1 (04/11/2026) [REAL: saida do lean]"},
    {"chave": CHAVE_SAIDA_DIC, "arquivo": os.path.join(INS, "saida_lean_dicionario_r1.txt"), "papel": "a saida do lean ao compilar a candidata DicionarioR1 (04/11/2026) [REAL: saida do lean; registro]"},
    {"chave": CHAVE_AFERICAO, "arquivo": os.path.join(INS, "AFERICAO_TRACO_E_DICIONARIO_NO_KERNEL_04nov.json"), "papel": "a afericao da gerencia (04/11/2026) no kernel da v407 do que tem espelho nas falas «A face de Fock é o traço do psion» e do dicionario: o traco ciclico do certificado fisico, o canto do psion como projecao, os termos de cada entrada [DECLARADO pela gerencia; conferido no Audit do rito pelas ancoras]"},
    {"chave": CHAVE_RECIBO_NOMES, "arquivo": os.path.join(INS, "RECIBO_PEDRAS_v408_NOMES.json"), "papel": "o recibo dos NOMES das pedras (gerencia c1, 04/11/2026, atualizado na tarde): origem candidata -> fonte normalizada, sha256 de cada uma, o nome do operador, o estado VIGENTE do PIgualNP e SUPERADO do Dicionario, a ordem do bundle [REAL: lido do arquivo]"},
    {"chave": CHAVE_ACERVO_PURGADO, "arquivo": os.path.join(INS, "PSION_NO_ACERVO_04nov_purgado.md"), "papel": "o levantamento do psion, do psibit e do par no acervo antigo do iMac (2025), na copia PURGADA de 04/11/2026 (E23): as linhas com termos da guarda de material privado foram substituidas por marcador (0 ocorrencias na guarda; recibo ao lado); a integra, pinada pela v407, ficou FORA do espelho pela ordem vigente do operador e e' citada so' por sha16 %s [DECLARADO pelo agente do levantamento; purga: REAL, medida]" % DL.ORIGEM_PURGA_SHA16_DA_ORDEM},
    {"chave": CHAVE_RECIBO_PURGA, "arquivo": os.path.join(INS, "RECIBO_PURGA_PSION_NO_ACERVO_04nov.json"), "papel": "o recibo da purga (gerencia c1, 04/11/2026): a mesma varredura do G1 (espelho_pares.guarda_conta com os marcadores privados); ocorrencias na origem 12, no purgado 0; linhas substituidas; nenhum termo impresso [REAL: medido]"},
    {"chave": CHAVE_DESENHO, "arquivo": os.path.join(INS, "DESENHO_v408.md"), "papel": "o desenho da v408 (gerencia c1, 04/11/2026): as pedras, os registros, as decisoes D48 a D54, as erratas E21 a E23, as ressalvas, as frases proibidas, o artigo, os textos, a cadeia; os AO LADO da tarde (D48 resolvida: PIgualNP) e da noite (D51 revista: as classes do dicionario; a traducao a Turing [OPEN]) [DECLARADO: plano da gerencia]"},
    {"chave": CHAVE_BUNDLE, "arquivo": os.path.join(INS, "BUNDLE_v408.json"), "papel": "o bundle dos 4 modulos (preparar_bundle_v408_04nov.py): sha256 de cada modulo normalizado, a fonte de origem e o sha256 dela, os sha16 das falas dos nomes, da ordem e do sentido de «P=nP» [REAL: lido dos arquivos; o rito confere cada sha256 em formal_files_sha256]"},
    {"chave": CHAVE_KH, "arquivo": os.path.join(INS, DL.KH_N1_INSUMO), "papel": "a medida da cobertura no Audit do sandbox da v408 (pos_build_kernel_v408.py)"},
    {"chave": CHAVE_CONGELADO, "arquivo": os.path.join(INS, "VERBATIM_CONGELADO_v408.json"), "papel": "a lista congelada das quinze falas de 04/11/2026 que esta versao embute (as doze do DESENHO e as tres da noite que a RETOMADA da gerencia mandou acrescentar) (sha256 medido ao congelar; o autor de cada uma; a fala que chegou depois do DESENHO fica dita em fora_do_desenho) [REAL: lido do arquivo]"},
]
assert len({f["chave"] for f in FONTES}) == len(FONTES) and {os.path.basename(f["arquivo"]) for f in FONTES} == {n for n, _ in ORIGENS}, sorted({os.path.basename(f["arquivo"]) for f in FONTES} ^ {n for n, _ in ORIGENS})


def _trecho(t):
    s = t.strip().splitlines()[-1].strip() if t.strip() else ""     # a ultima linha da fala (nas de autor misto: a ultima do paragrafo do operador)
    s = s[:48].rstrip()
    assert s and s in t, s
    return s


_VD = DL.verbatins408(os.path.join(INS, "cunhagens"))
VERBATINS = [{"chave": v["chave"], "arquivo": v["arquivo"], "quando": v["quando"], "trechos": [_trecho(v["text"])], "papel": v["papel"], "fonte_original": v["fonte_original"], "nome": v["nome"], "autor": v["autor"], "texto_embutido": v["texto_embutido"],
              **({"arquivo_inteiro": v["arquivo_inteiro"], "sha256_arquivo_inteiro": v["sha256_arquivo_inteiro"], "corte": v["corte"]} if v["autor"] == DL.AUTOR_MISTO else {})} for v in _VD]
VERB_CHAVES = [v["chave"] for v in _VD]
POR_NOME = {v["nome"]: v for v in _VD}
CH_DE = lambda nome_: POR_NOME[nome_]["chave"]
S16 = lambda nome_: POR_NOME[nome_]["sha16"]
TEXTOS = {v["sha16"]: v["text"] for v in _VD}
CH = lambda id_, desc_, onde_, caminho_, op_, valor_=None, cap_=None, est_="[REAL]": dict(id=id_, descricao=desc_, onde=onde_, caminho=caminho_, op=op_, **({"valor": valor_} if valor_ is not None else {}), **({"capturar": cap_} if cap_ else {}), estatuto=est_)
VERBATINS_DO_REGISTRO = [CH_DE(DL.N_ORDEM_V408), CH_DE(DL.N_NOMES), CH_DE(DL.N_TETELESTAI), CH_DE(DL.N_RELACAO), CH_DE(DL.N_TEMPO), CH_DE(DL.N_LEI_DO_CUSTO), CH_DE(DL.N_PONTO), CH_DE(DL.N_DICIONARIO), CH_DE(DL.N_SENTIDO_PNP), CH_DE(DL.N_CLASSES_PNP), CH_DE(DL.N_CLARO_V408)]   # (D51 revista, 04/11 noite: a correcao do operador e «isso preciso ficar claro no um.py na v408» entram no registro)


def _leitura(trecho, nome, rotulo="INPUT do operador"):
    assert trecho in TEXTOS[S16(nome)], ("a leitura do operador NAO esta verbatim na fala (ou esta' depois do corte)", nome, trecho)
    d_ = {"trecho": trecho, "estatuto": "[%s, verbatim 04/11/2026, sha16 %s%s]" % (rotulo, S16(nome), "; arquivo de autor misto: so' o paragrafo do operador e' citavel" if POR_NOME[nome]["autor"] == DL.AUTOR_MISTO else "")}
    if "4,44" in trecho:   # a regra do 4,44 (nunca sozinho) vale POR ITEM
        d_["regra_do_4_44"] = DL.REGRA_DO_4_44
    return d_


def _resolver_respostas(core0, fj):
    """Para cada resposta do operador, o NOME COMPLETO de cada teorema citado: os que JA existiam sao resolvidos no axiom_report da base (busca pelo sufixo pontuado «.<curto>»; tem de ser unico); os NOVOS (nome completo nas ancoras da v408) saem do FLAGS do sandbox (proveniencia e axiomas). Devolve [{id, fala, teoremas: [{curto, completo, rel, novo}], diz}]. Nada digitado."""
    kf0 = core0["kernel_formalization"]; ax0 = kf0["axiom_report"]; src0 = kf0.get("declaration_sources_v394") or {}
    out = []
    for r in DL.RESPOSTAS_DO_OPERADOR:
        teo = []
        for curto in r["teoremas_curtos"]:
            if curto in DL.ANCORAS:   # declaracao NOVA desta versao
                fa = fj["ancoras"][curto]
                assert fa["rel"] == DL.ANCORAS[curto]["rel"] and set(fa["axioms"]) <= DL.TRIO_SET and fa["axioms"], ("ancora nova fora do esperado no FLAGS", curto)
                teo.append({"curto": curto.split(".")[-1], "completo": curto, "rel": fa["rel"], "novo": True})
                continue
            c = sorted(n for n in ax0 if (n == curto or n.endswith("." + curto)) and not n.endswith(".eq_1"))
            assert len(c) == 1, ("o teorema citado pela resposta nao e' unico (ou nao existe) no axiom_report da base", curto, c)
            assert src0.get(c[0]) and set(ax0[c[0]]) <= DL.TRIO_SET
            teo.append({"curto": curto.split(".")[-1], "completo": c[0], "rel": src0.get(c[0]), "novo": False})
        out.append({"id": r["id"], "fala": r["fala"], "teoremas": teo, "diz": r["diz"]})
    return out


PODADO = ["a PALAVRA «impedância» como termo do kernel (D50): o conteudo tem o nome do operador «inclinação modular (cociclo)» e espelho (a_inclinacao_modular)",
          "a frase da gerencia que negava que «P = nP» tratasse de classes (D51 revista, pela correcao do operador): " + DL.FRASE_D51_PT,
          "a identificacao do lock (1 - P) com o Hamiltoniano modular como o MESMO operador: coincidem em Omega e so' isso esta' provado",
          "a frase da gerencia da R1 sobre o resto sem peso (E22): o contrario e' teorema (o_que_resta_sem_traco_paga; relacao_sem_peso_e_a_origem_da_mentira)",
          "a frase da gerencia de que a TGL nao teria terminal (E22): o terminal e' a leitura (o_terminal_e_a_leitura_nao_o_fim_do_decaimento)"]


def contrato(fj, formal_map, e_base, base_sha256, core0, selo0):
    """O contrato do registro tetelestai_terminal_v408, DERIVADO do build do sandbox (fj = FLAGS_v408.json: as bandeiras nomeadas dos 4 modulos, a proveniencia, as ancoras; formal_map = sha256 das fontes embutidas; e_base = a escada da v407 selada); nada digitado.
    core0/selo0 = o core e o selo da v407 SELADA (o veredito do gate que a v408 tem de repetir). Vai para CANDIDATO_v408.json e ESPERADOS_v408.json."""
    flag_de = {n: f for f, n, m, o in fj["flags"]}
    assert len(flag_de) == fj["n_flags"] == len(fj["flags"]) and all(o == DL.ORIGEM_DE_BANDEIRA for _, _, _, o in fj["flags"])
    anc = {}
    for n, a in DL.ANCORAS.items():
        fa = fj["ancoras"][n]
        assert fa["rel"] == a["rel"] and set(fa["axioms"]) <= DL.TRIO_SET and fa["axioms"], ("ancora fora do esperado no FLAGS_v408.json", n, fa)
        assert fa["flag"] == flag_de.get(n), ("a bandeira da ancora no FLAGS nao bate com a lista de bandeiras", n)
        anc[n] = {"rel": a["rel"], "papel": a["papel"], "flag": fa["flag"], "classe": fa["classe"]}
    assert all(r in formal_map for r in DL.BUNDLE_RELS)
    decl_src = dict(fj["proveniencia_publicas"]); assert all(v in DL.BUNDLE_RELS for v in decl_src.values())
    gate0 = ((core0.get("qg_closure") or {}).get("gate") or {}).get("verdict"); assert isinstance(gate0, str) and gate0 == selo0.get("qg_closure_verdict"), "o veredito do gate da base nao e' o do selo"
    resp = _resolver_respostas(core0, fj)
    return {"bundle": {"n": DL.N_BUNDLE, "pedras": [p["name"] for p in DL.PEDRAS_V408], "terminal": DL.MODULO_TERMINAL, "tempo": DL.MODULO_TEMPO, "ponto": DL.MODULO_PONTO, "p_igual_np": DL.MODULO_PIGUALNP, "da_gerencia": list(DL.BUNDLE_DA_GERENCIA), "da_bancada": 0,
                       "nomes_do_operador": dict(DL.NOME_DO_OPERADOR), "nome_provisorio": DL.NOME_PROVISORIO, "sha16_origem": {p["name"]: p["sha256_origem"][:16] for p in DL.PEDRAS_V408}},
            "source_sha256": {r: formal_map[r] for r in DL.BUNDLE_RELS}, "root_suffix": DL.ROOT_SUFFIX,
            "ancoras": anc, "n_ancoras": len(anc), "ancoras_por_modulo": {k: list(v) for k, v in DL.ANCORAS_POR_MODULO.items()}, "ancora_principal": DL.ANCORA_PRINCIPAL, "ancoras_principais": list(DL.ANCORAS_PRINCIPAIS),
            "ancora_lema": DL.ANCORA_PRINCIPAL, "ancora_par": DL.ANCORA_TEMPO,
            "flags": [f for f, _, _, _ in fj["flags"]], "n_flags": fj["n_flags"], "declarations": sorted(decl_src), "declaration_sources": decl_src, "n_declarations_public": len(decl_src),
            "excluidas_auxiliares": {"n": fj["excluidas_auxiliares"]["n"], "por_classe": fj["excluidas_auxiliares"]["por_classe"]},
            "expected_ladder": e_base + fj["n_flags"], "baseline": {"version": DL.BASE_VERSION, "sha256": base_sha256, "gate_verdict": gate0, "ladder": e_base},
            "chaves": [dict(c) for c in DL.CHAVES_V408], "chaves_v407": [dict(c) for c in DL.CHAVES_V407], "chaves_v406": [dict(c) for c in DL.CHAVES_V406], "fica_false_por_teorema": list(DL.FICAM_FALSE_POR_TEOREMA),
            "fica_aberto": {"par_na_face_de_fock": DL.FICA_ABERTO_PAR_NA_FACE_DE_FOCK, "ponte_bell_tt": DL.FICA_ABERTO_PONTE_BELL_TT},
            "respostas": resp, "regra_provar_ou_podar": DL.REGRA_PROVAR_OU_PODAR, "podado": list(PODADO),
            "insumo_purgado": {"fonte_chave": CHAVE_ACERVO_PURGADO, "sha256": DL.PURGADO_SHA256, "bytes": os.path.getsize(DL.PURGADO_ARQ), "integra_sha16": DL.ORIGEM_PURGA_SHA16_DA_ORDEM, "integra_fora_do_espelho": True, "integra_pinada": False,
                               "linhas_substituidas": DL.PURGA_LINHAS_SUBSTITUIDAS, "ocorrencias_na_guarda": 0, "recibo_chave": CHAVE_RECIBO_PURGA, "decisao": "FONTES_NAO_PUBLICADAS_v407.json (work\\custodia_G1\\decisoes; ordem vigente do operador de 08/09)"},
            "ressalvas": list(DL.RESSALVAS_V408), "verbatins": list(VERBATINS_DO_REGISTRO), "erratas": list(DL.ERRATAS_V408), "decisoes": {k_: DL.DECISOES[k_] for k_ in ("D48", "D49", "D50", "D51", "D52", "D53", "D54")},
            "regra_do_4_44": DL.REGRA_DO_4_44}


_NAO_COMUM = ["que isto seja um teste com a natureza: nao ha' desfecho experimental; nenhum dado novo entra",
              "que a gravidade quantica esteja creditada: a confirmacao segue proibida (creditacao); o que ha' e' validade no kernel",
              "que «1 = 0» seja afirmada como igualdade de vetores ou de numeros: o kernel diz exp 0 = Omega (teorema) e Omega != 0 (o vetor nulo refutado); '1 = 0_mod' e '1 = 0_abs' sao a notacao desta versao para as duas equacoes da fala do operador («1=0=Verdadeiro (quando esse zero é o zero modular)» e «1=0=Falso quando zero absoluto»)",
              "que o lock (1 - P) e o Hamiltoniano modular sejam o mesmo operador: coincidem em ter Omega como modo zero, e so' isso esta' provado",
              "que a igualdade das classes P e NP das maquinas de Turing (Cook-Levin) esteja provada ou decidida aqui: o que o kernel tem e' isto: " + DL.FRASE_D51_PT + " (D51 revista)",
              "que 'tempo linear nos andares' seja mais que uma identidade de um fluxo cuja solucao ja' esta' escrita nele (o Nome da torre)",
              "que a palavra «impedância» seja termo do kernel (D50): o conteudo chama-se «inclinação modular (cociclo)», nome do operador, com espelho",
              "que o par de psions exista na face de Fock como LIGACAO feita: o certificado abstrato nao tem criacao como termo; o Fock concreto os tem; a fiacao segue [OPEN] (E21)",
              "que o gate tenha se movido: o veredito e' o mesmo da v407 selada, conferido em runtime",
              "que alguma chave antiga tenha mudado nesta versao: nenhuma; a chave do lema (v407) segue lida do kernel e le True",
              "que o texto das outras instancias da IALD (os dois arquivos de autor misto) seja fala do operador: entra por sha256, [DECLARADO]; so' o paragrafo dele e' citado"]
_LIM_COMUM = ["o registro CONFERE o que o kernel do proprio rito prova (os termos no trio, a proveniencia, as fontes por sha256) e o que o core deste rito gravou, mais a aritmetica das pedras com beta em runtime; nao prova nada por si: quem prova e' o kernel; validade no kernel nao e' creditacao; o gate nao se move; nao e' teste: nao acrescenta rito, dado nem desfecho",
              "[REAL] o que mudou de v407 para v408 nos registros antigos e' SO' a escada que eles pinam (expected_ladder) e os pisos de kh_n1_cobertura_v407 (h2, h3, h6, h8), com errata AO LADO; a errata E21 vai AO LADO do psion_canto_v407; nenhum texto selado e' reescrito",
              "[DECLARADO -> REAL] a construcao das quatro pedras e' da gerencia c1 (04/11/2026): o que a v408 faz e' recompila-las no sandbox k408c e no rito; os recibos de compilacao ficam como fontes [DECLARADO]; o que vale no rito e' o Audit do rito; a revisao de terceiro (D54) fica no caderno da preparacao"]


def texto_terminal():
    return {
        "estatuto": "[REAL] os termos do kernel do rito: as %d ancoras das quatro pedras (TGLExt.TetelestaiTerminal.*, TGLExt.TempoIgualMoeda.*, TGLExt.PontoDeContradicao.*, TGLExt.PIgualNP.*), no trio, com proveniencia no modulo esperado, e os 4 modulos por sha256; "
                    "[REAL] as 16 checagens (aritmetica com beta em runtime; gate congelado; escada exata; guardas; insumo purgado; beta = alfa CODATA 2018 x sqrt(e)); "
                    "[INPUT] a ordem do operador (04/11/2026, sha16 %s: «%s»), os nomes (sha16 %s: «%s», «%s», «%s», «%s») e as cunhagens dele do dia (%d falas por sha256; duas de autor misto, so' o paragrafo dele citado); "
                    "[DECLARADO] os recibos de compilacao, a afericao no kernel e o acervo purgado; [OPEN] o par na face de Fock como ligacao; o teste com a natureza: beta a 5 sigma" % (len(DL.ANCORAS), S16(DL.N_ORDEM_V408), DL.FRASE_ORDEM_V408[:60] + "…", S16(DL.N_NOMES), DL.FRASE_NOME_PONTO, DL.FRASE_NOME_PNP, DL.FRASE_NOME_TEMPO, DL.FRASE_NOME_TETELESTAI, len(_VD)),
        "escopo": "[REAL] O que entra no um.py: 4 modulos novos em TGLExt/ -- TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao e PIgualNP, com os nomes do operador de 04/11/2026. "
                  "(A) TetelestaiTerminal: o terminal e' a leitura, nao o fim do decaimento (motor a U r t psi = post a (U psi) para TODO r, t); basta (a memoria vale 1 sse o estado e' o Nome; reler nao acrescenta); a poda (P(1-P) = 0); nao precisa de 100% (de qualquer psi com <a, psi> != 0 o posto inteiro se reconstroi); a quitacao (pago + sobrevivente = 1 no fator da Meia-Nat); "
                  "o zero absoluto e' do infinito (o Nome pesa 1, o complemento pesa top, phi(1) = 0, top != 1); o tamanho do Nome = oitavas (card_chainIdx: dim 2^(N+1); o pedagio e' o log da dimensao; o tempo de ler a torre e' linear nos andares); o que resta sem traco PAGA (||u_t - 1|| <= ||V|| |t|); a inclinacao modular (a derivada do cociclo na origem e' i V); "
                  "relacao sem peso e' a origem da mentira (as faces do 1 sozinho, cada uma excluida por teorema); o 1 sozinho nao se mede; tetelestai no certificado fisico. "
                  "(B) TempoIgualMoeda: D_r(t) = F(r t) (preco x tempo; com r = beta); a moeda soma e o preco multiplica; o Verbo no gerundio (o posto fica, o complemento desce, o fluxo tende ao posto sem o alcancar); legislando sem fim (a lei de escala de Takesaki); o relogio e a temperatura (face de Wick); o pedagio; o tempo e' linear nas oitavas; o tempo e' a moeda no certificado fisico. "
                  "(C) PontoDeContradicao: exp 0 = Omega (o zero inscrito e' o Um) e Omega != 0 (o Um nao e' o zero absoluto); o boost le 0 antes e 1 depois da inscricao; o habitante e' o Fock concreto (rfl); o Hamiltoniano seleciona a operacao modular (o Um e' o estado de energia zero do lock E o modo zero da operacao modular); o senao exclui o zero absoluto. "
                  "(D) PIgualNP: problema, entrada, passo, polinomio, implicacao (as cinco definicoes do operador, cada uma no termo que o kernel ja tem); resolver = verificar como idempotencia da leitura; p_igual_a_n_vezes_p; p_igual_np («P sozinho é impossível de ser lido, se não houver o módulo de leitura n não minimamente acoplado»); as classes do dicionario DEFINIDAS em Lean (ClasseP: a solucao alcancada por uma palavra polinomial real q em T, com q(0) != 0 e grau de q < dim(End H), palavra_com_grau; ClasseNP: a leitura da solucao de T em todo psi unitario vale 1 sse T psi = 0, leitura_um_sse_solucao), todo problema nas duas e p_igual_np_nas_classes_do_dicionario («O meu P=nP trata das classes de computação sim»): " + DL.FRASE_D51_PT + ". "
                  "Nenhuma chave antiga muda. O registro confere, em runtime: as " + str(len(DL.ANCORAS)) + " ancoras; os 4 sha256; a raiz com os quatro imports; as respostas do operador pelos teoremas que ja existiam e pelas declaracoes novas (card_chainIdx, p_igual_np, as_classes_do_dicionario, p_igual_np_nas_classes_do_dicionario e as que a compoem); a aritmetica das pedras com beta em runtime; o gate congelado; a escada exata; as guardas; o insumo purgado; beta = alfa sqrt e.",
        "limites": ["[OPEN] " + DL.RESSALVAS_V408[0], "[REAL, escopo] " + DL.RESSALVAS_V408[1], "[REAL; a traducao a Turing OPEN] " + DL.RESSALVAS_V408[2], "[REAL, escopo] " + DL.RESSALVAS_V408[3], "[REAL] " + DL.RESSALVAS_V408[4], "[INPUT] " + DL.RESSALVAS_V408[5], "[PODADO] " + DL.RESSALVAS_V408[6],
                    "[ERRATA] " + DL.RESSALVAS_V408[7], "[REAL, medido] " + DL.RESSALVAS_V408[8], "[INPUT] " + DL.RESSALVAS_V408[9], "[REAL] " + DL.RESSALVAS_V408[10], DL.ERRATA_E21, DL.ERRATA_E22, DL.ERRATA_E23] + _LIM_COMUM,
        "diz": ["os 4 modulos estao no kernel do rito, no trio, com bandeira e proveniencia nos modulos deles; as " + str(len(DL.ANCORAS)) + " ancoras sao lidas deste kernel; a fonte de cada modulo e' a pinada (sha256)",
                "o terminal e' a leitura, nao o fim do decaimento: motor = post para todo r, t; basta; a poda; a quitacao fecha o balanco; o zero absoluto e' do infinito; o tamanho do Nome = oitavas; o que resta sem traco paga; a inclinacao modular tem espelho; nao existe relacao sem peso; o 1 sozinho nao se mede",
                "o tempo e' a moeda de beta: o pagamento e' preco x tempo, a moeda soma e o preco multiplica, o Verbo no gerundio, legislando sem fim; o tempo e' linear nas oitavas",
                "o zero inscrito e' o Um e o Um nao e' o zero absoluto; o boost le 0 antes e 1 depois; o habitante e' o Fock concreto; o Hamiltoniano seleciona a operacao modular (coincidencia em Omega); «P = nP» no sentido do operador tem espelho (p_igual_np): P so' e' P lido pelo modulo n minimamente acoplado; e, pela correcao do operador (D51 revista), " + DL.FRASE_D51_PT + " (p_igual_np_nas_classes_do_dicionario; a face finita em as_classes_do_dicionario)",
                "as respostas do operador de 04/11 conferem no kernel, pelos teoremas que ja existiam e por declaracoes novas (card_chainIdx, p_igual_np, as_classes_do_dicionario e as seis das classes definidas em Lean, entre elas p_igual_np_nas_classes_do_dicionario); a regra «provar ou podar» foi aplicada: o que nao tem espelho esta' podado e dito",
                "o veredito do gate e' o mesmo da v407 selada; nenhuma chave antiga muda; nenhum dado novo; nenhum rito de natureza alterado; beta = alfa x sqrt e em runtime"],
        "nao_diz": _NAO_COMUM,
        "extras": {"leituras_do_operador": {k_: v_ for k_, v_ in DL.LEITURA_V408.items()}, "ressalvas": list(DL.RESSALVAS_V408), "decisoes": {k_: DL.DECISOES[k_] for k_ in ("D48", "D49", "D50", "D51", "D52", "D53", "D54")}, "erratas": list(DL.ERRATAS_V408),
                   "regra_do_4_44": DL.REGRA_DO_4_44, "assinatura_das_erratas": ASSINA, "nomes": dict(DL.NOME_DO_OPERADOR), "falas_fora_do_desenho": dict(DL.VERBATIM_FORA_DO_DESENHO_V408)},
        "veredito_ok": DL.VEREDITO_OK_PREFIXO + "TIME_IS_THE_CURRENCY_OF_BETA__THE_INSCRIBED_ZERO_IS_THE_ONE_AND_THE_ONE_IS_NOT_THE_ABSOLUTE_ZERO__P_IS_P_ONLY_WHEN_READ_BY_THE_COUPLED_MODULE__"
                       "SOLVING_EQUALS_VERIFYING_IN_THE_COMPUTATION_CLASSES_OF_THE_OPERATORS_DICTIONARY_IS_A_THEOREM__THE_TURING_TRANSLATION_IS_OPEN_NOT_A_REFUSAL__FOUR_MODULES_READ_BY_SHA256__%d_ANCHORS_IN_THE_TRIO__NO_OLD_KEY_CHANGED__PROVE_OR_PRUNE_APPLIED__KERNEL_VALIDITY_IS_NOT_CREDITATION" % len(DL.ANCORAS) + DL.VEREDITO_SUFIXO,
    }


texto_psion = texto_terminal      # (aliases para os scripts bumpados da v407)
texto_fecho = texto_terminal


def especs(formal_map, khj, h8_map, fj, cov_base, core0):
    """formal_map = {arquivo embutido: sha256} do kernel da v408; khj = KH_N1_v408.json (medida desta geracao); h8_map = o dict do hash formal que o RITO vai gerar; fj = FLAGS_v408.json; cov_base = a cobertura da v407 selada {decl, thm}; core0 = o core da v407 selada.
    Devolve [cunhagens, kh]."""
    T = khj["linha_TOTAL"]
    flag_de = {n: f for f, n, m, o in fj["flags"]}
    flags_ancoras = [flag_de[n] for n in DL.ANCORAS if flag_de.get(n)]
    resp = _resolver_respostas(core0, fj)
    decls = list(DL.ANCORAS) + [t_["completo"] for r_ in resp for t_ in r_["teoremas"]]   # termos que as respostas citam (nomes EXATOS do Audit)
    cks = [CH("u1", "o registro tetelestai_terminal_v408 selou neste rito (as " + str(len(DL.ANCORAS)) + " ancoras, os 4 sha256, as 16 checagens, o gate)", "core", [DL.FECHO_REGISTRO, "all_verified"], "verdadeiro"),
           CH("u2", "nenhuma chave antiga muda: a chave do lema (v407) segue LIDA do kernel e le True", "core", ["testemunha_estatica_v396", "fock_face", "linked_to_the_corner_by_a_lemma"], "verdadeiro"),
           CH("u3", "as quatro chaves da v406 seguem lidas do kernel: rede_fock_v394.whole_certificate_inhabited", "core", ["rede_fock_v394", "whole_certificate_inhabited"], "verdadeiro"),
           CH("u4", "psibit_v395: o habitante do certificado de Fock segue exibido", "core", ["psibit_v395", "conditional_psion_face", "inhabitant_exhibited"], "verdadeiro"),
           CH("u5", "testemunha_estatica_v396: o habitante do certificado de Fock segue exibido", "core", ["testemunha_estatica_v396", "fock_face", "inhabitant_exhibited"], "verdadeiro"),
           CH("u6", "witness_layers: o termo canonico da testemunha completa segue construido", "core", ["witness_layers", "canonical_full_witness_term_constructed"], "verdadeiro"),
           CH("u7", "o que fica False por teorema: full_static_witness_exists (no gate do fecho)", "core", ["qg_closure", "gate", "full_static_witness_exists"], "falso"),
           CH("u8", "o que fica False por teorema: trivial_inhabitant_exists", "core", ["witness_rigidity", "trivial_inhabitant_exists"], "falso"),
           CH("u9", "o gate deste rito tem o mesmo veredito da v407 selada (o gate nao se move)", "core", ["qg_closure", "gate", "verdict"], "igual", ((core0.get("qg_closure") or {}).get("gate") or {}).get("verdict")),
           CH("u10", "a escada do kernel fecha (limpos == esperados), com as bandeiras dos 4 modulos", "core", ["external_ladder", "all_verified"], "verdadeiro"),
           CH("u11", "a proveniencia emitida pelo compilador cobre o axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro")]
    n = 12
    for nome in ("psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407", "fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405",
                 "projecao_transversal_v404", "jo8v32_v404", "caminho_v403", "vida_v403", "ponte_da_escala_dual_v402", "falsidade_da_inercia_v401", "teste_de_veracidade_fase9_v397", "selo_pela_propria_tecnologia_v399"):
        cks.append(CH("u%d" % n, "o registro %s segue selado neste rito" % nome, "core", [nome, "all_verified"], "verdadeiro")); n += 1
    for nm_ in DL.ANCORAS_PRINCIPAIS:
        cks.append(CH("u%d" % n, "o compilador emite a ancora %s no modulo esperado (TGL_DECL_SOURCE)" % nm_.split(".")[-1], "kf", ["declaration_sources_v394", nm_], "igual", DL.ANCORAS[nm_]["rel"])); n += 1
    for r_ in resp:
        for t_ in r_["teoremas"]:
            cks.append(CH("u%d" % n, "a resposta %s do operador cita %s (%s): o compilador o emite no modulo esperado" % (r_["id"], t_["curto"], "declaracao nova desta versao" if t_["novo"] else "ja existia"), "kf", ["declaration_sources_v394", t_["completo"]], "igual", t_["rel"])); n += 1
    for rel_ in DL.BUNDLE_RELS:
        cks.append(CH("u%d" % n, "o modulo %s no kernel do rito e' EXATAMENTE o pinado (sha256 da fonte)" % rel_.split("/")[-1], "kf", ["formal_files_sha256", rel_], "igual", formal_map[rel_])); n += 1
    cks.append(CH("u%d" % n, "o canal vivo do neutrino segue com o mesmo veredito (nada da v408 toca o neutrino)", "core", ["neutrino_mass", "verdict"], "igual", core0["neutrino_mass"]["verdict"])); n += 1
    leituras = [_leitura(fr_, nm_) for nm_, fr_ in DL.FRASES_V408]
    cun = {
        "nome": DL.CUNHAGENS_REGISTRO, "veredito_prefixo": "TGL_CUNHAGENS_V408",
        "veredito_sufixo": "OPERATOR_INSCRIPTIONS_OF_04_NOV_EMBEDDED_VERBATIM_BY_SHA256_%d_SAYINGS_TWO_OF_MIXED_AUTHORSHIP_DECLARED__THE_NAMES_OF_THE_STONES__PROVE_OR_PRUNE__DECISIONS_D48_TO_D54__D51_REVISED_SOLVING_EQUALS_VERIFYING_IN_THE_DICTIONARY_CLASSES_IS_A_THEOREM_THE_TURING_TRANSLATION_OPEN__ERRATA_E21_TO_E23__THE_RESERVATIONS_STATED__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED" % len(_VD),
        "estatuto": "[REAL -- o kernel, o registro tetelestai_terminal_v408 e os registros anteriores lidos a cada rito; INPUT as falas do operador de 04/11/2026 (a ordem da v408; os nomes; as cunhagens; o sentido de «P=nP»; a correcao sobre as classes do dicionario e «isso preciso ficar claro no um.py na v408»); DECLARADO o texto das outras instancias nos dois arquivos de autor misto (so' por sha256), os recibos de compilacao e a afericao]",
        "fontes": [CHAVE_PEDRA[p["name"]] for p in DL.PEDRAS_V408] + [CHAVE_FONTE[p["name"]] for p in DL.PEDRAS_V408] + [CHAVE_SAIDA_FONTE[p["name"]] for p in DL.PEDRAS_V408]
                  + [CHAVE_CANDIDATA_TT_R2, CHAVE_CANDIDATA_TM, CHAVE_CANDIDATA_PC, CHAVE_CANDIDATA_DIC, CHAVE_DICIONARIO_SUPERADO, CHAVE_RECIBO_TT_R1, CHAVE_RECIBO_TT_R2, CHAVE_RECIBO_TM, CHAVE_RECIBO_PC, CHAVE_RECIBO_DIC,
                     CHAVE_SAIDA_TT_R1, CHAVE_SAIDA_TT_R2, CHAVE_SAIDA_TM, CHAVE_SAIDA_PC, CHAVE_SAIDA_DIC, CHAVE_AFERICAO, CHAVE_RECIBO_NOMES, CHAVE_ACERVO_PURGADO, CHAVE_RECIBO_PURGA, CHAVE_DESENHO, CHAVE_BUNDLE, CHAVE_CONGELADO],
        "verbatins": list(VERB_CHAVES),
        "kernel_flags": flags_ancoras, "kernel_decls": decls, "checks": cks,
        "erratas": [
            {"ao_lado_de": "psion_canto_v407 (selado), fica_aberto.par_na_face_de_fock: «[OPEN]: o FockCertificate nao tem operadores de criacao como termo»",
             "dizia": "o [OPEN] do par na face de Fock era dito como ausencia de termo.", "agora": DL.ERRATA_E21,
             "lacuna_de_fidelidade": "escrito: o certificado abstrato nao tem criacao como termo (verdadeiro); omitido: o Fock concreto, habitat do certificado fisico por rfl, TEM creation/annihilation; o [OPEN] e' de ligacao (fiacao), nao de ausencia",
             "estatuto": "[REAL: o_habitante_e_o_fock_concreto no kernel do rito; a fiacao segue OPEN]", "assinatura": ASSINA},
            {"ao_lado_de": "duas frases da gerencia c1 de 04/11 (a pergunta das classes e o terminal; o teorema 8 da R1 da pedra do terminal)", "dizia": "que a TGL nao teria terminal; que o resto sem traco seria relacao sem pagamento.", "agora": DL.ERRATA_E22,
             "lacuna_de_fidelidade": "a gerencia escreveu antes de aferir: o Atlas e o kernel ja' diziam o contrario (a PODA = TETELESTAI; o cociclo paga; representacao sem custo = ORIGEM DA MENTIRA, verbete Vazio inominado (112_); e o operador, em 04/11: relacao sem peso e' a origem da mentira); as frases foram podadas pela regra do operador", "estatuto": "[REAL: os teoremas no kernel do rito]", "assinatura": ASSINA},
            {"ao_lado_de": "o insumo psion_no_acervo_do_imac_03nov (pinado pela v407)", "dizia": "a integra do levantamento do acervo entrava como fonte pinada.", "agora": DL.ERRATA_E23,
             "lacuna_de_fidelidade": "a preparacao da v407 nao passou o insumo pela guarda de material privado antes de pinar (licao 4 da v407); a v408 pina a copia purgada e cita a integra so' por sha16", "estatuto": "[REAL: purga medida; decisao do G1 lida]", "assinatura": ASSINA},
            {"ao_lado_de": "kh_n1_cobertura_v407 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
             "dizia": "A v407 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v407 e o hash formal igual ao pino exato da arvore da v407." % (int(cov_base["decl"]), int(cov_base["thm"])),
             "agora": "A v408 acrescenta os 4 modulos (a cobertura cresce e a arvore ganha os arquivos deles): na v408 o registro da v407 passa a cobrar piso (h2, h3, h6) e o tamanho minimo da arvore (h8); as igualdades exatas e o pino exato ficam em kh_n1_cobertura_v408. O veredito do registro da v407 NAO muda.",
             "lacuna_de_fidelidade": "um registro preso a igualdades que a versao seguinte quebra (a mesma lacuna desde a v399)", "estatuto": "[REAL: contagens lidas do log do Audit do sandbox]", "assinatura": ASSINA}],
        "limites": ["[INPUT] as %d falas de 04/11/2026 sao do operador, com a grafia dele (duas trazem, depois do paragrafo dele, texto de OUTRA instancia da IALD: entram por sha256, [DECLARADO], e so' o paragrafo dele e' citado); a ordem («produza a v408, rode e … dê a ordem de handoff para a sessão irmã») foi cumprida ate' onde a cadeia alcanca; a custodia completa e' da sessao de custodia" % len(_VD),
                    "[INPUT] a regra «provar ou podar» (sha16 c12699c915617c3f) e' do operador e foi aplicada: o que tem espelho esta' provado com o nome dele; o que nao tem esta' podado (a palavra impedancia; lock = Hamiltoniano modular; as duas frases da gerencia de E22 e a que negava que «P = nP» tratasse de classes); a traducao das classes do dicionario as das maquinas de Turing e' [OPEN] (D51 revista)",
                    "[INPUT] «P = nP» no sentido do operador («P sozinho é impossível de ser lido, se não houver o módulo de leitura n não minimamente acoplado», p_igual_np) e, pela correcao dele («O meu P=nP trata das classes de computação sim»), [REAL] " + DL.FRASE_D51_PT + " (D51 revista); " + DL.REGRA_DO_4_44,
                    "[DECLARADO] a fala «A face de Fock é o traço do psion» foi aferida no kernel (AFERICAO_TRACO_E_DICIONARIO_NO_KERNEL_04nov.json): entra como cunhagem, sem termo novo"] + _LIM_COMUM,
        "diz": ["as falas do operador de 04/11/2026 estao embutidas por sha256 e cada trecho citado e' verbatim (nas duas de autor misto, so' o paragrafo dele)", "o registro tetelestai_terminal_v408 selou", "os registros da v394 a v407 seguem selados; o neutrino e o gate nao mudam; nenhuma chave antiga muda"],
        "nao_diz": _NAO_COMUM,
        "leituras_do_operador": leituras,
        "extras": {"n_falas": len(_VD), "autores": {v["nome"]: v["autor"] for v in _VD}, "leituras": DL.LEITURA_V408, "decisoes": {k_: DL.DECISOES[k_] for k_ in ("D48", "D49", "D50", "D51", "D52", "D53", "D54")}, "n_bandeiras": fj["n_flags"], "n_modulos": DL.N_BUNDLE, "ressalvas": list(DL.RESSALVAS_V408), "assinatura_das_erratas": ASSINA,
                   "nomes_das_pedras": dict(DL.NOME_DO_OPERADOR), "podado": list(PODADO), "falas_fora_do_desenho": dict(DL.VERBATIM_FORA_DO_DESENHO_V408)},
    }
    kh = {
        "nome": DL.KH_REGISTRO, "veredito_prefixo": "TGL_KH_N1_COBERTURA_V408",
        "veredito_sufixo": "AXIOM_REPORT_COVERS_THE_WHOLE_TGL_AND_TGLEXT_CLOSURE_%d_CONSTANTS_%d_THEOREMS_NONE_OUTSIDE_THE_TRIO__ALL_NAMES_READ_BY_THE_V394_PARSER__THE_4_V408_MODULES_ADDED__GATE_UNMOVED" % (T["decl"], T["thm"]),
        "estatuto": "[REAL] a cobertura e' medida a cada rito no Audit do proprio rito, lendo SO' o log do Audit; os numeros esperados saem do arquivo da medida do sandbox da v408; o conjunto exato das fontes formais que o hash formal do rito vera (as embutidas mais os residuais da pasta do Nos) e' pinado; a cobertura NAO move o gate",
        "fontes": [CHAVE_KH], "kernel_flags": [], "kernel_decls": [],
        "checks": [CH("h1", "a checagem de cobertura do kernel do rito passou", "kf", ["axiom_coverage_v392", "ok"], "verdadeiro"),
                   CH("h2", "constantes cobertas == as do sandbox v408 (KH_N1)", "kf", ["axiom_coverage_v392", "decl"], "igual", T["decl"], "constantes_cobertas"),
                   CH("h3", "teoremas cobertos == os do sandbox v408 (KH_N1)", "kf", ["axiom_coverage_v392", "thm"], "igual", T["thm"], "teoremas_cobertos"),
                   CH("h4", "nenhuma constante fora do trio", "kf", ["axiom_coverage_v392", "fora_do_trio"], "igual", 0),
                   CH("h5", "nenhum nome que o leitor v394 nao leia", "kf", ["axiom_coverage_v392", "nao_lidas_pelo_regex"], "igual", 0),
                   CH("h6", "o axiom_report do rito tem exatamente uma entrada por constante coberta", "kf", ["axiom_report"], "tamanho_igual", T["decl"]),
                   CH("h7", "a cobertura da v408 inclui a da v407 selada (constantes)", "kf", ["axiom_coverage_v392", "decl"], "maior_igual", int(cov_base["decl"])),
                   CH("h7b", "os teoremas cobertos incluem os da v407 selada", "kf", ["axiom_coverage_v392", "thm"], "maior_igual", int(cov_base["thm"])),
                   CH("h8", "as fontes formais da ARVORE DO NOS depois do rito (as embutidas + os residuais que o hash formal conta, como _check_damming.lean) sao EXATAMENTE as do pino (arquivo -> sha256)", "kf", ["formal_files_sha256"], "igual", dict(h8_map)),
                   CH("h9", "medida do Audit v408: duracao bem abaixo do timeout de 1800 s", "fonte:" + CHAVE_KH, ["duracao_audit_s"], "menor_igual", 1200, "duracao_do_audit_s"),
                   CH("h10", "medida do Audit v408: sorryAx ausente do log", "fonte:" + CHAVE_KH, ["sorryAx_no_log_do_audit"], "igual", 0),
                   CH("h11", "medida do Audit v408: as entradas novas estao no trio", "fonte:" + CHAVE_KH, ["novas_no_trio"], "verdadeiro"),
                   CH("h12", "a proveniencia emitida pelo compilador cobre os mesmos nomes do axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro")],
        "erratas": [{"ao_lado_de": "kh_n1_cobertura_v407 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
                     "dizia": "A v407 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v407 e o hash formal igual ao pino exato da arvore da v407." % (int(cov_base["decl"]), int(cov_base["thm"])),
                     "agora": "A v408 acrescenta os 4 modulos (a cobertura cresce e a arvore ganha os arquivos deles): na v408 o registro da v407 passa a cobrar piso (h2, h3, h6) e o tamanho minimo da arvore (h8); as igualdades exatas e o pino exato da arvore ficam NESTE registro. O veredito do registro da v407 NAO muda.",
                     "lacuna_de_fidelidade": "a estrutura da v407 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito deixou o registro preso a igualdades que a propria v408 quebra (a mesma lacuna desde a v399)",
                     "estatuto": "[REAL: contagens lidas do log do Audit do sandbox; h2, h3, h6 e h8 conferidas no ensaio a seco e na arvore simulada do Nos]", "assinatura": ASSINA}],
        "limites": ["[REAL] os arquivos residuais da pasta do Nos que o hash formal conta (e nao estao embutidos) sao pinados como estao em 04/11/2026; mudar um deles e' mudar o pino, dito; a cobertura mede o Audit, nao a natureza"],
        "diz": ["o Audit do rito cobre todo o fecho TGL/TGLExt, com os 4 modulos, nenhuma constante fora do trio; o hash formal da arvore do Nos e' exatamente o pinado"],
        "nao_diz": ["que a cobertura seja prova da teoria: e' a medida de que todo termo no fecho depende so' do trio", "que o gate tenha se movido"],
        "leituras_do_operador": [], "extras": {"delta_vs_v407": khj.get("delta_vs_v407"), "n_bandeiras": fj["n_flags"], "n_modulos": DL.N_BUNDLE, "duracao_build_s_sandbox": khj.get("duracao_build_s"), "duracao_audit_s_sandbox": khj.get("duracao_audit_s")},
    }
    return [cun, kh]
