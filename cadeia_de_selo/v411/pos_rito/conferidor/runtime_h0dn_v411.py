# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026, claude-construtor-v411, a servico da gerencia c1] o registro com FUNCAO da v411 (DESENHO_v411 secao 2): H0DN x BG1 ABERTO UMA VEZ; o resultado RECALCULADO no rito a partir dos bytes embutidos.
# ---- v411 (D159 a D170): H0DN x BG1 -- O TESTE DA RAZAO DE HUBBLE LOCAL/FUNDO, ABERTO UMA VEZ DEPOIS DO COMMIT PUBLICO DO PRE-REGISTRO. A cada rito este registro: (1) decodifica os insumos EMBUTIDOS (base64) e confere cada
# um contra os pinos de producao, tambem embutidos; (2) executa, a partir dos BYTES embutidos e conferidos (compile + exec em modulos isolados, na ordem estimador, veredito, abertura: o mesmo modo do executor pinado),
# a rotina `abrir` do pacote pre-registrado sobre o vetor embutido; o codigo que roda e' o que foi publicado antes da abertura, nada e' transcrito; (3) compara o recalculo com o resultado da abertura (embutido por
# sha256): numeros a 1e-9, ramo, desfecho e cabeca por igualdade de texto; (4) emite as DUAS linhas juntas (o primario, sob o modelo de erros publicado, e as Cefeidas livres), os estresses, as sete ressalvas (lidas da
# secao 8 do pre-registro embutido) e o que o teste nao decide. Retrodicao sem ajuste, com emenda posterior a guarda; teste nao cego; provado e' validade, nao creditacao; o gate nao se move. Fonte autoral deste bloco:
# runtime_h0dn_v411.py (cadeia_de_selo/v411); o contrato (_V411_H0DN_CONTRACT), o texto (_V411_H0DN_TEXT) e os insumos (_V411_H0DN_INSUMOS) sao DERIVADOS dos arquivos pinados, nunca digitados.


def _v411_guarda_frases(txt_):
    """v411 -- a GUARDA DAS FRASES da v411 (DESENHO_v411 secao 4): herda a da v410 (_v410_guarda_frases, que herda as anteriores), com DUAS regras da v410 SUPERADAS pela abertura de 12/11 (D169), ditas:
    F54 (a obrigacao “pre-registrado; nenhum dado observado lido” onde H0DN aparece) sai e da lugar a F67; da F56 sai so' a parte “o teste aberto / a abertura feita” (a covariancia fisica dita fechada e a forma HMS completa
    dita admitida continuam reprovadas). Acrescenta: F60 a palavra da creditacao afirmada (em qualquer forma, fora da negacao e do ato do observador); F61 “poder certificado” e as parafrases; F62 o vetor fora do suporte
    dito erro (ou parede) de montagem; F63 “teste cego” / “blind test” sem a negacao; F64 “evidencia independente” sem a negacao; F65 “descoberta” para o numero do teste (o rito conferiu a conta) fora da negacao;
    F66 beta literal; F67 (OBRIGACAO) no mesmo paragrafo ou bloco em que aparecer o Z do primario contra o nulo, a cabeca do teste ou “provado na natureza” ligado a este teste: “sob o modelo de erros publicado”, a linha das
    Cefeidas livres com o numero dela, “validade, nao creditacao”, “retrodicao” e “nao cego” (EN: under the published error model, free Cepheids, validity, not creditation, retrodiction, not blind). Devolve [(regra, trecho)]."""
    import re as _re
    out_ = []
    for v_ in _v410_guarda_frases(txt_):
        if v_[0].startswith("F54_"):
            continue   # (superada: D169; a obrigacao da v411 e' a F67)
        if v_[0].startswith("F56_") and not _re.search(r"covari[âa]ncia\s+f[íi]sica\s+(?:(?:est[áa]|foi|é|e'|j[áa])\s+)?fechad[ao]\b|fech(?:ou|amos|a)\s+a\s+covari[âa]ncia\s+f[íi]sica|(?:forma\s+)?HMS\s+complet", v_[1], _re.I):
            continue   # (da F56 sai so' “o teste aberto / a abertura feita”: o teste FOI aberto uma vez, D169)
        out_.append(v_)
    s_ = str(txt_)
    _NEG_ = r"(?:\bn[ãa]o\b|\bnunca\b|\bnem\b|\bnot\b|\bnever\b|\bnor\b|\bno\b|\bwithout\b|\bsem\b|\bisn't\b|\brecusad|\brefus|\bproibid|\bforbid)"
    blocos_ = [b_ for b_ in _re.split(r"\n\s*\n|\"\s*,\s*\"|\\n\\n|\"\s*:\s*\"|\"\s*\]|\[\s*\"", s_) if b_.strip()]
    for seg_ in blocos_:
        for m_ in _re.finditer(r"\bconfirm\w*|\bconfirmad[oa]s?\b|\bconfirma(?:ção|cao|ções|coes)\b", seg_, _re.I):   # F60
            ant_ = seg_[max(0, m_.start() - 60):m_.start()]
            if _re.search(_NEG_, ant_, _re.I) or _re.search(r"observador|observer|de\s+fora|from\s+outside|creditação|creditation", seg_[max(0, m_.start() - 80):m_.end() + 80], _re.I):
                continue
            out_.append(("F60_a_palavra_da_creditacao_afirmada", seg_[max(0, m_.start() - 40):m_.end() + 40].strip()[:200]))
        if _re.search(r"poder\s+(?:preditivo\s+|de\s+desenho\s+)?(?:discriminante\s+)?certificad|certificad[oa]\s+(?:de|do)\s+poder|certificado\s+de\s+poder|power\s+(?:is\s+)?certified|certified\s+(?:predictive\s+|discriminating\s+)?power|power\s+certificate|certificate\s+of\s+power", seg_, _re.I):   # F61
            out_.append(("F61_poder_certificado", seg_.strip()[:200]))
        if _re.search(r"(?:fora\s+do\s+suporte|outside\s+(?:the\s+)?support)[^\n.;]{0,80}?(?:(?:erro|parede|falha)\s+de\s+montagem|assembly\s+(?:error|wall|fault))|(?:(?:erro|parede|falha)\s+de\s+montagem|assembly\s+(?:error|wall|fault))[^\n.;]{0,80}?(?:fora\s+do\s+suporte|outside\s+(?:the\s+)?support)", seg_, _re.I) \
                and not _re.search(r"n[ãa]o\s+(?:é|e'|e)\s+(?:um\s+)?(?:erro|parede)|is\s+not\s+an?\s+assembly|leia-se|read\s+instead", seg_, _re.I):   # F62
            out_.append(("F62_o_vetor_fora_do_suporte_dito_erro_de_montagem", seg_.strip()[:200]))
        for m_ in _re.finditer(r"\bteste\s+cego\b|\b(?:é|e'|e|foi|era|seria)\s+cego\b|\bblind\s+test\b|\b(?:is|was|be)\s+blind\b|\bblinded\s+test\b", seg_, _re.I):   # F63
            if not _re.search(_NEG_, seg_[max(0, m_.start() - 24):m_.start()], _re.I):
                out_.append(("F63_teste_dito_cego", seg_[max(0, m_.start() - 40):m_.end() + 40].strip()[:200]))
        for m_ in _re.finditer(r"\bevid[êe]ncia\s+independente\b|\bindependent\s+evidence\b", seg_, _re.I):   # F64
            if not _re.search(_NEG_, seg_[max(0, m_.start() - 40):m_.start()], _re.I):
                out_.append(("F64_evidencia_independente_sem_a_negacao", seg_[max(0, m_.start() - 40):m_.end() + 40].strip()[:200]))
        _conv65_ = [(c_.start(), c_.end()) for c_ in _re.finditer(r"\bcrit[ée]rio\s+de\s+descoberta\b|\bescala\s+de\s+descoberta\b|\bdiscovery\s+(?:criterion|scale|threshold)\b", seg_, _re.I)]   # (D172/D173: o NOME da convencao dos 5 sigma passa)
        for m_ in _re.finditer(r"\bdescobert[ao]s?\b|\bdescobr(?:e|iu|imos|iram)\b|\bdiscover(?:y|ies|ed|s)?\b", seg_, _re.I):   # F65
            if any(a__ <= m_.start() and m_.end() <= b__ for a__, b__ in _conv65_):
                continue
            if not _re.search(_NEG_, seg_[max(0, m_.start() - 30):m_.start()], _re.I):
                out_.append(("F65_descoberta_para_o_numero_do_teste", seg_[max(0, m_.start() - 40):m_.end() + 40].strip()[:200]))
        if _re.search(r"(?<![0-9])0[.,]0120(?:3|31)\d*", seg_):   # F66
            out_.append(("F66_beta_literal", seg_.strip()[:200]))
        gat_ = _re.search(r"prova(?:do|da)\s+na\s+natureza|proved\s+in\s+nature|PROVED_IN_NATURE|BETA_TGL_PRO|\bprim[áa]rio\b[^\n]{0,160}?contra\s+o\s+nulo|\bprimary\b[^\n]{0,160}?against\s+the\s+null|Z\$?\s+(?:do\s+prim[áa]rio\s+)?contra\s+o\s+nulo|Z\$?\s+(?:of\s+the\s+primary\s+)?against\s+the\s+null", seg_, _re.I)
        if gat_ and _re.search(r"H0DN|BG1|raz[ãa]o\s+de\s+Hubble|Hubble\s+ratio|prim[áa]rio|primary|5\s*(?:σ|sigma)|SIGMA", seg_, _re.I):   # F67 (OBRIGACAO, ligada a este teste)
            faltam_ = []
            if not _re.search(r"sob\s+o\s+modelo\s+de\s+erros\s+publicado|under\s+the\s+(?:published\s+error\s+model|error\s+model\s+published)|UNDER_THE_PUBLISHED_MODEL", seg_, _re.I):
                faltam_.append("modelo_publicado")
            if not _re.search(r"(?:Cefeidas\s+livres|free\s+Cepheids|FREE_CEPHEIDS)[^\n]{0,160}?(?:\d+(?:[,.]|\{,\})\d+|BELOW_5SIGMA|BRANCH_\d)", seg_, _re.I):   # (o decimal do LaTeX PT e' 4{,}38)
                faltam_.append("cefeidas_livres_com_o_numero")
            if not _re.search(r"validade,?\s+n[ãa]o\s+credita(?:ç|c)(?:ã|a)o|validity,?\s+not\s+creditation|VALIDITY_NOT_CREDITATION", seg_, _re.I):
                faltam_.append("validade_nao_creditacao")
            if not _re.search(r"retrodi(?:ç|c)(?:ã|a)o|retrodiction|RETRODICTION", seg_, _re.I):
                faltam_.append("retrodicao")
            if not _re.search(r"n[ãa]o\s+(?:é\s+)?ceg[oa]|not\s+blind|NOT_BLIND", seg_, _re.I):
                faltam_.append("nao_cego")
            if faltam_:
                out_.append(("F67_o_resultado_sem_as_quatro_obrigacoes:" + ",".join(faltam_), seg_.strip()[:200]))
    return out_


