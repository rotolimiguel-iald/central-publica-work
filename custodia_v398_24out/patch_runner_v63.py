# -*- coding: utf-8 -*-
"""Runner da Fronteira v63 (custódia v398 na Central, 24/10/2026, sessão a7; regra do operador de 23/10: custodiar quando o handoff aparecer):
REPIN v397->v398; a pedra v46 já lê o cofre v397 pelo nome: NENHUMA errata. Pedra nova custodia_v398 (v47) com DOIS CÉTICOS, que lê o
cofre v398 e o v397 PELO NOME. Medido em 24/10 (work/custodia_v398_24out/sondar_v398.py, fatos_v398.json): 4 blocos novos
(afinacao_das_cordas_v398, cunhagens_v398, kh_n1_cobertura_v398, sonico_v398), nenhum sumido; 40 chaves novas no kernel_formalization
(6 do sônico, 34 da afinação); registro 371 (PT == EN) com os 367 da v397 e 5 vereditos mudados (a troca numérica da escada); kernel
1428/29294 no trio; gate idêntico. Os números abaixo são os de fatos_v398.json (lidos do selo, do core e do manifesto)."""
import json, os, subprocess, sys
from datetime import datetime
R = r"C:\IALD\Central de Patentes\fronteira_tgl\runner\one_fronteira.py"
F = json.load(open(r"C:\IALD\Central de Patentes\work\custodia_v398_24out\fatos_v398.json", encoding="utf-8"))
assert F["versao"] == "v398" and len(F["bandeiras_novas"]) == 40 and F["registro"]["pt"] == F["registro"]["en"], F["registro"]
assert F["registros_novos"] == ["afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398", "sonico_v398"]
NB, NREG, NREG7 = len(F["bandeiras_novas"]), F["registro"]["pt"], F["registro"]["v397"]
FORM, DECL, FORM7 = F["kernel"]["formais"], F["kernel"]["declaracoes"], F["kernel"]["formais_v397"]
ESC = int(F["escada"].split("/")[0])
KHC, KHT = F["kh"]["constantes"], F["kh"]["teoremas"]
MUD = F["registro"]["mudados_desde_v397"]
assert len(MUD) == 5 and KHC == DECL, (MUD, KHC, DECL)
TS = datetime.now().strftime("%Y%m%d_%H%M%S")
raw = open(R, "rb").read(); s = raw.decode("utf-8"); nl = "\r\n" if "\r\n" in s else "\n"
if "_medir_v398_custodia" in s: raise SystemExit("ja aplicado")
open(R + ".bak_v63_" + TS, "wb").write(raw)


def troca(velho, novo, rot, n=1):
    global s
    v_, n_ = velho.replace("\n", nl), novo.replace("\n", nl); c = s.count(v_)
    assert c == n, (rot, c); s = s.replace(v_, n_); print("  ok ", rot)


troca('"""FRONTEIRA TEORICA TGL v62 — auto-auditoria honesta do fechamento, SINCRONIZADA ao um.py v397.',
      '"""FRONTEIRA TEORICA TGL v63 — auto-auditoria honesta do fechamento, SINCRONIZADA ao um.py v398.', "cabecalho v63")
troca("  A custodia viva passou a ser vault/originals_copy/um_unificado_v397. O RENOME v209: o selo",
      "  A custodia viva passou a ser vault/originals_copy/um_unificado_v398. O RENOME v209: o selo", "docstring custodia")
troca("(%d arquivos formais no manifesto v397; entre" % FORM7, "(%d arquivos formais no manifesto v398; entre" % FORM, "docstring kernel")
troca("Fonte canonica sincronizada (custodia): um.py unificado v397 (pin", "Fonte canonica sincronizada (custodia): um.py unificado v398 (pin", "docstring fonte")
troca('CUSTODY_DIR = CENTRAL_DIR / "vault" / "originals_copy" / "um_unificado_v397"',
      'CUSTODY_DIR = CENTRAL_DIR / "vault" / "originals_copy" / "um_unificado_v398"', "CUSTODY_DIR")
