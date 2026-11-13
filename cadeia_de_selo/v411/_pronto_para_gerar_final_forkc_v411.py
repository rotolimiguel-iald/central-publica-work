# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026, claude-construtor-v411 (retomada, fork C)] a regravacao UNICA do PRONTO_PARA_GERAR_v411.json com o estado final da cadeia REAL (ordem 3(b) da gerencia c1)
"""_pronto_para_gerar_final_forkc_v411.py -- grava UMA vez, no fim, o PRONTO_PARA_GERAR_v411.json (backup de BYTES antes; temporario -> conferir ->
substituir), LENDO do disco o estado da cadeia REAL: o candidato (que substitui o do relatorio do principal), o que passou (o ensaio a seco, os
ESPERADOS, os dois conferidores, as citacoes nos dois escopos, diff e pinos, instalar/rito, o p00, o PRONTO_PARA_O_POS_RITO, o fim_de_cadeia etapa a
etapa, os harnesses, a purga, a varredura), a cadeia inteira passo a passo (cadeia_v411_out.txt), o relatorio (pronta, falta) e o que ele EXIGE em cada
portao falso (as linhas do p00 e do relatorio lidas aqui por script), a condicao 3(a) da gerencia (o topo selado traz o resultado), a parada das 14h39
no passo 4 (historia) e o sha16 de cada marco. Mantem do arquivo anterior as chaves que seguem validas (a interpretacao do marcador sem fonte, o campo
p2_ao_lado_da_v387 com a origem do rotulo, as listas). Nao deposita, nao anota o Mapa, nao faz transition ACOM (isso e' do principal e da gerencia).
uso: python -B -X utf8 _pronto_para_gerar_final_forkc_v411.py [--seco]   (--seco: monta e imprime, nao grava)"""
import datetime, glob, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
SECO = "--seco" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
sha = lambda p_: hashlib.sha256(open(p_, "rb").read()).hexdigest()
s16 = lambda p_: sha(p_)[:16] if os.path.isfile(p_) else None
J = lambda p_: json.load(open(p_, encoding="utf-8")) if os.path.isfile(p_) else None
T = lambda p_: open(p_, encoding="utf-8", errors="replace").read() if os.path.isfile(p_) else ""
S = DL.saida
P = os.path.join(HERE, "PRONTO_PARA_GERAR_v411.json")
ANT = J(P) or {}
CM = J(DL.MANIFESTO_ARQ) or {}; EN = J(S("ensaio_a_seco_v411.json")) or {}; ESP = J(S("ESPERADOS_v411.json")) or {}; PC = J(S("PRECONDICOES_v411.json")) or {}; CIT = J(S("conferir_citacoes_v411.json")) or {}
CN = J(S("conferencia_rito_v411_CONTROLE_NEGATIVO_PRE_RITO.json")) or {}; POS = J(S("conferencia_rito_v411_POSITIVO_FALSO_NOS.json")) or {}; DER = J(S("DERIVACAO_v411.json")); PIN = J(S("PINOS_BN_v411.json")) or {}
PRON_P = os.path.join(DL.ENSAIO_DIR, "PRONTO_PARA_O_POS_RITO.json"); PRON = J(PRON_P) or {}; PREP_P = S("PREPARACAO_v411_PRONTA.json"); PREP = J(PREP_P)
H_T = J(S(os.path.join("pos_rito", "HARNESS_TEXTOS_ENSAIO_v411.json"))); H_F = J(S(os.path.join("pos_rito", "HARNESS_FECHAR_SANDBOX_v411.json")))
PUR = J(S("purga_v411.json")); VF = J(S("VARREDURA_FOCK_OMEGA_v411.json"))
cand16 = s16(DL.CANDIDATO_ARQ)
assert cand16 and cand16 == CM.get("sha16"), ("o manifesto nao e' do candidato em disco", cand16, CM.get("sha16"))


def linha(arq_, trecho_):
    """o numero da UNICA linha de arq_ (na pasta da cadeia) que traz trecho_; None se nao for unica (o texto mudou: dito, nao adivinhado)"""
    ls_ = [i_ + 1 for i_, l_ in enumerate(T(os.path.join(HERE, arq_)).split("\n")) if trecho_ in l_]
    return ls_[0] if len(ls_) == 1 else None


