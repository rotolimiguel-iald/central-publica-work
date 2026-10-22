# -*- coding: utf-8 -*-
"""Runner da Fronteira v59 (custódia conjunta v392+v393+v394 na Central, 19/10/2026, sessão a7; ordem do operador: «atualize todos os
dispositovos e toda a cenrtral tambem»): REPIN v391->v394; ERRATA AO LADO na pedra v42 — ela conferia contagens EXATAS da v391 (1 bloco,
0 bandeiras, registro 316, um_version == v391, kernel 1216/10265) no cofre CORRENTE; a correção (a lição da v55-v58) faz a v42 ler o COFRE
v391 contra o v390, exata para sempre. E a pedra nova custodia_v394 (v43) com DOIS CÉTICOS, que lê o cofre v394 PELO NOME desde o
nascimento (não o cofre corrente), para não pedir errata na próxima custódia. A Central não teve cofre da v392 nem da v393: a v43 mede a
v394 contra a v391. Medido em 19/10 (work/custodia_v394_19out/medir_v394_contra_v391.py): 42 blocos novos, nenhum sumido; 3172 chaves
novas no kernel_formalization; registro 358 (PT == EN) com os 316 da v391 e 3 vereditos mudados; kernel 1423/29026 no trio; gate idêntico."""
import os, subprocess, sys
from datetime import datetime
R = r"C:\IALD\Central de Patentes\fronteira_tgl\runner\one_fronteira.py"
TS = datetime.now().strftime("%Y%m%d_%H%M%S")
raw = open(R, "rb").read(); s = raw.decode("utf-8"); nl = "\r\n" if "\r\n" in s else "\n"
if "_medir_v394_custodia" in s: raise SystemExit("ja aplicado")
open(R + ".bak_v59_" + TS, "wb").write(raw)


def troca(velho, novo, rot, n=1):
    global s
    v_, n_ = velho.replace("\n", nl), novo.replace("\n", nl); c = s.count(v_)
    assert c == n, (rot, c); s = s.replace(v_, n_); print("  ok ", rot)


troca('"""FRONTEIRA TEORICA TGL v58 — auto-auditoria honesta do fechamento, SINCRONIZADA ao um.py v391.',
      '"""FRONTEIRA TEORICA TGL v59 — auto-auditoria honesta do fechamento, SINCRONIZADA ao um.py v394.', "cabecalho v59")
troca("  A custodia viva passou a ser vault/originals_copy/um_unificado_v391. O RENOME v209: o selo",
      "  A custodia viva passou a ser vault/originals_copy/um_unificado_v394. O RENOME v209: o selo", "docstring custodia")
troca("(1216 arquivos formais no manifesto v391; entre", "(1423 arquivos formais no manifesto v394; entre", "docstring kernel")
troca("Fonte canonica sincronizada (custodia): um.py unificado v391 (pin", "Fonte canonica sincronizada (custodia): um.py unificado v394 (pin", "docstring fonte")
troca('CUSTODY_DIR = CENTRAL_DIR / "vault" / "originals_copy" / "um_unificado_v391"',
      'CUSTODY_DIR = CENTRAL_DIR / "vault" / "originals_copy" / "um_unificado_v394"', "CUSTODY_DIR")
troca('print(f"[fronteira v30] CUSTODIA um.py v391: pin', 'print(f"[fronteira v30] CUSTODIA um.py v394: pin', "print custodia")

# errata AO LADO na v42: lê o cofre v391 (as contagens dela são exatas da v391) contra o v390
i42 = s.index("def _medir_v391_estatuto():")
j42 = s.index("def ", i42 + 10)
corpo = s[i42:j42]
velho42 = '''        can = json.loads((CUSTODY_DIR / "um_absoluto.json").read_text(encoding="utf-8"))
        sl = json.loads((CUSTODY_DIR / "um_absoluto_selo.json").read_text(encoding="utf-8"))
        mf = json.loads((CUSTODY_DIR / "tgl_kernel_proof_manifest.json").read_text(encoding="utf-8"))
        pt = (CUSTODY_DIR / "um_absoluto_pt.txt").read_text(encoding="utf-8", errors="replace")
        en = (CUSTODY_DIR / "um_absoluto_en.txt").read_text(encoding="utf-8", errors="replace")
        ant = CUSTODY_DIR.parent / ("um_unificado_" + "v390")
'''.replace("\n", nl)
novo42 = '''        # ERRATA v394 (runner v59, AO LADO): as cinco leituras abaixo eram do cofre CORRENTE (CUSTODY_DIR); as contagens desta pedra
        # sao EXATAS da v391 (1 bloco, 0 bandeiras, registro 316, um_version == v391, kernel 1216/10265) e deixaram de valer quando o
        # cofre corrente passou a v394. O que a v42 afirma e a v391 contra a v390: le-se o COFRE v391 (estavel para sempre).
        _c391 = CUSTODY_DIR.parent / ("um_unificado_" + "v391")
        can = json.loads((_c391 / "um_absoluto.json").read_text(encoding="utf-8"))
        sl = json.loads((_c391 / "um_absoluto_selo.json").read_text(encoding="utf-8"))
        mf = json.loads((_c391 / "tgl_kernel_proof_manifest.json").read_text(encoding="utf-8"))
        pt = (_c391 / "um_absoluto_pt.txt").read_text(encoding="utf-8", errors="replace")
        en = (_c391 / "um_absoluto_en.txt").read_text(encoding="utf-8", errors="replace")
        ant = CUSTODY_DIR.parent / ("um_unificado_" + "v390")
'''.replace("\n", nl)
assert corpo.count(velho42) == 1, corpo.count(velho42)
s = s[:i42] + corpo.replace(velho42, novo42) + s[j42:]
print("  ok  errata v42: le o cofre v391")