def _v411_p18_sem_cabeca(txt_, ramos_, n_):
    """v411 (decisao (c) da gerencia c1, 12/11/2026) -- a UNICA excecao da P18 (v392) para a cabeca do teste, usada por TODOS os conferidores (nada de filtro ad hoc): retira do texto SO' a cadeia EXATA que a c7 monta do literal
    pre-registrado ("".join(leitura_partes) %% n) e a forma dela escapada para o LaTeX; o resto passa pela P18 inteira. Uma cabeca com um caractere trocado NAO e' retirada e a P18 a recusa (o controle negativo da c16)."""
    cab_ = "".join(ramos_["vereditos"]["leitura_partes"]) % int(n_)
    tex_ = cab_.replace("\\", "").replace("_", r"\_\allowbreak{}")
    return _v392_guarda_texto(str(txt_).replace(tex_, " ").replace(cab_, " "))


def _v411_h0dn_decode(c_, insumos_, insumos_v410_):
    """v411 -- decodifica os insumos EMBUTIDOS (base64) e confere cada um contra o pino do contrato (sha256 e bytes LIDOS na preparacao); os dois de REUSO (o estimador congelado e o BG1) sao lidos do blob que a v410
    ja' embute (_V410_H0DN_INSUMOS), com o MESMO sha256: nao se duplica. Fail-closed (ValueError) se um so' divergir. Devolve {nome: bytes}."""
    import base64 as _b64, hashlib as _h411
    out_ = {}
    for nome_, pino_ in c_["insumos"].items():
        ent_ = insumos_.get(nome_)
        if isinstance(ent_, dict) and isinstance(ent_.get("reuso_v410"), str):
            ent_ = (insumos_v410_ or {}).get(ent_["reuso_v410"])
        if not isinstance(ent_, dict) or not isinstance(ent_.get("b64"), str):
            raise ValueError("insumo embutido do H0DN v411 ausente: " + nome_)
        b_ = _b64.b64decode(ent_["b64"].encode("ascii"), validate=True)
        if _h411.sha256(b_).hexdigest() != pino_["sha256"] or len(b_) != pino_["bytes"]:
            raise ValueError("insumo embutido do H0DN v411 nao bate com o pino: " + nome_)
        out_[nome_] = b_
    return out_