# ---- a cadeia inteira, passo a passo (cadeia_v411_out.txt)
CAD_P = S("cadeia_v411_out.txt"); CAD = T(CAD_P)
passos, atual = [], None
for l_ in CAD.split("\n"):
    m_ = re.match(r"^== (\d\d[a-z]?_[A-Za-z0-9_]+) \((\d\d:\d\d:\d\d)\): ", l_)
    if m_:
        atual = {"passo": m_.group(1), "hora": m_.group(2), "rc": None}; passos.append(atual); continue
    m_ = re.match(r"^   rc=(\d+)$", l_)
    if m_ and atual is not None and atual["rc"] is None:
        atual["rc"] = int(m_.group(1))
cad_ini = re.search(r"^inicio (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)", CAD); cad_fim = re.search(r"^fim (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) rc=0$", CAD, re.M)
parados = re.findall(r"^PARADO.*$", CAD, re.M)
fim_etapas = re.findall(r"^== (\d)\. ", CAD, re.M); fim_ok = bool(re.search(r"^== FIM \d\d:\d\d:\d\d$", CAD, re.M)); fim_falhou = re.findall(r"^FALHOU: .*$", CAD, re.M)
rc_nao_zero = [(p_["passo"], p_["rc"]) for p_ in passos if p_["rc"] not in (0, None)]
# ---- a rodada do fork C por fora da cadeia (o fim_de_cadeia de novo, a varredura, o p00): o estado do driver, fora de work
DRV_P = os.path.join(DL.RODADA_PAI, "saidas_forkc_20261112", "driver_status.txt"); DRV = [l_ for l_ in T(DRV_P).split("\n") if l_.strip()]
DRV_RES = [l_ for l_ in DRV if re.match(r"^(inicio|fim|[A-E] .* rc=\d+|PAROU)", l_)]

