# -*- coding: utf-8 -*-
# [AUTORAL v410, 09/11/2026, claude-construtor-v410, a servico da gerencia c1] o SEGUNDO registro com FUNCAO da v410 (D72 + E30 + D76 do DESENHO_v410): o teste PRE-REGISTRADO da razao de Hubble H0DN x BG1.
# ---- v410 (D72): H0DN x BG1 -- O TESTE PRE-REGISTRADO DA RAZAO DE HUBBLE LOCAL/FUNDO: pré-registrado; nenhum dado observado lido. O desenho e' o do Codex astra-bell de 06/11 (congelado ANTES de qualquer olhar no dado:
# FREEZE_R2.json, 9 pinos); a leitura da gerencia esta' em LEITURA_DOSSIE_5SIGMA_09nov.json. Nulo: H_local/H_fundo = 1. Alternativa TGL: K = E(z*)^(2 beta/3), beta = alfa CODATA 2018 x sqrt(e) em runtime (nunca literal);
# z* e K sao conferidos contra o que a Fase 9 V1 (hubble_ratio_v387, ja' no um.py) transcreveu por hash; Omega_m e Omega_r vem do BG1.json embutido (a lei congelada da S5). Estatistica Z = (h_hat - log10 H_bg)/sigma_nulo,
# unilateral, limiar 5; dois modelos (o publicado; o vies diferencial Cefeida livre), nenhum selecionado. Os insumos entram EMBUTIDOS (base64) e pinados por sha256 LIDO na preparacao; network.npz so' pinado pelo FREEZE_R2.
# A FUNCAO DE VEREDITO CONGELADA (veredito_h0dn; E30 + D76): a primeira que casa decide; a cabeca do ramo de 5 sigma e' a LEITURA do 5 sigma -- beta_TGL provado na natureza (validade, nao creditacao) a n sigma --,
# nunca a palavra do livro de cobrancas, que vai no campo `outcome`. NESTA VERSAO nenhum vetor observado e' lido nem procurado: o poder e' prospectivo e sintetico; a abertura e' de versao futura, com a covariancia fisica
# fechada (G3/G4). Validade no kernel nao e' creditacao; o gate nao se move; nenhuma chave antiga muda. Fonte autoral deste bloco: runtime_h0dn_v410.py (cadeia_de_selo/v410); o contrato (_V410_H0DN_CONTRACT), o texto
# (_V410_H0DN_TEXT) e os insumos (_V410_H0DN_INSUMOS) sao DERIVADOS dos arquivos pinados, nunca digitados.


def _v410_h0dn_decode(c_, insumos_):
    """v410 -- decodifica os insumos EMBUTIDOS (base64) e confere cada um contra o pino do contrato (sha256 e bytes LIDOS na preparacao): fail-closed (ValueError) se um so' divergir. Devolve {nome: bytes}."""
    import base64 as _b64, hashlib as _h410
    out_ = {}
    for nome_, pino_ in c_["insumos"].items():
        ent_ = insumos_.get(nome_)
        if not isinstance(ent_, dict) or not isinstance(ent_.get("b64"), str):
            raise ValueError("insumo embutido do H0DN ausente: " + nome_)
        b_ = _b64.b64decode(ent_["b64"].encode("ascii"), validate=True)
        if _h410.sha256(b_).hexdigest() != pino_["sha256"] or len(b_) != pino_["bytes"]:
            raise ValueError("insumo embutido do H0DN nao bate com o pino: " + nome_)
        out_[nome_] = b_
    return out_


def _v410_h0dn_cabeca(partes_):
    """v410 -- monta a cabeca de um ramo do veredito a partir das PARTES do contrato (a cabeca do ramo da leitura traz a palavra da prova com a validade na MESMA string, D57b/D76; o texto do um.py nunca a traz inteira)."""
    return "".join(partes_)


