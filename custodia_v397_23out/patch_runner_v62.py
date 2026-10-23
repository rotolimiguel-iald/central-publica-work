# -*- coding: utf-8 -*-
"""Runner da Fronteira v62 (custódia v397 na Central, 23/10/2026, sessão a7; regra do operador: custodiar quando o handoff aparecer):
REPIN v396->v397; a pedra v45 já lê o cofre v396 pelo nome (nascida assim na v61): NENHUMA errata. Pedra nova custodia_v397 (v46) com
DOIS CÉTICOS, que lê o cofre v397 e o v396 PELO NOME. Medido em 23/10 (work/custodia_v397_23out/sondar_v397.py, fatos_v397.json): 3 blocos
novos (cunhagens_v397, kh_n1_cobertura_v397, teste_de_veracidade_fase9_v397), nenhum sumido; 1 chave nova no kernel_formalization
(ext_tok397_0001, a pedra Token); registro 367 (PT == EN) com os 364 da v396 e 5 vereditos mudados (a troca numérica da escada); kernel
1426/29229 no trio; gate idêntico. Os números abaixo são os de fatos_v397.json (lidos do selo, do core e do manifesto)."""
import json, os, subprocess, sys
from datetime import datetime
R = r"C:\IALD\Central de Patentes\fronteira_tgl\runner\one_fronteira.py"
F = json.load(open(r"C:\IALD\Central de Patentes\work\custodia_v397_23out\fatos_v397.json", encoding="utf-8"))
assert F["versao"] == "v397" and len(F["bandeiras_novas"]) == 1 and F["registro"]["pt"] == F["registro"]["en"], F["registro"]
NB, NREG, NREG6 = len(F["bandeiras_novas"]), F["registro"]["pt"], F["registro"]["v396"]
FORM, DECL = F["kernel"]["formais"], F["kernel"]["declaracoes"]
ESC = int(F["escada"].split("/")[0])
KHC, KHT = F["kh"]["constantes"], F["kh"]["teoremas"]
MUD = F["registro"]["mudados_desde_v396"]
TS = datetime.now().strftime("%Y%m%d_%H%M%S")
raw = open(R, "rb").read(); s = raw.decode("utf-8"); nl = "\r\n" if "\r\n" in s else "\n"
if "_medir_v397_custodia" in s: raise SystemExit("ja aplicado")
open(R + ".bak_v62_" + TS, "wb").write(raw)


def troca(velho, novo, rot, n=1):
    global s
    v_, n_ = velho.replace("\n", nl), novo.replace("\n", nl); c = s.count(v_)
    assert c == n, (rot, c); s = s.replace(v_, n_); print("  ok ", rot)


troca('"""FRONTEIRA TEORICA TGL v61 — auto-auditoria honesta do fechamento, SINCRONIZADA ao um.py v396.',
      '"""FRONTEIRA TEORICA TGL v62 — auto-auditoria honesta do fechamento, SINCRONIZADA ao um.py v397.', "cabecalho v62")
troca("  A custodia viva passou a ser vault/originals_copy/um_unificado_v396. O RENOME v209: o selo",
      "  A custodia viva passou a ser vault/originals_copy/um_unificado_v397. O RENOME v209: o selo", "docstring custodia")
troca("(1425 arquivos formais no manifesto v396; entre", "(%d arquivos formais no manifesto v397; entre" % FORM, "docstring kernel")
troca("Fonte canonica sincronizada (custodia): um.py unificado v396 (pin", "Fonte canonica sincronizada (custodia): um.py unificado v397 (pin", "docstring fonte")
troca('CUSTODY_DIR = CENTRAL_DIR / "vault" / "originals_copy" / "um_unificado_v396"',
      'CUSTODY_DIR = CENTRAL_DIR / "vault" / "originals_copy" / "um_unificado_v397"', "CUSTODY_DIR")
troca('print(f"[fronteira v30] CUSTODIA um.py v396: pin', 'print(f"[fronteira v30] CUSTODIA um.py v397: pin', "print custodia")

