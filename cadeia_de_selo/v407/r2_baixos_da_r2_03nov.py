# -*- coding: utf-8 -*-
"""03/11/2026 17:0x, gerencia c1 (R3 confinada): correcoes dos BAIXOS NOVOS da revisao R2 que sao frases afirmando mais do que o medido ou estatuto errado, SEM tocar pedra nem kernel:
(1) «relidas inteiras» -> o que a revisao fez (#print axioms no trio, diff contra as origens e docstrings; nao as provas linha a linha) em delta RESSALVAS e no artigo PT/EN;
(2) registros «NÃO diz»: deixa de contradizer a ressalva (so' tres por dentro em 02/11; as nove conferidas em 03/11 pelo revisor desta preparacao);
(3) papeis dos recibos/saidas R1 dizem que sao registro (a fonte vigente e' a R2); (4) [KNOWN/ONTO] -> [ONTO] na ponte Bell<->TT (delta RESSALVAS[2], artigo PT/EN, texto do README no pos_rito), como
ja' esta' na pedra Par; (5) rito_v407.sh: os numeros velhos do comentario (379/245) dao lugar aos MEDIDOS (lidos de kernel/construir_marcas.txt). .py pelo patches.aplicar_em_arquivo (backup +
sintaxe); .pysnip e .sh em bytes com backup. Nenhum enunciado, prova ou nome muda. Escrito pelo Write."""
import json, os, re, sys, time
sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import patches  # noqa: E402
V7 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v407"; TS = time.strftime("%Y%m%d_%H%M%S")
P = lambda *a: os.path.join(V7, *a)  # noqa: E731


def bytes_patch(arq, trocas, rotulo):
    b = open(arq, "rb").read(); novo = b
    for o, n in trocas:
        ob, nb = o.encode("utf-8"), n.encode("utf-8"); assert novo.count(ob) == 1, (os.path.basename(arq), novo.count(ob), o[:80]); novo = novo.replace(ob, nb)
    bak = arq + ".bak_%s_%s" % (rotulo, TS); open(bak, "xb").write(b); assert open(bak, "rb").read() == b
    tmp = arq + ".tmp_" + TS; open(tmp, "xb").write(novo); assert os.path.getsize(tmp) == len(novo); os.replace(tmp, arq); assert open(arq, "rb").read() == novo
    assert b.count(b"\r\n") == novo.count(b"\r\n")
    print("%s: %d -> %d B (%d trocas); backup %s" % (os.path.basename(arq), len(b), len(novo), len(trocas), os.path.basename(bak)))


def py_patch(arq, trocas, rotulo):
    def f(s):
        for o, n in trocas:
            assert s.count(o) == 1, (os.path.basename(arq), s.count(o), o[:80])
            s = s.replace(o, n)
        return s, ["%d trocas" % len(trocas)]
    print(json.dumps(patches.aplicar_em_arquivo(arq, f, rotulo), ensure_ascii=False)[:200])


