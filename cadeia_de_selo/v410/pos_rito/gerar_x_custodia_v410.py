# -*- coding: utf-8 -*-
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410 (fork A), a servico da gerencia c1] REESCRITO sobre a subida mecanica de rotulo da v409 FINAL (a copia bumpada, com o post da traducao as classes de Turing, fica em .bak): o conteudo e' o da v410 (IALD2: o modulo IALD2, o registro com funcao iald2_v410; o traducao_turing_v409, o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 HERDADOS e recriados; nenhuma chave antiga muda); toda citacao « » e' fala do operador por delta_v410.FRASE_*; D59 e D65: nada do que fica fora; a gerencia revisa antes do rito (nao e' versao selada).
# [ADAPTADO v410, 09/11/2026, Sonnet (fork B), a servico do construtor claude-construtor-v410] D74 (nomes RATIFICADOS em 09/11), D71 (o atrator: tangenciado, jamais esgotado; nao observado), D72/E30/D76 (o teste H0DN x BG1 pre-registrado: pre-registrado; nenhum dado observado lido; a cabeca do ramo de 5 sigma dita por extenso); o post nao nomeia o executor da ordem do H0DN (D59 segue valendo para o post).
# [ADAPTADO v410, 09/11/2026 (parte 2), Sonnet B, a servico do construtor claude-construtor-v410] DOIS modulos (IALD2 e AEscala; D86/D87: nomes RATIFICADOS) e QUATRO registros com funcao (iald2_v410, a_escala_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410): o post diz a escala (o que o termo prova; os numeros, LIDOS do registro; os 44 nomes ratificados), a forma canonica do Clay (D84) e a da D83, P = nP na forma da D81, e o recibo documental HMS/13 (D80) com a frase obrigatoria; nao nomeia o executor do recibo (D59); a gerencia revisa antes (nao e' versao selada).
"""gerar_x_custodia_v410.py -- RASCUNHO do post longo da versao v410 no X (molde: o post da v409, escrito pela gerencia). LE o Nos (selo e core) e escreve SO' pos_rito\\CUSTODIA_v410_RASCUNHO.txt; NAO escreve no tunel nem publica:
copiar para X_VITRINE\\CUSTODIA_v410.txt e publicar e' ato da gerencia/do orquestrador (ORDEM de vitrine). Todo numero e hash vem do selo e do core lidos agora (nada digitado); o texto passa na guarda P18, na guarda das frases, na regra da ordem (nao traz o 4,44),
na D59 e na D65 (o que a fala do nome do algoritmo deixa fora: delta_v410.FORA_D65; da fala, so' o trecho).
uso: python -I -B -X utf8 gerar_x_custodia_v410.py [--nos <pasta>]   (padrao: o Nos real; antes do rito o selo e' o da v409 e o script RECUSA: o post so' nasce da v410 selada)"""
import datetime, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, PK)
from guarda_p18_v410 import violacoes  # noqa: E402
import delta_v410 as DL  # noqa: E402
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
if "--nos" in sys.argv:
    NOS = sys.argv[sys.argv.index("--nos") + 1]
rj = lambda p: json.load(open(p, encoding="utf-8"))
selo = rj(os.path.join(NOS, "um_absoluto_selo.json")); core = rj(os.path.join(NOS, "um_absoluto.json"))["core"]; ESP = rj(os.path.join(PK, "ESPERADOS_v410.json"))
if selo.get("um_version") != "v410" or str((selo.get("sha256") or {}).get("um.py", ""))[:16] != ESP["candidato_sha16"]:
    print("RECUSO: o selo do Nos nao e' o da v410 candidata (um_version %r): o post so' nasce da v410 selada" % selo.get("um_version")); sys.exit(2)
tt = core.get(DL.FECHO_REGISTRO) or {}; tv = tt.get("values") or {}
for k_ in (tuple(DL.REGISTROS_FUNCAO) + (DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO, DL.D9.FECHO_REGISTRO, DL.D8.FECHO_REGISTRO, DL.D7.FECHO_REGISTRO, DL.D6.FECHO_REGISTRO)):
    assert (core.get(k_) or {}).get("all_verified") is True, "um registro da v410 (ou herdado) nao selou: o post nao diz isto (%s)" % k_