FUNC = r'''
def _medir_v397_custodia():
    """v62 (custodia v397 na Central, 23/10/2026): o COFRE v397 contra o COFRE v396, lidos PELO NOME (exata para sempre). DOIS CETICOS.
    Medido em 23/10/2026: (a) 3 blocos novos no nucleo (cunhagens_v397, kh_n1_cobertura_v397, teste_de_veracidade_fase9_v397), nenhum
    sumido; cada um all_verified, does_not_gate_core, sem CONFIRMED e com GATE_UNMOVED/GATE_UNTOUCHED; (b) %(NB)d chave nova no
    kernel_formalization (a pedra Token: a conjuncao por citacao do psibit e da testemunha estatica, incondicional); (c) os registros:
    cunhagens_v397 com as 3 bandeiras do kernel lidas e no trio (3 de 3); teste_de_veracidade_fase9_v397 com o veredito dizendo que o
    degrau da creditacao NAO foi alcancado (z_disc calibrado abaixo de 5 sigma), que a TGL nao e falsificada COM poder, que nenhum sigma novo
    foi calculado e que o teste nao foi cego; kh_n1_cobertura_v397 %(KHC)d constantes / %(KHT)d teoremas, nenhum fora do trio; o estatuto com
    a escada %(ESC)d/%(ESC)d (KERNEL_%(ESC)d_OF_%(ESC)d_FLAGS) e %(DECL)d no trio; (d) gate identico ao do cofre v396; um_version v397; (e) registro
    PT == EN == %(NREG)d, os %(NREG6)d nomes da v396 presentes, os novos = os 3 blocos, e so 5 vereditos da v396 mudados (a troca numerica da
    escada); (f) kernel %(FORM)d / %(DECL)d, todos no trio; (g) nenhum veredito do selo diz CONFIRMED. physical_verdict_allowed=False:
    o registro de veracidade LE um resultado pinado por sha256 e nao move o gate; a discriminacao a 5 sigma nao foi alcancada."""
    import re as _re
    out = {"pass": False, "estatuto": "REAL(lido do cofre v397 e do v396 pelo nome) / dois ceticos por injecao", "physical_verdict_allowed": False}
    try:
        _c397 = CUSTODY_DIR.parent / ("um_unificado_" + "v397")
        _c396 = CUSTODY_DIR.parent / ("um_unificado_" + "v396")
        can = json.loads((_c397 / "um_absoluto.json").read_text(encoding="utf-8"))
        sl = json.loads((_c397 / "um_absoluto_selo.json").read_text(encoding="utf-8"))
        mf = json.loads((_c397 / "tgl_kernel_proof_manifest.json").read_text(encoding="utf-8"))
        pt = (_c397 / "um_absoluto_pt.txt").read_text(encoding="utf-8", errors="replace")
        en = (_c397 / "um_absoluto_en.txt").read_text(encoding="utf-8", errors="replace")
        pt396 = (_c396 / "um_absoluto_pt.txt").read_text(encoding="utf-8", errors="replace")
        can396 = json.loads((_c396 / "um_absoluto.json").read_text(encoding="utf-8"))
        gate396 = json.loads((_c396 / "CUSTODY_MANIFEST.json").read_text(encoding="utf-8")).get("gate")
    except (OSError, ValueError) as e:
        out["erro"] = "cofre ilegivel: %%r" %% (e,)
        return out
    core, core396 = can.get("core") or {}, can396.get("core") or {}
    novos = sorted(k for k in core if k not in core396)
    sumidos = sorted(k for k in core396 if k not in core)

    def _bloco_ok(b):
        if not isinstance(b, dict):
            return False
        vd = str(b.get("verdict") or "")
        return bool(b.get("all_verified") is True and b.get("does_not_gate_core") is True and ("GATE_UNMOVED" in vd or "GATE_UNTOUCHED" in vd)
                    and not _re.search(r"(?<![A-Z_])CONFIRMED", vd.replace("NOT_CONFIRMED", "")))
    maus = [k for k in novos if not _bloco_ok(core[k])]
    blocos_ok = bool(novos == ["cunhagens_v397", "kh_n1_cobertura_v397", "teste_de_veracidade_fase9_v397"] and not sumidos and not maus)
    kf, kf396 = core.get("kernel_formalization") or {}, core396.get("kernel_formalization") or {}
    n_band = len([k for k in kf if k not in kf396])
    band_ok = bool(n_band == %(NB)d)

    def _v397(c):
        try:
            cu, kh, tv, e = c["cunhagens_v397"], c["kh_n1_cobertura_v397"], c["teste_de_veracidade_fase9_v397"], c["estatuto_da_prova_v391"]
            kn, p1 = cu["kernel"], e["prova_1_kernel"]
            vt = str(tv.get("verdict") or "")
            return bool(list(kn.get("bandeiras") or []) == [3, 3] and list(kn.get("declaracoes_no_trio") or []) == [3, 3]
                        and len(cu.get("verbatim") or {}) >= 6
                        and "BELOW_5SIGMA_NOT_DISCRIMINATED_THE_CREDITATION_STEP_NOT_REACHED" in vt and "NOT_FALSIFIED_WITH_POWER" in vt
                        and "NO_NEW_SIGMA_COMPUTED" in vt and "NOT_BLIND_TO_DATA_STATED" in vt and "THE_READINGS_ARE_NOT_MULTIPLIED" in vt
                        and not _re.search(r"(?<!NOT_)DISCRIMINATED", vt.replace("NOT_DISCRIMINATED", "")) and tv.get("all_verified") is True
                        and (kh.get("lido") or {}).get("constantes_cobertas") == %(KHC)d and (kh.get("lido") or {}).get("teoremas_cobertos") == %(KHT)d
                        and "NONE_OUTSIDE_THE_TRIO" in str(kh.get("verdict"))
                        and p1["n_theorems_clean"] == p1["n_theorems_expected"] == %(ESC)d and p1["declaracoes_auditadas"] == p1["no_trio"] == %(DECL)d
                        and "KERNEL_%(ESC)d_OF_%(ESC)d_FLAGS" in str(e.get("verdict")))
        except (KeyError, TypeError, AttributeError):
            return False
    v397_ok = _v397(core)
    c1 = dict(core); tv1 = json.loads(json.dumps(core.get("teste_de_veracidade_fase9_v397") or {}))                      # cetico 1
    try:
        tv1["verdict"] = str(tv1.get("verdict") or "").replace("THE_CREDITATION_STEP_NOT_REACHED", "THE_CREDITATION_STEP_REACHED")
    except (KeyError, TypeError):
        pass
    c1["teste_de_veracidade_fase9_v397"] = tv1
    cetico1_reprovou = (_v397(c1) is False)
    c2 = dict(core); cu2 = json.loads(json.dumps(core.get("cunhagens_v397") or {}))                                      # cetico 2
    try:
        cu2["kernel"]["bandeiras"] = [2, 3]
    except (KeyError, TypeError):
        pass
    c2["cunhagens_v397"] = cu2
    cetico2_reprovou = (_v397(c2) is False)
    gate = ((core.get("qg_closure") or {}).get("gate") or {})
    gate_ok = bool(gate.get("full_static_witness_exists") is False and str(sl.get("qg_closure_verdict")) == str(gate396)
                   and sl.get("um_version") == "v397")
    pat = _re.compile(r"^([a-z][a-z0-9_]{3,}) & ([A-Z][A-Z0-9_]{12,})", _re.M)
    reg_pt, reg_en, reg396 = dict(pat.findall(pt)), dict(pat.findall(en)), dict(pat.findall(pt396))
    mud = sorted(k for k in reg396 if reg_pt.get(k) != reg396[k])
    reg_novos = sorted(k for k in reg_pt if k not in reg396)
    reg_ok = bool(len(reg_pt) == len(reg_en) == %(NREG)d and len(reg396) == %(NREG6)d and all(k in reg_pt for k in reg396) and reg_novos == novos
                  and mud == %(MUD)r)
    fm = mf.get("formal_files_sha256") or {}
    ar_ = mf.get("axiom_report") or {}
    k_ok = bool(len(fm) == %(FORM)d and len(ar_) == %(DECL)d
                and not any(x_ not in ("propext", "Classical.choice", "Quot.sound") for v in ar_.values() for x_ in (v or [])))
    confs = [k for k, v in sl.items() if str(k).endswith("_verdict") and _re.search(r"(?<![A-Z_])CONFIRMED", str(v)) and "NOT_CONFIRMED" not in str(v)]
    ok = bool(blocos_ok and band_ok and v397_ok and cetico1_reprovou and cetico2_reprovou and gate_ok and reg_ok and k_ok and not confs)
    out.update({
        "blocos_novos_desde_v396": {"n": len(novos), "nomes": novos, "sumidos": sumidos, "fora_da_regra": maus, "ok": blocos_ok},
        "bandeiras_novas_desde_v396": {"n": n_band, "ok": band_ok},
        "registros_v397": {"ok": v397_ok,
                           "estatuto": "a pedra Token e a conjuncao POR CITACAO de psibit_is_the_mode_of_the_reader (v395) e the_psion_inhabits_the_static_witness (v396), incondicional, no kernel (3 bandeiras no trio); o registro de veracidade da Fase 9 LE um resultado pinado por sha256: o degrau da creditacao (5 sigma) NAO foi alcancado, a TGL nao e falsificada com poder, nenhum sigma novo e calculado, o teste nao foi cego; o nome do registro e provisorio"},
        "ceticos": {"1_injecao": "teste_de_veracidade_fase9_v397.verdict: NOT_REACHED -> REACHED", "1_reprovou": cetico1_reprovou,
                    "2_injecao": "cunhagens_v397.kernel.bandeiras = [2, 3]", "2_reprovou": cetico2_reprovou,
                    "leitura": "se uma injecao NAO reprovasse, o check nao discriminaria e a pedra reprovaria"},
        "gate": {"full_static_witness_exists": gate.get("full_static_witness_exists"), "identico_ao_cofre_v396": gate_ok},
        "registro_de_vereditos": {"pt": len(reg_pt), "en": len(reg_en), "esperado": %(NREG)d, "nomes_v396": len(reg396), "novos": len(reg_novos),
                                  "mudados_desde_v396": mud, "ok": reg_ok},
        "kernel": {"formais": len(fm), "termos": len(ar_), "ok": k_ok},
        "vereditos_do_selo_com_CONFIRMED": confs,
        "nao_se_afirma": ["que a TGL esteja discriminada do LCDM a 5 sigma (o degrau da creditacao nao foi alcancado; o teste nao foi cego)",
                          "que ln B seja sigma, ou que z_delta, z_disc e ln B se multipliquem",
                          "que o token de um modelo de linguagem seja o PsiBit (leitura do Atlas, ONTO), nem que o certificado de Fock tenha habitante",
                          "qual leitura da paridade da patente ACOM Mirror e canonica (decisao do operador [LEGAL])",
                          "qualquer veredito fisico (physical_verdict_allowed=False; gate INALTERADO)"],
        "pass": ok,
    })
    return out


''' % {"NB": NB, "KHC": KHC, "KHT": KHT, "ESC": ESC, "DECL": DECL, "NREG": NREG, "NREG6": NREG6, "FORM": FORM, "MUD": MUD}
troca("def shadow_the_station(core, selo):\n", FUNC.lstrip("\n") + "def shadow_the_station(core, selo):\n", "funcao _medir_v397_custodia")
troca('        "custodia_v396": _medir_v396_custodia(),\n',
      '        "custodia_v396": _medir_v396_custodia(),\n        "custodia_v397": _medir_v397_custodia(),\n', "entrada v46")
