# -*- coding: utf-8 -*-
"""Monta ORDEM_018_INSUMOS (túnel PARA_CHATGPT): os quatro textos verbatim do operador de 05/10 (por sha256), os números da gerência lidos do core v386
(a razão de Hubble; N_eff; o livro de cobranças; o pilar), o V1 do ramo B (cópia de bytes), a lei da prova (memória), o README e o MANIFESTO_INSUMOS.json
com sha256 de tudo. Só acréscimo (a pasta nasce agora); nada confidencial; nada do Nós é escrito."""
import hashlib, json, math, os, re, shutil, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TUN = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "Chatgpt", "TUNEL", "PARA_CHATGPT")
INS = os.path.join(TUN, "ORDEM_018_INSUMOS"); os.makedirs(INS, exist_ok=True)
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
UMEM = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
B1 = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_ramo_b_05out")
agora = time.strftime("%Y-%m-%d %H:%M:%S")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def copia(src, nome=None):
    dst = os.path.join(INS, nome or os.path.basename(src)); b = open(src, "rb").read()
    if os.path.exists(dst) and open(dst, "rb").read() == b:
        return dst
    open(dst + ".tmp", "wb").write(b); assert open(dst + ".tmp", "rb").read() == b; os.replace(dst + ".tmp", dst); return dst


man = {"quando": agora, "ordem": "ORDEM_018_o_discriminante.md", "arquivos": {}, "nota": "sha256 calculado por script na montagem; o ChatGPT reconfere antes de usar"}
# 1. os verbatins do operador
for fn in ("VERBO_operador_05out.txt", "RESPOSTAS_operador_05out.txt", "TRES_TESTES_operador_05out.txt", "POS_DICAO_operador_05out.txt"):
    copia(os.path.join(HERE, fn))
copia(os.path.join(HERE, "ramo_b", "DECISAO_OPERADOR_RAMO_B_05out.json"))
# 2. a lei da prova e os três testes (memórias)
for fn in ("pos-dicao-nao-e-prova-diabolica-05out.md", "tres-testes-de-estresse-conjuntos-05out.md", "ramo-b-reaberto-05out.md", "rg-limite-classico-nao-rival.md", "as-tres-reguas-da-afirmacao.md"):
    p = os.path.join(UMEM, fn)
    if os.path.exists(p):
        copia(p, "MEMORIA_" + fn)
# 3. o V1 do ramo B (cópia de bytes)
for fn in sorted(os.listdir(B1)):
    if fn.endswith((".json", ".md", ".py")) and ".bak" not in fn:
        copia(os.path.join(B1, fn), "RAMO_B_V1__" + fn)
# 4. os números da gerência, lidos do core v386 AGORA
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
src = open(os.path.join(NOS, "um.py"), encoding="utf-8", errors="replace").read()
a = float(re.search(r"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", src, re.M).group(1)); beta = a * math.sqrt(math.e)
f4 = (core.get("bancada_fase4_v378") or {}).get("P_ladder_d1b") or {}
f5 = (core.get("bancada_fases_5_6_7_v380") or {}).get("fase5") or {}
led = core["the_ledger_of_charges_v383"]; rows = led["ledger"]
qp = core.get("quantum_pillar_v384") or {}; S = qp.get("summary") or {}
w = 1.0 / 3.0; delta = beta * abs(1 + w); fnu = 7.0 / 8.0 * (4.0 / 11.0) ** (4.0 / 3.0); Neff0 = 3.044; dNeff = delta * (1 + fnu * Neff0) / fnu
N = {"gerado": agora, "um_py_sha16": sha(os.path.join(NOS, "um.py"))[:16], "selo_timestamp": selo.get("timestamp"), "um_version": selo.get("um_version"),
     "beta_runtime": beta, "alpha_lido": a, "n_theorems_clean": (core.get("external_ladder") or {}).get("n_theorems_clean"), "gate": selo.get("qg_closure_verdict"),
     "hubble": {"fase4_P_ladder_d1b": f4, "fase5": {"veredito": f5.get("veredito"), "validacao": f5.get("validacao"), "P_sombra": f5.get("P_sombra"), "alvo_H0": f5.get("alvo_H0")},
                "razao_simples_da_gerencia": {"nota": "K = (1+z*)^(2beta/3) e' APROXIMACAO; a lei da casa usa E(z*) (Fase 4: K = 1,083807); z* = 1089,92; Planck 67,36 +- 0,54 e SH0ES 73,04 +- 1,04 sao [KNOWN] de memoria da gerencia — A LER DAS FONTES",
                                              "K_E_zstar_fase4": f4.get("K"), "H0_bg_fase4": f4.get("H0_bg"), "H0_local_previsto_fase4": f4.get("H0_local")}},
     "n_eff_era_da_radiacao": {"lei": "delta<K_d> = beta |1+w|", "w": w, "delta": delta, "fator_por_especie": fnu, "N_eff_padrao": Neff0, "delta_N_eff_se_fracao_da_radiacao_total": dNeff,
                               "planck_2018_N_eff": "2,99 +- 0,17 [KNOWN — a ler da fonte]", "sigma_planck": 0.17, "z_planck": dNeff / 0.17, "cmb_s4_sigma_previsao": 0.03, "z_cmb_s4": dNeff / 0.03,
                               "estatuto": "a lei e' REAL na forma; o MAPA (fracao da radiacao total / so-materia / speed-up) e' decisao do operador [INPUT]"},
     "livro_de_cobrancas_v383": {r.get("id"): {"side": r.get("side"), "law": r.get("law"), "outcome": r.get("outcome"), "number_read": r.get("number_read")} for r in rows},
     "pilar_quantico": {"verdict": qp.get("verdict"), "T2": S.get("T2"), "T4": S.get("T4"), "cpuref": S.get("cpuref"), "env": S.get("env")},
     "ramo_b_v386": {"verdict": (core.get("ramo_b_preregistration_v386") or {}).get("verdict")}, "the_verb_v386": {"verdict": (core.get("the_verb_v386") or {}).get("verdict")}}
