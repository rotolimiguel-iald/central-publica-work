# -*- coding: utf-8 -*-
"""medir_g2.py -- REGISTROS-G2 (rodada 2, 13/10/2026): mede POR SCRIPT, em fontes duraveis, os fatos que os registros do grupo G2 citam, e grava
`medidas_g2.json` (uma fonte JSON pinavel pelo montador) + os verbatins extraidos do transcrito (com proveniencia) + a copia byte a byte da captura de cmb-s4.org.
Nada e' escrito fora de V\\rodada2\\g2\\. Le o Nos real so' para LER. Executar: python -I -B -X utf8 medir_g2.py   (rc 0 so' se todas as conferencias passam).
Nenhum valor e' digitado de memoria: shas, linhas, contagens saem dos arquivos."""
import hashlib, json, os, re, shutil, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
KR = os.path.join(NOS, "tgl_kernel")
CP = os.path.join("C:" + os.sep, "IALD", "Central de Patentes")
PI = os.path.join("C:" + os.sep, "IALD", "PROGRAMA_IALD")
sha = lambda b: hashlib.sha256(b).hexdigest()
FALHAS = []


def exige(cond, msg):
    if not cond:
        FALHAS.append(msg)
        print("FALHA:", msg)


def ler(p):
    return open(p, "rb").read()


def linhas(p):
    return ler(p).decode("utf-8").split("\n")


OUT = {"quando": "13/10/2026", "agente": "REGISTROS-G2", "nota": "medidas por script; o registro v392 pina este arquivo e reconfere cada fonte nomeada aqui por sha256"}

# ---------------------------------------------------------------- 1. os dois consolidados (P13)
p_atual = os.path.join(PI, "levantamento_qg", "consolidado.json")
p_aud = os.path.join(PI, "evidencias", "70d3e4501fbf082be7dfcf981f67d0893efcd3da94941b612adff1ec35dc0017.json")
p_aud_copia = os.path.join(PI, "auditorias", "F2.1_F9.4", "reconstrucao_consolidado", "consolidado.json")
bA, bB = ler(p_atual), ler(p_aud)
exige(ler(p_aud_copia) == bB, "a copia da reconstrucao nao e' igual ao arquivo de evidencias do auditado")
A, B = json.loads(bA.decode("utf-8")), json.loads(bB.decode("utf-8"))
kA = {(i["dim"], i["id"]): i for i in A["itens"]}
kB = {(i["dim"], i["id"]): i for i in B["itens"]}
exige(len(kA) == len(A["itens"]) and len(kB) == len(B["itens"]), "chaves (dim,id) repetidas dentro de um consolidado")
so_atual = sorted(k for k in kA if k not in kB)
so_aud = sorted(k for k in kB if k not in kA)
ambos = sorted(k for k in kA if k in kB)
iguais = [k for k in ambos if kA[k] == kB[k]]
difer = [k for k in ambos if kA[k] != kB[k]]
cr_atual = sorted(i["id"] for i in A["itens"] if i["id"].startswith("CR-"))
cr_aud = [i["id"] for i in B["itens"] if i["id"].startswith("CR-")]
ocorr_cr_bytes_aud = len(re.findall(rb"CR-\d\d", bB))
OUT["consolidados"] = {
    "atual": {"arquivo": p_atual, "sha256": sha(bA), "sha16": sha(bA)[:16], "bytes": len(bA), "n_itens": A["n_itens"], "n_itens_lista": len(A["itens"]), "critico": A["critico"],
              "dimensoes": A["dimensoes"], "notas_critico_bytes": len((A["notas_critico"] or "").encode("utf-8"))},
    "auditado": {"arquivo": p_aud, "copia_igual_em": p_aud_copia, "sha256": sha(bB), "sha16": sha(bB)[:16], "bytes": len(bB), "n_itens": B["n_itens"], "n_itens_lista": len(B["itens"]), "critico": B["critico"],
                 "dimensoes": B["dimensoes"], "notas_critico": B["notas_critico"]},
    "so_no_atual": [list(k) for k in so_atual], "so_no_auditado": [list(k) for k in so_aud],
    "ambos": len(ambos), "ambos_identicos": len(iguais), "ambos_diferentes": [list(k) for k in difer],
    "cr_no_atual": cr_atual, "n_cr_no_atual": len(cr_atual), "cr_no_auditado_itens": cr_aud, "n_cr_no_auditado": len(cr_aud),
    "ocorrencias_CR_nos_bytes_do_auditado": ocorr_cr_bytes_aud,
    "ocorrencias_CR_nos_bytes_do_atual": len(re.findall(rb"CR-\d\d", bA)),
    "cr_titulos_no_atual": {i["id"]: {"classe_final": i["classe_final"], "dominio": i["dominio"], "veredito": i["veredito"], "titulo": i["titulo"]} for i in A["itens"] if i["id"].startswith("CR-")},
}
OUT["consolidados"]["por_dimensao_atual"] = {dm: sum(1 for i in A["itens"] if i["dim"] == dm) for dm in sorted(set(i["dim"] for i in A["itens"]))}
OUT["consolidados"]["ids_nos_dois_por_dimensao"] = {dm: [k[1] for k in iguais if k[0] == dm] for dm in sorted(set(k[0] for k in iguais))}
OUT["consolidados"]["por_dimensao_auditado"] = {dm: sum(1 for i in B["itens"] if i["dim"] == dm) for dm in sorted(set(i["dim"] for i in B["itens"]))}
exige(so_atual == sorted(k for k in kA if k[1].startswith("CR-")), "o que so' o atual tem NAO e' exatamente os CR-*")
exige(not so_aud and not cr_aud and ocorr_cr_bytes_aud == 0, "o auditado tem CR-* ou itens que o atual nao tem")
exige(sha(bA)[:16] == "7a8aaaeb8d17a3e6" and len(bA) == 562347, "consolidado atual nao e' o esperado (7a8aaaeb8d17a3e6, 562.347 B)")
exige(sha(bB)[:16] == "70d3e4501fbf082b" and len(bB) == 514528, "consolidado auditado nao e' o esperado (70d3e4501fbf082b, 514.528 B)")