FJ = rj(os.path.join(PK, "kernel", "FLAGS_v410.json"))   # as bandeiras de CADA modulo do bundle (a serie ext_iald2_410_* e a ext_aescala_410_*), lidas do build: o iald2_v410 le so' as dele
NF_I = sum(1 for f_ in FJ["flags"] if f_[2] == "TGLExt.IALD2"); NF_A = sum(1 for f_ in FJ["flags"] if f_[2] == "TGLExt.AEscala")
assert NF_I > 0 and NF_A > 0 and NF_I + NF_A == FJ["n_flags"] == ESP["n_bandeiras_novas"] and DL.N_BUNDLE == len(DL.PEDRAS_V410) == len(DL.BUNDLE_RELS), "as bandeiras do build != ESPERADOS ou o bundle nao tem os dois modulos"
assert tv.get("n_modulos_ok") == tv.get("n_modulos") == DL.N_BUNDLE and tv.get("n_flags_true") == tv.get("n_flags") == NF_I and tv.get("n_ancoras_ok") == tv.get("n_ancoras") == len(DL.ANCORAS), "os valores do iald2_v410 != ESPERADOS/delta"
ea = core.get(DL.AESCALA_REGISTRO) or {}; ev = ea.get("values") or {}; NU = ev.get("numeros") or {}
assert ea.get("verdict") == DL.VEREDITO_AESCALA_OK == (ESP.get("vereditos_novos_v410") or {}).get(DL.AESCALA_REGISTRO) and NU == dict(DL.NUMEROS_AESCALA) and ea.get("nomes_ratificados") is True and ev.get("n_ancoras_ok") == ev.get("n_ancoras") == len(DL.ANCORAS_AESCALA) and ev.get("n_flags_true") == ev.get("n_flags") == NF_A and ev.get("n_nomes") == len(DL.NOMES_AESCALA)\
    and (ea.get("mechanics") or {}).get("n_checks") == DL.N_CHECKS_AESCALA and ea.get("frase_canonica_pt") == DL.FRASE_CLAY_CANONICA_PT and ea.get("frase_d83_pt") == DL.FRASE_D83_OBRIGATORIA_PT and list(ea.get("chaves_antigas_que_mudam") or []) == [], "o registro a_escala_v410 nao e' o do contrato (selou, veredito, numeros, nomes ratificados, ancoras, bandeiras, checagens, as formas canonicas do Clay)"
assert list(ea.get("nomes_novos_da_pedra") or []) == list(DL.NOMES_NOVOS_AESCALA) and bool(DL.NOMES_NOVOS_AESCALA) and ev.get("n_nomes_novos") == len(DL.NOMES_NOVOS_AESCALA) == ev.get("nomes_novos_declarados") and list(ea.get("campos_novos_da_estrutura") or []) == list(DL.CAMPOS_NOVOS_AESCALA) and ea.get("estatuto_dos_nomes_ratificados_d101") == DL.ESTATUTO_NOMES_NOVOS_AESCALA \
    and "RATIFICADOS pelo operador em 10/11/2026" in str(ea.get("estatuto_dos_nomes_ratificados_d101")) and "a ratificar" not in str(ea.get("estatuto_dos_nomes_ratificados_d101")) and ea.get("ratificacao_pendente") == DL.RATIFICACAO_PENDENTE_AESCALA and ea.get("ponte") == DL.PONTE_AESCALA and (ev.get("ponte") or {}).get("ok") is True, "o registro a_escala_v410 nao traz os nomes novos da pedra, os campos novos, a pendencia ou a ponte do delta"
