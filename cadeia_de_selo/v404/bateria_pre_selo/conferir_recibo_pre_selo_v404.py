# -*- coding: utf-8 -*-
"""conferir_recibo_pre_selo_v404.py -- SO LEITURA. Confere o recibo pre_selo do ensaio (ensaio_1) PELO MESMO CAMINHO que o B(n) pos_selo da v404 usara:
conferir_recibo_pre_selo(...) do esboco R3.5 contra a Bancada de PRODUCAO (estado_anterior, so leitura), com o sha do recibo pinado, o selo e o manifesto do kernel da v403
(--selo-anterior / --kernel-manifesto-anterior: as copias de bytes de v404/base_v403) e SEM cadeia de selos (nao ha salto: a Bancada pina a v403 e o Nos e a v403).
ja_sincronizada=False: no B(n) o Nos sera a v404 e a Bancada ainda pinara a v403. Alem da funcao do esboco, repete por script cada condicao da regra (nome, observado, esperado)
e roda cinco controles negativos (recibo adulterado / pino errado), que a funcao do esboco tem de recusar. Esboco e bateria sao os PINADOS (path e sha256 lidos dos pinos, conferidos
contra o disco). Nada e' escrito na producao nem no Nos; so' grava conferencia_pelo_esboco_v404.json ao lado do ensaio e as copias adulteradas em C:\\t\\vb21\\ctl.
uso: python -I -B -X utf8 conferir_recibo_pre_selo_v404.py"""
import sys

sys.dont_write_bytecode = True
import glob
import hashlib
import importlib.util
import json
import os
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.dirname(HERE)                                   # ...\cadeia_de_selo\v404
V13 = os.path.join(os.path.dirname(V), "v403")
CTL = os.path.join("C:" + os.sep, "t", "vb21", "ctl")        # copias adulteradas (sandbox curto, apagado no fim)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def lj(p):
    return json.load(open(p, encoding="utf-8"))


# os pinos do esboco R3.5 e da bateria da v403: path e sha256 LIDOS dos pinos e conferidos contra o disco
pbn = lj(os.path.join(V13, "PINOS_BN_v403.json"))
pbat = lj(os.path.join(V13, "bateria_pos_selo", "PINOS_BATERIA_v403.json"))
ESB, ESB_SHA = pbn["esboco_R3_5"]["path"], pbn["esboco_R3_5"]["sha256"]
BAT, BAT_SHA = pbat["bateria"]["path"], pbat["bateria"]["sha256"]
assert sha(ESB) == ESB_SHA, "o esboco R3.5 em disco nao e o pinado"
assert sha(BAT) == BAT_SHA, "a bateria da v403 em disco nao e a pinada"

spec = importlib.util.spec_from_file_location("sincronizar_bancada_r35", ESB)
MOD = importlib.util.module_from_spec(spec)
sys.modules["sincronizar_bancada_r35"] = MOD
spec.loader.exec_module(MOD)

ENS = os.path.join(HERE, "ensaio_1")
rps = glob.glob(os.path.join(ENS, "RECIBO_SINCRONIZACAO_v403_*.json"))
assert len(rps) == 1, rps
RP = rps[0]
raw = open(RP, "rb").read()
RSHA = hashlib.sha256(raw).hexdigest()
r = json.loads(raw.decode("utf-8"))
out_txt = open(os.path.join(HERE, "etapa1_stdout.txt"), encoding="utf-8").read().splitlines()
imp = json.loads([l for l in out_txt if l.strip().startswith("{")][-1])
rc_lancador = int([l for l in out_txt if l.startswith("ETAPA1_RC=")][-1].split("=", 1)[1])

SELO_ANT = os.path.join(V, "base_v403", "um_absoluto_selo.json")
KM_ANT = os.path.join(V, "base_v403", "tgl_kernel_proof_manifest.json")
SELO_V402 = os.path.join(V13, "base_v402", "um_absoluto_selo.json")      # o selo da versao ANTES da anterior: o controle negativo "selo anterior errado"
KM_V402 = os.path.join(V13, "base_v402", "tgl_kernel_proof_manifest.json")

canon, _pin = MOD.carregar_canonical(MOD.PRODUCAO)
ant = MOD.estado_anterior(MOD.PRODUCAO, canon)      # so leitura da producao, como o B(n) faz
GER = int(MOD.RE_GERACAO.match(str(ant["deployment_id"])).group(1))   # a geracao B<n> que a Bancada pina agora; o B(n) da v404 grava a B<n+1>