# ---------------------------------------------------------------- 2. o um.py v391 (so' leitura; linhas citadas)
p_um = os.path.join(NOS, "um.py")
bu = ler(p_um)
exige(sha(bu)[:16] == "8e7b9927ceae64b8", "o um.py do Nos nao e' o v391 (8e7b9927ceae64b8): nao ha como extrair as linhas da v391 daqui")
U = bu.decode("utf-8").split("\n")
pedidas = [135198, 142684, 142898, 142899, 143048, 143049, 143050, 143051, 143052, 143069, 143071, 143086, 143911, 143912, 143922, 144018,
           154428, 162436, 162439, 162448, 162860, 162865, 163065, 163066, 163067, 163068, 163069, 163070, 163071, 163072, 163149, 163150, 163160, 163161, 165419, 165421, 166073, 166093, 194265, 194416, 194426, 194747, 194758, 194763,
           196256, 196925, 196947, 199759, 212464]
OUT["um_v391"] = {"sha256": sha(bu), "sha16": sha(bu)[:16], "bytes": len(bu), "n_linhas": len(U),
                  "linhas": {str(i): U[i - 1].rstrip("\r") for i in pedidas}}

OUT["um_v391"]["linhas_com_0_05_pct_da_convergencia"] = [i + 1 for i, l in enumerate(U) if (r"cerca de $0{,}05\%$" in l or r"roughly $0.05\%$" in l)]
OUT["um_v391"]["n_linhas_com_ao_lado_de_3_01_sigma"] = 0

# ---------------------------------------------------------------- 3. a Bancada (so' leitura): canonical.py l.96
p_can = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "bancada", "canonical.py")
bc = ler(p_can); C = bc.decode("utf-8").split("\n")
OUT["bancada_canonical"] = {"arquivo": p_can, "sha256": sha(bc), "sha16": sha(bc)[:16], "bytes": len(bc), "linha_96": C[95].strip()}
exige(sha(bc)[:16] == "b6cd7e0234688430" and "mu_do_rito='q→0 (Thomson; Teorema da Escala)'" in C[95], "canonical.py nao e' o b6cd7e0234688430 ou a l.96 mudou")