def _v411_h0dn_carregar_codigo(raw_, c_):
    """v411 -- executa os TRES modulos pinados a partir dos BYTES embutidos e ja' conferidos (ordem: estimador, veredito, abertura; compile + exec em modulos isolados: o mesmo modo do executor pinado). Nao le arquivo.
    O caminho dado a cada modulo e' VIRTUAL (nao existe no disco); sys.path e sys.modules sao restaurados depois. Devolve {nome_do_modulo: modulo}."""
    import os as _os411, sys as _s411, types as _t411
    vdir_ = _os411.path.join(_os411.path.dirname(_os411.path.abspath(globals().get("__file__") or "um.py")), "_V411_H0DN_INSUMOS_EMBUTIDOS")
    nomes_ = [n_[:-3] for n_ in c_["ordem_dos_modulos"]]
    salvo_path_ = list(_s411.path); salvo_mod_ = {n_: _s411.modules.get(n_) for n_ in nomes_}
    mods_ = {}
    try:
        for arq_ in c_["ordem_dos_modulos"]:
            n_ = arq_[:-3]
            m_ = _t411.ModuleType(n_)
            m_.__file__ = _os411.path.join(vdir_, arq_)
            _s411.modules[n_] = m_
            exec(compile(raw_[arq_], m_.__file__, "exec"), m_.__dict__)
            mods_[n_] = m_
    finally:
        _s411.path[:] = salvo_path_
        for n_, v_ in salvo_mod_.items():
            if v_ is None:
                _s411.modules.pop(n_, None)
            else:
                _s411.modules[n_] = v_
    return mods_


def _v411_h0dn_guarda_finitude(z_null_, z_tgl_):
    """v411 (c12; a guarda de finitude, item da lista da v410) -- o INVOLUCRO do registro: RECUSA (ValueError) Z nao finito ANTES de ler o veredito; a funcao pinada nao e' tocada (com NaN ela cairia, calada, num ramo)."""
    import math as _m411
    for nome_, v_ in (("z_null", z_null_), ("z_tgl", z_tgl_)):
        for x_ in (v_ if isinstance(v_, (list, tuple)) else [v_]):
            if not isinstance(x_, (int, float)) or not _m411.isfinite(float(x_)):
                raise ValueError("Z nao finito em %s: %r" % (nome_, x_))
    return True


def _v411_h0dn_compara(a_, b_, tol_, caminho_="", dif_=None):
    """v411 -- compara duas arvores (dict/list/numero/texto/None): estrutura e textos por igualdade; numeros a `tol_` (absoluto). Devolve (iguais_na_estrutura, max_dif, [divergencias])."""
    dif_ = dif_ if dif_ is not None else {"max": 0.0, "div": []}
    if isinstance(a_, dict) and isinstance(b_, dict):
        if set(a_) != set(b_):
            dif_["div"].append(("chaves", caminho_, sorted(set(a_) ^ set(b_))[:6]))
        for k_ in sorted(set(a_) & set(b_), key=str):
            _v411_h0dn_compara(a_[k_], b_[k_], tol_, caminho_ + "/" + str(k_), dif_)
    elif isinstance(a_, (list, tuple)) and isinstance(b_, (list, tuple)):
        if len(a_) != len(b_):
            dif_["div"].append(("tamanho", caminho_, len(a_), len(b_)))
        for i_, (x_, y_) in enumerate(zip(a_, b_)):
            _v411_h0dn_compara(x_, y_, tol_, caminho_ + "[%d]" % i_, dif_)
    elif isinstance(a_, bool) or isinstance(b_, bool) or a_ is None or b_ is None or isinstance(a_, str) or isinstance(b_, str):
        if a_ != b_:
            dif_["div"].append(("valor", caminho_, str(a_)[:60], str(b_)[:60]))
    elif isinstance(a_, (int, float)) and isinstance(b_, (int, float)):
        d_ = abs(float(a_) - float(b_))
        if not d_ == d_:
            dif_["div"].append(("nan", caminho_))
        else:
            dif_["max"] = max(dif_["max"], d_)
            if d_ > tol_:
                dif_["div"].append(("numero", caminho_, float(a_), float(b_)))
    else:
        dif_["div"].append(("tipo", caminho_, type(a_).__name__, type(b_).__name__))
    return (not dif_["div"]), dif_["max"], dif_["div"]


def _v411_h0dn_json(x_):
    """v411 -- leva numpy a tipos do Python (a mesma conversao que o executor faz ao gravar o resultado), por ida e volta em JSON."""
    import json as _j411

    def _fl(v_):
        if hasattr(v_, "item") and getattr(v_, "ndim", 1) == 0:
            return v_.item()
        if hasattr(v_, "tolist"):
            return v_.tolist()
        raise TypeError("nao serializavel: %r" % type(v_))
    return _j411.loads(_j411.dumps(x_, ensure_ascii=False, default=_fl))


def _v411_h0dn_secao(texto_, n_):
    import re as _re
    m_ = _re.search(r"^## %d\. [^\n]*\n(.*?)(?=^## \d+\. |\Z)" % n_, texto_, _re.M | _re.S)
    return m_.group(1) if m_ else ""