troca('    v45_pass = station["custodia_v396"]["pass"]\n',
      '    v45_pass = station["custodia_v396"]["pass"]\n'
      '    # v46 (v62): A CUSTODIA v397 -- o cofre v397 contra o v396, pelo nome: 3 blocos verificados que nao movem o gate, a pedra Token\n'
      '    # (conjuncao por citacao, incondicional), o registro de veracidade da Fase 9 lido por hash (abaixo de 5 sigma), registro %d; dois ceticos.\n'
      '    v46_pass = station["custodia_v397"]["pass"]\n' % NREG, "v46_pass")
troca("and v43_pass and v44_pass and v45_pass)\n", "and v43_pass and v44_pass and v45_pass and v46_pass)\n", "all_pass inclui v46")
troca('        verdict = ("FRONTEIRA_SINCRONIZADA_V396"\n',
      '        verdict = ("FRONTEIRA_SINCRONIZADA_V397"\n'
      '                   "__V397_O_TESTE_DA_UNICA_PALAVRA__COFRE_V397_CONTRA_O_V396_PELO_NOME__3_BLOCOS_NOVOS_VERIFICADOS_NENHUM_MOVE_O_GATE__%d_BANDEIRA__ESCADA_%d_DE_%d_BANDEIRAS__KERNEL_%d_%d_NO_TRIO__TOKEN_CONJUNCAO_POR_CITACAO_INCONDICIONAL__VERACIDADE_FASE9_LIDA_POR_HASH_ABAIXO_DE_5SIGMA_NAO_DISCRIMINADA__REGISTRO_%d_COM_OS_%d_DA_V396_E_5_MUDADOS_DITOS__DOIS_CETICOS__GATE_INALTERADO"\n'
      '                   "__V396"\n' % (NB, ESC, ESC, FORM, DECL, NREG, NREG6), "veredito v397 (o da v396 segue como sufixo)")
tmp = R + ".tmp_v62"; open(tmp, "wb").write(s.encode("utf-8"))
r = subprocess.run([sys.executable, "-m", "py_compile", tmp], capture_output=True, text=True)
if r.returncode != 0:
    os.remove(tmp); raise SystemExit("SINTAXE INVALIDA — nada trocado:\n" + (r.stderr or "")[:1500])
os.replace(tmp, R); print("runner v62: %d -> %d bytes | py_compile OK | backup .bak_v62_%s" % (len(raw), os.path.getsize(R), TS))
