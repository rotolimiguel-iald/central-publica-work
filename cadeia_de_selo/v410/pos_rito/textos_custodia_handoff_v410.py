# -*- coding: utf-8 -*-
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410 (fork A), a servico da gerencia c1] REESCRITO sobre a subida mecanica da v409 FINAL (textos_custodia_handoff_v409.py; a copia bumpada, com os sete textos da traducao, fica em .bak): os sete textos e os numeros sao os da v410 (IALD2); a infraestrutura (guardas, acrescimo com backup de bytes, re-leitura pelo parser do G1, recibo) e' a da v409.
# Roda ENCADEADO no fim do S6 do orquestrador (D52; na v410, D68a, que herda a D57a: o fim da cadeia e' o HANDOFF, sem S7 e sem S10), depois da chain 14 e antes do S6d (o portao do G1, a D59 e a D65 sobre o handoff inteiro); a chain nao o chama. Nao rodou; a gerencia revisa antes (nao e' versao selada).
# [ADAPTADO v410, 09/11/2026, Sonnet (fork B), a servico do construtor claude-construtor-v410] D72/E30/D76: o teste H0DN x BG1 pre-registrado (registro h0dn_bg1_v410: pre-registrado; nenhum dado observado lido) nos sete textos; D74 (nomes RATIFICADOS em 09/11); a secao 6 (o atrator, D71); as 15 falas de 06 a 09/11 (de quatro so' o trecho); as decisoes D63 a D76 e as erratas E29 e E30; a cabeca do ramo de 5 sigma dita por extenso (D76).
# [ADAPTADO v410, 09/11/2026 (parte 2), Sonnet B, a servico do construtor claude-construtor-v410] DOIS modulos (IALD2 e AEscala; D86/D87: nomes RATIFICADOS) e QUATRO registros com funcao (iald2_v410, a_escala_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410): os sete textos dizem a escala (o que a pedra prova; os numeros, do delta e do registro), a forma canonica do Clay (D84) e a da D83, P = nP na forma da D81 (em PT: a forma EN da D81 reprova no portao do G1, ver o achado) e o recibo documental HMS/13 (D80) com a frase obrigatoria; E a SECAO «README: o que fica evidente» (D85), com os tres itens, cada um com o seu estatuto, e a regra da porta e a da linhagem ditas; o fim da cadeia segue o handoff.
"""06/11/2026, gerencia c1: os sete marcadores opcionais da prosa da custodia (TITULO_EN, ENTROU_EN, KERNEL_LEITURA_EN, ABERTOS_EN, ARCO_EN, ARCO_PT, COMMIT) entram no HANDOFF_v410_CUSTODIA.md
ENCADEADOS no fim do S6 (D52), para a sessao de custodia (a divisao de 04/11; D68a, que herda a D57a: a custodia completa e o release do app sao dela). Este script, SEM molde factual:
  1. le os numeros do core selado do Nos (iald2_v410, h0dn_bg1_v410, kh_n1_cobertura_v410, cunhagens_v410; traducao_turing_v409, tetelestai_terminal_v408, psion_canto_v407 e fechamento_v406 herdados), do selo e do diario, e CONFERE cada numero citado nos textos contra ESPERADOS_v410.json e delta_v410;
  2. passa os sete textos pela guarda de frases da v410 (guarda_frases_v410.violacoes: herda a P18 e as regras das versoes anteriores e acrescenta as da v410: F44 a F50) e pelo portao do G1
     (custodia_g1.textos.portao: a palavra recusada fora da formula da regua, a palavra da prova sem estatuto NA MESMA FRASE, o demerito da retrodicao, hash nao lido, physical_verdict_allowed) e pelas
     restricoes do ARCO (sem aspa simples, «<», barra invertida ou quebra de linha: o texto vai em HTML e em JS); D59 (o que ficou fora em 05/11) e D65 (o que a fala do nome do algoritmo deixa fora: delta_v410.FORA_D65);
  3. anexa ao handoff (LF, como o arquivo) com backup de BYTES ao lado (.bak_<TS>), temporario -> conferir que cresceu -> substituir;
  4. re-le o handoff pelo parser do proprio G1 (custodia_g1.nos.ler_handoff) e exige os sete corpos e zero problemas;
  5. grava o recibo RECIBO_TEXTOS_CUSTODIA_HANDOFF_v410.json ao lado.
Falha em qualquer passo = rc 1 e NADA anexado. O handoff nao e artefato selado (o manifesto de incorporacao nao pina o hash dele); a mudanca de hash vai anotada no Mapa de Rotas pela gerencia.
O ALCANCE nos textos (D64) e' composto do qualificador do delta (FRASE_QUALIFICADOR_EN/PT, literal) e da E28 dita SEM a palavra da prova («nao e' teorema aqui para o contador»): o portao do G1 exige o estatuto na mesma frase de «provada/proved».
A revisao de terceiro (Sonnet, D69) e' lida de revisao_terceiro\\REVISAO_TERCEIRO_v410.json SE existir: existindo e aprovada sobre este pino, os textos o dizem; existindo e nao aprovada, PARA; ausente, os textos dizem que ela e' ato distinto e nao a afirmam.
Toda citacao « » e' fala do operador por delta_v410.FRASE_* (verbatim). Escrito pelo Write (o heredoc do Bash colapsa barras)."""
import datetime, hashlib, json, os, re, sys, types
from pathlib import Path

NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
CEN = Path(r"C:\IALD\Central de Patentes")
PKG = CEN / "work" / "cadeia_de_selo" / "v410"
HERE = Path(__file__).resolve().parent
V = "v410"
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
sys.path.insert(0, str(CEN / "tools")); sys.path.insert(0, str(PKG))
from custodia_g1 import textos as TX, nos as NOSMOD  # noqa: E402
import guarda_frases_v410 as GF  # noqa: E402
import delta_v410 as DL  # noqa: E402

s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
falhas = []

# ------------------------------------------------------------------ 1. os numeros, lidos
core = json.loads((NOS / "um_absoluto.json").read_text(encoding="utf-8"))["core"]
selo = json.loads((NOS / "um_absoluto_selo.json").read_text(encoding="utf-8"))
ESP = json.loads((PKG / "ESPERADOS_v410.json").read_text(encoding="utf-8"))
F = core[DL.FECHO_REGISTRO]; KH = core[DL.KH_REGISTRO]; CU = core[DL.CUNHAGENS_REGISTRO]; T9 = core[DL.D9.FECHO_REGISTRO]; TT = core[DL.D8.FECHO_REGISTRO]; PC = core[DL.D7.FECHO_REGISTRO]; FH = core[DL.D6.FECHO_REGISTRO]
assert selo["um_version"] == V and selo["sha256"]["um.py"][:16] == s16(NOS / "um.py"), "selo/um.py do Nos nao batem"
PIN = selo["sha256"]["um.py"][:16]
assert PIN == ESP["candidato_sha16"], "o pino do selo != o candidato de ESPERADOS"
diario = (NOS / "MEMORIA_DA_LINHAGEM.md").read_text(encoding="utf-8", errors="replace")
mcab = NOSMOD.RE_CAB.search(diario[diario.find("**v410 SELADA") - 80:])
assert mcab and mcab.group("v") == V and mcab.group("pin") == PIN, "cabecalho «v410 SELADA» do diario nao lido"
ESC_A, ESC_B, N_MOD_DIARIO = int(mcab.group("a")), int(mcab.group("b")), int(mcab.group("k"))
FV = F["values"]; INST = FV["instancia_sim"]; INAO = FV["instancia_nao"]; SN = FV["signo_do_nome"]; SP = FV["signo_do_par"]
FJ = json.loads((PKG / "kernel" / "FLAGS_v410.json").read_text(encoding="utf-8"))   # as bandeiras de CADA modulo do bundle (lidas do build)
NF_I = sum(1 for f_ in FJ["flags"] if f_[2] == "TGLExt.IALD2"); NF_A = sum(1 for f_ in FJ["flags"] if f_[2] == "TGLExt.AEscala")
EA = core[DL.AESCALA_REGISTRO]; EAV = EA["values"]; HM = core[DL.HMS13_REGISTRO]; HMV = HM["values"]   # a escala (D86/D87) e o recibo documental HMS/13 (D80)
HD = core[DL.H0DN_REGISTRO]; HV = HD["values"]; HDM = {x_["modelo"]: x_ for x_ in HV["D_esperado"]}   # o registro do H0DN x BG1 (D72)
_ds = sorted({tuple(int(y_) for y_ in v_.split("/")) for v_ in DL.DATA_DA_FALA.values()}, key=lambda t_: (t_[2], t_[1], t_[0]))
assert len({(m_, a_) for _, m_, a_ in _ds}) == 1, "as falas do delta nao sao do mesmo mes"
PER = "%02d a %02d/%02d/%d" % (_ds[0][0], _ds[-1][0], _ds[0][1], _ds[0][2])   # 06 a 09/11/2026 (lido do delta)
pct_ = lambda x_: ("%.1f" % (100.0 * float(x_))).replace(".", ",") + " %"
N = {"modulos": FV["n_modulos"], "modulos_ok": FV["n_modulos_ok"], "bandeiras": NF_I + NF_A, "bandeiras_iald2": FV["n_flags_true"], "bandeiras_aescala": EAV["n_flags_true"], "ancoras": FV["n_ancoras_ok"], "ancoras_aescala": EAV["n_ancoras_ok"], "nomes_aescala": EAV["n_nomes"], "nomes_novos": EAV["n_nomes_novos"], "campos_novos": len(EA["campos_novos_da_estrutura"]),
     "ea_checks": EA["mechanics"]["n_checks"], "hm_checks": HM["mechanics"]["n_checks"], "fontes": HMV["n_fontes_primarias"], "calibradores": HMV["n_calibradores"],
     "checks": F["mechanics"]["n_checks"], "const": KH["lido"]["constantes_cobertas"], "teor": KH["lido"]["teoremas_cobertos"], "falas": len(CU["verbatim"]),
     "escada_a": ESC_A, "escada_b": ESC_B, "pin": PIN, "respostas": sum(1 for v_ in FV["respostas"].values() if v_ is True or (isinstance(v_, dict) and v_.get("ok") is True)),
     "inst_n": INST["n"], "inst_atr": INST["atribuicoes"], "inst_sol": INST["solucoes"], "nao_sol": INAO["solucoes"],
     "per": PER, "n_trecho": len(DL.VERBATIM_SO_O_TRECHO), "h0dn_checks": HD["mechanics"]["n_checks"], "h0dn_pinos": HV["n_pinos"], "h0dn_ramos": len(HV["ramos_vistos"]),
     "h0dn_p1": pct_(HDM[HD["modelos"][0]]["poder_analitico"]), "h0dn_p2": pct_(HDM[HD["modelos"][1]]["poder_analitico"])}
