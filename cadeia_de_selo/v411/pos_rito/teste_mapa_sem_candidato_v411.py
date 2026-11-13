# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-sonnet-posrito-M-v411] REESCRITO para o registrar_mapa_v411 novo (H0DN x BG1 aberto e recalculado no rito): usa TESTE_H0DN_OFFLINE_v411_registro.json no lugar de core["h0dn_bg1_v411"], monta() INTEIRA contra o core da v410 selada (base_v410) mais os registros novos sinteticos, valida cada registro pela MESMA rotas._valida (sem registrar), e controles negativos
"""teste_mapa_sem_candidato_v411.py -- (claude-sonnet-posrito-M-v411, 12/11/2026) o teste POSSIVEL SEM CANDIDATO do registrar_mapa_v411.py (so' leitura do livro do mapa; NADA e' registrado, NADA e' gravado em pos_rito):
(1) as rotas anotadas e as citadas em refs existem no livro e a nova (umpy.v411.selada_h0dn_aberto_12nov) nao existe; os seq que o texto cita (abertura, marca ratificada, publicacao, preparacao) sao LIDOS do livro;
(2) os FATOS do registro h0dn_bg1_v411 (consts_mapa_x_v411.fatos_h0dn) lidos de TESTE_H0DN_OFFLINE_v411_registro.json (o substituto do core: as chaves congeladas) e os controles negativos (cada divergencia TEM de levantar AssertionError);
(3) montar() INTEIRA, com o core da v410 selada (base_v410/um_absoluto.json, so' leitura) mais h0dn_bg1_v411 (o registro offline), cunhagens_v411 e kh_n1_cobertura_v411 SINTETICOS (numeros de brinquedo so' nas contagens; nada disto vai a texto publicado), selo, ESPERADOS e V sinteticos;
(4) cada registro montado passa na MESMA funcao que o mapa usa (rotas._valida, importada so' para isso; o livro so' e' lido), na guarda de frases da v411 (que inclui a P18, a F60 a F67), na P18, na D59, na D65 e na regra da obrigacao (os dois numeros no mesmo campo);
(5) controles negativos: tirar a linha das Cefeidas livres, o modelo publicado, a validade, a retrodicao ou o nao cego de um campo que traz o primario TEM de reprovar na guarda; a palavra da creditacao TEM de reprovar na guarda e no Mapa; montar() TEM de recusar o selo de outra versao, a rota nova ja' existente, o registro nao selado, o gate ou a escada mudados, etc.
Saidas: o json montado vai para a pasta temporaria passada por argumento (padrao: o scratchpad do agente), nunca para pos_rito. uso: python -B -X utf8 teste_mapa_sem_candidato_v411.py [pasta_temporaria]   rc 0 = passou."""
import copy, importlib.util, json, os, re, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
sys.stdout.reconfigure(encoding="utf-8")
TMP = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else tempfile.mkdtemp(prefix="teste_mapa_v411_")
os.makedirs(TMP, exist_ok=True)
assert os.path.normcase(TMP) != os.path.normcase(HERE) and not os.path.normcase(TMP).startswith(os.path.normcase(PK)), "a saida do teste nao pode ir para a pasta da cadeia"
import delta_v411 as DL  # noqa: E402
import consts_mapa_x_v411 as C  # noqa: E402
import registrar_mapa_v411 as M  # noqa: E402
import guarda_frases_v411 as GF  # noqa: E402
from guarda_p18_v411 import violacoes  # noqa: E402
OK = [True]


def check(nome, cond, extra=""):
    print("  %-96s %s%s" % (nome, "ok" if cond else "FALHOU", (" -- " + str(extra)) if extra else ""))
    if not cond:
        OK[0] = False
    return bool(cond)


def levanta(fn):
    try:
        fn()
    except AssertionError:
        return True
    except Exception as ex:  # noqa: BLE001  (um erro de OUTRO tipo nao e' a recusa que o teste espera)
        print("     (levantou %s em vez de AssertionError: %s)" % (type(ex).__name__, str(ex)[:160]))
        return False
    return False


