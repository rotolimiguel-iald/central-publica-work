# -*- coding: utf-8 -*-
"""_adapt_forkA_orquestrador_v409.py -- (claude-construtor-v409, fork A, 05/11/2026) adapta orquestrador/pos_treino_v409.py (subida mecanica da v408) a v409 (DESENHO_v409 §6, D57):
a ORDEM desta versao (05/11, «Prossigamos para a próxima verão do um.py; concordo com todos os nomes que foram dados»; o sha16 e a frase LIDOS de delta_v409, nunca digitados, e conferidos contra o arquivo);
SEM o S7 (G1 --publicar) e SEM o S10 (release do app): o fim da cadeia e' o HANDOFF (D57a; a custodia completa e o release do app sao da sessao de custodia, pela divisao de 04/11);
o S6d roda pos_rito/textos_custodia_handoff_v409.py e DEPOIS o portao do G1 (custodia_g1.textos.portao) e a D59 sobre o HANDOFF INTEIRO (o do Nos e o da memoria);
--ensaio sem o S10 (so' o plano); S1b com a D58; os tempos do S4. Trocas com contagem exata (_adapt_util_v409.Arq)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

a = Arq("orquestrador/pos_treino_v409.py")
ls = a.t.split("\n")
assert ls[1].startswith("# [A ADAPTAR v409]") and ls[2].startswith("# [ADAPTADO v409, 04/11/2026, claude-construtor-v409 (fork C)]")
ls[1] = ("# [ADAPTADO v409, 05/11/2026, claude-construtor-v409 (fork A), a servico da gerencia c1] molde: pos_treino_v408.py FINAL (a subida mecanica fica em bump/); por _adapt_forkA_orquestrador_v409.py: a ORDEM da v409 (05/11; sha16 e frase lidos de delta_v409 e conferidos contra o arquivo) como AUT; "
         "SEM S7 e SEM S10 (D57: o fim da cadeia e' o HANDOFF; a custodia completa e o release do app sao da sessao de custodia); o S6d roda os textos da custodia e o portao do G1 sobre o handoff inteiro; a gerencia lanca (nao rodou).")
del ls[2]
a.t = "\n".join(ls)

# ---------------------------------------------------------------- o docstring
a.troca_re(r'^"""pos_treino_v409\.py — O ORQUESTRADOR DA v409 \(claude-construtor-v409, a serviço da gerência c1, 04/11/2026; molde: o orquestrador pós-treino da v408\)\. Ordem do operador DESTA versão \(04/11/2026, verbatim sha16 685b8d8bcf0ddbbd\):\n«liste as pedras[^\n]*$',
           '"""pos_treino_v409.py — O ORQUESTRADOR DA v409 (claude-construtor-v409, a serviço da gerência c1, 05/11/2026; molde: o orquestrador pós-treino da v408). Ordem do operador DESTA versão (05/11/2026; o sha16 e a frase são LIDOS de delta_v409 e conferidos contra o arquivo):\n'
           '«Prossigamos para a próxima verão do um.py; concordo com todos os nomes que foram dados». O fim da cadeia é o HANDOFF (D57a): a custódia completa (site, repositórios, links, dispositivos, Central, commit e push) e o release do app são da sessão de custódia, pela divisão de 04/11.', flags=0x8)
a.troca("  S1b exige a revisão de terceiro APROVADA sobre ESTE candidato (revisao_terceiro/REVISAO_TERCEIRO_v409.json; revisor: Sonnet, D54, até três rodadas)", "  S1b exige a revisão de terceiro APROVADA sobre ESTE candidato (revisao_terceiro/REVISAO_TERCEIRO_v409.json; revisor: Sonnet, D58, até três rodadas)")
a.troca("Só 4 módulos novos compilam a frio (o tempo do sandbox é lido de kernel/construir_marcas.txt; o rito da v408, com 9, é lido de v408/rito_horarios_v408.txt; teto aqui: 5 h).",
        "Só 1 módulo novo compila a frio (o tempo do sandbox é lido de kernel/construir_marcas.txt; o rito da v408, com 4, é lido de v408/rito_horarios_v408.txt; teto aqui: 5 h).")
a.troca("e ENTÃO S6d (D52): textos_custodia_handoff_v409.py ENCADEADO (os sete textos da custódia no handoff; rc 0 e o recibo), antes do S7.",
        "e ENTÃO S6d (D52, D57): textos_custodia_handoff_v409.py ENCADEADO (os sete textos da custódia no handoff; rc 0 e o recibo) e o portão do G1 (custodia_g1.textos.portao) e a D59 sobre o HANDOFF INTEIRO (o do Nós e o da memória). O handoff é o FIM da cadeia.")
a.troca_re(r"^  S7  custódia G1: planejar --seco, executar --publicar, auditar \(código 5 = só decisões do operador\)\.\n  S10 a ORDEM de release do app [^\n]*\n      \(RELATORIO ou RESULTADOS[^\n]*\n",
           "  (SEM S7 e SEM S10 nesta versão, D57: a custódia G1 com --publicar e a ORDEM de release do app são da sessão de custódia; as funções s7_g1 e s10_app ficam no arquivo como registro e NÃO são chamadas.)\n", flags=0x8)
