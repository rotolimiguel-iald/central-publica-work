# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork A)] o conferidor idempotente dos logs do kernel da v411 (build incremental SEM modulo novo, nada compilado; o Audit): o registro que o pos_build_kernel_v411.py gravou e' o KERNEL_RECIBO_v411.json (build_full_log e audit_log, sha256) e o POS_BUILD_v411.json (marcas); o LOGS_COPIADOS_v411.json NAO e' escrito na v411 e, se existir, tambem e' conferido; nada e' gravado
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] conferidor idempotente dos logs do kernel da v410 (le KH_N1_v410.json e LOGS_COPIADOS_v410.json); nada de bundle no corpo; conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
"""copiar_logs_do_kernel_v411.py -- CONFERIDOR IDEMPOTENTE dos logs da construcao do kernel da v411 (adaptado em 06/11/2026 a v411; desde a v410 ele nao grava nada: so' compara).
A construcao (construir_kernel_v411.sh: `lake build` incremental -- a v411 NAO tem modulo novo; nada a compilar -- e `lake env lean TGL/Audit.lean` no sandbox C:\\t\\k411c\\final) escreve DIRETO em v411\\kernel\\ (lake_build.log, audit.log, construir_marcas.txt), e o pos_build_kernel_v411.py grava kernel\\LOGS_COPIADOS_v411.json
(sha256 e bytes de cada log, a linha TGL_AXIOM_COVERAGE_TOTAL). Origem e destino sao a mesma pasta: nada se copia, e como o pos_build ja grava o JSON, este script so' COMPARA e NUNCA REGRAVA (nem o JSON, nem os logs):
  (a) construir_marcas.txt diz rc=0, rc_build=0 e rc_audit=0; (b) a linha TGL_AXIOM_COVERAGE_TOTAL do build e a do audit sao a mesma e igual a linha_TOTAL do KH_N1_v411.json (decl, thm, fora_do_trio); (c) os tempos das marcas (epoch) == duracao_build_s e duracao_audit_s do KH_N1_v411.json;
  (d) o sha256 do lake_build.log e do audit.log, recalculados agora, == o que kernel\\KERNEL_RECIBO_v411.json registrou (build_full_log, audit_log) e as marcas == as do kernel\\POS_BUILD_v411.json (o log nao mudou depois do pos_build); (v411) o LOGS_COPIADOS_v411.json nao e' escrito pelo pos_build da v411: se existir, o bytes e o sha256 dos tres arquivos tambem sao conferidos contra ele. Sai 0 se tudo bate; 1 se algo difere ou o JSON nao existe (rode o pos_build_kernel_v411.py antes). Re-executavel quantas vezes se quiser: nao escreve em lugar nenhum.
uso: python -I -B -X utf8 copiar_logs_do_kernel_v411.py   (molde: copiar_logs_do_kernel_v410.py)"""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
KD = os.path.join(HERE, "kernel")
sha = lambda b: hashlib.sha256(b).hexdigest()
falhas = []


def chk(nome, ok, det=None):
    print(("OK   " if ok else "FALHA"), nome, "" if det is None else "-> " + str(det)[:200])
    if not ok:
        falhas.append(nome)


marcas = open(os.path.join(KD, "construir_marcas.txt"), encoding="utf-8").read()
chk("construir_marcas.txt: rc=0, rc_build=0 e rc_audit=0", bool(re.search(r"^rc=0$", marcas, re.M) and re.search(r"rc_build=0\b", marcas) and re.search(r"rc_audit=0\b", marcas)))
mm = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", marcas, re.M)}
atual = {}; cov = {}
for nome in ("lake_build.log", "audit.log", "construir_marcas.txt"):
    b = open(os.path.join(KD, nome), "rb").read()
    atual[nome] = {"bytes": len(b), "sha256": sha(b)}
    if nome.endswith(".log"):
        cov[nome] = [x.decode() for x in re.findall(rb"(?m)^TGL_AXIOM_COVERAGE_TOTAL[^\r\n]*", b)]