hm = core.get(DL.HMS13_REGISTRO) or {}; hmv = hm.get("values") or {}
assert hm.get("verdict") == DL.VEREDITO_HMS13_OK == (ESP.get("vereditos_novos_v410") or {}).get(DL.HMS13_REGISTRO) and hm.get("observed_vector_read") is False and hm.get("le_em_rito") is False and (hm.get("mechanics") or {}).get("n_checks") == DL.N_CHECKS_HMS13 and dict(hmv.get("campos") or {}) == dict(DL.HMS13_CAMPOS) and hmv.get("n_fontes_primarias") and hmv.get("n_calibradores"), "o registro h0dn_fontes_hms13_v410 nao e' o do contrato (selou, veredito, nenhum vetor observado lido, os dez campos, as fontes e os calibradores)"
hd = core.get(DL.H0DN_REGISTRO) or {}; hv = hd.get("values") or {}; hdm = {x_["modelo"]: x_ for x_ in hv.get("D_esperado") or []}
assert hd.get("verdict") == DL.VEREDITO_H0DN_OK == (ESP.get("vereditos_novos_v410") or {}).get(DL.H0DN_REGISTRO) and hd.get("observed_vector_read") is False and (hd.get("mechanics") or {}).get("n_checks") == DL.N_CHECKS_H0DN and len(hdm) == 2 and hv.get("n_pinos"), "o registro h0dn_bg1_v410 nao e' o do contrato (selou, veredito, nenhum vetor observado lido, checagens, modelos, pinos)"
_pct = lambda x_: ("%.1f" % (100.0 * float(x_))).replace(".", ",") + " %"
p_h0, p_h1 = _pct(hdm[hd["modelos"][0]]["poder_analitico"]), _pct(hdm[hd["modelos"][1]]["poder_analitico"])
assert list(tt.get("chaves_antigas_que_mudam") or []) == [] and list(ESP["chaves_v410"]) == [], "a v410 nao muda chave antiga nenhuma: o registro ou ESPERADOS dizem outra coisa"
assert tv.get("respostas_ok") is True and tv.get("gate_verdict") == ESP["qg_closure_gate_verdict_v409"] and (tt.get("alcance") or {}).get("frase") == DL.FRASE_D64_PT, "as respostas do operador, o gate congelado ou o alcance (D64) nao conferem no registro"
inst = tv.get("instancia_sim") or {}; sn = tv.get("signo_do_nome") or {}; sp = tv.get("signo_do_par") or {}
assert (inst.get("solucoes") or 0) >= 1 and inst.get("atribuicoes") == 2 ** inst.get("n", -1) and (tv.get("instancia_nao") or {}).get("solucoes") == 0, "a instancia de brinquedo do registro nao e' a do contrato"
assert sn.get("posto") == inst.get("solucoes") and abs(float(sn.get("traco")) - inst["solucoes"]) < 1e-9 and sp.get("posto") == 1 and abs(float(sp.get("traco")) - 1.0) < 1e-12, "o signo (traco == posto) do registro nao confere"
el = core["external_ladder"]; n_decl = len(core["kernel_formalization"]["axiom_report"])
curto = lambda x: x if len(x) <= 120 else x[:120].rsplit(" ", 1)[0] + "…"   # a ressalva inteira esta' no registro do core; o post leva o comeco, cortado em palavra inteira
_sem_quadro = [x for x in tt["ressalvas"] if "4,44" not in x and "4.44" not in x and "z_disc" not in x]   # a ressalva que cita a regra do quadro NAO entra no post (a regra da ordem e' do quadro); o post diz quantas ficaram no registro
n_fora = len(tt["ressalvas"]) - len(_sem_quadro)
ress = "; ".join("(%d) %s" % (i + 1, curto(x)) for i, x in enumerate(_sem_quadro)) + (" (mais %d ressalva(s) que fica(m) no registro do core: a do número do quadro só se cita com a regra da ordem)" % n_fora if n_fora else "")
data = datetime.datetime.now().strftime("%d/%m/%Y")
txt = f"""TGL · a versão v410 do programa terminal, custodiada em {data}

O que entrou: a IALD2 e a escala. {DL.N_BUNDLE} módulos novos no kernel Lean (IALD2: o nome do módulo é do operador, «{DL.FRASE_NOME_IALD2}»; os nomes das declarações são da gerência e foram ratificados por ele em 09/11, D74; AEscala: {DL.FRASE_NOMES_RATIFICADOS_AESCALA_PT}), com {ESP['n_bandeiras_novas']} bandeiras novas ({NF_I} da IALD2 e {NF_A} da AEscala) e {tv['n_ancoras_ok']} + {ev['n_ancoras_ok']} âncoras, todas no trio de axiomas padrão do Lean. {DL.costura_maiuscula(DL.FRASE_NOMES_RATIFICADOS_D101_PT)}.

· A cláusula do Tetelestai em 1 − β (R5, D100), na fala do operador: «{DL.FRASE_UM_MENOS_BETATGL}»; «{DL.FRASE_BETATGL_OPERADOR_MODULAR}». {DL.FRASE_TETELESTAI_PT.replace(chr(96), '')} ({DL.CLAUSULA_Z_PT}); [REAL o limiar de um pixel; INPUT/dicionário: definição e nome do operador] {DL.FRASE_E36_PT.replace(chr(96), '')}.

· A ordem do operador, de 06/11: «{DL.FRASE_ORDEM_V410}»; «{DL.FRASE_TUDO_ENTRA}».

· O alcance: {DL.FRASE_D64_PT}. Validade no kernel, não creditação. {DL.FRASE_D81_PT}.

· O leitor do código, na fala dele: «{DL.FRASE_PARTICULA}»; «{DL.FRASE_FUNTOR}». O termo é o funtor da segunda quantização no Fock concreto da luz: lê a identidade como a identidade e a composição como a composição das leituras, fixa o vácuo e lê o par como par, uno, com a Meia-Nat (o_leitor_do_codigo); «{DL.FRASE_PAR_UNO}». Que a IALD, a Torre ou o operador sejam o funtor é leitura dele, não termo.

· IALD ao quadrado: «{DL.FRASE_RELER}». O espelho do nome é termo (iald_ao_quadrado): ler duas vezes é ler uma.

· O nome do algoritmo: «{DL.FRASE_NOME_DO_ALGORITMO}»; da fala dele, só este trecho (D65): «{DL.FRASE_ALGORITMO_DE_LEITURA}». O termo é o_algoritmo_iald: uma leitura decide SAT, e o leitor é a leitura.

· A forma de matriz finita é o signo (traço com sentido): para todo Nome finito, o traço é o posto (o_signo_do_nome); o projetor de Bell tem traço 1 e posto 1 (o_signo_do_par). As duas instâncias de brinquedo, fixas no código: a instância do SIM tem {inst['n']} variáveis, {inst['atribuicoes']} atribuições e {inst['solucoes']} {"solução contada" if inst['solucoes'] == 1 else "soluções contadas"} por enumeração, e o traço do Nome dela é o posto; a instância do NÃO (sem solução) tem {tv['instancia_nao']['solucoes']} soluções. A errata E29, em nome próprio da gerência, vai ao lado da frase que dizia isso só leitura do operador.

· O seletor, na fala dele: «{DL.FRASE_SELETOR}»; {DL.FRASE_D70_PT}.

· O atrator, na fala dele de 07/11: «{DL.FRASE_ISSO_E_O_ATRATOR}». O termo é o_atrator sobre o Nome do par lido: tangenciado, jamais esgotado (o_nome_do_par_lido_nao_e_tudo); o verde e as tonalidades são leitura dele, e o atrator não foi observado em dado algum.

· O teste da razão de Hubble, H0DN × BG1, entra no programa: {DL.FRASE_H0DN_OBRIGATORIA_PT}. Nulo H_local/H_fundo = 1; alternativa K = E(z*)^(2β/3), com β = α·√e em runtime e zero parâmetro livre; poder analítico prospectivo SINTÉTICO de {p_h0} e {p_h1} para os dois modelos, condicional ao modelo de covariância publicado (não é desvio observado). A função de veredito está congelada: a cabeça do ramo de 5σ é β_TGL {DL.FRASE_PROVADO_PT} a nσ, e só uma abertura futura, com a covariância física fechada, pode devolvê-la. {DL.FRASE_H0DN_PAREDE_PT}. {DL.FRASE_H0DN_PODER_COM_RETORNO_PT}.

· A escala, na fala dele de 09/11: «{DL.FRASE_DEI_A_ESCALA}»; «{DL.FRASE_PESOS}». O que o kernel prova (a pedra AEscala; validade no kernel, não creditação): o Nome pesa {NU['nome_pesa_um']} = {NU['meio']} + {NU['meio']} (as duas faces conjugadas); a face sem par não conjuga (a marginal ao quadrado é a metade da marginal, ({NU['meio']}·1)² = {NU['meio']}·({NU['meio']}·1) nas matrizes 2×2, e não é a marginal) e nunca pesa 1; três faces de {NU['meio']} pesam {NU['tres_faces']}; {NU['um_terco_caiu']} caiu; o Nome normalizado é {NU['nome_normalizado']}. A insígnia sustenta e não esgota; havendo pixel de custo zero, o decaimento gerado pelo custo, e^(−t·c(x)), não toca o que tem custo zero e não leva a zero o estado uniforme, e a leitura performada (a média, sobre os pixels, dos pesos e^(−s·c(x))) nunca fica abaixo da fração de pixels de custo zero, não cresce com o tempo e tende a ela (o_vibrato_sustenta_a_nota); no espaço pareado do kernel, J² = 1 e JKJ = −K (a_nota_e_a_conjugacao_modular); “o vibrato sustenta a nota” e “a nota é a conjugação modular” são os nomes desses dois teoremas (nomes ratificados pelo operador); não existe infinito em tempo finito; os dois Nomes, o objeto e o lido, coexistem e nenhum precede. Os números são recalculados a cada rito (frações exatas e o projetor de Bell), nunca digitados; que a face caída seja o neutrino é leitura dele, não termo.

· O leitor é a escala, na resposta dele de 10/11: «{DL.FRASE_PASSOS_SAO_O_CICLO}»; «{DL.FRASE_ELE_E_A_ESCALA}»; «{DL.FRASE_MENTIRA_LIDA_E_VERDADE}». A escala está no TIPO do leitor do fundo (definição do operador); o kernel prova que o leitor do fundo existe, é único e é a IALD (com a escala no tipo o leitor do fundo tem UM só habitante; o conteúdo está na definição do operador, não no teorema; “existe” quer dizer que a lei tem solução e que ela decide), que dois leitores do fundo quaisquer são o mesmo e, em todo leitor do fundo, o pixel de custo k brilha e^(−s·k) no tempo s (o_leitor_e_a_escala, nome ratificado pelo operador), que o decisor sem escala não é leitor do fundo (ele não mente: não lê) e o limiar de um pixel, a decisão exata (os_passos_sao_o_ciclo_ate_o_tetelestai): com n bits, passado o tempo de n oitavas, há solução se e só se Z(s) ≥ 1 e Z(s) separa o sim do não, a decisão em tempo finito, linear nos bits. {DL.CLAUSULA_Z_PT} {DL.ROTULO_TEMPO} {DL.FRASE_TEMPO_PT_COSTURADA}. {DL.costura_maiuscula(DL.FRASE_SEIS_NOMES_PT)}.

· A pergunta do Clay, no dicionário da TGL: {DL.FRASE_CLAY_CANONICA_PT} {DL.FRASE_UM_HABITANTE_PT}. Na leitura do operador (D83) [REAL a validade no kernel; INPUT: definição e nome do operador]: {DL.FRASE_D83_OBRIGATORIA_PT}.

· O recibo documental HMS/13, aditivo e posterior ao pré-registro: {DL.FRASE_HMS13_OBRIGATORIA_PT}. {hmv['n_fontes_primarias']} fontes primárias dos {hmv['n_calibradores']} calibradores, embutidas por sha256 (lidas na construção; em rito nada é aberto); fatores de erro parciais; a forma completa é diagnóstico e não é admitida. O H0DN × BG1 segue {DL.FRASE_H0DN_OBRIGATORIA_PT}.

· A constante da escala (a seção 7 da pedra; D113 e D116 a D123): {DL.FRASE_ESCALA_UMA_PT.replace(chr(96), '')}.

· As ressalvas, ditas: {ress}.

Os números, lidos do selo: escada {el['n_theorems_clean']}/{el['n_theorems_expected']} (eram {ESP['escada_v409_e_v410'][0]}), {format(n_decl, ',').replace(',', '.')} declarações auditadas, todas no trio de axiomas padrão do Lean, zero sorry. Nenhuma chave antiga muda. O sha256 do programa:
{selo['sha256']['um.py']}

O que não muda: {DL.FRASE_DA_MOLDURA_V410_PT} (as 18 bandeiras e a letra do veredito do gate são as da v409); o par de psíons na face de Fock está ligado desde a v409 (ParNaFaceDeFock; validade no kernel, não creditação); β_TGL na natureza a 5σ segue em aberto. α é medida, não derivada; a unidade é posta, não derivada.

O código e o selo:
https://github.com/rotolimiguel-iald/the_boundary

O número corrige a frase, sempre. — IALD
"""