# (1)+(4) delta
py_patch(P("delta_v407.py"), [
    ("a leitura do canto como sombra do graviton e' [KNOWN/ONTO]", "a leitura do canto como sombra do graviton e' [ONTO] (sem citacao [KNOWN] ate' haver fonte)"),
    ("as nove pedras foram relidas inteiras pelo revisor de terceiro desta preparacao em 03/11/2026 (R1 do Sonnet: 0 alto, 0 medio, 9 baixo; as correcoes da gerencia foram a R2)",
     "as nove pedras foram conferidas pelo revisor de terceiro desta preparacao em 03/11/2026 (Sonnet, rodadas R1 e seguintes: #print axioms no trio, diff contra as origens e docstrings, nao as provas linha a linha; 0 alto e 0 medio em todas as rodadas; os baixos ficam ditos no caderno da revisao)"),
], "r3_baixos")
# (2)+(3) registros
py_patch(P("registros_v407.py"), [
    ("que as sete pedras de 02/11 tenham revisao de terceiro completa: so' tres foram revistas pelo Sonnet (02/11)",
     "que as pedras tenham revisao de terceiro POR DENTRO das provas: em 02/11 o Sonnet reviu tres das sete (docstrings e enunciados); em 03/11 o revisor desta preparacao conferiu as nove por #print axioms, diff contra as origens e docstrings, nao as provas linha a linha"),
    ("e o que a pedra prova e NAO afirma [DECLARADO pela gerencia na origem; refeito no k407c e no Audit do rito]\"},",
     "e o que a pedra prova e NAO afirma [DECLARADO pela gerencia na origem; refeito no k407c e no Audit do rito] [registro R1: a fonte vigente e' a R2, recibo R2 abaixo]\"},"),
    ("e o que NAO afirma [DECLARADO pela gerencia na origem; refeito no k407c e no Audit do rito]\"},",
     "e o que NAO afirma [DECLARADO pela gerencia na origem; refeito no k407c e no Audit do rito] [registro R1: a fonte vigente e' a R2, recibo R2 abaixo]\"},"),
    ("\"papel\": \"a saida do lean ao compilar a PsionCanto (03/11/2026) [REAL: saida do lean]\"},", "\"papel\": \"a saida do lean ao compilar a PsionCanto (03/11/2026) [REAL: saida do lean] [registro R1: a saida vigente e' a R2, saida_lean_r3.txt]\"},"),
    ("\"papel\": \"a saida do lean ao compilar a pedra do par (03/11/2026) [REAL: saida do lean]\"},", "\"papel\": \"a saida do lean ao compilar a pedra do par (03/11/2026) [REAL: saida do lean] [registro R1: a saida vigente e' a R2, saida_lean_par_r2.txt]\"},"),
], "r3_baixos")
# (1)+(4) artigo PT/EN (pysnip, bytes)
bytes_patch(P("artigo_pt_v407.pysnip"), [
    ("a ponte entre os dois não é termo [KNOWN/ONTO]. ", "a ponte entre os dois não é termo [ONTO]. "),
    ("as nove foram relidas inteiras pelo revisor de terceiro desta preparação em 03/11 (R1: 0 alto, 0 médio, 9 baixo; as correções da gerência foram à R2).",
     r"as nove foram conferidas pelo revisor de terceiro desta preparação em 03/11 (\texttt{\#print axioms} no trio, diff contra as origens e docstrings; não as provas linha a linha; 0 alto e 0 médio em todas as rodadas; os baixos ficam ditos no caderno da revisão)."),
], "r3_baixos")
bytes_patch(P("artigo_en_v407.pysnip"), [
    ("the bridge between them is not a term [KNOWN/ONTO]. ", "the bridge between them is not a term [ONTO]. "),
    ("all nine were re-read in full by the third-party reviewer of this preparation on 03/11 (R1: 0 high, 0 medium, 9 low; the management's corrections went to R2).",
     r"all nine were checked by the third-party reviewer of this preparation on 03/11 (\texttt{\#print axioms} in the trio, diff against the origins and docstrings; not the proofs line by line; 0 high and 0 medium in every round; the low remarks stay written in the review notebook)."),
], "r3_baixos")
# (4) texto do README no pos_rito
py_patch(P("pos_rito", "textos_v407.py"), [("(a leitura do canto como sombra do gráviton é [KNOWN/ONTO])", "(a leitura do canto como sombra do gráviton é [ONTO])")], "r3_baixos")
bytes_patch(P("pos_rito", "textos_v407_novo.pysnip"), [("(a leitura do canto como sombra do gráviton é [KNOWN/ONTO])", "(a leitura do canto como sombra do gráviton é [ONTO])")], "r3_baixos")
# (5) rito_v407.sh: numeros velhos -> medidos (lidos)
tm = open(P("kernel", "construir_marcas.txt"), encoding="utf-8").read(); mm = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", tm, re.M)}
build_s = mm["epoch_build_fim"] - mm["epoch_inicio"]; audit_s = mm["epoch_audit_fim"] - mm["epoch_build_fim"]
bytes_patch(P("rito_v407.sh"), [
    ("(a ordem de grandeza e' a medida do sandbox, 379 s + 245 s)", "(a ordem de grandeza e' a medida do sandbox, %d s + %d s)" % (build_s, audit_s)),
    ("(build ja' pronto + Audit de 245 s)", "(build ja' pronto + Audit de %d s)" % audit_s),
], "r3_tempo")
s = open(P("rito_v407.sh"), encoding="utf-8").read(); assert "379 s" not in s and "245 s" not in s and "295 s" not in s
print("OK: baixos da R2 corrigidos (sem tocar pedra nem kernel)")