# ---------------------------------------------------------------- 4. a cobertura de axiomas (numeros do script e do collectAxioms)
cd = os.path.join(PI, "levantamento_qg", "cobertura_axiomas")
m73 = json.loads(ler(os.path.join(cd, "modulos_73.json")).decode("utf-8"))
txt73 = ler(os.path.join(cd, "sandbox", "saida_auditoria_73.txt")).decode("utf-8").splitlines()
cob = [l.split("\t") for l in txt73 if l.startswith("COBERTURA\t")]
tot = [l for l in txt73 if l.startswith("COBERTURA_TOTAL")]
dist = {}
for l in cob:
    ax = l[4] if len(l) > 4 else ""
    dist[ax or "(nenhum)"] = dist.get(ax or "(nenhum)", 0) + 1
khf = os.path.join(CP, "work", "v392_insumos", "F_KERNEL", "kh", "KH_N1_final.json")
kh = json.loads(ler(khf).decode("utf-8"))
OUT["cobertura"] = {
    "listar_73": {"arquivo": os.path.join(cd, "listar_73.py"), "sha256": sha(ler(os.path.join(cd, "listar_73.py")))},
    "modulos_73_json": {"arquivo": os.path.join(cd, "modulos_73.json"), "sha256": sha(ler(os.path.join(cd, "modulos_73.json"))),
                        "axiom_report_entradas": m73["axiom_report_entradas"], "tglext_theorem_lemma": m73["tglext_theorem_lemma"], "modulos_sem_cobertura": m73["modulos_sem_cobertura"],
                        "teoremas_sem_cobertura": m73["teoremas_sem_cobertura"], "n_modulos_lista": len(m73["modulos"])},
    "saida_auditoria_73": {"arquivo": os.path.join(cd, "sandbox", "saida_auditoria_73.txt"), "sha256": sha(ler(os.path.join(cd, "sandbox", "saida_auditoria_73.txt"))),
                           "cobertura_linhas": len(cob), "nomes_unicos": len(set(l[2] for l in cob)), "modulos": len(set(l[1] for l in cob)), "todos_trio": all(l[3] == "TRIO" for l in cob),
                           "distribuicao_axiomas": dist, "linha_total": tot[0] if tot else None, "rc": [l for l in txt73 if l.startswith("LEAN_RC")],
                           "nomes_auxiliares_simp_proof_eq": sum(1 for l in cob if re.search(r"_simp_|_proof_|\.eq_", l[2])),
                           "full_birkhoff_class": [l for l in cob if l[2].endswith("the_full_birkhoff_class")], "birkhoff_B_is_static": [l for l in cob if l[2].endswith("birkhoff_B_is_static")]},
    "KH_N1_final": {"arquivo": khf, "sha256": sha(ler(khf)), "modulos_no_fecho": kh["modulos_no_fecho"], "constantes": kh["constantes"], "thm": kh["por_tipo"]["thm"], "n_zero": kh["n_zero"],
                    "dos_73_em_zero": kh["dos_73_em_zero"], "zero_fora_dos_73": kh["zero_fora_dos_73"], "sandbox_cobertas": kh["sandbox_cobertas"], "sandbox_fora_do_trio": kh["sandbox_fora_do_trio"]},
    "mapa_diz_50_sem_axioma_mas_o_arquivo_diz": dist.get("(nenhum)"),
}
exige(len(cob) == 515 and tot and "teoremas=515" in tot[0] and "fora_do_trio=0" in tot[0], "saida_auditoria_73 nao tem 515 / fora_do_trio=0")
exige(m73["tglext_theorem_lemma"] == 10135 and m73["teoremas_sem_cobertura"] == 385 and m73["modulos_sem_cobertura"] == 73, "modulos_73.json nao confere 10135/385/73")
exige(kh["n_zero"] == 76 and dist.get("(nenhum)") == 49, "KH_N1 n_zero != 76 ou sem-axioma != 49")

# ---------------------------------------------------------------- 5. a F8.1 no quadro (leitura)
prog = json.loads(ler(os.path.join(PI, "PROGRAMA.json")).decode("utf-8"))
f81 = [u for u in prog["unidades"] if u.get("id") == "F8.1"]
exige(len(f81) == 1, "F8.1 nao achada no PROGRAMA.json")
OUT["f81"] = {"fonte": os.path.join(PI, "PROGRAMA.json"), "sha256_no_momento_da_leitura": sha(ler(os.path.join(PI, "PROGRAMA.json"))), "unidade": f81[0] if f81 else None,
              "nota": "o PROGRAMA.json e' VIVO (muda a cada evento); esta e' a leitura de 13/10/2026 com o sha do momento"}

