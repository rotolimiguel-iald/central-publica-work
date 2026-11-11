# -*- coding: utf-8 -*-
"""_r5ag_14_rito_marcas_v410.py -- R5: o CABECALHO descritivo de rito_v410.sh (comentario; o corpo do rito NAO muda) com as marcas que conferir_instalar_rito_v410.py exige: as 62 ancoras e as 107 bandeiras, as 28 falas, as decisoes D63 a D96 e D99 a D101, as erratas E29 a E37, as 13 checagens da AEscala,
os tempos MEDIDOS (kernel/construir_marcas.txt e kernel/KH_N1_v410.json) e a ressalva do tempo atualizada. Substitui o _r4ag_12 (que falha na regex do cabecalho da R2). Os numeros sao LIDOS (delta, FLAGS, marcas); as trocas sao por regex e o script e' IDEMPOTENTE; backup de BYTES antes."""
import json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v410 as DL

tm = open(os.path.join(HERE, "kernel", "construir_marcas.txt"), encoding="utf-8").read()
mm = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", tm, re.M)}
build_s = mm["epoch_build_fim"] - mm["epoch_inicio"]; audit_s = mm["epoch_audit_fim"] - mm["epoch_build_fim"]
KHT = json.load(open(os.path.join(HERE, "kernel", "KH_N1_v410.json"), encoding="utf-8"))
soma, mx = KHT.get("build_modulos_s_soma"), KHT.get("build_modulos_s_max")
FJ = json.load(open(os.path.join(HERE, "kernel", "FLAGS_v410.json"), encoding="utf-8"))
n_anc_a = len(DL.ANCORAS_AESCALA); n_flags = FJ["n_flags"]
err_ids = [e_.split(" ")[0] for e_ in DL.ERRATAS_V410]
err_txt = ", ".join(err_ids[:-1]) + " e " + err_ids[-1]          # E29, ..., E36 e E37
rot = DL.DECISOES_ROTULO                                           # D63 a D96 e D99 a D101

p = os.path.join(HERE, "rito_v410.sh")
t0 = open(p, "rb").read().decode("utf-8"); crlf = "\r\n" in t0; t = t0.replace("\r\n", "\n"); n_trocas = 0


def troca(rx, novo, count_min=1):
    global t, n_trocas
    t, n = re.subn(rx, novo, t)
    assert n >= count_min, ("a marca do cabecalho nao foi achada", rx)
    n_trocas += n


troca(r"AEscala: \d+ ancoras; \d+ bandeiras em duas series", "AEscala: %d ancoras; %d bandeiras em duas series" % (n_anc_a, n_flags))
troca(r"\d+ falas de 06 a 10/11, decisoes D63 a D96 e D99(?: a D101)?, erratas E29(?:, E\d+)* e E\d+;", "%d falas de 06 a 10/11, decisoes %s, erratas %s;" % (DL.N_FALAS_V410, rot, err_txt))
troca(r"as \d+ falas de 06, 07, 08, 09 e 10/11", "as %d falas de 06, 07, 08, 09 e 10/11" % DL.N_FALAS_V410, 2)
troca(r"as decisoes D63 a D96 e D99(?: a D101)? e as erratas E29(?:, E\d+)* e E\d+ vao nos registros", "as decisoes %s e as erratas %s vao nos registros" % (rot, err_txt), 1)
troca(r"as decisoes D63 a D96 e D99(?: a D101)?, as erratas E29(?:, E\d+)*(?: e E\d+)?", "as decisoes %s, as erratas %s" % (rot, ", ".join(err_ids)), 0)
troca(r"le as \d+ ancoras do axiom_report do rito, a pedra por sha256", "le as %d ancoras do axiom_report do rito, a pedra por sha256" % n_anc_a)
troca(r"faz as \d+ checagens da AEscala", "faz as %d checagens da AEscala" % DL.N_CHECKS_AESCALA)
troca(r"\[D63 a D96 e D99(?: a D101)?\] as muda", "[%s] as muda" % rot)
troca(r"\(build \d+ s, Audit \d+ s; a soma dos tempos por modulo [\d.]+ s, o maximo [\d.]+ s\)", "(build %d s, Audit %d s; a soma dos tempos por modulo %s s, o maximo %s s)" % (build_s, audit_s, soma, mx))
troca(r"= \d+ s e 1 Audit = \d+ s \(a soma dos tempos por modulo e' [\d.]+ s, o maximo de um modulo [\d.]+ s\)", "= %d s e 1 Audit = %d s (a soma dos tempos por modulo e' %s s, o maximo de um modulo %s s)" % (build_s, audit_s, soma, mx))
# a ressalva do tempo, atualizada pelo build de 10/11 (09:13 a 09:25): incremental no que e' antigo e a frio nos 2 modulos novos (o recibo do kernel o diz); o rito do Nos compila tudo a frio
RESSALVA = "[RESSALVA DO TEMPO, 10/11: o ultimo build do sandbox (10/11, das 09:13 as 09:25) foi INCREMENTAL no que e' antigo (copia do kernel da v409 ja' compilado) e A FRIO nos 2 modulos novos (IALD2 e AEscala R5); o build a frio COMPLETO, medido na R3 em 09/11, foi de 329 s; o rito compila tudo a frio]"
troca(r"\[RESSALVA DO TEMPO, 10/11:[^\]]*\]", RESSALVA.replace("\\", "\\\\"), 1)
LINHA = "# [ADAPTADO v410 R5, 10/11/2026, agente de adaptacao, a servico do construtor claude-construtor-v410] so' o texto descritivo do cabecalho; o corpo do rito NAO muda: a rodada R5 (D100 e D101; ADENDOS 5 e 6): a pedra AEscala R5 (a clausula do Tetelestai em 1 - beta) e a ratificacao de 10/11; a c13 do registro a_escala_v410; as decisoes da v410 sao " + rot + " e as erratas " + err_ids[0] + " a " + err_ids[-1] + "; os numeros dos cabecalhos abaixo foram atualizados e lidos do delta, do FLAGS e das marcas do kernel\n"
if "[ADAPTADO v410 R5" not in t:
    t = t.replace("#!/bin/sh\n", "#!/bin/sh\n" + LINHA, 1); n_trocas += 1
nb = (t.replace("\n", "\r\n") if crlf else t).encode("utf-8")
if nb != t0.encode("utf-8"):
    open(p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_r5", "wb").write(t0.encode("utf-8"))
    open(p + ".tmp", "wb").write(nb); assert os.path.getsize(p + ".tmp") == len(nb); os.replace(p + ".tmp", p)
    print("rito_v410.sh atualizado (%d trocas); build %d s, Audit %d s, soma %s, max %s; %d ancoras da AEscala, %d bandeiras, %d falas, decisoes %s, erratas %s" % (n_trocas, build_s, audit_s, soma, mx, n_anc_a, n_flags, DL.N_FALAS_V410, rot, err_txt))
else:
    print("rito_v410.sh ja' esta' como o delta e as marcas mandam")