a.troca("     python pos_treino_v409.py --ensaio   (a seco: o S10 contra um app SINTÉTICO — um caso positivo e controles negativos; não toca TUNEL_CLAUDE_APP, o app, o Nós nem ESTADO.json)",
        "     python pos_treino_v409.py --ensaio   (só leitura: o mesmo que --plano; o ensaio do S10 não roda, porque o S10 não é desta versão, D57)")
a.troca("(a decisão de restaurar é da gerência), não grava pensamento do dia (X_TEXTO = None).", "(a decisão de restaurar é da gerência), não grava pensamento do dia (X_TEXTO = None), não publica, não faz commit nem push, não escreve ordem ao app (D57).")

# ---------------------------------------------------------------- a ORDEM e o AUT (lidos de delta_v409)
a.troca('ORDEM = CEN / "work" / "cunhagens_13out" / "OPERADOR_04nov_ordem_v409_liste_as_pedras_produza_rode_handoff_custodia_completa_verbatim.txt"',
        'sys.path.insert(0, str(PK))\nimport delta_v409 as _DL  # noqa: E402   (o nome do arquivo da ordem, o sha16 pinado dela e a frase verbatim saem do delta: nada digitado aqui)\nORDEM = CEN / "work" / "cunhagens_13out" / _DL.N_ORDEM_V409')
a.troca_re(r'^AUT = \("Ordem do operador de 04/11/2026 \(verbatim sha16 685b8d8bcf0ddbbd\):[^\n]*\n[^\n]*\n[^\n]*\)\nAUT_FRASE = "liste as pedras[^\n]*$',
           'AUT_FRASE = _DL.FRASE_ORDEM_V409   # a frase da ordem (verbatim, do delta): tem de estar no ARQUIVO (conferido por _conferir_ordem) e e\' o que os recibos da Bancada recebem no AUT\n'
           'AUT = ("Ordem do operador de 05/11/2026 (verbatim sha16 %s): «%s» (a ordem da v409, que ratifica os nomes dados pela gerência). "\n'
           '       "D57 (gerência c1, em nome próprio, 05/11): o fim da cadeia do orquestrador é o HANDOFF; a sincronização da Bancada Um (parada e religamento do serviço da porta 18777, o B(n) da versão) segue o rito da casa como na v408; "\n'
           '       "a custódia completa e o release do app são da sessão de custódia." % (_DL.VERBATIM_PREFIXOS_DA_ORDEM_V409[_DL.N_ORDEM_V409], AUT_FRASE))', flags=0x8)
a.troca('    """fail-closed: o arquivo da ordem existe, o sha16 LIDO dele esta no AUT (o texto do AUT nao vale por si) e a frase do AUT esta no arquivo; senao o orquestrador nao age."""\n'
        '    assert ORDEM.exists(), "falta o verbatim da ordem do operador: %s" % ORDEM\n'
        '    s = sha16(ORDEM); txt = ORDEM.read_text(encoding="utf-8")\n',
        '    """fail-closed: o arquivo da ordem existe, o sha16 LIDO dele e\' o pinado em delta_v409 e esta no AUT (o texto do AUT nao vale por si) e a frase do AUT esta no arquivo; senao o orquestrador nao age."""\n'
        '    assert ORDEM.exists(), "falta o verbatim da ordem do operador: %s" % ORDEM\n'
        '    s = sha16(ORDEM); txt = ORDEM.read_text(encoding="utf-8")\n'
        '    assert s == _DL.VERBATIM_PREFIXOS_DA_ORDEM_V409[_DL.N_ORDEM_V409], ("o sha16 do arquivo da ordem != o pinado em delta_v409", s)\n')

# ---------------------------------------------------------------- S4: os tempos
a.troca("4 módulos novos a frio: no sandbox k409c o build levou %s s e o Audit %s s [kernel/construir_marcas.txt]; o rito da v408, com 9, levou %s [v408/rito_horarios_v408.txt]; teto 5 h)",
        "1 módulo novo a frio: no sandbox k409c o build levou %s s e o Audit %s s [kernel/construir_marcas.txt]; o rito da v408, com 4, levou %s [v408/rito_horarios_v408.txt]; teto 5 h)")

# ---------------------------------------------------------------- S6d: os textos da custodia e o portao do G1 sobre o handoff inteiro
a.troca('    """S6d (D52, lição da v408): os sete textos da custódia entram ENCADEADOS, depois da chain 14 e antes do S7: pos_rito/textos_custodia_handoff_v409.py (rc 0 e o recibo RECIBO_TEXTOS_CUSTODIA_HANDOFF_v409.json ao lado); sem isso o G1 planejar --seco parava em rc 20 na v408."""',
        '    """S6d (D52, D57): os sete textos da custódia entram ENCADEADOS, depois da chain 14: pos_rito/textos_custodia_handoff_v409.py (rc 0 e o recibo RECIBO_TEXTOS_CUSTODIA_HANDOFF_v409.json ao lado); DEPOIS, o portão do G1 (custodia_g1.textos.portao)\n'
        '    e a D59 sobre o HANDOFF INTEIRO (Nós\\\\HANDOFF_v409_CUSTODIA.md e memory\\\\handoff-v409-custodia.md; os hashes conhecidos são os do próprio texto). O handoff é o FIM da cadeia desta versão (sem S7 e sem S10)."""')