def conferir(rp, sha_esp, selo, km, ja=False):
    try:
        res = MOD.conferir_recibo_pre_selo(Path(rp), ant, MOD.PRODUCAO, ja, sha_esp, selo, km, None)
        return True, None, res
    except MOD.Recusa as exc:
        return False, str(exc), None


aceito, recusa, res = conferir(RP, RSHA, SELO_ANT, KM_ANT)

# ---- cada condicao da regra, repetida por script (nome, observado, esperado)
checks = []


def chk(nome, ok, observado, esperado):
    checks.append({"nome": nome, "ok": bool(ok), "observado": observado, "esperado": esperado})


H64 = lambda x: isinstance(x, str) and len(x) == 64 and all(c in "0123456789abcdef" for c in x)
bat = r.get("bateria_resultado") or {}
ids = {t.get("id"): t.get("resultado") for t in bat.get("testes") or []}
nos = r.get("nos") or {}
kern = nos.get("kernel") or {}
selo_r = nos.get("selo") or {}
pv = (r.get("bateria") or {}).get("pinos_da_versao") or {}
selo_ant_j = lj(SELO_ANT)
pin_k = str((selo_ant_j.get("sha256") or {}).get("tgl_kernel_proof_manifest.json") or "")
man_sinc = (ant["_man"].get("sincronizacao") or {})

chk("fase", r.get("fase") == "pre_selo", r.get("fase"), "pre_selo")
chk("modo_ensaio_nada_gravado", r.get("modo") == "ensaio" and str(r.get("veredito") or "").endswith("__ENSAIO__NADA_GRAVADO_NA_BANCADA"), [r.get("modo"), r.get("veredito")],
    "ensaio / ...__ENSAIO__NADA_GRAVADO_NA_BANCADA")
chk("bateria_passa", bat.get("veredito") == "BATERIA_PASSA", bat.get("veredito"), "BATERIA_PASSA")
chk("veredito_ja_sincronizada", str(r.get("veredito") or "").startswith("JA_SINCRONIZADA__ENSAIO"), r.get("veredito"), "prefixo JA_SINCRONIZADA__ENSAIO")
chk("sem_salto_e_sem_cadeia", r.get("salto") is None and r.get("cadeia_de_selos") is None, [r.get("salto"), r.get("cadeia_de_selos")], "ambos ausentes")
chk("versao_alvo_igual_a_versao_pinada_pela_bancada", r.get("versao_alvo") == ant["version"], [r.get("versao_alvo"), ant["version"]], "iguais")
chk("um_py_do_recibo_igual_ao_pinado_pela_bancada", (nos.get("um_py") or {}).get("sha256") == ant["um_py_pinado"],
    [str((nos.get("um_py") or {}).get("sha256"))[:16], str(ant["um_py_pinado"])[:16]], "iguais")
chk("selo_do_recibo_igual_ao_pinado_pela_bancada", selo_r.get("sha256") == ant["seal_sha_pinado"], [str(selo_r.get("sha256"))[:16], str(ant["seal_sha_pinado"])[:16]], "iguais")
chk("bancada_do_recibo_e_a_producao_por_identidade", os.path.samefile((r.get("bancada") or {}).get("dir"), str(MOD.PRODUCAO)), (r.get("bancada") or {}).get("dir"), str(MOD.PRODUCAO))
chk("T01_e_T15_passam", ids.get("T01_IDENTIDADE") == "PASSA" and ids.get("T15_SONDAS") == "PASSA", [ids.get("T01_IDENTIDADE"), ids.get("T15_SONDAS")], "PASSA e PASSA")
chk("kernel_do_recibo_completo", all(H64(kern.get(c)) for c in ("sha256", "raiz_sha256", "audit_sha256", "impressao_formal")), sorted(k for k in kern if H64(kern.get(k))),
    "sha256, raiz_sha256, audit_sha256, impressao_formal (64 hex)")
chk("manifesto_do_kernel_do_recibo_igual_ao_pino_do_selo_do_recibo", kern.get("sha256") == selo_r.get("tgl_kernel_proof_manifest_sha256"),
    [str(kern.get("sha256"))[:16], str(selo_r.get("tgl_kernel_proof_manifest_sha256"))[:16]], "iguais")
