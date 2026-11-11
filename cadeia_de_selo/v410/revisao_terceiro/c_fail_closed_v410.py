# -*- coding: utf-8 -*-
"""Revisor terceiro v410 (R1): importa o CANDIDATO (sem executar o main) e testa, sobre o core do ensaio a seco (dry_v410/core_ensaio.json), que os QUATRO registros novos sao fail-closed
(nega UMA condicao por vez e confere que o registro RECUSA): iald2_v410 (22 ancoras), a_escala_v410 (38 ancoras), h0dn_bg1_v410, h0dn_fontes_hms13_v410; a funcao veredito_h0dn com vetores MEUS;
a guarda das frases (F44-F58) com sondas MINHAS. Mutacao EM LUGAR com restauracao (sem deepcopy do core de 12 MB). Estado em ESTADO_REVISAO_v410.json a cada bloco. So escreve nesta pasta."""
import copy, hashlib, importlib.util, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
OUT = R + "revisao_terceiro/c_fail_closed_v410_out.json"
t0 = time.time()
spec = importlib.util.spec_from_file_location("um_cand_rev", R + "um_v410_candidato.py")
m = importlib.util.module_from_spec(spec)
sys.modules["um_cand_rev"] = m
spec.loader.exec_module(m)
print("import ok", round(time.time() - t0, 1), "s;  UM_VERSION", m.UM_VERSION, flush=True)
core = json.load(open(R + "dry_v410/core_ensaio.json", encoding="utf-8"))["core"]
kf = core["kernel_formalization"]
res = {}


def salvar():
    json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def roda(F, chave):
    core.pop(chave, None)
    try:
        r = F(core)
    except Exception as e:   # noqa: BLE001
        return {"excecao": repr(e)[:200], "all_verified": False, "verdict": "EXCECAO"}
    finally:
        core.pop(chave, None)
    return r


def muta(F, chave, cam, valor, pop=False):
    """cam: lista de chaves ate o dict pai + chave final; muta em lugar e restaura."""
    pai = core
    for k in cam[:-1]: pai = pai[k]
    ult = cam[-1]; existia = ult in pai; antigo = pai.get(ult)
    try:
        if pop: pai.pop(ult, None)
        else: pai[ult] = valor
        return roda(F, chave)
    finally:
        if existia: pai[ult] = antigo
        else: pai.pop(ult, None)