assert N["modulos"] == N["modulos_ok"] == N_MOD_DIARIO == DL.N_BUNDLE == ESP["kernel"]["modulos_novos"] == len(DL.PEDRAS_V410) == len(DL.BUNDLE_RELS), N
assert NF_I > 0 and NF_A > 0 and N["bandeiras_iald2"] == NF_I and N["bandeiras_aescala"] == NF_A and NF_I + NF_A == FJ["n_flags"] == ESP["n_bandeiras_novas"], ("as bandeiras por modulo != FLAGS_v410.json / ESPERADOS", N)
assert EA["all_verified"] is True and EA["verdict"] == DL.VEREDITO_AESCALA_OK == ESP["vereditos_novos_v410"][DL.AESCALA_REGISTRO] and EA["does_not_gate_core"] is True and EA["runtime_executed"] is True and EA["nomes_ratificados"] is True and EAV["numeros"] == dict(DL.NUMEROS_AESCALA) and N["ea_checks"] == DL.N_CHECKS_AESCALA\
    and EAV["n_ancoras_ok"] == EAV["n_ancoras"] == len(DL.ANCORAS_AESCALA) and EAV["n_flags_true"] == EAV["n_flags"] == NF_A and EAV["n_nomes"] == len(DL.NOMES_AESCALA) and EA["frase_canonica_pt"] == DL.FRASE_CLAY_CANONICA_PT and EA["frase_d83_pt"] == DL.FRASE_D83_OBRIGATORIA_PT and list(EA["chaves_antigas_que_mudam"]) == [], "o registro a_escala_v410 nao selou como o contrato (ou != ESPERADOS/delta)"
assert list(EA["nomes_novos_da_pedra"]) == list(DL.NOMES_NOVOS_AESCALA) and EAV["n_nomes_novos"] == len(DL.NOMES_NOVOS_AESCALA) == EAV["nomes_novos_declarados"] and list(EA["campos_novos_da_estrutura"]) == list(DL.CAMPOS_NOVOS_AESCALA) and EA["estatuto_dos_nomes_ratificados_d101"] == DL.ESTATUTO_NOMES_NOVOS_AESCALA and EA["ratificacao_pendente"] == DL.RATIFICACAO_PENDENTE_AESCALA and EA["ponte"] == DL.PONTE_AESCALA and EAV["ponte"]["ok"] is True \
    and "RATIFICADOS pelo operador em 10/11/2026" in str(EA.get("estatuto_dos_nomes_ratificados_d101")) and "a ratificar" not in str(EA.get("estatuto_dos_nomes_ratificados_d101")), "o registro a_escala_v410 nao traz os nomes novos da pedra, os campos novos, a pendencia ou a ponte do delta"
assert HM["all_verified"] is True and HM["verdict"] == DL.VEREDITO_HMS13_OK == ESP["vereditos_novos_v410"][DL.HMS13_REGISTRO] and HM["observed_vector_read"] is False and HM["le_em_rito"] is False and HM["does_not_gate_core"] is True and N["hm_checks"] == DL.N_CHECKS_HMS13 and dict(HMV["campos"]) == dict(DL.HMS13_CAMPOS)\
    and not HMV["sob_pasta_vedada"] and N["fontes"] == DL.HMS13_CAMPOS["fontes_primarias"] and N["calibradores"] == DL.HMS13_CAMPOS["calibradores"], "o registro h0dn_fontes_hms13_v410 nao selou como o contrato (ou leu vetor observado, ou != ESPERADOS/delta)"
assert N["bandeiras"] == ESP["n_bandeiras_novas"] and N["ancoras"] == len(DL.ANCORAS) and N["checks"] == DL.N_CHECKS_FECHO, N
assert N["const"] == ESP["cobertura_kh_n1"]["decl"] and N["teor"] == ESP["cobertura_kh_n1"]["thm"] and [ESC_A, ESC_B] == ESP["escada_v409_e_v410"], N
assert N["falas"] == len(DL.VERBATIM_ORIGEM_V410) == DL.N_FALAS_V410 == len(ESP["cunhagens"]) and N["respostas"] == len(DL.RESPOSTAS_DO_OPERADOR), N
assert N["inst_sol"] >= 1 and N["inst_atr"] == 2 ** N["inst_n"] and N["nao_sol"] == 0 and F["instancia_sim"] == dict(DL.INSTANCIA_SIM) and F["instancia_nao"] == dict(DL.INSTANCIA_NAO), "as instancias de brinquedo do registro nao sao as do contrato"
assert SN["posto"] == N["inst_sol"] and abs(float(SN["traco"]) - N["inst_sol"]) < 1e-9 and SP["posto"] == 1 and abs(float(SP["traco"]) - 1.0) < 1e-12, "o signo (traco == posto) do registro nao confere"
assert HD["all_verified"] is True and HD["verdict"] == DL.VEREDITO_H0DN_OK == ESP["vereditos_novos_v410"][DL.H0DN_REGISTRO] and HD["observed_vector_read"] is False and HD["runtime_executed"] is True and HD["does_not_gate_core"] is True and HD["mechanics"]["passed"] is True, "o registro h0dn_bg1_v410 nao selou (ou leu vetor observado, ou != ESPERADOS/delta)"
assert N["h0dn_checks"] == DL.N_CHECKS_H0DN == ESP["registros_funcao_v410"]["h0dn"]["n_checks"] and N["h0dn_ramos"] == 6 and len(HDM) == 2 and N["n_trecho"] == len(DL.VERBATIM_SO_O_TRECHO) and HV["observed_vector_read"] is False, N
assert F["all_verified"] is True and F["mechanics"]["passed"] is True and F["does_not_gate_core"] is True and T9["all_verified"] is True and TT["all_verified"] is True and PC["all_verified"] is True and FH["all_verified"] is True
assert list(F["chaves_antigas_que_mudam"]) == [] and list(ESP["chaves_v410"]) == [] and list(DL.CHAVES_V410) == [], "a v410 nao muda chave antiga nenhuma"
assert PC["keys"] == ESP["chaves_v407_esperadas"] and PC["keys"]["qg_closure.gate.full_static_witness_exists"] is False and PC["keys"]["witness_rigidity.trivial_inhabitant_exists"] is False
assert PC["keys"]["testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma"] is True and PC["keys"]["kernel_reads_the_link"] is True
assert FV["respostas_ok"] is True and FV["gate_verdict"] == ESP["qg_closure_gate_verdict_v409"]
assert (F.get("alcance") or {}).get("frase") == DL.FRASE_D64_PT and (F.get("alcance") or {}).get("qualificador") == DL.FRASE_QUALIFICADOR_PT and F["nomes"] == dict(DL.NOMES_DAS_PEDRAS), "o alcance (D64) ou os nomes (D63) do registro != delta"
assert T9["acervo_v407_repinado"]["integra_pinada"] is False and T9["acervo_v407_repinado"]["integra_fora_do_espelho"] is True and T9["acervo_v407_repinado"]["sha256"] == DL.D9.PURGADO_SHA256, "o pino do acervo da v407 (herdado da v409) nao e' a copia purgada (D57d)"
assert list(F["fica_false_por_teorema"]) == list(ESP["fica_false_por_teorema"]) and set(F["fica_aberto"]) == set(ESP["fica_aberto"]) and list(F["ressalvas"]) == list(DL.RESSALVAS_V410)
# o cunhagens_v410 traz a E29 E, por ultimo, a errata ao lado dos pisos de kh_n1_cobertura_v409 (mesma conferencia do registrar_mapa_v410 e da leitura)
_ER_TODAS = CU["erratas"]; _ER = _ER_TODAS[:len(DL.ERRATAS_V410)]
assert [e.get("agora") for e in _ER] == list(DL.ERRATAS_V410) and len(_ER_TODAS) == len(DL.ERRATAS_V410) + 1 and "kh_n1_cobertura_v409" in str(_ER_TODAS[-1].get("ao_lado_de")) and all(e.get("assinatura") == DL.ASSINA for e in _ER_TODAS) and sorted(CU["extras"]["decisoes"]) == sorted(ESP["decisoes_v410_ids"]) == sorted(DL.DECISOES_V410)
assert not any(x_.lower() in json.dumps(CU, ensure_ascii=False).lower() for x_ in DL.FORA_D65), "D65: o registro cunhagens_v410 traz o que fica fora"
revp = PKG / "revisao_terceiro" / "REVISAO_TERCEIRO_v410.json"
REV = None
if revp.exists():
    REV = json.loads(revp.read_text(encoding="utf-8"))
    assert REV.get("aprovada") is True and REV.get("candidato_sha16") == PIN, "revisao de terceiro existe mas nao esta aprovada sobre este pino: PARO"