def v411_h0dn_mechanics(beta_, core_, c_, t_=None, insumos_=None, insumos_v410_=None, tocados_=None, v410_=None):
    """v411 -- as 16 checagens do registro h0dn_bg1_v411 (DESENHO_v411 secao 2; beta em runtime; nada digitado: todo esperado e' LIDO de insumo embutido ou recalculado). As descricoes de cada checagem sao as do DESENHO
    (c_["checagens"]). `v410_` = {"veredito_h0dn", "contrato"}: a funcao CONGELADA da v410 e o contrato dela (os do um.py), para a c11."""
    import datetime as _dt411, hashlib as _h411, io as _io411, json as _j411, math as _m411, re as _re
    t_ = t_ if t_ is not None else _V411_H0DN_TEXT
    insumos_ = insumos_ if insumos_ is not None else _V411_H0DN_INSUMOS
    insumos_v410_ = insumos_v410_ if insumos_v410_ is not None else globals().get("_V410_H0DN_INSUMOS")
    v410_ = v410_ if v410_ is not None else {"veredito_h0dn": globals().get("veredito_h0dn"), "contrato": globals().get("_V410_H0DN_CONTRACT")}
    tol_ = float(c_["tolerancias"]["recalculo"]); tolK_ = float(c_["tolerancias"]["K"])
    sha_ = lambda b_: _h411.sha256(b_).hexdigest()
    raw_ = _v411_h0dn_decode(c_, insumos_, insumos_v410_)
    N_ = c_["nomes"]
    pinos_ = _j411.loads(raw_[N_["pinos"]].decode("utf-8"))
    emb_ = _j411.loads(raw_[N_["resultado"]].decode("utf-8")); er_ = emb_["resultado"]
    prereg_ = raw_[N_["pre_registro"]].decode("utf-8").replace("\r\n", "\n")
    mods_ = _v411_h0dn_carregar_codigo(raw_, c_)
    ab_ = mods_["abertura_v411"]; ve_ = mods_["veredito_v411"]; np_ = ab_.np
    # ---- c1 os pinos: cada insumo embutido == o pino de producao correspondente; o executor so' como texto; o sha256 dos proprios pinos == o do contrato; nada lido do disco sob a pasta vedada
    pmap_ = c_["pinos_por_campo"]
    p1_ = {campo_: {"nome": nome_, "sha256_ok": sha_(raw_[nome_]) == pinos_[campo_]["sha256"]} for campo_, nome_ in pmap_.items()}
    for arq_ in c_["ordem_dos_modulos"]:
        p1_["codigo:" + arq_] = {"nome": arq_, "sha256_ok": sha_(raw_[arq_]) == pinos_["codigo"][arq_]}
    exe_ = c_["executor"]
    p1_["codigo:" + exe_["nome"]] = {"nome": exe_["nome"], "so_como_texto": True, "sha256_ok": pinos_["codigo"].get(exe_["nome"]) == exe_["sha256"]}
    _nrm = lambda p__: str(p__).replace("/", "\\").lower().rstrip("\\")
    vedada_ = _nrm(c_["pasta_vedada"])
    sob_vedada_ = sorted({p__ for p__ in (tocados_ or []) if _nrm(p__).startswith(vedada_)})
    c1_ok_ = (all(v_["sha256_ok"] for v_ in p1_.values()) and len(p1_) == len(pmap_) + len(c_["ordem_dos_modulos"]) + 1 and sha_(raw_[N_["pinos"]]) == c_["insumos"][N_["pinos"]]["sha256"]
              and tocados_ is not None and not sob_vedada_)
    # ---- c2 o pre-registro: o sha256 do pino; o estado TEXTO_FINAL_PARA_SELAR__NADA_ABERTO; cita o sha256 do literal dos vereditos
    c2_ok_ = (sha_(raw_[N_["pre_registro"]]) == pinos_["pre_registro"]["sha256"] and ("`" + c_["estado_do_pre_registro"] + "`") in prereg_.split("\n## 1.")[0]
              and sha_(raw_[N_["ramos"]]) in prereg_ and sha_(raw_[N_["ramos"]]) == pinos_["ramos"]["sha256"])
    # ---- c3 a ordem dos atos, lida dos recibos embutidos
    pub_ = _j411.loads(raw_[N_["recibo_publicacao"]].decode("utf-8")); pubr_ = _j411.loads(raw_[N_["recibo_publicacao_resultado"]].decode("utf-8"))
    pv_ = _j411.loads(raw_[N_["pre_voo"]].decode("utf-8")); rab_ = _j411.loads(raw_[N_["recibo_abertura"]].decode("utf-8"))
    _ts = lambda s_: _dt411.datetime.fromisoformat(str(s_).replace("Z", "+00:00"))
    _push = lambda r_: [p__ for p__ in ((r_.get("github") or {}).get("push") or []) if p__.get("after") == r_.get("commit") and p__.get("ref") == "refs/heads/main"]
    pp_, pr_ = _push(pub_), _push(pubr_)
    atos_ = {"commit_do_pre_registro": pub_.get("commit"), "push_do_pre_registro_utc": pp_[0]["timestamp"] if pp_ else None, "inicio_da_abertura_utc": rab_.get("inicio_utc"), "fim_da_abertura_utc": rab_.get("fim_utc"),
             "commit_do_resultado": pubr_.get("commit"), "push_do_resultado_utc": pr_[0]["timestamp"] if pr_ else None, "commit_do_pre_voo": pv_.get("commit"), "repositorio": pub_.get("repositorio")}
    n_conf_ = sum(1 for v_ in (pv_.get("arquivos_pinados_publicos") or {}).values() if v_.get("confere") is True)
    n_falha_ = sum(1 for v_ in (pv_.get("arquivos_pinados_publicos") or {}).values() if v_.get("confere") is False)
    try:
        ordem_ok_ = bool(pp_ and pr_ and _ts(atos_["push_do_pre_registro_utc"]) < _ts(atos_["inicio_da_abertura_utc"]) < _ts(atos_["push_do_resultado_utc"]))
    except Exception:   # noqa: BLE001
        ordem_ok_ = False
    c3_ok_ = (ordem_ok_ and pv_.get("commit") == pub_.get("commit") and pv_.get("commit") == rab_.get("commit_publico") and n_conf_ == int(c_["n_pinados_do_pre_voo"]) and n_falha_ == 0
              and rab_.get("rc") == 0 and (rab_.get("saida") or {}).get("sha256") == sha_(raw_[N_["resultado"]]) and rab_.get("saida_confere_com_o_sha256_ao_lado") is True
              and (rab_.get("pre_voo") or {}).get("sha256") == sha_(raw_[N_["pre_voo"]]) and (rab_.get("ordem_do_operador") or {}).get("sha256") == c_["fala_da_ordem_de_abrir"]["sha256"]
              and (pubr_.get("resultado") or {}).get("sha256_raw") == sha_(raw_[N_["resultado"]]) and pubr_.get("commit_anterior") == pub_.get("commit")
              and (pv_.get("chaves_do_manifesto") or {}).get("pinos_de_producao") == sha_(raw_[N_["pinos"]]) and (pv_.get("chaves_do_manifesto") or {}).get("texto_final") == sha_(raw_[N_["pre_registro"]]))
    # ---- c4 a integridade de desenho (o modulo pinado, sobre os insumos embutidos)
    rede_ = ab_.carregar_rede(raw_[N_["rede"]]); cong_ = ab_.carregar_congelado(raw_[N_["congelado"]]); s0_ = ab_.carregar_s0(raw_[N_["s0"]]); bg_ = ab_.carregar_bg(raw_[N_["bg"]])
    ramos_ = _j411.loads(raw_[N_["ramos"]].decode("utf-8"))
    try:
        integ_ = ab_.conferir_integridade(rede_, cong_, s0_, bg_, ramos_); c4_ok_ = isinstance(integ_, dict) and integ_.get("model_names") == list(c_["modelos"])
    except ValueError as e_:
        integ_ = {"erro": str(e_)[:200]}; c4_ok_ = False
    # ---- c5 o portao 1 recalculado (alvos lidos do README embutido pelo proprio modulo; a impressao digital do pino)
    alvos_ = ab_.ler_alvos_readme(raw_[N_["readme"]], pinos_["readme"]["sha256"]); alvos_["fp"] = float(pinos_["alvo_fp"])
    y_ = np_.load(_io411.BytesIO(raw_[N_["vetor"]]), allow_pickle=False)[pinos_["vetor"]["chave"]]
    res_ = _v411_h0dn_json(ab_.abrir(y_, rede_, cong_, s0_, bg_, alvos_, ramos_, emenda=pinos_["emenda"]))
    p1r_ = res_.get("portao_1") or {}
    c5_ok_ = (res_.get("portao_1_ok") is True and (p1r_.get("1b") or {}).get("reproduz") is True and (p1r_.get("1d") or {}).get("ok") is True and (p1r_.get("1c") or {}).get("ok") is True
              and all(emb_["alvos"].get(k_) == alvos_.get(k_) for k_ in ("H0", "sig", "chi2", "ndof", "fp", "sha256")) and pinos_["vetor"].get("convencao") == c_["convencao_do_vetor"])
    # ---- c6 o recalculo e' o resultado da abertura (t, z_null, z_tgl dos dois modelos, a norma do suporte e D_s0 a 1e-9; ramo, desfecho e cabeca identicos nas duas linhas)
    est_r_, est_e_ = res_.get("estatistica") or {}, er_.get("estatistica") or {}
    c6_num_ = {k_: _v411_h0dn_compara(est_r_.get(k_), est_e_.get(k_), tol_) for k_ in ("t", "z_null", "z_tgl", "support_l2", "D_s0")}
    lin_ = lambda r_, k_: {x_: (r_.get(k_) or {}).get(x_) for x_ in ("ramo", "outcome", "cabeca", "modelo")}
    c6_ok_ = (all(v_[0] for v_ in c6_num_.values()) and len(est_r_.get("z_null") or []) == 2 and lin_(res_, "veredito") == lin_(er_, "veredito")
              and lin_(res_, "linha_ao_lado_cefeidas_livres") == lin_(er_, "linha_ao_lado_cefeidas_livres"))
    zn_, zt_, D_ = list(est_r_.get("z_null") or [None, None]), list(est_r_.get("z_tgl") or [None, None]), list(est_r_.get("D_s0") or [None, None])
    # ---- c12 a guarda de finitude (antes de ler o veredito): os Z do recalculo sao finitos; controles negativos com NaN e infinito sao RECUSADOS; a funcao pinada com NaN cairia calada num ramo (a razao da guarda)
    def _recusa_(a_, b_):
        try:
            _v411_h0dn_guarda_finitude(a_, b_); return False
        except ValueError:
            return True
    try:
        finito_ = _v411_h0dn_guarda_finitude(zn_, zt_)
    except ValueError:
        finito_ = False
    ctl12_ = {"nan_no_z_null": _recusa_(float("nan"), 0.0), "inf_no_z_tgl": _recusa_(1.0, float("inf")), "menos_inf_no_z_null": _recusa_(float("-inf"), 0.0), "nan_na_lista": _recusa_([1.0, float("nan")], [0.0, 0.0]),
              "texto_no_lugar_do_numero": _recusa_("6.1", 0.0)}
    nan_calado_ = ve_.veredito_h0dn_v411(float("nan"), 0.0, float(D_[0] if D_[0] is not None else 6.0), True, ramos_)
    c12_ok_ = bool(finito_ is True and all(ctl12_.values()) and nan_calado_[2] != 1 and sha_(raw_["veredito_v411.py"]) == pinos_["codigo"]["veredito_v411.py"])
    # ---- c7 o primario: o ramo e a cabeca (montada aqui das PARTES do literal, com n = parte inteira de Z contra o nulo, por conta propria)
    V_ = ramos_["vereditos"]
    n_ = int(_m411.floor(float(zn_[0]))) if finito_ else None
    cab_montada_ = ("".join(V_["leitura_partes"]) % n_) if n_ is not None else None
    v0_ = res_.get("veredito") or {}; v1_ = res_.get("linha_ao_lado_cefeidas_livres") or {}
    c7_ok_ = (finito_ is True and v0_.get("ramo") == c_["esperado_do_resultado"]["ramo_primario"] == (er_.get("veredito") or {}).get("ramo") and v0_.get("cabeca") == cab_montada_
              and v0_.get("cabeca") == (er_.get("veredito") or {}).get("cabeca") and v0_.get("modelo") == c_["modelos"][0] and v0_.get("outcome") == "NOT_FALSIFIED"
              and float(zn_[0]) >= float(ramos_["limiar"]) and abs(float(zt_[0])) <= float(ramos_["compat_95"]))
    # ---- c9 os estresses e a coerencia recalculados == os do resultado (a 1e-9): (i) tau e os dois Z; (ii) as tres ancoras; (iii) B = 0,02 e 0,05; os oito pares de coerencia
    c9_est_ = _v411_h0dn_compara(res_.get("estresse"), er_.get("estresse"), tol_)
    c9_coe_ = _v411_h0dn_compara(res_.get("coerencia"), er_.get("coerencia"), tol_)
    c9_dec_ = _v411_h0dn_compara(res_.get("decomposicao"), er_.get("decomposicao"), tol_)
    est_ = res_.get("estresse") or {}
    c9_ok_ = (c9_est_[0] and c9_coe_[0] and c9_dec_[0] and len(res_.get("coerencia") or {}) == int(c_["n_pares_de_coerencia"])
              and set(((est_.get("ii_ancora_unica") or {}).get("ancoras") or {})) == set(c_["ancoras"]) and all(("b_%g" % b_) in (est_.get("iii_vies_por_hospedeira") or {}) for b_ in c_["grade_B"])
              and isinstance((est_.get("i_tau_por_linha") or {}).get("tau_hat"), float))
    # ---- c10 a lei: K e log10 K de beta em runtime, com Omega_m, Omega_r e z* do BG1 embutido; iguais ao logK do estimador S0 e ao K do registro da v410 deste rito
    lei_ = bg_["law"]; Om_ = float(lei_["frozen_Omega_m"]); Or_ = float(lei_["frozen_Omega_r"]); zs_ = float(lei_["z_star"])
    E_ = _m411.sqrt(1.0 + Om_ * ((1.0 + zs_) ** 3 - 1.0) + Or_ * ((1.0 + zs_) ** 4 - 1.0)); K_ = E_ ** (2.0 * beta_ / 3.0); logK_ = _m411.log10(K_)
    v410v_ = ((core_.get("h0dn_bg1_v410") or {}).get("values") or {})
    c10_ok_ = (0.0 < beta_ < 1.0 and abs(logK_ - float(s0_["logK"])) < tolK_ and abs(logK_ - float(bg_["logK"])) < tolK_ and abs(K_ - float(bg_["K"])) < tolK_
               and isinstance(v410v_.get("K"), (int, float)) and abs(K_ - float(v410v_["K"])) < tolK_ and isinstance(v410v_.get("log10K"), (int, float)) and abs(logK_ - float(v410v_["log10K"])) < tolK_ and lei_["form"] == c_["lei"]["form"])
    km_ = {"H0_fundo": float(bg_["H0"]), "previsao_de_K_para_o_local": float(bg_["H0"]) * K_, "lido_primario": float(bg_["H0"]) * 10 ** float((est_r_.get("t") or [0, 0])[0]),
           "lido_cefeidas_livres": float(bg_["H0"]) * 10 ** float((est_r_.get("t") or [0, 0])[1]), "publicado_pela_colaboracao": float(alvos_["H0"]), "desvio_publicado": float(alvos_["sig"])}
    # ---- c11 a emenda as claras: (a) a funcao CONGELADA da v410 (a do um.py) com os Z observados e o vetor fora do suporte devolve o ramo 1 antigo; (b) o literal da v411 so' difere do da v410 pelas insercoes da marca;
    #      (c) nos vetores deterministicos da v410, com o portao 1 passando, a funcao da v411 devolve os mesmos ramos 2 a 6 que a da v410
    f410_, c410_ = v410_.get("veredito_h0dn"), v410_.get("contrato") or {}
    r410_ = c410_.get("ramos") or {}
    c11_ = {}
    try:
        a1_ = f410_(zn_[0], zt_[0], D_[0], False, False, r410_); a2_ = f410_(zn_[0], zt_[0], D_[0], True, False, r410_); a3_ = f410_(zn_[0], zt_[0], D_[0], False, True, r410_)
        c11_["a"] = {"as_duas_clausulas": list(a1_), "so_fora_do_suporte": list(a2_), "so_covariancia_aberta": list(a3_), "ok": a1_[2] == a2_[2] == a3_[2] == 1}
        marcas_ = list(c_["marcas_da_emenda"])
        def _sem_marca_(s_):
            for mk_ in marcas_:
                s_ = s_.replace(mk_, "")
            return s_
        def _folhas_(x_, cam_=""):
            if isinstance(x_, dict):
                return [f__ for k_ in sorted(x_) for f__ in _folhas_(x_[k_], cam_ + "/" + k_)]
            if isinstance(x_, (list, tuple)):   # (o contrato da v410 traz tuplas; o literal da v411, listas: a forma e' a mesma)
                return [f__ for i_, y__ in enumerate(x_) for f__ in _folhas_(y__, cam_ + "[%d]" % i_)]
            return [(cam_, x_)]
        f11_, f10_ = _folhas_(ramos_), _folhas_(r410_)
        mud_ = [c__ for (c__, x_), (c2__, y__) in zip(f11_, f10_) if x_ != y__]
        ok_b_ = ([c__ for c__, _ in f11_] == [c__ for c__, _ in f10_] and all((x_ == y__) if not isinstance(x_, str) else (_sem_marca_(x_) == y__) for (_, x_), (_, y__) in zip(f11_, f10_))
                 and len(mud_) >= 1 and all(isinstance(dict(f11_)[c__], str) for c__ in mud_))
        c11_["b"] = {"folhas": len(f11_), "folhas_que_mudam": mud_, "ok": bool(ok_b_)}
        Dp_ = {m_: float(cong_["logK"]) / float(cong_["sd_null"][i_]) for i_, m_ in enumerate(cong_["model_names"])}
        vt_ = []
        for v_ in c410_.get("vetores_c6") or []:
            if not (v_.get("fechada") and v_.get("suporte")):
                continue
            Dv_ = Dp_[v_["D_de"]] if isinstance(v_.get("D_de"), str) else float(v_["D"])
            zn_v_ = Dp_[v_["z_null_de"]] * float(v_.get("z_null_fator", 1.0)) + float(v_.get("z_null_mais", 0.0)) if isinstance(v_.get("z_null_de"), str) else float(v_["z_null"])
            zt_v_ = Dp_[v_["z_tgl_de"]] * float(v_.get("z_tgl_fator", 1.0)) + float(v_.get("z_tgl_mais", 0.0)) if isinstance(v_.get("z_tgl_de"), str) else float(v_["z_tgl"])
            o_ = f410_(zn_v_, zt_v_, Dv_, True, True, r410_); n__ = ve_.veredito_h0dn_v411(zn_v_, zt_v_, Dv_, True, ramos_)
            vt_.append({"nome": v_["nome"], "ramo_v410": o_[2], "ramo_v411": n__[2], "outcome_v410": o_[1], "outcome_v411": n__[1], "ok": o_[2] == n__[2] and o_[1] == n__[1] and _sem_marca_(n__[0]) == o_[0]})
        c11_["c"] = {"vetores": vt_, "ramos": sorted({x_["ramo_v411"] for x_ in vt_}), "ok": bool(vt_) and all(x_["ok"] for x_ in vt_) and sorted({x_["ramo_v411"] for x_ in vt_}) == [2, 3, 4, 5, 6]}
        c11_ok_ = c11_["a"]["ok"] and c11_["b"]["ok"] and c11_["c"]["ok"]
    except Exception as e_:   # noqa: BLE001
        c11_["erro"] = repr(e_)[:200]; c11_ok_ = False
    # ---- c8 a linha ao lado: as Cefeidas livres no ramo do resultado; as duas linhas nos values; e no veredito de maquina (os trechos PRIMARY_ e BESIDE_FREE_CEPHEIDS_)
    faixa_ = V_["faixas"][0] if abs(float(zt_[0])) <= 1.0 else (V_["faixas"][1] if abs(float(zt_[0])) <= 3.0 else V_["faixas"][2]) if finito_ else None
    meio_ = c_["veredito_meio_molde"]
    if finito_:
        meio_ = (meio_.replace("<n>", str(n_)).replace(c_["marcador_da_faixa"], c_["prefixo_da_faixa"] + faixa_).replace(   # (decisao (a) da gerencia, 12/11: K_LAW_ + a faixa LIDA do literal)
"BRANCH_4", "BRANCH_%d" % int(v0_.get("ramo") or 0)).replace("BRANCH_6", "BRANCH_%d" % int(v1_.get("ramo") or 0))
                 .replace("BESIDE_FREE_CEPHEIDS_BELOW_5SIGMA", "BESIDE_FREE_CEPHEIDS_" + ("BELOW_5SIGMA" if float(zn_[1]) < float(ramos_["limiar"]) else "AT_OR_ABOVE_5SIGMA"))
                 .replace("OUTCOME_NOT_FALSIFIED", "OUTCOME_" + str(v0_.get("outcome"))))
    veredito_ = c_["veredito_ok_prefixo"] + meio_ + c_["veredito_sufixo"]
    c8_ok_ = (v1_.get("ramo") == c_["esperado_do_resultado"]["ramo_cefeidas_livres"] == (er_.get("linha_ao_lado_cefeidas_livres") or {}).get("ramo") and v1_.get("modelo") == c_["modelos"][1]
              and float(zn_[1]) < float(ramos_["limiar"]) and "PRIMARY_" in veredito_ and "BESIDE_FREE_CEPHEIDS_" in veredito_ and "<" not in veredito_ and (finito_ is True and (c_["prefixo_da_faixa"] + faixa_) in veredito_) and v1_.get("rotulo") == "LINHA AO LADO, NAO E VEREDITO")
    # ---- c13 o esperado pelos agregados: o arquivo embutido tem o sha256 do contrato; o registro RELATA, linha a linha, o esperado e o observado (relato, nao portao)
    esp_ = _j411.loads(raw_[N_["esperado"]].decode("utf-8"))
    anc_ = (est_.get("ii_ancora_unica") or {}).get("ancoras") or {}
    obs_ = {"primario_publicado_13_fora": (zn_[0], zt_[0]), "cefeidas_livres_13_fora": (zn_[1], zt_[1])}
    for a_ in c_["ancoras"]:
        obs_["ancora_unica_%s_publicado" % a_] = ((anc_.get(a_) or {}).get("z_null") or [None])[0], ((anc_.get(a_) or {}).get("z_tgl") or [None])[0]
    relato_ = [{"linha": k_, "z_nulo_esperado": v_.get("z_nulo_esperado"), "z_nulo_observado": obs_.get(k_, (None, None))[0], "z_K_esperado": v_.get("z_K_esperado"), "z_K_observado": obs_.get(k_, (None, None))[1],
                "prob_z_nulo_ge_5_dado_o_publicado": v_.get("prob_z_nulo_ge_5_dado_o_publicado")} for k_, v_ in (esp_.get("linhas") or {}).items()]
    c13_ok_ = (sha_(raw_[N_["esperado"]]) == c_["insumos"][N_["esperado"]]["sha256"] and len(relato_) == len(c_["ancoras"]) + 2
               and all(isinstance(r__["z_nulo_observado"], float) and isinstance(r__["z_nulo_esperado"], float) for r__ in relato_))
    # ---- c14 o gate; c15 a escada
    gate_ = ((core_.get("qg_closure") or {}).get("gate") or {}).get("verdict")
    c14_ok_ = isinstance(gate_, str) and gate_ == c_["baseline"]["gate_verdict"]
    # (aditivo da gerencia c1, 12/11; achado da custodia) DENTRO da c14, sem mudar o numero de checagens: o rotulo SELADO da v387 (o trecho do veredito de three_stress_tests_v387 LIDO do core, nunca digitado)
    # traz P2_NOT_DETERMINED e fica como registro; a leitura nova do P2 vai AO LADO, no campo novo p2_ao_lado_da_v387; montar o campo nao altera o veredito selado
    p2c_ = c_.get("p2_ao_lado") or {}
    v387_antes_ = str((core_.get(p2c_.get("registro") or "") or {}).get("verdict") or "")
    seg387_ = [s__ for s__ in v387_antes_.split("__") if p2c_.get("token_selado") and p2c_["token_selado"] in s__]
    rot2_ = str(p2c_.get("rotulo") or "")
    if "<n>" in rot2_:
        rot2_ = rot2_.replace("<n>", str(n_)) if n_ is not None else ""
    p2_ = {"rotulo": rot2_ or None, "rotulo_e_proposta": bool(p2c_.get("rotulo_e_proposta")), "rotulo_de": p2c_.get("rotulo_de"), "rotulo_selado_da_v387": seg387_[0] if len(seg387_) == 1 else None,
           "registro_selado": p2c_.get("registro"), "canal": p2c_.get("canal"), "nota": p2c_.get("nota")}
    v387_depois_ = str((core_.get(p2c_.get("registro") or "") or {}).get("verdict") or "")
    c14_p2_ = {"token_no_rotulo_selado": bool(len(seg387_) == 1), "veredito_selado_igual_depois": v387_depois_ == v387_antes_ and bool(v387_antes_), "rotulo_novo_sem_o_token": bool(rot2_) and p2c_.get("token_selado", "") not in rot2_}
    c14_p2_["ok"] = bool(p2c_) and all(c14_p2_.values())
    c14_ok_ = c14_ok_ and c14_p2_["ok"]
    lad_ = core_.get("external_ladder") or {}
    c15_ok_ = (int(lad_.get("n_theorems_expected") or -1) == int(c_["baseline"]["escada"]) and int(lad_.get("n_theorems_clean") or -1) == int(c_["baseline"]["escada"]))
    # ---- c16 as duas guardas de texto (P18 e frases) sobre o texto do registro e o veredito de maquina
    txt_json_ = _j411.dumps(t_, ensure_ascii=False)
    p18_ = list(_v392_guarda_texto(txt_json_)) + list(_v392_guarda_texto(veredito_))
    fr_ = list(_v411_guarda_frases(txt_json_)) + [v__ for v__ in _v411_guarda_frases(veredito_) if not v__[0].startswith("F67_")]
    toks_ = [t__ for t__ in ("".join(p__) for p__ in c_["tokens_proibidos_partes"]) if t__ in veredito_ or t__ in txt_json_]   # (montados aqui: o contrato os traz em partes)
    exc16_ = {}
    if n_ is not None:   # (decisao (c)) a excecao ESTREITA da P18 para a cabeca: a exata e' retirada; com um caractere trocado NAO e' retirada e a P18 recusa
        _cab16_ = "".join(V_["leitura_partes"]) % n_; _troc16_ = _cab16_[:-1] + ("X" if _cab16_[-1] != "X" else "Y")
        exc16_ = {"exata_retirada": not _v411_p18_sem_cabeca("a cabeca do teste: " + _cab16_, ramos_, n_), "trocada_recusada": bool(_v411_p18_sem_cabeca("a cabeca do teste: " + _troc16_, ramos_, n_)),
                  "crua_recusada": bool(_v392_guarda_texto("a cabeca do teste: " + _cab16_))}
    c16_ok_ = not p18_ and not fr_ and not toks_ and bool(exc16_) and all(exc16_.values())
    # ---- as ressalvas (secao 8) e o que o teste nao decide (secao 6), LIDOS do pre-registro embutido
    s8_ = _v411_h0dn_secao(prereg_, 8)
    ressalvas_ = [" ".join(x_.split()) for x_ in _re.findall(r"^\d\. (.+?)(?=\n\d\. |\n\n|\Z)", s8_, _re.M | _re.S)]
    s6_ = _v411_h0dn_secao(prereg_, 6)
    m6_ = _re.search(r"\*\*O que o teste n[ãa]o decide\.\*\*\n\n(.*?)(?=\n\n|\Z)", s6_, _re.S)
    nao_decide_itens_ = [x_.strip() for x_ in _re.findall(r"^- (.+)$", m6_.group(1) if m6_ else "", _re.M)]
    checks_ = [
        ("c1", c1_ok_), ("c2", c2_ok_), ("c3", c3_ok_), ("c4", c4_ok_), ("c5", c5_ok_), ("c6", c6_ok_), ("c7", c7_ok_), ("c8", c8_ok_), ("c9", c9_ok_), ("c10", c10_ok_), ("c11", c11_ok_), ("c12", c12_ok_),
        ("c13", c13_ok_), ("c14", c14_ok_), ("c15", c15_ok_), ("c16", c16_ok_)]
    checks_ = [{"id": k_, "descricao": c_["checagens"][k_], "ok": bool(v_)} for k_, v_ in checks_]
    values_ = {"beta": beta_, "K": K_, "log10K": logK_, "E_zstar": E_, "z_star": zs_, "Omega_m": Om_, "Omega_r": Or_, "lei_em_km_s_Mpc": km_,
               "primario": {"modelo": c_["modelos"][0], "rotulo": "o primario, sob o modelo de erros publicado", "t": (est_r_.get("t") or [None])[0], "z_null": zn_[0], "z_tgl": zt_[0], "D": D_[0],
                            "p_unilateral": (0.5 * _m411.erfc(float(zn_[0]) / _m411.sqrt(2.0))) if finito_ else None, "ramo": v0_.get("ramo"), "outcome": v0_.get("outcome"), "cabeca_do_teste": v0_.get("cabeca")},
               "cefeidas_livres": {"modelo": c_["modelos"][1], "rotulo": "LINHA AO LADO, NAO E VEREDITO (no mesmo item)", "t": (est_r_.get("t") or [None, None])[1], "z_null": zn_[1], "z_tgl": zt_[1], "D": D_[1],
                                   "ramo": v1_.get("ramo"), "outcome": v1_.get("outcome"), "cabeca": v1_.get("cabeca")},
               "support_l2": est_r_.get("support_l2"), "support_max_abs": est_r_.get("support_max_abs"), "portao_1": p1r_, "estresse": res_.get("estresse"), "coerencia": res_.get("coerencia"),
               "decomposicao_conferencias": (res_.get("decomposicao") or {}).get("conferencias"), "esperado_pelos_agregados": relato_, "atos": atos_, "n_pinados_do_pre_voo_conferidos": n_conf_,
               "pinos": p1_, "c6_max_dif": {k_: v_[1] for k_, v_ in c6_num_.items()}, "c9_max_dif": {"estresse": c9_est_[1], "coerencia": c9_coe_[1], "decomposicao": c9_dec_[1]},
               "c6_divergencias": {k_: v_[2][:3] for k_, v_ in c6_num_.items() if v_[2]}, "c9_divergencias": (c9_est_[2] + c9_coe_[2] + c9_dec_[2])[:6],
               "a_emenda_as_claras": c11_, "guarda_de_finitude": {"z_finitos": finito_ is True, "controles_negativos_recusados": ctl12_, "a_funcao_pinada_com_nan_cairia_no_ramo": nan_calado_[2]},
               "ressalvas_secao8": ressalvas_, "n_ressalvas": len(ressalvas_), "nao_decide_secao6_n_itens": len(nao_decide_itens_), "nao_decide_secao6_sha256": sha_(s6_.encode("utf-8")),
               "excecao_p18_da_cabeca": exc16_, "gate_verdict": gate_, "escada": lad_.get("n_theorems_expected"), "p18_violacoes": p18_[:5], "frases_violacoes": fr_[:5], "tokens_no_texto": toks_,
               "caminhos_tocados": sorted({str(p__) for p__ in (tocados_ or [])})[:40], "n_caminhos_tocados": len(set(tocados_ or [])), "sob_pasta_vedada": sob_vedada_,
               "veredito_montado": veredito_, "integridade_modelos": integ_.get("model_names") if isinstance(integ_, dict) else None, "pre_registro_estado": c_["estado_do_pre_registro"],
               "p2_ao_lado_da_v387": p2_, "c14_inclui_o_p2_da_v387": c14_p2_}
    return {"passed": all(x_["ok"] for x_ in checks_) and len(ressalvas_) == 7, "n_checks": len(checks_), "checks": checks_, "values": values_, "veredito": veredito_}