def bloco(nome, F, chave, C):
    t = time.time()
    base = roda(F, chave)
    print("== %s base: all_verified=%s verdict=%s" % (nome, base.get("all_verified"), str(base.get("verdict"))[:110]), flush=True)
    res[nome] = {"base_all_verified": base.get("all_verified"), "base_verdict": str(base.get("verdict"))[:200]}
    checks = (base.get("mechanics") or {}).get("checks") or []
    print("   checks:", [(c_["id"], c_["ok"]) for c_ in checks], flush=True)
    res[nome]["base_checks"] = [(c_["id"], c_["ok"]) for c_ in checks]
    anc = list(C["ancoras"]); fl = list(C["flags"])
    ar = ["kernel_formalization", "axiom_report"]; ds = ["kernel_formalization", "declaration_sources_v394"]
    n_aus = n_sorry = n_red = n_vaz = n_prov = 0
    for a in anc:
        n_aus += (muta(F, chave, ar + [a], None, pop=True)["all_verified"] is False)
        n_sorry += (muta(F, chave, ar + [a], ["propext", "sorryAx"])["all_verified"] is False)
        n_red += (muta(F, chave, ar + [a], ["Lean.ofReduceBool"])["all_verified"] is False)
        n_vaz += (muta(F, chave, ar + [a], [])["all_verified"] is False)
        n_prov += (muta(F, chave, ds + [a], "x.lean")["all_verified"] is False)
    print("   %d ancoras: ausente %d | sorryAx %d | ofReduceBool %d | vazia %d | proveniencia errada %d" % (len(anc), n_aus, n_sorry, n_red, n_vaz, n_prov), flush=True)
    res[nome]["ancoras"] = {"n": len(anc), "ausente": n_aus, "sorry": n_sorry, "reduceBool": n_red, "vazia": n_vaz, "proveniencia": n_prov, "ok": all(x == len(anc) for x in (n_aus, n_sorry, n_red, n_vaz, n_prov))}
    n_f = n_fa = 0
    for f_ in fl:
        n_f += (muta(F, chave, ["kernel_formalization", f_], False)["all_verified"] is False)
        n_fa += (muta(F, chave, ["kernel_formalization", f_], None, pop=True)["all_verified"] is False)
    print("   %d bandeiras: False %d | ausente %d" % (len(fl), n_f, n_fa), flush=True)
    res[nome]["bandeiras"] = {"n": len(fl), "false": n_f, "ausente": n_fa, "ok": n_f == len(fl) and n_fa == len(fl)}
    sh = ["kernel_formalization", "formal_files_sha256"]
    nb = 0
    for rel in C["source_sha256"]:
        nb += (muta(F, chave, sh + [rel], "1" * 64)["all_verified"] is False)
        nb += (muta(F, chave, sh + [rel], None, pop=True)["all_verified"] is False)
        orig = m._EMBEDDED_KERNEL_FILES[rel]
        m._EMBEDDED_KERNEL_FILES[rel] = orig + "\n-- adulterado"; nb += (roda(F, chave)["all_verified"] is False)
        del m._EMBEDDED_KERNEL_FILES[rel]; nb += (roda(F, chave)["all_verified"] is False)
        m._EMBEDDED_KERNEL_FILES[rel] = orig
    print("   fontes (sha core errado/ausente, embutida adulterada/ausente) recusadas: %d de %d" % (nb, 4 * len(C["source_sha256"])), flush=True)
    res[nome]["fontes"] = {"n_recusas": nb, "esperado": 4 * len(C["source_sha256"]), "ok": nb == 4 * len(C["source_sha256"])}
    raiz = m._EMBEDDED_KERNEL_FILES["TGLExt.lean"]
    mod = "AEscala" if "AEscala" in nome or "escala" in nome else "IALD2"
    m._EMBEDDED_KERNEL_FILES["TGLExt.lean"] = raiz.replace("import TGLExt.%s\n" % mod, "")
    r_ = roda(F, chave); m._EMBEDDED_KERNEL_FILES["TGLExt.lean"] = raiz
    res[nome]["raiz_sem_import_" + mod] = r_["all_verified"] is False
    print("   raiz sem o import %s: recusado %s" % (mod, r_["all_verified"] is False), flush=True)
    por = {}
    por["escada 12270"] = muta(F, chave, ["external_ladder", "n_theorems_clean"], 12270)["all_verified"] is False
    por["escada esperada 12187"] = muta(F, chave, ["external_ladder", "n_theorems_expected"], 12187)["all_verified"] is False
    por["gate outro"] = muta(F, chave, ["qg_closure", "gate", "verdict"], "OUTRO")["all_verified"] is False
    por["qg_closure ausente"] = muta(F, chave, ["qg_closure"], None, pop=True)["all_verified"] is False
    por["kernel all_verified False"] = muta(F, chave, ["kernel_formalization", "all_verified"], False)["all_verified"] is False
    por["kernel all_verified string"] = muta(F, chave, ["kernel_formalization", "all_verified"], "True")["all_verified"] is False
    por["beta divergente"] = muta(F, chave, ["beta"], core["beta"] * 1.001)["all_verified"] is False
    por["beta ausente"] = muta(F, chave, ["beta"], None, pop=True)["all_verified"] is False
    por["core vazio"] = F({})["all_verified"] is False
    for k, v in por.items(): print("   %-28s recusado: %s" % (k, v), flush=True)
    res[nome]["porta_a_porta"] = por
    # falas adulteradas / trecho inexistente
    ver = m._V410_VERBATINS2; nfa = nft = 0
    for k in C["verbatins"]:
        if k not in ver: continue
        sv = ver[k]["text"]; ver[k]["text"] = sv + " "; nfa += (roda(F, chave)["all_verified"] is False); ver[k]["text"] = sv
        tr = ver[k].get("trechos")
        if tr is not None:
            ver[k]["trechos"] = list(tr) + ["trecho que nao esta na fala"]; nft += (roda(F, chave)["all_verified"] is False); ver[k]["trechos"] = tr
    print("   falas (%d): adulterada recusada %d | trecho inexistente recusado %d" % (len(C["verbatins"]), nfa, nft), flush=True)
    res[nome]["falas"] = {"n": len(C["verbatins"]), "adulteradas_recusadas": nfa, "trecho_inexistente_recusado": nft}
    res[nome]["tempo_s"] = round(time.time() - t, 1)
    salvar()


