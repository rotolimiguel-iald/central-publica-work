# -*- coding: utf-8 -*-
"""_prevoo_gerador_v410.py -- PRE-VOO do gerar_candidato_v410.py (09/11/2026, claude-construtor-v410): repete, SEM gravar nada, as assercoes que o gerador faz sobre as pecas NOVAS da v410 (contrato/texto da IALD2, contrato/texto/insumos
do H0DN, as fontes, as falas, os specs, o runtime emendado, os snippets do artigo): P18 (crua onde o motor v392 a aplica no rito; sem as falas embutidas onde o gerador varre o texto novo), a palavra recusada, a guarda das frases,
os literais de beta, as colisoes de nomes com a base, os caracteres de controle. O candidato NAO e' gerado (a gerencia libera). Grava PREVOO_GERADOR_v410.json. uso: python -B -X utf8 _prevoo_gerador_v410.py"""
import ast, hashlib, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
t0 = time.time()
import guarda_p18_v410 as GP  # noqa: E402
import delta_v410 as DL  # noqa: E402
import registros_v410 as RG  # noqa: E402
import registros_h0dn_v410 as RH  # noqa: E402
import registros_hms13_v410 as RF  # noqa: E402   (D80)
import registros_aescala_v410 as RA  # noqa: E402   (D86/D87)
import acom_conferencias_v410 as AC  # noqa: E402
import guarda_frases_v410 as GF  # noqa: E402
RT = GF.RT
sha256 = lambda b: hashlib.sha256(b).hexdigest(); sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONF" + r"IRMED|(?<!AP)PRO" + r"VED_BY|TGL_PRO" + r"VED")
R = {"quando": time.strftime("%Y-%m-%dT%H:%M:%S"), "checks": {}}


def chk(nome, cond, det=None):
    R["checks"][nome] = {"ok": bool(cond), "det": det}
    print(("OK   " if cond else "FALHA") + " " + nome + ("" if det is None else " -> " + str(det)[:200]))


BASE = os.path.join(HERE, DL.BASE_DIR)
raw = open(os.path.join(BASE, "um.py"), "rb").read(); T0 = raw.decode("utf-8")
selo0 = json.load(open(os.path.join(BASE, "um_absoluto_selo.json"), encoding="utf-8")); core0 = json.load(open(os.path.join(BASE, "um_absoluto.json"), encoding="utf-8"))["core"]
chk("a base e' a v409 selada", selo0.get("um_version") == DL.BASE_VERSION and sha256(raw) == selo0["sha256"]["um.py"] and sha16(raw) == DL.BASE_SHA16_DA_ORDEM, sha16(raw))
E409 = int(core0["external_ladder"]["n_theorems_expected"])
tree0 = ast.parse(T0)
top = lambda name: [n for n in tree0.body if (isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == name)][0]
old_d = ast.literal_eval(top("_EMBEDDED_KERNEL_FILES").value)
rd = lambda p: open(p, "r", encoding="utf-8", newline="").read()
KB = DL.SANDBOX
final_emb = dict(old_d); final_emb["TGLExt.lean"] = rd(os.path.join(KB, "TGLExt.lean")); final_emb["TGL/Audit.lean"] = rd(os.path.join(KB, "TGL", "Audit.lean"))
for rel in DL.BUNDLE_RELS:
    final_emb[rel] = rd(os.path.join(KB, *rel.split("/")))
