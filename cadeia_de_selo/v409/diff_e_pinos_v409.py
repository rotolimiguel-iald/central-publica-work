# -*- coding: utf-8 -*-
# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] o corpo le tudo do delta e do CANDIDATO (1 modulo, a raiz; o Audit nao muda); so' a docstring mudou sobre a subida de rotulo
"""diff_e_pinos_v409.py -- (1) DIFF_KERNEL_v409.txt: arquivos novos (o modulo do bundle da v409, em TGLExt/: 1 pelo DESENHO_v409, TraducaoTuring; o numero e' o de CANDIDATO_v409.json), removidos e mudados do kernel embutido do candidato contra o da v408 (com o diff da raiz; o Audit nao muda); (1b) DIFF_v408_v409.diff: `diff -u` do um.py da v408 selada (base_v408) contra o candidato (o registro da subida; texto, nao e' prova de nada); (2) PINOS_BN_v409.json: os sha256 que o elo B(n)
pede (esboco R3.5, gerador e driver da bateria, base R2, CRITERIOS, recibo do kernel, recibo pre_selo, selo e manifesto do kernel da v408 SELADA), LIDOS dos arquivos por script (o path e o sha256 de cada um sao recalculados aqui;
nada digitado). O recibo pre_selo e' o que o ensaio do B(n) gerou ANTES da instalacao (PINO_RECIBO_PRE_SELO_v409.json); ENQUANTO ELE NAO EXISTE (a preparacao ainda nao rodou o B(n) pre-selo) o pino dele e o da bateria do pre_selo saem `NAO_PREPARADO` e a lista `pendentes` os diz: pendente, nao erro do script. Nao ha salto de versoes (a Bancada pina a v408 e o Nos e' a v408): nao ha pino de cadeia de selos.
Molde: diff_e_pinos_v408.py (adaptado em 05/11/2026 ao bundle de UM modulo, TraducaoTuring; os 4 da v408, os 9 da v407 e os 301 da v406 ficam no kernel como registro). Uso: python -I -B -X utf8 diff_e_pinos_v409.py   (roda DEPOIS de gerar_esperados_v409.py: o pino do ESPERADOS e' o do arquivo final. Se o ESPERADOS_v409.json ainda NAO existe, o pino dele sai `NAO_PREPARADO` e entra em `pendentes` -- dito na saida; o p00 e o refazer_candidato rodam este script DEPOIS do gerar_esperados, entao la' ele sai pinado)"""
import ast, difflib, hashlib, json, os, shutil, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "v390_pacote")); sys.path.insert(0, HERE)
from carregar_embutido import carregar  # noqa: E402
import delta_v409 as DL  # noqa: E402
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v409.json"), encoding="utf-8"))
sha = lambda b: hashlib.sha256(b).hexdigest()
BASE = os.path.join(HERE, DL.BASE_DIR)
E0, _, _, h0 = carregar(os.path.join(BASE, "um.py")); E1, _, _, h1 = carregar(os.path.join(HERE, DL.CANDIDATO))
novos = sorted(set(E1) - set(E0)); removidos = sorted(set(E0) - set(E1)); mudados = sorted(k for k in set(E0) & set(E1) if E0[k] != E1[k])
out = ["DIFF DO KERNEL EMBUTIDO v408 (%s) -> v409 (%s)" % (h0, h1), "", "novos (%d):" % len(novos)] + ["  + %s  %s  %d B" % (k, sha(E1[k].encode())[:16], len(E1[k].encode())) for k in novos]
out += ["", "removidos (%d):" % len(removidos)] + ["  - " + k for k in removidos] + ["", "mudados (%d):" % len(mudados)]
for k in mudados:
    a, b = E0[k].splitlines(), E1[k].splitlines(); d = list(difflib.unified_diff(a, b, "v408/" + k, "v409/" + k, lineterm="", n=0))
    out.append("  ~ %s  %s -> %s  (+%d linhas, -%d linhas)" % (k, sha(E0[k].encode())[:16], sha(E1[k].encode())[:16], sum(1 for l in d if l.startswith("+") and not l.startswith("+++")), sum(1 for l in d if l.startswith("-") and not l.startswith("---"))))
    out += ["      " + l[:200] for l in d[:40]]