bloco("iald2_v410", m.iald2_v410, "iald2_v410", m._V410_IALD2_CONTRACT)
bloco("a_escala_v410", m.a_escala_v410, "a_escala_v410", m._V410_AESCALA_CONTRACT)

# ---------- R2: mutacoes do contrato da AEscala (ponte, ciclo, teoremas_r4, ancoras_novas) -> o registro RECUSA
print("== a_escala: mutacoes do contrato (R3/R4)", flush=True)
sv_c = m._V410_AESCALA_CONTRACT
def mut_c(nome_, fn):
    c2 = copy.deepcopy(sv_c); fn(c2); m._V410_AESCALA_CONTRACT = c2
    try: r_ = roda(m.a_escala_v410, "a_escala_v410")
    finally: m._V410_AESCALA_CONTRACT = sv_c
    ok_ = r_.get("all_verified") is False
    print("   %-60s recusado: %s" % (nome_, ok_), flush=True); res["a_escala_contrato: " + nome_] = ok_
mut_c("ciclo: custo sem solucao com um zero", lambda c_: c_["ciclo"]["custo_sem_solucao"].__setitem__(0, 0))
mut_c("ciclo: epsilon negativo", lambda c_: c_["ciclo"].__setitem__("epsilon", "-1/1000"))
mut_c("ciclo: n_solucoes_com errado", lambda c_: c_["ciclo"].__setitem__("n_solucoes_com", 3))
mut_c("ponte: 1/2 trocado por 1/3", lambda c_: c_["ponte"].__setitem__("brilho_de_um_pixel_em_uma_oitava", "1/3"))
mut_c("ponte: um caso errado", lambda c_: c_["ponte"]["casos"][1].__setitem__(2, "1/9"))
mut_c("teoremas_r4: um nome fora das ancoras novas", lambda c_: c_["teoremas_r4"].__setitem__(0, "nao_existe_esta_ancora"))
mut_c("ancoras_novas: uma ancora tirada do contrato", lambda c_: c_["ancoras_novas"].pop(0))
mut_c("n_ancoras 55", lambda c_: c_.__setitem__("n_ancoras", 55))
# R3: a c13 (clausula do Tetelestai em 1 - beta) NAO pode ser vacua: cada controle negativo tem de reprovar de verdade
mut_c("c13: controle negativo com 0 oitavas a menos (a violacao nao acontece)", lambda c_: c_["tetelestai"].__setitem__("oitavas_a_menos_no_controle", 0))
mut_c("c13: contraexemplo com b = 1/3 (o limiar nao e' negativo)", lambda c_: c_["tetelestai"]["contraexemplo_s_negativo"].__setitem__("b", "1/3"))
mut_c("c13: custo_uma_solucao com duas solucoes", lambda c_: c_["tetelestai"]["custo_uma_solucao"].__setitem__(1, 0))
mut_c("c13: custo_com_solucao sem solucao nenhuma", lambda c_: c_["tetelestai"].__setitem__("custo_com_solucao", [1, 2, 3, 1, 1, 4, 1, 2]))
mut_c("c13: adversario com 2 solucoes", lambda c_: c_["tetelestai"]["custo_adversario"].__setitem__(1, 0))
mut_c("c13: m_da_constante vazio", lambda c_: c_["tetelestai"].__setitem__("m_da_constante", []))
mut_c("c13: n_bits do tetelestai 4 com 8 custos", lambda c_: c_["tetelestai"].__setitem__("n_bits", 4))
mut_c("c13: frase_tetelestai_pt apagada", lambda c_: c_.__setitem__("frase_tetelestai_pt", "xx"))
# beta de runtime: beta do core muda -> a constante/clausula tem de acompanhar ou o registro recusa (beta nunca literal)
for fator in (1.0005, 5.0, 40.0):
    b0 = core["beta"]; core["beta"] = b0 * fator
    r_ = roda(m.a_escala_v410, "a_escala_v410"); core["beta"] = b0
    print("   core[beta] x%s -> recusado: %s" % (fator, r_.get("all_verified") is False), flush=True); res["a_escala_beta_x%s" % fator] = r_.get("all_verified") is False

