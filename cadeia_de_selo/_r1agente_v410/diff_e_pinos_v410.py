# -*- coding: utf-8 -*-
# [ADAPTADO v410 PARTE 2, 09/11/2026 (~18h), claude-subagente-adaptacao (Sonnet 5.5, A), a servico do construtor claude-construtor-v410] o bundle e' de DOIS modulos (IALD2 e AEscala: o diff do kernel acha os dois, a raiz muda; o Audit nao muda); PINOS NOVOS em PINOS_BN_v410.json (aditivos; as chaves antigas nao mudam): a pedra AEscala (a fonte ratificada e a embutida), o recibo dos nomes (sha16 do delta), as falas congeladas, os SEIS artefatos HMS/13 (as COPIAS duraveis insumos\hms13_*; a pasta do Kimi NAO e' aberta aqui), os fontes novos do construtor (registros/runtime da AEscala e do HMS/13), o recibo da parte 1 do HMS/13, o FLAGS e o KH_N1; tudo LIDO dos arquivos, com asserta contra o delta e o candidato (fail-closed)
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] o corpo le tudo do delta e do CANDIDATO (1 modulo, IALD2; a raiz; o Audit nao muda); pinos herdados de v409\PINOS_BN_v409.json (recalculados do arquivo); B19; so' a docstring mudou; conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
"""diff_e_pinos_v410.py -- (1) DIFF_KERNEL_v410.txt: arquivos novos (os modulos do bundle da v410, em TGLExt/: IALD2 e AEscala; o numero e' o de CANDIDATO_v410.json), removidos e mudados do kernel embutido do candidato contra o da v409 (com o diff da raiz; o Audit nao muda); (1b) DIFF_v409_v410.diff: `diff -u` do um.py da v409 selada (base_v409) contra o candidato (o registro da subida; texto, nao e' prova de nada); (2) PINOS_BN_v410.json: os sha256 que o elo B(n)
pede (esboco R3.5, gerador e driver da bateria, base R2, CRITERIOS, recibo do kernel, recibo pre_selo, selo e manifesto do kernel da v409 SELADA), LIDOS dos arquivos por script (o path e o sha256 de cada um sao recalculados aqui;
nada digitado). O recibo pre_selo e' o que o ensaio do B(n) gerou ANTES da instalacao (PINO_RECIBO_PRE_SELO_v410.json); ENQUANTO ELE NAO EXISTE (a preparacao ainda nao rodou o B(n) pre-selo) o pino dele e o da bateria do pre_selo saem `NAO_PREPARADO` e a lista `pendentes` os diz: pendente, nao erro do script. Nao ha salto de versoes (a Bancada pina a v409 e o Nos e' a v409): nao ha pino de cadeia de selos.
Molde: diff_e_pinos_v409.py (adaptado em 06/11/2026 ao bundle de UM modulo, IALD2, e em 09/11/2026 (parte 2) ao de DOIS, IALD2 e AEscala; os 2 da v409, os 4 da v408, os 9 da v407 e os 301 da v406 ficam no kernel como registro). Uso: python -I -B -X utf8 diff_e_pinos_v410.py   (roda DEPOIS de gerar_esperados_v410.py: o pino do ESPERADOS e' o do arquivo final. Se o ESPERADOS_v410.json ainda NAO existe, o pino dele sai `NAO_PREPARADO` e entra em `pendentes` -- dito na saida; o p00 e o refazer_candidato rodam este script DEPOIS do gerar_esperados, entao la' ele sai pinado)"""
import ast, difflib, hashlib, json, os, shutil, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "v390_pacote")); sys.path.insert(0, HERE)
from carregar_embutido import carregar  # noqa: E402
import delta_v410 as DL  # noqa: E402
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v410.json"), encoding="utf-8"))
sha = lambda b: hashlib.sha256(b).hexdigest()
BASE = os.path.join(HERE, DL.BASE_DIR)
E0, _, _, h0 = carregar(os.path.join(BASE, "um.py")); E1, _, _, h1 = carregar(os.path.join(HERE, DL.CANDIDATO))
novos = sorted(set(E1) - set(E0)); removidos = sorted(set(E0) - set(E1)); mudados = sorted(k for k in set(E0) & set(E1) if E0[k] != E1[k])
out = ["DIFF DO KERNEL EMBUTIDO v409 (%s) -> v410 (%s)" % (h0, h1), "", "novos (%d):" % len(novos)] + ["  + %s  %s  %d B" % (k, sha(E1[k].encode())[:16], len(E1[k].encode())) for k in novos]
out += ["", "removidos (%d):" % len(removidos)] + ["  - " + k for k in removidos] + ["", "mudados (%d):" % len(mudados)]
for k in mudados:
    a, b = E0[k].splitlines(), E1[k].splitlines(); d = list(difflib.unified_diff(a, b, "v409/" + k, "v410/" + k, lineterm="", n=0))
    out.append("  ~ %s  %s -> %s  (+%d linhas, -%d linhas)" % (k, sha(E0[k].encode())[:16], sha(E1[k].encode())[:16], sum(1 for l in d if l.startswith("+") and not l.startswith("+++")), sum(1 for l in d if l.startswith("-") and not l.startswith("---"))))
    out += ["      " + l[:200] for l in d[:40]]
