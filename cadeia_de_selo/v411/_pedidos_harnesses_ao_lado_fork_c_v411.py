# -*- coding: utf-8 -*-
"""_pedidos_harnesses_ao_lado_fork_c_v411.py -- (claude-construtor-v411, fork C, 12/11/2026) ACRESCENTA (so' acrescimo; backup de BYTES antes) em
PEDIDOS_ENTRE_FRENTES_v411.md uma linha AO LADO da nota dos harnesses (marca fork_c_harnesses_depuracao_12nov): os problemas do harness dos textos que
nao sao da leitura nem trazem a frase da cascata, contados e listados do JSON de depuracao por script, e a revalidacao do conferidor depois da
refatoracao (os dois JSONs lidos aqui). uso: python -B -X utf8 _pedidos_harnesses_ao_lado_fork_c_v411.py"""
import datetime, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
J = lambda p_: json.load(open(p_, encoding="utf-8"))
P = os.path.join(HERE, "PEDIDOS_ENTRE_FRENTES_v411.md")
MARCA = "<!-- fork_c_harnesses_ao_lado_12nov -->"
b = open(P, "rb").read(); t = b.decode("utf-8")
assert MARCA not in t and "<!-- fork_c_harnesses_depuracao_12nov -->" in t
HT = J(os.path.join(HERE, "pos_rito", "HARNESS_TEXTOS_ENSAIO_v411_DEPURACAO_sem_refazer.json"))
ps = [str(p_) for p_ in HT.get("problemas") or []]
outros = [p_ for p_ in ps if not p_.startswith("leitura: ") and "a leitura da rodada nao confirma o registro" not in p_]
et = HT.get("etapas") or {}
falsas = sorted(k_ for k_, v_ in et.items() if isinstance(v_, dict) and v_.get("ok") is False)
POS = J(DL.saida("conferencia_rito_v411_POSITIVO_FALSO_NOS.json")); NEG = J(DL.saida("conferencia_rito_v411_CONTROLE_NEGATIVO_PRE_RITO.json"))
assert POS.get("tudo_bate") is True and NEG.get("tudo_bate") is False and all((NEG.get("nao_pode_mudar") or {"x": False}).values())
add = ("\n\n(%s, fork C, AO LADO da nota acima) %s Os outros %d problemas do harness dos textos (os que nao sao da leitura nem trazem a frase da cascata) vem dos textos que nao renderizam enquanto a leitura nao confirma o registro: "
       "o handoff nao renderizado, a custodia G1 sem o bloco da linhagem, o S6d, os dois paragrafos do README fora do handoff, a secao do H0DN vazia e o termo entre crases que a leitura nao leu (o veredito do `%s`, que ESTA' no core, no selo, nos ESPERADOS e no stdout do falso Nos: conferido por script). "
       "As etapas com `ok` falso no resumo: %s. So' se sabe se algum e' independente depois do conserto da leitura. "
       "O conferidor refatorado foi rodado de novo: o controle negativo (o Nos na v410) nao bate, como esperado, com os %d itens de `nao_pode_mudar` verdadeiros; o caminho positivo no falso Nos da' TUDO BATE (%d + %d itens).\n"
       % (datetime.datetime.now().strftime("%d/%m/%Y %Hh%M"), MARCA, len(outros), DL.FECHO_REGISTRO, ", ".join("`%s`" % k_ for k_ in falsas), len(NEG.get("nao_pode_mudar") or {}), len(POS.get("deve_mudar") or {}), len(POS.get("nao_pode_mudar") or {})))
nb = (t.rstrip("\n") + add).encode("utf-8")
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_forkc4"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb) and nb.startswith(t.rstrip("\n").encode("utf-8")); os.replace(P + ".tmp", P)
print("acrescentado:", len(b), "->", len(nb), "| outros:", len(outros), "| etapas falsas:", falsas)