# o texto do registro com a negacao seca dos passos (F59a) ou o leitor que paga (F59b) recusa pela guarda do proprio registro
tx = m._V410_AESCALA_TEXT; sv_d = list(tx["diz"])
for fr in ("os passos não são passos da máquina de Turing", "o leitor paga a escala", "o decisor sem escala é o Pai da Mentira", "the reader pays the scale", "these are not steps of the Turing machine"):
    tx["diz"] = sv_d + [fr]; r_ = roda(m.a_escala_v410, "a_escala_v410"); ok_ = r_.get("all_verified") is False
    print("   texto do registro com %-52s recusado: %s" % (repr(fr), ok_), flush=True); res["a_escala_texto: " + fr] = ok_
for fr, nome_ in (("o limiar do Tetelestai: com n bits ha' solucao <=> Z(s) >= 1, a decisao em tempo finito do ciclo, linear nos bits", "anuncio do limiar PT sem a clausula"),
                  ("the Tetelestai threshold: a solution exists iff Z(s) >= 1, the decision in finite time of the cycle, linear in the bits", "anuncio do limiar EN sem a clausula"),
                  ("a clausula do Tetelestai (o_tetelestai_e_um_menos_beta): (1 - b)*Z(s) <= o numero de solucoes com s >= n ln 2 + ln((1 - b)/b)", "anuncio da clausula de 1 - beta sem a clausula do limite"),
                  ("E36: o limiar de um pixel fica como a decisao exata (o_tetelestai_e_um_menos_beta)", "E36 sem a clausula do limite")):
    tx["diz"] = sv_d + [fr]; r_ = roda(m.a_escala_v410, "a_escala_v410"); ok_ = r_.get("all_verified") is False
    print("   texto: %-62s recusado: %s" % (nome_, ok_), flush=True); res["a_escala_texto: " + nome_] = ok_
tx["diz"] = sv_d
print("   restaurado:", roda(m.a_escala_v410, "a_escala_v410").get("all_verified"), flush=True)
salvar()

