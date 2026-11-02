# -*- coding: utf-8 -*-
# Inventario do conjunto D (29/10/2026): sha256 LIDO DO DISCO por script, nunca de memoria.
# Nao abre amostras de strain (apenas bytes para hash), nao abre posterior de nenhum evento do conjunto D.
# Calcula tambem a projecao de PODER de planejamento do conjunto D a partir de
# (SNR GWOSC, delta_pred V1, ajuste sigma(SNR) da bancada) -- sem nenhum dado de deformacao.
import json, hashlib, os, sys, time, math

W = "C:/IALD/Central de Patentes/work/conjunto_D_20261029"
CH = "C:/IALD/Central de Patentes/Chatgpt"
R13 = CH + "/ORDEM_013_RINGDOWN"
BIS = R13 + "/bis"
O18 = CH + "/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d"
V1D = "C:/IALD/Bancada_Um/investigacao/preregistro_ramo_b_05out"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


files = []


def add(path, papel, estatuto="REAL"):
    files.append((path, papel, estatuto))


for n, papel in [("PREREGISTRO_RAMO_B_RINGDOWN_V1.json", "pre-registro V1 congelado (JSON)"),
                 ("PREREGISTRO_RAMO_B_RINGDOWN_V1.md", "pre-registro V1 congelado (MD)"),
                 ("V1_RAMO_B_HASHES.json", "hashes do V1"),
                 ("PODER_CEGO_RAMO_B_v2.json", "poder cego (so sigma e spin) do A/B/C"),
                 ("poder_cego_ramo_b_v2.py", "script do poder cego"),
                 ("gerar_preregistro_ramo_b_05out.py", "gerador do V1")]:
    add(V1D + "/" + n, papel)
add("C:/IALD/Bancada_Um/bancada/gw_stack.py", "funcao de veredito da Fase 6 (ECO V3): empilhar() + veredito()")
add("C:/IALD/Bancada_Um/investigacao/fase6_eco_radical_01out/preregistro_fase6.py", "constantes CR da Fase 6 (min_eventos=10, poder_min=5, z_excl=5, sist_max=0.3)")

for tree, papel in [("e2_code", "013-bis v1 (27/09)"), ("e2_code_v1_1", "015 v1.1"), ("e2_code_v1_1_2", "015 v1.1.2 (ultima)")]:
    d = BIS + "/" + tree
    for n in sorted(os.listdir(d)):
        if n.endswith(".py"):
            add(d + "/" + n, tree + " :: " + papel)
for p, papel in [(BIS + "/015/amend_source_runner.py", "emenda 015 do source/runner (grade de geracao, EDOM)"),
                 (BIS + "/015/amend_clock_and_nulls.py", "emenda 015 relogio/nulos"),
                 (BIS + "/015/amend_reading_and_failure.py", "emenda 015 leitura/falha"),
                 (BIS + "/015/t05/measure.py", "T05 diagnosticos NAO-CEGOS"),
                 (BIS + "/015/t05/RESULT.json", "T05 resultado"),
                 (BIS + "/015/t03/R5/INPUT_MANIFEST.json", "R5 manifesto de entradas da qualificacao de fonte"),
                 (BIS + "/015/t03/R5/generation_4096/RESULT.json", "R5 qualificacao de fonte (1015 waveforms)"),
                 (BIS + "/015/E2_PE_JOBS_ALLOCATION_015_V4.json", "alocacao de jobs 015 V4 (GW250114)")]:
    add(p, papel)

for n in ["RINGDOWN_5SIGMA_V1.json", "RINGDOWN_5SIGMA_V1_1.json", "RINGDOWN_5SIGMA_V1_1_1.json",
          "RINGDOWN_5SIGMA_V1_1_2.json", "RINGDOWN_5SIGMA_V1_1_3.json", "ORCAMENTO_40H.json"]:
    add(R13 + "/" + n, "registro/orcamento da cadeia 013-bis/015")