chk("raiz do sandbox = raiz da base + o import; Audit igual", final_emb["TGLExt.lean"] == old_d["TGLExt.lean"] + DL.ROOT_SUFFIX and final_emb["TGL/Audit.lean"] == old_d["TGL/Audit.lean"])
FORMAL_MAP = {k: sha256(v.encode("utf-8")) for k, v in final_emb.items()}
chk("o modulo do sandbox == o pino do bundle", all(FORMAL_MAP[r_] == DL.BUNDLE_POR_REL[r_]["sha256"] for r_ in DL.BUNDLE_RELS))
KD = os.path.join(HERE, DL.KERNEL_DIR)
FJ = json.load(open(os.path.join(KD, "FLAGS_v410.json"), encoding="utf-8")); khj = json.load(open(os.path.join(KD, "KH_N1_v410.json"), encoding="utf-8"))
CONTR = RG.contrato(FJ, FORMAL_MAP, E409, sha256(raw), core0, selo0); TXT = RG.texto_iald2()
chk("contrato IALD2: escada, ancoras, chaves, alcance", CONTR["expected_ladder"] == E409 + FJ["n_flags"] and CONTR["n_ancoras"] == len(DL.ANCORAS) == DL.N_ANCORAS_ESPERADAS == 22 and CONTR["chaves"] == [] and CONTR["alcance"]["frase"] == DL.FRASE_D64_PT, [E409, E409 + FJ["n_flags"], FJ["n_flags"]])
chk("contrato IALD2 traz t_c16 (c16, D71)", "t_c16" in CONTR and "c16_fator_longo" in CONTR and "c16_tol" in CONTR and DL.N_CHECKS_FECHO == 16)
CONTR_H = RH.contrato_h0dn(core0, selo0); TXT_H = RH.texto_h0dn(); INS_H = RH.insumos_embutidos()
CONTR_F = RF.contrato_hms13(core0, selo0, CONTR_H); TXT_F = RF.texto_hms13(); INS_F = RF.insumos_embutidos_hms13()
CONTR_A = RA.contrato_aescala(FJ, FORMAL_MAP, E409, sha256(raw), core0, selo0); TXT_A = RA.texto_aescala()
chk("contrato AEscala (D86/D87; R1): as checagens, as ancoras, os nomes RATIFICADOS e os nomes novos da pedra, as falas, a ponte, a escada, o gate, as bandeiras das duas series somam o FLAGS (tudo lido do delta, do FLAGS e do contrato)", CONTR_A["n_checks"] == DL.N_CHECKS_AESCALA and CONTR_A["n_ancoras"] == DL.N_ANCORAS_AESCALA == len(DL.ANCORAS_AESCALA) and CONTR_A["n_nomes"] == len(DL.NOMES_AESCALA) and CONTR_A["nomes_ratificados"] is True and len(CONTR_A["falas"]) == CONTR_A["n_falas"] == len(RA.NOMES_FALAS) and CONTR_A["n_nomes_novos"] == len(DL.NOMES_NOVOS_AESCALA) and CONTR_A["nomes_novos_da_pedra"] == list(DL.NOMES_NOVOS_AESCALA) and CONTR_A["campos_novos_da_estrutura"] == list(DL.CAMPOS_NOVOS_AESCALA) and CONTR_A["ponte"] == DL.PONTE_AESCALA and CONTR_A["ratificacao_pendente"] == DL.RATIFICACAO_PENDENTE_AESCALA and CONTR_A["expected_ladder"] == CONTR["expected_ladder"] == E409 + FJ["n_flags"] and CONTR_A["baseline"]["gate_verdict"] == selo0.get("qg_closure_verdict") and CONTR_A["n_flags"] + CONTR["n_flags"] == FJ["n_flags"])
chk("P18 CRUA no texto da AEscala (sem as falas embutidas) e a guarda das frases (F58 do Clay)", not GP.violacoes(json.dumps({k_: TXT_A[k_] for k_ in ("estatuto", "escopo", "limites", "diz", "nao_diz")}, ensure_ascii=False)) and not GF.violacoes(json.dumps(TXT_A, ensure_ascii=False)), (GP.violacoes(json.dumps({k_: TXT_A[k_] for k_ in ("estatuto", "escopo", "limites", "diz", "nao_diz")}, ensure_ascii=False)) + GF.violacoes(json.dumps(TXT_A, ensure_ascii=False)))[:3])
chk("contrato HMS13 (D80): 12 checagens, gate, 4 insumos, 6 pinos do build relidos, guarda numerica, nada lido em rito, os dez campos", CONTR_F["n_checks"] == DL.N_CHECKS_HMS13 == 12 and CONTR_F["baseline"]["gate_verdict"] == selo0.get("qg_closure_verdict") and set(CONTR_F["insumos"]) == set(INS_F) and len(CONTR_F["pinos_build"]) == 6 and CONTR_F["guarda_numerica_no_build"]["ok"] is True and CONTR_F["le_em_rito"] is False and CONTR_F["campos"] == DL.HMS13_CAMPOS and "vibrato" not in json.dumps([CONTR_F, TXT_F], ensure_ascii=False).lower())
chk("P18 CRUA no texto do HMS/13", not GP.violacoes(json.dumps(TXT_F, ensure_ascii=False)), GP.violacoes(json.dumps(TXT_F, ensure_ascii=False))[:2])
chk("contrato H0DN: 12 checagens, gate, insumos, nenhum vetor observado", CONTR_H["n_checks"] == DL.N_CHECKS_H0DN == 12 and CONTR_H["baseline"]["gate_verdict"] == selo0.get("qg_closure_verdict") and set(CONTR_H["insumos"]) == set(INS_H) and all(INS_H[k_]["sha256"] == v_["sha256"] for k_, v_ in CONTR_H["insumos"].items()) and CONTR_H["observed_vector_read"] is False)
chk("D57b/D76: a cabeca do ramo da leitura em partes, sem a palavra inteira", all(("TGL_PRO" + "VED") not in p_ for p_ in CONTR_H["ramos"]["vereditos"]["leitura_partes"]) and "".join(CONTR_H["ramos"]["vereditos"]["leitura_partes"]) == DL.VEREDITOS_H0DN["leitura"])
fontes = {}
for f in RG.FONTES:
    b = open(f["arquivo"], "rb").read(); fontes[f["chave"]] = {"arquivo": f["arquivo"], "papel": f["papel"], "sha256": sha256(b), "bytes": len(b)}
