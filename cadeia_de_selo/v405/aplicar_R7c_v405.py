# -*- coding: utf-8 -*-
"""aplicar_R7c_v405.py -- a errata R7 nos insumos, no relatorio e no fecho (uso unico). Nao toca nada que entre no candidato, salvo a copia do recibo. Backup de BYTES (.bak_<ts>_R7c); temporario -> conferir -> os.replace; cada ancora exatamente 1x."""
import os, time

HERE = os.path.dirname(os.path.abspath(__file__))
TS = time.strftime("%Y%m%d_%H%M%S")


def patch(nome, subs, troca_tudo=()):
    p = os.path.join(HERE, nome)
    b = open(p, "rb").read()
    s = b.decode("utf-8")
    for a, c in subs:
        n = s.count(a)
        assert n == 1, (nome, n, a[:120])
        s = s.replace(a, c)
    for a, c, k in troca_tudo:
        n = s.count(a)
        assert n == k, (nome, n, k, a[:120])
        s = s.replace(a, c)
    open(p + ".bak_" + TS + "_R7c", "wb").write(b)
    t = p + ".tmp_R7c"
    open(t, "wb").write(s.encode("utf-8"))
    assert open(t, "rb").read() == s.encode("utf-8")
    os.replace(t, p)
    print("ok", nome, len(subs) + len(troca_tudo))


patch("copiar_insumos_v405.py", [
    ("(os.path.basename(RG.RECIBO_ERRATA_R6_ARQ), RG.RECIBO_ERRATA_R6_ARQ),", "(os.path.basename(RG.RECIBO_ERRATA_R6_ARQ), RG.RECIBO_ERRATA_R6_ARQ), (os.path.basename(RG.RECIBO_ERRATA_R7_ARQ), RG.RECIBO_ERRATA_R7_ARQ),"),
])