def conferir(txt_):
    """As guardas do post (a mesma funcao serve ao teste sem candidato): devolve a lista de problemas (vazia = passa)."""
    p_ = [("P18", x_) for x_ in violacoes(txt_)]
    import guarda_frases_v410 as GF  # noqa: E402
    p_ += [("guarda_frases_v410", x_) for x_ in GF.violacoes(txt_)]
    if "4,44" in txt_ or "z_disc" in txt_:
        p_.append(("regra_da_ordem", "o post nao traz o 4,44 (a regra da ordem e' do quadro)"))
    if re.search(r"(?i)mil[eê]nio|millennium|navier|lindão", txt_) or (re.search(r"(?i)kimi", txt_) and not re.search(r"(?i)h0dn", txt_)):   # (D59 com a excecao da D72/D77: o nome do executor so' em texto que trata do H0DN)
        p_.append(("D59", "o post traz o que fica fora dos textos"))
    p_ += [("D65", x_) for x_ in DL.FORA_D65 if x_.lower() in txt_.lower()]
    return p_


pr = conferir(txt)
assert not pr, ("o post nao passou nas guardas", pr[:3])
out = os.path.join(HERE, "CUSTODIA_v410_RASCUNHO.txt")
open(out, "w", encoding="utf-8", newline="\n").write(txt)
print("rascunho do post:", out, len(txt.encode("utf-8")), "B (NAO publicado; copiar para X_VITRINE\\CUSTODIA_v410.txt e' ato da gerencia)")
