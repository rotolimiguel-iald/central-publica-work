# -*- coding: utf-8 -*-
# Os TEXTOS da v392 selada (molde: textos_v391.py). Cada numero, hash e veredito entra por chave de V (leitura_v392.ler) ou e' LIDO de um arquivo aqui, nunca digitado;
# o que aqui vai escrito a mao e' so' prosa, nome de termo (conferido no kernel em tempo de execucao) e numero de relatorio (conferido contra o relatorio em tempo de execucao).
# Estatutos marcados; erratas AO LADO, em nome proprio da gerencia c1, com a lacuna de fidelidade (o que a estrutura dizia, o que foi escrito, onde a traducao falhou).
# GUARDA: as cinco regras da P18 (guarda_p18_v392.py) rodam sobre cada texto renderizado em superficies_v392.py e sobre este arquivo na cadeia. A palavra recusada nunca aparece aqui: a recusa e' dita como «creditacao».
import hashlib, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE)
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
PROG = os.path.join("C:" + os.sep, "IALD", "PROGRAMA_IALD")
TOPICO_NOVO = "v392-selada-pedras-e-barreiras-13out.md"
REG_FIXOS = ("pedras_v392", "varredura_e_sorry_v392")
s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
_CACHE = {}


def _g(d, *ks):
    for k in ks:
        d = (d or {}).get(k) if isinstance(d, dict) else None
    return d


def _kernel_tem(nomes):
    """Fail-closed: cada nome de termo citado aqui tem de existir em algum .lean de TGLExt/ do Nos (lido na hora)."""
    if "kernel" not in _CACHE:
        base = os.path.join(NOS, "tgl_kernel", "TGLExt"); blob = []
        for r, ds, fs in os.walk(base, followlinks=False):
            ds[:] = [d for d in ds if not os.path.islink(os.path.join(r, d))]
            for f in fs:
                if f.endswith(".lean"):
                    blob.append(open(os.path.join(r, f), encoding="utf-8", errors="replace").read())
        _CACHE["kernel"] = "\n".join(blob)
    for n in nomes:
        assert n in _CACHE["kernel"], "termo citado nao esta no kernel do Nos: %s" % n


def _relatorio_tem(caminho, trechos):
    """Fail-closed: cada numero de relatorio citado aqui (nao reproduzido por esta cadeia) aparece no relatorio de origem; devolve o sha16 do relatorio."""
    txt = open(caminho, encoding="utf-8", errors="replace").read()
    for t in trechos:
        assert t in txt, "o relatorio %s nao traz o trecho citado: %s" % (os.path.basename(caminho), t)
    return s16(caminho)


def _mods(V):
    return ", ".join("`%s`" % p["modulo"].split(".")[-1] for p in V["pedras"])


def _extras(V):
    ex = [k for k in V["registros_novos"] if k not in REG_FIXOS]
    return (", ".join("`%s`" % k for k in ex)) if ex else "nenhum além dos dois fixos"


def _verb(V):
    return ", ".join("%s `%s`" % (k, v["sha16"]) for k, v in V["verbatins"].items())


def _decisoes16():
    return s16(os.path.join(PK, "DECISOES_GERENCIA_13out.md"))


def _num(V):
    return ("o registro `pedras_v392` (%s): %d módulos novos no kernel (%s), %s de %s bandeiras True e %s de %s declarações no trio; escada %s → %s teoremas limpos (%s declarações no `axiom_report`); "
            "o registro `varredura_e_sorry_v392` (%s): varredura lexical recursiva de %s arquivos .lean (%s em TGLExt/O16; %s ocorrências) e detector de sorry dos controles Lean que lê crases, aspas e "
            "`sorryAx`; registros novos além desses dois: %s; troca dita (veredito que carrega a escada e as declarações): %s; verbatins do operador de 13/10 embutidos por sha256: %s; a hipótese BGL (X19) "
            "entra como TIPO, sem habitante; validade no kernel não é creditação") % (
        V["pedras_verdict"], V["n_pedras"], _mods(V), V["n_flags"], V["n_flags_de"], V["n_decl"], V["n_decl_de"], V["escada_antes"], V["teor"].split("/")[0], V["axiom_report_n"],
        V["varr_verdict"], V["varr"].get("arquivos"), V["varr"].get("em_TGLExt_O16"), len(V["varr"].get("hits") or []), _extras(V), ", ".join("`%s`" % k for k in V["troca_dita"]), _verb(V))