# ---- o que passou (cada um LIDO do disco)
_nm = CN.get("nao_pode_mudar") or {}
passou = {
    "ensaio_a_seco_TUDO_PASSOU_deste_candidato": bool(EN.get("veredito") == "TUDO PASSOU" and EN.get("sha16") == cand16),
    "esperados_deste_candidato": bool(ESP.get("candidato_sha16") == cand16),
    "conferidor_controle_negativo_nao_bate_com_o_nos_na_v410": bool(CN.get("tudo_bate") is False and CN.get("um_py_sha16") == ESP.get("origem_sha16") and _nm and all(_nm.values())),
    "conferidor_positivo_no_falso_nos_TUDO_BATE": bool(POS.get("tudo_bate") is True and POS.get("um_py_sha16") == cand16),
    "citacoes_limpas_nos_dois_escopos": bool(CIT.get("ok") is True and CIT.get("ok_do_um_py") is True and CIT.get("ok_do_pos_rito") is True and not CIT.get("nao_verbatim")),
    "diff_e_pinos_sem_pendente": bool(((PIN.get("candidato") or {}).get("sha256") or "")[:16] == cand16 and not PIN.get("pendentes")),
    "instalar_reverter_rito_estatico_sem_falhas": bool(DER is not None and not DER.get("falhas")),
    "p00_sem_falhas": bool(PC.get("n_falhas") == 0 and str(PC.get("veredito", "")).startswith(("NENHUMA FALHA", "TODAS PASSARAM"))),
    "pronto_para_o_pos_rito_da_cadeia_real": bool(PRON.get("modo") == "cadeia real" and PRON.get("artefato_sha16") == cand16),
    "fim_de_cadeia_etapas_1_a_7_dentro_da_cadeia": bool(fim_ok and set(fim_etapas) >= set("1234567") and not fim_falhou),
    "harness_dos_textos": bool(H_T and H_T.get("tudo_passou") is True),
    "harness_do_fechar_com_o_pino_real": bool(H_F and H_F.get("tudo_passou") is True and not H_F.get("pino_emulado")),
    "purga_zero_ocorrencias": bool(PUR and PUR.get("total_com_ocorrencia") == 0 and PUR.get("fala_excluida_total_com_ocorrencia") == 0),
    "varredura_fock_omega_zero_novos": bool(VF and VF.get("n_novos") == 0 and VF.get("arquivos", 0) > 0),
    "cadeia_inteira_ate_o_fim_sem_PARADO": bool(cad_fim and not parados and any(p_["passo"].startswith("18_") and p_["rc"] == 0 for p_ in passos)),
}
# ---- a condicao 3(a) da gerencia (o topo selado traz o resultado): no ensaio e no conferidor
_art = EN.get("artigo") or {}
_k3a = ("topo_com_o_resultado_tex", "topo_com_o_resultado_txt", "topo_do_candidato_e_o_preenchimento_independente", "topo_com_o_resultado_controles_negativos")
topo3a = {l_: {k_: ((_art.get(l_) or {}).get("v411") or {}).get(k_) for k_ in _k3a} for l_ in ("pt", "en")}
var3a = {l_: ((EN.get("variante") or {}).get(l_) or {}).get("topo_de_recuo_sem_a_v397_nao_passa_como_selo") for l_ in ("pt", "en")}
var3a11 = {l_: ((EN.get("variante_v411") or {}).get(l_) or {}).get("topo_de_recuo_sem_o_registro_nao_passa_como_selo") for l_ in ("pt", "en")}
pos3a = {k_[:60]: v_ for k_, v_ in (POS.get("deve_mudar") or {}).items() if k_.startswith("o TOPO do artigo PT/EN SELADO traz o RESULTADO")}
cond3a_ok = bool(all(v_ is True for d_ in topo3a.values() for v_ in d_.values()) and all(v_ is True for v_ in list(var3a.values()) + list(var3a11.values())) and pos3a and all(v_ is True for v_ in pos3a.values()))
# ---- o relatorio: pronta, falta e o que cada portao falso EXIGE
falta = list((PREP or {}).get("falta") or [])
L_PEND = linha("p00_precondicoes_v411.py", 'pend("a folga do MEMORY.md'); L_P00 = linha("gerar_relatorio_v411.py", '    "p00": bool('); L_CAD = linha("gerar_relatorio_v411.py", '    "cadeia_limpa_ate_o_relatorio": bool(')
_pend_p00 = [x_.get("checagem") for x_ in PC.get("pendentes") or []]
exige = {}
for k_ in falta:
    if k_ == "p00":
        exige[k_] = ("o portao p00 (gerar_relatorio_v411.py, linha %s) exige o veredito TODAS PASSARAM; o p00 desta rodada: %s; pendentes: %s. O pendente da folga do MEMORY.md e do pino do MEMORY.md e' INCONDICIONAL "
                     "(p00_precondicoes_v411.py, linha %s): como esta' escrito, nenhum ato o apaga" % (L_P00, PC.get("veredito"), _pend_p00, L_PEND))
    elif k_ == "cadeia_limpa_ate_o_relatorio":
        exige[k_] = ("o portao cadeia_limpa_ate_o_relatorio (gerar_relatorio_v411.py, linha %s) exige todo rc=0 no cadeia_v411_out.txt, sem PARADO e sem Traceback, com o passo 15; passos com rc diferente de 0 nesta rodada: %s "
                     "(o p00 devolve rc 3 enquanto houver pendente; a cadeia aceita o 3, o portao nao); PARADO: %s; Traceback no out: %s" % (L_CAD, rc_nao_zero, parados[:3], "Traceback" in CAD))
    else:
        exige[k_] = "portao falso nesta rodada: ver o quadro dos portoes em RELATORIO_PREPARACAO_v411.md e PREPARACAO_v411_PRONTA.json (portoes)"
so_atos_da_gerencia = bool(PREP is not None and set(falta) <= {"p00", "cadeia_limpa_ate_o_relatorio"} and rc_nao_zero and all(p_.startswith(("14_p00", "17_p00")) and r_ == 3 for p_, r_ in rc_nao_zero)
                           and all(str(x_).startswith(("PINO_MEMORIA_PY_v411.json", "a folga do MEMORY.md")) for x_ in _pend_p00))