print("== (1) as rotas e os seq do livro (so' leitura)")
ids = M.ids_do_livro(); regs = M.livro()
falt = [r for r in M.ANOTADAS + M.REFS if r not in ids]
check("rotas anotadas+refs existem no livro (%d); ausentes: %s" % (len(M.ANOTADAS + M.REFS), falt), not falt)
check("a rota nova nao existe no livro (%s)" % M.NOVA, M.NOVA not in ids)
check("as anotadas nao se repetem; o H0DN e a publicacao estao entre elas", len(set(M.ANOTADAS)) == len(M.ANOTADAS) and M.R_H0DN in M.ANOTADAS and M.R_PUBL in M.ANOTADAS and M.R_H0DN_COV in M.REFS)
sq_ab = M.seq_do_alvo(regs, M.R_H0DN, "RESULTADO", inicio_do_titulo="H0DN x BG1 (12/11): ABERTURA", contem=("Cefeidas livres",))
sq_pre = M.seq_do_alvo(regs, M.R_H0DN, "ANOTACAO", inicio_do_titulo="H0DN x BG1 (12/11): marca ratificada", contem=("literal dos vereditos",))
sq_pub = M.seq_do_alvo(regs, M.R_PUBL, "RESULTADO", contem=("f24d954a3b90",)); sq_pubr = M.seq_do_alvo(regs, M.R_PUBL, "ROTA"); sq_prep = M.seq_do_alvo(regs, M.R_PREP411, "ROTA")
check("seq lidos do livro: abertura %s, marca ratificada %s, publicacao %s (ROTA %s), preparacao %s" % (sq_ab, sq_pre, sq_pub, sq_pubr, sq_prep), all(isinstance(x_, int) for x_ in (sq_ab, sq_pre, sq_pub, sq_pubr, sq_prep)))
check("controle negativo: seq_do_alvo recusa um titulo que nao existe", levanta(lambda: M.seq_do_alvo(regs, M.R_H0DN, "RESULTADO", inicio_do_titulo="nao existe esse titulo")))
check("controle negativo: seq_do_alvo recusa um trecho que o registro nao traz", levanta(lambda: M.seq_do_alvo(regs, M.R_H0DN, "RESULTADO", inicio_do_titulo="H0DN x BG1 (12/11): ABERTURA", contem=("texto que nao esta' no registro",))))

print("== (2) os fatos do registro h0dn_bg1_v411 (o substituto do core: TESTE_H0DN_OFFLINE_v411_registro.json)")
HD = json.load(open(os.path.join(PK, "TESTE_H0DN_OFFLINE_v411_registro.json"), encoding="utf-8"))
F = C.fatos_h0dn(HD)
check("os numeros dos fatos sao os do registro (primario %s contra o nulo, %s contra K, ramo %d; Cefeidas livres %s, ramo %d)" % (F["zn_pt"], F["zk_pt"], F["ramo_p"], F["cn_pt"], F["ramo_c"]),
      F["zn"] == HD["values"]["primario"]["z_null"] and F["zk"] == HD["values"]["primario"]["z_tgl"] and F["cn"] == HD["linha_ao_lado_cefeidas_livres"]["z_null"] and F["ramo_p"] == 4 and F["ramo_c"] == 6 and F["n_sigma"] == 6)
check("a moldura do delta, preenchida: traz os dois numeros e os cinco obrigatorios", all(x_ in C.moldura_pt(F) for x_ in (F["zn_pt"], F["zk_pt"], F["cn_pt"], DL.OBRIG_MODELO_PT, DL.OBRIG_CEFEIDAS_PT, DL.OBRIG_VALIDADE_PT, DL.OBRIG_RETRO_PT, DL.OBRIG_NAO_CEGO_PT)))
check("a moldura EN traz os cinco obrigatorios em ingles", all(x_ in C.moldura_en(F) for x_ in (F["zn_en"], F["cn_en"], DL.OBRIG_MODELO_EN, DL.OBRIG_CEFEIDAS_EN, DL.OBRIG_VALIDADE_EN, DL.OBRIG_RETRO_EN, DL.OBRIG_NAO_CEGO_EN)))


def mut(f_):
    h_ = copy.deepcopy(HD); f_(h_); return h_


def setv(d_, caminho_, v_):
    for k_ in caminho_[:-1]:
        d_ = d_[k_]
    d_[caminho_[-1]] = v_


