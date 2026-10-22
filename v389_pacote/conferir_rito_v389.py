# -*- coding: utf-8 -*-
"""conferir_rito_v389.py -- confere, DEPOIS do rito v389, o que tinha de mudar e o que NAO podia (ESPERADOS_v389.json; so leitura do Nos). Molde: conferir_rito_v388.py.
A v389 e' so texto e rotulo: NENHUM veredito da v388 pode mudar; a escada fica 6154; as bandeiras True ficam as mesmas; o iii1_net_image fica igual salvo o rotulo."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
umsha = hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()[:16]
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v389.json"), encoding="utf-8"))
kf = core.get("kernel_formalization") or {}; axr = kf.get("axiom_report") or {}
V = lambda k: str((core.get(k) or {}).get("verdict") or "")
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
VELHO = "CLOCK_TORSION_" + "CONF" + "IRMED_ON_PHYSICAL_NET"
qg = core.get("qg_closure") or {}; n18 = sum(1 for fam in ("formal_flags", "physics_flags", "experiment_flags") for v in (qg.get(fam) or {}).values() if v is True)
esc = core.get("external_ladder") or {}; qp = core.get("quantum_pillar_v384") or {}
txt = {l: re.sub(r"\s+", " ", open(os.path.join(NOS, "um_absoluto_%s.txt" % l), encoding="utf-8", errors="replace").read()) for l in ("pt", "en")}
toc = {l: (open(os.path.join(NOS, "um_absoluto_%s.toc" % l), encoding="utf-8", errors="replace").read().replace("\n", "").replace("$\\to $", "→") if os.path.exists(os.path.join(NOS, "um_absoluto_%s.toc" % l)) else "") for l in ("pt", "en")}
fc = open(os.path.join(NOS, "um_absoluto_forma_canonica.md"), encoding="utf-8", errors="replace").read(); mf = open(os.path.join(NOS, "um_absoluto_manifest.md"), encoding="utf-8", errors="replace").read()
tl = core.get("text_label_errata_v389") or {}; im = core.get("iii1_net_image") or {}
reused = qp.get("mode") == "REUSE"; computed = qp.get("mode") == "COMPUTE"
_im_sem = {k: v for k, v in im.items() if k not in ("seals", "seals_errata_v389")}
_s0 = ESP["iii1_seals_v388"]
DEVE = {
    "um.py = o candidato (sha16 %s)" % ESP["candidato_sha16"]: umsha == ESP["candidato_sha16"],
    "selo um_version v389; o registro v389 no selo igual ao core": selo.get("um_version") == "v389" and (selo.get("text_label_errata_v389") or {}).get("verdict") == V("text_label_errata_v389") and V("text_label_errata_v389"),
    "o registro v389 SELOU e = o pinado do ensaio": tl.get("all_verified") is True and V("text_label_errata_v389") == ESP["veredito_v389_do_ensaio"],
    "o rotulo novo no core; o velho so no campo da errata; o resto do iii1_net_image igual": im.get("seals") == [ESP["rotulo_novo"] if s == VELHO else s for s in _s0] and VELHO not in (im.get("seals") or [])
        and (im.get("seals_errata_v389") or {}).get("old") == VELHO and json.dumps(_im_sem, sort_keys=True) == json.dumps(ESP["iii1_sem_rotulo"], sort_keys=True),
    "o artigo PT/EN traz as frases novas e a secao v389 (antes da v388)": all(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_marcas"][l])
        and all(txt[l].rfind(ESP["artigo_marcas"][l][0]) < txt[l].rfind(ESP["artigo_marcas"][l][-1]) for l in ("pt", "en")) and all(V("text_label_errata_v389") in txt[l].replace("_ ", "_") for l in ("pt", "en")),
    "o artigo PT/EN NAO traz as frases velhas nem o rotulo velho": not any(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_nao"][l]) and not any(VELHO in txt[l].replace("_ ", "_") for l in ("pt", "en")),
    "o sumario lista «Ao lado (v389)», «(v388)» e o titulo novo da Introducao": all(w in toc[l] for l in ("pt", "en") for w in ESP["toc"][l]),
    "o .md canonico: carimbo v389, «Ao lado (v389)», o rotulo novo e o velho ausente; carimbo = sha16 do um.py": ESP["md_carimbo"] in fc and ESP["md_carimbo"] in mf and ESP["md_ao_lado"] in fc
        and ESP["rotulo_novo"] in fc and VELHO not in fc and ("sha256/16 `%s`" % umsha) in fc,
    "o pilar reaproveitado pela mesma chave -- ou calculado de novo, DITO": (reused and qp.get("key") == ESP["pilar"]["key"] and qp.get("result_sha256") == ESP["pilar"]["result_sha256"] and V("quantum_pillar_v384") == ESP["pilar"]["verdict"]) or computed,
}
mud = {k: (v, V(k)) for k, v in ESP["vereditos_v388"].items() if V(k) != v}
# A UNICA diferenca DITA nos registros do selo (achada na 1a conferencia, que reprovou e fica como registro: conferencia_rito_v389_PRIMEIRA_NAO_BATE.json):
# beta_runs_bounded_below_v388.memory_file.on_disk_matches True -> False, porque a CADEIA DE SELO DA v388 acrescentou um bloco a memoria-topico que o registro confere por sha.
# So se aceita com a PROVA: o sha pinado = o do backup _sup388 (o estado ANTES da cadeia v388) e o arquivo atual comeca por esses bytes (so acrescimo).
_MEM = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "beta-escalar-limitado-inferiormente-06out.md")
_bk388 = [os.path.join(os.path.dirname(_MEM), f) for f in os.listdir(os.path.dirname(_MEM)) if f.startswith(os.path.basename(_MEM) + ".bak_") and f.endswith("_sup388")]


def _so_o_acrescimo_da_cadeia_v388(esperado, atual):
    try:
        if json.dumps(esperado, sort_keys=True) == json.dumps(atual, sort_keys=True):
            return True
        e2 = json.loads(json.dumps(esperado)); a2 = json.loads(json.dumps(atual))
        pin = ((e2.get("memory_file") or {}).get("sha256"))
        if not (len(_bk388) == 1 and (e2.get("memory_file") or {}).get("on_disk_matches") is True and (a2.get("memory_file") or {}).get("on_disk_matches") is False):
            return False
        bk = open(_bk388[0], "rb").read(); cur = open(_MEM, "rb").read()
        if not (hashlib.sha256(bk).hexdigest() == pin and cur.startswith(bk) and len(cur) > len(bk)):
            return False
        a2["memory_file"]["on_disk_matches"] = True
        return json.dumps(e2, sort_keys=True) == json.dumps(a2, sort_keys=True)
    except (OSError, ValueError, AttributeError, TypeError):
        return False
_ft = sorted(k for k, v in kf.items() if v is True)
NAO = {
    "qg_closure_verdict inteiro": selo.get("qg_closure_verdict") == ESP["qg_closure_verdict"],
    "beta, alpha, omega_I": core.get("beta") == ESP["beta"] and core.get("alpha") == ESP["alpha"] and core.get("omega_I") == ESP["omega_I"],
    "a escada segue 6154/6154": [esc.get("n_theorems_clean"), esc.get("n_theorems_expected")] == ESP["escada"],
    "18 bandeiras do gate; sem sorryAx": n18 == 18 and not any("sorryAx" in a for v in axr.values() for a in (v or [])),
    "bandeiras True = as da v388, exatamente": _ft == ESP["flags_true_v388"],
    "NENHUM veredito da v388 mudou (%d mudaram)" % len(mud): not mud,
    "os registros v388/v387 do selo inalterados (salvo a diferenca DITA: memory_file.on_disk_matches da v388, provada so-acrescimo da cadeia v388)":
        all((json.dumps(selo.get(k), sort_keys=True) == json.dumps(v, sort_keys=True)) or (k == "beta_runs_bounded_below_v388" and _so_o_acrescimo_da_cadeia_v388(v, selo.get(k))) for k, v in ESP["selo_registros_v388"].items()),
    "nao selados inalterados": sorted((selo.get("not_sealed_this_run") or {}).get("formais") or []) == ESP["not_sealed_formais"] and sorted((selo.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []) == ESP["not_sealed_recusas"],
    "nenhum veredito proibido": not [k for k, m in core.items() if isinstance(m, dict) and GUARDA.search(str(m.get("verdict") or ""))],
    "selftest e rodada completa": selo.get("fail_closed_selftest") == "FAIL_CLOSED_SELFTEST_PASSED" and (selo.get("rite_checkpoints") or {}).get("switch_on") is False,
}
res = {"um_py_sha16": umsha, "deve_mudar": DEVE, "nao_pode_mudar": NAO, "vereditos_que_mudaram": mud, "pilar": {k: qp.get(k) for k in ("mode", "key", "result_sha256", "verdict")}}
for sec in ("deve_mudar", "nao_pode_mudar"):
    print("==", sec)
    for k, v in res[sec].items():
        print("  [%s] %s" % ("OK " if v else "NAO", k))
if mud:
    print("vereditos que mudaram:", json.dumps({k: v[1][:160] for k, v in mud.items()}, ensure_ascii=False)[:1500])
_lg = os.path.join(HERE, "rito_servidor_v389.log"); _lt = open(_lg, encoding="utf-8", errors="replace").read() if os.path.exists(_lg) else ""
res["servidor_depois_do_rito"] = "RELIGADO (a porta 8081 escuta)" if "servidor de volta" in _lt else ("nao religado: nao estava ligado antes" if "nao religo" in _lt else "ver o log do lancador")
res["marcador_ficou"] = os.path.exists(os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work", "v389_pacote", ".servidor_parado_pelo_rito"))
print("servidor:", res["servidor_depois_do_rito"], "| marcador ficou:", res["marcador_ficou"])
ok = all(DEVE.values()) and all(NAO.values()); res["tudo_bate"] = ok
p = os.path.join(HERE, "conferencia_rito_v389%s.json" % (sys.argv[1] if len(sys.argv) > 1 else ""))
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1, default=str)); os.replace(p + ".tmp", p)
print("TUDO BATE" if ok else "NAO BATE"); sys.exit(0 if ok else 1)