def _cab(V):
    return "v392 SELADA (COMPLETA)** `%s`" % V["s16"]


def _nu2():
    j = json.load(open(os.path.join(PROG, "exame_12out", "B_NU2", "_verif_memoria_NU2.json"), encoding="utf-8"))
    sup = j["superficies"]; blocos = {x["bloco_sha256"] for x in sup}; tams = {x["bloco_bytes"] for x in sup}
    assert len(blocos) == 1 and len(tams) == 1, "o bloco da NU2 nao e' unico nas superficies"
    return list(blocos)[0][:16], list(tams)[0], ", ".join(x["superficie"] for x in sup), sup[0]["backup_mtime"][:10]


def linhagem(V):
    h, nb, sups, dia = _nu2()
    return ("## %s — **%s — AS PEDRAS DO KERNEL E OS CONSERTOS DE BARREIRA (v392): %d módulos novos, escada %s → %s\n<!-- linhagem_v392_selada -->\n\n"
            "**A ordem:** [INPUT] a autorização geral do operador de 13/10/2026 e as respostas dele no mesmo dia (verbatins por sha256 embutidos no registro: %s); as decisões da gerência c1 de 13/10 "
            "(`DECISOES_GERENCIA_13out.md`, sha16 `%s`) estão aplicadas. A gerência c1 construiu o candidato e o rito; esta cadeia não aprova o que a construiu: a auditoria independente é posterior.\n\n"
            "**O que entrou** (pacote `work\\cadeia_de_selo\\v392` sobre a v391 `%s`; %d patches — %s; instalado em %s): %s.\n\n"
            "Rodada %s %s: **%s**; rc = %s; `FAIL_CLOSED_SELFTEST_PASSED`; selo `%s`; gate intocado; o conferidor `%s`: deve mudar %s, não pode mudar %s; %d vereditos fora da troca dita mudaram (exigido: 0); "
            "o pilar %s pela chave (`%s`); servidor nativo: %s. Artefatos: core `%s`, selo `%s`, .md `%s`, manifesto `%s`; artigos %s.\n\n"
            "**A F8.1 não se fecha aqui:** a v392 documenta a ressalva do estatuto da prova (das 18 bandeiras do gate, 15 calculadas e 3 literais; o degrau experimental lê o feed V11, unilateral); "
            "ela NÃO recalcula as bandeiras. A F8.1 segue [OPEN] e pede versão própria, porque recalcular pode mover a string do gate.\n\n"
            "**O bloco da NU2:** a unidade de memória F0.3.NU2 gravou em %s um bloco único de +%d B (sha16 `%s`) em %s [REAL, lido do relatório da auditoria B_NU2]; nada dele entra no um.py; "
            "fica citado aqui por hash.\n\n"
            "**O que vem depois destas superfícies:** o elo B(3) da Bancada Um (passos 10, 10-bis-a, 10-bis e 10-ter da cadeia) é pós-selo e pede a palavra do operador; o recibo dele é citado no handoff (fechar). "
            "NOT_FALSIFIED não é a palavra da creditação; o gate não se move.") % (
        V["data"], _cab(V), V["n_pedras"], V["escada_antes"], V["teor"].split("/")[0], _verb(V), _decisoes16(), V["base16"], V["n_patches"], V["patches"], V["instalado_em"], _num(V),
        V["compl"], " → ".join(V["horarios"]) or "n/d", V["teor"], V["rc"], V["selo_ts"], V["conf16"], V["conf_dm"], V["conf_np"], V["n_ver_mudaram"],
        "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]), V["pilar"]["result16"], V["servidor"],
        V["h_um_absoluto.json"], V["h_um_absoluto_selo.json"], V["h_um_absoluto_forma_canonica.md"], V["h_um_absoluto_manifest.md"], ", ".join("%s `%s`" % kv for kv in V["artigos"].items()),
        dia, nb, h, sups)