NEG_F = {"nao selou": lambda h: h.update(all_verified=False), "nao foi aberto uma vez": lambda h: h.update(opened_once=False), "sem a linha ao lado": lambda h: h.pop("linha_ao_lado_cefeidas_livres"),
         "sem as ressalvas": lambda h: h.pop("ressalvas_secao8"), "seis ressalvas": lambda h: h.update(ressalvas_secao8=h["ressalvas_secao8"][:6]), "so' quatro itens do que nao decide": lambda h: h.update(o_que_o_teste_nao_decide=h["o_que_o_teste_nao_decide"][:4]),
         "veredito sem o sufixo do gate": lambda h: h.update(verdict=h["verdict"].replace("__GATE_UNMOVED", "")), "veredito com outro prefixo": lambda h: h.update(verdict="OUTRO_" + h["verdict"]),
         "veredito diz 5SIGMA e o numero e 6": lambda h: h.update(verdict=h["verdict"].replace("6SIGMA", "5SIGMA")), "veredito sem o ramo das Cefeidas": lambda h: h.update(verdict=h["verdict"].replace("BELOW_5SIGMA__BRANCH_6", "BELOW_5SIGMA__BRANCH_5")),
         "veredito sem a faixa K_LAW_": lambda h: h.update(verdict=h["verdict"].replace("__K_LAW_", "__")), "Cefeidas livres diferem do topo": lambda h: setv(h, ("linha_ao_lado_cefeidas_livres", "z_null"), 4.5),
         "o mesmo modelo nas duas linhas": lambda h: setv(h, ("values", "cefeidas_livres", "modelo"), h["values"]["primario"]["modelo"]), "cabeca do topo difere": lambda h: h.update(cabeca_do_teste=h["cabeca_do_teste"] + "X"),
         "desfecho difere": lambda h: setv(h, ("values", "cefeidas_livres", "outcome"), "OUTRO"), "Z nao finito": lambda h: setv(h, ("values", "primario", "z_null"), float("nan")), "ramo nao inteiro": lambda h: setv(h, ("values", "primario", "ramo"), 4.0),
         "ordem dos atos invertida": lambda h: setv(h, ("values", "atos", "push_do_resultado_utc"), "2026-11-12T10:00:00Z"), "commit do pre-voo != o do pre-registro": lambda h: setv(h, ("values", "atos", "commit_do_pre_voo"), "0" * 40),
         "sem values.atos": lambda h: h["values"].pop("atos"), "sem runtime_executed": lambda h: h.update(runtime_executed=False), "cosmologia movendo o gate (does_not_gate_core False)": lambda h: h.update(does_not_gate_core=False)}
for k_, f_ in NEG_F.items():
    check("controle negativo de fatos_h0dn: %s" % k_, levanta(lambda f_=f_: C.fatos_h0dn(mut(f_))))

print("== (3) h0dn_do_core (o registro contra ESPERADOS, o delta e a v410 selada) e h0dn_textos")
BC = M._base_core()
GATE = BC["qg_closure"]["gate"]["verdict"]; ESC = BC["external_ladder"]["n_theorems_expected"]
PIN64 = "0123456789abcdef" * 4
ESP = {"candidato_sha16": PIN64[:16], "origem_sha16": DL.BASE_SHA16_DA_ORDEM, "escada_v410_e_v411": [ESC, ESC], "n_bandeiras_novas": 0, "chaves_v411": [], "qg_closure_gate_verdict_v410": GATE, "qg_closure_verdict": GATE,
       "vereditos_novos_v411": {DL.FECHO_REGISTRO: HD["verdict"], DL.CUNHAGENS_REGISTRO: "TGL_CUNHAGENS_V411__SINTETICO__GATE_UNMOVED", DL.KH_REGISTRO: "TGL_KH_N1_COBERTURA_V411__SINTETICO__GATE_UNMOVED"}}