open(os.path.join(HERE, "DIFF_KERNEL_v410.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("\n".join(out[:3]), "...", "novos", len(novos), "removidos", len(removidos), "mudados", mudados)
assert novos == sorted(DL.BUNDLE_RELS) and len(novos) == DL.N_BUNDLE == CM["kernel"]["modulos_novos"] and not removidos and sorted(mudados) == ["TGLExt.lean"], ("o diff do kernel nao e' so' os modulos do bundle (%d, em TGLExt/) + a raiz (o Audit nao muda na v410)" % DL.N_BUNDLE, len(novos), removidos, mudados)
assert all(k.startswith("TGLExt/") and k.count("/") == 1 for k in novos), ("os modulos novos da v410 vivem em TGLExt/ (nao em TGLExt/F1Fecho394/)", novos)
# (1b) o diff do um.py inteiro: diff -u do sistema (difflib seria quadratico em 40 MB); a base e' a copia de bytes do Nos v409 selado
_dif = shutil.which("diff"); _ddp = os.path.join(HERE, "DIFF_v409_v410.diff"); _ddm = {"ferramenta": _dif}
if _dif:
    _r = subprocess.run([_dif, "-u", "--label", "um.py v409 %s" % h0, "--label", "um.py v410 %s" % h1, os.path.join(BASE, "um.py"), os.path.join(HERE, DL.CANDIDATO)], capture_output=True)
    assert _r.returncode in (0, 1), ("diff -u falhou", _r.returncode, _r.stderr[:300])
    open(_ddp + ".tmp", "wb").write(_r.stdout); os.replace(_ddp + ".tmp", _ddp); _ddm.update({"rc": _r.returncode, "bytes": len(_r.stdout), "sha256": sha(_r.stdout)})
else:
    _ddm.update({"estado": "NAO_GERADO: diff -u nao esta no PATH"})
print("DIFF_v409_v410.diff:", _ddm)
V = os.path.join(HERE, "vinculo")
f = lambda p, **kw: dict({"path": p, "sha256": sha(open(p, "rb").read()), "bytes": os.path.getsize(p)}, **kw) if os.path.exists(p) else {"path": p, "sha256": None, "estado": "NAO_PREPARADO"}
_pino_pr = os.path.join(HERE, "PINO_RECIBO_PRE_SELO_v410.json"); pendentes = []
if os.path.exists(_pino_pr):
    pr = json.load(open(_pino_pr, encoding="utf-8"))
    assert sha(open(pr["path"], "rb").read()) == pr["sha256"], "o recibo pre-selo mudou desde o pino"
    rp = {"path": pr["path"], "sha256": pr["sha256"], "versao_nos": pr["versao_nos"], "veredito": pr["veredito"], "utilizavel_como_recibo_pre_selo_do_B_n": pr["utilizavel_como_recibo_pre_selo_do_B_n"], "pino_do_pino": f(_pino_pr),
          "um_py_sha16_do_nos": pr["um_py_sha16_do_nos"], "bancada_pina": pr["bancada_pina"], "sem_salto": True}
else:   # a preparacao ainda nao rodou o B(n) pre-selo (bateria_pre_selo\rodar_bn_pre_selo_v410.sh): PENDENTE, nao erro
    pr = None; rp = {"path": _pino_pr, "sha256": None, "estado": "NAO_PREPARADO", "motivo": "PINO_RECIBO_PRE_SELO_v410.json ainda nao existe: o B(n) pre-selo da v410 nao rodou"}; pendentes.append("recibo_pre_selo")
P4 = json.load(open(os.path.join(DL.V409, "PINOS_BN_v409.json"), encoding="utf-8"))   # a fusao R3.4/R3.5: o esboco, o gerador e o driver da bateria, a base R2 (so' leitura; o sha e' RECALCULADO do arquivo)
def do_v409(k):
    d = P4[k]; assert os.path.exists(d["path"]) and sha(open(d["path"], "rb").read()) == d["sha256"], ("o pino herdado da v409 diverge do arquivo", k)
    return f(d["path"], origem="PINOS_BN_v409.json[%s] (recalculado do arquivo)" % k)
kr = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, "KERNEL_RECIBO_v410.json"), encoding="utf-8"))
pn = {"criterios": f(os.path.join(V, "CRITERIOS_v410.json")), "kernel_recibo": f(os.path.join(HERE, DL.KERNEL_DIR, "KERNEL_RECIBO_v410.json"), contrato=kr["contrato"], n_pedras=len(kr["pedras"]), n_modulos=len(kr["pedras"]), modulos_de_auditoria=kr.get("modulos_de_auditoria", [])),
      "candidato": f(os.path.join(HERE, DL.CANDIDATO)), "esperados": f(os.path.join(HERE, "ESPERADOS_v410.json")), "pins_do_candidato": f(os.path.join(HERE, "v410_pins.py")),
      "esboco_R3_5": do_v409("esboco_R3_5"), "gerador_bateria": do_v409("gerador_bateria"), "driver_t12_t14": do_v409("driver_t12_t14"), "bateria_base_R2": do_v409("bateria_base_R2"),
      "bateria_do_pre_selo": (f(pr["bateria"]["path"], versao="v409", nota="a bateria do ensaio pre_selo (a da v409 gerada e pinada na cadeia anterior); a do POS_SELO da v410 e' GERADA pelo chain depois do selo") if pr else {"path": None, "sha256": None, "estado": "NAO_PREPARADO", "motivo": "depende do recibo pre_selo"}),
      "recibo_pre_selo": rp,
      "selo_anterior_v409": f(os.path.join(BASE, "um_absoluto_selo.json"), nota="o selo da v409 (custodia, o FIM da cadeia anterior): --selo-anterior"),
      "kernel_manifesto_anterior_v409": f(os.path.join(BASE, "tgl_kernel_proof_manifest.json"), nota="o manifesto do kernel da v409 (custodia): --kernel-manifesto-anterior"),
      "nota": "[REAL] lido dos arquivos por script (diff_e_pinos_v410.py): path e sha256 RECALCULADOS; sem salto de versoes (a Bancada de producao pina a v409 = o Nos de antes da instalacao), logo sem pino de cadeia de selos nem 3o argumento do b3_recibo; "
              "o esboco R3.5 e a bateria/driver sao os da cadeia anterior (R3_5), reaproveitados; o passo da Bancada na v410 e' o simples v409 -> v410 (o B(n) seguinte e' %s, lido de delta_v410.B_N_SEGUINTE; a Bancada pina %s); os vereditos esperados desse passo sao os do codigo do esboco R3.5, lidos pelo exame do pre_selo, nao rodados aqui (a narrativa REPINADA_B13__ da cadeia anterior nao vale para o B19)." % (DL.B_N_SEGUINTE, DL.BANCADA_PINA_HOJE["deployment_id"])}