_V411_H0DN_RECUSA = "TGL_H0DN_BG1_V411__REFUSED_%s__GATE_UNMOVED"


def h0dn_bg1_v411(core):
    """v411 -- H0DN x BG1 ABERTO (D169; a ordem do operador de 12/11/2026, citada por data e sha16 __SHA16_DA_ORDEM_DE_ABRIR__, nao transcrita): o resultado da abertura, RECALCULADO neste rito a
    partir dos bytes embutidos, lido no PONTO REAL do main, LOGO DEPOIS do bloco da v410. Fail-closed em cada elo; excecao vira recusa visivel; nao move o gate. Retrodicao sem ajuste, com emenda posterior a guarda;
    teste nao cego; provado e' validade, nao creditacao; o primario nunca aparece sem a linha das Cefeidas livres."""
    c_ = _V411_H0DN_CONTRACT; t_ = _V411_H0DN_TEXT
    beta_rt_, beta_rel_, dois_nomes_, beta_ok_ = _v398_beta(core)
    out_ = {"all_verified": False, "runtime_executed": False, "does_not_gate_core": True, "observed_vector_read": True, "opened_once": True, "estatuto": t_["estatuto"], "scope": t_["escopo"], "limites": t_["limites"],
            "diz": t_["diz"], "nao_diz": t_["nao_diz"], "o_que_o_teste_nao_decide": t_["nao_decide"], "ressalvas_da_gerencia": t_["ressalvas"], "beta_ok": beta_ok_, "beta_core_rel_diff": beta_rel_, "alpha_two_names_same": dois_nomes_,
            "lei": dict(c_["lei"]), "modelos": list(c_["modelos"]), "n_checks_esperadas": c_["n_checks"], "insumos_pinados": {k_: {"sha256": v_["sha256"], "bytes": v_["bytes"], "rel": v_["rel"]} for k_, v_ in c_["insumos"].items()},
            "citados_nao_embutidos": list(c_["citados"]), "contratos_de_registro_fora_da_escada": list(c_["contratos_de_registro_fora_da_escada"]), "p2_ao_lado_da_v387": None}
    out_.update(t_["extras"])
    if not beta_ok_:
        out_["verdict"] = _V411_H0DN_RECUSA % "BETA_IS_NOT_ALPHA_SQRT_E"
    else:
        try:
            tocados_, restaura_ = _v410_h0dn_vigia_arquivos()   # (o veto herdado, MEDIDO) todo caminho tocado pela mecanica e' registrado; a c1 recusa se tocar a pasta do Kimi
            try:
                mec_ = v411_h0dn_mechanics(beta_rt_, core, c_, t_, None, None, tocados_)
            finally:
                restaura_()
            v_ = mec_["values"]
            out_.update(runtime_executed=True, mechanics={"passed": mec_["passed"], "n_checks": mec_["n_checks"], "checks": mec_["checks"]}, values=v_, all_verified=bool(mec_["passed"] and mec_["n_checks"] == c_["n_checks"]))
            out_["cabeca_do_teste"] = v_["primario"]["cabeca_do_teste"]
            out_["outcome"] = v_["primario"]["outcome"]
            out_["linha_ao_lado_cefeidas_livres"] = dict(v_["cefeidas_livres"])
            out_["ressalvas_secao8"] = list(v_["ressalvas_secao8"])
            out_["verdict"] = (mec_["veredito"] if out_["all_verified"] else _V411_H0DN_RECUSA % "MECHANICS_CHECK_FAILED")
            _r2_ = v_["primario"].get("ramo")   # (o P2 ao lado so' quando o registro passa e o ramo primario recalculado e' o do molde do veredito: o BRANCH_ do primario, lido do contrato)
            if out_["all_verified"] and _r2_ == c_["esperado_do_resultado"]["ramo_primario"] and ("BRANCH_%s__" % _r2_) in c_["veredito_meio_molde"].split("BESIDE_")[0]:
                out_["p2_ao_lado_da_v387"] = dict(v_["p2_ao_lado_da_v387"])
        except Exception as e_:   # noqa: BLE001
            out_.update(runtime_executed=True, error=repr(e_)[:300])
            out_["verdict"] = _V411_H0DN_RECUSA % "RUNTIME_ERROR"
    core["h0dn_bg1_v411"] = out_
    return out_