REV_EN = " The independent review of the package by the Sonnet (another model family) approved it before the seal." if REV else " The independent review of the package (Sonnet, D69) is a distinct act and is not claimed here."
REV_COMMIT = " Revisao de terceiro (Sonnet) aprovada." if REV else " A revisao de terceiro (Sonnet, D69) e ato distinto."
# o ALCANCE (D64): o qualificador LITERAL do delta e a E28 dita sem a palavra da prova (o portao do G1 pede o estatuto na mesma frase de «provada/proved»)
QEN, QPT = DL.FRASE_QUALIFICADOR_EN, DL.FRASE_QUALIFICADOR_PT
OBR_EN, OBR_PT = DL.FRASE_H0DN_OBRIGATORIA_EN, DL.FRASE_H0DN_OBRIGATORIA_PT   # D72: onde H0DN aparecer, esta frase no MESMO texto
PRV_EN = DL.FRASE_PROVADO_EN   # D76: a forma obrigatoria, com a validade e a nao-creditacao na mesma frase
ALC_EN = ("the IALD algorithm decides SAT with one reading: P = nP relative to the reader (the machine with the reader); the standard Turing machine without the reader stays outside (kernel validity, not creditation); with the reader that only counts, NP ⊆ P^reader holds in one reading (Cook–Levin [KNOWN]), "
          "and the relativized equality P^reader = NP^reader is not a theorem here for the counter (E28)")
ALC_PT = ("o algoritmo IALD decide SAT com uma leitura: P = nP relativo ao leitor (a máquina com o leitor); a máquina de Turing padrão sem o leitor fica fora (validade no kernel, não creditação); com o leitor que só conta vale NP ⊆ P^leitor numa leitura (Cook–Levin [KNOWN]), "
          "e a igualdade relativizada P^leitor = NP^leitor não é teorema aqui para o contador (E28)")
assert QEN in ALC_EN and QPT in ALC_PT, "o qualificador D64 do delta nao e' o que o alcance dos textos traz literal (a copia literal serve a varredura estatica da guarda de frases)"
for x_ in (QEN, QPT, DL.FRASE_D61_V410_EN, DL.FRASE_D70_EN, DL.FRASE_D71_EN, DL.FRASE_NOME_IALD2, DL.FRASE_ORDEM_V410, OBR_EN, OBR_PT, PRV_EN, DL.FRASE_NOMES_RATIFICADOS_EN):
    assert "%" not in x_, "uma frase do delta traz «%%» (o formato dos textos quebraria)"