def veredito_h0dn(z_null, z_tgl, D_esperado, covariancia_fisica_fechada, no_suporte, ramos):
    """v410 -- A FUNCAO DE VEREDITO CONGELADA do teste H0DN x BG1 (D72 + E30 + D76): a PRIMEIRA que casa decide. Devolve (cabeca, outcome, ramo).
    (1) INCONCLUSIVE_SYSTEMATICS se a covariancia fisica nao estiver fechada (G3/G4) ou o vetor estiver fora do suporte; (2) a lei K falsificada a 5 sigma a esta sensibilidade se |z_tgl| >= 5;
    (3) subpotente se o D esperado do modelo < 5; (4) a LEITURA do 5 sigma -- beta_TGL provado na natureza (validade, nao creditacao) a n sigma, n = floor(z_null) -- se z_null >= 5 e |z_tgl| <= 1,959963984540054;
    (5) discrimina do LCDM a n sigma com K em tensao de 2 a 5 sigma se z_null >= 5 e 1,96 < |z_tgl| < 5; (6) nao discriminado a sensibilidade disponivel, com a faixa do desvio |z_tgl|, se z_null < 5.
    A palavra do livro de cobrancas (TheLedgerOfCharges, imposta pelo tipo) vai em `outcome`, nunca na cabeca. O sha256 do texto-fonte desta funcao vai ao registro. Nenhum dado observado e' lido nesta versao."""
    import math as _m410
    L_ = float(ramos["limiar"]); C_ = float(ramos["compat_95"]); V_ = ramos["vereditos"]; suf_ = V_["sufixo"]
    zn_ = float(z_null); az_ = abs(float(z_tgl)); D_ = float(D_esperado)
    if not covariancia_fisica_fechada or not no_suporte:
        return V_["inconclusivo"] + suf_, "INCONCLUSIVE", 1
    if az_ >= L_:
        return V_["lei_falsificada"] + suf_, "FALSIFIED", 2
    if D_ < L_:
        return (V_["subpotente"] % ("%.2f" % D_).replace(".", "_")) + suf_, "INCONCLUSIVE", 3
    if zn_ >= L_ and az_ <= C_:
        return _v410_h0dn_cabeca(V_["leitura_partes"]) % int(_m410.floor(zn_)), "NOT_FALSIFIED", 4
    if zn_ >= L_:
        return (V_["tensao"] % int(_m410.floor(zn_))) + suf_, "NOT_FALSIFIED", 5
    faixa_ = V_["faixas"][0] if az_ <= 1.0 else (V_["faixas"][1] if az_ <= 3.0 else V_["faixas"][2])
    return (V_["nao_discriminado"] % faixa_) + suf_, "NOT_FALSIFIED", 6


def _v410_h0dn_vigia_arquivos():
    """v410 -- (AVISO da gerencia, 09/11) instrumenta open/os.path.exists/os.listdir/os.scandir/os.stat para REGISTRAR todo caminho tocado enquanto o registro H0DN corre: a prova de que nenhum vetor observado e' lido e' MEDIDA, nao frase.
    Devolve (lista dos caminhos, funcao que restaura). Fail-closed: a c7 recusa se um caminho cair sob a pasta vedada ou levar um nome vedado."""
    import builtins as _bi, os as _os410
    tocados_ = []
    def _reg(p_):
        try:
            if isinstance(p_, (str, bytes, _os410.PathLike)):
                tocados_.append(_os410.fspath(p_) if not isinstance(p_, bytes) else p_.decode("utf-8", "replace"))
        except Exception:   # noqa: BLE001
            tocados_.append(repr(p_))
    o_open, o_exists, o_listdir, o_scandir, o_stat = _bi.open, _os410.path.exists, _os410.listdir, _os410.scandir, _os410.stat
    def w_open(f_, *a_, **k_):
        _reg(f_); return o_open(f_, *a_, **k_)
    def w_exists(p_):
        _reg(p_); return o_exists(p_)
    def w_listdir(p_="."):
        _reg(p_); return o_listdir(p_)
    def w_scandir(p_="."):
        _reg(p_); return o_scandir(p_)
    def w_stat(p_, *a_, **k_):
        _reg(p_); return o_stat(p_, *a_, **k_)
    _bi.open = w_open; _os410.path.exists = w_exists; _os410.listdir = w_listdir; _os410.scandir = w_scandir; _os410.stat = w_stat
    def restaura_():
        _bi.open = o_open; _os410.path.exists = o_exists; _os410.listdir = o_listdir; _os410.scandir = o_scandir; _os410.stat = o_stat
    return tocados_, restaura_