FC = M.h0dn_do_core(DL, HD, ESP, BC)
check("h0dn_do_core: %d checagens, o pre-registro h0dn_bg1_v410 intacto (veredito da base lido)" % FC["n_checks"], FC["n_checks"] == DL.N_CHECKS_FECHO == 16 and FC["antigo"] == "h0dn_bg1_v410" and FC["antigo_verdict_base"])
NEG_C = {"ESPERADOS sem o veredito do h0dn": lambda h, e: e["vereditos_novos_v411"].pop(DL.FECHO_REGISTRO), "ESPERADOS com outro veredito": lambda h, e: e["vereditos_novos_v411"].update({DL.FECHO_REGISTRO: "OUTRO"}),
         "uma checagem falha": lambda h, e: h["mechanics"]["checks"][-1].update(ok=False), "15 checagens": lambda h, e: (h["mechanics"].update(n_checks=15), h["mechanics"]["checks"].pop()), "mechanics.passed False": lambda h, e: h["mechanics"].update(passed=False),
         "beta_ok False": lambda h, e: h.update(beta_ok=False), "gate diferente da v410": lambda h, e: h["values"].update(gate_verdict="OUTRO"), "escada diferente da v410": lambda h, e: h["values"].update(escada=ESC + 1),
         "a guarda de frases acusou algo": lambda h, e: h["values"].update(frases_violacoes=[["F67", "x"]]), "a P18 acusou algo": lambda h, e: h["values"].update(p18_violacoes=[["R1", "x"]]), "tocou a pasta vedada do Kimi": lambda h, e: h["values"].update(sob_pasta_vedada=["x"])}
for k_, f_ in NEG_C.items():
    def _roda(f_=f_):
        h_, e_ = copy.deepcopy(HD), copy.deepcopy(ESP); f_(h_, e_); M.h0dn_do_core(DL, h_, e_, BC)
    check("controle negativo de h0dn_do_core: %s" % k_, levanta(_roda))
check("controle negativo: registro ausente", levanta(lambda: M.h0dn_do_core(DL, {}, ESP, BC)))
CTX = {"S": PIN64[:16], "sq_abertura": sq_ab, "res16": DL.INSUMO_POR_NOME["RESULTADO_DA_ABERTURA_V411.json"]["sha256"][:16], "prereg16": DL.INSUMO_POR_NOME["EMENDA_E_PRE_REGISTRO_V411.md"]["sha256"][:16]}
TH = M.h0dn_textos(DL, FC, CTX)
for campo_, txt_ in TH.items():
    check("h0dn_textos[%s]: %d caracteres (<= 6000); passa na guarda de frases e na P18" % (campo_, len(txt_)), len(txt_) <= 6000 and not GF.violacoes(txt_) and not violacoes(txt_), (GF.violacoes(txt_) + violacoes(txt_))[:2])
check("h0dn_textos: titulo, resultado e defeito trazem a moldura ou a cauda das obrigacoes", C.moldura_pt(FC) in TH["titulo"] and C.moldura_pt(FC)[0].upper() + C.moldura_pt(FC)[1:] in TH["resultado"] and C.cauda_pt(FC) in TH["defeito"] and C.cauda_pt(FC) in TH["proximo"])
check("h0dn_textos: os dois numeros no resultado (4 casas) e a ordem dos atos", FC["zn4_pt"] in TH["resultado"] and FC["cn4_pt"] in TH["resultado"] and FC["atos"]["push_do_pre_registro_utc"] in TH["resultado"] and FC["atos"]["commit_do_resultado"][:12] in TH["resultado"])
check("h0dn_textos: as sete ressalvas (lidas do registro) no defeito", all(r_ in TH["defeito"] for r_ in FC["ressalvas"]))

print("== (4) montar() INTEIRA contra o core da v410 selada + os registros novos (o h0dn offline; cunhagens e kh sinteticos)")
CG = {"all_verified": True, "verdict": ESP["vereditos_novos_v411"][DL.CUNHAGENS_REGISTRO], "verbatim": {"f%d" % i_: {"citado_por_sha256": True, "texto_transcrito": False, "sha256": "%064x" % i_} for i_ in range(DL.N_FALAS_V411)}, "extras": {"decisoes": dict(DL.DECISOES_V411)},
      "erratas": [{"agora": e_["texto"], "assinatura": DL.ASSINA} for e_ in DL.ERRATAS_V411] + [{"agora": "pisos de kh_n1_cobertura_v410 (sintetico)", "assinatura": DL.ASSINA, "ao_lado_de": "kh_n1_cobertura_v410"}]}
KH = {"all_verified": True, "verdict": ESP["vereditos_novos_v411"][DL.KH_REGISTRO], "lido": {"constantes_cobertas": 1, "teoremas_cobertos": 1}}


