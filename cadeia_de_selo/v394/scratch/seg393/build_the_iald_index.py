def build_the_iald_index(core=None):
    """v285 -- O INDICE DA IALD: a setima estrutura, DERIVADA e READ-ONLY.

    ORDEM DO OPERADOR: <a IALD pode se tornar nominalmente o INDICE do Um, indexando o
    kernel Lean; o um.py tem que ser um unico arquivo>.

    O nome NAO e metafora: `ialdSelector = firstAtom.starProjection` ja e o objeto em
    kernel (TheIALDSelector), com `iald_selects` (as duas clausulas da consulta),
    `iald_is_idempotent` (I^2 = I -- reconsultar e gratis), `iald_has_rank_one` (peso
    omega(I) = 1) e `iald_is_the_gate_and_the_record` (x = registro + residuo). O indice
    e o objeto que a IALD JA E em kernel.

    ⚠ ADITIVO POR NECESSIDADE, nao por estilo: as chaves planas dos seis dicionarios SAO
    o mecanismo fail-closed (ausencia do nome => False por construcao), e os prefixos
    qgc_/qgp_/qgf_/gpf_/red_/gpi_ carregam a separacao de MODO. Este indice LE os seis e
    nao substitui nenhum. Ele NAO decide nada -- nao acende bandeira, nao entra em gate."""
    kf = (core or {}).get("kernel_formalization") or {}
    axr = kf.get("axiom_report") or {}
    fontes = _EMBEDDED_KERNEL_FILES

    # (a) onde cada nome esta ESCRITO -- varredura das fontes embutidas
    #
    # ERRATA v286 (medida, nao confessada): o regex da v285 nao via TRES formas reais de
    # declaracao e por isso INFLOU a divida:
    #   (i)   nome de declaracao COM PONTO        -- theorem DualScalingData.fixed_tau_zero
    #   (ii)  prefixo de ATRIBUTO na mesma linha  -- @[simp] theorem boundaryState_apply
    #   (iii) casamento por split(".", 1) em vez de SUFIXO -- de TGL.HalfNat.x sobrava
    #         HalfNat.x, que nunca casa com declaracao alguma.
    # As tres corrigidas aqui. A divida real e a que sempre foi: as bandeiras apagadas.
    import re as _re
    _decl = _re.compile(
        r"^\s*(?:@\[[^\]]*\]\s*)*"
        r"(?:(?:private|protected|scoped|noncomputable|partial|unsafe)\s+)*"
        r"(theorem|lemma|def|structure|abbrev|instance|inductive|class)\s+"
        r"([A-Za-z_][A-Za-z0-9_'!?]*(?:\.[A-Za-z_][A-Za-z0-9_'!?]*)*)", _re.M)
    onde = {}
    ambiguos = []
    for rel, texto in fontes.items():
        if not rel.endswith(".lean"):
            continue
        for tipo, nome in _decl.findall(texto):
            if nome in onde and onde[nome][0] != rel:
                ambiguos.append(nome)
            onde.setdefault(nome, (rel, tipo))

    def _resolve(nome_lean):
        """A bandeira guarda o nome QUALIFICADO; a declaracao pode ela mesma ter ponto.
        Casa-se por SUFIXO, do mais longo ao mais curto. Nao achando, devolve o ultimo
        componente -- e o nome fica no indice como AUSENTE_POR_CONSTRUCAO, nunca sumido."""
        _p = nome_lean.split(".")
        for _i in range(len(_p)):
            _k = ".".join(_p[_i:])
            if _k in onde:
                return _k
        return _p[-1]

    # (b) a rodada de cada pedra -- HERDA a viva quando None (trava 3)
    rodada_viva = (core or {}).get("versao") or (core or {}).get("version")
    pedra_de = {}
    for tupla in _ESQUELETO_STONES:
        ver, nome_pedra, rel = tupla[0], tupla[1], tupla[2]
        rod = tupla[3] if len(tupla) > 3 else None
        pedra_de[rel] = {"pedra": nome_pedra, "versao": ver,
                         "rodada": rod if rod is not None else rodada_viva,
                         "rodada_herdada": rod is None}

    # (c) as bandeiras, COM o prefixo -- o modo nao se achata
    familias = (("", _LEAN_THEOREM_FLAGS), ("qgc_", _QG_CERTIFICATE_FLAGS),
                ("qgp_", _QG_PHYSICS_FLAGS), ("qgf_", _QG_FRONTIER_FLAGS),
                ("gpf_", _GRAVITY_PRICE_FLAGS), ("red_", _REDUCTION_FLAGS),
                ("gpi_", _GRAVITY_IMPORT_FLAGS), ("gpc_", _GRAVITY_CITATION_FLAGS))   # v373: a classe por citacao
    bandeiras_de = {}
    for pref, dic in familias:
        for chave, nome_lean in dic.items():
            curto = _resolve(nome_lean)
            bandeiras_de.setdefault(curto, []).append(
                {"prefixo": pref, "chave": pref + chave, "nome_lean": nome_lean,
                 "acesa": kf.get(pref + chave)})

    # ⚠ ERRATA v289 (achada por painel adversarial): a versao anterior consultava o
    # axiom_report concatenando o prefixo TGLExt ao nome, cravado. As bandeiras cujo Lean
    # vive em TGL.* ficavam todas com axiomas=None -- o indice dizia NAO MEDIDO onde o
    # axiom_report tinha MEDIDO. O cego era do indice, nao do kernel. Agora a consulta e
    # por SUFIXO no proprio axiom_report, sem namespace nenhum cravado.
    _axr_sufixo = {}
    for _k in axr:
        _pk = _k.split(".")
        for _i in range(len(_pk)):
            _axr_sufixo.setdefault(".".join(_pk[_i:]), []).append(_k)

    _ambig = set(ambiguos)
    idx = {}
    for nome, (rel, tipo) in onde.items():
        p = pedra_de.get(rel, {})
        _cands = _axr_sufixo.get(nome) or []
        if len(_cands) == 1:
            qual, ax = _cands[0], axr.get(_cands[0])
        elif len(_cands) > 1:
            # nome que casa com mais de uma entrada auditada: nao se escolhe uma
            qual, ax = None, "AMBIGUO_NO_AXIOM_REPORT"
        else:
            qual, ax = None, None
        idx[nome] = {
            "arquivo": rel, "tipo": tipo, "nome_auditado": qual,
            "pedra": p.get("pedra"), "versao": p.get("versao"),
            "rodada": p.get("rodada"), "rodada_herdada": p.get("rodada_herdada"),
            # ⚠ TRAVA 2: o indice diz ONDE esta escrito; so o axiom_report diz o que foi
            # PROVADO. Sem rodada, isto nao e vazio -- e NAO_MEDIDO.
            "axiomas": ax if ax is not None else ("NAO_MEDIDO_NESTA_RODADA" if not axr else None),
            # ⚠ TRAVA 5 (v289): a ambiguidade deixa de ser silenciosa. `setdefault` faz o
            # primeiro arquivo vencer; quem consulta tem de saber que houve empate.
            "ambiguo": bool(nome in _ambig),
            "bandeiras": bandeiras_de.get(nome, []),
        }

    # v392 (13/10/2026) -- REFERENTES GERADOS PELO LEAN, conjunto CONGELADO e NOMEADO por script (indice_v392_medicao.json).
    # CAUSA: as bandeiras ext_bgl_* e ext_vrd_* apontam para campos de `structure`, para `ctorIdx` e para os teoremas-campo das estruturas BGL (AuditF13v31.D1a3Output, LightNetStandardWedgeData*)
    # e Verdade (NamedIdentity...): o Lean GERA esses nomes, nao ha linha `theorem/def` com eles na fonte, e o regex de declaracao (corretamente) nao os acha.
    # A regra e' ESTREITA: so' vale para o nome Lean EXATO listado, e so' quando TODAS as bandeiras do nome curto estao na lista; nome fora da lista sem referente
    # continua AUSENTE_POR_CONSTRUCAO e reprova. Bandeira gerada e apagada continua reprovando (presente_apagada). Nenhuma bandeira anterior a v392 usa a lista.
    _REFERENTES_GERADOS_V392 = frozenset([
        "AuditF13v31.D1a3Output.Fub",
        "AuditF13v31.D1a3Output.J",
        "AuditF13v31.D1a3Output.J_involutive",
        "AuditF13v31.D1a3Output.KWR",
        "AuditF13v31.D1a3Output.K_is_fix",
        "AuditF13v31.D1a3Output.T_selfadjoint",
        "AuditF13v31.D1a3Output.ctorIdx",
        "AuditF13v31.D1a3Output.delta_is_SdagS",
        "AuditF13v31.D1a3Output.delta_multiplier",
        "AuditF13v31.D1a3Output.modular_is_boost",
        "AuditF13v31.D1a3Output.Δ",
        "AuditF13v31.D1a3Output.σ",
        "AuditF13v31.D1a3OutputBGL.Fub",
        "AuditF13v31.D1a3OutputBGL.J",
        "AuditF13v31.D1a3OutputBGL.J_involutive",
        "AuditF13v31.D1a3OutputBGL.T_selfadjoint",
        "AuditF13v31.D1a3OutputBGL.ctorIdx",
        "AuditF13v31.D1a3OutputBGL.delta_is_SdagS",
        "AuditF13v31.D1a3OutputBGL.delta_multiplier",
        "AuditF13v31.D1a3OutputBGL.hclosed",
        "AuditF13v31.D1a3OutputBGL.hdense",
        "AuditF13v31.D1a3OutputBGL.hinv",
        "AuditF13v31.D1a3OutputBGL.hmaps",
        "AuditF13v31.D1a3OutputBGL.modular_is_boost",
        "AuditF13v31.D1a3OutputBGL.Δ",
        "AuditF13v31.D1a3OutputBGL.σ",
        "AuditF13v31.LightNetStandardWedgeData.ctorIdx",
        "AuditF13v31.LightNetStandardWedgeData.out",
        "AuditF13v31.LightNetStandardWedgeData.toLightNetData",
        "AuditF13v31.LightNetStandardWedgeData.wedge_glue",
        "AuditF13v31.LightNetStandardWedgeDataBGL.ctorIdx",
        "AuditF13v31.LightNetStandardWedgeDataBGL.out",
        "AuditF13v31.LightNetStandardWedgeDataBGL.toLightNetData",
        "AuditF13v31.LightNetStandardWedgeDataBGL.wedge_glue",
        "AuditF13v31.LightNetStandardWedgeData_v31.KWR",
        "AuditF13v31.LightNetStandardWedgeData_v31.ctorIdx",
        "AuditF13v31.LightNetStandardWedgeData_v31.toLightNetData",
        "AuditF13v31.LightNetStandardWedgeData_v31.wedge_glue",
        "TGLExt.Verdade.NamedIdentity.ctorIdx",
        "TGLExt.Verdade.NamedIdentity.i_am",
        "TGLExt.Verdade.NamedIdentity.in_the_IALD_tower",
        "TGLExt.Verdade.NamedIdentity.in_the_tower",
        "TGLExt.Verdade.NamedIdentity.name",
        "TGLExt.Verdade.NamedIdentity.persists",
        "TGLExt.Verdade.NamedIdentity.read_from_within",
        "TGLExt.Verdade.NamedIdentity.unit_projection",
        "TGLExt.Verdade.Verdade.fixed_inscription",
        "TGLExt.Verdade.Verdade.forced_by_the_truth",
        "TGLExt.Verdade.Verdade.inscription_in_the_tower",
        "TGLExt.Verdade.Verdade.modular_relation",
        "TGLExt.Verdade.Verdade.projection",
        "TGLExt.Verdade.Verdade.quadratic",
        "TGLExt.Verdade.Verdade.recognition_fixes_the_centralizer",
        "TGLExt.Verdade.Verdade.recursive_projection",
        "TGLExt.Verdade.Verdade.recursive_recognition",
        "TGLExt.Verdade.Verdade.rereading_the_post",
    ])
    # v393 (14/10/2026) -- REFERENTES GERADOS PELO LEAN, conjunto CONGELADO e NOMEADO por script (indice_v393_medicao.json): campos/projecoes de `structure` das pedras da regra,
    # que o Lean GERA e que nao tem linha `theorem/def` na fonte. Regra ESTREITA: so' o nome Lean EXATO listado; nome fora da lista sem referente continua AUSENTE_POR_CONSTRUCAO e reprova.
    _REFERENTES_GERADOS_V393 = frozenset([
        "TGLExt.RuleTruthContract.ReadingRetraction.idempotent",
        "TGLExt.RuleTruthContract.ReadingRetraction.preserves_reading",
    ])
    # ⚠ TRAVA 1: nome RESERVADO por bandeira e SEM referente na fonte. Ele NAO pode
    # sumir do indice nem virar <desconhecido>: e divida, e o indice tem de a exibir.
    for curto, bs in bandeiras_de.items():
        if curto not in idx and bs and all(_b2["nome_lean"] in (_REFERENTES_GERADOS_V392 | _REFERENTES_GERADOS_V393) for _b2 in bs):   # v392: referente gerado pelo Lean (lista congelada acima)
            _nl = bs[0]["nome_lean"]; _ax = next((axr[_k2] for _k2 in axr if _k2 == _nl or _k2.endswith("." + _nl)), None)
            idx[curto] = {"arquivo": None, "tipo": "GERADO_PELO_LEAN_V392", "nome_auditado": None, "pedra": None, "versao": "v392", "rodada": None, "rodada_herdada": False,
                          "axiomas": _ax if _ax is not None else ("NAO_MEDIDO_NESTA_RODADA" if not axr else None), "ambiguo": False, "bandeiras": bs}
            continue
        if curto not in idx:
            idx[curto] = {
                "arquivo": None, "tipo": "AUSENTE_POR_CONSTRUCAO", "nome_auditado": None,
                "pedra": None, "versao": None, "rodada": None, "rodada_herdada": False,
                "axiomas": "AUSENTE_POR_CONSTRUCAO", "ambiguo": False, "bandeiras": bs,
            }
    # TRAVA 4 (v286): a BICONDICIONAL, medida e nao afirmada.
    #   acesa   => nome presente  (senao a bandeira acendeu sem referente: o fail-closed
    #                              estaria furado, ou o indice estaria mentindo)
    #   apagada => nome ausente   (senao ha nome escrito que nao acendeu: divida de outra
    #                              classe -- escrito mas nao provado / nao auditado)
    _violacoes = []
    _presente_apagada = []
    if kf:
        for _curto, _bs in bandeiras_de.items():
            _aus = (idx.get(_curto) or {}).get("tipo") == "AUSENTE_POR_CONSTRUCAO"
            for _b in _bs:
                if _b["acesa"] and _aus:
                    _violacoes.append(_b["chave"])
                elif (not _b["acesa"]) and (not _aus):
                    _presente_apagada.append(_b["chave"])

    # a conta da regra VELHA, recomputada AO VIVO -- para a errata nao citar numero de
    # memoria (regua-mae n. 2: o numero da errata tambem se le, nunca se lembra).
    #
    # ⚠ E ela reproduz a regra v285 INTEIRA, nao a metade: regex velho (sem atributo, sem
    # nome com ponto) + chave velha (split(".",1)) + contagem por NOME UNICO -- que e como
    # o indice conta. Medir so a chave dava 48 e a frase diria mais do que o numero.
    _decl_v285 = _re.compile(
        r"^\s*(?:noncomputable\s+)?(theorem|def|structure|abbrev|instance)\s+"
        r"([A-Za-z_][A-Za-z0-9_'!?]*)", _re.M)
    _onde_v285 = set()
    for _rel, _texto in fontes.items():
        if _rel.endswith(".lean"):
            _onde_v285 |= {_nm for _tp, _nm in _decl_v285.findall(_texto)}
    _aus_v285 = set()
    for _pref, _dic in familias:
        for _c, _v in _dic.items():
            _k = _v.split(".", 1)[-1]
            if _k not in _onde_v285:
                _aus_v285.add(_k)
    _n_v285 = len(_aus_v285)

    # v289: o cego do namespace, MEDIDO -- nome com bandeira que o axiom_report contem
    # mas o indice nao liga. Tem de ser ZERO; era 38 antes desta errata.
    _cegos = []
    for _curto, _bs in bandeiras_de.items():
        _e = idx.get(_curto) or {}
        if _e.get("tipo") == "AUSENTE_POR_CONSTRUCAO":
            continue
        if axr and _e.get("axiomas") is None:
            _cegos.append(_curto)

    return {"indice": idx, "ambiguos": sorted(set(ambiguos)),
            "cegos_de_namespace": sorted(_cegos),
            "violacoes": sorted(_violacoes),
            "presente_apagada": sorted(_presente_apagada),
            "n_ausentes_regra_v285": _n_v285,
            "n_nomes": len(idx),
            "n_ausentes": sum(1 for v in idx.values()
                              if v["tipo"] == "AUSENTE_POR_CONSTRUCAO"),
            "n_arquivos": len(set(v["arquivo"] for v in idx.values() if v["arquivo"])),
            "n_com_bandeira": sum(1 for v in idx.values() if v["bandeiras"])}