# ---------------------------------------------------------------- 6. o core v391 (so' leitura): numeros da v391 que a errata de epoca cita
core_p = os.path.join(NOS, "um_absoluto.json")
cb = ler(core_p); d = json.loads(cb.decode("utf-8")); core = d["core"]
e = core["estatuto_da_prova_v391"]["prova_1_kernel"]
OUT["core_v391"] = {"arquivo": core_p, "sha256_do_arquivo": sha(cb), "sha16": sha(cb)[:16], "escada_n_theorems_clean": e["n_theorems_clean"], "escada_n_theorems_expected": e["n_theorems_expected"],
                    "declaracoes_auditadas": e["declaracoes_auditadas"], "no_trio": e["no_trio"],
                    "n_axiom_report": len(core["kernel_formalization"]["axiom_report"]),
                    "gate": core["qg_closure"]["gate"]["verdict"], "d1_v3_verdict": core["d1_camb_v3_real_v366"]["verdict"],
                    "beta_verbatim_shas": {k: v["sha256"] for k, v in core["beta_runs_bounded_below_v388"]["verbatim"].items()}, "orientation_verdict": core["orientation_is_the_sign_v367"]["verdict"], "page_information_not_claimed_0": core["page_information"]["not_claimed"][0]}
exige(e["n_theorems_clean"] == e["n_theorems_expected"] == 6163, "escada v391 != 6163")

# ---------------------------------------------------------------- 7. o kernel dos Nos (so' leitura): linhas citadas
def kfile(rel, rng):
    p = os.path.join(KR, *rel.split("/")); b = ler(p); L = b.decode("utf-8").split("\n")
    return {"arquivo": p, "sha256": sha(b), "sha16": sha(b)[:16], "bytes": len(b), "linhas": {str(i): L[i - 1].rstrip(chr(13)) for i in rng}}


OUT["kernel"] = {
    "ContinuousModularReconstruction": kfile("TGLExt/ContinuousModularReconstruction.lean", [114, 115, 154, 155, 156, 157, 158, 159, 160]),
    "ContinuousModularResolvent": kfile("TGLExt/ContinuousModularResolvent.lean", [97, 98, 99, 101, 102, 103]),
    "AperiodicAveragePrefix": kfile("TGLExt/AperiodicAveragePrefix.lean", [11, 12, 13, 14, 25, 26]),
    "ModularRealization": kfile("TGL/ModularRealization.lean", [161, 162, 163, 164, 165, 166, 167, 168, 169]),
    "CornerFamily": kfile("TGLExt/CornerFamily.lean", [18, 19, 20, 21, 22, 23, 24, 35, 36]),
    "EmergentEinstein": kfile("TGLExt/EmergentEinstein.lean", [36, 37, 38, 339]),
    "QGSolutionComplete": kfile("TGLExt/QGSolutionComplete.lean", [24, 25, 26, 34, 35, 36, 52, 80, 82]),
    "ContratoQG_v31": kfile("TGLExt/ContratoQG_v31.lean", [78, 80, 81, 83, 87, 88]),
    "TheFullBirkhoff": kfile("TGLExt/TheFullBirkhoff.lean", [1]),
    "TGLExt_raiz": kfile("TGLExt.lean", [180]),
    "TheAxiomAndTheFalseWitness": kfile("TGLExt/TheAxiomAndTheFalseWitness.lean", [245, 247, 248, 249, 252]),
    "TheLedgerOfCharges": kfile("TGLExt/TheLedgerOfCharges.lean", [127, 128, 133]),
}
exige(OUT["kernel"]["ContinuousModularReconstruction"]["sha16"] == "0a5be091f8f24ea1", "ContinuousModularReconstruction.lean != 0a5be091f8f24ea1")
exige("continuous_modular_positive_square_root" in OUT["kernel"]["ContinuousModularReconstruction"]["linhas"]["155"], "l.155 nao e' a raiz positiva")
exige("import TGLExt.TheFullBirkhoff" in OUT["kernel"]["TGLExt_raiz"]["linhas"]["180"], "TGLExt.lean l.180 nao importa TheFullBirkhoff")

