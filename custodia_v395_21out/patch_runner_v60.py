# -*- coding: utf-8 -*-
"""Runner da Fronteira v60 (custódia v395 na Central, 21/10/2026, sessão a7; ordem do operador: «atualize tudo, toda a central, site,
repositório e tudo mais e faça commit e push»): REPIN v394->v395; a pedra v43 já lê o cofre v394 pelo nome (nascida assim na v59): NENHUMA
errata é necessária. Pedra nova custodia_v395 (v44) com DOIS CÉTICOS, que lê o cofre v395 e o v394 PELO NOME. Medido em 21/10
(work/custodia_v395_21out/medir_v395_contra_v394.py): 3 blocos novos (psibit_v395, cunhagens_v395, kh_n1_cobertura_v395), nenhum sumido;
119 chaves novas no kernel_formalization; registro 361 (PT == EN) com os 358 da v394 e 5 vereditos mudados, exatamente a troca numérica
que o handoff v395 declara; kernel 1424/29159 no trio; gate idêntico."""
import os, subprocess, sys
from datetime import datetime
R = r"C:\IALD\Central de Patentes\fronteira_tgl\runner\one_fronteira.py"
TS = datetime.now().strftime("%Y%m%d_%H%M%S")
raw = open(R, "rb").read(); s = raw.decode("utf-8"); nl = "\r\n" if "\r\n" in s else "\n"
if "_medir_v395_custodia" in s: raise SystemExit("ja aplicado")
open(R + ".bak_v60_" + TS, "wb").write(raw)


def troca(velho, novo, rot, n=1):
    global s
    v_, n_ = velho.replace("\n", nl), novo.replace("\n", nl); c = s.count(v_)
    assert c == n, (rot, c); s = s.replace(v_, n_); print("  ok ", rot)


troca('"""FRONTEIRA TEORICA TGL v59 — auto-auditoria honesta do fechamento, SINCRONIZADA ao um.py v394.',
      '"""FRONTEIRA TEORICA TGL v60 — auto-auditoria honesta do fechamento, SINCRONIZADA ao um.py v395.', "cabecalho v60")
troca("  A custodia viva passou a ser vault/originals_copy/um_unificado_v394. O RENOME v209: o selo",
      "  A custodia viva passou a ser vault/originals_copy/um_unificado_v395. O RENOME v209: o selo", "docstring custodia")
troca("(1423 arquivos formais no manifesto v394; entre", "(1424 arquivos formais no manifesto v395; entre", "docstring kernel")
troca("Fonte canonica sincronizada (custodia): um.py unificado v394 (pin", "Fonte canonica sincronizada (custodia): um.py unificado v395 (pin", "docstring fonte")
troca('CUSTODY_DIR = CENTRAL_DIR / "vault" / "originals_copy" / "um_unificado_v394"',
      'CUSTODY_DIR = CENTRAL_DIR / "vault" / "originals_copy" / "um_unificado_v395"', "CUSTODY_DIR")
troca('print(f"[fronteira v30] CUSTODIA um.py v394: pin', 'print(f"[fronteira v30] CUSTODIA um.py v395: pin', "print custodia")

