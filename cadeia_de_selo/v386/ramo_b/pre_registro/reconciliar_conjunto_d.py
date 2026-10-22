# -*- coding: utf-8 -*-
"""reconciliar_conjunto_d.py -- G5: reconciliar «31 dos 45» (memoria 22/09, gerencia) x 44 test_candidates (RINGDOWN_5SIGMA_V1, 22/09 21:44Z)
lendo o CRITERIO do proprio registro (quality_INPUT, publication_census, test_candidates[*].role/eligible/data_quality_hold) e contando.
So leitura fora desta pasta; nao le valor central nenhum; nao baixa nada. Saida: RECONCILIACAO_CONJUNTO_D.json ao lado."""
import json, hashlib, os, collections
R = r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "RECONCILIACAO_CONJUNTO_D.json")
MANIF = r"C:\IALD\Bancada_Um\fontes_externas\gwosc_o4\GWOSC_O4_32S_V1.manifest.json"
CENSO = os.path.join(R, "bis", "e2_publication_census", "PUBLICATION_CENSUS.json")
P5 = os.path.join(R, "RINGDOWN_5SIGMA_V1.json")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


j5 = json.load(open(P5, encoding="utf-8"))
tc = j5["test_candidates"]
out = {"fontes": {"RINGDOWN_5SIGMA_V1.json": sha(P5), "PUBLICATION_CENSUS.json": sha(CENSO) if os.path.exists(CENSO) else "nao achado"},
       "registered_utc": j5.get("registered_utc"), "status": j5.get("status"),
       "quality_INPUT": j5.get("quality_INPUT"),
       "publication_census_resumo": {k: j5["publication_census"].get(k) for k in ("known_pseob_unique", "additional_published_exclusions", "scope", "sha256")}}
out["n_test_candidates"] = len(tc)
out["por_role"] = dict(collections.Counter(v.get("role") for v in tc.values()))
out["por_eligible"] = dict(collections.Counter(str(v.get("eligible")) for v in tc.values()))
out["por_run"] = dict(collections.Counter(v.get("run") for v in tc.values()))
out["por_publication_status"] = dict(collections.Counter(v.get("publication_status") for v in tc.values()))
eleg = [e for e, v in tc.items() if v.get("eligible") is True]
hold = [e for e, v in tc.items() if v.get("data_quality_hold") is True]
eleg_sem_hold = [e for e in eleg if e not in hold]
pend = [e for e, v in tc.items() if v.get("eligible") is None]
reprov = [e for e, v in tc.items() if v.get("eligible") is False]
# por que os reprovados reprovam (contra o quality_INPUT)
qi = j5["quality_INPUT"]
motivos = collections.Counter()
for e in reprov:
    v = tc[e]
    m = []
    if v.get("SNR_network_GWOSC") is not None and v["SNR_network_GWOSC"] < qi["network_snr_min_inclusive"]:
        m.append("SNR<%s" % qi["network_snr_min_inclusive"])
    if v.get("GR_final_mass_detector_median") is not None and v["GR_final_mass_detector_median"] < qi["Mf_detector_median_min_solar_inclusive"]:
        m.append("Mf_det<%s" % qi["Mf_detector_median_min_solar_inclusive"])
    if v.get("GR_final_spin_median") is not None and v["GR_final_spin_median"] >= qi["chi_final_median_max_exclusive"]:
        m.append("chi_f>=%s" % qi["chi_final_median_max_exclusive"])
    motivos["+".join(m) or "sem_motivo_identificado"] += 1
out["reprovados_motivo_contra_quality_INPUT"] = dict(motivos)
out["conjunto_D"] = {
    "elegiveis_eligible_True": {"n": len(eleg), "eventos": eleg},
    "com_data_quality_hold": {"n": len(hold), "eventos": hold},
    "elegiveis_sem_hold": {"n": len(eleg_sem_hold), "eventos": eleg_sem_hold},
    "pendentes_AWAITING_GR_METADATA": {"n": len(pend), "eventos": pend},
    "reprovados_INPUT_NOT_MET": {"n": len(reprov)},
    "criterio_do_registro": "eligible = quality_INPUT (SNR_rede >= 12; M_f,det mediana >= 40 Msun; 0 <= chi_f < 0,98; fonte GWOSC/GR IMR) E ausente do corpus de publicacao congelado em 22/09 20:32Z (PUBLICATION_CENSUS: FOUND = analise publicada que admite desvios QNM de f/tau) E fora do GWTC-5.0 33 / GWTC-3 18 / corpus auditado de 39",
}
# strain em casa (banco O4 da Bancada; manifesto): busca por substring do nome do evento
mtxt = open(MANIF, encoding="utf-8", errors="replace").read() if os.path.exists(MANIF) else ""
out["fontes"]["GWOSC_O4_32S_V1.manifest.json"] = sha(MANIF) if os.path.exists(MANIF) else "nao achado"
out["strain_em_casa_pelo_manifesto_O4"] = {e: (e in mtxt) for e in eleg + pend}
out["strain_em_casa_resumo"] = {"elegiveis_com_strain": sum(1 for e in eleg if e in mtxt), "elegiveis_sem_hold_com_strain": sum(1 for e in eleg_sem_hold if e in mtxt),
                                "pendentes_com_strain": sum(1 for e in pend if e in mtxt), "todos_44_com_strain": sum(1 for e in tc if e in mtxt)}
# os dois censos, lado a lado
out["os_dois_censos"] = {
    "memoria_22set_gerencia": "«31 dos 45 eventos O4 com strain publico nao tem dtau publicado» (ordem-013-confrontacao-ringdown.md l.102; ORDEM 013-bis §(j): 45 = GWTC-5.0 com SNR_rede >= 12 e strain publico; 31 = sem posterior pSEOBNR publicado; contagem da gerencia ANTES do censo congelado da bancada)",
    "registro_V1_bancada_22set_21h44Z": "test_candidates = 44 (O4a 12 + O4b 31 + O4c 1) = TODOS os eventos O4 fora do corpus auditado; destes, eligible True = %d (quality_INPUT atendido e ausentes do censo congelado), com hold de qualidade = %d, pendentes de metadados GR = %d, reprovados no quality_INPUT = %d" % (len(eleg), len(hold), len(pend), len(reprov)),
    "T01_ORDEM_015_RELATORIO_PARCIAL": "«Registro: 44 test_candidates = 14 elegiveis + 22 reprovados + 8 pendentes» (bis/015/t01_core/RELATORIO_PARCIAL.md l.15)",
    "leitura": "os dois numeros nao medem a mesma coisa: 45/31 e o universo com strain e SNR >= 12 sem posterior publicado (contagem da gerencia); 44 e o universo do registro e 14 e o que passa no criterio do registro (10 sem pendencia de qualidade). O numero UNICO do conjunto D para este V1 e o do criterio do registro.",
}
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: out[k] for k in ("n_test_candidates", "por_role", "por_eligible", "por_run", "reprovados_motivo_contra_quality_INPUT", "strain_em_casa_resumo")}, ensure_ascii=False, indent=1))
print("elegiveis:", eleg)
print("hold:", hold)
print("pendentes:", pend)
print("saida:", OUT, sha(OUT)[:16], os.path.getsize(OUT), "B")