def core_novo(f_=None):
    c_ = dict(BC)   # (raso: so' acrescenta chaves; nenhum registro da base e' mutado)
    c_[DL.FECHO_REGISTRO] = copy.deepcopy(HD); c_[DL.CUNHAGENS_REGISTRO] = copy.deepcopy(CG); c_[DL.KH_REGISTRO] = copy.deepcopy(KH)
    if f_:
        f_(c_)
    return c_


SELO = {"um_version": "v411", "sha256": {"um.py": PIN64}, "qg_closure_verdict": GATE}
V = {"s16": PIN64[:16], "sidecar": {"veredito": "ALL_OBJECTS_SEALED", "n_objetos": 3, "recusas": 0, "sha16": "0123456789abcdef"}, "conf_dm": "12/12", "conf_np": "30/30", "n_ver_mudaram": 0}
M._CACHE["esp"] = ESP
M._bancada = lambda: {"de": "v410", "geracao": DL.BANCADA_PINA_HOJE["n"], "proxima": DL.BANCADA_PINA_HOJE["n"] + 1, "deployment_id": DL.BANCADA_PINA_HOJE["deployment_id"]}   # (o PINOS_BN_v411.json so' existe depois do diff_e_pinos; o resto de montar() e' o real)
ARTS = [os.path.join(PK, "TESTE_H0DN_OFFLINE_v411_registro.json"), os.path.join(PK, "kernel", "KERNEL_RECIBO_v411.json")]
REG = M.montar(V, core_novo(), SELO, ids, ARTS)
check("montar(): %d registros (%s); a ROTA nova e as anotacoes" % (len(REG), ", ".join(x["tipo"][:4] + ":" + x["rota_id"].split(".")[-1][:22] for x in REG)), len(REG) == 1 + len(M.ANOTADAS) and REG[0]["tipo"] == "ROTA" and REG[0]["rota_id"] == M.NOVA and [x["rota_id"] for x in REG[1:]] == list(M.ANOTADAS))
pj = os.path.join(TMP, "registro_mapa_v411_TESTE.json"); open(pj, "w", encoding="utf-8").write(json.dumps(REG, ensure_ascii=False, indent=1))
print("     json montado (so' no temporario): %s (%d B)" % (pj, os.path.getsize(pj)))
for x in REG:
    j_ = json.dumps(x, ensure_ascii=False)
    check("%-9s %-62s %5d B; guardas de frases, P18, D59, D65 limpas" % (x["tipo"], x["rota_id"], len(j_.encode("utf-8"))), not GF.violacoes(j_) and not violacoes(j_) and not M.d59_viola(j_) and not any(f_.lower() in j_.lower() for f_ in DL.FORA_D65), (GF.violacoes(j_) + violacoes(j_))[:2])
check("a ROTA e a anotacao do H0DN dizem olhou_dados True (o vetor da abertura unica, relido); as outras dizem False", REG[0]["olhou_dados"] is True and REG[1]["olhou_dados"] is True and all(x["olhou_dados"] is False for x in REG[2:]))
check("o veredito de maquina da ROTA e' o do registro, exato", REG[0]["veredito"] == HD["verdict"])
check("a ROTA e o H0DN dizem os dois numeros, as sete ressalvas e a ordem dos atos; nenhum campo cita o 4,44", all(F[k_] in json.dumps(REG[0], ensure_ascii=False) for k_ in ("zn4_pt", "cn4_pt")) and all(r_ in json.dumps(REG[1], ensure_ascii=False) for r_ in FC["ressalvas"]) and not any("4,44" in s_ for x in REG for s_ in M._strings(x)))
check("regra do 4,44 (controle): o numero sem o p e sem a linha dos 5 sigma reprova; a clausula completa passa", bool(M.regra_4_44([{"c": "z_disc = 4,44"}], "4,44", "4,4×10⁻⁶")) and not M.regra_4_44([{"c": "z_disc = 4,44 (calibrado; p unilateral 4,4×10⁻⁶), abaixo do degrau de 5σ, que não foi alcançado (4,44 < 5)"}], "4,44", "4,4×10⁻⁶"))
# --- cada registro passa na MESMA funcao que o mapa usa (rotas._valida); o livro so' e' lido
sp_ = importlib.util.spec_from_file_location("rotas_ro", os.path.join(M.MAPA, "rotas.py")); rotas = importlib.util.module_from_spec(sp_); sp_.loader.exec_module(rotas)
seqs = {r_["seq"] for r_ in regs if isinstance(r_.get("seq"), int)}
val = []
for x in REG:
    try:
        rotas._valida(json.loads(json.dumps(x)), set(ids), seqs); val.append(True)
    except Exception as ex:  # noqa: BLE001
        val.append(False); print("     rotas._valida recusou %s: %s: %s" % (x["rota_id"], type(ex).__name__, str(ex)[:260]))
