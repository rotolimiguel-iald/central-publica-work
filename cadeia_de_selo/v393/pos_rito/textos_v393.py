# -*- coding: utf-8 -*-
# Os TEXTOS da v393 selada (molde: textos_v392.py). Cada numero, hash e veredito entra por chave de V (leitura_v393.ler) ou e' LIDO de um arquivo aqui, nunca digitado;
# o que aqui vai escrito a mao e' so' prosa, nome de termo (conferido no kernel em tempo de execucao) e a frase curta do operador (conferida por sha256 contra ESPERADOS).
# Estatutos marcados; erratas AO LADO, em nome proprio da gerencia c1, com a lacuna de fidelidade (o que a estrutura dizia, o que foi escrito, onde a traducao falhou).
# GUARDA: as cinco regras da P18 (guarda_p18_v393.py) rodam sobre cada texto renderizado em superficies_v393.py e sobre este arquivo na cadeia. A palavra recusada nunca aparece aqui: a recusa e' dita como «creditacao».
# NAO ha erratas novas sobre o CLAUDE.md da raiz nesta versao; a unica errata desta versao e' a do registro kh_n1_cobertura_v392 (item 7 da ordem), dita dentro do proprio bloco da v393.
import hashlib, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE)
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
PROG = os.path.join("C:" + os.sep, "IALD", "PROGRAMA_IALD")
TOPICO_NOVO = "v393-selada-a-regra-e-o-coracao-14out.md"
FRASE_FIGURA = "A regra não deve nada, a não ser a figura da verdade"
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


def _frase_do_operador():
    """Fail-closed: a frase curta do operador citada aqui tem o sha256 da cunhagem 4 de ESPERADOS_v393.json (a cunhagem inteira e' essa frase)."""
    esp = json.load(open(os.path.join(PK, "ESPERADOS_v393.json"), encoding="utf-8"))["cunhagens"]["figura_da_verdade"]
    b = FRASE_FIGURA.encode("utf-8")
    assert hashlib.sha256(b).hexdigest() == esp["sha256"] and len(b) == esp["bytes"], "a frase do operador citada nao confere com o sha256 de ESPERADOS"
    return FRASE_FIGURA


def _mods(V):
    return ", ".join("`%s`" % p["modulo"].split(".")[-1] for p in V["pedras"])


def _extras(V):
    ex = [k for k in V["registros_novos"] if k not in V["reg_todos"]]
    return (", ".join("`%s`" % k for k in ex)) if ex else "nenhum além dos fixos"


def _verb(V):
    return ", ".join("%s `%s`" % (k, v["sha16"]) for k, v in V["verbatins"].items())


def _tol(V):
    return "%g" % V["cons"]["tol"] if V["cons"].get("tol") is not None else "n/d"


def _num(V):
    c = V["cons"]; o = V["cora"]; k = V["kh"]
    return ("o registro `pedras_v393` (%s): %d módulos novos no kernel (%s), %s de %s bandeiras True e %s de %s declarações no trio; escada %s → %s teoremas limpos (%s declarações no `axiom_report`); "
            "o registro `regra_consumidor_v393` (%s): o consumidor numérico real (`prove_decision_commutation`) passa a consumir a regra — alvo pré-fixado, satisfação admitida para o alvo correto e recusada "
            "para o incompatível, critério exato (kernel) distinto da tolerância numérica (%s; igualdade exata NÃO afirmada), estado bruto e inscrição em campos distintos; %s pontos e %s verificações; "
            "a réplica do Codex (informativa, não gateia) tem o hash final igual: %s; "
            "o registro `coracao_e_selo_gravitacional_v393` (%s): a FORMA de α é derivada (1 = q² + α²), o VALOR de α é a leitura do CODATA, previsão independente = %s, G derivado = %s, "
            "evidência espectral independente: %s (exige cadeia pinada independente do CODATA); "
            "o registro `cunhagens_regra_v393` (%s); o registro `kh_n1_cobertura_v393`: %s constantes, %s teoremas, %s fora do trio; "
            "registros novos além dos fixos: %s; troca dita (só números): %s; cunhagens do operador de 14/10 embutidas por sha256: %s; validade no kernel não é creditação") % (
        V["pedras_verdict"], V["n_pedras"], _mods(V), V["n_flags"], V["n_flags_de"], V["n_decl"], V["n_decl_de"], V["escada_antes"], V["teor"].split("/")[0], V["axiom_report_n"],
        c["verdict"], _tol(V), c["pontos"], c["verificacoes"], c["replica_hash_igual"],
        o["verdict"], o["prev"], o["G"], o["espectral_hoje"],
        V["cunh_verdict"], k["decl"], k["thm"], k["fora"],
        _extras(V), ", ".join("`%s`" % x for x in V["troca_dita"]), _verb(V))