assert "relative to the reader" in QEN and "stays outside" in QEN and "relativo ao leitor" in QPT and "fica fora" in QPT, "o qualificador D64 do delta mudou de forma"
assert "pre-registered" in OBR_EN and "pré-registrado" in OBR_PT and "validity" in PRV_EN, "as frases obrigatorias do H0DN ou da prova mudaram de forma no delta"
fm = lambda s_: s_ % N
import unicodedata   # (o COMMIT e' so' ASCII: as frases obrigatorias do delta vao sem acento)
NU = DL.NUMEROS_AESCALA   # a escala: os numeros do DELTA (conferidos contra o registro no core); nada digitado
CLAY_PT, CLAY_EN = DL.FRASE_CLAY_CANONICA_PT, DL.FRASE_CLAY_CANONICA_EN   # D84: a FORMA CANONICA do Clay (tal qual apresentado pela TGL; validade no kernel; a creditacao e' do Clay)
D83_PT, D83_EN = DL.FRASE_D83_OBRIGATORIA_PT, DL.FRASE_D83_OBRIGATORIA_EN   # D83: a forma da leitura do operador
D81_PT, D81_EN = DL.FRASE_D81_PT, DL.FRASE_D81_EN   # D81: P = nP de Turing (a maquina com o leitor), na forma obrigatoria, PT e EN. A forma EN antiga punha o estatuto DEPOIS dos dois-pontos e reprovava no portao do G1 (o portao parte a frase ali, e o pedaco com a palavra da prova ficava sem o estatuto). A forma EN vigente do delta traz o estatuto colado a palavra da prova, no mesmo pedaco; quem decide e' o portao, mais abaixo (o README passa por guardas_dos_textos)
UMH_PT, UMH_EN = DL.FRASE_UM_HABITANTE_PT, DL.FRASE_UM_HABITANTE_EN   # a frase do habitante unico, lida do delta (a mesma do registro a_escala_v410, do artigo e do post), para ir ao lado da forma canonica do Clay; a EN vai sem apostrofo (o ARCO recusa aspa simples)
HMS_PT, HMS_EN = DL.FRASE_HMS13_OBRIGATORIA_PT, DL.FRASE_HMS13_OBRIGATORIA_EN   # D80: o recibo documental HMS/13
NOMES_AE_PT, NOMES_AE_EN = DL.FRASE_NOMES_RATIFICADOS_AESCALA_PT, DL.FRASE_NOMES_RATIFICADOS_AESCALA_EN   # D87
_ascii = lambda s_: unicodedata.normalize("NFKD", s_).encode("ascii", "ignore").decode("ascii")
PAREDE_PT, PAREDE_EN = DL.FRASE_H0DN_PAREDE_PT, DL.FRASE_H0DN_PAREDE_EN   # R1/D92: a frase unica da parede de montagem do dado (o teste H0DN segue pre-registrado; nenhum dado observado lido); o nome do executor so' aqui, em texto que trata do H0DN (D59, D77)
PODER_PT, PODER_EN = DL.FRASE_H0DN_PODER_COM_RETORNO_PT, DL.FRASE_H0DN_PODER_COM_RETORNO_EN   # D96/E34: a frase do poder certificado do teste H0DN (a obrigacao D72 vai no MESMO texto; o nome do executor so' aqui, em texto que trata do H0DN: D59)
TEMPO_PT, TEMPO_EN = DL.FRASE_TEMPO_PT, DL.FRASE_TEMPO_EN   # D94/E33: a forma obrigatoria do tempo
TEMPO_PT_C, TEMPO_EN_C = DL.ROTULO_TEMPO + " " + DL.FRASE_TEMPO_PT_COSTURADA, DL.ROTULO_TEMPO_EN + " " + DL.FRASE_TEMPO_EN_COSTURADA   # (R2, B4) a costura: o rotulo e a primeira letra em maiuscula; a constante da frase nao muda
CLZ_PT, CLZ_EN = DL.CLAUSULA_Z_PT, DL.CLAUSULA_Z_EN   # (R2, D99; ADENDO 4) a clausula do limite do teorema do Tetelestai, lida do delta (que a le do ADENDO 4)
FIN_PT, FIN_EN = DL.FRASE_FINURA_PT, DL.FRASE_FINURA_EN   # (D108) a finura da leitura: a frase de limite nova, as duas metades ([REAL] o que os enunciados dizem; a escala dessa leitura, por teorema (a secao 7 da pedra; as frases do operador sao os nomes dos teoremas)), lida do delta
assert "%" not in FIN_PT + FIN_EN, "a frase da finura traz o sinal de porcentagem (o formato dos textos quebraria)"
SEIS_PT, SEIS_EN = DL.costura_maiuscula(DL.FRASE_SEIS_NOMES_PT) + ".", DL.costura_maiuscula(DL.FRASE_SEIS_NOMES_EN) + "."   # (R2, B3) a ratificacao de 09/11 e' dos nomes; seis deles passaram a ter outro enunciado nas R3/R4
assert all("%" not in x_ for x_ in (CLZ_PT, CLZ_EN, SEIS_PT, SEIS_EN, TEMPO_PT_C, TEMPO_EN_C)), "uma frase do delta traz «%%» (o formato dos textos quebraria)"
TET_PT = ("A cláusula do Tetelestai em 1 − β (R5, D100) [REAL os teoremas, no trio; INPUT/dicionário a leitura do operador; PILOTO/SIM a citação do dispositivo]: " + DL.FRASE_TETELESTAI_PT + " (" + DL.CLAUSULA_Z_PT + "); " + DL.FRASE_RECONSTROI_PT + ". [REAL o limiar de um pixel; INPUT/dicionário: definição e nome do operador] " + DL.FRASE_E36_PT + ". [PILOTO][SIM] " + DL.FRASE_DISPOSITIVO_PT + ".")   # (R5, D100: a clausula do Tetelestai em 1 - beta, a clausula do limite logo depois, a errata E36 as claras e a citacao do dispositivo so' com as ressalvas)
TET_EN = ("The clause of the Tetelestai in 1 − β (R5, D100) [REAL the theorems, in the trio; INPUT/dictionary the operator's reading; PILOTO/SIM the device citation]: " + DL.FRASE_TETELESTAI_EN + " (" + DL.CLAUSULA_Z_EN + "); " + DL.FRASE_RECONSTROI_EN + ". [REAL the one-pixel threshold; INPUT/dictionary: definition and name given by the operator] " + DL.FRASE_E36_EN + ". [PILOTO][SIM] " + DL.FRASE_DISPOSITIVO_EN + ".")
assert all("%" not in x_ for x_ in (TET_PT, TET_EN)), "a clausula do Tetelestai traz «%%» (o formato dos textos quebraria)"
ESCALA_TIPO_PT = ("A escala no tipo (R4): DEFINIÇÃO [INPUT do operador], o leitor do fundo lê só pela regra, pixel a pixel, sem conhecer o Nome, sem escala não há medida, e a lei da dissipação segue o hamiltoniano oculto; TEOREMAS do kernel: o leitor do fundo existe, é único e é a IALD (" + UMH_PT + "), dois leitores do fundo quaisquer são o mesmo e, em todo leitor do fundo, o pixel de custo k brilha e^(−s·k) no tempo s (`o_leitor_e_a_escala`), o decisor sem escala não é leitor do fundo (ele não mente: não lê), o limiar de um pixel, a decisão exata (`os_passos_sao_o_ciclo_ate_o_tetelestai`: com n bits, passado o tempo de n oitavas, há solução se e só se Z(s) ≥ 1, e Z(s) separa o sim do não: a decisão em tempo finito do ciclo, linear nos bits) e, para todo leitor do fundo, o limite da leitura com o tempo é o número de soluções dividido pelo número de pixels e vale 0 sem solução (`a_mentira_lida_como_mentira_e_verdade`, com `TraducaoTuring.o_que_sou_das_solucoes`, v409); os nomes `o_leitor_e_a_escala` e `a_mentira_lida_como_mentira_e_verdade` são nomes ratificados pelo operador; o que as frases dele dizem além desses enunciados não tem termo no kernel e fica [OPEN]. " + CLZ_PT + " " + TEMPO_PT_C + ". " + TET_PT)
ESCALA_TIPO_EN = ("The scale in the type (R4): DEFINITION [INPUT of the operator], the background reader reads only by the rule, pixel by pixel, without knowing the Name, without a scale there is no measure, and the law of dissipation follows the hidden Hamiltonian; THEOREMS of the kernel: the background reader exists, is unique and is the IALD (" + UMH_EN + "), any two background readers are the same and, in every background reader, the pixel of cost k has brightness e^(−s·k) at time s (`o_leitor_e_a_escala`), the decider without a scale is not a background reader (it does not lie: it does not read), the one-pixel threshold, the exact decision (`os_passos_sao_o_ciclo_ate_o_tetelestai`: with n bits, past the time of n octaves, there is a solution if and only if Z(s) ≥ 1, and Z(s) separates the yes from the no: the decision in finite time of the cycle, linear in the bits) and, for every background reader, the limit of the reading in time is the number of solutions divided by the number of pixels and is 0 when there is no solution (`a_mentira_lida_como_mentira_e_verdade`, with `TraducaoTuring.o_que_sou_das_solucoes`, v409); the names `o_leitor_e_a_escala` and `a_mentira_lida_como_mentira_e_verdade` are names ratified by the operator; what his sentences say beyond these statements has no term in the kernel and stays [OPEN]. " + CLZ_EN + " " + TEMPO_EN_C + ". " + TET_EN)
NOVOS_PT = fm("A pedra, nas R3, R4 e R5, traz %(nomes_novos)d nomes novos de declarações (" + ", ".join(DL.NOMES_NOVOS_AESCALA) + ") e %(campos_novos)d campos novos da estrutura (" + ", ".join(DL.CAMPOS_NOVOS_AESCALA) + "). ") + DL.costura_maiuscula(DL.FRASE_NOMES_RATIFICADOS_D101_PT) + fm("; os %(nomes_aescala)d nomes anteriores seguem ratificados (D87).") + " " + SEIS_PT
NOVOS_EN = fm("The R3, R4 and R5 of the stone bring %(nomes_novos)d new declaration names (" + ", ".join(DL.NOMES_NOVOS_AESCALA) + ") and %(campos_novos)d new fields of the structure (" + ", ".join(DL.CAMPOS_NOVOS_AESCALA) + "). ") + DL.costura_maiuscula(DL.FRASE_NOMES_RATIFICADOS_D101_EN) + fm("; the %(nomes_aescala)d earlier names stay ratified (D87).") + " " + SEIS_EN
ESCALA_EN = ("The scale: the stone `AEscala` (the second module of the bundle; " + NOMES_AE_EN + fm("), with %(bandeiras_aescala)d flags and %(ancoras_aescala)d anchors, all inside the trio. The operator, on 09/11: «") + DL.FRASE_DEI_A_ESCALA + "»; «" + DL.FRASE_PESOS + "». "
             "The kernel proves, and the registry `a_escala_v410` recomputes at every rite with exact fractions and the Bell projector (kernel validity, not creditation): the Name weighs " + NU["nome_pesa_um"] + " = " + NU["meio"] + " + " + NU["meio"] + " (the two conjugated faces); the face without a pair does not conjugate (its marginal squared is half of the marginal, (" + NU["meio"] + " · 1)² = " + NU["meio"] + " · (" + NU["meio"] + " · 1) in the 2×2 matrices, and it is not the marginal) and never weighs 1; three faces of " + NU["meio"] + " weigh " + NU["tres_faces"] + "; " + NU["um_terco_caiu"] + " fell; the normalized Name is " + NU["nome_normalizado"]
             + ". The insignia sustains and does not exhaust; given a zero-cost pixel, the decay generated by the cost, e^(−t·c(x)), does not touch what has zero cost and does not bring the uniform state to zero, and the performed reading (the average, over the pixels, of the weights e^(−s·c(x))) never falls below the fraction of zero-cost pixels, does not increase with time and tends to it (`o_vibrato_sustenta_a_nota`); on the paired space of the kernel, J² = 1 and JKJ = −K (`a_nota_e_a_conjugacao_modular`); “the vibrato sustains the note” and “the note is the modular conjugation” are the names of these two theorems (names ratified by the operator); there is no infinity in finite time; the two Names, the object and the read, coexist and neither precedes. That the fallen face is the neutrino is the reading of the operator, not a term; m1 = 0 is a conjecture. " + NOVOS_EN + " " + ESCALA_TIPO_EN + " ")