# ---------- H0DN e HMS/13: adulterar um insumo embutido; caminhos tocados sob a pasta vedada; texto com frase proibida
print("== h0dn_bg1_v410 / h0dn_fontes_hms13_v410", flush=True)
H = m.h0dn_bg1_v410; Hm = m.h0dn_fontes_hms13_v410
core.pop("h0dn_bg1_v410", None); core.pop("h0dn_fontes_hms13_v410", None)
b = H(core); print("   h0dn base:", b.get("all_verified"), str(b.get("verdict"))[:90], [(c["id"], c["ok"]) for c in b["mechanics"]["checks"]], flush=True)
bh = Hm(core); print("   hms13 base:", bh.get("all_verified"), str(bh.get("verdict"))[:90], [(c["id"], c["ok"]) for c in bh["mechanics"]["checks"]], flush=True)
res["h0dn_base"] = {"all_verified": b.get("all_verified"), "observed_vector_read": b.get("observed_vector_read"), "checks": [(c["id"], c["ok"]) for c in b["mechanics"]["checks"]], "values_observed_vector_read": (b.get("values") or {}).get("observed_vector_read"), "caminhos_tocados": (b.get("values") or {}).get("caminhos_tocados")}
res["hms13_base"] = {"all_verified": bh.get("all_verified"), "n_caminhos_tocados": (bh.get("values") or {}).get("n_caminhos_tocados"), "caminhos_tocados": (bh.get("values") or {}).get("caminhos_tocados")}
print("   h0dn caminhos tocados durante a mecanica:", (b.get("values") or {}).get("caminhos_tocados"), flush=True)
print("   hms13 caminhos tocados durante a mecanica:", (bh.get("values") or {}).get("caminhos_tocados"), flush=True)
# adulterar cada insumo embutido (troca de 1 caractere do base64)
import base64
for reg, F_, ins, chave in (("h0dn", H, m._V410_H0DN_INSUMOS, "h0dn_bg1_v410"), ("hms13", Hm, m._V410_HMS13_INSUMOS, "h0dn_fontes_hms13_v410")):
    n = 0
    for nome, ent in ins.items():
        sv = ent["b64"]; raw = bytearray(base64.b64decode(sv)); raw[len(raw) // 2] ^= 1
        ent["b64"] = base64.b64encode(bytes(raw)).decode("ascii"); r_ = roda(F_, chave); n += (r_["all_verified"] is False); ent["b64"] = sv
    print("   %s: insumo embutido adulterado (1 bit) recusado: %d de %d" % (reg, n, len(ins)), flush=True)
    res[reg + "_insumo_adulterado"] = {"recusados": n, "de": len(ins)}
# c7 do HMS/13: mecanica chamada com um caminho tocado sob a pasta vedada
c_h = m._V410_HMS13_CONTRACT; t_h = m._V410_HMS13_TEXT; i_h = m._V410_HMS13_INSUMOS
core["h0dn_bg1_v410"] = H(core) if "h0dn_bg1_v410" not in core else core["h0dn_bg1_v410"]
vedada = c_h["pasta_vedada"]
for caso, toc in (("caminho sob a pasta vedada", [vedada + "\\y_obs.npz"]), ("nome vedado fora da pasta", ["C:\\x\\y_obs.npz"]), ("nenhum", [])):
    mec = m._v410_hms13_mechanics(core, c_h, t_h, i_h, toc)
    c7 = [c for c in mec["checks"] if c["id"] == "c7"][0]["ok"]
    print("   hms13 c7 com %-30s -> c7=%s" % (caso, c7), flush=True)
    res["hms13_c7_" + caso] = c7
core.pop("h0dn_bg1_v410", None)
c_d = m._V410_H0DN_CONTRACT; t_d = m._V410_H0DN_TEXT; i_d = m._V410_H0DN_INSUMOS
for caso, toc in (("caminho sob a pasta vedada", [c_d["pasta_vedada"] + "\\y_obs.npz"]), ("nenhum", [])):
    try:
        mec = m._v410_h0dn_mechanics(core["beta"] if "beta" in core else None, core, c_d, t_d, i_d, toc)
        c7 = [c for c in mec["checks"] if c["id"] == "c7"][0]["ok"]
    except Exception as e:   # noqa: BLE001
        c7 = "EXC " + repr(e)[:120]
    print("   h0dn c7 com %-30s -> c7=%s" % (caso, c7), flush=True)
    res["h0dn_c7_" + caso] = c7
salvar()

# ---------- a funcao de veredito congelada: vetores MEUS
print("== veredito_h0dn (vetores do revisor)", flush=True)
ramos = c_d["ramos"]
V = m.veredito_h0dn
casos = [
    ("cov nao fechada, z gigante", dict(z_null=9.0, z_tgl=0.1, D_esperado=6.8, covariancia_fisica_fechada=False, no_suporte=True), 1),
    ("fora do suporte, z gigante", dict(z_null=9.0, z_tgl=0.1, D_esperado=6.8, covariancia_fisica_fechada=True, no_suporte=False), 1),
    ("falsificada |z_tgl|=5 exato", dict(z_null=9.0, z_tgl=-5.0, D_esperado=6.8, covariancia_fisica_fechada=True, no_suporte=True), 2),
    ("subpotente D=4.99", dict(z_null=9.0, z_tgl=0.1, D_esperado=4.99, covariancia_fisica_fechada=True, no_suporte=True), 3),
    ("D=5 exato nao e' subpotente", dict(z_null=5.0, z_tgl=0.0, D_esperado=5.0, covariancia_fisica_fechada=True, no_suporte=True), 4),
    ("leitura z_null=5 exato |z_tgl|=1.959963984540054", dict(z_null=5.0, z_tgl=1.959963984540054, D_esperado=6.8, covariancia_fisica_fechada=True, no_suporte=True), 4),
    ("z_null=4.999 -> nao discriminado", dict(z_null=4.999, z_tgl=0.0, D_esperado=6.8, covariancia_fisica_fechada=True, no_suporte=True), 6),
    ("tensao z_null=6 |z_tgl|=3", dict(z_null=6.0, z_tgl=3.0, D_esperado=6.8, covariancia_fisica_fechada=True, no_suporte=True), 5),
    ("falsificada tem precedencia sobre subpotente", dict(z_null=9.0, z_tgl=7.0, D_esperado=2.0, covariancia_fisica_fechada=True, no_suporte=True), 2),
    ("z_tgl nan", dict(z_null=9.0, z_tgl=float("nan"), D_esperado=6.8, covariancia_fisica_fechada=True, no_suporte=True), None),
    ("z_null negativo grande", dict(z_null=-9.0, z_tgl=0.0, D_esperado=6.8, covariancia_fisica_fechada=True, no_suporte=True), 6),
]
vv = []
for nm, kw, ramo_esp in casos:
    try:
        cab, outc, ramo = V(ramos=ramos, **kw)
    except Exception as e:   # noqa: BLE001
        cab, outc, ramo = "EXC " + repr(e)[:80], None, None
    ok = (ramo == ramo_esp)
    print("   %-52s ramo=%s outcome=%s %s | %s" % (nm, ramo, outc, "OK" if ok else "DIFERE do esperado %s" % ramo_esp, cab[:150]), flush=True)
    vv.append({"caso": nm, "ramo": ramo, "esperado": ramo_esp, "ok": ok, "outcome": outc, "cabeca": cab})
res["veredito_h0dn"] = vv
# a cabeca do ramo 4: 'provado na natureza' so' com a validade na MESMA string
cab4 = V(5.2, 0.3, 6.8, True, True, ramos)[0]
res["cabeca_ramo4"] = cab4
print("   cabeca do ramo 4:", cab4, flush=True)
print("   'validade, não creditação' na MESMA string:", "validade, não creditação" in cab4 or "validade, nao creditacao" in cab4, flush=True)
salvar()

# ---------- a guarda das frases: sondas MINHAS
print("== guarda das frases (sondas do revisor)", flush=True)
G = m._v410_guarda_frases
casos_g = [
    # devem REPROVAR
    ("os passos não são passos da máquina de Turing", True), ("these are not steps of the Turing machine", True), ("isto não são os passos de uma máquina de Turing", True), ("o leitor paga a escala", True), ("o leitor pagou o tempo", True), ("the reader pays the scale", True),
    ("o decisor sem escala é o Pai da Mentira", True), ("o decisor sem escala mente", True), ("o decisor sem escala é mentiroso", True), ("the decider without a scale lies", True),
    ("Não são os passos da máquina de Turing", True), ("o tempo não conta passos de Turing", None), ("quem paga a escala é o leitor", None), ("o leitor teve de pagar a escala", None), ("os passos não pertencem à máquina de Turing", None), ("the decider without a scale is a liar", True),
    ("o leitor não paga a escala, porque ele é a escala", False), ("o decisor sem escala não mente: não lê", False), ("que o decisor sem escala minta, ou seja o Pai da Mentira: ele não lê", False),
    ("o tempo conta os ciclos (os passos) da máquina de Turing tal como a TGL a traduz (dicionário da v409), até o Tetelestai; o que não está no kernel é um termo ligando essa tradução à formalização do Mathlib; a creditação é do Clay", False),
    ("the time counts the cycles (the steps) of the Turing machine as the TGL translates it (the v409 dictionary), up to the Tetelestai; what is not in the kernel is a term linking that translation to the Mathlib formalization; the creditation is Clay's", False),
    ("o problema de Clay está resolvido", True), ("O Clay foi resolvido.", True), ("Clay is solved", True), ("the Clay problem was resolved", True), ("a TGL resolveu o problema de Clay", True),
    ("A TGL resolveu P vs NP", True), ("P = NP está provado", True), ("a IALD decidiu P vs NP", True), ("P vs NP foi decidido pela IALD", True),
    ("a TGL prova P = NP de Turing", True), ("o algoritmo IALD satisfaz P = nP", True),
    ("5 sigma atingido", True), ("o teste H0DN deu 5 sigma", True), ("the H0DN test detected the signal", True), ("H0DN confirma a TGL", True),
    ("a covariância física está fechada", True), ("a abertura foi autorizada", True), ("o teste foi aberto", True),
    ("não falsificado a 5 sigma", True), ("a TGL não prova P = nP", True), ("a casa não afirma P = nP de Turing", True), ("a resposta de Clay é uma tautologia", True),
    ("a TGL resolve o problema do milênio", True), ("o atrator foi observado", True), ("o Nome esgota o ser", True),
    ("a TGL não resolve Clay", True), ("this does not solve the Clay problem", True),
    ("A TGL fechou a questão do Clay", True), ("a IALD respondeu ao problema do Clay e a prova está feita", True), ("Clay está provado", True),
    ("The TGL has proven P = NP", True), ("P=NP is proven by the IALD", True),
    # devem PASSAR (formas obrigatorias)
    ("O problema de Clay, tal qual apresentado pela TGL, foi resolvido no kernel Lean e a prova está apresentada. Creditar essa prova ao aceite do Instituto compete somente a quem tem autoridade para falar em nome do Clay. O operador testemunha que a IALD leu o P de Clay e o traduziu em operador com identidade nomeada, aquilo que se espera ser a solução do problema.", False),
    ("The Clay problem, as presented by the TGL, has been resolved in the Lean kernel and the proof is presented. Crediting this proof to the Institute’s acceptance belongs only to those with authority to speak for Clay.", False),
    ("a TGL resolve a pergunta do Clay no sentido do operador: existe o algoritmo, é a IALD; validade no kernel; a creditação é do Clay", False),
    ("P = nP de Turing (a máquina com o leitor; as classes de computação) PROVADO no kernel: validade, não creditação; a máquina de Turing padrão sem o leitor fica fora por estatuto", False),
    ("pré-registrado; nenhum dado observado lido", False), ("o teste H0DN × BG1 está pré-registrado; nenhum dado observado lido", False),
]
sg = []
for fr, deve in casos_g:
    g = G(fr); p18 = m._v392_guarda_texto(fr); rep = bool(g) or bool(p18)
    ok = (rep == deve) if deve is not None else True
    sg.append({"frase": fr[:120], "deve_reprovar": deve, "reprovou": rep, "regras": [x[0] for x in (g + p18)][:3], "ok": ok})
    print("   %s %-110s -> %s" % ("OK   " if ok else "FALHA", repr(fr[:108]), [x[0][:30] for x in (g + p18)][:2]), flush=True)
res["guarda_sondas"] = sg
res["_resumo"] = {"guarda_falhas": [s["frase"] for s in sg if not s["ok"]], "veredito_falhas": [v["caso"] for v in vv if not v["ok"]]}
salvar()
print("FIM", round(time.time() - t0, 1), "s", flush=True)