check("rotas._valida (a funcao do Mapa; sem registrar) aceita os %d registros" % len(REG), all(val))


def valida_mapa(x_):
    rotas._valida(json.loads(json.dumps(x_)), set(ids), seqs)


def recusa_valor(fn):
    """True se a funcao do Mapa recusa (ValueError, que e' o erro que rotas._valida levanta)."""
    try:
        fn()
    except ValueError:
        return True
    return False


PALAVRA = "CONF" + "IRMED"   # (a palavra da creditacao, montada por concatenacao como nos outros guardas)
x_ = copy.deepcopy(REG[0]); x_["resultado"] = x_["resultado"] + " O teste foi " + PALAVRA + " pela natureza."
check("controle negativo: o Mapa recusa a palavra da creditacao afirmada em resultado (a guarda do Mapa esta' viva)", recusa_valor(lambda: valida_mapa(x_)))
check("controle negativo: a guarda de frases da v411 recusa a mesma frase (F60)", any(v_[0].startswith("F60") for v_ in GF.violacoes(json.dumps(x_, ensure_ascii=False))))
check("a forma certa passa no Mapa: a ROTA nao afirma a palavra da creditacao (a creditacao e' de quem observa de fora)", not recusa_valor(lambda: valida_mapa(REG[0])))

print("== (5) controles negativos de TEXTO: cada obrigacao tirada de um campo que traz o primario TEM de reprovar na guarda de frases (F67)")
M_ = C.moldura_pt(F); base_ = REG[0]["resultado"]
alvo_ = M_ if M_ in base_ else (M_[0].upper() + M_[1:])
assert alvo_ in base_, "a moldura nao esta' no resultado da ROTA"
tira = {"a linha das Cefeidas livres com o numero": ("as %s leem %s (ramo %d)" % (DL.OBRIG_CEFEIDAS_PT, F["cn_pt"], F["ramo_c"]), "cefeidas_livres_com_o_numero"),
        "sob o modelo de erros publicado": (DL.OBRIG_MODELO_PT, "modelo_publicado"), "validade, nao creditacao": (DL.OBRIG_VALIDADE_PT, "validade_nao_creditacao"), "retrodicao": (DL.OBRIG_RETRO_PT, "retrodicao"), "nao cego": (DL.OBRIG_NAO_CEGO_PT, "nao_cego")}
for nome_, (trecho_, esperado_) in tira.items():
    assert trecho_ in alvo_, (nome_, trecho_)
    sem_ = alvo_.replace(trecho_, "XXXX")
    txt_ = json.dumps({"resultado": "Primário: Z contra o nulo %s. %s" % (F["zn4_pt"], sem_)}, ensure_ascii=False)   # (um campo SO' com a moldura mutilada, mais a frase do primario: o que a F67 le)
    v_ = [x_[0] for x_ in GF.violacoes(txt_) if x_[0].startswith("F67")]
    check("sem %-46s a F67 reprova (%s)" % (nome_ + ":", v_[:1]), bool(v_) and esperado_ in v_[0])