MARCOS = {"candidato": cand16, "manifesto": s16(DL.MANIFESTO_ARQ), "topo_ratificado": s16(DL.TOPO_RATIFICADO_ARQ), "esperados": s16(S("ESPERADOS_v411.json")), "ensaio_a_seco": s16(S("ensaio_a_seco_v411.json")),
          "conferencia_controle_negativo": s16(S("conferencia_rito_v411_CONTROLE_NEGATIVO_PRE_RITO.json")), "conferencia_positivo_falso_nos": s16(S("conferencia_rito_v411_POSITIVO_FALSO_NOS.json")),
          "citacoes": s16(S("conferir_citacoes_v411.json")), "pinos_bn": s16(S("PINOS_BN_v411.json")), "derivacao": s16(S("DERIVACAO_v411.json")), "precondicoes": s16(S("PRECONDICOES_v411.json")),
          "pronto_para_o_pos_rito": s16(PRON_P), "cadeia_v411_out": s16(CAD_P), "purga": s16(S("purga_v411.json")), "varredura_fock_omega": s16(S("VARREDURA_FOCK_OMEGA_v411.json")),
          "preparacao_pronta": s16(PREP_P), "plano": s16(S("PLANO_v411.md")), "relatorio": s16(S("RELATORIO_PREPARACAO_v411.md")), "cadeia_v411_sh": s16(os.path.join(HERE, "cadeia_v411.sh"))}
_ant_c16 = (ANT.get("candidato") or {}).get("sha16")
_n_ok = sum(1 for v_ in passou.values() if v_)
estado = ("CADEIA REAL, estado final do fork C: candidato %s; %d de %d marcos passaram (falsos: %s); a cadeia inteira (cadeia_v411.sh) %s; o relatorio: pronta = %s, falta = %s%s"
          % (cand16, _n_ok, len(passou), [k_ for k_, v_ in passou.items() if not v_], ("chegou ao fim (inicio %s, fim %s)" % (cad_ini.group(1) if cad_ini else "?", cad_fim.group(1))) if cad_fim else ("NAO chegou ao fim (ultimo passo: %s)" % (passos[-1] if passos else "nenhum")),
             (PREP or {}).get("pronta"), falta, "; o que falta sao SO' os dois portoes que dependem dos atos da gerencia (a folga e o pino do MEMORY.md)" if so_atos_da_gerencia else ""))