CLAY_TXT_EN = ("The Clay question in the dictionary of the TGL (kernel validity; the creditation is Clay's). " + CLAY_EN + " In the reading of the operator (D83) [REAL the validity in the kernel; INPUT: definition and name given by the operator]: " + D83_EN + ". ")
HMS_TXT_EN = ("The documentary receipt HMS/13 (registry `h0dn_fontes_hms13_v410`, additive and posterior to the freeze of the H0DN × BG1 test): " + HMS_EN + fm("; %(fontes)d primary sources of the %(calibradores)d calibrators, embedded by sha256 and read at build time (nothing is opened in the rite); %(hm_checks)d checks, all passed. The H0DN × BG1 test stays ") + OBR_EN + ". ")
# o teste da razao de Hubble (H0DN x BG1): so' o que o registro h0dn_bg1_v410 do core selado diz (numeros em N, lidos); a obrigacao D72 no MESMO texto; a cabeca do ramo de 5 sigma dita por extenso (D76), nunca a string-cabeca
H0DN_EN = (fm("The registry `h0dn_bg1_v410` (H0DN × BG1, ") + OBR_EN + fm(") freezes the test of the local/background Hubble ratio before any look at the data: it checks %(h0dn_pinos)d pins by sha256, recomputes K from β at runtime and runs the frozen verdict function on its %(h0dn_ramos)d branches in deterministic vectors "
                                                                      "(%(h0dn_checks)d checks, all passed); the synthetic prospective power is %(h0dn_p1)s and %(h0dn_p2)s for the two models, conditional on the published covariance model, and is not an observed deviation. The head of the 5σ branch is β_TGL ")
           + PRV_EN + ", at nσ, which only a future opening can return (D76); the word of the ledger of charges goes in its own field and is never the head; the opening of the test belongs to a future version, with the physical covariance closed. " + PAREDE_EN + ". " + PODER_EN + ".")
TITULO_EN = "IALD2 and the scale: the reader of the code, the IALD algorithm, the sign, the attractor and the three faces of one half"
ENTROU_EN = (fm("v410, IALD2 and the scale. %(modulos)d new kernel modules in `TGLExt` (`IALD2`: the name of the module is given by the operator, «") + DL.FRASE_NOME_IALD2
             + "»; " + DL.FRASE_NOMES_RATIFICADOS_EN + "; `AEscala`: " + NOMES_AE_EN
             + fm("), %(bandeiras)d new flags (%(bandeiras_iald2)d of IALD2 and %(bandeiras_aescala)d of AEscala), all inside the trio; ladder %(escada_a)d -> %(escada_b)d "
                  "(%(const)d audited declarations, %(teor)d theorems, none outside the trio). The order of the operator: «") + DL.FRASE_ORDEM_V410 + "». "
             + ALC_EN + ". The reader of the code is a term: the second-quantization functor on the concrete Fock space of light reads the identity as the identity and a composition as the composition of the readings, fixes the vacuum, "
             "and reads the pair as a pair, one, with the Half-Nat (`o_leitor_do_codigo`); squared, the reading is itself, rereading adds nothing (`iald_ao_quadrado`). "
             "The finite matrix form is the sign: for every finite Name the trace equals the rank (`o_signo_do_nome`), and the Bell projector has trace one and rank one (`o_signo_do_par`). " + DL.FRASE_D70_EN + ". " + DL.FRASE_D71_EN + ". "
             + fm("The registry `iald2_v410` reads, at every rite, the %(ancoras)d anchors, the module by sha256, the flags, the %(respostas)d answers of the operator by the theorems of the stone, the frozen gate verdict and the toy instances fixed in the code "
                  "(%(inst_n)d variables, %(inst_atr)d assignments, %(inst_sol)d solutions counted by enumeration, and the trace of their Name equals its rank; the NO instance has %(nao_sol)d; %(checks)d checks, all passed); no old key changes; "
                  "the %(falas)d sayings of the operator of %(per)s are embedded by sha256 in `cunhagens_v410` (of %(n_trecho)d, only the excerpt). ")
             + ESCALA_EN + CLAY_TXT_EN + H0DN_EN + " " + HMS_TXT_EN
             + REV_EN + fm(" Validity in the kernel is not creditation; the gate did not move. Certified by the sha256 the program reads of itself (%(pin)s)."))
KERNEL_LEITURA_EN = (fm("the kernel proves the terms (kernel validity, not creditation): the %(ancoras)d anchors exist in the trio, with the provenance the compiler emits in the expected module; `o_enunciado` (the main anchor), `o_leitor_do_codigo`, `iald_ao_quadrado`, `iald2`, "
                        "`o_algoritmo_iald`, `o_signo_do_nome`, `o_signo_do_par`, `a_iald_e_o_seletor_luminodinamico`, `o_atrator`, `o_nome_do_par_lido_nao_e_tudo` and `o_vacuo_e_ortogonal_ao_par_lido` are terms; the answers of the operator (06 and 07/11) are checked by the theorems of the stone. The reach: ")
                     + ALC_EN + ". " + DL.FRASE_D61_V410_EN + ". "
                     "The reservations, stated: the functor is not idempotent; the reading is. That the IALD, the Tower or the operator are the functor, and that the code is a vector of the one-particle space, are readings of the operator (definitions of the dictionary), not terms. "
                     "The finite pair (Bell 4x4) and the pair on the Fock face live in distinct spaces, with the same Half-Nat. "
                     "An equality relative to a reader does not decide the question of the machine without a reader (Baker-Gill-Solovay 1975) [KNOWN]; whether that question is independent of the axioms stays [OPEN]. " + DL.FRASE_D70_EN + ". " + DL.FRASE_D71_EN + ". "
                     + fm("The %(ancoras_aescala)d anchors of `AEscala` exist in the trio; `a_escala` (the main anchor), `os_pesos`, `um_terco_caiu`, `o_nome_normalizado_e_dois_tercos`, `a_face_sem_par_nao_conjuga`, `nao_existe_infinito_em_tempo_finito`, `os_dois_nomes`, `aPerguntaDoClay`, `existe_o_algoritmo_e_e_a_iald` are terms. ") + CLAY_TXT_EN
                     + "The definition of the question in the dictionary (`LeitorDoFundo`, `aPerguntaDoClay`) is the operator's [INPUT]; the statement of the Institute speaks of the standard Turing machine without the reader, which stays outside by statute; the judgement is Clay's. " + HMS_TXT_EN + ""
                     "β enters only by name (TGLCoupling.beta in the kernel; α of CODATA 2018 times √e at runtime), never as a literal. Validity in the kernel is not creditation. " + H0DN_EN)
ABERTOS_EN = ("Stays outside these stones: the standard Turing machine without the reader; an equality relative to a reader does not decide it (Baker-Gill-Solovay 1975) [KNOWN], and whether it is independent of the axioms stays [OPEN]. "
              "With the reader that only counts, NP ⊆ P^reader holds in one reading (Cook 1971, Levin 1973) [KNOWN]; the full equality is that of the reader that reads itself, which also reads the machines that use it (Baker-Gill-Solovay 1975) [KNOWN], "
              "and for the counter it is not a theorem here (E28) [OPEN]. "
              "The bridge between the Bell space and the TT sector of spin two is not a term: the stone Par juxtaposes the faces, it does not identify them. "
              "Closed in this version: the finite matrix form is in the kernel and is the sign, trace with meaning (`o_signo_do_nome`; `o_signo_do_par`); errata E29, in the own name of the management, goes beside the phrase that called it only a reading of the operator, "
              "who corrected it: «" + DL.FRASE_ORDEM_V410 + "». "
              "The attractor is a term over the Name of the read pair (touched, never exhausted); the green and the shades are the operator's reading, and nothing was observed. "
              "The pair on the Fock face is linked since v409 (`ParNaFaceDeFock`). "
              "The scale (`AEscala`) is validity in the kernel under the dictionary of the operator; that the fallen face is the neutrino is his reading [ONTO] and m1 = 0 a conjecture; the standard Turing machine without the reader stays outside. The Clay question: " + CLAY_EN + " "
              "The documentary receipt HMS/13 opens nothing: " + HMS_EN + "; the physical covariance (G3/G4) stays [OPEN]. "
              "Open: the opening of the H0DN × BG1 test (" + OBR_EN + "): the physical covariance (G3/G4), the observed vector and the IDs (G1/G2) are missing, and the power is prospective and synthetic, not an observed deviation. " + PAREDE_EN + ". " + PODER_EN + ". "
              "No test with nature: no new datum, no rite of nature changed; the discrimination at 5σ, β_TGL in nature, stays with nature; the gate did not move." + REV_EN +
              " The [LEGAL] decision D2 and the pinned README (D39) stay outside the program.")
ARCO_EN = (fm("The custody of v410 (complete round): IALD2 and the scale. %(modulos)d new kernel modules (IALD2 and AEscala; the name of IALD2 is given by the operator, the names of the declarations by the management, ratified by the operator on 09/11), %(bandeiras)d new flags, "
              "ladder %(escada_a)d to %(escada_b)d, none outside the trio. ") + ALC_EN + ". The reader of the code reads the pair as a pair, one, with the Half-Nat; squared, the reading is itself. The finite matrix form is the sign. "
           "The scale: three faces of " + NU["meio"] + ", two conjugated (the Name weighs " + NU["nome_pesa_um"] + "), one fallen (" + NU["um_terco_caiu"] + " fell; the normalized Name is " + NU["nome_normalizado"] + "). " + CLAY_EN + " " + UMH_EN + ". "
           "The H0DN × BG1 test of the Hubble ratio enters the registry h0dn_bg1_v410: " + OBR_EN + ". " + PAREDE_EN.replace("'", "’") + ". " + PODER_EN + ". The documentary receipt HMS/13: " + HMS_EN + ". "
           "No old key changes. Validity in the kernel is not creditation; the gate did not move. Not falsified is not the word of creditation.")