p = os.path.join(INS, "NUMEROS_DA_GERENCIA_core_v386.json")
json.dump(N, open(p + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(p + ".tmp", p)
# 5. README
README = ("# ORDEM_018_INSUMOS — o que está aqui (montado por script em %s)\n\n"
          "- `VERBO_operador_05out.txt`, `RESPOSTAS_operador_05out.txt`, `TRES_TESTES_operador_05out.txt`, `POS_DICAO_operador_05out.txt`, `DECISAO_OPERADOR_RAMO_B_05out.json`: as palavras do operador de 05/10/2026, VERBATIM (extraídas do transcrito por script; cite com «…» nos cortes; [sic] fora das «»).\n"
          "- `MEMORIA_*.md`: a lei da prova (novidade de uso; «pós-dição» nunca como demérito), os três testes conjuntos, o ramo B reaberto, a RG como limite clássico, as três réguas da afirmação.\n"
          "- `RAMO_B_V1__*`: o pré-registro V1 do ramo B do ringdown, CONGELADO por hash (os originais, read-only, em `C:\\IALD\\Bancada_Um\\investigacao\\preregistro_ramo_b_05out\\`; o `um.py` v386 o lê por hash). Molde de pré-registro.\n"
          "- `NUMEROS_DA_GERENCIA_core_v386.json`: os números citados na ORDEM, lidos do core/selo v386 por script (Fase 4/5 da razão de Hubble; a conta de N_eff; o livro de cobranças; o pilar). O que está marcado [KNOWN — a ler da fonte] é valor de memória da gerência: a bancada o lê da fonte publicada por hash antes de usar.\n"
          "- `MANIFESTO_INSUMOS.json`: sha256 e bytes de cada arquivo desta pasta.\n\n"
          "Regras: β nunca literal (α_CODATA2018·√e em runtime); hash lido por script; nada do Nós se escreve; o mapa de rotas se consulta antes e se registra depois.\n" % agora)
p = os.path.join(INS, "README_INSUMOS.md"); open(p + ".tmp", "w", encoding="utf-8", newline="\n").write(README); os.replace(p + ".tmp", p)
for fn in sorted(os.listdir(INS)):
    fp = os.path.join(INS, fn)
    if os.path.isfile(fp) and fn != "MANIFESTO_INSUMOS.json":
        man["arquivos"][fn] = {"sha256": sha(fp), "bytes": os.path.getsize(fp)}
ordem = os.path.join(TUN, "ORDEM_018_o_discriminante.md"); man["ordem_sha256"] = sha(ordem); man["ordem_bytes"] = os.path.getsize(ordem)
p = os.path.join(INS, "MANIFESTO_INSUMOS.json"); json.dump(man, open(p + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(p + ".tmp", p)
print("INSUMOS:", len(man["arquivos"]), "arquivos |", "ORDEM sha16", man["ordem_sha256"][:16], man["ordem_bytes"], "B")
for k, v in man["arquivos"].items():
    print("  ", k, v["bytes"], v["sha256"][:16])