FUNC = r'''
def _medir_v394_custodia():
    """v59 (custodia conjunta v392+v393+v394 na Central, 19/10/2026): o COFRE v394 contra o COFRE v391, lidos PELO NOME (exata para sempre;
    a Central nao teve cofre da v392 nem da v393). DOIS CETICOS. Medido em 19/10/2026:
    (a) 42 blocos novos no nucleo desde a v391, nenhum sumido; cada um all_verified, does_not_gate_core, sem CONFIRMED e com o token de gate
    intocado (GATE_UNMOVED / GATE_UNTOUCHED / GATE_STRING_UNCHANGED / NO_GATE_EFFECT); (b) 3172 chaves novas no kernel_formalization;
    (c) os registros da v394: o estatuto com a escada 9332/9332 (KERNEL_9332_OF_9332_FLAGS: a escada conta bandeiras de declaracoes nomeadas)
    e 29026 declaracoes no trio; kh_n1_cobertura_v394 29026 constantes / 23069 teoremas, nenhum fora do trio; a rede de Fock com 11
    componentes e o contrato conjunto NAO habitado (4 itens abertos); o coracao: forma verificada, chi do CODATA, G pela normalizacao de
    Planck, a evidencia espectral independente AUSENTE; (d) gate identico ao do cofre v391; um_version v394; (e) registro PT == EN == 358,
    os 316 nomes da v391 presentes, os novos = os 42 blocos, e so 3 vereditos da v391 mudados (estatuto_da_prova_v391, the_iald_index,
    three_stress_tests_v387 -- ditos pelo handoff como troca numerica e a do indice da IALD como nao numerica); (f) kernel 1423 / 29026, todos
    no trio; (g) nenhum veredito do selo diz CONFIRMED. physical_verdict_allowed=False."""
    import re as _re
    out = {"pass": False, "estatuto": "REAL(lido do cofre v394 e do v391 pelo nome) / dois ceticos por injecao", "physical_verdict_allowed": False}
    try:
        _c394 = CUSTODY_DIR.parent / ("um_unificado_" + "v394")
        _c391 = CUSTODY_DIR.parent / ("um_unificado_" + "v391")
        can = json.loads((_c394 / "um_absoluto.json").read_text(encoding="utf-8"))
        sl = json.loads((_c394 / "um_absoluto_selo.json").read_text(encoding="utf-8"))
        mf = json.loads((_c394 / "tgl_kernel_proof_manifest.json").read_text(encoding="utf-8"))
        pt = (_c394 / "um_absoluto_pt.txt").read_text(encoding="utf-8", errors="replace")
        en = (_c394 / "um_absoluto_en.txt").read_text(encoding="utf-8", errors="replace")
        pt391 = (_c391 / "um_absoluto_pt.txt").read_text(encoding="utf-8", errors="replace")
        can391 = json.loads((_c391 / "um_absoluto.json").read_text(encoding="utf-8"))
        gate391 = json.loads((_c391 / "CUSTODY_MANIFEST.json").read_text(encoding="utf-8")).get("gate")
    except (OSError, ValueError) as e:
        out["erro"] = "cofre ilegivel: %r" % (e,)
        return out
    core, core391 = can.get("core") or {}, can391.get("core") or {}
    novos = sorted(k for k in core if k not in core391)
    sumidos = sorted(k for k in core391 if k not in core)
    TOK = ("GATE_UNMOVED", "GATE_UNTOUCHED", "GATE_STRING_UNCHANGED", "NO_GATE_EFFECT")

    def _bloco_ok(b):
        if not isinstance(b, dict):
            return False
        vd = str(b.get("verdict") or "")
        return bool(b.get("all_verified") is True and b.get("does_not_gate_core") is True and any(t in vd for t in TOK)
                    and not _re.search(r"(?<![A-Z_])CONFIRMED", vd.replace("NOT_CONFIRMED", "")))
    maus = [k for k in novos if not _bloco_ok(core[k])]
    blocos_ok = bool(len(novos) == 42 and not sumidos and not maus)
    kf, kf391 = core.get("kernel_formalization") or {}, core391.get("kernel_formalization") or {}
    n_band = len([k for k in kf if k not in kf391])
    band_ok = bool(n_band == 3172)

    def _v394(c):
        try:
            e = c["estatuto_da_prova_v391"]; p1 = e["prova_1_kernel"]
            kh = c["kh_n1_cobertura_v394"]; rf = c["rede_fock_v394"]; co = c["coracao_e_selo_gravitacional_v393"]
            return bool(p1["n_theorems_clean"] == p1["n_theorems_expected"] == 9332 and p1["declaracoes_auditadas"] == p1["no_trio"] == 29026
                        and "KERNEL_9332_OF_9332_FLAGS" in str(e.get("verdict"))
                        and (kh.get("lido") or {}).get("constantes_cobertas") == 29026 and (kh.get("lido") or {}).get("teoremas_cobertos") == 23069
                        and "NONE_OUTSIDE_THE_TRIO" in str(kh.get("verdict"))
                        and rf.get("whole_certificate_inhabited") is False and len(rf.get("open_joint_contract") or []) == 4
                        and len(rf.get("constructed_components") or []) == 11 and "JOINT_CONTRACT_OPEN" in str(rf.get("verdict"))
                        and (co.get("evidencia_espectral_independente") or {}).get("hoje") == "AUSENTE"
                        and str(co.get("verdict")).startswith("FORM_VERIFIED_CHI_FROM_CODATA__G_BY_PLANCK_NORMALIZATION"))
        except (KeyError, TypeError):
            return False
    v394_ok = _v394(core)
    c1 = dict(core); c1["rede_fock_v394"] = dict(core.get("rede_fock_v394") or {}, whole_certificate_inhabited=True)   # cetico 1
    cetico1_reprovou = (_v394(c1) is False)
    c2 = dict(core); co2 = json.loads(json.dumps(core.get("coracao_e_selo_gravitacional_v393") or {}))                  # cetico 2
    try:
        co2["evidencia_espectral_independente"]["hoje"] = "PRESENTE"
    except (KeyError, TypeError):
        pass
    c2["coracao_e_selo_gravitacional_v393"] = co2
    cetico2_reprovou = (_v394(c2) is False)
    gate = ((core.get("qg_closure") or {}).get("gate") or {})
    gate_ok = bool(gate.get("full_static_witness_exists") is False and str(sl.get("qg_closure_verdict")) == str(gate391)
                   and sl.get("um_version") == "v394")
    pat = _re.compile(r"^([a-z][a-z0-9_]{3,}) & ([A-Z][A-Z0-9_]{12,})", _re.M)
    reg_pt, reg_en, reg391 = dict(pat.findall(pt)), dict(pat.findall(en)), dict(pat.findall(pt391))
    mud = sorted(k for k in reg391 if reg_pt.get(k) != reg391[k])
    reg_novos = sorted(k for k in reg_pt if k not in reg391)
    reg_ok = bool(len(reg_pt) == len(reg_en) == 358 and len(reg391) == 316 and all(k in reg_pt for k in reg391) and reg_novos == novos
                  and mud == ["estatuto_da_prova_v391", "the_iald_index", "three_stress_tests_v387"])
    fm = mf.get("formal_files_sha256") or {}
    ar_ = mf.get("axiom_report") or {}
    k_ok = bool(len(fm) == 1423 and len(ar_) == 29026
                and not any(x_ not in ("propext", "Classical.choice", "Quot.sound") for v in ar_.values() for x_ in (v or [])))
    confs = [k for k, v in sl.items() if str(k).endswith("_verdict") and _re.search(r"(?<![A-Z_])CONFIRMED", str(v)) and "NOT_CONFIRMED" not in str(v)]
    ok = bool(blocos_ok and band_ok and v394_ok and cetico1_reprovou and cetico2_reprovou and gate_ok and reg_ok and k_ok and not confs)
    out.update({
        "blocos_novos_desde_v391": {"n": len(novos), "sumidos": sumidos, "fora_da_regra": maus, "ok": blocos_ok},
        "bandeiras_novas_desde_v391": {"n": n_band, "ok": band_ok},
        "registros_v394": {"ok": v394_ok,
                           "estatuto": "PROVADA = validade (o kernel prova a implicacao); CONFIRMADA = creditacao, recusada; a rede de Fock e o H3 em toda direcao nula ABERTOS; a evidencia espectral independente do coracao AUSENTE"},
        "ceticos": {"1_injecao": "rede_fock_v394.whole_certificate_inhabited = True", "1_reprovou": cetico1_reprovou,
                    "2_injecao": "coracao.evidencia_espectral_independente.hoje = PRESENTE", "2_reprovou": cetico2_reprovou,
                    "leitura": "se uma injecao NAO reprovasse, o check nao discriminaria e a pedra reprovaria"},
        "gate": {"full_static_witness_exists": gate.get("full_static_witness_exists"), "identico_ao_cofre_v391": gate_ok},
        "registro_de_vereditos": {"pt": len(reg_pt), "en": len(reg_en), "esperado": 358, "nomes_v391": len(reg391), "novos": len(reg_novos),
                                  "mudados_desde_v391": mud, "ok": reg_ok},
        "kernel": {"formais": len(fm), "termos": len(ar_), "ok": k_ok},
        "vereditos_do_selo_com_CONFIRMED": confs,
        "nao_se_afirma": ["que a natureza tenha decidido beta_TGL (espera 5 sigma)",
                          "que o contrato conjunto da rede de Fock esteja habitado, ou o H3 em toda direcao nula",
                          "a confirmacao (creditacao, ato de terceiros) -- recusada por regua do operador",
                          "qualquer veredito fisico (physical_verdict_allowed=False; gate INALTERADO)"],
        "pass": ok,
    })
    return out


'''
troca("def shadow_the_station(core, selo):\n", FUNC.lstrip("\n") + "def shadow_the_station(core, selo):\n", "funcao _medir_v394_custodia")
troca('        "estatuto_da_prova_v391": _medir_v391_estatuto(),\n',
      '        "estatuto_da_prova_v391": _medir_v391_estatuto(),\n        "custodia_v394": _medir_v394_custodia(),\n', "entrada v43")