chk("a linha TGL_AXIOM_COVERAGE_TOTAL do build e a do audit sao a mesma (uma so' em cada)", len(cov["lake_build.log"]) == 1 and cov["lake_build.log"] == cov["audit.log"], cov)
kh = json.load(open(os.path.join(KD, "KH_N1_v411.json"), encoding="utf-8"))
t = kh["linha_TOTAL"]
chk("a linha de cobertura == linha_TOTAL do KH_N1_v411.json (decl, thm, fora_do_trio)", cov["audit.log"] == ["TGL_AXIOM_COVERAGE_TOTAL decl=%d thm=%d fora_do_trio=%d" % (t["decl"], t["thm"], t["fora_do_trio"])], [cov["audit.log"], t])
chk("os tempos das marcas == duracao_build_s e duracao_audit_s do KH_N1_v411.json", mm.get("epoch_build_fim", 0) - mm.get("epoch_inicio", 0) == kh["duracao_build_s"] and mm.get("epoch_audit_fim", 0) - mm.get("epoch_build_fim", 0) == kh["duracao_audit_s"], [mm, kh["duracao_build_s"], kh["duracao_audit_s"]])
chk("o sha256 do audit.log == o que o KH_N1_v411.json registrou (audit_log_sha256) e os bytes == audit_log_bytes", atual["audit.log"]["sha256"] == kh["audit_log_sha256"] and atual["audit.log"]["bytes"] == kh["audit_log_bytes"], [atual["audit.log"]["sha256"][:16], kh["audit_log_sha256"][:16]])
kr = json.load(open(os.path.join(KD, "KERNEL_RECIBO_v411.json"), encoding="utf-8")); pb = json.load(open(os.path.join(KD, "POS_BUILD_v411.json"), encoding="utf-8"))   # (v411) o registro que o pos_build_kernel_v411.py gravou
chk("KERNEL_RECIBO_v411.json[build_full_log] e [audit_log]: sha256 == os recalculados agora (lake_build.log e audit.log)", kr["build_full_log"]["sha256"] == atual["lake_build.log"]["sha256"] and kr["audit_log"]["sha256"] == atual["audit.log"]["sha256"], [kr["build_full_log"]["sha256"][:16], kr["audit_log"]["sha256"][:16]])
chk("POS_BUILD_v411.json[marcas] == as marcas lidas agora de construir_marcas.txt (os epochs e os rc)", {k_: int(v_) for k_, v_ in pb["marcas"].items() if k_.startswith("epoch_")} == mm and all(pb["marcas"].get(k_) == "0" for k_ in ("rc", "rc_build", "rc_audit")), pb.get("marcas"))
jp = os.path.join(KD, "LOGS_COPIADOS_v411.json")
if not os.path.exists(jp):
    print("     (o LOGS_COPIADOS_v411.json nao existe: o pos_build da v411 nao o escreve; o registro conferido acima e' o KERNEL_RECIBO e o POS_BUILD)")
else:
    reg = json.load(open(jp, encoding="utf-8"))
    for nome in atual:
        chk("LOGS_COPIADOS_v411.json[%s]: bytes e sha256 == os recalculados agora" % nome, reg.get(nome, {}).get("bytes") == atual[nome]["bytes"] and reg.get(nome, {}).get("sha256") == atual[nome]["sha256"], [reg.get(nome, {}).get("sha256", "")[:16], atual[nome]["sha256"][:16]])
    chk("LOGS_COPIADOS_v411.json[cobertura_linha] == a linha lida agora do audit.log", reg.get("cobertura_linha") == cov["audit.log"], reg.get("cobertura_linha"))
print("LOGS DO KERNEL v411:", "CONFEREM (nada foi gravado)" if not falhas else "DIFEREM: %s" % falhas)
sys.exit(0 if not falhas else 1)