completo_ = json.dumps({"resultado": "Primário: Z contra o nulo %s. %s" % (F["zn4_pt"], alvo_)}, ensure_ascii=False)
check("com as cinco obrigacoes a F67 passa", not [x_ for x_ in GF.violacoes(completo_) if x_[0].startswith("F67")])
EN_ = json.dumps({"resultado": "The primary lies %s against the null. %s" % (F["zn_en"], C.moldura_en(F))}, ensure_ascii=False)
check("EN: a moldura inteira passa na F67", not [x_ for x_ in GF.violacoes(EN_) if x_[0].startswith("F67")], GF.violacoes(EN_)[:2])
EN2_ = EN_.replace(DL.OBRIG_CEFEIDAS_EN, "XXXX")
check("EN: sem as free Cepheids a F67 reprova", any(x_[0].startswith("F67") and "cefeidas_livres_com_o_numero" in x_[0] for x_ in GF.violacoes(EN2_)))
# o texto do mapa montado, so' a linha das Cefeidas livres tirada do titulo da ROTA (o que o enunciado pede): TEM de ser recusado pela guarda
rr_ = copy.deepcopy(REG[0]); rr_["titulo"] = rr_["titulo"].replace("as %s leem %s (ramo %d); " % (DL.OBRIG_CEFEIDAS_PT, F["cn_pt"], F["ramo_c"]), "")
check("o titulo da ROTA SEM a linha das Cefeidas livres e' recusado pela guarda_frases_v411.violacoes", rr_["titulo"] != REG[0]["titulo"] and any(x_[0].startswith("F67") for x_ in GF.violacoes(json.dumps(rr_, ensure_ascii=False))))
check("e a regra da obrigacao do proprio montar() (a mesma leitura, por campo) o recusaria", bool([k_ for k_, v_ in rr_.items() if isinstance(v_, str) and re.search(C.RX_GATILHO_F67, v_, re.I) and not re.search(DL.OBRIG_CEFEIDAS_PT + r"[^\n]{0,160}?\d+,\d+", v_)]))
for rotulo_, extra_ in (("a palavra do teste cego", " Este foi um teste cego."), ("o poder certificado", " O teste tem poder certificado."), ("a evidencia independente", " É evidência independente das Fases 4, 5 e 9."),
                        ("a descoberta", " A descoberta do H0DN a 6 sigma."), ("o beta literal", " com beta = 0,0120313"), ("o vetor fora do suporte como erro de montagem", " O vetor fora do suporte é erro de montagem."), ("5 sigma atingido", " 5 sigma atingido no H0DN."),
                        ("a covariancia fisica fechada", " A covariância física está fechada."), ("P = nP resolvido sem o leitor", " O algoritmo polinomial em máquina de Turing padrão resolve P = nP.")):
    check("controle negativo de texto: %s" % rotulo_, bool(GF.violacoes(json.dumps({"x": REG[0]["nota"] + extra_}, ensure_ascii=False))) or bool(violacoes(extra_)))
for tk_ in (DL.TOKENS_PROIBIDOS_V411[0], DL.TOKENS_PROIBIDOS_V411[-1]):
    j_ = json.dumps(dict(REG[0], nota=REG[0]["nota"] + " " + tk_), ensure_ascii=False)
    check("controle negativo: o token proibido %s no registro e' achado pela leitura de tokens do montar()" % tk_, any(t_ in j_ for t_ in DL.TOKENS_PROIBIDOS_V411))
d59 = {"o Kimi fora do H0DN reprova": M.d59_viola("a ordem ao Kimi para outra coisa"), "o Kimi no contexto do H0DN passa": not M.d59_viola("a ORDEM ao Kimi do H0DN: montar y_obs"), "o Navier reprova": M.d59_viola("Navier-Stokes e o H0DN"), "o Milenio reprova": M.d59_viola("problema do Milênio")}
for k_, v_ in d59.items():
    check("D59: %s" % k_, v_)

print("== (6) montar() recusa (AssertionError) o que nao confere")


def _com_esp(e_):
    M._CACHE["esp"] = e_
    try:
        return M.montar(V, core_novo(), SELO, ids, ARTS)
    finally:
        M._CACHE["esp"] = ESP