def _v410_h0dn_mechanics(beta_, core_, c_, t_, insumos_, tocados_=None):
    """v410 -- as 12 checagens do registro pre-registrado H0DN x BG1 (D72; os numeros esperados vem dos insumos embutidos e do core deste rito; beta em runtime; nada digitado):
    c1 os pinos do FREEZE_R2 (os embutidos por sha256; os so' em disco, se presentes); c2 K e log10 K recomputados de beta com Omega_m/Omega_r do BG1 e z* conferido contra a Fase 9 V1 do proprio um.py (|Delta| < 1e-12);
    c3 sd_null e sd_tgl dos dois modelos reproduzidos de weights, C_joint, gradient_h/k do npz (|Delta| rel < 1e-9); c4 D esperado = log10 K/sd_null contra a ENTREGA (|Delta| < 1e-9); c5 o poder analitico Phi(D - 5) e a cauda nula
    Phi(-5) (|Delta| < 1e-12) e o poder MC da ENTREGA dentro do IC95 dela (conferencia, nao recalculo); c6 a funcao de veredito congelada em vetores DETERMINISTICOS (os 6 ramos), o sha256 do texto-fonte, as cabecas sem a palavra do
    livro de cobrancas; c7 observed_vector_read = False e nenhum vetor observado embutido nem procurado; c8 a guarda: tokens proibidos e a aritmetica do agregado publico fora do texto; c9 o gate identico ao da v409; c10 a rota Kimi
    espectro x fotometria como NOT_TESTABLE (nao e' o teste); c11 a regra conjunta CONGELADA na funcao; c12 o texto do registro passa P18 e a guarda das frases."""
    import hashlib as _h410, inspect as _insp, io as _io, json as _j410, math as _m410, os as _os410
    import numpy as _np410
    Phi_ = lambda x_: 0.5 * _m410.erfc(-float(x_) / _m410.sqrt(2.0))
    tol_ = c_["tolerancias"]
    toks_ = ["".join(p_) for p_ in c_["tokens_proibidos_partes"]]; agreg_ = ["".join(p_) for p_ in c_["agregado_publico_nao_entra_partes"]]   # (montados aqui: o contrato os traz em partes)
    raw_ = _v410_h0dn_decode(c_, insumos_)
    freeze_ = _j410.loads(raw_["FREEZE_R2.json"].decode("utf-8")); bg1_ = _j410.loads(raw_["BG1.json"].decode("utf-8")); entrega_ = _j410.loads(raw_["ENTREGA_H0DN_BG1.json"].decode("utf-8"))
    plano_ = _j410.loads(raw_["analysis_plan.json"].decode("utf-8"))
    npz_ = _np410.load(_io.BytesIO(raw_["estimator_frozen.npz"]), allow_pickle=False)
    # ---- c1 os pinos do FREEZE_R2: os embutidos (sha256 dos bytes decodificados) e os so' em disco (se presentes); o FREEZE_R2 e a ENTREGA pinados pelo contrato
    fz_ = {_os410.path.basename(f_["path"]) if not f_["path"].replace("\\", "/").endswith(("network/network.npz", "network/MANIFEST.json", "background/BG1.json", "background/build_bg1.py")) else "/".join(f_["path"].replace("\\", "/").split("/")[-2:]): f_ for f_ in freeze_["files"]}
    pinos_ = {}
    for nome_, pino_ in c_["insumos"].items():
        rel_ = pino_["rel"]; sha_emb_ = _h410.sha256(raw_[nome_]).hexdigest()
        if rel_ in fz_:
            pinos_[rel_] = {"embutido": True, "sha256_ok": sha_emb_ == fz_[rel_]["sha256"] == pino_["sha256"], "bytes_ok": len(raw_[nome_]) == fz_[rel_]["bytes"] == pino_["bytes"]}
        else:
            pinos_[rel_] = {"embutido": True, "sha256_ok": sha_emb_ == pino_["sha256"], "bytes_ok": len(raw_[nome_]) == pino_["bytes"], "fora_do_freeze": True}
    for rel_ in c_["pinos_freeze_r2_so_no_disco"]:
        f_ = fz_.get(rel_); p_ = f_["path"] if f_ else None
        if f_ and p_ and _os410.path.exists(p_):
            b_ = open(p_, "rb").read()
            pinos_[rel_] = {"embutido": False, "no_disco": True, "sha256_ok": _h410.sha256(b_).hexdigest() == f_["sha256"], "bytes_ok": len(b_) == f_["bytes"]}
        else:
            pinos_[rel_] = {"embutido": False, "no_disco": False, "sha256_ok": bool(f_), "bytes_ok": bool(f_)}
    c1_ok_ = len(freeze_["files"]) == c_["n_pinos_freeze"] and len(pinos_) == c_["n_pinos_freeze"] + 2 and all(v_["sha256_ok"] and v_["bytes_ok"] for v_ in pinos_.values()) and len(raw_) == len(c_["insumos"])
    # ---- c2 K e log10 K recomputados de beta (runtime); z* e K conferidos contra a Fase 9 V1 transcrita no proprio um.py (hubble_ratio_v387, lida por hash)
    lei_ = bg1_["law"]; Om_ = float(lei_["frozen_Omega_m"]); Or_ = float(lei_["frozen_Omega_r"]); zs_ = float(lei_["z_star"])
    E_ = _m410.sqrt(1.0 + Om_ * ((1.0 + zs_) ** 3 - 1.0) + Or_ * ((1.0 + zs_) ** 4 - 1.0))
    K_ = E_ ** (2.0 * beta_ / 3.0); logK_ = _m410.log10(K_)
    v387_ = core_.get("hubble_ratio_v387") or {}; tr_ = v387_.get("transcribed") or {}
    zs_um_ = tr_.get("z_star"); K_um_ = tr_.get("K_no_fundo_nu")
    c2_ok_ = (abs(K_ - float(bg1_["K"])) < tol_["K"] and abs(logK_ - float(bg1_["logK"])) < tol_["K"] and abs(logK_ - float(npz_["logK"])) < tol_["K"]
              and isinstance(zs_um_, (int, float)) and float(zs_um_) == zs_ and isinstance(K_um_, (int, float)) and abs(K_ - float(K_um_)) < tol_["K"] and v387_.get("all_verified") is True
              and lei_["form"] == c_["lei"]["form"] and 0.0 < beta_ < 1.0)
    # ---- c3 sd_null e sd_tgl reproduzidos de weights, C_joint, gradient_h/k (a independencia condicional local/fundo: o bloco cruzado do C_joint e' zero)
    W_ = _np410.asarray(npz_["weights"], float); Cj_ = _np410.asarray(npz_["C_joint"], float); gh_ = _np410.asarray(npz_["gradient_h"], float); gk_ = _np410.asarray(npz_["gradient_k"], float)
    n_ = W_.shape[1]; Cl_ = Cj_[:n_, :n_]; Cb_ = Cj_[n_:, n_:]; cruz_ = float(_np410.max(_np410.abs(Cj_[:n_, n_:]))) if Cj_.shape[0] > n_ else None
    modelos_ = [str(x_) for x_ in npz_["model_names"]]
    sd_ = []
    for m_ in range(W_.shape[0]):
        w_ = W_[m_]; vh_ = float(w_ @ Cl_ @ w_); vb_ = float(gh_ @ Cb_ @ gh_); vbk_ = float((gh_ + gk_) @ Cb_ @ (gh_ + gk_))
        sdn_ = _m410.sqrt(vh_ + vb_); sdt_ = _m410.sqrt(vh_ + vbk_)
        sd_.append({"modelo": modelos_[m_], "sd_null": sdn_, "sd_null_npz": float(npz_["sd_null"][m_]), "sd_tgl": sdt_, "sd_tgl_npz": float(npz_["sd_tgl"][m_]), "var_h_local": vh_, "var_bg_h": vb_, "var_bg_h_mais_k": vbk_})
    c3_ok_ = (modelos_ == list(c_["modelos"]) and len(sd_) == 2 and cruz_ is not None and cruz_ == 0.0 and Cj_.shape == (n_ + len(gh_), n_ + len(gh_))
              and all(abs(x_["sd_null"] - x_["sd_null_npz"]) <= tol_["sd_rel"] * x_["sd_null_npz"] and abs(x_["sd_tgl"] - x_["sd_tgl_npz"]) <= tol_["sd_rel"] * x_["sd_tgl_npz"] for x_ in sd_))
    # ---- c4 D esperado = log10 K / sd_null, contra a ENTREGA; c5 o poder analitico, a cauda nula e o poder MC da ENTREGA dentro do IC95 dela
    ent_mod_ = {m_["name"]: m_ for m_ in entrega_["models"]}
    D_ = []; c4_ok_ = len(ent_mod_) == 2; c5_ok_ = abs(Phi_(-c_["ramos"]["limiar"]) - float(freeze_["null_alpha"])) < tol_["poder"]
    for x_ in sd_:
        em_ = ent_mod_.get(x_["modelo"]) or {}
        d_ = logK_ / x_["sd_null"]; pw_ = Phi_(d_ - c_["ramos"]["limiar"])
        mc_ = em_.get("power_MC_frozen_threshold") or {}; ic_ = mc_.get("ci95") or [None, None]
        D_.append({"modelo": x_["modelo"], "D": d_, "D_entrega": em_.get("D_expected"), "poder_analitico": pw_, "poder_analitico_entrega": em_.get("power_analytic_gaussian"), "poder_mc_entrega": mc_.get("estimate"), "ic95_mc_entrega": ic_})
        c4_ok_ = c4_ok_ and isinstance(em_.get("D_expected"), float) and abs(d_ - em_["D_expected"]) < tol_["D"]
        c5_ok_ = c5_ok_ and isinstance(em_.get("power_analytic_gaussian"), float) and abs(pw_ - em_["power_analytic_gaussian"]) < tol_["poder"] and isinstance(mc_.get("estimate"), float) and isinstance(ic_[0], float) and isinstance(ic_[1], float) and ic_[0] <= mc_["estimate"] <= ic_[1] and abs(mc_["estimate"] - pw_) <= (ic_[1] - ic_[0])
    D_por_ = {x_["modelo"]: x_["D"] for x_ in D_}
    # ---- c6 a funcao de veredito CONGELADA: os vetores deterministicos do contrato (os 6 ramos), o sha256 do texto-fonte, as cabecas
    fonte_ = _insp.getsource(veredito_h0dn); fonte_sha_ = _h410.sha256(fonte_.encode("utf-8")).hexdigest()
    ramos_ = c_["ramos"]; vet_ = []; ramos_vistos_ = set()
    for v_ in c_["vetores_c6"]:
        Dv_ = D_por_[v_["D_de"]] if isinstance(v_.get("D_de"), str) else float(v_["D"])
        zn_ = D_por_[v_["z_null_de"]] * float(v_.get("z_null_fator", 1.0)) + float(v_.get("z_null_mais", 0.0)) if isinstance(v_.get("z_null_de"), str) else float(v_["z_null"])
        zt_ = D_por_[v_["z_tgl_de"]] * float(v_.get("z_tgl_fator", 1.0)) + float(v_.get("z_tgl_mais", 0.0)) if isinstance(v_.get("z_tgl_de"), str) else float(v_["z_tgl"])
        cab_, outc_, ramo_ = veredito_h0dn(zn_, zt_, Dv_, bool(v_["fechada"]), bool(v_["suporte"]), ramos_)
        ok_v_ = (ramo_ == int(v_["ramo"]) and outc_ == v_["outcome"] and cab_.endswith("__GATE_UNMOVED") and "NOT_FALSIFIED" not in cab_ and not any(tk_ in cab_ for tk_ in toks_)
                 and (("PRO" + "VED_IS_VALIDITY_NOT_CREDITATION") in cab_ if ramo_ == 4 else True))
        ramos_vistos_.add(ramo_); vet_.append({"nome": v_["nome"], "z_null": zn_, "z_tgl": zt_, "D": Dv_, "fechada": bool(v_["fechada"]), "suporte": bool(v_["suporte"]), "cabeca": cab_, "outcome": outc_, "ramo": ramo_, "ramo_esperado": int(v_["ramo"]), "ok": bool(ok_v_)})
    c6_ok_ = bool(vet_) and all(x_["ok"] for x_ in vet_) and ramos_vistos_ == {1, 2, 3, 4, 5, 6} and len(fonte_sha_) == 64 and ramos_["compat_95"] == c_["ramos"]["compat_95"]
    # ---- c7 nenhum vetor observado (MEDIDO): a bandeira do contrato, nenhuma chave de dado observado no npz, e os caminhos TOCADOS durante esta mecanica (open/exists/listdir/scandir/stat instrumentados) nao caem sob a pasta vedada
    #      (a entrega do Kimi, work\h0dn_bg1_v410_09nov\kimi\) nem levam nome vedado (y_obs, ...); a v410 pre-registra e NAO abre
    chaves_npz_ = list(npz_.files)
    _nrm = lambda p_: _os410.path.normcase(_os410.path.normpath(str(p_)))
    vedada_ = _nrm(c_["pasta_vedada"]); toc_ = sorted({_nrm(p_) for p_ in (tocados_ or [])})
    sob_vedada_ = [p_ for p_ in toc_ if p_.startswith(vedada_ + _os410.sep) or p_ == vedada_]
    vedados_ = ["".join(p_) for p_ in c_["nomes_vedados_partes"]]   # (montados aqui: o contrato os traz em partes)
    nomes_vedados_ = [p_ for p_ in toc_ if any(n_.lower() in _os410.path.basename(p_).lower() for n_ in vedados_)]
    c7_ok_ = (c_["observed_vector_read"] is False and not c_["observed_paths"] and not any(k_ in chaves_npz_ for k_ in c_["chaves_observadas_proibidas"]) and plano_.get("not_a_nature_verdict") is True
              and tocados_ is not None and not sob_vedada_ and not nomes_vedados_)
    # ---- c8 a guarda do texto: tokens proibidos ausentes do texto e das cabecas; a aritmetica do agregado publico fora do texto; as frases que dao o teste por feito ausentes
    txt_json_ = _j410.dumps(t_, ensure_ascii=False)
    frases_ = list(_v410_guarda_frases(txt_json_))
    c8_ok_ = (not any(tk_ in txt_json_ for tk_ in toks_) and not any(a_ in txt_json_ for a_ in agreg_) and not [f_ for f_ in frases_ if f_[0].startswith(("F53", "F54", "F55"))]
              and not any(tk_ in c_["veredito_ok"] for tk_ in toks_) and all(_v410_h0dn_cabeca(c_["ramos"]["vereditos"]["leitura_partes"]).find(tk_) < 0 for tk_ in toks_) and len(toks_) == 3)
    # ---- c9 o gate congelado; c10 a rota Kimi espectro x fotometria como NOT_TESTABLE (nao e' o teste); c11 a regra conjunta congelada na funcao; c12 P18 e a guarda das frases sobre o texto inteiro
    gate_ = ((core_.get("qg_closure") or {}).get("gate") or {}).get("verdict")
    c9_ok_ = isinstance(gate_, str) and gate_ == c_["baseline"]["gate_verdict"]
    rk_ = c_["rota_kimi"]
    c10_ok_ = rk_.get("estado") == "NOT_TESTABLE" and rk_.get("eta") == 1 and isinstance(rk_.get("mapa_seq"), int) and ("não é o teste" in txt_json_ or "nao e' o teste" in txt_json_)
    D0_ = D_por_[c_["modelos"][0]]
    r11a_ = veredito_h0dn(6.0, 2.5, D0_, True, True, ramos_)[2]; r11b_ = veredito_h0dn(6.0, 1.9, D0_, True, True, ramos_)[2]; r11c_ = veredito_h0dn(4.9, 0.0, D0_, True, True, ramos_)[2]; r11d_ = veredito_h0dn(6.0, -1.9, D0_, True, True, ramos_)[2]
    c11_ok_ = (r11a_, r11b_, r11c_, r11d_) == (5, 4, 6, 4) and c_["ramos"]["compat_95"] == 1.959963984540054 and c_["ramos"]["limiar"] == 5.0 and D0_ >= 5.0
    p18_ = list(_v392_guarda_texto(txt_json_))
    c12_ok_ = not p18_ and not frases_
    checks_ = [
        {"id": "c1", "descricao": "os %d pinos do FREEZE_R2 batem: os embutidos (base64 -> sha256 e bytes == o pino do contrato == o do FREEZE_R2) e os so' em disco, se presentes; o FREEZE_R2 e a ENTREGA pinados pelo contrato" % c_["n_pinos_freeze"], "ok": bool(c1_ok_)},
        {"id": "c2", "descricao": "K = E(z*)^(2 beta/3) e log10 K recomputados de beta (alfa CODATA 2018 x sqrt(e), runtime) com Omega_m/Omega_r e z* da lei congelada do BG1, |Delta| < %s contra o BG1 e o npz; z* e K iguais aos que a Fase 9 V1 transcreveu por hash no proprio um.py (hubble_ratio_v387)" % tol_["K"], "ok": bool(c2_ok_)},
        {"id": "c3", "descricao": "sd_null e sd_tgl dos dois modelos reproduzidos de weights, C_joint, gradient_h e gradient_k do npz (bloco cruzado local/fundo zero: independencia condicional ASSUMIDA, nao medida), |Delta| rel < %s" % tol_["sd_rel"], "ok": bool(c3_ok_)},
        {"id": "c4", "descricao": "D esperado = log10 K / sd_null dos dois modelos, |Delta| < %s contra a ENTREGA" % tol_["D"], "ok": bool(c4_ok_)},
        {"id": "c5", "descricao": "o poder analitico Phi(D - 5) e a cauda nula Phi(-5) (|Delta| < %s contra a ENTREGA e o FREEZE_R2), e o poder MC da ENTREGA dentro do IC95 dela (conferencia, nao recalculo)" % tol_["poder"], "ok": bool(c5_ok_)},
        {"id": "c6", "descricao": "a FUNCAO DE VEREDITO CONGELADA veredito_h0dn (E30 + D76) em %d vetores DETERMINISTICOS sem semente cobre os 6 ramos com os outcomes esperados; nenhuma cabeca traz a palavra do livro de cobrancas; a do ramo da leitura traz a validade na mesma string; sha256 do texto-fonte no registro" % len(c_["vetores_c6"]), "ok": bool(c6_ok_)},
        {"id": "c7", "descricao": "observed_vector_read = False, MEDIDO: nenhum vetor observado embutido (o npz nao tem chave de dado observado); os %d caminhos tocados durante esta mecanica (open/exists/listdir/scandir/stat instrumentados) nao caem sob a pasta vedada (a entrega do Kimi) nem levam nome vedado (%d nomes, montados do contrato); o plano diz not_a_nature_verdict" % (len(toc_), len(vedados_)), "ok": bool(c7_ok_)},
        {"id": "c8", "descricao": "a guarda: os tokens proibidos do H0DN ausentes do texto, do veredito e das cabecas; a aritmetica do agregado publico fora do texto; nenhuma frase que de o teste por feito (F53/F54/F55 limpas)", "ok": bool(c8_ok_)},
        {"id": "c9", "descricao": "o veredito do gate deste rito e' IDENTICO ao da v409 selada (congelado no contrato): o gate nao se move", "ok": bool(c9_ok_)},
        {"id": "c10", "descricao": "a rota Kimi “coerencia espectro x fotometria” consta como NOT_TESTABLE (eta = 1; Mapa seq %s): nao e' o teste" % rk_.get("mapa_seq"), "ok": bool(c10_ok_)},
        {"id": "c11", "descricao": "a regra conjunta (z_null >= 5 e |z_tgl| <= 1,959963984540054), exploratoria no Kimi, esta' CONGELADA na funcao de veredito: (6, 2,5) -> tensao; (6, 1,9) e (6, -1,9) -> a leitura; (4,9, 0) -> nao discriminado", "ok": bool(c11_ok_)},
        {"id": "c12", "descricao": "o texto do registro passa a guarda P18 (v392) e a guarda das frases (v405 -> v410)", "ok": bool(c12_ok_)},
    ]
    values_ = {"beta": beta_, "K": K_, "log10K": logK_, "E_zstar": E_, "z_star": zs_, "Omega_m": Om_, "Omega_r": Or_, "z_star_fase9_v1_no_um_py": zs_um_, "K_fase9_v1_no_um_py": K_um_, "H0_bg": float(bg1_["H0"]), "sigma_H0_bg": float(bg1_["sigma_H0"]),
               "modelos": sd_, "D_esperado": D_, "cauda_nula_analitica": Phi_(-c_["ramos"]["limiar"]), "cauda_nula_freeze": float(freeze_["null_alpha"]), "pinos": pinos_, "n_pinos": len(pinos_), "n_pinos_freeze": c_["n_pinos_freeze"], "n_embutidos": len(c_["insumos"]), "chaves_npz": chaves_npz_, "bloco_cruzado_max": cruz_,
               "veredito_h0dn_source_sha256": fonte_sha_, "vetores_c6": vet_, "ramos_vistos": sorted(ramos_vistos_), "regra_conjunta": {"6_e_2_5": r11a_, "6_e_1_9": r11b_, "4_9_e_0": r11c_, "6_e_menos_1_9": r11d_},
               "observed_vector_read": False, "gate_verdict": gate_, "p18_violacoes": p18_[:5], "frases_violacoes": frases_[:5], "plano_status": plano_.get("status"), "entrega_status": entrega_.get("status"),
               "caminhos_tocados": toc_, "n_caminhos_tocados": len(toc_), "sob_pasta_vedada": sob_vedada_, "com_nome_vedado": nomes_vedados_, "pasta_vedada": c_["pasta_vedada"]}
    return {"passed": all(x_["ok"] for x_ in checks_), "n_checks": len(checks_), "checks": checks_, "values": values_}


