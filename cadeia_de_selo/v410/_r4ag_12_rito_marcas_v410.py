# -*- coding: utf-8 -*-
"""_r4ag_12_rito_marcas_v410.py -- agente de adaptacao da R1 (R4): o CABECALHO descritivo de rito_v410.sh (comentario; o corpo do rito NAO muda) com as marcas que conferir_instalar_rito_v410.py exige, e a marca das falas no conferidor (06, 07, 08, 09 e 10/11).
Os numeros do cabecalho sao LIDOS (ancoras do delta, decisoes e erratas do delta, falas do delta, tempos de kernel/construir_marcas.txt e de kernel/KH_N1_v410.json) e reescritos por regex: o script e' IDEMPOTENTE e pode ser rodado de novo depois de um build a frio novo."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r4ag_lib_v410 import aplicar, HERE
import json
import delta_v410 as DL

tm = open(os.path.join(HERE, "kernel", "construir_marcas.txt"), encoding="utf-8").read()
mm = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", tm, re.M)}
build_s = mm["epoch_build_fim"] - mm["epoch_inicio"]; audit_s = mm["epoch_audit_fim"] - mm.get("epoch_audit_inicio", mm["epoch_build_fim"])
KHT = json.load(open(os.path.join(HERE, "kernel", "KH_N1_v410.json"), encoding="utf-8"))
soma, mx = KHT.get("build_modulos_s_soma"), KHT.get("build_modulos_s_max")
n_anc_a = len(DL.ANCORAS_AESCALA); n_flags = DL.N_ANCORAS_AESCALA   # (as ancoras da AEscala: do delta)
FJ = json.load(open(os.path.join(HERE, "kernel", "FLAGS_v410.json"), encoding="utf-8"))
dec0, dec1 = DL.DECISOES_V410[0], DL.DECISOES_V410[-1]
err_ids = [e_.split(" ")[0] for e_ in DL.ERRATAS_V410]
err_txt = ", ".join(err_ids[:-1]) + " e " + err_ids[-1]
err_txt_virg = ", ".join(err_ids)

p = os.path.join(HERE, "rito_v410.sh")
t0 = open(p, "rb").read().decode("utf-8"); crlf = "\r\n" in t0; t = t0.replace("\r\n", "\n")
n_trocas = 0


def troca(rx, novo, count_min=1):
    global t, n_trocas
    t, n = re.subn(rx, novo, t)
    assert n >= count_min, ("a marca do cabecalho nao foi achada", rx)
    n_trocas += n


# os numeros estaticos do cabecalho (R3 -> R4), por regex (idempotente)
troca(r"AEscala: \d+ ancoras; \d+ bandeiras em duas series", "AEscala: %d ancoras; %d bandeiras em duas series" % (n_anc_a, FJ["n_flags"]))
troca(r"\d+ falas de 06 a (?:09|10)/11, decisoes D63 a D\d+, erratas E29, E30, E31, E32(?:, E33, E34)?;", "%d falas de 06 a 10/11, decisoes %s a %s, erratas %s;" % (DL.N_FALAS_V410, dec0, dec1, err_txt_virg))
troca(r"as \d+ falas de 06, 07, 08(?:,| e) (?:09 e 10|09)/11", "as %d falas de 06, 07, 08, 09 e 10/11" % DL.N_FALAS_V410, 2)
troca(r"com as \d+ falas de 06, 07, 08(?:,| e) (?:09 e 10|09)/11", "com as %d falas de 06, 07, 08, 09 e 10/11" % DL.N_FALAS_V410, 0)
troca(r"as decisoes D63 a D\d+ e as erratas E29, E30, E31(?:,)? e E32 vao nos registros", "as decisoes %s a %s e as erratas %s vao nos registros" % (dec0, dec1, err_txt), 0)
troca(r"as decisoes D63 a D\d+ e as erratas E29, E30, E31(?:, E32, E33)? e E\d+ vao nos registros", "as decisoes %s a %s e as erratas %s vao nos registros" % (dec0, dec1, err_txt), 1)
troca(r"as decisoes D63 a D\d+, as erratas E29, E30, E31(?:,)? e E32 e a dos pisos", "as decisoes %s a %s, as erratas %s e a dos pisos" % (dec0, dec1, err_txt), 0)
troca(r"le as \d+ ancoras do axiom_report do rito, a pedra por sha256", "le as %d ancoras do axiom_report do rito, a pedra por sha256" % n_anc_a)
troca(r"\[D63 a D\d+\] as muda", "[%s a %s] as muda" % (dec0, dec1))
# os tempos MEDIDOS (kernel/construir_marcas.txt e KH_N1_v410.json)
troca(r"\(build \d+ s, Audit \d+ s; a soma dos tempos por modulo [\d.]+ s, o maximo [\d.]+ s\)", "(build %d s, Audit %d s; a soma dos tempos por modulo %s s, o maximo %s s)" % (build_s, audit_s, soma, mx))
troca(r"= \d+ s e 1 Audit = \d+ s \(a soma dos tempos por modulo e' [\d.]+ s, o maximo de um modulo [\d.]+ s\)", "= %d s e 1 Audit = %d s (a soma dos tempos por modulo e' %s s, o maximo de um modulo %s s)" % (build_s, audit_s, soma, mx))
# a ressalva honesta do tempo: o ultimo build (10/11 02:31) reaproveitou a raiz e o Audit do build anterior da R4 (linha Replayed); o build a frio completo da R3 (09/11) foi de 329 s
RESSALVA = " [RESSALVA DO TEMPO, 10/11: no ultimo build do sandbox (10/11 02:31) so' os 2 modulos novos foram Built; a raiz TGLExt e o Audit vieram do build anterior da R4 (linha Replayed), por isso o build medido e' curto; o build a frio COMPLETO, medido na R3 em 09/11, foi de 329 s; o rito compila tudo a frio]"
if "RESSALVA DO TEMPO, 10/11" not in t:
    t, n = re.subn(r"(= \d+ s e 1 Audit = \d+ s \(a soma dos tempos por modulo e' [\d.]+ s, o maximo de um modulo [\d.]+ s\))", lambda m: m.group(1) + RESSALVA, t, count=1)
    assert n == 1
    n_trocas += n
nb = (t.replace("\n", "\r\n") if crlf else t).encode("utf-8")
if nb != t0.encode("utf-8"):
    open(p + ".bak_" + __import__("time").strftime("%Y%m%d_%H%M%S") + "_r4_agente_marcas", "wb").write(t0.encode("utf-8"))
    open(p + ".tmp", "wb").write(nb); os.replace(p + ".tmp", p)
    print("rito_v410.sh atualizado (%d trocas); build %d s, Audit %d s, soma %s, max %s" % (n_trocas, build_s, audit_s, soma, mx))
else:
    print("rito_v410.sh ja' esta' como o delta e as marcas mandam")

# a marca das falas no conferidor: 06, 07, 08, 09 e 10/11
aplicar("conferir_instalar_rito_v410.py", [('"%d falas de 06, 07, 08 e 09/11" % DL.N_FALAS_V410', '"%d falas de 06, 07, 08, 09 e 10/11" % DL.N_FALAS_V410', 1)]) if '"%d falas de 06, 07, 08 e 09/11" % DL.N_FALAS_V410' in open(os.path.join(HERE, "conferir_instalar_rito_v410.py"), encoding="utf-8").read() else None