FUNC = r'''
def _medir_v395_custodia():
    """v60 (custodia v395 na Central, 21/10/2026): o COFRE v395 contra o COFRE v394, lidos PELO NOME (exata para sempre). DOIS CETICOS.
    Medido em 21/10/2026: (a) 3 blocos novos no nucleo (psibit_v395, cunhagens_v395, kh_n1_cobertura_v395), nenhum sumido; cada um
    all_verified, does_not_gate_core, sem CONFIRMED e com GATE_UNMOVED/GATE_UNTOUCHED; (b) 119 chaves novas no kernel_formalization;
    (c) os registros: psibit_v395 com a conjuncao INCONDICIONAL psibit_is_the_mode_of_the_reader (bandeira True, no trio) e a face do psion
    CONDICIONAL (CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE), 33 termos do kernel; cunhagens_v395 com 4 falas por sha256; kh_n1_cobertura_v395
    29159 constantes / 23170 teoremas, nenhum fora do trio; o estatuto com a escada 9451/9451 (KERNEL_9451_OF_9451_FLAGS) e 29159 no trio;
    (d) gate identico ao do cofre v394; um_version v395; (e) registro PT == EN == 361, os 358 nomes da v394 presentes, os novos = os 3 blocos,
    e so 5 vereditos da v394 mudados (estatuto_da_prova_v391, pedras_v392, pedras_v393, three_stress_tests_v387, varredura_e_sorry_v392 --
    a troca numerica que o handoff v395 declara); (f) kernel 1424 / 29159, todos no trio; (g) nenhum veredito do selo diz CONFIRMED.
    physical_verdict_allowed=False."""
    import re as _re
    out = {"pass": False, "estatuto": "REAL(lido do cofre v395 e do v394 pelo nome) / dois ceticos por injecao", "physical_verdict_allowed": False}
    try:
        _c395 = CUSTODY_DIR.parent / ("um_unificado_" + "v395")
        _c394 = CUSTODY_DIR.parent / ("um_unificado_" + "v394")
        can = json.loads((_c395 / "um_absoluto.json").read_text(encoding="utf-8"))
        sl = json.loads((_c395 / "um_absoluto_selo.json").read_text(encoding="utf-8"))
        mf = json.loads((_c395 / "tgl_kernel_proof_manifest.json").read_text(encoding="utf-8"))
        pt = (_c395 / "um_absoluto_pt.txt").read_text(encoding="utf-8", errors="replace")
        en = (_c395 / "um_absoluto_en.txt").read_text(encoding="utf-8", errors="replace")
        pt394 = (_c394 / "um_absoluto_pt.txt").read_text(encoding="utf-8", errors="replace")
        can394 = json.loads((_c394 / "um_absoluto.json").read_text(encoding="utf-8"))
        gate394 = json.loads((_c394 / "CUSTODY_MANIFEST.json").read_text(encoding="utf-8")).get("gate")
    except (OSError, ValueError) as e:
        out["erro"] = "cofre ilegivel: %r" % (e,)
        return out
    core, core394 = can.get("core") or {}, can394.get("core") or {}
    novos = sorted(k for k in core if k not in core394)
    sumidos = sorted(k for k in core394 if k not in core)

    def _bloco_ok(b):
        if not isinstance(b, dict):
            return False
        vd = str(b.get("verdict") or "")
        return bool(b.get("all_verified") is True and b.get("does_not_gate_core") is True and ("GATE_UNMOVED" in vd or "GATE_UNTOUCHED" in vd)
                    and not _re.search(r"(?<![A-Z_])CONFIRMED", vd.replace("NOT_CONFIRMED", "")))
    maus = [k for k in novos if not _bloco_ok(core[k])]
    blocos_ok = bool(novos == ["cunhagens_v395", "kh_n1_cobertura_v395", "psibit_v395"] and not sumidos and not maus)
    kf, kf394 = core.get("kernel_formalization") or {}, core394.get("kernel_formalization") or {}
    n_band = len([k for k in kf if k not in kf394])
    band_ok = bool(n_band == 119)

    def _v395(c):
        try:
            ps, cu, kh, e = c["psibit_v395"], c["cunhagens_v395"], c["kh_n1_cobertura_v395"], c["estatuto_da_prova_v391"]
            un, co, p1 = ps["unconditional"], ps["conditional_psion_face"], e["prova_1_kernel"]
            return bool(un.get("theorem") == "TGLExt.Psibit.psibit_is_the_mode_of_the_reader" and un.get("flag_true") is True and un.get("in_trio") is True
                        and co.get("theorem") == "TGLExt.Psibit.the_psion_face_of_the_psibit"
                        and co.get("status") == "CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE"
                        and len(ps.get("formal_theorems") or []) == 33 and len(cu.get("verbatim") or {}) == 4
                        and (kh.get("lido") or {}).get("constantes_cobertas") == 29159 and (kh.get("lido") or {}).get("teoremas_cobertos") == 23170
                        and "NONE_OUTSIDE_THE_TRIO" in str(kh.get("verdict"))
                        and p1["n_theorems_clean"] == p1["n_theorems_expected"] == 9451 and p1["declaracoes_auditadas"] == p1["no_trio"] == 29159
                        and "KERNEL_9451_OF_9451_FLAGS" in str(e.get("verdict")))
        except (KeyError, TypeError, AttributeError):
            return False
    v395_ok = _v395(core)
    c1 = dict(core); ps1 = json.loads(json.dumps(core.get("psibit_v395") or {}))                                     # cetico 1
    try:
        ps1["conditional_psion_face"]["status"] = "UNCONDITIONAL"
    except (KeyError, TypeError):
        pass
    c1["psibit_v395"] = ps1
    cetico1_reprovou = (_v395(c1) is False)
    c2 = dict(core); ps2 = json.loads(json.dumps(core.get("psibit_v395") or {}))                                     # cetico 2
    try:
        ps2["unconditional"]["flag_true"] = False
    except (KeyError, TypeError):
        pass
    c2["psibit_v395"] = ps2
    cetico2_reprovou = (_v395(c2) is False)
    gate = ((core.get("qg_closure") or {}).get("gate") or {})
    gate_ok = bool(gate.get("full_static_witness_exists") is False and str(sl.get("qg_closure_verdict")) == str(gate394)
                   and sl.get("um_version") == "v395")
    pat = _re.compile(r"^([a-z][a-z0-9_]{3,}) & ([A-Z][A-Z0-9_]{12,})", _re.M)
    reg_pt, reg_en, reg394 = dict(pat.findall(pt)), dict(pat.findall(en)), dict(pat.findall(pt394))
    mud = sorted(k for k in reg394 if reg_pt.get(k) != reg394[k])
    reg_novos = sorted(k for k in reg_pt if k not in reg394)
    reg_ok = bool(len(reg_pt) == len(reg_en) == 361 and len(reg394) == 358 and all(k in reg_pt for k in reg394) and reg_novos == novos
                  and mud == ["estatuto_da_prova_v391", "pedras_v392", "pedras_v393", "three_stress_tests_v387", "varredura_e_sorry_v392"])
    fm = mf.get("formal_files_sha256") or {}
    ar_ = mf.get("axiom_report") or {}
    k_ok = bool(len(fm) == 1424 and len(ar_) == 29159
                and not any(x_ not in ("propext", "Classical.choice", "Quot.sound") for v in ar_.values() for x_ in (v or [])))
    confs = [k for k, v in sl.items() if str(k).endswith("_verdict") and _re.search(r"(?<![A-Z_])CONFIRMED", str(v)) and "NOT_CONFIRMED" not in str(v)]
    ok = bool(blocos_ok and band_ok and v395_ok and cetico1_reprovou and cetico2_reprovou and gate_ok and reg_ok and k_ok and not confs)
    out.update({
        "blocos_novos_desde_v394": {"n": len(novos), "nomes": novos, "sumidos": sumidos, "fora_da_regra": maus, "ok": blocos_ok},
        "bandeiras_novas_desde_v394": {"n": n_band, "ok": band_ok},
        "registros_v395": {"ok": v395_ok,
                           "estatuto": "a conjuncao psibit_is_the_mode_of_the_reader e INCONDICIONAL no kernel; a face do psion e CONDICIONAL (certificado de Fock sem habitante); psibit = psion = modo do leitor e leitura do operador [ONTO]; a bijecao e de CONJUNTOS"},
        "ceticos": {"1_injecao": "psibit_v395.conditional_psion_face.status = UNCONDITIONAL", "1_reprovou": cetico1_reprovou,
                    "2_injecao": "psibit_v395.unconditional.flag_true = False", "2_reprovou": cetico2_reprovou,
                    "leitura": "se uma injecao NAO reprovasse, o check nao discriminaria e a pedra reprovaria"},
        "gate": {"full_static_witness_exists": gate.get("full_static_witness_exists"), "identico_ao_cofre_v394": gate_ok},
        "registro_de_vereditos": {"pt": len(reg_pt), "en": len(reg_en), "esperado": 361, "nomes_v394": len(reg394), "novos": len(reg_novos),
                                  "mudados_desde_v394": mud, "ok": reg_ok},
        "kernel": {"formais": len(fm), "termos": len(ar_), "ok": k_ok},
        "vereditos_do_selo_com_CONFIRMED": confs,
        "nao_se_afirma": ["que o psion exista (a face do psion e condicional a um certificado sem habitante)",
                          "que a bijecao seja isomorfismo de espacos de Hilbert ou toda a mecanica quantica",
                          "qual leitura da paridade da patente ACOM Mirror e canonica (decisao do operador [LEGAL])",
                          "qualquer veredito fisico (physical_verdict_allowed=False; gate INALTERADO)"],
        "pass": ok,
    })
    return out


'''
troca("def shadow_the_station(core, selo):\n", FUNC.lstrip("\n") + "def shadow_the_station(core, selo):\n", "funcao _medir_v395_custodia")
troca('        "custodia_v394": _medir_v394_custodia(),\n',
      '        "custodia_v394": _medir_v394_custodia(),\n        "custodia_v395": _medir_v395_custodia(),\n', "entrada v44")