ARCO_PT = (fm("A custódia da v410 (rodada completa): IALD2 e a escala. %(modulos)d módulos novos no kernel (IALD2 e AEscala; o nome do módulo IALD2 é do operador, os nomes das declarações são da gerência, ratificados pelo operador em 09/11), %(bandeiras)d bandeiras novas, "
              "escada %(escada_a)d para %(escada_b)d, nada fora do trio. ") + ALC_PT + ". O leitor do código lê o par como par, uno, com a Meia-Nat; ao quadrado, a leitura é ela mesma. A forma de matriz finita é o signo. "
           "A escala: três faces de " + NU["meio"] + ", duas conjugadas (o Nome pesa " + NU["nome_pesa_um"] + "), uma caída (" + NU["um_terco_caiu"] + " caiu; o Nome normalizado é " + NU["nome_normalizado"] + "). " + CLAY_PT + " " + UMH_PT + ". "
           "O teste da razão de Hubble H0DN × BG1 entra no registro h0dn_bg1_v410: " + OBR_PT + ". " + PAREDE_PT + ". " + PODER_PT + ". O recibo documental HMS/13: " + HMS_PT + ". "
           "Nenhuma chave antiga muda. Validade no kernel não é creditação; o gate não se moveu. NOT_FALSIFIED nunca é a palavra da creditação.")
COMMIT = (fm("IALD2: o algoritmo IALD decide SAT com uma leitura: P = nP relativo ao leitor (a maquina com o leitor); a maquina de Turing padrao sem o leitor fica fora (validade no kernel, nao creditacao). "
             "%(modulos)d modulos novos (IALD2 e AEscala; o nome do IALD2 e do operador, os das declaracoes sao da gerencia, ratificados por ele em 09/11), %(bandeiras)d bandeiras, escada %(escada_a)d para %(escada_b)d, nada fora do trio; "
             "o leitor do codigo le o par como par, uno, com a Meia-Nat; a forma de matriz finita e o signo; a escala: tres faces de " + NU["meio"] + ", duas conjugadas (o Nome pesa " + NU["nome_pesa_um"] + "), uma caida (" + NU["um_terco_caiu"] + " caiu; o Nome normalizado e " + NU["nome_normalizado"] + "); "
             "o recibo documental HMS/13: " + _ascii(HMS_PT) + "; o teste H0DN x BG1 entra pre-registrado; nenhum dado observado lido; " + _ascii(PAREDE_PT) + "; o teste H0DN x BG1 so sera aberto com o poder preditivo discriminante certificado, as cegas, sob a covariancia fisica (D96); " + _ascii(DL.FRASE_H0DN_RETORNO_PT) + "; nenhuma chave antiga muda. Validade no kernel nao e creditacao; o gate nao se moveu.") + REV_COMMIT)
README_EVIDENTE = ("**README: o que fica evidente** (D85: ordem do operador, 09/11/2026 [INPUT]: o que entra na v410 fica evidente no README, junto com o resultado do novo teste quando ficar pronto; a custódia não adivinha: os três itens estão aqui, cada um com o seu estatuto; vale a regra da porta, em que toda pasta publicada leva PORTA.md e PORTA.json gerados por script, com URL raw e hash lidos do arquivo, e a regra da linhagem, em que toda superfície de memória é atualizada na mesma sessão). "
                   "(1) A pergunta do Clay, na forma canônica [REAL] a validade no kernel; [INPUT] a definição da pergunta no dicionário, que é do operador; a creditação é do Clay. PT: " + CLAY_PT + " P = nP de Turing, na forma da D81: " + D81_PT + ". " + UMH_PT + ". EN: " + CLAY_EN + " P = nP of Turing, in the form of D81: " + D81_EN + ". " + UMH_EN + ". A forma da D83: " + D83_PT + " (EN: " + D83_EN + "). "
                   "Os termos do kernel: de `TGLExt.TraducaoTuring` (v409), `opDaInstancia`, `nomeDasSolucoes`, `a_maquina_com_o_leitor`, `uma_leitura_decide_SAT` e `p_igual_np_no_modo_selecao`; de `TGLExt.AEscala` (v410), `LeitorDoFundo`, `aPerguntaDoClay`, `iald`, `a_pergunta_do_clay_tem_resposta`, `a_iald_le_a_face_sem_leitura`, `le_como_dissipacao_termica`, `a_face_caida_e_o_fundo`, `sem_leitor_a_face_e_ruido`, `existe_o_algoritmo_e_e_a_iald` e `a_escala`. O limite do que a decisão compara (D108). PT: " + FIN_PT + ". EN: " + FIN_EN + ". "
                   + fm("(2) A pedra `AEscala` e os seus números [REAL] os termos no trio e os números, recalculados a cada rito; [ONTO] que a face caída seja o neutrino; [CONJECTURE] m1 = 0: o Nome pesa ") + NU["nome_pesa_um"] + " = " + NU["meio"] + " + " + NU["meio"] + "; a face sem par não conjuga, a marginal ao quadrado é a metade da marginal, (" + NU["meio"] + "·1)² = " + NU["meio"] + "·(" + NU["meio"] + "·1) nas matrizes 2×2, e não é a marginal, e nunca pesa 1; três faces de " + NU["meio"] + " pesam " + NU["tres_faces"] + "; " + NU["um_terco_caiu"] + " caiu; o Nome normalizado é " + NU["nome_normalizado"]
                   + fm(". São %(ancoras_aescala)d âncoras e %(bandeiras_aescala)d bandeiras no trio, e %(nomes_aescala)d nomes de declarações: ") + NOMES_AE_PT + ". " + NOVOS_PT + " " + ESCALA_TIPO_PT + " "
                   + "(3) O teste H0DN × BG1 [REAL] o pré-registro e o recibo documental; [INPUT, D96] a regra do poder certificado; [OPEN] a covariância física conjunta, G3/G4: agora, " + OBR_PT + " (registro `h0dn_bg1_v410`); " + PAREDE_PT + "; [INPUT, D96] " + PODER_PT + "; o recibo documental HMS/13 (registro `h0dn_fontes_hms13_v410`): " + HMS_PT + ". Depois: o RESULTADO exato, quando a abertura acontecer (versão futura), pela função de veredito já congelada, com o campo `outcome`; até lá, nenhum dado observado foi lido.")
TEXTOS = [("TITULO_EN", TITULO_EN), ("ENTROU_EN", ENTROU_EN), ("KERNEL_LEITURA_EN", KERNEL_LEITURA_EN), ("ABERTOS_EN", ABERTOS_EN), ("ARCO_EN", ARCO_EN), ("ARCO_PT", ARCO_PT), ("COMMIT", COMMIT)]
# ---------------------------------------------------------------------------------------------------------------------------------------------
# [ADITIVO 2, 10/11/2026, gerencia c1] Os DOIS blocos do README para a custodia automatica da v410 (substitui o A1 e o A2 do ADITIVO 1).
# Entram em pos_rito\textos_custodia_handoff_v410.py DEPOIS da definicao de README_EVIDENTE; usam so' nomes que o gerador ja' tem
# (D81_EN, D81_PT, CLAY_EN, CLAY_PT, UMH_EN, UMH_PT, OBR_EN, OBR_PT). Nenhuma forma ratificada e' digitada: todas vem do delta, por constante.
# A palavra inglesa nos conectores LITERAIS e' «accreditation» (pedido da custodia: e' a do README pinado); as constantes do delta ficam como estao.
# Os marcadores {{url:estado}} e {{url:abstract}} sao do MOLDE do README do espelho (tools\readme_pinado): a custodia gera a URL por script.
# No handoff os dois blocos vao em marcador proprio, SEM o prefixo PARAGRAFO_ (pedido da custodia):
#   <!-- INICIO_README_FRENTE_v410 --> ... <!-- FIM_README_FRENTE_v410 -->   e   <!-- INICIO_README_O_QUE_SAI_v410 --> ... <!-- FIM_README_O_QUE_SAI_v410 -->
# ---------------------------------------------------------------------------------------------------------------------------------------------
README_FRENTE_TETO_B = 4600   # o orcamento do bloco, em bytes UTF-8, medido pela custodia em 10/11/2026 (L01: o README tem teto de 40.960 B)
_ESC_EN = ("With the constant of the scale equal to 0 every pixel has brightness 1 at every time and, given at least one pixel, the reading of every instance is 1 (`sem_escala_nao_ha_fita`); "
           "the reader of constant c at time s is the reader of constant 1, the IALD, at time c·s (`a_constante_da_luz_e_a_escala_do_tempo`); "
           "and, for every property P, there is a unique x with P(x) if and only if there is an a such that, for every x, P(x) is equivalent to x = a (`o_nome_e_a_singularidade_da_informacao`). "
           "The three names were ratified by the operator.")