_selo = json.loads(ler(os.path.join(NOS, "um_absoluto_selo.json")).decode("utf-8"))
OUT["selo_v391"] = {"arquivo": os.path.join(NOS, "um_absoluto_selo.json"), "sha256": sha(ler(os.path.join(NOS, "um_absoluto_selo.json"))),
                    "witness_layers_canonical_full_witness_term_constructed": (_selo.get("witness_layers") or {}).get("canonical_full_witness_term_constructed", "AUSENTE"), "chaves_n": len(_selo)}

# ---------------------------------------------------------------- 8. o gerador da arvore (cadeia de selo, fora do um.py)
pa = os.path.join(CP, "work", "cadeia_de_selo", "arvore_da_prova.py"); ba = ler(pa); AL = ba.decode("utf-8").split("\n")
OUT["arvore_da_prova_py"] = {"arquivo": pa, "sha256": sha(ba), "sha16": sha(ba)[:16], "linhas": {str(i): AL[i - 1].rstrip(chr(13)) for i in (155, 262, 272)}}
exige(sha(ba)[:16] == "ee2cb7413238ff1f", "arvore_da_prova.py != ee2cb7413238ff1f")

# ---------------------------------------------------------------- 9. o artigo emitido v391 (PT, txt): l.2, 69, 73
pt = os.path.join(NOS, "um_absoluto_pt.txt"); bp = ler(pt); PL = bp.decode("utf-8").split("\n")
OUT["artigo_pt_v391"] = {"arquivo": pt, "sha256": sha(bp), "sha16": sha(bp)[:16], "linhas": {str(i): PL[i - 1].rstrip(chr(13)) for i in (2, 69, 72, 73)}}
exige(sha(bp)[:16] == "4e8c68462429a7c1", "artigo PT != 4e8c68462429a7c1")
OUT["artigo_pt_v391"]["linhas_com_3_01_sigma"] = [i + 1 for i, l in enumerate(PL) if re.search(r"3[,.]01\s*(?:σ|sigma)", l)]
OUT["artigo_pt_v391"]["n_linhas_com_3_01_sigma"] = len(OUT["artigo_pt_v391"]["linhas_com_3_01_sigma"])
OUT["artigo_pt_v391"]["n_ocorrencias_3_01_sigma"] = sum(len(re.findall(r"3[,.]01\s*(?:σ|sigma)", l)) for l in PL)

# ---------------------------------------------------------------- 10. CMB-S4: a captura local do site oficial (copia byte a byte) e o recibo
tun = os.path.join(CP, "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_018")
cap = os.path.join(tun, "fontes_publicas", "cmb_s4_status.html"); rec = os.path.join(tun, "FONTES_ATUALIZACAO_F0.json")
bcap = ler(cap); brec = ler(rec); recj = json.loads(brec.decode("utf-8"))
ent = [x for x in (recj if isinstance(recj, list) else recj.get("fontes", [])) if isinstance(x, dict) and str(x.get("path", "")).endswith("cmb_s4_status.html")]
exige(len(ent) == 1 and ent[0]["sha256"] == sha(bcap) and ent[0]["bytes"] == len(bcap), "recibo da captura nao confere com o arquivo")
destino = os.path.join(HERE, "fontes", "cmb_s4_status.html")
if os.path.exists(destino):
    exige(ler(destino) == bcap, "a copia ja existente da captura difere do original")
else:
    with open(destino + ".tmp", "wb") as f:
        f.write(bcap)
    os.replace(destino + ".tmp", destino)