chk("fontes: a pedra embutida == FORMAL_MAP; a fonte == o pino; o H0DN copiado", fontes[RG.CHAVE_PEDRA["IALD2"]]["sha256"] == FORMAL_MAP[DL.MODULO_IALD2] and fontes[RG.CHAVE_FONTE["IALD2"]]["sha256"][:16] == DL.TESTEMUNHA["sha16_da_ordem"] and all(ch_ in fontes for ch_, _, _, _ in RH.FONTES_H0DN), len(fontes))
d65 = [f_["arquivo"] for f_ in fontes.values() if any(x_.lower() in open(f_["arquivo"], "rb").read().decode("utf-8", errors="replace").lower() for x_ in DL.FORA_D65)]
chk("D65: nenhuma fonte pinada traz o que fica fora", not d65, d65)
verb = {}
for v in RG.VERBATINS:
    b = open(v["arquivo"], "rb").read(); t = b.decode("utf-8")
    assert all(tr in t for tr in v["trechos"]), v["chave"]
    verb[v["chave"]] = {"text": t, "sha256": sha256(b), "bytes": len(b), "trechos": list(v["trechos"]), "autor": v["autor"], "so_o_trecho": v.get("so_o_trecho")}
    if v.get("so_o_trecho"):
        assert sha256(open(v["fonte_original"], "rb").read()) == v["sha256_arquivo_inteiro"]
    else:
        assert sha256(open(v["fonte_original"], "rb").read()) == sha256(b)
chk("as %d falas embutidas (de %d so' o trecho; as da parte 2 e as de 10/11 entram inteiras), chaves == delta" % (DL.N_FALAS_V410, len(DL.VERBATIM_SO_O_TRECHO)), len(verb) == DL.N_FALAS_V410 == len(DL.VERBATIM_ORIGEM_V410) and set(CONTR_A["verbatins"]) <= set(verb) and sum(1 for v_ in verb.values() if v_["so_o_trecho"]) == len(DL.VERBATIM_SO_O_TRECHO) and set(RG.VERB_CHAVES) == set(verb) and set(CONTR["verbatins"]) <= set(verb))


def _p18_sem_falas(txt_):
    s_ = txt_
    for v_ in sorted([x_["text"] for x_ in verb.values()] + list(DL.FRASES_VERBATIM_V410), key=len, reverse=True):
        for ln_ in [l_.strip() for l_ in v_.splitlines() if len(l_.strip()) >= 12]:
            for forma_ in (ln_, json.dumps(ln_, ensure_ascii=False)[1:-1], repr(ln_)[1:-1]):
                s_ = s_.replace(forma_, " ")
    return GP.violacoes(s_)


