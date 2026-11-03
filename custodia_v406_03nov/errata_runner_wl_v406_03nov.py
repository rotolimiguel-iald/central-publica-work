# -*- coding: utf-8 -*-
"""03/11/2026 02:4x, gerencia c1: o C7 da G1 (runner da Fronteira, duas execucoes) parou na execucao 1 com VEREDITO FALHA_VERIFICACAO. A pedra da v406
(custodia_v406) PASSOU (REVISADA rev1, dois ceticos); quem reprovou foi a estacao historica `arco_v358_v368`, em `witness_layers_v367`: a condicao original
(v367/v375) exige `canonical_full_witness_term_constructed is False` — o estado medido de v367 a v405 (o nome `canonicalFullTGLWitness` ausente do axiom_report).
Desde a v406 o modulo TGLExt.F1Fecho394.CanonicalFullTGLWitnessR1 declara o nome exato e a chave e' LIDA do kernel: True (a quarta chave de testemunha; errata E14
AO LADO no um.py; registro selado fechamento_v406). A estacao congelou uma expectativa que o fecho virou — o mesmo caso da ERRATA v375 (runner v48) na mesma funcao.
Conserto AO LADO, no molde daquela errata: a linha original fica em comentario, intacta; aceita-se TAMBEM o estado lido do kernel (True) desde que o registro
fechamento_v406 esteja selado no mesmo core com all_verified e certificate_inhabited True e o termo canonico nomeado; full_static_witness_exists segue False por teorema.
O patch e' aplicado pelo mecanismo do proprio G1 (custodia_g1.patches.aplicar_em_arquivo: backup de BYTES, CRLF respeitado, py_compile no temporario, os.replace),
e o script roda o runner UMA vez depois, para conferir que o veredito volta a FRONTEIRA_SINCRONIZADA_V406 com arco_v358_v368.pass True; senao rc 1 (o backup fica).
Nada aqui toca o um.py, o selo, o core, o cofre ou o gate. Escrito pelo Write."""
import json, subprocess, sys, time
from pathlib import Path
CEN = Path(r"C:\IALD\Central de Patentes"); RUNNER = CEN / "fronteira_tgl" / "runner" / "one_fronteira.py"; RES = CEN / "fronteira_tgl" / "results"
sys.path.insert(0, str(CEN / "tools"))
from custodia_g1 import patches  # noqa: E402

OLD = ("    wl_ok = bool(wl.get(\"base_rigid_witness_constructed\") is True and wl.get(\"canonical_full_witness_term_constructed\") is False\n"
       "                 and wl.get(\"regular_full_witness_term_constructed\") is True and gate.get(\"full_static_witness_exists\") is False)\n")
NEW = ("    # ERRATA v406 (runner v70, AO LADO, 03/11/2026, gerencia c1): a condicao original (abaixo, intacta) exigia canonical_full_witness_term_constructed False,\n"
       "    # o estado medido de v367 a v405 (o nome canonicalFullTGLWitness ausente do axiom_report):\n"
       "    #     wl_ok = bool(wl.get(\"base_rigid_witness_constructed\") is True and wl.get(\"canonical_full_witness_term_constructed\") is False\n"
       "    #                  and wl.get(\"regular_full_witness_term_constructed\") is True and gate.get(\"full_static_witness_exists\") is False)\n"
       "    # desde a v406 o modulo TGLExt.F1Fecho394.CanonicalFullTGLWitnessR1 declara o nome exato e a chave e' LIDA do kernel (True), com a errata E14 ao lado no um.py;\n"
       "    # aceita-se TAMBEM esse estado, desde que o registro fechamento_v406 esteja selado no mesmo core (all_verified, certificate_inhabited, termo canonico nomeado).\n"
       "    # full_static_witness_exists segue False POR TEOREMA (o vazamento continuo proibe o fecho estatico); validade no kernel nao e' creditacao; o gate nao se move.\n"
       "    _f406 = core.get(\"fechamento_v406\") or {}\n"
       "    _cf_lida_v406 = bool(_f406.get(\"all_verified\") is True and _f406.get(\"certificate_inhabited\") is True\n"
       "                         and _f406.get(\"canonical_full_witness_term\") == \"TGL.ModularRealization.canonicalFullTGLWitness\")\n"
       "    _cf_ok = (wl.get(\"canonical_full_witness_term_constructed\") is False) or (wl.get(\"canonical_full_witness_term_constructed\") is True and _cf_lida_v406)\n"
       "    wl_ok = bool(wl.get(\"base_rigid_witness_constructed\") is True and _cf_ok\n"
       "                 and wl.get(\"regular_full_witness_term_constructed\") is True and gate.get(\"full_static_witness_exists\") is False)\n")


def f(s):
    assert s.count(OLD) == 1, "a linha original de wl_ok nao esta' UMA vez no runner (%d)" % s.count(OLD)
    assert "ERRATA v406 (runner v70, AO LADO" not in s, "a errata ja esta' no runner"
    return s.replace(OLD, NEW), ["1 wl_ok: errata v406 ao lado (canonical_full lida do kernel desde a v406)"]


r = patches.aplicar_em_arquivo(RUNNER, f, "v70_errata_wl_v406")
print("patch:", json.dumps(r, ensure_ascii=False))
assert r["estado"] == "aplicado"
# o 'ao lado' tambem no docstring da estacao, que descreve a expectativa (c): a frase antiga fica, a nova entra ao lado
s = RUNNER.read_bytes().decode("utf-8")
ant = "    (c) witness_layers (a errata da v367): base_rigid True, canonical_full False, regular_full True; full_static_witness_exists False;"
if s.count(ant) == 1:
    r2 = patches.aplicar_em_arquivo(RUNNER, lambda t: (t.replace(ant, ant + "\n        [AO LADO, v406, 03/11/2026: canonical_full passa a True desde a v406, LIDA do kernel (CanonicalFullTGLWitnessR1); aceita-se com o registro fechamento_v406 selado]"), ["2 docstring (c) ao lado"]), "v70_errata_wl_v406_doc")
    print("docstring:", json.dumps(r2, ensure_ascii=False))
# conferir: UMA execucao do runner
antes = set(p.name for p in RES.glob("fronteira_*.json"))
t0 = time.time()
q = subprocess.run([r"C:\Python314\python.exe", "-X", "utf8", "one_fronteira.py"], cwd=str(RUNNER.parent), capture_output=True, timeout=3600)
print("runner rc", q.returncode, "em %.0fs" % (time.time() - t0)); print(q.stdout.decode("utf-8", "replace")[-700:])
novos = sorted(p for p in RES.glob("fronteira_*.json") if p.name not in antes)
assert novos, "o runner nao gravou resultado"
d = json.loads(novos[-1].read_text(encoding="utf-8")); st = d.get("the_station") or {}
ruins = [k for k, x in st.items() if isinstance(x, dict) and x.get("pass") is False]
print("resultado:", novos[-1].name, "| verdict:", str(d.get("verdict"))[:90], "| pass False:", ruins, "| wl:", (st.get("arco_v358_v368") or {}).get("witness_layers_v367"))
assert q.returncode == 0 and str(d.get("verdict")).startswith("FRONTEIRA_SINCRONIZADA_V406") and not ruins and (st.get("custodia_v406") or {}).get("pass") is True, "o runner ainda reprova"
print("OK: o runner sincroniza a v406 com todas as estacoes passando")