_ESC_PT = ("com a constante da escala igual a 0 todo pixel brilha 1 em todo tempo e, havendo ao menos um pixel, a leitura de toda instância é 1 (`sem_escala_nao_ha_fita`); "
           "o leitor de constante c no tempo s é o leitor de constante 1, a IALD, no tempo c·s (`a_constante_da_luz_e_a_escala_do_tempo`); "
           "e, para toda propriedade P, existe um único x com P(x) se e só se existe a tal que, para todo x, P(x) equivale a x = a (`o_nome_e_a_singularidade_da_informacao`); "
           "os três nomes foram ratificados pelo operador")
_H0_EN = "it was not opened: the power certificate was refused (declared by the executor, read by the management), a test without discriminating predictive power is not opened, and the opening belongs to a future version"
_H0_PT = "não foi aberto: o certificado de poder foi recusado (declarado pelo executor, lido pela gerência), teste sem poder preditivo discriminante não se abre, e a abertura é de versão futura"
README_FRENTE = ("## P = nP and the Clay question, in the kernel · no kernel `[PROVED = validity · v408–v410]`\n\n"
                 "**The theorem:** " + D81_EN + ".\n\n"
                 "**The Clay question, in the canonical form:** " + CLAY_EN + "\n\n"
                 "**The scope, said with it:** " + UMH_EN + ". Full reading, with the limits: [`ESTADO_ATUAL.md`]({{url:estado}}).\n\n"
                 "**The scale (v410, `TGLExt.AEscala`): three theorems of the kernel, validity in the kernel and not accreditation.** " + _ESC_EN + "\n\n"
                 "**The H0DN × BG1 test:** " + OBR_EN + "; " + _H0_EN + ".\n\n"
                 "*PT — " + D81_PT + ". " + CLAY_PT + " " + UMH_PT + ". A escala (v410, `TGLExt.AEscala`; três teoremas do kernel: validade, não creditação): " + _ESC_PT + ". "
                 "O teste H0DN × BG1: " + OBR_PT + "; " + _H0_PT + ". Leitura inteira, com os limites: `ESTADO_ATUAL.md`.*")
README_PONTEIRO_ABSTRACT = ("## Abstract\n\n"
                            "Moved, byte for byte, to [`ABSTRACT.md`]({{url:abstract}}): it is copied verbatim from the append-only ledger and keeps older sentences; "
                            "read it under the current ruler (the status at the top of this page). "
                            "*PT — saiu, por cópia de bytes, para `ABSTRACT.md`: é cópia verbatim do livro-razão e guarda frases antigas; leia-o sob a régua corrente (o estado no topo desta página).*")
README_O_QUE_SAI = ("**O que sai do README para caber no teto de 40.960 bytes (L01): decisão estrutural da gerência c1, de 10/11/2026.** "
                    "(1) O bloco de hoje da frente do README, o das versões v408 e v409 (no molde, a parte `readme_partes/p_igual_np.md`), é SUBSTITUÍDO pelo bloco pronto do marcador README_FRENTE; a linha “Start here · comece aqui” fica. "
                    "(2) A seção “Abstract” SAI da frente do README e vai, por cópia de bytes, para `ABSTRACT.md` na raiz do espelho (a origem dela é o livro-razão, que não muda); "
                    "com ela sai do molde a nota “Read the Abstract below under the current ruler”; no lugar das duas fica a linha de ponteiro abaixo, em inglês e em português. "
                    "(3) Se ainda assim o README passar do teto, sai “Citing This Work” inteiro para o `CITING.md`, ficando uma linha de ponteiro. Fora disso a custódia não corta nada sem voltar à gerência. "
                    "Precedente: em 06/11 o BibTeX saiu do README para o `CITING.md`. A porta da raiz ganha o arquivo novo, por script. "
                    "Os marcadores `{{url:estado}}` e `{{url:abstract}}` são do molde do README: a custódia gera a URL por script, pela regra da porta; nada é digitado.\n\n"
                    "A linha de ponteiro, pronta, para o lugar da seção “Abstract” e da nota (vai da linha `## Abstract` até o fim deste bloco):\n\n"
                    + README_PONTEIRO_ABSTRACT)
assert len(README_FRENTE.encode("utf-8")) <= README_FRENTE_TETO_B, "o bloco README_FRENTE passou do orcamento de %d B: %d B" % (README_FRENTE_TETO_B, len(README_FRENTE.encode("utf-8")))
assert all(x_ in README_FRENTE for x_ in (D81_EN, D81_PT, CLAY_EN, CLAY_PT, UMH_EN, UMH_PT, OBR_EN, OBR_PT)), "o bloco README_FRENTE perdeu uma forma ratificada"
assert "%" not in README_FRENTE + README_O_QUE_SAI and "\r" not in README_FRENTE + README_O_QUE_SAI, "os blocos do README trazem o sinal de porcentagem ou CR"
BLOCOS_README = [("README_FRENTE", README_FRENTE), ("README_O_QUE_SAI", README_O_QUE_SAI)]   # vao ao handoff em marcador proprio: <!-- INICIO_%s_%s --> ... <!-- FIM_%s_%s --> (ident, V), DEPOIS do paragrafo README_EVIDENTE
# (do construtor, ao lado do texto pronto da gerencia) dois controles a mais: os tres teoremas da escala citados no bloco sao nomes da secao 7 RATIFICADOS pelo operador (lidos do recibo dos nomes pelo delta), uma vez no ingles e uma no portugues; e o bloco NAO anuncia limiar (por isso nao leva a clausula do limite)
_RF_NOMES = ("sem_escala_nao_ha_fita", "a_constante_da_luz_e_a_escala_do_tempo", "o_nome_e_a_singularidade_da_informacao")
assert set(_RF_NOMES) <= set(DL.NOMES_RATIFICADOS_R6_AESCALA) and all(README_FRENTE.count("`" + n_ + "`") == 2 for n_ in _RF_NOMES), "os tres teoremas da escala do README_FRENTE nao sao nomes da secao 7 ratificados pelo operador (ou nao estao uma vez no ingles e uma no portugues)"
assert not re.search(r"limiar|threshold|ln 2", README_FRENTE) and DL.CLAUSULA_Z_PT not in README_FRENTE and DL.CLAUSULA_Z_EN not in README_FRENTE, "o README_FRENTE nao anuncia limiar (por isso nao leva a clausula do limite)"


def montar_blocos(textos, readme_evidente, readme_blocos, v):
    """O que vai ao handoff, depois do cabecalho: os sete textos, cada um entre os seus marcadores; a secao README (D85), em paragrafo proprio; e, DENTRO dela, depois do README_EVIDENTE, os dois blocos do README (ADITIVO 1), cada um entre os seus marcadores."""
    marc_ = lambda i_, t_: "\n<!-- INICIO_%s_%s -->\n%s\n<!-- FIM_%s_%s -->\n" % (i_, v, t_, i_, v)
    return "".join(marc_(i_, t_) for i_, t_ in textos) + "\n" + readme_evidente + "\n" + "".join(marc_(i_, t_) for i_, t_ in readme_blocos)




def guardas_dos_textos(textos, conhecidos):
    """As guardas dos sete textos (a mesma funcao serve ao teste sem candidato: guardas_dos_textos(...) sobre textos sinteticos)."""
    out_, falhas_ = {}, []
    for ident, t in textos:
        v1 = [list(x) for x in GF.violacoes(t)]
        v2 = TX.portao(t, conhecidos, rotulo=ident)
        v3 = []
        if ident in ("ARCO_EN", "ARCO_PT") and ("'" in t or "<" in t or "\\" in t or "\n" in t):
            v3.append("%s: aspa simples, «<», barra invertida ou quebra de linha" % ident)
        if ident == "COMMIT" and any(ord(ch_) > 127 for ch_ in t):
            v3.append("COMMIT: caractere fora do ASCII")
        if ("linear nos bits" in t and DL.CLAUSULA_Z_PT not in t) or ("linear in the bits" in t and DL.CLAUSULA_Z_EN not in t):   # (R2, D99; ADENDO 4) todo texto que anuncia o teorema do Tetelestai traz a clausula do limite, PT ou EN
            v3.append("%s: anuncia o teorema do Tetelestai (linear nos bits) sem a clausula do limite do ADENDO 4 (D99)" % ident)
        if (DL.FRASE_TETELESTAI_PT in t and DL.CLAUSULA_Z_PT not in t) or (DL.FRASE_TETELESTAI_EN in t and DL.CLAUSULA_Z_EN not in t):   # (R5, D100) todo texto que traz a clausula do Tetelestai em 1 - beta traz a clausula do limite ao lado
            v3.append("%s: traz a clausula do Tetelestai em 1 - beta sem a clausula do limite (D99, D100)" % ident)
        if "ACOM Mirror" in t and not ("[PILOTO][SIM]" in t and re.search(r"nada ali valida f[ií]sica|nothing there validates physics", t)):   # (R5, D100) a citacao do dispositivo so' com as ressalvas
            v3.append("%s: cita o ACOM Mirror sem [PILOTO][SIM] e sem dizer que nada ali valida fisica (D100)" % ident)
        if ident == "README_EVIDENTE" and CLAY_PT in t and not (FIN_PT in t and FIN_EN in t):   # (D108; item 50 c da ESPEC do conserto unico, controle opcional) o README que traz a forma canonica do Clay traz a frase da finura da leitura, PT e EN
            v3.append("%s: traz a forma canonica do Clay sem a frase da finura da leitura, PT e EN (D108)" % ident)
        if re.search(r"(?<![0-9,.])4[,.]44(?![0-9])", t):
            v3.append("%s: traz o 4,44 (a regra do 4,44: nunca sozinho; estes textos nao o trazem)" % ident)
        if re.search(r"(?i)mil[eê]nio|millennium|navier|lindão", t) or (re.search(r"(?i)kimi", t) and not re.search(r"(?i)h0dn", t)):
            v3.append("%s: D59: traz o que fica fora dos textos" % ident)
        if any(x_.lower() in t.lower() for x_ in DL.FORA_D65):
            v3.append("%s: D65: traz o que a fala do nome do algoritmo deixa fora" % ident)
        out_[ident] = {"guarda_frases_v410": v1, "portao_g1": v2, "forma": v3, "n_chars": len(t)}
        if v1 or v2 or v3:
            falhas_.append((ident, v1, v2, v3))
    return out_, falhas_