chk("selo_anterior_da_custodia_igual_ao_pinado_pela_bancada", sha(SELO_ANT) == ant["seal_sha_pinado"], [sha(SELO_ANT)[:16], str(ant["seal_sha_pinado"])[:16]], "iguais")
chk("selo_anterior_da_custodia_diz_a_versao_da_bancada", selo_ant_j.get("um_version") == ant["version"], [selo_ant_j.get("um_version"), ant["version"]], "iguais")
chk("manifesto_do_kernel_da_custodia_igual_ao_pino_do_selo_anterior", sha(KM_ANT) == pin_k, [sha(KM_ANT)[:16], pin_k[:16]], "iguais")
chk("manifesto_do_kernel_do_recibo_igual_ao_da_custodia", kern.get("sha256") == sha(KM_ANT), [str(kern.get("sha256"))[:16], sha(KM_ANT)[:16]], "iguais")
chk("kernel_registrado_na_bancada_igual_ao_pino_do_selo_anterior", str(man_sinc.get("kernel_manifesto_sha256")).lower() == pin_k.lower(),
    [str(man_sinc.get("kernel_manifesto_sha256"))[:16], pin_k[:16]], "iguais")
chk("estado_do_contrato_instalado_ok", ant["estado_do_contrato_instalado"] == "OK", ant["estado_do_contrato_instalado"], "OK")
chk("pinos_da_versao_da_bateria_conferidos_contra_o_nos_lido", pv.get("declarados") is True and pv.get("conferidos_contra_o_nos_lido") is True and pv.get("versao") == ant["version"],
    {k: pv.get(k) for k in ("declarados", "conferidos_contra_o_nos_lido", "versao")}, "declarados, conferidos e da versao pinada pela bancada")
chk("script_do_recibo_e_o_esboco_pinado", r.get("script_sha256") == ESB_SHA, [str(r.get("script_sha256"))[:16], ESB_SHA[:16]], "iguais")
chk("bateria_do_recibo_e_a_pinada", (r.get("bateria") or {}).get("sha256") == BAT_SHA, [str((r.get("bateria") or {}).get("sha256"))[:16], BAT_SHA[:16]], "iguais")
chk("stdout_cita_o_recibo_com_o_sha_lido", imp.get("recibo_sha256") == RSHA and os.path.samefile(imp.get("recibo"), RP), [str(imp.get("recibo_sha256"))[:16], RSHA[:16]], "iguais")
chk("lancador_saiu_com_rc_0", rc_lancador == 0, rc_lancador, 0)

# ---- controles negativos: a funcao do esboco tem de RECUSAR cada adulteracao (leitura da producao; as copias ficam em C:\t\vb21\ctl)
os.makedirs(CTL, exist_ok=True)
controles = []


def controle(nome, esperado_prefixo, ok_recusou, recusa_txt):
    controles.append({"nome": nome, "recusou": (not ok_recusou), "esperado_comecar_por": esperado_prefixo, "recusa": recusa_txt,
                      "como_esperado": (not ok_recusou) and str(recusa_txt).startswith(esperado_prefixo)})


ok, rec_t, _ = conferir(RP, "0" * 64, SELO_ANT, KM_ANT)
controle("sha_do_recibo_errado", "RECIBO_PRE_SELO_SHA_DIVERGE", ok, rec_t)
ok, rec_t, _ = conferir(RP, RSHA, SELO_V402, KM_V402)
controle("selo_anterior_e_o_da_v402_nao_o_pinado", "SELO_ANTERIOR_NAO_E_O_PINADO", ok, rec_t)