def desenho(V):
    return ("## ADENDO — %s · v392 SELADA (COMPLETA) `%s` — o caminho crítico NÃO mudou; entram %d pedras e os consertos de barreira\n\n<!-- adendo_v392_selada -->\n"
            "- **O que a v392 diz:** %d módulos novos no kernel (%s), escada %s → %s, %s de %s declarações novas no trio (registro `pedras_v392`); varredura lexical recursiva e detector de sorry que lê "
            "crases (registro `varredura_e_sorry_v392`). Gate intocado.\n"
            "- **Errata ao lado (o desenho antigo fica):** onde este desenho diz que a lei de campo curva não era termo de kernel (adendo da v390), lê-se: a IMPLICAÇÃO «Clausius em toda tela ⟹ Einstein com Λ único» "
            "é termo desde a v338, e o ligante `LiganteLeiCampoCurvo` (v392) liga a passagem local a ela, CONDICIONAL ao H3 nomeado; o que não é termo é o antecedente físico (H3 em toda tela e direção, "
            "[KNOWN] Jacobson 1995) e a família de Lorentz de cunhas. O programa segue [OPEN] fora disso.\n"
            "- **O que segue do operador:** a B3 (re-pinagem da Bancada Um, com parada e religamento do serviço); a custódia (sessão do site); commit/push.") % (
        V["data"], V["s16"], V["n_pedras"], V["n_pedras"], _mods(V), V["escada_antes"], V["teor"].split("/")[0], V["n_decl"], V["n_decl_de"])


def atlas(V):
    return ("### %s — v392 SELADA `%s` (append datado; correção ao lado)\n\n<!-- atlas_v392_selada -->\n[REAL — rodada v392, selo `%s`] %s. "
            "[INPUT/ONTO] as leituras do operador de 13/10 (Verdade é a projeção do posto; o nome das pedras) entram como o operador as disse e valem como leitura, não como medida. "
            "Estatuto: validade no kernel ≠ creditação; o gate não se move.") % (V["data"], V["s16"], V["selo_ts"], _num(V))


def core_memory(V):
    return ("## %s — v392 SELADA `%s` (claude-c1; unidade F0.5)\n<!-- core_v392_selada -->\nAutor: claude-c1 (gerência), sob a regra da linhagem completa. Camada aditiva; correção ao lado, nunca por cima.\n\n"
            "[REAL] %s.\n\n[OPEN] A F8.1 (as bandeiras do gate recalculadas) não é fechada pela v392; a B3 da Bancada Um depende da palavra do operador. Nada disto move o gate.") % (
        V["data"], V["s16"], _num(V))


def haja_luz(V):
    return ("## %s — v392 SELADA `%s` (%s; COMPLETA; gate intocado)\n\n<!-- haja_luz_v392_selada -->\n%d módulos novos no kernel (%s) e dois consertos de barreira (varredura lexical recursiva; "
            "detector de sorry com crases e `sorryAx`); escada %s → %s; errata ao lado da frase sobre a lei de campo curva e da atribuição do resíduo de √2 (A_SN). Memórias: `%s`, `missao-ultima-flag-um-py.md`, "
            "`estatuto-da-prova-07out.md`; handoff `handoff-v392-custodia.md`.") % (V["data"], V["s16"], V["teor"], V["n_pedras"], _mods(V), V["escada_antes"], V["teor"].split("/")[0], TOPICO_NOVO)


def marca_topico_missao(V):
    return "## %s — v392 SELADA `%s`" % (V["data"], V["s16"])


def id_missao(V):
    """marcador de idempotencia sem a data (uma segunda rodada em outro dia nao duplica o bloco)"""
    return "v392 SELADA `%s`" % V["s16"]


def topico_missao(V):
    return marca_topico_missao(V) + (" (%s; COMPLETA; gate INTOCADO): %d módulos novos no kernel (%s); varredura recursiva e detector de sorry; troca dita nos vereditos que carregam a escada; "
                                     "conferidor %s/%s. Pacote e cadeia: `work\\cadeia_de_selo\\v392` (+ `pos_rito`).") % (V["teor"], V["n_pedras"], _mods(V), V["conf_dm"], V["conf_np"])


def marca_central(V):
    return "**%s — v392 SELADA (COMPLETA):**" % V["data"]