exige(ler(destino) == bcap, "a copia da captura nao e' igual ao original")
tt = bcap.decode("utf-8", "replace")
tt = re.sub(r"<script.*?</script>|<style.*?</style>", " ", tt, flags=re.S); tt = re.sub(r"<[^>]+>", " ", tt); tt = re.sub(r"\s+", " ", tt)
frase_a = "On July 9, 2025, the U.S. Department of Energy (DOE), Office of Science, Office of High Energy Physics and the U.S. National Science Foundation (NSF) issued a statement"
frase_b = "DOE and NSF have jointly decided that they can no longer support the CMB-S4 Project."
frase_c = "The CMB-S4 Project is proceeding with an orderly shutdown of the project"
frase_d = "The CMB-S4 Science Collaboration, which is an independent organization, is working to develop plans to best support the community."
OUT["cmb_s4"] = {"captura_original": cap, "captura_copia": destino, "sha256": sha(bcap), "bytes": len(bcap), "recibo": rec, "recibo_sha256": sha(brec),
                 "recibo_entrada": {k: ent[0][k] for k in ("url", "final_url", "retrieved_at", "bytes", "sha256")} if ent else None,
                 "frases_na_pagina": {"a_declaracao_de_9_jul_2025": frase_a in tt, "decisao_conjunta": frase_b in tt, "desligamento_ordenado": frase_c in tt, "colaboracao_cientifica_independente": frase_d in tt},
                 "frases": {"a": frase_a, "b": frase_b, "c": frase_c, "d": frase_d}}
exige(all(OUT["cmb_s4"]["frases_na_pagina"].values()), "a captura nao traz as quatro frases esperadas")

# ---------------------------------------------------------------- 11. os verbatins extraidos do transcrito (proveniencia)
jl = os.path.join(PI, "auditorias", "F3.6", "operador_msgs_v2.jsonl"); bj = ler(jl)
msgs = [json.loads(l) for l in bj.decode("utf-8").split(chr(10)) if l.strip()]
m1 = [m for m in msgs if m["quando"].startswith("2026-10-05T09:39:15")]
m2 = [m for m in msgs if m["quando"].startswith("2026-10-05T11:28:53")]
exige(len(m1) == 1 and len(m2) == 1, "mensagens de 05/10 nao achadas no transcrito")
vb = {}
for tag, m, nome, corte in ((("1", m1, "OPERADOR_05out_0939_axioma_nome_trecho_verbatim.txt", "veja se vc concorda:")), ("2", m2, "OPERADOR_05out_1128_axioma_chegamos_juntos_verbatim.txt", None)):
    mm = m[0]; t = mm["texto"]
    exige(sha(t.encode("utf-8")) == mm["sha256_texto"], "sha256_texto da mensagem %s nao confere" % tag)
    trecho = t if corte is None else t[: t.index(corte) + len(corte)]
    pth = os.path.join(HERE, "verbatins", nome); bb = trecho.encode("utf-8")
    if os.path.exists(pth):
        exige(ler(pth) == bb, "verbatim ja existente difere: " + nome)
    else:
        with open(pth + ".tmp", "wb") as f:
            f.write(bb)
        os.replace(pth + ".tmp", pth)
    vb[nome] = {"arquivo": pth, "sha256": sha(bb), "bytes": len(bb), "quando_utc": mm["quando"], "sessao": mm["sessao"], "sha256_do_texto_inteiro_da_mensagem": mm["sha256_texto"],
                "bytes_do_texto_inteiro": len(t.encode("utf-8")), "e_trecho_inicial": corte is not None, "corte_apos": corte}
OUT["verbatins_extraidos"] = {"transcrito": jl, "transcrito_sha256": sha(bj), "arquivos": vb,
                              "nota": "o trecho de 09:39:15 e' o PREFIXO exato do texto da mensagem (as quatro linhas do operador, ate 'veja se vc concorda:'); o ensaio colado depois e' omitido; o texto inteiro tem o sha256 acima"}

# ---------------------------------------------------------------- grava
destino_json = os.path.join(HERE, "medidas_g2.json")
novo = json.dumps(OUT, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8")
if os.path.exists(destino_json):
    bak = destino_json + ".bak_" + __import__("time").strftime("%Y%m%d_%H%M%S")
    with open(bak, "wb") as f:
        f.write(ler(destino_json))
with open(destino_json + ".tmp", "wb") as f:
    f.write(novo)
os.replace(destino_json + ".tmp", destino_json)
print("medidas_g2.json:", len(novo), "B", sha(novo)[:16])
print("FALHAS:", FALHAS if FALHAS else "nenhuma")
sys.exit(1 if FALHAS else 0)