troca('print(f"[fronteira v30] CUSTODIA um.py v397: pin', 'print(f"[fronteira v30] CUSTODIA um.py v398: pin', "print custodia")

FUNC = r'''
def _medir_v398_custodia():
    """v63 (custodia v398 na Central, 24/10/2026): o COFRE v398 contra o COFRE v397, lidos PELO NOME (exata para sempre). DOIS CETICOS.
    Medido em 24/10/2026: (a) 4 blocos novos no nucleo (afinacao_das_cordas_v398, cunhagens_v398, kh_n1_cobertura_v398, sonico_v398),
    nenhum sumido; cada um all_verified, does_not_gate_core, sem CONFIRMED e com GATE_UNMOVED/GATE_UNTOUCHED; (b) %(NB)d chaves novas no
    kernel_formalization (as pedras Sonico e AfinacaoDasCordas: 6 + 34, so declaracoes nomeadas); (c) os registros: sonico_v398 com a
    composicao INCONDICIONAL no trio, exact_ladder e 8 checagens numericas passadas (ln 2 = o bit justo; exp(ln 2) = 2; n oitavas = n bits;
    o pino nao e a meia-nat; o seletor pina; beta = alfa CODATA 2018 x sqrt(e) em runtime); afinacao_das_cordas_v398 com a composicao
    INCONDICIONAL, 7 checagens passadas, a hipotese MasslessFirstLevel NOMEADA e nao provada, a geometria OPEN e derives_strings_from_the_axiom
    = False (nada deriva as cordas do axioma); cunhagens_v398 com as 2 bandeiras das pedras no trio (2 de 2; 41 declaracoes) e as 6
    inscricoes de 23/10 por sha256 (cinco do operador e uma leitura da gerencia que ele ratificou, rotulada); kh_n1_cobertura_v398
    %(KHC)d constantes / %(KHT)d teoremas, nenhum fora do trio; o estatuto com a escada %(ESC)d/%(ESC)d (KERNEL_%(ESC)d_OF_%(ESC)d_FLAGS) e %(DECL)d
    no trio; o registro teste_de_veracidade_fase9_v397 segue selado (o quadro do topo le os numeros dele); (d) gate identico ao do cofre
    v397; um_version v398; (e) registro PT == EN == %(NREG)d, os %(NREG7)d nomes da v397 presentes, os novos = os 4 blocos, e so 5 vereditos
    da v397 mudados (a troca numerica da escada); (f) kernel %(FORM)d / %(DECL)d, todos no trio; (g) nenhum veredito do selo diz CONFIRMED.
    physical_verdict_allowed=False: os registros LEEM o kernel do proprio rito e conferem um calculo; nao abrem dado, nao sao teste."""
    import re as _re
    out = {"pass": False, "estatuto": "REAL(lido do cofre v398 e do v397 pelo nome) / dois ceticos por injecao", "physical_verdict_allowed": False}
    try:
        _c398 = CUSTODY_DIR.parent / ("um_unificado_" + "v398")
        _c397 = CUSTODY_DIR.parent / ("um_unificado_" + "v397")
        can = json.loads((_c398 / "um_absoluto.json").read_text(encoding="utf-8"))
        sl = json.loads((_c398 / "um_absoluto_selo.json").read_text(encoding="utf-8"))
        mf = json.loads((_c398 / "tgl_kernel_proof_manifest.json").read_text(encoding="utf-8"))
        pt = (_c398 / "um_absoluto_pt.txt").read_text(encoding="utf-8", errors="replace")
        en = (_c398 / "um_absoluto_en.txt").read_text(encoding="utf-8", errors="replace")
        pt397 = (_c397 / "um_absoluto_pt.txt").read_text(encoding="utf-8", errors="replace")
        can397 = json.loads((_c397 / "um_absoluto.json").read_text(encoding="utf-8"))
        gate397 = json.loads((_c397 / "CUSTODY_MANIFEST.json").read_text(encoding="utf-8")).get("gate")
    except (OSError, ValueError) as e:
        out["erro"] = "cofre ilegivel: %%r" %% (e,)
        return out
    core, core397 = can.get("core") or {}, can397.get("core") or {}
    novos = sorted(k for k in core if k not in core397)
    sumidos = sorted(k for k in core397 if k not in core)

    def _bloco_ok(b):
        if not isinstance(b, dict):
            return False
        vd = str(b.get("verdict") or "")
        return bool(b.get("all_verified") is True and b.get("does_not_gate_core") is True and ("GATE_UNMOVED" in vd or "GATE_UNTOUCHED" in vd)
                    and not _re.search(r"(?<![A-Z_])CONFIRMED", vd.replace("NOT_CONFIRMED", "")))
    maus = [k for k in novos if not _bloco_ok(core[k])]
    blocos_ok = bool(novos == ["afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398", "sonico_v398"] and not sumidos and not maus)
    kf, kf397 = core.get("kernel_formalization") or {}, core397.get("kernel_formalization") or {}
    n_band = len([k for k in kf if k not in kf397])
    band_ok = bool(n_band == %(NB)d)

    def _v398(c):
        try:
            so, af, cu, kh, tv, e = (c["sonico_v398"], c["afinacao_das_cordas_v398"], c["cunhagens_v398"], c["kh_n1_cobertura_v398"],
                                     c["teste_de_veracidade_fase9_v397"], c["estatuto_da_prova_v391"])
            kn, p1 = cu["kernel"], e["prova_1_kernel"]
            inc = "UNCONDITIONAL__NO_CERTIFICATE_AS_HYPOTHESIS"
            return bool(so.get("all_verified") is True and af.get("all_verified") is True and cu.get("all_verified") is True
                        and so["unconditional"]["composition"] == inc and so["unconditional"]["in_trio"] is True and so.get("exact_ladder") is True
                        and so["mechanics"]["passed"] is True and so["mechanics"]["n_checks"] == 8 and so.get("beta_ok") is True
                        and af["unconditional"]["composition"] == inc and af["unconditional"]["in_trio"] is True and af.get("exact_ladder") is True
                        and af["mechanics"]["passed"] is True and af["mechanics"]["n_checks"] == 7
                        and af.get("derives_strings_from_the_axiom") is False and af.get("geometry") == "OPEN"
                        and af["hypothesis"]["named_not_proved"] is True and af["hypothesis"]["name"] == "MasslessFirstLevel"
                        and list(kn.get("bandeiras") or []) == [2, 2] and list(kn.get("declaracoes_no_trio") or []) == [41, 41]
                        and len(cu.get("verbatim") or {}) >= 6
                        and "THE_CREDITATION_STEP_NOT_REACHED" in str(tv.get("verdict")) and tv.get("all_verified") is True
                        and (kh.get("lido") or {}).get("constantes_cobertas") == %(KHC)d and (kh.get("lido") or {}).get("teoremas_cobertos") == %(KHT)d
                        and "NONE_OUTSIDE_THE_TRIO" in str(kh.get("verdict"))
                        and p1["n_theorems_clean"] == p1["n_theorems_expected"] == %(ESC)d and p1["declaracoes_auditadas"] == p1["no_trio"] == %(DECL)d
                        and "KERNEL_%(ESC)d_OF_%(ESC)d_FLAGS" in str(e.get("verdict")))
        except (KeyError, TypeError, AttributeError):
            return False
    v398_ok = _v398(core)
    c1 = dict(core); af1 = json.loads(json.dumps(core.get("afinacao_das_cordas_v398") or {}))                           # cetico 1
    af1["derives_strings_from_the_axiom"] = True
    c1["afinacao_das_cordas_v398"] = af1
    cetico1_reprovou = (_v398(c1) is False)
    c2 = dict(core); cu2 = json.loads(json.dumps(core.get("cunhagens_v398") or {}))                                      # cetico 2
    try:
        cu2["kernel"]["bandeiras"] = [1, 2]
    except (KeyError, TypeError):
        pass
    c2["cunhagens_v398"] = cu2
    cetico2_reprovou = (_v398(c2) is False)
    gate = ((core.get("qg_closure") or {}).get("gate") or {})
    gate_ok = bool(gate.get("full_static_witness_exists") is False and str(sl.get("qg_closure_verdict")) == str(gate397)
                   and sl.get("um_version") == "v398")
    pat = _re.compile(r"^([a-z][a-z0-9_]{3,}) & ([A-Z][A-Z0-9_]{12,})", _re.M)
    reg_pt, reg_en, reg397 = dict(pat.findall(pt)), dict(pat.findall(en)), dict(pat.findall(pt397))
    mud = sorted(k for k in reg397 if reg_pt.get(k) != reg397[k])
    reg_novos = sorted(k for k in reg_pt if k not in reg397)
    reg_ok = bool(len(reg_pt) == len(reg_en) == %(NREG)d and len(reg397) == %(NREG7)d and all(k in reg_pt for k in reg397) and reg_novos == novos
                  and mud == %(MUD)r)
    fm = mf.get("formal_files_sha256") or {}
    ar_ = mf.get("axiom_report") or {}
    k_ok = bool(len(fm) == %(FORM)d and len(ar_) == %(DECL)d
                and not any(x_ not in ("propext", "Classical.choice", "Quot.sound") for v in ar_.values() for x_ in (v or [])))
    confs = [k for k, v in sl.items() if str(k).endswith("_verdict") and _re.search(r"(?<![A-Z_])CONFIRMED", str(v)) and "NOT_CONFIRMED" not in str(v)]
    ok = bool(blocos_ok and band_ok and v398_ok and cetico1_reprovou and cetico2_reprovou and gate_ok and reg_ok and k_ok and not confs)
    out.update({
        "blocos_novos_desde_v397": {"n": len(novos), "nomes": novos, "sumidos": sumidos, "fora_da_regra": maus, "ok": blocos_ok},
        "bandeiras_novas_desde_v397": {"n": n_band, "ok": band_ok},
        "registros_v398": {"ok": v398_ok,
                           "estatuto": "as composicoes das pedras Sonico e AfinacaoDasCordas sao INCONDICIONAIS no kernel do rito (no trio); os registros "
                                       "LEEM o kernel e conferem calculos (8 e 7 checagens); a lei de custo e INPUT; a hipotese MasslessFirstLevel e nomeada [KNOWN]; "
                                       "a geometria e OPEN; nada deriva as cordas do axioma; o quadro do Teste da Unica Palavra (v397) segue selado e intocado; "
                                       "validade no kernel nao e creditacao"},
        "ceticos": {"1_injecao": "afinacao_das_cordas_v398.derives_strings_from_the_axiom: False -> True", "1_reprovou": cetico1_reprovou,
                    "2_injecao": "cunhagens_v398.kernel.bandeiras = [1, 2]", "2_reprovou": cetico2_reprovou,
                    "leitura": "se uma injecao NAO reprovasse, o check nao discriminaria e a pedra reprovaria"},
        "gate": {"full_static_witness_exists": gate.get("full_static_witness_exists"), "identico_ao_cofre_v397": gate_ok},
        "registro_de_vereditos": {"pt": len(reg_pt), "en": len(reg_en), "esperado": %(NREG)d, "nomes_v397": len(reg397), "novos": len(reg_novos),
                                  "mudados_desde_v397": mud, "ok": reg_ok},
        "kernel": {"formais": len(fm), "termos": len(ar_), "ok": k_ok},
        "vereditos_do_selo_com_CONFIRMED": confs,
        "nao_se_afirma": ["que a TGL seja teoria de cordas, ou que as cordas derivem do axioma omega(I) = 1 (derives_strings_from_the_axiom = False)",
                          "que a natureza cobre ln 2 por oitava, ou que o seletor pague a oitava (a lei de custo e INPUT; nenhum termo o diz)",
                          "que o som seja onda num meio (sonico e a estrutura logaritmica e de oitava)",
                          "que a TGL esteja discriminada do LCDM a 5 sigma (o quadro do topo segue: o degrau da creditacao nao foi alcancado)",
                          "qual leitura da paridade da patente ACOM Mirror e canonica (decisao do operador [LEGAL])",
                          "qualquer veredito fisico (physical_verdict_allowed=False; gate INALTERADO)"],
        "pass": ok,
    })
    return out


''' % {"NB": NB, "KHC": KHC, "KHT": KHT, "ESC": ESC, "DECL": DECL, "NREG": NREG, "NREG7": NREG7, "FORM": FORM, "MUD": MUD}
troca("def shadow_the_station(core, selo):\n", FUNC.lstrip("\n") + "def shadow_the_station(core, selo):\n", "funcao _medir_v398_custodia")
troca('        "custodia_v397": _medir_v397_custodia(),\n',
      '        "custodia_v397": _medir_v397_custodia(),\n        "custodia_v398": _medir_v398_custodia(),\n', "entrada v47")