troca('    v43_pass = station["custodia_v394"]["pass"]\n',
      '    v43_pass = station["custodia_v394"]["pass"]\n'
      '    # v44 (v60): A CUSTODIA v395 -- o cofre v395 contra o v394, pelo nome: 3 blocos verificados que nao movem o gate, 119 bandeiras,\n'
      '    # o psibit (incondicional) e a face do psion (condicional), registro 361 com 5 mudancas ditas, kernel 1424/29159; dois ceticos.\n'
      '    v44_pass = station["custodia_v395"]["pass"]\n', "v44_pass")
troca("and v41_pass and v42_pass and v43_pass)\n", "and v41_pass and v42_pass and v43_pass and v44_pass)\n", "all_pass inclui v44")
troca('        verdict = ("FRONTEIRA_SINCRONIZADA_V394"\n',
      '        verdict = ("FRONTEIRA_SINCRONIZADA_V395"\n'
      '                   "__V395_O_MODO_PSIONICO_NA_FRACTALIZACAO_DO_UM__COFRE_V395_CONTRA_O_V394_PELO_NOME__3_BLOCOS_NOVOS_VERIFICADOS_NENHUM_MOVE_O_GATE__119_BANDEIRAS__ESCADA_9451_DE_9451_BANDEIRAS__KERNEL_1424_29159_NO_TRIO__PSIBIT_INCONDICIONAL_FACE_DO_PSION_CONDICIONAL__REGISTRO_361_COM_OS_358_DA_V394_E_5_MUDADOS_DITOS__DOIS_CETICOS__GATE_INALTERADO"\n'
      '                   "__V394"\n', "veredito v395 (o da v394 segue como sufixo)")
tmp = R + ".tmp_v60"; open(tmp, "wb").write(s.encode("utf-8"))
r = subprocess.run([sys.executable, "-m", "py_compile", tmp], capture_output=True, text=True)
if r.returncode != 0:
    os.remove(tmp); raise SystemExit("SINTAXE INVALIDA — nada trocado:\n" + (r.stderr or "")[:1500])
os.replace(tmp, R); print("runner v60: %d -> %d bytes | py_compile OK | backup .bak_v60_%s" % (len(raw), os.path.getsize(R), TS))