for n in ["PART_B_BUDGET_START.json", "PART_015_BUDGET_START.json", "FINAL_DELIVERY_RECEIPT.json",
          "E3_PILOT_FAILURE_AUDIT_V1.json", "C3_C6_TIMING_013BIS.json", "E0_SNR_INFORMATION_FIT.json",
          "E0_SNR_FIT_REVIEW.md", "B1_DELIVERY_MANIFEST.json", "B2_DELIVERY_MANIFEST.json",
          "B3_DELIVERY_MANIFEST.json", "B4_TEST_DELIVERY_MANIFEST.json", "B5_DELIVERY_MANIFEST.json"]:
    add(BIS + "/" + n, "recibo/manifesto da bancada")
for n in ["COST_RECEIPT.json", "SYSTEMATICS_COST.json", "SYSTEMATICS_ADENDO.md"]:
    add(BIS + "/e0_core/" + n, "custo/sistematica E0 (escalar)")

for d in ["E3_PSEOB_PILOT_V2_S220", "E3_PSEOB_PILOT_V2_S220_C1", "E3_PSEOB_PILOT_V2_S220_H1"]:
    for n in ["CONTROLLER.json", "PRIVATE_CONVERGENCE.json", "FAILURE.json"]:
        p = R13 + "/cache/" + d + "/" + n
        if os.path.exists(p):
            add(p, "piloto GW250114 (calibracao NOT_BLIND; nao e evento de D): " + d)

for n in ["MANIFESTO_CONJUNTO_D.json", "PROPOSTA_MANIFESTO_METADATA_D.json", "NOTA_CONJUNTO_D.md",
          "PLANO_PILOTO_SINTETICO_SO220.json", "AUDITORIA_INSTRUMENTO_SO220.json",
          "p3_scientific_design_proposal/PROPOSTA_CONTINUACAO.md",
          "p3_startup_pin_preparation/driver_p3.py", "p3_startup_pin_preparation/launch_p3.py",
          "p3_startup_pin_preparation/ROOT_DECISION.json", "p3_startup_pin_preparation/COMANDO_CANDIDATO.json"]:
    add(O18 + "/" + n, "preparacao Codex ORDEM 018", "DECLARADO")
for n in ["PREPARACAO_GATE.md", "RESULTADO.json"]:
    add(CH + "/TUNEL/DO_CHATGPT/ORDEM_019/F4.2/" + n, "preparacao F4.2 (07/10)", "DECLARADO")

add("C:/IALD/Central de Patentes/work/cunhagens_13out/OPERADOR_29out_autoriza_conjunto_D_verbatim.txt", "autorizacao verbatim do operador, 29/10 (registrada pela gerencia, Mapa seq 1545)", "INPUT")
add(W + "/rota_mapa_autorizacao_D_29out.json", "registro da autorizacao no Mapa (gerencia c1, 29/10)", "DECLARADO")
add("C:/IALD/Bancada_Um/fontes_externas/gwosc_o4/GWOSC_O4_32S_V1.manifest.json", "manifesto de strain 32s/4096s (336 OK)")
add("C:/IALD/Bancada_Um/investigacao/fase6_eco_radical_01out/catalogo_v3.csv", "catalogo residente (GPS)")
add("C:/IALD/Central de Patentes/work/cadeia_de_selo/v386/ramo_b/pre_registro/RECONCILIACAO_CONJUNTO_D.json", "reconciliacao 44/14/10")
add("C:/IALD/Central de Patentes/work/cadeia_de_selo/v386/ramo_b/dados_na_casa/INVENTARIO_DADOS_NA_CASA_RAMO_B_v386.json", "inventario de dados na casa")