_LINHAS_R7 = '''| R7, achado 1 (ALTO, o homônimo do gap) | o gap espectral do lock é 1, na unidade posta `u`, o `E₀` da Lei do Diminuto, e a tônica fica meio-tom acima dele; `Δ = β · u` é o valor esperado do lock no ângulo de Miguel, a energia retida, e não é gap (1/β vezes menor). Registro, artigos PT/EN, moldura e parágrafo público corrigidos; o nome do registro e o título O GAP ficam; que o ângulo de Miguel seja o sistema do gap com unidade é leitura [ONTO] dele (leitura 15, nova); check x11 novo, `x_h` e `x_i` no registro |
| R7, achado 2 (o lock em Hilbert) | os lemas do lock saem [REAL] em qualquer espaço de Hilbert; `HminMic` é instância (`HminMic_e_o_lock`), condicional a um `FockCertificate` que o kernel não habita: o registro lê `psibit_v395.conditional_psion_face.inhabitant_exhibited` = falso (check `x_i`) |
| R7, achado 3 (a inscrição e a medida) | [REAL] os dois teoremas existem; [ONTO, da gerência] lê-los como a forma da fala do operador; homônimo dito: `alphaKappa` não é a α de estrutura fina, e κ ali não é o relógio; gradiente negativo em κ > 0; a palavra cauda não está no teorema |
| R7, achado 4 (o tom) | [REAL] as notas sustentadas e as razões entre elas ficam; [INPUT] o tom fica, na fala dele: o kernel não tem termo para o tom |
| R7, achado 5 (stealth) | origem conferida: é derivação da própria teoria, condicional (`prove_ga_mass_audit`, v98: «[CONDICIONAL linear] M_TGL = M_RG», (P1)-(P4) + T1, Face C na ordem linear). A etiqueta passou de [KNOWN] a [DERIVED, condicional] no registro e nos textos. `RECLASSIFICACAO_GA_01nov.md` não tem o vício: não usa [KNOWN]; diz stealth sem etiqueta e sem a condição, e fica intacto |
| R7, BAIXOS | E10 e parágrafo público: «mais uma leitura do mesmo sen 45°»; x7 sem o número no `valor`, «como antecedente»; `gap_v405` no `__HEADER__`, em `topico_missao`, no remissivo e no cabeçalho de `rito_v405.sh`; `reverter_v405.py` com a guarda de -O e dizendo o que não restaura; «O que segue do operador» sem a revisão; a reescala «corresponde à» transposição; nomes `derivad-` ficam por decisão da gerência; checks tautológicos ficam, descritos como tal (g1, p6, d6, x7, x10) |
| R7, guarda | F13 recusa `Δ`, a energia retida ou 12,03 meV chamados de gap, em PT, EN e token; F14 recusa «a escala e o tom ficam»; as duas com controle negativo |
'''
patch("gerar_relatorio_v405.py", [
    ('''    "o COAUTOR do orquestrador diz Claude Fable 5.1, enquanto a atribuicao vigente desta sessao e' Claude Opus 5.5 (o orquestrador nao foi editado: a gerencia decide)",
''', ''),
    ('''    "checks tautologicos da revisao: enxuguei so' o du_ do g1 (comparava forma(57) com forma(57)); p6 e d6 ficam como estao, descritos como conferencia de identidade",
''', '''    "checks tautologicos: ficam, por decisao da gerencia, descritos como tal (g1, p6, d6, x7 e x10); so' o du_ do g1 saiu, porque comparava forma(57) com forma(57)",
'''),
    ('''    "os nomes de declaracao com derivad- (transicaoDerivada, leiDerivada, emprestimoDerivado, angulo_derivado_do_absoluto) ficam: a decisao e' da gerencia; as docstrings avisam",
''', '''    "os nomes de declaracao com derivad- (transicaoDerivada, leiDerivada, emprestimoDerivado, angulo_derivado_do_absoluto) ficam, por decisao da gerencia: as docstrings avisam",
    "tempoDoRetido como o tau* do sistema segue sem ratificacao do operador; a leitura 15 (o angulo de Miguel como o sistema do gap com unidade) tambem e' dele, nao teorema",
    "achado 5 da segunda revisao: a origem de stealth e' derivacao propria e condicional (prove_ga_mass_audit, v98); RECLASSIFICACAO_GA_01nov.md nao usa [KNOWN]: diz stealth sem etiqueta e sem a condicao, e ficou intacto",
    "BAIXO do instalar_v405.py (a janela minima: o recibo APLICADO so' e' gravado depois do os.replace) nao foi tocado: a revisao o deu por aceitavel e a ordem nao o pediu",
'''),
    ('''NAO_REVISADO = "este candidato (erratas R2 a R6) NAO foi revisado por terceiro: a revisao de 01/11 reprovou o anterior, a30f9f0ebf90c277, e a trava do orquestrador fica fechada ate uma nova revisao aprovar; aquela revisao nao examinou o pos-rito, instalar, reverter, rito, B(n) nem o servico da Bancada (quem constroi nao aprova)"''',
     '''NAO_REVISADO = "este candidato (erratas R2 a R7) NAO foi revisado por terceiro: a primeira revisao de 01/11 reprovou a30f9f0ebf90c277, a segunda reprovou eaefcd095abbaee7, e a trava do orquestrador fica fechada ate uma nova revisao aprovar; a segunda revisao nao examinou leitura_v405, fechar, superficies, chain, registrar_mapa, harnesses nem o B(n) (quem constroi nao aprova)"'''),
    ('''ERRATA_R2 = {"revisao_anterior": {"candidato": "a30f9f0ebf90c277", "veredito": "NAO APROVADA (2 ALTO, 11 MEDIO, 10 BAIXO)", "caderno": "revisao_terceiro/REVISAO_TERCEIRO_v405.md"},
''', '''ERRATA_R2 = {"revisao_anterior": {"candidato": "eaefcd095abbaee7", "veredito": "NAO APROVADA (1 ALTO, 4 MEDIO, 11 BAIXO)", "caderno": "revisao_terceiro/REVISAO_TERCEIRO_v405.md"}, "revisao_primeira": {"candidato": "a30f9f0ebf90c277", "veredito": "NAO APROVADA (2 ALTO, 11 MEDIO, 10 BAIXO)", "caderno": "revisao_terceiro/REVISAO_TERCEIRO_v405_R1.md"},
'''),
    ('''"recibo_vigente_das_pedras": "RECIBO_ERRATA_PEDRAS_R6_01nov.json",''', '''"recibo_vigente_das_pedras": "RECIBO_ERRATA_PEDRAS_R7_01nov.json",'''),
    ('''RECIBO_ERRATA_PEDRAS_R6_01nov.json`, cadeia de custódia R6 → R5 → R4 → R3 → R2 → primeira errata)''', '''RECIBO_ERRATA_PEDRAS_R7_01nov.json`, cadeia de custódia R7 → R6 → R5 → R4 → R3 → R2 → primeira errata)'''),
    ("## 1b. As erratas R2 a R6 (a revisão de terceiro não aprovou `a30f9f0ebf90c277`)", "## 1b. As erratas R2 a R7 (a primeira revisão de terceiro não aprovou `a30f9f0ebf90c277`; a segunda não aprovou `eaefcd095abbaee7`)"),
    ("e a guarda desta preparação pegou uma docstring da Tônica (`..._R6_01nov.json`, a referência vigente); o resto foi refeito aqui,", "a guarda desta preparação pegou uma docstring da Tônica (`..._R6_01nov.json`); e a segunda revisão, 1 ALTO, 4 MÉDIO e 11 BAIXO, mudou três (`..._R7_01nov.json`, a referência vigente: `gap` virou `retidoNoAngulo`); o resto foi refeito aqui,"),
    ("| guarda | F6 (a frase do no-go),", _LINHAS_R7 + "| guarda | F6 (a frase do no-go),"),
    ("registro novo, ao lado, com dez checagens em runtime: Δ, τ, Γ_B, Q,", "registro novo, ao lado, com onze checagens em runtime: Δ, τ, Γ_B, Q,"),
    ("`tempoDoGap` como τ★ é [ONTO], a ratificar", "`tempoDoRetido` como τ★ é [ONTO], a ratificar"),
])