out = dict(ANT)
out.update({
    "quando": datetime.datetime.now().isoformat(timespec="seconds"), "agente": "claude-construtor-v411 (retomada; principal + forks A, B e C); esta regravacao UNICA: fork C, no fim da cadeia real (ordem 3(b) da gerencia c1)",
    "topo_ratificado_presente": os.path.exists(DL.TOPO_RATIFICADO_ARQ), "topo_ratificado_sha256": DL.TOPO_SHA256, "estado": estado,
    "candidato": {"arquivo": DL.CANDIDATO_ARQ, "sha16": cand16, "manifesto_sha16": CM.get("sha16"), "n_patches": CM.get("n_patches"), "verbatins_embutidos": CM.get("verbatins_embutidos"), "n_bandeiras": CM.get("n_bandeiras"), "topo": CM.get("topo"),
                  "substitui_o_do_relatorio_do_principal": _ant_c16 if _ant_c16 != cand16 else None,
                  "regeneracoes_na_cadeia_real": ["16871a350670d80c -> 652eaa4f201682bc: a fonte AUSENTE de um marcador do topo derrubava o artigo da variante sem o registro da v397 (ValueError no build); passou a dizer, visivel, que o resultado nao e' dito",
                                                   "652eaa4f201682bc -> %s: o pdflatex parava em Missing $ inserted (o sublinhado de um veredito de maquina fora do modo matematico no texto ratificado do topo); o conversor _v411_tex_misto passou a escapar o sublinhado no modo texto" % cand16]},
    "o_que_passou": passou, "marcos_sha16": MARCOS,
    "ensaio_a_seco": {"veredito": EN.get("veredito"), "sha16_do_candidato": EN.get("sha16"), "arquivo": S("ensaio_a_seco_v411.json")},
    "condicao_3a_da_gerencia": {"regra": "a variante de recuo do topo (a fonte de um marcador ausente; o registro sem selar) nunca passa como selo: o ensaio a seco e o conferidor do rito FALHAM se o topo do artigo selado vier sem o resultado (os doze marcadores preenchidos, as duas linhas juntas)",
                                "conferencia": "topo_com_resultado_v411.py: independente da funcao do candidato (o texto e os formatos do TOPO_RATIFICADO_v411.json, os numeros do core; do candidato so' a tabela de caminhos e os dois renderizadores)",
                                "no_ensaio_a_seco": {"artigo": topo3a, "o_artigo_de_recuo_sem_a_v397_e_reprovado": var3a, "o_artigo_de_recuo_sem_o_registro_da_v411_e_reprovado": var3a11},
                                "no_conferidor_do_rito": {"onde": "conferir_rito_v411.py: o item proprio de DEVE (topo411_resultado_ok) e o detalhe em topo_com_o_resultado_v411 no JSON", "no_falso_nos": pos3a,
                                                          "o_que_ja_havia": "quadro411_ok procurava so' o PREFIXO do topo: reprovava o recuo por consequencia, e um artigo com o prefixo seguido de outra coisa passaria"},
                                "controles_negativos": "sete sinteticos (sem a v397 no core; o registro sem selar; um marcador nao finito; o texto do candidato diferente do ratificado; o topo de recuo; sem a linha das Cefeidas livres; so' o prefixo) e os dois artigos de recuo compilados pelo ensaio",
                                "ok": cond3a_ok},
    "citacoes": {"ok": CIT.get("ok"), "ok_do_um_py": CIT.get("ok_do_um_py"), "ok_do_pos_rito": CIT.get("ok_do_pos_rito"), "regra_do_pos_rito": CIT.get("regra_do_pos_rito"), "n_rotulos": CIT.get("n_rotulos"), "residuo_do_pos_rito": CIT.get("nao_verbatim_do_pos_rito"),
                 "saltados_no_pos_rito": CIT.get("pos_rito_saltados"),
                 "concatenacao": "trecho com + ou %s nao e' residuo: como na v410, a concatenacao cerca, em execucao, um trecho VERBATIM lido do arquivo do operador por sha256 (ou e' molde de formatacao); o trecho e' conferido onde e' lido, nao no fonte",
                 "historia": "o residuo unico (um comentario em pos_rito\\textos_custodia_handoff_v411.py) foi consertado pela gerencia as 14h39 de 12/11"},
    "p00": {"veredito": PC.get("veredito"), "n_falhas": PC.get("n_falhas"), "pendentes": _pend_p00},
    "pronto_para_o_pos_rito": {"arquivo": PRON_P, "existe": bool(PRON), "modo": PRON.get("modo"), "artefato_sha16": PRON.get("artefato_sha16")},
    "parada_das_14h39_no_passo_4": {"o_que": "o fim_de_cadeia_v411.sh das 14h37 passou as etapas 1 a 3 e parou na etapa 4 (a derivacao do pos-rito, da outra frente): pos_rito\\ trazia DIGITADAS nove falas e as seis decisoes ate' a D170; o delta tem %d falas e %d decisoes (%s)"
                                             % (DL.N_FALAS_V411, len(DL.DECISOES_V411), DL.DECISOES_TOKEN_V411),
                                    "a_lista_dos_pinos_velhos": "PEDIDOS_ENTRE_FRENTES_v411.md, a nota com a marca fork_c_parada_passo4_12nov",
                                    "o_conserto": "[DECLARADO pela gerencia c1, 12/11 ~14h50] um agente dela consertou pos_rito\\ (backups .bak_20261112_144557_delta11): tudo passou a ler DL.N_FALAS_V411, DL.DECISOES_V411 e DL.DECISOES_TOKEN_V411; o fork C nao editou pos_rito\\",
                                    "depois_do_conserto": DRV_RES},
    "cadeia_inteira": {"script": "cadeia_v411.sh", "arquivo_de_saida": CAD_P, "inicio": cad_ini.group(1) if cad_ini else None, "fim_rc0": cad_fim.group(1) if cad_fim else None, "passos": passos, "PARADO": parados,
                       "fim_de_cadeia_no_passo_15": {"etapas_vistas": fim_etapas, "chegou_ao_FIM": fim_ok, "FALHOU": fim_falhou},
                       "instrucao": "depois de QUALQUER novo conserto em pos_rito\\ (ou em script da cadeia), rodar a cadeia_v411.sh INTEIRA de uma vez: o portao cadeia_limpa_ate_o_relatorio le o cadeia_v411_out.txt; passo rodado a mao nao conta"},
    "varredura_fock_omega": {"n_novos": (VF or {}).get("n_novos"), "arquivos": (VF or {}).get("arquivos"), "nota": "nenhum passo da cadeia_v411.sh a roda e o relatorio a exige: o fork C a rodou por fora, antes da cadeia inteira (para o portao) e depois dela (com o relatorio e o plano no conjunto)"},
    "preparacao_pronta": {"arquivo": PREP_P, "existe": PREP is not None, "pronta": (PREP or {}).get("pronta"), "falta": falta, "o_que_o_relatorio_exige": exige, "falta_so_o_que_depende_dos_atos_da_gerencia": so_atos_da_gerencia},
    "tmp_na_pasta": [p_ for p_ in glob.glob(os.path.join(HERE, "**", "*.tmp"), recursive=True)],
})
_interp = list(ANT.get("interpretacoes_para_a_gerencia") or [])
for x_ in ("a interpretacao do marcador sem fonte (a fonte AUSENTE vira a frase visivel) foi ACEITA pela gerencia c1 em 12/11 com a CONDICAO 3(a): essa variante nunca passa como selo (ver condicao_3a_da_gerencia)",
           "condicao 3(a): o numero sustenta a frase do texto ratificado (o primario a n >= 5; as Cefeidas livres abaixo de 5; o z_disc abaixo do degrau de 5): se o core mudar esses numeros, o topo selado reprova, em vez de sair com a frase errada",
           "o conferidor do rito julga os trechos HERDADOS selados da v410 (as secoes da IALD2, da Escala e do H0DN pre-registrado) com a guarda de frases da v410, por caminho, e o texto novo da v411 com a guarda da v411: a mesma politica do ensaio a seco"):
    if x_ not in _interp:
        _interp.append(x_)