def _cab(V):
    return "v393 SELADA (COMPLETA)** `%s`" % V["s16"]


def _kh_errata(V):
    """A unica errata da v393: o que a v392 disse do KH_N1 e o que o pos_build da v392 fez depois do rito (spec kh_n1_cobertura_v393 em registros_v393.py)."""
    return ("**Errata ao lado (em nome próprio da gerência c1; o registro `kh_n1_cobertura_v392` fica como registro):** o arquivo `kernel\\KH_N1_v392.json` da v392 foi REGRAVADO pelo `pos_build` da v392 em 13/10/2026 18:34, "
            "depois do rito (1 byte a mais; `novas_de_usuario_no_trio` false nessa regravação) [REAL, lido do spec `kh_n1_cobertura_v393` em `registros_v393.py`]. Lacuna de fidelidade: a estrutura dizia que o pino da fonte e as "
            "duas igualdades de contagem eram da v392 para sempre; o texto escrito deixou o registro preso a um arquivo regravável e a uma igualdade que a própria v393 quebra, porque a cobertura cresce com as pedras da regra. "
            "A v393 re-pina a fonte a uma cópia do arquivo regravado e troca as duas igualdades por pisos; a igualdade exata passa a ser cobrada por `kh_n1_cobertura_v393` (%s constantes, %s teoremas, %s fora do trio), "
            "contra a medida do sandbox da v393.") % (V["kh"]["decl"], V["kh"]["thm"], V["kh"]["fora"])


