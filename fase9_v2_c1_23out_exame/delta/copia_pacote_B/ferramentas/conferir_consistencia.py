# -*- coding: utf-8 -*-
"""conferir_consistencia.py -- confere (so leitura) que spec, funcao, registro, runner, recibo de calibracao, testes e pedido estao em harmonia.
Rodar:  python -B -P -E -X utf8 ferramentas/conferir_consistencia.py   (sai com 1 se algo divergir)"""
import hashlib
import json
import os
import sys

sys.dont_write_bytecode = True

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda rel: open(os.path.join(ROOT, *rel.split("/")), "rb").read()
js = lambda rel: json.loads(rd(rel).decode("utf-8"))
bad = []


def chk(nome, ok):
    print(("OK    " if ok else "FALHA ") + nome)
    if not ok:
        bad.append(nome)


cal = js("calibracao/CALIBRACAO_CAUDA_RECIBO.json")
sp = js("spec/PREREGISTRO_FASE9_V2_C1_A_UNICA_PALAVRA.json")
reg = js("spec/REGISTRO_DH_V2_C1.json")
tests = js("testes/RESULTADO_TESTES.json")
ped = js("PEDIDO_DE_CONGELAMENTO.json")
pins = ped["o_recibo_pinara"]
chk("recibo de calibracao refere o spec canonico atual", cal["entradas"]["spec_canonico_sha256"] == sp["spec_sha256"])
chk("recibo de calibracao refere os modulos atuais do runner", all(sha(rd("runner/" + f))[:16] == h for f, h in cal["entradas"]["modulos_do_runner_sha16"].items())
    and sorted(cal["entradas"]["modulos_do_runner_sha16"]) == sorted(f for f in os.listdir(os.path.join(ROOT, "runner")) if f.endswith(".py")))
chk("recibo de calibracao refere a qualificacao do fundo atual", sha(rd("testes/QUALIFICACAO_FORNECEDOR_REAL.json")) == cal["entradas"]["qualificacao_fundo_sha256"])
chk("spec.registro_dh.sha256 = bytes do registro D-H", sp["spec"]["registro_dh"]["sha256"] == sha(rd("spec/REGISTRO_DH_V2_C1.json")))
chk("spec.funcao.sha256 = arquivo da funcao", sp["spec"]["funcao_de_veredito"]["sha256"] == sha(rd("spec/veredito_fase9_v2_c1.py")))
chk("spec_sha256 interno = forma canonica", sp["spec_sha256"] == sha(json.dumps(sp["spec"], sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")))
chk("fontes do spec = fontes do registro D-H = disco", all(sp["spec"]["leitores"][r]["documentary_source"]["sha256"] == v["sha256"] == sha(rd(v["file"])) for r, v in reg["leitores"].items()))
chk("testes: todos passam", tests["ok"] == tests["n"] and not tests["falhas"])
chk("pedido: pinos = arquivos atuais", all(sha(rd(p["path"])) == p["sha256"] for k, p in pins.items() if isinstance(p, dict) and "path" in p and "sha256" in p)
    and all(sha(rd(k)) == v["sha256"] for k, v in pins["runner_modulos"].items()) and all(sha(rd(v["path"])) == v["sha256"] for v in pins["fontes"].values()))
chk("pacote real intocado: sem freeze/, sem saidas/, sem ALVOS", not os.path.isdir(os.path.join(ROOT, "saidas")) and not os.path.exists(os.path.join(ROOT, "freeze", "RECIBO_DE_CONGELAMENTO.json"))
    and not os.path.exists(os.path.join(ROOT, "freeze", "RECIBO_DE_ABERTURA.json")) and not os.path.exists(os.path.join(ROOT, "freeze", "ABERTURA_CONSUMIDA.json")) and not any(f.startswith("REGISTRO_DE_RECUSA_") for f in (os.listdir(os.path.join(ROOT, "freeze")) if os.path.isdir(os.path.join(ROOT, "freeze")) else [])) and not any("ALVOS_FASE9_LIDOS.json" in fs for _d, _s, fs in os.walk(ROOT)))
sys.exit(1 if bad else 0)