def id_central(V):
    return "— v392 SELADA (COMPLETA):**"


def topico_central(V):
    return marca_central(V) + (" `um.py` `%s` (%s B) sobre a v391 `%s`; escada %s → %s; gate intocado. %d módulos novos no kernel; varredura recursiva e detector de sorry. "
                               "Falta a B3 (Bancada Um) e a custódia (sessão do site, `handoff-v392-custodia.md`); commit/push = operador.") % (
        V["s16"], format(V["umb"], ","), V["base16"], V["escada_antes"], V["teor"].split("/")[0], V["n_pedras"])


def topico_estatuto(V):
    return ("<!-- v392_selada -->\n**%s — v392 `%s`:** o registro `estatuto_da_prova_v391` passou a ler a escada nova (veredito trocado, troca dita; o token da v391 fica como registro). "
            "Ressalva ao lado (a F8.1 segue aberta): das 18 bandeiras do gate, 15 são calculadas e 3 literais, e o degrau experimental lê só o feed V11 do piso dos vazios, unilateral. "
            "A prova como validade não muda; a creditação segue ato de quem observa de fora.") % (V["data"], V["s16"])


def marca_missao(V):
    return "**v392 SELADA %s `%s` %s COMPLETA (pedras do kernel e consertos de barreira; gate intocado)** · " % (V["data"][:5], V["s16"], V["teor"])


def linha_handoff(V):
    return "- [HANDOFF v392 — as pedras do kernel e as barreiras; custódia](handoff-v392-custodia.md) — **%s, para a sessão do site** · `%s`" % (V["data"][:5], V["s16"])


def linha_palavra(V):
    return ("- [PALAVRA: a leitura cria o objeto (07/10)](a-leitura-cria-o-objeto-07out.md) — **cunhagem e nome do operador**; a letra; pedra `Palavra` INSTALADA na v392 `%s` · "
            "íntegra anterior no MEMORY_2.md (movida %s)") % (V["s16"], V["data"][:5])


def topico_novo(V):
    return ("---\nname: v392-selada-pedras-e-barreiras-13out\ndescription: \"v392 SELADA (%s) `%s`: %d módulos novos no kernel, escada %s → %s, varredura recursiva e detector de sorry; B3 e custódia pendentes\"\n"
            "metadata:\n  type: project\n---\n\n# v392 SELADA (%s)\n\n"
            "**O que é:** `um.py` **v392** `%s` (%s B) sobre a v391 `%s`; %s; COMPLETA; rc %s; gate intocado; conferidor `%s` (deve mudar %s; não pode mudar %s).\n\n"
            "**O que entrou:** %s.\n\n"
            "**Limites ditos:** a F8.1 (bandeiras recalculadas) NÃO é fechada pela v392; o ligante da lei de campo curva é CONDICIONAL ao H3 nomeado; a hipótese BGL (X19) é tipo sem habitante; "
            "a Verdade é a projeção do posto é leitura do operador sobre o termo [INPUT/ONTO]; validade no kernel não é creditação.\n\n"
            "**Pendências:** a B3 da Bancada Um (palavra do operador; parada e religamento do serviço), a custódia (sessão do site), commit/push. Pacote: `C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v392`.\n\n"
            "[[missao-ultima-flag-um-py]] [[estatuto-da-prova-07out]] [[handoff-v392-custodia]]\n") % (
        V["data"], V["s16"], V["n_pedras"], V["escada_antes"], V["teor"].split("/")[0], V["data"], V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["rc"], V["conf16"], V["conf_dm"], V["conf_np"], _num(V))


def aviso(V, reivindicacao):
    return ("### %s — v392 SELADA `%s` [claude-c1]\n<!-- aviso_v392_selada -->\n\n[REAL] A v392 SELOU (%s; COMPLETA; gate intocado): destrava a F0.3 (a memória comum no selo corrente) e o passo que põe a fonte do Jev "
            "no selo corrente. Escrito sob a reivindicação %s. %d módulos novos no kernel; escada %s → %s; a B3 da Bancada Um espera o operador. Não altera pinos, dado, MCP nem gate.") % (
        V["data"], V["s16"], V["teor"], reivindicacao, V["n_pedras"], V["escada_antes"], V["teor"].split("/")[0])