def mutado(nome, fn):
    m = json.loads(raw.decode("utf-8"))
    fn(m)
    b = (json.dumps(m, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    p = os.path.join(CTL, nome + ".json")
    with open(p, "wb") as fh:
        fh.write(b)
    return p, hashlib.sha256(b).hexdigest()


p, s_ = mutado("veredito_de_outra_forma", lambda m: m.__setitem__("veredito", "REPINADA_B%d__ENSAIO__NADA_GRAVADO_NA_BANCADA" % (GER + 1)))
ok, rec_t, _ = conferir(p, s_, SELO_ANT, KM_ANT)
controle("veredito_nao_e_ja_sincronizada", "RECIBO_PRE_SELO_NAO_CORRESPONDE", ok, rec_t)


def _bat_falha(m):
    m["bateria_resultado"]["veredito"] = "BATERIA_FALHOU"


p, s_ = mutado("bateria_falhou", _bat_falha)
ok, rec_t, _ = conferir(p, s_, SELO_ANT, KM_ANT)
controle("bateria_nao_passa", "RECIBO_PRE_SELO_INVALIDO", ok, rec_t)


def _um_outro(m):
    m["nos"]["um_py"]["sha256"] = "1" * 64


p, s_ = mutado("um_py_de_outra_versao", _um_outro)
ok, rec_t, _ = conferir(p, s_, SELO_ANT, KM_ANT)
controle("um_py_do_recibo_nao_e_o_pinado", "RECIBO_PRE_SELO_NAO_CORRESPONDE", ok, rec_t)

motivos = [c["nome"] + ": observado %r, esperado %r" % (c["observado"], c["esperado"]) for c in checks if not c["ok"]]
if not aceito:
    motivos.append("conferir_recibo_pre_selo do esboco R3.5 RECUSOU: %s" % recusa)
motivos += ["controle negativo nao recusou como esperado: " + c["nome"] for c in controles if not c["como_esperado"]]
utilizavel = (not motivos)

resumo_res = None
if res is not None:
    resumo_res = {k: res.get(k) for k in ("path", "sha256", "bytes", "versao", "veredito", "um_py_sha256", "bancada_dir", "bateria", "selo_sha256", "selo_cruzado_com_o_manifesto_anterior",
                                          "kernel_manifesto_anterior_sha256", "kernel_anterior", "salto")}
    resumo_res["kernel_cruzado_com_o_selo_anterior"] = res.get("kernel_cruzado_com_o_selo_anterior")

conf = {
    "contrato": "CONFERENCIA_PELO_ESBOCO_RECIBO_PRE_SELO_v404",
    "como": ("conferir_recibo_pre_selo do esboco R3.5 com ja_sincronizada=False (no B(n) da v404 o Nos sera a v404 e a Bancada ainda pinara a v403), sem cadeia de selos, "
             "selo e manifesto do kernel anteriores = copias de bytes v404/base_v403; producao so lida"),
    "script": {"path": os.path.abspath(__file__), "sha256": sha(os.path.abspath(__file__))},
    "esboco": {"path": ESB, "sha256": ESB_SHA, "revisao": getattr(MOD, "REVISAO", None)},
    "bateria": {"path": BAT, "sha256": BAT_SHA},
    "recibo": {"path": RP, "sha256": RSHA, "bytes": len(raw)},
    "selo_anterior": {"path": SELO_ANT, "sha256": sha(SELO_ANT)},
    "kernel_manifesto_anterior": {"path": KM_ANT, "sha256": sha(KM_ANT)},
    "bancada_de_producao_lida": {"deployment_id": ant["deployment_id"], "version": ant["version"], "manifesto_sha256": ant["sha256"], "um_py_pinado": ant["um_py_pinado"],
                                 "seal_sha_pinado": ant["seal_sha_pinado"], "estado_do_contrato_instalado": ant["estado_do_contrato_instalado"]},
    "esboco_aceita": aceito,
    "recusa_do_esboco": recusa,
    "resultado_do_esboco": resumo_res,
    "condicoes": checks,
    "n_condicoes": len(checks),
    "n_condicoes_ok": sum(1 for c in checks if c["ok"]),
    "controles_negativos": controles,
    "n_controles_como_esperado": sum(1 for c in controles if c["como_esperado"]),
    "utilizavel_como_recibo_pre_selo_do_B_n": utilizavel,
    "motivos_de_nao_ser_utilizavel": motivos,
    "validade": ("vale enquanto a Bancada de producao pinar o que esta em bancada_de_producao_lida (deployment_id, manifesto, um.py, selo); um re-pino da producao antes do "
                 "B(n) da v404 torna o recibo obsoleto e a conferencia o recusa"),
    "escopo": "so leitura da producao; nada gravado na Bancada nem no Nos; NOT_FALSIFIED nao e creditacao; o gate nao se move",
}
dest = os.path.join(HERE, "conferencia_pelo_esboco_v404.json")
if os.path.exists(dest):
    raise SystemExit("ja existe, nao sobrescrevo: " + dest)
dados = (json.dumps(conf, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
with open(dest + ".tmp", "wb") as fh:
    fh.write(dados)
if os.path.getsize(dest + ".tmp") != len(dados):
    raise SystemExit("tamanho do temporario nao confere")
os.replace(dest + ".tmp", dest)
print(json.dumps({"arquivo": dest, "sha16": sha(dest)[:16], "esboco_aceita": aceito, "recusa": recusa, "condicoes_ok": "%d/%d" % (conf["n_condicoes_ok"], conf["n_condicoes"]),
                  "controles_como_esperado": "%d/%d" % (conf["n_controles_como_esperado"], len(controles)), "utilizavel": utilizavel, "motivos": motivos}, ensure_ascii=False))
sys.exit(0 if utilizavel else 1)