troca('    v46_pass = station["custodia_v397"]["pass"]\n',
      '    v46_pass = station["custodia_v397"]["pass"]\n'
      '    # v47 (v63): A CUSTODIA v398 -- o cofre v398 contra o v397, pelo nome: 4 blocos verificados que nao movem o gate, as pedras Sonico e\n'
      '    # AfinacaoDasCordas (composicoes incondicionais; nada deriva as cordas do axioma), registro %d; dois ceticos.\n'
      '    v47_pass = station["custodia_v398"]["pass"]\n' % NREG, "v47_pass")
troca("and v43_pass and v44_pass and v45_pass and v46_pass)\n", "and v43_pass and v44_pass and v45_pass and v46_pass and v47_pass)\n", "all_pass inclui v47")
troca('        verdict = ("FRONTEIRA_SINCRONIZADA_V397"\n',
      '        verdict = ("FRONTEIRA_SINCRONIZADA_V398"\n'
      '                   "__V398_O_SONICO_E_A_AFINACAO_DAS_CORDAS__COFRE_V398_CONTRA_O_V397_PELO_NOME__4_BLOCOS_NOVOS_VERIFICADOS_NENHUM_MOVE_O_GATE__%d_BANDEIRAS__ESCADA_%d_DE_%d_BANDEIRAS__KERNEL_%d_%d_NO_TRIO__SONICO_E_AFINACAO_COMPOSICOES_INCONDICIONAIS__NADA_DERIVA_AS_CORDAS_DO_AXIOMA__REGISTRO_%d_COM_OS_%d_DA_V397_E_5_MUDADOS__DOIS_CETICOS_REPROVAM__GATE_INALTERADO"\n'
      '                   "__V397"\n' % (NB, ESC, ESC, FORM, DECL, NREG, NREG7), "veredito v398 (o da v397 segue como sufixo)")
tmp = R + ".tmp_v63"; open(tmp, "wb").write(s.encode("utf-8"))
r = subprocess.run([sys.executable, "-m", "py_compile", tmp], capture_output=True, text=True)
if r.returncode != 0:
    os.remove(tmp); raise SystemExit("SINTAXE INVALIDA — nada trocado:\n" + (r.stderr or "")[:1500])
os.replace(tmp, R); print("runner v63: %d -> %d bytes | py_compile OK | backup .bak_v63_%s" % (len(raw), os.path.getsize(R), TS))