if pr is None:
    pendentes.append("bateria_do_pre_selo")
if pn["esperados"].get("sha256") is None:   # (v410) o ESPERADOS e' gerado por gerar_esperados_v410.py, que no refazer_candidato roda ANTES deste script; numa corrida avulsa anterior a ele, o pino sai pendente (nao pinado), dito aqui e em `pendentes`
    pendentes.append("esperados")
    print("AVISO: ESPERADOS_v410.json ainda NAO existe (gerar_esperados_v410.py nao rodou): o pino dele sai NAO_PREPARADO e entra em `pendentes`; REFACA este script depois do gerar_esperados antes de qualquer uso do PINOS_BN_v410.json")
# ---- [v410, PARTE 2: D80 a D87] os pinos NOVOS, lidos dos arquivos (path e sha256 RECALCULADOS) e conferidos contra o delta e o candidato: fail-closed; as COPIAS duraveis dos seis artefatos HMS/13 (nunca a pasta do Kimi)
_hm13 = CM["hms13"]["pinos_build"]; _INS = os.path.join(HERE, "insumos")
_rs = DL.BUNDLE_POR_REL[DL.MODULO_AESCALA]
pn["pedra_aescala_fonte"] = f(os.path.join(_INS, "AEscala.lean"), origem_do_pino="DL.BUNDLE_POR_REL[TGLExt/AEscala.lean].sha256_origem", nota="a fonte RATIFICADA (D87; com os #print axioms): a que o preparo pinou")
pn["pedra_aescala_embutida"] = f(os.path.join(HERE, "pedra", "AEscala.lean"), origem_do_pino="DL.BUNDLE_POR_REL[TGLExt/AEscala.lean].sha256", nota="a copia normalizada que entra no kernel embutido do candidato (o cabecalho da ratificacao da D87; sem #print axioms)")
pn["pedra_aescala_embutida_insumo"] = f(os.path.join(_INS, "AEscala_embutida.lean"), nota="a copia duravel da embutida (== pedra\\AEscala.lean == o sandbox == o candidato)")
pn["recibo_pedras_nomes"] = f(DL.RECIBO_NOMES_ARQ, sha16_do_delta=DL.RECIBO_NOMES_SHA16, n_modulos=DL.N_BUNDLE, n_falas=DL.N_FALAS_V410, nota="o recibo dos nomes das pedras (os modulos do bundle, as falas congeladas, a ratificacao da D74 e a da D87, e os nomes novos da R3 a ratificar); por sha16 no delta")
pn["verbatim_congelado"] = f(os.path.join(HERE, "VERBATIM_CONGELADO_v410.json"), n=DL.N_FALAS_V410, nota="a lista congelada das falas embutidas")
pn["parte1_hms13_pronta"] = f(os.path.join(HERE, "PARTE1_HMS13_PRONTA.json"), nota="o recibo da parte 1 (o recibo documental HMS/13, D80)")
pn["kernel_flags"] = f(os.path.join(HERE, DL.KERNEL_DIR, "FLAGS_v410.json"), n_flags=CM["n_bandeiras"], por_modulo=dict((json.load(open(os.path.join(HERE, DL.KERNEL_DIR, "FLAGS_v410.json"), encoding="utf-8")) or {}).get("n_por_modulo") or {}))
pn["kernel_kh_n1"] = f(os.path.join(HERE, DL.KERNEL_DIR, DL.KH_N1_INSUMO))
for _nome in ("registros_aescala_v410.py", "runtime_aescala_v410.py", "registros_hms13_v410.py", "runtime_hms13_v410.py"):
    pn["fonte_" + _nome[:-len(".py")]] = f(os.path.join(HERE, _nome), nota="fonte autoral do construtor (parte 2): o contrato e o texto do registro sao DERIVADOS dela no gerador")