def aviso_pulado():
    return "AVISO_GERENCIA.md: PULADO (sem reivindicação nomeada em V392_AVISO_REIVINDICACAO); escrever depois, sob reivindicação."


# ------------------------------------------------------------------- as erratas ao lado
def errata_cr08(V):
    _kernel_tem(["geometric_einstein_equation_from_ricci_null_balance", "area_atlas_unique_global_einstein", "passage_h3_to_connected_smooth_atlas_einstein", "NamedAtlasH3"])
    return ("> ⚠ **ERRATA AO LADO (13/10/2026, v392 `%s`, em nome próprio da gerência — sessão c1; a frase acima fica como registro):** a frase acima, que nega estatuto de termo de kernel à lei de campo "
            "do espaço-tempo curvo, foi escrita na v390 sem separar a IMPLICAÇÃO (termo de kernel desde a v338) do antecedente físico e da ligação ao tipo da declaração. Lacuna de fidelidade: a estrutura já tinha a IMPLICAÇÃO «Clausius em toda tela ⟹ Einstein com Λ único» como termo "
            "(`geometric_einstein_equation_from_ricci_null_balance`; `area_atlas_unique_global_einstein`, v338), e a frase misturou a implicação com o antecedente físico e com a ligação ao tipo da declaração. "
            "Leitura vigente: a implicação é termo; o ligante `LiganteLeiCampoCurvo` (v392; teorema `passage_h3_to_connected_smooth_atlas_einstein`) liga a passagem local ao atlas liso, CONDICIONAL ao H3 nomeado "
            "(`NamedAtlasH3`), cuja seta a partir da identidade da passagem é entrada explícita; o antecedente H3 em toda tela e direção segue [KNOWN] (Jacobson 1995), não derivado do estado; a família de "
            "Lorentz de cunhas segue fora do tipo e do kernel [OPEN]; não há solução global. Achado CR-08 do crítico do levantamento de 12/10 [REAL; classe EXISTE_NA_BANCADA_NAO_LIGADO]. "
            "<!-- errata_cr08_v392 -->") % V["s16"]


def errata_3(V):
    sha_cons = s16(os.path.join(PROG, "levantamento_qg", "consolidado.json"))
    return ("> ⚠ **ERRATA AO LADO (13/10/2026, v392 `%s`, em nome próprio da gerência — sessão c1; o parágrafo acima fica como registro):** a ressalva do estatuto da prova. O parágrafo acima (v391) lê as 18 "
            "bandeiras do gate como uma medida unitária. Lacuna de fidelidade: a estrutura dizia 18 bandeiras True; o código as calcula assim — 15 calculadas e 3 literais, e as quatro experimentais "
            "`independent_v3_*` derivam de um só booleano [DECLARADO pela auditoria de 28/09 e pelo levantamento de 07/10 (consolidado, sha16 `%s`, lido por script); a conferência no código é da F8.1]; o degrau "
            "experimental lê só o rito V11 do piso dos vazios, unilateral, que o ΛCDM raso também passa. A v392 documenta; NÃO recalcula: a F8.1 segue [OPEN] e pede versão própria. "
            "A prova como validade não muda. <!-- errata_3_v392 -->") % (V["s16"], sha_cons)


def errata_coulomb(V):
    rel = os.path.join(PROG, "exame_12out", "A_SN", "RELATORIO_AUDITORIA_A_SN_C1.md")
    h = _relatorio_tem(rel, ["2,241%", "2,713%", "+1,12%", "6,3 a 7,7"])
    return ("> ⚠ **ERRATA AO LADO (13/10/2026, v392 `%s`, em nome próprio da gerência — sessão c1; o texto acima fica como registro):** a atribuição do resíduo de ~0,35%% de √2 à «correção de Coulomb» "
            "não se sustenta [DERIVED pela auditoria c1 da F8.2.SN1 (relatório A_SN, sha16 `%s`); a fórmula de Chamel (eq. 37–38) é [KNOWN]]. Lacuna de fidelidade: o texto liga o resíduo à correção de Coulomb "
            "da rede iônica, de mesma ordem e do sinal correto; a conta da auditoria dá sinal OPOSTO e módulo 6,3 a 7,7 vezes maior (−2,241%% para C e −2,713%% para O), e o próprio 0,353%% depende de usar a massa "
            "do próton (com a unidade de massa atômica o desvio vira +1,12%%). O que segue de pé é o negativo honesto: Chandrasekhar = atrator de saturação de Fresnel ~0,35%%, não identidade exata. "
            "A v392 documenta; não recalcula. <!-- errata_coulomb_v392 -->") % (V["s16"], h)