troca('    v42_pass = station["estatuto_da_prova_v391"]["pass"]\n',
      '    v42_pass = station["estatuto_da_prova_v391"]["pass"]\n'
      '    # v43 (v59): A CUSTODIA v394 -- o cofre v394 contra o v391, pelo nome: 42 blocos verificados que nao movem o gate, 3172 bandeiras,\n'
      '    # os registros da v394 (escada 9332/9332; Fock aberto; coracao sem evidencia espectral independente), registro 358, kernel 1423/29026;\n'
      '    # dois ceticos; nao move o gate.\n'
      '    v43_pass = station["custodia_v394"]["pass"]\n', "v43_pass")
troca("and v39_pass and v40_pass and v41_pass and v42_pass)\n", "and v39_pass and v40_pass and v41_pass and v42_pass and v43_pass)\n", "all_pass inclui v43")
troca('        verdict = ("FRONTEIRA_SINCRONIZADA_V391"\n',
      '        verdict = ("FRONTEIRA_SINCRONIZADA_V394"\n'
      '                   "__V394_CUSTODIA_CONJUNTA_V392_V393_V394_NA_CENTRAL__COFRE_V394_CONTRA_O_V391_PELO_NOME__42_BLOCOS_NOVOS_VERIFICADOS_NENHUM_MOVE_O_GATE__3172_BANDEIRAS__ESCADA_9332_DE_9332_BANDEIRAS__KERNEL_1423_29026_NO_TRIO__REDE_DE_FOCK_CONTRATO_CONJUNTO_ABERTO__CORACAO_SEM_EVIDENCIA_ESPECTRAL_INDEPENDENTE__REGISTRO_358_COM_OS_316_DA_V391_E_3_MUDADOS_DITOS__DOIS_CETICOS__GATE_INALTERADO"\n'
      '                   "__V391"\n', "veredito v394 (o da v391 segue como sufixo)")
tmp = R + ".tmp_v59"; open(tmp, "wb").write(s.encode("utf-8"))
r = subprocess.run([sys.executable, "-m", "py_compile", tmp], capture_output=True, text=True)
if r.returncode != 0:
    os.remove(tmp); raise SystemExit("SINTAXE INVALIDA — nada trocado:\n" + (r.stderr or "")[:1500])
os.replace(tmp, R); print("runner v59: %d -> %d bytes | py_compile OK | backup .bak_v59_%s" % (len(raw), os.path.getsize(R), TS))