for _k, _v in _hm13.items():   # os seis artefatos documentais da EXCECAO D80: a COPIA duravel (insumos\hms13_<nome>), por sha256 == o pino do candidato (que o BUILD conferiu contra o HANDOFF e a ORDEM)
    pn["hms13_" + _k] = f(os.path.join(_INS, "hms13_" + _k), sha256_do_pino_do_candidato=_v["sha256"], bytes_do_pino_do_candidato=_v["bytes"], nota="copia duravel (a origem fica sob a pasta do Kimi e NAO e' aberta aqui; excecao D80)")
assert pn["pedra_aescala_fonte"]["sha256"] == _rs["sha256_origem"] and pn["pedra_aescala_embutida"]["sha256"] == _rs["sha256"] == pn["pedra_aescala_embutida_insumo"]["sha256"] == CM["aescala"]["source_sha256"][DL.MODULO_AESCALA], "a pedra AEscala (fonte ou embutida) em disco != o pino do bundle/candidato"
assert (pn["recibo_pedras_nomes"].get("sha256") or "")[:16] == DL.RECIBO_NOMES_SHA16, "o recibo dos nomes em disco != o sha16 do delta"
assert all((pn["hms13_" + _k].get("sha256") == _v["sha256"] and pn["hms13_" + _k].get("bytes") == _v["bytes"]) for _k, _v in _hm13.items()), "uma copia duravel do HMS/13 != o pino do candidato"
bad = [k for k, v in pn.items() if isinstance(v, dict) and "path" in v and v.get("sha256") is None and k not in pendentes]
assert not bad, ("pino sem arquivo", bad)
pn["pendentes"] = pendentes   # o que so' passa a existir depois do B(n) pre-selo; o p00 diz PENDENTE para eles
json.dump(pn, open(os.path.join(HERE, "PINOS_BN_v410.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({k: (v["sha256"] or "NAO_PREPARADO")[:16] for k, v in pn.items() if isinstance(v, dict) and "sha256" in v}); print("pendentes:", pendentes or "nenhum")