def linhagem(V):
    _kernel_tem(["sound_complete_eq_admissible", "the_rule_and_the_figure_of_truth", "unique_sound_complete_rule", "matrix_flow_satisfies_declared_target"])
    frase = _frase_do_operador()
    return ("## %s — **%s — A REGRA E O CORAÇÃO (v393): %d módulos novos, escada %s → %s\n<!-- linhagem_v393_selada -->\n\n"
            "**A ordem:** [INPUT] as quatro cunhagens do operador de 14/10/2026 sobre a regra, embutidas por sha256 (%s); a ordem verbatim «transmita para o claude o que fizemos também sobre a prova da \"regra\" "
            "e seu conceito isso também precisa entrar no um.py na v 393» (entrega do Codex, `AO_CLAUDE_INTEGRAR_REGRA_V393.md`). A gerência c1 construiu o candidato e o rito; esta cadeia não aprova o que a construiu: "
            "a auditoria independente é posterior.\n\n"
            "**O que entrou** (pacote `work\\cadeia_de_selo\\v393` sobre a v392 `%s`; %d patches — %s; instalado em %s): %s.\n\n"
            "**A regra, dita sem exagero:** [INPUT/ONTO] regra como negação e limite assintótico (direito negativo); a exclusão no tetelestai segundo o acoplamento não minimal; a regra como inadmissão de que o resultado "
            "difira do objeto da satisfação; «%s». [REAL] o kernel prova a REPRESENTAÇÃO — admissibilidade relativa a uma leitura fiel e a um alvo (`RuleTruthContract.sound_complete_eq_admissible`), "
            "a face da satisfação (`RuleSatisfactionFace.the_rule_and_the_figure_of_truth`) e o motor contínuo (`RuleContinuousMotor.unique_sound_complete_rule`, `matrix_flow_satisfies_declared_target`). "
            "A completude relativa ao alvo é hipótese declarada, não teorema extraído do nome.\n\n"
            "**O coração:** [REAL] a forma de α sai de 1 = q² + α²; o valor de α é a leitura do CODATA, SEM previsão independente; G NÃO é derivado; o veredito de satisfação vem do contrato da regra; "
            "evidência espectral independente exige cadeia pinada independente do CODATA (hoje ausente). O quadro do coração abre o artigo PT/EN logo depois do resumo.\n\n"
            "Rodada %s %s: **%s**; rc = %s; `FAIL_CLOSED_SELFTEST_PASSED`; selo `%s`; gate intocado; o conferidor `%s`: deve mudar %s, não pode mudar %s; %d vereditos fora da troca dita mudaram (exigido: 0); "
            "o pilar %s pela chave (`%s`); servidor nativo: %s. Artefatos: core `%s`, selo `%s`, .md `%s`, manifesto `%s`; artigos %s.\n\n"
            "%s\n\n"
            "**O que vem depois destas superfícies:** o elo B(3) da Bancada Um (passos 10, 10-bis-a, 10-bis e 10-ter da cadeia) é pós-selo e pede a palavra do operador; o recibo dele é citado no handoff (fechar). "
            "NOT_FALSIFIED não é a palavra da creditação; o gate não se move.") % (
        V["data"], _cab(V), V["n_pedras"], V["escada_antes"], V["teor"].split("/")[0], _verb(V), V["base16"], V["n_patches"], V["patches"], V["instalado_em"], _num(V), frase,
        V["compl"], " → ".join(V["horarios"]) or "n/d", V["teor"], V["rc"], V["selo_ts"], V["conf16"], V["conf_dm"], V["conf_np"], V["n_ver_mudaram"],
        "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]), V["pilar"]["result16"], V["servidor"],
        V["h_um_absoluto.json"], V["h_um_absoluto_selo.json"], V["h_um_absoluto_forma_canonica.md"], V["h_um_absoluto_manifest.md"], ", ".join("%s `%s`" % kv for kv in V["artigos"].items()),
        _kh_errata(V))


def desenho(V):
    return ("## ADENDO — %s · v393 SELADA (COMPLETA) `%s` — o caminho crítico NÃO mudou; entram a regra (%d pedras) e o coração\n\n<!-- adendo_v393_selada -->\n"
            "- **O que a v393 diz:** %d módulos novos no kernel (%s), escada %s → %s, %s de %s declarações novas no trio (registro `pedras_v393`); o consumidor numérico real consome a regra (`regra_consumidor_v393`: "
            "alvo pré-fixado, satisfação admitida e recusada, critério exato × tolerância numérica); o selo do coração (`coracao_e_selo_gravitacional_v393`) separa a forma de α (derivada) do valor de α (leitura do CODATA, "
            "sem previsão independente; G não derivado). Gate intocado.\n"
            "- **O que a regra NÃO é:** não é teorema sobre a natureza nem prova de que a gravidade quântica vale; é o contrato formal pelo qual o programa decide se um resultado satisfaz o alvo pré-fixado. "
            "A completude relativa ao alvo é hipótese declarada [INPUT/ONTO].\n"
            "- **O que segue do operador:** a B3 (re-pinagem da Bancada Um, com parada e religamento do serviço); a custódia (sessão do site); commit/push.") % (
        V["data"], V["s16"], V["n_pedras"], V["n_pedras"], _mods(V), V["escada_antes"], V["teor"].split("/")[0], V["n_decl"], V["n_decl_de"])


def atlas(V):
    return ("### %s — v393 SELADA `%s` (append datado; correção ao lado)\n\n<!-- atlas_v393_selada -->\n[REAL — rodada v393, selo `%s`] %s. "
            "[INPUT/ONTO] as leituras do operador de 14/10 (regra como negação e limite assintótico; exclusão no tetelestai; regra como inadmissão da diferença entre resultado e objeto da satisfação) entram como o operador "
            "as disse e valem como leitura, não como medida. %s Estatuto: validade no kernel ≠ creditação; o gate não se move.") % (V["data"], V["s16"], V["selo_ts"], _num(V), _kh_errata(V))