for n in ["smoke/smoke_pseob.py", "smoke/smoke_pseob_saida.txt", "smoke/dq_meta.py", "smoke/dq_meta2.py",
          "smoke/dq_meta_D_v2.json", "smoke/bounds_corners.py", "projecao_poder_D.py", "PROJECAO_PODER_D_planejamento.json", "copias_somente_leitura_v1_1_2/pseob_source.py",
          "copias_somente_leitura_v1_1_2/temporal_contract.py"]:
    p = W + "/" + n
    if os.path.exists(p):
        add(p, "artefato desta sessao (29/10)", "REAL")

rows = []
for p, papel, est in files:
    if not os.path.exists(p):
        rows.append(dict(path=p, papel=papel, existe=False, estatuto="AUSENTE"))
        continue
    s = sha(p)
    rows.append(dict(path=p, papel=papel, existe=True, bytes=os.path.getsize(p), sha256=s, sha16=s[:16],
                     estatuto_conteudo=est, mtime=time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(os.path.getmtime(p)))))

EV = ["GW230919_215712", "GW240513_183302", "GW240920_073424", "GW240923_204006", "GW241111_111552",
      "GW241130_034908", "GW241210_060606", "GW250104_015122", "GW250109_010541", "GW250118_170523"]
man = json.load(open("C:/IALD/Bancada_Um/fontes_externas/gwosc_o4/GWOSC_O4_32S_V1.manifest.json", encoding="utf-8"))
v1 = json.load(open(V1D + "/PREREGISTRO_RAMO_B_RINGDOWN_V1.json", encoding="utf-8"))
prev = {r["evento"]: r for r in v1["spec"]["conjuntos"]["D"]["previsao_da_hipotese_por_evento_INFORMACAO_CEGA"]}
prop = json.load(open(O18 + "/PROPOSTA_MANIFESTO_METADATA_D.json", encoding="utf-8"))
gps = {}
pe = prop["events"]
items = pe.items() if isinstance(pe, dict) else [((v.get("event") or v.get("evento")), v) for v in pe]
prop_rows = {}
for k, v in items:
    prop_rows[k] = {kk: v[kk] for kk in v if not isinstance(v[kk], (dict, list))}
    gps[k] = v.get("GPS_proposed", v.get("gps_proposed", v.get("GPS")))

strain = []
t0 = time.time()
for e in EV:
    for s in [x for x in man["series"] if x["event"] == e]:
        h = s["hdf5"].replace("/mnt/c/", "C:/")
        n = s["npz"].replace("/mnt/c/", "C:/")
        sh = sha(h)
        sn = sha(n)
        strain.append(dict(event=e, det=s["det"], hdf5=h, hdf5_bytes=os.path.getsize(h), hdf5_sha256=sh,
                           hdf5_sha256_confere_manifesto=(sh == s["hdf5_sha256"]), npz=n, npz_sha256=sn,
                           npz_sha256_confere_manifesto=(sn == s["npz_sha256"]), t0_npz=s["t0"], fs=s["fs"]))
hash_seconds = time.time() - t0

out = dict(gerado=time.strftime("%Y-%m-%dT%H:%M:%S%z"), script=os.path.basename(__file__), script_sha256=sha(__file__),
           arquivos=rows, strain_D=strain, strain_hash_seconds=hash_seconds, D10=EV, gps_proposto=gps,
           proposta_linhas_escalares=prop_rows,
           previsao_V1_por_evento={e: {k: prev[e][k] for k in ("SNR_rede_GWOSC", "Mf_det_mediana_GR", "chi_f_mediana_GR", "k_kms", "N_a", "x", "delta_pred_exato")} for e in EV})
json.dump(out, open(W + "/INVENTARIO_D_29out.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("arquivos", len(rows), "ausentes", [r["path"] for r in rows if not r["existe"]])
print("strain", len(strain), "hdf5 confere:", all(s["hdf5_sha256_confere_manifesto"] for s in strain),
      "npz confere:", all(s["npz_sha256_confere_manifesto"] for s in strain), "hash_s=%.1f" % hash_seconds)
print("gps", gps)