chk("P18: a crua ve a 15a fala (R4); sem as falas, limpa (o controle da excecao)", bool(GP.violacoes(json.dumps(verb, ensure_ascii=False))) and not _p18_sem_falas(json.dumps(verb, ensure_ascii=False)))
specs = RG.especs(FORMAL_MAP, khj, FORMAL_MAP, FJ, core0["kernel_formalization"]["axiom_coverage_v392"], core0)
chk("specs: cunhagens_v410 e kh_n1_cobertura_v410", [s["nome"] for s in specs] == [DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO])
for s in specs:
    corpo = json.dumps({k: s.get(k) for k in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, ensure_ascii=False)
    chk("P18 CRUA no corpo do spec %s (como o motor v392 no rito)" % s["nome"], not GP.violacoes(corpo), GP.violacoes(corpo)[:2])
    chk("palavra recusada/tokens no veredito do spec %s" % s["nome"], not GUARDA.search(s["veredito_prefixo"] + "__" + s["veredito_sufixo"]) and not any(t_ in s["veredito_prefixo"] + s["veredito_sufixo"] for t_ in DL.TOKENS_PROIBIDOS_V410))
    chk("fontes e verbatins do spec %s existem" % s["nome"], all(ch in fontes for ch in s.get("fontes", [])) and all(ch in verb for ch in s.get("verbatins", [])))
chk("P18 no texto da IALD2 (sem falas) e no veredito", not _p18_sem_falas(json.dumps(TXT, ensure_ascii=False)) and not GUARDA.search(TXT["veredito_ok"]) and not any(t_ in TXT["veredito_ok"] for t_ in DL.TOKENS_PROIBIDOS_V410))
chk("P18 CRUA no texto da IALD2 (o c13 do rito a aplica crua)", not GP.violacoes(json.dumps(TXT, ensure_ascii=False)), GP.violacoes(json.dumps(TXT, ensure_ascii=False))[:2])
chk("P18 CRUA no texto do H0DN (o c12 do rito a aplica crua)", not GP.violacoes(json.dumps(TXT_H, ensure_ascii=False)), GP.violacoes(json.dumps(TXT_H, ensure_ascii=False))[:2])
chk("palavra recusada/tokens no H0DN", not GUARDA.search(json.dumps(TXT_H, ensure_ascii=False)) and not any(t_ in CONTR_H["veredito_ok"] for t_ in DL.TOKENS_PROIBIDOS_V410 + DL.TOKENS_PROIBIDOS_H0DN))
RUNTIME_SRC = open(os.path.join(HERE, "runtime_v410.py"), encoding="utf-8").read().rstrip("\n") + "\n\n\n" + open(os.path.join(HERE, "runtime_h0dn_v410.py"), encoding="utf-8").read().rstrip("\n") + "\n\n\n" + open(os.path.join(HERE, "runtime_hms13_v410.py"), encoding="utf-8").read().rstrip("\n") + "\n\n\n" + open(os.path.join(HERE, "runtime_aescala_v410.py"), encoding="utf-8").read()
ast.parse(RUNTIME_SRC)
chk("runtime emendado: sem CR, sem palavra recusada, sem literal de beta", "\r" not in RUNTIME_SRC and not GUARDA.search(RUNTIME_SRC) and not AC.literais_de_beta(RUNTIME_SRC))
_nomes_base = AC.nomes_de_nivel_de_modulo(T0); _nomes_rt = AC.nomes_de_nivel_de_modulo(RUNTIME_SRC)
chk("sem colisao de nomes com a base (C3)", not (_nomes_rt & set(_nomes_base)), sorted(_nomes_rt & set(_nomes_base))[:5])
NOVOS = ("_v410_sem_falas_do_operador", "_v410_guarda_frases", "_v410_rotacao", "v410_iald2_mechanics", "_v410_formal", "_V410_RECUSA", "iald2_v410", "_v410_h0dn_decode", "_v410_h0dn_cabeca", "veredito_h0dn", "_v410_h0dn_mechanics", "_V410_H0DN_RECUSA", "h0dn_bg1_v410", "_v410_hms13_numeros", "_v410_hms13_mechanics", "_V410_HMS13_RECUSA", "h0dn_fontes_hms13_v410", "_v410_aescala_bell", "_v410_aescala_ciclo", "_v410_aescala_mechanics", "_V410_AESCALA_RECUSA", "a_escala_v410")   # (D80; os _V410_HMS13_* nascem no RCODE do gerador, como os _V410_H0DN_*)
chk("os nomes novos do runtime existem uma vez", all(sum(1 for n_ in _nomes_rt if n_ == x_) == 1 for x_ in NOVOS))
_corpo_guarda = RUNTIME_SRC[RUNTIME_SRC.index("def _v410_sem_falas_do_operador(txt_):"):RUNTIME_SRC.index("def _v410_rotacao(")]
_txt_ger = RUNTIME_SRC.replace(_corpo_guarda, "") + json.dumps([CONTR, TXT, specs, CONTR_H, TXT_H, CONTR_F, TXT_F, CONTR_A, TXT_A, {k_: v_["papel"] for k_, v_ in fontes.items()}], ensure_ascii=False)
V_GF = GF.violacoes(_txt_ger)
chk("guarda das frases (v405 -> v410) no texto novo da gerencia", not V_GF, V_GF[:4])
G0 = GF.controle_negativo(); chk("controle negativo da guarda das frases", G0["ok"])
chk("P18 no bloco de runtime + specs (sem as falas embutidas)", not _p18_sem_falas(RUNTIME_SRC + json.dumps(specs, ensure_ascii=False) + json.dumps(verb, ensure_ascii=False)), _p18_sem_falas(RUNTIME_SRC + json.dumps(specs, ensure_ascii=False))[:2])


def _controles(obj, onde):
    ruins = []
    if isinstance(obj, str):
        ruins = sorted({hex(ord(c)) for c in obj if ord(c) < 32 and c not in "\n\r"})
    elif isinstance(obj, dict):
        for k, v in obj.items():
            ruins += _controles(k, onde) + _controles(v, onde)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            ruins += _controles(v, onde)
    return ruins


chk("sem caractere de controle nos objetos novos", not _controles([CONTR, TXT, specs, fontes, CONTR_H, TXT_H, CONTR_F, TXT_F, CONTR_A, TXT_A, RUNTIME_SRC], "x"))
for nome in ("artigo_pt_v410.pysnip", "artigo_en_v410.pysnip", "artigo_pt_aescala_v410.pysnip", "artigo_en_aescala_v410.pysnip", "artigo_pt_h0dn_v410.pysnip", "artigo_en_h0dn_v410.pysnip"):
    sn = open(os.path.join(HERE, nome), encoding="utf-8").read()
    try:
        ast.parse("def _f(core, verdict, data_path, s):\n" + sn); ok_ast = True
    except SyntaxError as e:
        ok_ast = False
    chk("snippet %s: ast, palavra recusada, P18, frases, beta em LaTeX, controle" % nome, ok_ast and not GUARDA.search(sn) and not GP.violacoes(sn) and not GF.violacoes(sn) and "β" not in sn and not _controles(sn, nome), (GP.violacoes(sn) + GF.violacoes(sn))[:2])
src_h = open(os.path.join(HERE, "runtime_h0dn_v410.py"), encoding="utf-8").read()
chk("o runtime do H0DN nao escreve a palavra do livro de cobrancas em cabeca nem o token inteiro da prova", "NOT_FALSIFIED_P" not in src_h and ("TGL_PRO" + "VED") not in src_h)
R["ok"] = all(c["ok"] for c in R["checks"].values()); R["duracao_s"] = round(time.time() - t0, 1)
R["sha16"] = {n_: sha16(open(os.path.join(HERE, n_), "rb").read()) for n_ in ("delta_v410.py", "registros_v410.py", "registros_h0dn_v410.py", "runtime_v410.py", "runtime_h0dn_v410.py", "registros_hms13_v410.py", "runtime_hms13_v410.py", "registros_aescala_v410.py", "runtime_aescala_v410.py", "guarda_frases_v410.py", "gerar_candidato_v410.py", "artigo_pt_v410.pysnip", "artigo_en_v410.pysnip", "artigo_pt_h0dn_v410.pysnip", "artigo_en_h0dn_v410.pysnip")}
json.dump(R, open(os.path.join(HERE, "PREVOO_GERADOR_v410.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nPRE-VOO:", "VERDE" if R["ok"] else "FALHOU", "| checks", sum(1 for c in R["checks"].values() if c["ok"]), "/", len(R["checks"]), "| %.1f s" % R["duracao_s"])