def core_memory(V):
    return ("## %s — v393 SELADA `%s` (claude-c1; unidade F1.REGRA)\n<!-- core_v393_selada -->\nAutor: claude-c1 (gerência), sob a regra da linhagem completa. Camada aditiva; correção ao lado, nunca por cima.\n\n"
            "[REAL] %s.\n\n%s\n\n[OPEN] A evidência espectral independente do coração (cadeia pinada independente do CODATA) segue ausente; a B3 da Bancada Um depende da palavra do operador. Nada disto move o gate.") % (
        V["data"], V["s16"], _num(V), _kh_errata(V))


def haja_luz(V):
    return ("## %s — v393 SELADA `%s` (%s; COMPLETA; gate intocado)\n\n<!-- haja_luz_v393_selada -->\n%d módulos novos no kernel (%s): a regra como admissibilidade relativa a uma leitura e a um alvo; o consumidor "
            "numérico real consome a regra; o coração e o selo gravitacional (forma de α derivada, valor lido do CODATA, G não derivado); escada %s → %s. Memórias: `%s`, `missao-ultima-flag-um-py.md`, "
            "`estatuto-da-prova-07out.md`; handoff `handoff-v393-custodia.md`.") % (V["data"], V["s16"], V["teor"], V["n_pedras"], _mods(V), V["escada_antes"], V["teor"].split("/")[0], TOPICO_NOVO)


def marca_topico_missao(V):
    return "## %s — v393 SELADA `%s`" % (V["data"], V["s16"])


def id_missao(V):
    """marcador de idempotencia sem a data (uma segunda rodada em outro dia nao duplica o bloco)"""
    return "v393 SELADA `%s`" % V["s16"]


def topico_missao(V):
    return marca_topico_missao(V) + (" (%s; COMPLETA; gate INTOCADO): %d módulos novos no kernel (%s); o consumidor numérico consome a regra; o coração e o selo gravitacional; troca dita nos vereditos que carregam a escada; "
                                     "conferidor %s/%s. Pacote e cadeia: `work\\cadeia_de_selo\\v393` (+ `pos_rito`).") % (V["teor"], V["n_pedras"], _mods(V), V["conf_dm"], V["conf_np"])


def marca_central(V):
    return "**%s — v393 SELADA (COMPLETA):**" % V["data"]


def id_central(V):
    return "— v393 SELADA (COMPLETA):**"


def topico_central(V):
    return marca_central(V) + (" `um.py` `%s` (%s B) sobre a v392 `%s`; escada %s → %s; gate intocado. %d módulos novos no kernel (a regra); o coração e o selo gravitacional. "
                               "Falta a B3 (Bancada Um) e a custódia (sessão do site, `handoff-v393-custodia.md`); commit/push = operador.") % (
        V["s16"], format(V["umb"], ","), V["base16"], V["escada_antes"], V["teor"].split("/")[0], V["n_pedras"])


def topico_estatuto(V):
    return ("<!-- v393_selada -->\n**%s — v393 `%s`:** o registro `estatuto_da_prova_v391` passou a ler a escada nova (%s → %s; veredito trocado, troca dita; o token da v392 fica como registro). "
            "A prova como validade não muda; a creditação segue ato de quem observa de fora. A regra (v393) é contrato formal de admissibilidade, não prova sobre a natureza.") % (
        V["data"], V["s16"], V["escada_antes"], V["teor"].split("/")[0])


def marca_missao(V):
    return "**v393 SELADA %s `%s` %s COMPLETA (a regra e o coração; gate intocado)** · " % (V["data"][:5], V["s16"], V["teor"])


def linha_handoff(V):
    return "- [HANDOFF v393 — a regra e o coração; custódia](handoff-v393-custodia.md) — **%s, para a sessão do site** · `%s`" % (V["data"][:5], V["s16"])