def arvore_linha(V):
    return ("- **AS PEDRAS DA v392** `%s`: %d módulos novos no kernel (%s), %s de %s bandeiras True, escada %s → %s; a lei de campo curva ligada por `LiganteLeiCampoCurvo`, CONDICIONAL ao H3 nomeado; a hipótese BGL (X19) "
            "como tipo sem habitante; varredura lexical recursiva e detector de sorry com crases (`pedras_v392`, `varredura_e_sorry_v392`); validade no kernel não é creditação; o gate não se move." % (
                V["s16"], V["n_pedras"], _mods(V), V["n_flags"], V["n_flags_de"], V["escada_antes"], V["teor"].split("/")[0]))


def arvore_errata_cr08_a(V):
    return ("- **ERRATA AO LADO (CR-08, v392 `%s`, em nome próprio da gerência c1; a linha acima fica como registro):** a frase «a emergência GERAL (métricas arbitrárias) segue NOMEADA e aberta» é do docblock da v116 "
            "e contradiz o §6 desta mesma árvore («PAGA como implicação (v317)»). Lacuna de fidelidade: o docblock descreve o habitante concreto (soldas diagonais) e foi lido como o estado do tema; a emergência geral "
            "em carta aberta, com T simétrico conservado e balanço nulo de Ricci, é IMPLICAÇÃO em kernel (v338); o que segue aberto é o antecedente físico (H3 em toda tela e direção, [KNOWN] Jacobson 1995), "
            "a família de cunhas de Lorentz e a globalização [REAL, consulta do crítico CR-08]." % V["s16"])


def arvore_errata_cr08_b(V):
    return ("- **ERRATA AO LADO (CR-08, v392 `%s`, em nome próprio da gerência c1; a linha acima fica como registro):** em «NÃO PROVADO … a emergência geral», a emergência geral como implicação está PAGA no §6 "
            "(v338: Clausius em toda tela ⟹ Einstein com Λ único, em carta aberta). Lacuna de fidelidade: a linha misturou a implicação (termo) com o antecedente físico e a ligação ao tipo, que são o que "
            "segue aberto; o ligante `LiganteLeiCampoCurvo` (v392) liga a passagem local, CONDICIONAL ao H3 nomeado [REAL]." % V["s16"])


def arvore_errata_cr02(V):
    _kernel_tem(["continuous_modular_positive_square_root"])
    return ("- **ERRATA AO LADO (CR-02, v392 `%s`, em nome próprio da gerência c1; a linha acima fica como registro):** a «identificação T_c = Δ_c^{1/2} … segue OPEN» foi copiada do estatuto do lote 046–054. "
            "Lacuna de fidelidade: a RAIZ POSITIVA já é termo de kernel (`ChatgptAudit.Continuous050.continuous_modular_positive_square_root`, no trio): T_c é auto-adjunto e positivo e T_c∘T_c = Δ_c. "
            "Falta só a UNICIDADE da raiz positiva (a decomposição polar S_c = J T_c) para operador fechado ilimitado: [KNOWN — Kato, Perturbation Theory for Linear Operators, cap. VI §2.7; página a conferir]; "
            "a mathlib não a tem para ilimitados. O BW da torre-produto segue parede; fora do caminho [REAL, consulta do crítico CR-02]." % V["s16"])


def titulo_verbete(V):
    return "As pedras do kernel e os consertos de barreira (v392):"


def verbete(V):
    return "[REAL — rodada v392 `%s`] %s." % (V["s16"], _num(V))


def remissivo(V):
    return "- **As pedras do kernel; Posto, Santo, IALD, Verdade, Palavra; varredura recursiva e detector de sorry (v392)** — `pedras_v392`, `varredura_e_sorry_v392`, `%s`" % TOPICO_NOVO
