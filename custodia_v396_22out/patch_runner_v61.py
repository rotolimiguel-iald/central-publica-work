# -*- coding: utf-8 -*-
"""Runner da Fronteira v61 (custódia v396 na Central, 22/10/2026, sessão a7; ordem do operador: «Atualize tudo com a nova versão do
um.py»): REPIN v395->v396; a pedra v44 já lê o cofre v395 pelo nome (nascida assim na v60): NENHUMA errata é necessária. Pedra nova
custodia_v396 (v45) com DOIS CÉTICOS, que lê o cofre v396 e o v395 PELO NOME. Medido em 22/10 (work/custodia_v396_22out/
medir_v396_contra_v395.py): 3 blocos novos (cunhagens_v396, kh_n1_cobertura_v396, testemunha_estatica_v396), nenhum sumido; 47 chaves
novas no kernel_formalization; registro 364 (PT == EN) com os 361 da v395 e 5 vereditos mudados (a troca numérica da escada); kernel
1425/29228 no trio; gate idêntico."""
import os, subprocess, sys
from datetime import datetime
R = r"C:\IALD\Central de Patentes\fronteira_tgl\runner\one_fronteira.py"
TS = datetime.now().strftime("%Y%m%d_%H%M%S")
raw = open(R, "rb").read(); s = raw.decode("utf-8"); nl = "\r\n" if "\r\n" in s else "\n"
if "_medir_v396_custodia" in s: raise SystemExit("ja aplicado")
open(R + ".bak_v61_" + TS, "wb").write(raw)


def troca(velho, novo, rot, n=1):
    global s
    v_, n_ = velho.replace("\n", nl), novo.replace("\n", nl); c = s.count(v_)
    assert c == n, (rot, c); s = s.replace(v_, n_); print("  ok ", rot)


troca('"""FRONTEIRA TEORICA TGL v60 — auto-auditoria honesta do fechamento, SINCRONIZADA ao um.py v395.',
      '"""FRONTEIRA TEORICA TGL v61 — auto-auditoria honesta do fechamento, SINCRONIZADA ao um.py v396.', "cabecalho v61")
troca("  A custodia viva passou a ser vault/originals_copy/um_unificado_v395. O RENOME v209: o selo",
      "  A custodia viva passou a ser vault/originals_copy/um_unificado_v396. O RENOME v209: o selo", "docstring custodia")
troca("(1424 arquivos formais no manifesto v395; entre", "(1425 arquivos formais no manifesto v396; entre", "docstring kernel")
troca("Fonte canonica sincronizada (custodia): um.py unificado v395 (pin", "Fonte canonica sincronizada (custodia): um.py unificado v396 (pin", "docstring fonte")
troca('CUSTODY_DIR = CENTRAL_DIR / "vault" / "originals_copy" / "um_unificado_v395"',
      'CUSTODY_DIR = CENTRAL_DIR / "vault" / "originals_copy" / "um_unificado_v396"', "CUSTODY_DIR")
troca('print(f"[fronteira v30] CUSTODIA um.py v395: pin', 'print(f"[fronteira v30] CUSTODIA um.py v396: pin', "print custodia")