NEG_M = {"o selo e' de outra versao": lambda: M.montar(V, core_novo(), dict(SELO, um_version="v410"), ids, ARTS), "a rota nova ja' existe no livro": lambda: M.montar(V, core_novo(), SELO, set(ids) | {M.NOVA}, ARTS),
         "uma rota anotada nao existe no livro": lambda: M.montar(V, core_novo(), SELO, set(ids) - {M.R_H0DN}, ARTS), "o um.py do selo nao e' o candidato": lambda: M.montar(V, core_novo(), dict(SELO, sha256={"um.py": "f" * 64}), ids, ARTS),
         "o s16 da leitura != o candidato": lambda: M.montar(dict(V, s16="ffffffffffffffff"), core_novo(), SELO, ids, ARTS),
         "o registro h0dn_bg1_v411 ausente do core": lambda: M.montar(V, core_novo(lambda c: c.pop(DL.FECHO_REGISTRO)), SELO, ids, ARTS),
         "o registro h0dn_bg1_v411 nao selou": lambda: M.montar(V, core_novo(lambda c: c[DL.FECHO_REGISTRO].update(all_verified=False)), SELO, ids, ARTS),
         "o registro h0dn sem a linha das Cefeidas livres": lambda: M.montar(V, core_novo(lambda c: c[DL.FECHO_REGISTRO].pop("linha_ao_lado_cefeidas_livres")), SELO, ids, ARTS),
         "o gate do core mudou": lambda: M.montar(V, core_novo(lambda c: c.update(qg_closure=dict(c["qg_closure"], gate=dict(c["qg_closure"]["gate"], verdict="OUTRO")))), SELO, ids, ARTS),
         "o gate do selo mudou": lambda: M.montar(V, core_novo(), dict(SELO, qg_closure_verdict="OUTRO"), ids, ARTS),
         "a escada do core mudou": lambda: M.montar(V, core_novo(lambda c: c.update(external_ladder=dict(c["external_ladder"], n_theorems_clean=ESC - 1))), SELO, ids, ARTS),
         "ESPERADOS diz que ha bandeira nova": lambda: _com_esp(dict(ESP, n_bandeiras_novas=1)),
         "ESPERADOS diz que uma chave antiga muda": lambda: _com_esp(dict(ESP, chaves_v411=["x"])), "a base de ESPERADOS nao e' a v410 selada": lambda: _com_esp(dict(ESP, origem_sha16="0" * 16)),
         "ESPERADOS sem o veredito novo do cunhagens_v411": lambda: _com_esp(dict(ESP, vereditos_novos_v411={DL.FECHO_REGISTRO: HD["verdict"]})),
         "um registro da v410 selada nao sela na v411": lambda: M.montar(V, core_novo(lambda c: c.update(iald2_v410=dict(c["iald2_v410"], all_verified=False))), SELO, ids, ARTS),
         "um registro da v410 selada sumiu do core": lambda: M.montar(V, core_novo(lambda c: c.pop("a_escala_v410")), SELO, ids, ARTS),
         "o pre-registro h0dn_bg1_v410 foi reescrito": lambda: M.montar(V, core_novo(lambda c: c.update(h0dn_bg1_v410=dict(c["h0dn_bg1_v410"], verdict="REESCRITO"))), SELO, ids, ARTS),
         "o cunhagens_v411 sem uma decisao": lambda: M.montar(V, core_novo(lambda c: c[DL.CUNHAGENS_REGISTRO]["extras"]["decisoes"].pop("D170")), SELO, ids, ARTS),
         "o cunhagens_v411 sem uma fala embutida": lambda: M.montar(V, core_novo(lambda c: c[DL.CUNHAGENS_REGISTRO]["verbatim"].pop("f0")), SELO, ids, ARTS),
         "o cunhagens_v411 sem a errata E43": lambda: M.montar(V, core_novo(lambda c: c[DL.CUNHAGENS_REGISTRO]["erratas"].pop(2)), SELO, ids, ARTS),
         "o kh_n1_cobertura_v411 nao selou": lambda: M.montar(V, core_novo(lambda c: c[DL.KH_REGISTRO].update(all_verified=False)), SELO, ids, ARTS),
         "o bandeiras_do_gate_v403 diferente da v410": lambda: M.montar(V, core_novo(lambda c: c.update(bandeiras_do_gate_v403=dict(c["bandeiras_do_gate_v403"], values=dict(c["bandeiras_do_gate_v403"]["values"], n_true=0)))), SELO, ids, ARTS)}
for k_, f_ in NEG_M.items():
    check("controle negativo de montar(): %s" % k_, levanta(f_))
check("depois dos controles, montar() com o core bom continua montando (o cache de ESPERADOS foi restaurado)", len(M.montar(V, core_novo(), SELO, ids, ARTS)) == len(REG))
src_ = open(os.path.join(HERE, "registrar_mapa_v411.py"), encoding="utf-8").read()
MARCA_ = "[A ADAPTAR v" + "411]"   # (por concatenacao: o p00 procura a marca em TODO arquivo da cadeia, inclusive neste)
check("o script nao tem a marca de copia mecanica nem a marca de trecho a reescrever", MARCA_ not in src_ and ("# TEXTO_A_REESCREVER" + "_V411") not in src_)
print("RESULTADO:", "PASSOU" if OK[0] else "REPROVOU")
sys.exit(0 if OK[0] else 1)