open(os.path.join(HERE, "DIFF_KERNEL_v409.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("\n".join(out[:3]), "...", "novos", len(novos), "removidos", len(removidos), "mudados", mudados)
assert novos == sorted(DL.BUNDLE_RELS) and len(novos) == DL.N_BUNDLE == CM["kernel"]["modulos_novos"] and not removidos and sorted(mudados) == ["TGLExt.lean"], ("o diff do kernel nao e' so' os modulos do bundle (%d, em TGLExt/) + a raiz (o Audit nao muda na v409)" % DL.N_BUNDLE, len(novos), removidos, mudados)
assert all(k.startswith("TGLExt/") and k.count("/") == 1 for k in novos), ("os modulos novos da v409 vivem em TGLExt/ (nao em TGLExt/F1Fecho394/)", novos)
# (1b) o diff do um.py inteiro: diff -u do sistema (difflib seria quadratico em 40 MB); a base e' a copia de bytes do Nos v408 selado
_dif = shutil.which("diff"); _ddp = os.path.join(HERE, "DIFF_v408_v409.diff"); _ddm = {"ferramenta": _dif}
if _dif:
    _r = subprocess.run([_dif, "-u", "--label", "um.py v408 %s" % h0, "--label", "um.py v409 %s" % h1, os.path.join(BASE, "um.py"), os.path.join(HERE, DL.CANDIDATO)], capture_output=True)
    assert _r.returncode in (0, 1), ("diff -u falhou", _r.returncode, _r.stderr[:300])
    open(_ddp + ".tmp", "wb").write(_r.stdout); os.replace(_ddp + ".tmp", _ddp); _ddm.update({"rc": _r.returncode, "bytes": len(_r.stdout), "sha256": sha(_r.stdout)})
else:
    _ddm.update({"estado": "NAO_GERADO: diff -u nao esta no PATH"})
print("DIFF_v408_v409.diff:", _ddm)
V = os.path.join(HERE, "vinculo")
f = lambda p, **kw: dict({"path": p, "sha256": sha(open(p, "rb").read()), "bytes": os.path.getsize(p)}, **kw) if os.path.exists(p) else {"path": p, "sha256": None, "estado": "NAO_PREPARADO"}
_pino_pr = os.path.join(HERE, "PINO_RECIBO_PRE_SELO_v409.json"); pendentes = []
if os.path.exists(_pino_pr):
    pr = json.load(open(_pino_pr, encoding="utf-8"))
    assert sha(open(pr["path"], "rb").read()) == pr["sha256"], "o recibo pre-selo mudou desde o pino"
    rp = {"path": pr["path"], "sha256": pr["sha256"], "versao_nos": pr["versao_nos"], "veredito": pr["veredito"], "utilizavel_como_recibo_pre_selo_do_B_n": pr["utilizavel_como_recibo_pre_selo_do_B_n"], "pino_do_pino": f(_pino_pr),
          "um_py_sha16_do_nos": pr["um_py_sha16_do_nos"], "bancada_pina": pr["bancada_pina"], "sem_salto": True}
else:   # a preparacao ainda nao rodou o B(n) pre-selo (bateria_pre_selo\rodar_bn_pre_selo_v409.sh): PENDENTE, nao erro
    pr = None; rp = {"path": _pino_pr, "sha256": None, "estado": "NAO_PREPARADO", "motivo": "PINO_RECIBO_PRE_SELO_v409.json ainda nao existe: o B(n) pre-selo da v409 nao rodou"}; pendentes.append("recibo_pre_selo")
P4 = json.load(open(os.path.join(DL.V408, "PINOS_BN_v408.json"), encoding="utf-8"))   # a fusao R3.4/R3.5: o esboco, o gerador e o driver da bateria, a base R2 (so' leitura; o sha e' RECALCULADO do arquivo)
def do_v408(k):
    d = P4[k]; assert os.path.exists(d["path"]) and sha(open(d["path"], "rb").read()) == d["sha256"], ("o pino herdado da v408 diverge do arquivo", k)
    return f(d["path"], origem="PINOS_BN_v408.json[%s] (recalculado do arquivo)" % k)
kr = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, "KERNEL_RECIBO_v409.json"), encoding="utf-8"))
pn = {"criterios": f(os.path.join(V, "CRITERIOS_v409.json")), "kernel_recibo": f(os.path.join(HERE, DL.KERNEL_DIR, "KERNEL_RECIBO_v409.json"), contrato=kr["contrato"], n_pedras=len(kr["pedras"]), n_modulos=len(kr["pedras"]), modulos_de_auditoria=kr.get("modulos_de_auditoria", [])),
      "candidato": f(os.path.join(HERE, DL.CANDIDATO)), "esperados": f(os.path.join(HERE, "ESPERADOS_v409.json")), "pins_do_candidato": f(os.path.join(HERE, "v409_pins.py")),
      "esboco_R3_5": do_v408("esboco_R3_5"), "gerador_bateria": do_v408("gerador_bateria"), "driver_t12_t14": do_v408("driver_t12_t14"), "bateria_base_R2": do_v408("bateria_base_R2"),
      "bateria_do_pre_selo": (f(pr["bateria"]["path"], versao="v408", nota="a bateria do ensaio pre_selo (a da v408 gerada e pinada na cadeia anterior); a do POS_SELO da v409 e' GERADA pelo chain depois do selo") if pr else {"path": None, "sha256": None, "estado": "NAO_PREPARADO", "motivo": "depende do recibo pre_selo"}),
      "recibo_pre_selo": rp,
      "selo_anterior_v408": f(os.path.join(BASE, "um_absoluto_selo.json"), nota="o selo da v408 (custodia, o FIM da cadeia anterior): --selo-anterior"),
      "kernel_manifesto_anterior_v408": f(os.path.join(BASE, "tgl_kernel_proof_manifest.json"), nota="o manifesto do kernel da v408 (custodia): --kernel-manifesto-anterior"),
      "nota": "[REAL] lido dos arquivos por script (diff_e_pinos_v409.py): path e sha256 RECALCULADOS; sem salto de versoes (a Bancada de producao pina a v408 = o Nos de antes da instalacao), logo sem pino de cadeia de selos nem 3o argumento do b3_recibo; "
              "o esboco R3.5 e a bateria/driver sao os da cadeia anterior (R3_5), reaproveitados; o passo da Bancada na v409 e' o simples v408 -> v409 (o B(n) seguinte e' %s, lido de delta_v409.B_N_SEGUINTE; a Bancada pina %s); os vereditos esperados desse passo sao os do codigo do esboco R3.5, lidos pelo exame do pre_selo, nao rodados aqui (a narrativa REPINADA_B13__ da cadeia anterior nao vale para o B18)." % (DL.B_N_SEGUINTE, DL.BANCADA_PINA_HOJE["deployment_id"])}
if pr is None:
    pendentes.append("bateria_do_pre_selo")
if pn["esperados"].get("sha256") is None:   # (v409) o ESPERADOS e' gerado por gerar_esperados_v409.py, que no refazer_candidato roda ANTES deste script; numa corrida avulsa anterior a ele, o pino sai pendente (nao pinado), dito aqui e em `pendentes`
    pendentes.append("esperados")
    print("AVISO: ESPERADOS_v409.json ainda NAO existe (gerar_esperados_v409.py nao rodou): o pino dele sai NAO_PREPARADO e entra em `pendentes`; REFACA este script depois do gerar_esperados antes de qualquer uso do PINOS_BN_v409.json")
bad = [k for k, v in pn.items() if isinstance(v, dict) and "path" in v and v.get("sha256") is None and k not in pendentes]
assert not bad, ("pino sem arquivo", bad)
pn["pendentes"] = pendentes   # o que so' passa a existir depois do B(n) pre-selo; o p00 diz PENDENTE para eles
json.dump(pn, open(os.path.join(HERE, "PINOS_BN_v409.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({k: (v["sha256"] or "NAO_PREPARADO")[:16] for k, v in pn.items() if isinstance(v, dict) and "sha256" in v}); print("pendentes:", pendentes or "nenhum")