_V410_H0DN_RECUSA = "TGL_H0DN_BG1_V410__REFUSED_%s__GATE_UNMOVED"


def h0dn_bg1_v410(core):
    """v410 -- H0DN x BG1 (D72; a fala do operador de 09/11: «quanto ao teste da v410 concordo com tudo que vc falou, pode dar a ordem ao kimi k3pro»): o teste PRE-REGISTRADO da razao de Hubble local/fundo, lido no PONTO REAL do main,
    LOGO DEPOIS de iald2_v410. Pré-registrado; nenhum dado observado lido: os insumos embutidos e pinados por sha256, K recomputado de beta em runtime, sd/D/poder reproduzidos, a funcao de veredito congelada (E30 + D76) testada em
    vetores deterministicos, a guarda. Fail-closed em cada elo; excecao vira recusa visivel; nao move o gate. O poder e' prospectivo e sintetico; a abertura e' de versao futura, com a covariancia fisica fechada (G3/G4)."""
    c_ = _V410_H0DN_CONTRACT; t_ = _V410_H0DN_TEXT; i_ = _V410_H0DN_INSUMOS
    beta_rt_, beta_rel_, dois_nomes_, beta_ok_ = _v398_beta(core)
    out_ = {"all_verified": False, "runtime_executed": False, "does_not_gate_core": True, "observed_vector_read": False, "estatuto": t_["estatuto"], "scope": t_["escopo"], "limites": t_["limites"], "diz": t_["diz"], "nao_diz": t_["nao_diz"],
            "beta_ok": beta_ok_, "beta_core_rel_diff": beta_rel_, "alpha_two_names_same": dois_nomes_, "lei": dict(c_["lei"]), "modelos": list(c_["modelos"]), "ramos_da_funcao_de_veredito": {k_: v_ for k_, v_ in c_["ramos"]["vereditos"].items() if k_ != "leitura_partes"},
            "outcomes_do_livro_de_cobrancas": list(c_["ramos"]["outcomes"]), "n_checks_esperadas": c_["n_checks"], "insumos_pinados": {k_: {"sha256": v_["sha256"], "bytes": v_["bytes"], "rel": v_["rel"]} for k_, v_ in c_["insumos"].items()},
            "pinos_so_no_disco": list(c_["pinos_freeze_r2_so_no_disco"]), "ordem_kimi": dict(c_["ordem_kimi"]), "leitura_dossie": dict(c_["leitura_dossie"]), "rota_kimi": dict(c_["rota_kimi"]), "o_que_falta": list(t_["o_que_falta"]), "ressalvas": list(t_["ressalvas"])}
    out_.update(t_["extras"])
    if not beta_ok_:
        out_["verdict"] = _V410_H0DN_RECUSA % "BETA_IS_NOT_ALPHA_SQRT_E"
    else:
        try:
            tocados_, restaura_ = _v410_h0dn_vigia_arquivos()   # (AVISO 09/11) todo caminho tocado pela mecanica e' registrado; a c7 recusa se tocar a entrega do Kimi ou um nome de dado observado
            try:
                mec_ = _v410_h0dn_mechanics(beta_rt_, core, c_, t_, i_, tocados_)
            finally:
                restaura_()
            out_.update(runtime_executed=True, mechanics={"passed": mec_["passed"], "n_checks": mec_["n_checks"], "checks": mec_["checks"]}, values=mec_["values"], all_verified=bool(mec_["passed"] and mec_["n_checks"] == c_["n_checks"]))
            out_["veredito_h0dn_source_sha256"] = mec_["values"]["veredito_h0dn_source_sha256"]
            out_["verdict"] = (c_["veredito_ok"] if out_["all_verified"] else _V410_H0DN_RECUSA % "MECHANICS_CHECK_FAILED")
        except Exception as e_:   # noqa: BLE001
            out_.update(runtime_executed=True, error=repr(e_)[:300])
            out_["verdict"] = _V410_H0DN_RECUSA % "RUNTIME_ERROR"
    core["h0dn_bg1_v410"] = out_
    return out_