patch("fechar_preparacao_v405.py", [
    ('''"nota": "a revisao de terceiro NAO aprovou o candidato anterior, a30f9f0ebf90c277 (2 ALTO, 11 MEDIO, 10 BAIXO; caderno revisao_terceiro/REVISAO_TERCEIRO_v405.md); esta e' a refacao pelas erratas R2 a R6 da gerencia.''',
     '''"nota": "a segunda revisao de terceiro NAO aprovou o candidato anterior, eaefcd095abbaee7 (1 ALTO, 4 MEDIO, 11 BAIXO; caderno revisao_terceiro/REVISAO_TERCEIRO_v405.md; os 13 achados da primeira fecharam); esta e' a refacao pela errata R7 da gerencia.'''),
    ('''"corrige": 1600, "estatuto": "REAL", "olhou_dados": False, "titulo": "a anotacao de 16:11 dizia pronta=true para a30f9f0ebf90c277: a revisao de terceiro nao aprovou esse candidato",''',
     '''"corrige": 1606, "estatuto": "REAL", "olhou_dados": False, "titulo": "a anotacao de 20:40 dizia pronta=true para eaefcd095abbaee7: a segunda revisao de terceiro nao aprovou esse candidato",'''),
    ('''"resultado": "o candidato a30f9f0ebf90c277 foi reprovado pela revisao de terceiro; nenhuma prova caiu e nenhum numero fisico estava errado; o candidato vigente da preparacao e' " + J["candidato_sha16"],''',
     '''"resultado": "o candidato eaefcd095abbaee7 foi reprovado pela segunda revisao de terceiro; nenhuma prova caiu, nenhum numero estava errado e o gate nao foi tocado; o candidato vigente da preparacao e' " + J["candidato_sha16"],'''),
    ('''pelas erratas R2 a R6, depois de a revisao de terceiro nao aprovar o candidato a30f9f0ebf90c277 (nada instalado; o rito nao rodou). Este deposito substitui o de 16:11 (20261101_161153_v405-preparada.md, seq 187). "''',
     '''pelas erratas R2 a R7, depois de a segunda revisao de terceiro nao aprovar o candidato eaefcd095abbaee7 (nada instalado; o rito nao rodou). Este deposito substitui o de 20:40 (20261101_204059_v405-preparada-r2.md, seq 191). "'''),
    ('''"--slug", "v405-preparada-r2",''', '''"--slug", "v405-preparada-r7",'''),
    ('''"prep-v405-r2-fechada-" + S''', '''"prep-v405-r7-fechada-" + S'''),
    ('''"titulo": "v405 preparada de novo, erratas R2 a R6 (01/11/2026): candidato %s; pronta=%s"''', '''"titulo": "v405 preparada de novo, erratas R2 a R7 (01/11/2026): candidato %s; pronta=%s"'''),
    ('''(8) um harness que reprova cedo nao roda os controles negativos: a primeira passada limpa leva muito mais tempo que a reprovada, e nao e' travamento.''',
     '''(8) um harness que reprova cedo nao roda os controles negativos: a primeira passada limpa leva muito mais tempo que a reprovada, e nao e' travamento; (9) a mesma palavra para duas grandezas numa secao so' e' achado de ALTO, ainda que cada igualdade esteja certa: o gap espectral e o valor esperado precisavam de nomes distintos.'''),
])
print("FEITO", TS)