out["interpretacoes_para_a_gerencia"] = _interp
out["nao_verificado"] = ["o rito real e o conferidor DEPOIS do rito: o falso Nos e' emulacao (o core, o selo e o stdout vem do ensaio a seco, nao do rito)",
                         "a instalacao e o S3: instalar_v411.py, reverter_v411.py e rito_v411.sh so' foram conferidos estaticamente (DERIVACAO_v411.json), nunca executados",
                         "a revisao de terceiro, fechar_preparacao_v411.py e acom_inscrever_prep_v411.py (atos da gerencia; nao executados)",
                         "os testes que o agente da gerencia rodou dentro de pos_rito\\ depois do conserto (declarados por ela); aqui rodaram a derivacao, os dois harnesses e a previa do X, pelo fim_de_cadeia",
                         "o PDF do artigo: o topo foi conferido no .tex e no .txt (o pdflatex compila com rc 0); a pagina rendida nao foi lida",
                         "as traducoes EN do construtor (o titulo e as frases EN do quadro, o item da fala do autor): marcadas para a revisao"]
b = json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8")
print("estado:", estado[:700]); print("falsos:", [k_ for k_, v_ in passou.items() if not v_], "| 3(a):", cond3a_ok, "| exige:", json.dumps(exige, ensure_ascii=False)[:900]); print("marcos:", json.dumps({k_: MARCOS[k_] for k_ in ("candidato", "esperados", "ensaio_a_seco", "preparacao_pronta")}))
if SECO:
    print("--seco: nada gravado (%d bytes montados)" % len(b)); sys.exit(0)
if os.path.exists(P):
    _bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_forkc_final"; open(_bak, "wb").write(open(P, "rb").read()); assert open(_bak, "rb").read() == open(P, "rb").read()
open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P)
print("PRONTO_PARA_GERAR_v411.json gravado:", sha(P)[:16], len(b), "bytes")