FUNC = r'''
def _medir_v396_custodia():
    """v61 (custodia v396 na Central, 22/10/2026): o COFRE v396 contra o COFRE v395, lidos PELO NOME (exata para sempre). DOIS CETICOS.
    Medido em 22/10/2026: (a) 3 blocos novos no nucleo (cunhagens_v396, kh_n1_cobertura_v396, testemunha_estatica_v396), nenhum sumido;
    cada um all_verified, does_not_gate_core, sem CONFIRMED e com GATE_UNMOVED/GATE_UNTOUCHED; (b) 47 chaves novas no kernel_formalization;
    (c) os registros: testemunha_estatica_v396 com a composicao INCONDICIONAL the_psion_inhabits_the_static_witness (bandeira True, no trio,
    nenhum certificado como hipotese), a face de Fock do psion CONDICIONAL (CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE, sem habitante, fora
    da pedra), 19 termos da pedra e 8 de apoio, a mecanica numerica aprovada; cunhagens_v396 com 3 falas por sha256; kh_n1_cobertura_v396
    29228 constantes / 23227 teoremas, nenhum fora do trio; o estatuto com a escada 9498/9498 (KERNEL_9498_OF_9498_FLAGS) e 29228 no trio;
    (d) gate identico ao do cofre v395; um_version v396; (e) registro PT == EN == 364, os 361 nomes da v395 presentes, os novos = os 3
    blocos, e so 5 vereditos da v395 mudados (estatuto_da_prova_v391, pedras_v392, pedras_v393, three_stress_tests_v387,
    varredura_e_sorry_v392 -- a troca numerica da escada); (f) kernel 1425 / 29228, todos no trio; (g) nenhum veredito do selo diz
    CONFIRMED. physical_verdict_allowed=False."""
    import re as _re
    out = {"pass": False, "estatuto": "REAL(lido do cofre v396 e do v395 pelo nome) / dois ceticos por injecao", "physical_verdict_allowed": False}
    try:
        _c396 = CUSTODY_DIR.parent / ("um_unificado_" + "v396")
        _c395 = CUSTODY_DIR.parent / ("um_unificado_" + "v395")
        can = json.loads((_c396 / "um_absoluto.json").read_text(encoding="utf-8"))
        sl = json.loads((_c396 / "um_absoluto_selo.json").read_text(encoding="utf-8"))
        mf = json.loads((_c396 / "tgl_kernel_proof_manifest.json").read_text(encoding="utf-8"))
        pt = (_c396 / "um_absoluto_pt.txt").read_text(encoding="utf-8", errors="replace")
        en = (_c396 / "um_absoluto_en.txt").read_text(encoding="utf-8", errors="replace")
        pt395 = (_c395 / "um_absoluto_pt.txt").read_text(encoding="utf-8", errors="replace")
        can395 = json.loads((_c395 / "um_absoluto.json").read_text(encoding="utf-8"))
        gate395 = json.loads((_c395 / "CUSTODY_MANIFEST.json").read_text(encoding="utf-8")).get("gate")
    except (OSError, ValueError) as e:
        out["erro"] = "cofre ilegivel: %r" % (e,)
        return out
    core, core395 = can.get("core") or {}, can395.get("core") or {}
    novos = sorted(k for k in core if k not in core395)
    sumidos = sorted(k for k in core395 if k not in core)

    def _bloco_ok(b):
        if not isinstance(b, dict):
            return False
        vd = str(b.get("verdict") or "")
        return bool(b.get("all_verified") is True and b.get("does_not_gate_core") is True and ("GATE_UNMOVED" in vd or "GATE_UNTOUCHED" in vd)
                    and not _re.search(r"(?<![A-Z_])CONFIRMED", vd.replace("NOT_CONFIRMED", "")))
    maus = [k for k in novos if not _bloco_ok(core[k])]
    blocos_ok = bool(novos == ["cunhagens_v396", "kh_n1_cobertura_v396", "testemunha_estatica_v396"] and not sumidos and not maus)
    kf, kf395 = core.get("kernel_formalization") or {}, core395.get("kernel_formalization") or {}
    n_band = len([k for k in kf if k not in kf395])
    band_ok = bool(n_band == 47)

    def _v396(c):
        try:
            te, cu, kh, e = c["testemunha_estatica_v396"], c["cunhagens_v396"], c["kh_n1_cobertura_v396"], c["estatuto_da_prova_v391"]
            un, fo, p1 = te["unconditional"], te["fock_face"], e["prova_1_kernel"]
            ft, st = te.get("formal_theorems") or {}, te.get("support_theorems") or {}
            return bool(un.get("theorem") == "TGLExt.TestemunhaEstatica.the_psion_inhabits_the_static_witness" and un.get("flag_true") is True
                        and un.get("in_trio") is True and un.get("composition") == "UNCONDITIONAL__NO_CERTIFICATE_AS_HYPOTHESIS"
                        and fo.get("theorem") == "TGLExt.Psibit.the_psion_face_of_the_psibit"
                        and fo.get("status") == "CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE" and fo.get("inhabitant_exhibited") is False
                        and len(ft) == 19 and all(v is True for v in ft.values()) and len(st) == 8 and all(v is True for v in st.values())
                        and (te.get("mechanics") or {}).get("passed") is True and len(cu.get("verbatim") or {}) == 3
                        and (kh.get("lido") or {}).get("constantes_cobertas") == 29228 and (kh.get("lido") or {}).get("teoremas_cobertos") == 23227
                        and "NONE_OUTSIDE_THE_TRIO" in str(kh.get("verdict"))
                        and p1["n_theorems_clean"] == p1["n_theorems_expected"] == 9498 and p1["declaracoes_auditadas"] == p1["no_trio"] == 29228
                        and "KERNEL_9498_OF_9498_FLAGS" in str(e.get("verdict")))
        except (KeyError, TypeError, AttributeError):
            return False
    v396_ok = _v396(core)
    c1 = dict(core); te1 = json.loads(json.dumps(core.get("testemunha_estatica_v396") or {}))                     # cetico 1
    try:
        te1["fock_face"]["status"] = "UNCONDITIONAL"
    except (KeyError, TypeError):
        pass
    c1["testemunha_estatica_v396"] = te1
    cetico1_reprovou = (_v396(c1) is False)
    c2 = dict(core); te2 = json.loads(json.dumps(core.get("testemunha_estatica_v396") or {}))                     # cetico 2
    try:
        te2["unconditional"]["flag_true"] = False
    except (KeyError, TypeError):
        pass
    c2["testemunha_estatica_v396"] = te2
    cetico2_reprovou = (_v396(c2) is False)
    gate = ((core.get("qg_closure") or {}).get("gate") or {})
    gate_ok = bool(gate.get("full_static_witness_exists") is False and str(sl.get("qg_closure_verdict")) == str(gate395)
                   and sl.get("um_version") == "v396")
    pat = _re.compile(r"^([a-z][a-z0-9_]{3,}) & ([A-Z][A-Z0-9_]{12,})", _re.M)
    reg_pt, reg_en, reg395 = dict(pat.findall(pt)), dict(pat.findall(en)), dict(pat.findall(pt395))
    mud = sorted(k for k in reg395 if reg_pt.get(k) != reg395[k])
    reg_novos = sorted(k for k in reg_pt if k not in reg395)
    reg_ok = bool(len(reg_pt) == len(reg_en) == 364 and len(reg395) == 361 and all(k in reg_pt for k in reg395) and reg_novos == novos
                  and mud == ["estatuto_da_prova_v391", "pedras_v392", "pedras_v393", "three_stress_tests_v387", "varredura_e_sorry_v392"])
    fm = mf.get("formal_files_sha256") or {}
    ar_ = mf.get("axiom_report") or {}
    k_ok = bool(len(fm) == 1425 and len(ar_) == 29228
                and not any(x_ not in ("propext", "Classical.choice", "Quot.sound") for v in ar_.values() for x_ in (v or [])))
    confs = [k for k, v in sl.items() if str(k).endswith("_verdict") and _re.search(r"(?<![A-Z_])CONFIRMED", str(v)) and "NOT_CONFIRMED" not in str(v)]
    ok = bool(blocos_ok and band_ok and v396_ok and cetico1_reprovou and cetico2_reprovou and gate_ok and reg_ok and k_ok and not confs)
    out.update({
        "blocos_novos_desde_v395": {"n": len(novos), "nomes": novos, "sumidos": sumidos, "fora_da_regra": maus, "ok": blocos_ok},
        "bandeiras_novas_desde_v395": {"n": n_band, "ok": band_ok},
        "registros_v396": {"ok": v396_ok,
                           "estatuto": "a composicao the_psion_inhabits_the_static_witness e INCONDICIONAL no kernel (nenhum certificado como hipotese); a ponte e CONSTRUIDA, nao derivada da dinamica da teoria; a face de Fock do psion e CONDICIONAL (certificado sem habitante) e mora fora da pedra; o psion habita a testemunha estatica e a leitura do operador [INPUT/ONTO]"},
        "ceticos": {"1_injecao": "testemunha_estatica_v396.fock_face.status = UNCONDITIONAL", "1_reprovou": cetico1_reprovou,
                    "2_injecao": "testemunha_estatica_v396.unconditional.flag_true = False", "2_reprovou": cetico2_reprovou,
                    "leitura": "se uma injecao NAO reprovasse, o check nao discriminaria e a pedra reprovaria"},
        "gate": {"full_static_witness_exists": gate.get("full_static_witness_exists"), "identico_ao_cofre_v395": gate_ok},
        "registro_de_vereditos": {"pt": len(reg_pt), "en": len(reg_en), "esperado": 364, "nomes_v395": len(reg395), "novos": len(reg_novos),
                                  "mudados_desde_v395": mud, "ok": reg_ok},
        "kernel": {"formais": len(fm), "termos": len(ar_), "ok": k_ok},
        "vereditos_do_selo_com_CONFIRMED": confs,
        "nao_se_afirma": ["que o Nome da fronteira da TGL seja o vetor de Bell, nem que o fluxo construido seja a dinamica da teoria",
                          "que o certificado de Fock da luz tenha habitante, nem que o psion de Fock seja o canto do psion",
                          "que 1/2 seja meia nat de entropia (e a entropia LINEAR; a de von Neumann e ln 2 nat)",
                          "qual leitura da paridade da patente ACOM Mirror e canonica (decisao do operador [LEGAL])",
                          "qualquer veredito fisico (physical_verdict_allowed=False; gate INALTERADO)"],
        "pass": ok,
    })
    return out


'''
troca("def shadow_the_station(core, selo):\n", FUNC.lstrip("\n") + "def shadow_the_station(core, selo):\n", "funcao _medir_v396_custodia")
troca('        "custodia_v395": _medir_v395_custodia(),\n',
      '        "custodia_v395": _medir_v395_custodia(),\n        "custodia_v396": _medir_v396_custodia(),\n', "entrada v45")