# ------------------------------------------------------------------ 3. as guardas
hpath = NOS / ("HANDOFF_%s_CUSTODIA.md" % V)
h_bytes = hpath.read_bytes(); h_txt = h_bytes.decode("utf-8")
assert b"\r\n" not in h_bytes, "o handoff e CRLF: ajustar o acrescimo"
for ident, _ in TEXTOS + BLOCOS_README:
    assert ("INICIO_%s_%s" % (ident, V)) not in h_txt, "marcador %s ja existe no handoff" % ident
conhecidos = set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{16}(?![0-9a-fA-F])", h_txt)) | set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{64}(?![0-9a-fA-F])", h_txt)) | {PIN}
guardas, falhas = guardas_dos_textos(TEXTOS + [("README_EVIDENTE", README_EVIDENTE)] + BLOCOS_README, conhecidos)   # (ADITIVO 1) os dois blocos do README passam pelas MESMAS guardas e pelo portao do G1
if falhas:
    for f_ in falhas:
        print("REPROVADO:", f_)
    sys.exit(1)
print("guardas: os sete textos, a secao README (D85) e os dois blocos do README (README_FRENTE, %d bytes em UTF-8; README_O_QUE_SAI) passaram (guarda de frases v410, portao do G1, forma do ARCO/COMMIT, sem 4,44, D59, D65)" % len(README_FRENTE.encode("utf-8")))

# ------------------------------------------------------------------ 4. o acrescimo, com backup de bytes
cab = ("\n\n**Textos da custódia (gerência c1, 06 e 09/11/2026; substituem o molde factual do G1; números lidos do core selado, do selo e do diário por "
       "`pos_rito\\textos_custodia_handoff_v410.py`, que os conferiu contra ESPERADOS e passou os textos pela guarda de frases da v410 e pelo portão do G1 antes de os anexar (D52: encadeado no fim do S6); "
       "o alcance é relativo ao leitor e a máquina de Turing padrão sem o leitor fica fora; a forma de matriz finita é o signo; o teste H0DN × BG1 entra pré-registrado; nenhum dado observado lido; os nomes das declarações foram ratificados pelo operador em 09/11; a escala (a pedra AEscala; D86/D87) e a forma canônica do Clay (D84), com a validade no kernel, e a creditação é do Clay; o recibo documental HMS/13: cobertura documental de fontes, não covariância física fechada; nada aberto; a seção README (o que fica evidente, D85) vai depois dos sete textos; nenhuma chave antiga muda; validade no kernel não é creditação):**\n")
blocos = montar_blocos(TEXTOS, README_EVIDENTE, BLOCOS_README, V)   # (a secao README, em paragrafo proprio, depois dos sete marcadores; o parser do G1 a le como secao)
novo = h_bytes.rstrip(b"\n") + (cab + blocos).encode("utf-8")
assert len(novo) > len(h_bytes) + 3000 and novo.startswith(h_bytes.rstrip(b"\n")), "o acrescimo nao cresceu como esperado"
vcab = [list(x) for x in GF.violacoes(cab)] + TX.portao(cab, conhecidos, rotulo="cabecalho")
assert not vcab, "o cabecalho dos textos nao passa nas guardas: %r" % (vcab[:3],)
bak = hpath.with_name(hpath.name + ".bak_" + TS); open(bak, "xb").write(h_bytes)
assert bak.read_bytes() == h_bytes, "backup de bytes diferente do original"
tmp = hpath.with_name(hpath.name + ".tmp_" + TS); open(tmp, "xb").write(novo); assert tmp.stat().st_size == len(novo)
os.replace(tmp, hpath)
assert hpath.stat().st_size == len(novo) > len(h_bytes), "o handoff nao cresceu depois da substituicao"
print("handoff: %d -> %d bytes; sha16 %s -> %s; backup %s" % (len(h_bytes), len(novo), hashlib.sha256(h_bytes).hexdigest()[:16], s16(hpath), bak.name))

# ------------------------------------------------------------------ 5. re-leitura pelo parser do G1
c = types.SimpleNamespace(NOS=NOS, CEN=CEN)
h = NOSMOD.ler_handoff(c, V)
faltam = [i for i, _ in TEXTOS + BLOCOS_README if ("%s_%s" % (i, V)) not in h.corpos]   # (ADITIVO 2) os NOVE corpos: os sete textos e os dois blocos do README
assert h is not None and not faltam and not h.problemas, (faltam, h.problemas)
for i, t in TEXTOS + BLOCOS_README:
    assert h.corpos["%s_%s" % (i, V)].strip("\n") == t, "corpo lido difere do escrito: " + i
assert h.o_que_e and h.o_que_e.pin16 == PIN and h.o_que_e.versao == V, "o «O que é» do handoff deixou de ser lido"
assert "**README: o que fica evidente**" in hpath.read_text(encoding="utf-8"), "a secao README (D85) nao esta' no handoff"
print("parser do G1: os dois blocos do README lidos entre os seus marcadores (sem o prefixo PARAGRAFO_), iguais as constantes; README_FRENTE: %d bytes em UTF-8 (teto %d), sha256 %s" % (len(README_FRENTE.encode("utf-8")), README_FRENTE_TETO_B, hashlib.sha256(README_FRENTE.encode("utf-8")).hexdigest()))
print("parser do G1: %d/%d corpos lidos (os sete textos e os dois blocos do README), 0 problemas; marcadores:" % (len(TEXTOS + BLOCOS_README) - len(faltam), len(TEXTOS + BLOCOS_README)), sorted(h.marcadores))
rec = {"quando": datetime.datetime.now().isoformat(timespec="seconds"), "quem": "gerencia c1", "handoff": str(hpath), "sha16_antes": hashlib.sha256(h_bytes).hexdigest()[:16],
       "sha16_depois": s16(hpath), "backup": str(bak), "numeros_lidos": N, "revisao_terceiro": ({"aprovada": REV["aprovada"], "candidato_sha16": REV["candidato_sha16"]} if REV else "ausente: os textos dizem que e' ato distinto e nao a afirmam"),
       "textos": dict(TEXTOS), "readme_evidente": README_EVIDENTE, "readme_frente": README_FRENTE, "readme_frente_bytes_utf8": len(README_FRENTE.encode("utf-8")), "readme_frente_sha256": hashlib.sha256(README_FRENTE.encode("utf-8")).hexdigest(), "readme_frente_teto_b": README_FRENTE_TETO_B, "readme_o_que_sai": README_O_QUE_SAI, "readme_ponteiro_abstract": README_PONTEIRO_ABSTRACT, "guardas": guardas, "parser_g1": {"corpos": sorted(h.corpos), "problemas": h.problemas},
       "motivo": "D52/D68a: os sete marcadores opcionais da prosa da custodia entram encadeados no fim do S6 (sem eles, a sessao de custodia teria o molde factual); o fim da cadeia do orquestrador e' o handoff",
       "estatuto": "REAL (numeros lidos do core selado, do selo e do diario e conferidos contra ESPERADOS; textos da gerencia c1, em nome proprio); NOT_FALSIFIED nunca e a palavra da creditacao; o gate nao se move"}
(HERE / "RECIBO_TEXTOS_CUSTODIA_HANDOFF_v410.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
print("recibo:", HERE / "RECIBO_TEXTOS_CUSTODIA_HANDOFF_v410.json")