a.troca('glob("textos_custodia_handoff_v408*.py")', 'glob("textos_custodia_handoff_v409*.py")', n=2)
a.troca('motivo="esperava UM pos_rito/textos_custodia_handoff_v408*.py (sufixo .py)"', 'motivo="esperava UM pos_rito/textos_custodia_handoff_v409*.py (sufixo .py)"')
a.troca('faltam.append(str(PK / "pos_rito" / "textos_custodia_handoff_v408*.py") + " (S6d, D52: exatamente um, sufixo .py)")', 'faltam.append(str(PK / "pos_rito" / "textos_custodia_handoff_v409*.py") + " (S6d, D52: exatamente um, sufixo .py)")')
a.troca('    ok = rc == 0 and rec.exists()\n    marcar(e, "S6d_textos_custodia", ok, rc=rc, script=cands[0].name, recibo=(rec.name if rec.exists() else None))\n    return ok\n',
        '    ok = rc == 0 and rec.exists()\n'
        '    if not ok:\n'
        '        marcar(e, "S6d_textos_custodia", False, rc=rc, script=cands[0].name, recibo=(rec.name if rec.exists() else None)); return False\n'
        '    viol = {}\n'
        '    try:\n'
        '        sys.path.insert(0, str(CEN / "tools"))\n'
        '        from custodia_g1 import textos as _TXG1   # o portão do G1 (a mesma função que a custódia usa)\n'
        '        for hp in (NOS / "HANDOFF_v409_CUSTODIA.md", UMEM / "handoff-v409-custodia.md"):\n'
        '            if not hp.exists():\n'
        '                viol[hp.name] = ["o handoff não existe"]; continue\n'
        '            ht = hp.read_text(encoding="utf-8")\n'
        '            conh = set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{16}(?![0-9a-fA-F])", ht)) | set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{64}(?![0-9a-fA-F])", ht))\n'
        '            v_ = list(_TXG1.portao(ht, conh, rotulo=hp.name))\n'
        '            if re.search(r"(?i)kimi|mil[eê]nio|millennium|navier|lindão", ht):\n'
        '                v_.append("D59: o handoff traz o que fica fora dos textos")\n'
        '            if v_:\n'
        '                viol[hp.name] = v_[:5]\n'
        '    except Exception:  # noqa: BLE001\n'
        '        viol["erro"] = [traceback.format_exc()[-600:]]\n'
        '    ok = not viol\n'
        '    marcar(e, "S6d_textos_custodia", ok, rc=rc, script=cands[0].name, recibo=rec.name, portao_g1_handoff_inteiro=(viol or "limpo"), fim_da_cadeia="HANDOFF (D57)")\n'
        '    if ok:\n'
        '        log("S6d: o handoff passou no portão do G1 e na D59; FIM DA CADEIA (D57): a custódia completa e o release do app são da sessão de custódia")\n'
        '    return ok\n')
a.troca('UMEM_ = None' if False else 'TUNEL_APP = Path(r"C:\\IALD\\TUNEL_CLAUDE_APP")', 'UMEM = Path(r"C:\\Users\\rotol\\.claude\\projects\\c--IALD-Central-de-Patentes\\memory")   # o handoff da memória (o fechar o grava; o S6d o passa pelo portão)\nTUNEL_APP = Path(r"C:\\IALD\\TUNEL_CLAUDE_APP")')

# ---------------------------------------------------------------- o plano e o main: sem S7 e sem S10
a.troca('"S6c_chain_10c_14", "S6d_textos_custodia", "S7_g1", "S10_app", "S8_nativa"]', '"S6c_chain_10c_14", "S6d_textos_custodia", "S8_nativa"]   # (D57: sem S7_g1 e sem S10_app nesta versao)')
a.troca(', TEMPLATE_ORDEM, PK / "um_v409_candidato.py"', ', PK / "um_v409_candidato.py"')
a.troca("        for passo in (s0_treino, s1_prep, s1b_revisao, s2_prevoo, s3_instalar, s4_rito, s5_cadeia_0_10, s6_bancada, s7_g1, s10_app, s8_nativa):",
        "        for passo in (s0_treino, s1_prep, s1b_revisao, s2_prevoo, s3_instalar, s4_rito, s5_cadeia_0_10, s6_bancada, s8_nativa):   # D57: o fim da cadeia e' o HANDOFF (S6d); sem s7_g1 e sem s10_app")
a.troca('    if "--ensaio" in sys.argv:\n        _plano()\n        sys.exit(0 if _ensaio_s10() else 1)\n',
        '    if "--ensaio" in sys.argv:   # D57: o S10 nao e\' desta versao; o ensaio e\' so\' o plano (so\' leitura)\n        sys.exit(0 if _plano() else 1)\n')
a.grava()