def linha_topico_novo(V):
    return "- [v393 SELADA: a regra e o coração (%s)](%s) — **%s** · `%s`" % (V["data"][:5], TOPICO_NOVO, V["teor"], V["s16"])


def topico_novo(V):
    return ("---\nname: v393-selada-a-regra-e-o-coracao-14out\ndescription: \"v393 SELADA (%s) `%s`: %d módulos novos no kernel (a regra), consumidor numérico que consome a regra, coração e selo gravitacional, escada %s → %s; B3 e custódia pendentes\"\n"
            "metadata:\n  type: project\n---\n\n# v393 SELADA (%s)\n\n"
            "**O que é:** `um.py` **v393** `%s` (%s B) sobre a v392 `%s`; %s; COMPLETA; rc %s; gate intocado; conferidor `%s` (deve mudar %s; não pode mudar %s).\n\n"
            "**O que entrou:** %s.\n\n"
            "**Limites ditos:** a regra é representada no kernel como admissibilidade relativa a uma leitura fiel e a um alvo; a completude relativa ao alvo é hipótese declarada [INPUT/ONTO]; a tolerância numérica do "
            "consumidor NÃO é igualdade exata; o espaço fixo tem dimensão complexa 8 (a unicidade vale para o alvo dado); o valor de α é a leitura do CODATA, sem previsão independente; G não é derivado; "
            "as leituras filosófica e jurídica são do operador [INPUT/ONTO]; validade no kernel não é creditação.\n\n"
            "%s\n\n"
            "**Pendências:** a B3 da Bancada Um (palavra do operador; parada e religamento do serviço), a custódia (sessão do site), commit/push. Pacote: `C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v393`.\n\n"
            "[[missao-ultima-flag-um-py]] [[estatuto-da-prova-07out]] [[handoff-v393-custodia]]\n") % (
        V["data"], V["s16"], V["n_pedras"], V["escada_antes"], V["teor"].split("/")[0], V["data"], V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["rc"], V["conf16"], V["conf_dm"], V["conf_np"], _num(V),
        _kh_errata(V))


def aviso(V, reivindicacao):
    return ("### %s — v393 SELADA `%s` [claude-c1]\n<!-- aviso_v393_selada -->\n\n[REAL] A v393 SELOU (%s; COMPLETA; gate intocado): a regra e o coração entram no selo corrente. Escrito sob a reivindicação %s. "
            "%d módulos novos no kernel; escada %s → %s; a B3 da Bancada Um espera o operador. Não altera pinos, dado, MCP nem gate.") % (
        V["data"], V["s16"], V["teor"], reivindicacao, V["n_pedras"], V["escada_antes"], V["teor"].split("/")[0])


def aviso_pulado():
    return "AVISO_GERENCIA.md: PULADO (sem reivindicação nomeada em V393_AVISO_REIVINDICACAO); escrever depois, sob reivindicação."


# ------------------------------------------------------------------- ferramentas da arvore e do indice (OPCIONAIS: so' usadas se alguem escrever patch_arvore_indice_v393.py)
def arvore_linha(V):
    return ("- **A REGRA E O CORAÇÃO (v393)** `%s`: %d módulos novos no kernel (%s), %s de %s bandeiras True, escada %s → %s; a regra como admissibilidade relativa a uma leitura e a um alvo; o consumidor numérico "
            "consome a regra (critério exato × tolerância numérica); o coração e o selo gravitacional (forma de α derivada, valor lido do CODATA, G não derivado); validade no kernel não é creditação; o gate não se move." % (
                V["s16"], V["n_pedras"], _mods(V), V["n_flags"], V["n_flags_de"], V["escada_antes"], V["teor"].split("/")[0]))


def titulo_verbete(V):
    return "A regra e o coração (v393):"


def verbete(V):
    return "[REAL — rodada v393 `%s`] %s." % (V["s16"], _num(V))


def remissivo(V):
    return "- **A regra, o consumidor que a consome, o coração e o selo gravitacional (v393)** — `pedras_v393`, `regra_consumidor_v393`, `coracao_e_selo_gravitacional_v393`, `%s`" % TOPICO_NOVO