troca('    v44_pass = station["custodia_v395"]["pass"]\n',
      '    v44_pass = station["custodia_v395"]["pass"]\n'
      '    # v45 (v61): A CUSTODIA v396 -- o cofre v396 contra o v395, pelo nome: 3 blocos verificados que nao movem o gate, 47 bandeiras,\n'
      '    # a testemunha estatica (incondicional) e a face de Fock (condicional), registro 364 com 5 mudancas ditas, kernel 1425/29228; dois ceticos.\n'
      '    v45_pass = station["custodia_v396"]["pass"]\n', "v45_pass")
troca("and v42_pass and v43_pass and v44_pass)\n", "and v42_pass and v43_pass and v44_pass and v45_pass)\n", "all_pass inclui v45")
troca('        verdict = ("FRONTEIRA_SINCRONIZADA_V395"\n',
      '        verdict = ("FRONTEIRA_SINCRONIZADA_V396"\n'
      '                   "__V396_A_TESTEMUNHA_ESTATICA__COFRE_V396_CONTRA_O_V395_PELO_NOME__3_BLOCOS_NOVOS_VERIFICADOS_NENHUM_MOVE_O_GATE__47_BANDEIRAS__ESCADA_9498_DE_9498_BANDEIRAS__KERNEL_1425_29228_NO_TRIO__O_PSION_HABITA_A_TESTEMUNHA_ESTATICA_INCONDICIONAL_PONTE_CONSTRUIDA_FACE_DE_FOCK_CONDICIONAL__REGISTRO_364_COM_OS_361_DA_V395_E_5_MUDADOS_DITOS__DOIS_CETICOS__GATE_INALTERADO"\n'
      '                   "__V395"\n', "veredito v396 (o da v395 segue como sufixo)")
tmp = R + ".tmp_v61"; open(tmp, "wb").write(s.encode("utf-8"))
r = subprocess.run([sys.executable, "-m", "py_compile", tmp], capture_output=True, text=True)
if r.returncode != 0:
    os.remove(tmp); raise SystemExit("SINTAXE INVALIDA — nada trocado:\n" + (r.stderr or "")[:1500])
os.replace(tmp, R); print("runner v61: %d -> %d bytes | py_compile OK | backup .bak_v61_%s" % (len(raw), os.path.getsize(R), TS))
