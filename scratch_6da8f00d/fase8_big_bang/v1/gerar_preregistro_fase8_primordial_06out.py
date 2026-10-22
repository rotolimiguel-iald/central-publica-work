# -*- coding: utf-8 -*-
"""Gerador UNICO do V1 da Fase 8 — beta na era da radiacao / o «Big Bang» (06/10/2026, gerencia, sessao 946c4deb).

Le do disco por script: o rascunho de 05/10 (base, por sha256), a critica (C1-C12, F1-F9), o canal N_eff da Bancada
(bancada/neff_canal.py, rodado AGORA: as duas convencoes D9 e o controle anti-dupla-contagem D3), beta = alfa(um.py)*sqrt(e) em
runtime. Aplica D1-D11 pelo PADRAO da gerencia (delegacao do operador de 05/10), fixa UMA funcao de veredito como texto-fonte com
sha256, testa os ramos so com casos SINTETICOS, e grava JSON (autoridade) + MD + V1_FASE8_HASHES.json. Nenhum veredito de natureza:
o poder de hoje e < 5 em todo observavel primordial (NOT_FALSIFIED_UNDERPOWERED predeterminado pelo poder) e as medidas seguem
[DECLARADO] ate as fontes por sha256 (D8). NOT_FALSIFIED nunca e a palavra proibida; a RG/LCDM e o limite classico.
"""
import os, re, sys, json, math, hashlib, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = sys.argv[1] if len(sys.argv) > 1 else HERE
F8 = os.path.dirname(HERE)
sys.path.insert(0, r"C:\IALD\Bancada_Um")
from bancada import neff_canal as NC  # noqa: E402

NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
SELO = os.path.join(NOS, "um_absoluto_selo.json")
CANAL_PY = r"C:\IALD\Bancada_Um\bancada\neff_canal.py"
MCP_PY = r"C:\IALD\Bancada_Um\mcp_um.py"
EVID = {
    "PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1_RASCUNHO.json": os.path.join(F8, "pre_registro", "PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1_RASCUNHO.json"),
    "PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1_RASCUNHO.md": os.path.join(F8, "pre_registro", "PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1_RASCUNHO.md"),
    "PODER_FASE8_UNIVERSO_PRIMORDIAL.json": os.path.join(F8, "pre_registro", "PODER_FASE8_UNIVERSO_PRIMORDIAL.json"),
    "VERBATIM_OPERADOR_05out_big_bang.txt": os.path.join(F8, "pre_registro", "VERBATIM_OPERADOR_05out_big_bang.txt"),
    "CRITICA_FASE8.md": os.path.join(F8, "critico", "CRITICA_FASE8.md"),
    "fase8_fisica_resultado.json": os.path.join(F8, "fisica", "fase8_fisica_resultado.json"),
    "REGISTRO_DA_CASA_BIG_BANG.md": os.path.join(F8, "registro_da_casa", "REGISTRO_DA_CASA_BIG_BANG.md"),
    "neff_canal.py": CANAL_PY,
}
ID = "PREREG_FASE8_UNIVERSO_PRIMORDIAL_20261006_V1"
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED|\bconfirmada\b|\bresolvida\b")
LIDOS = {}


def fsha(p):
    h = hashlib.sha256(open(p, "rb").read()).hexdigest(); LIDOS[p] = h; return h


def canon(o):
    return json.dumps(o, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


for p in list(EVID.values()) + [SELO, MCP_PY]:
    fsha(p)
rasc = json.load(open(EVID["PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1_RASCUNHO.json"], encoding="utf-8"))["spec"]
selo = json.load(open(SELO, encoding="utf-8"))

# ---------------------------------------------------------------------------------------------------------------------
# 0. O canal da Bancada, rodado agora (D4: a Bancada primeiro), e o controle D3
# ---------------------------------------------------------------------------------------------------------------------
canal = NC.canal(sigmas_extra=(0.0239,))
ctrl = NC.controle_anti_dupla_contagem()
assert ctrl["passou"], ctrl
BETA = canal["beta_runtime"]; LIDOS[NC.UM] = canal["um_py_sha256"]; LIDOS[NC.FROZEN] = canal["fonte_sha256"]
DELTA_RAD = 4.0 * BETA / 3.0
S_BBN = math.sqrt(1.0 + DELTA_RAD)                       # speed-up exato, constante em H(T) (C3)
DN_BBN = DELTA_RAD * 10.75 / 1.75                        # DeltaN-equivalente antes da aniquilacao e+- (g* = 10,75)
DN_CMB = canal["delta_N_eff"]                            # depois da aniquilacao (CMB e o gargalo do D)
indep = [m for m in canal["medidas"] if m["independente"]]
poder_hoje = {m["rotulo"]: round(m["separacao_TGL_SM_sigma"], 4) for m in canal["medidas"]}
poder_futuro = {p["rotulo"]: round(p["separacao_TGL_SM_sigma"], 4) for p in canal["projecoes"]}

# ---------------------------------------------------------------------------------------------------------------------
# 1. A FUNCAO DE VEREDITO UNICA (texto-fonte, hasheado)
# ---------------------------------------------------------------------------------------------------------------------
FUNCAO_FONTE = '''def veredito_fase8_v1(r):
    """Funcao UNICA de veredito da Fase 8 (V1, 06/10/2026), por MAPA (A = N_eff publicado, TGL-S; A_N2 = Nivel 2 S; C = BBN).
    Entrada r: mapa, n_alvos_sem_hash, dispersao_por_gl, p_dispersao, z_indep (lista dos z = (X_obs - X_TGL)/sigma das analises
    INDEPENDENTES de experimento), poder (Delta/sigma da melhor analise independente), fechamento ('S' ou 'L').
    Ordem (a primeira que casa decide):
    0 AWAITING_SOURCE: mapa C sem a parametrizacao/abundancia lida da fonte (r["awaiting_source"]);
    1 INCONCLUSIVE_SYSTEMATICS: alvo decisorio sem fonte por hash (n_alvos_sem_hash > 0) OU chi2_int/(n-1) > 2 OU p < 0,01;
    2 FALSIFIED_AT_5SIGMA: |z| >= 5 em DUAS analises independentes (regra do frozen 96b51333) — falsifica o PAR (mapa x observavel),
      nao beta, nao a teoria;
    3 TENSION_3_TO_5_SIGMA: alguma analise independente com |z| >= 3;
    4 NOT_FALSIFIED_UNDERPOWERED: poder < 5 (sufixo POWER_<x>_OF_5_SIGMA); sob fechamento L o mapa A e CEGO (sufixo BLIND_UNDER_TGL_L);
    5 NOT_FALSIFIED_POWERED (senao).
    Sufixo sempre: __MAP_<mapa>__NOT_BLIND_TO_PUBLISHED_DATA_STATED__NOT_A_CONFIRMATION__GATE_UNTOUCHED."""
    def f(x):
        return ("M" if x < 0 else "P") + ("%.2f" % abs(x)).replace(".", "P")
    base = "TGL_FASE8_UNIVERSO_PRIMORDIAL_V1__"
    suf = "__MAP_%s__NOT_BLIND_TO_PUBLISHED_DATA_STATED__NOT_A_CONFIRMATION__GATE_UNTOUCHED" % r["mapa"]
    if r.get("awaiting_source"):
        return base + "AWAITING_SOURCE" + suf
    if r["n_alvos_sem_hash"] > 0 or (len(r["z_indep"]) > 1 and (r["dispersao_por_gl"] > 2.0 or r["p_dispersao"] < 0.01)):
        return base + "INCONCLUSIVE_SYSTEMATICS" + suf
    if sum(1 for z in r["z_indep"] if abs(z) >= 5) >= 2:
        return base + "FALSIFIED_AT_5SIGMA" + suf
    if any(abs(z) >= 3 for z in r["z_indep"]):
        return base + "TENSION_3_TO_5_SIGMA" + suf
    if r["poder"] < 5:
        t = base + "NOT_FALSIFIED_UNDERPOWERED__POWER_%s_OF_5_SIGMA" % f(r["poder"])
        if r.get("fechamento") == "L":
            t += "__BLIND_UNDER_TGL_L"
        return t + suf
    return base + "NOT_FALSIFIED_POWERED" + suf
'''
FUNCAO_SHA = hashlib.sha256(FUNCAO_FONTE.encode("utf-8")).hexdigest()
ns = {}; exec(FUNCAO_FONTE, ns); vf = ns["veredito_fase8_v1"]
b = {"mapa": "A", "n_alvos_sem_hash": 0, "dispersao_por_gl": 1.0, "p_dispersao": 0.5, "z_indep": [0.5, -1.0], "poder": 6.0, "fechamento": "S"}
casos = {"awaiting": {"mapa": "C", "awaiting_source": True}, "inconclusive": {"n_alvos_sem_hash": 3}, "falsified": {"z_indep": [5.2, -5.6]},
         "um_so_a_5": {"z_indep": [5.2, 0.1]}, "tension": {"z_indep": [3.1, 0.2]}, "underpowered": {"poder": 0.99}, "cego_L": {"poder": 0.05, "fechamento": "L"},
         "powered": {}}
testes = {}
for k, m in casos.items():
    r = dict(b); r.update(m); o = vf(r); assert not GUARDA.search(o), o; testes[k] = o
assert "TENSION" in testes["um_so_a_5"]  # uma analise a 5 sigma sozinha nao falsifica (regra das duas)
assert all(any(s in t for t in testes.values()) for s in ("AWAITING_SOURCE", "INCONCLUSIVE", "FALSIFIED_AT_5SIGMA", "TENSION", "UNDERPOWERED", "BLIND_UNDER_TGL_L", "NOT_FALSIFIED_POWERED"))
# predeterminado (SO pelo poder; nenhum centro entra): hoje, as medidas [DECLARADO] => regra 1; com D8 cumprido, o teto pelo poder e UNDERPOWERED
melhor = max(m["separacao_TGL_SM_sigma"] for m in indep)
pre_hoje = vf(dict(b, n_alvos_sem_hash=len(indep), poder=melhor, z_indep=[]))
pre_com_D8 = vf(dict(b, poder=melhor, z_indep=[]))

SPEC = {
    "id": ID,
    "estado": "V1 CONGELADO POR HASH — nenhum veredito de natureza emitido; AWAITING_DATA (D8: fontes por sha256 = ato do operador; abrir = palavra do operador)",
    "pergunta_do_operador_verbatim": rasc["pergunta_do_operador_verbatim"],
    "base": {"um_py_sha16": canal["um_py_sha256"][:16], "selo_sha16": LIDOS[SELO][:16], "gate": selo.get("qg_closure_verdict"),
             "rascunho_05out_spec_sha256": json.load(open(EVID["PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1_RASCUNHO.json"], encoding="utf-8"))["spec_sha256"]},
    "beta": {"regra": "ALPHA_FINE_CODATA_2018 x sqrt(e) em runtime; nunca literal; nunca prior", "beta_runtime": BETA, "alpha_lido_do_um_py": canal["alpha_lido_do_um_py"]},
    "lei": {"identidade": "rho_TGL = beta(rho+p) = beta[(4/3)rho_r + rho_m] => H^2 = (1+4beta/3)rho_r + (1+beta)rho_m + rho_Lambda (pedra 105 RhoPlusPClosure.hubble_form)",
            "delta_por_era": {"radiacao_w_1_3": DELTA_RAD, "materia_w_0": BETA, "atrator_w_m1": 0.0},
            "leitura": "a lei da o MAXIMO na radiacao (4beta/3) e zero no atrator — conjuncao, nao deducao, com o [ONTO] «Big Bang = inscricao originaria» (D10)"},
    "decisoes_padrao_da_gerencia": {
        "fonte_da_delegacao": "operador 05/10: «o resto vc consegue responder tudo agroa»; «prossiga» (memorias proximo-passo-06out, handoff-sessao-nova-06out)",
        "D1": "a radiacao paga 4beta/3 (identidade rho+p); a opcao «so-materia» NAO tem registro na casa: fica como contrafactual dito (mapa B, ~5e-9), sem estimador (C9)",
        "D2": "TGL-S (free-streaming) primario; TGL-L co-rodado e DITO cego: sigma(beta)_L = 0,244 => poder ~0,05 (F4); nao se decide por dado",
        "D3": "UMA entrada de beta por instrumento: Bancada = Phi_total.(rho+p) com N_eff FIXO; CAMB/Nivel 2 = nnu = N + (4/3)(1+F.N)/F.beta e omega_c,eff, sem Phi_total; proibido somar (C10/F1). Controle medido: secao controle_D3",
        "D4": "Bancada antes do um.py (ordem verbatim de 30/09, C11/F9): o canal N_eff foi ligado na Bancada (bancada/neff_canal.py + ferramenta MCP neff_canal) ANTES deste V1",
        "D5": "BBN: tabelas PRIMAT/PArthENoPE do camb como BRACKET DeltaN em [%.4f; %.4f] (aproximacao dita: nenhum DeltaN unico representa a vestimenta, C3); o exato e S(T) = sqrt(1+4beta/3) = %.6f constante num codigo de BBN = ato do operador, antes de qualquer cobranca no livro" % (DN_BBN, DN_CMB, S_BBN),
        "D6": "omega_b do CMB, nunca do D/H (o Cooke+2018 e inferido sob S = 1: circular no observavel, F2); o prior OMB_BBN(S=1) do Nivel 2 e inconsistente em ~Dln eta = -0,8 %% (~0,3 sigma do prior): DITO",
        "D7": "sinal fixado antes do dado: DeltaN_eff > 0; os centros atuais estao ABAIXO do padrao — a TGL fica mais longe que o SM e nada se inverte",
        "D8": "fontes por sha256 (1807.06209, 2503.14454, 2506.20707, Cooke+2018, Steigman 2007, Cyburt+2016, Aver) = ato do operador (rede); ate la tudo [DECLARADO]",
        "D9": "duas convencoes de citacao SEMPRE lado a lado: separacao TGL-SM em sigma (poder) e tensao de cada modelo contra o centro medido (o canal as devolve)",
        "D10": "o PROVADO e a face de kernel sobre o FLUXO (beta > 0 => sem testemunha estatica plena; zero inatingivel em tempo finito); «Big Bang = inscricao originaria» segue [ONTO]",
        "D11": "Nivel 2 canonico = o frozen original (teste_acustico_beta_tgl_v1, 13_nivel2_chains.h5 af118c94a693ac3c, CHAIN_OF_CUSTODY 13/13); a copia do Nos (7e5ad3e2681ee3c8) = continuacao (F5)",
    },
    "mapas": {
        "A": {"nome": "N_eff publicado (TGL-S)", "decisorio": True, "previsao": {"N_base_SM": canal["N_base"], "dN_eff_dbeta": canal["dN_eff_dbeta"], "delta_N_eff": DN_CMB, "N_eff_TGL": canal["N_eff_TGL"]},
              "regra": "FALSIFIED so com |z| >= 5 em DUAS analises independentes (frozen 96b51333)"},
        "A_N2": {"nome": "Nivel 2 S (CAMB + plik_lite + low-ell + DESI)", "decisorio": False, "estado": "N2_INCAPAZ: sigma(beta) = 0,01765 ~ 1,5 beta (medido em agosto); diagnostico"},
        "B": {"nome": "so-materia (contrafactual sem registro)", "decisorio": False, "estado": "sem previsao na radiacao (~5e-9); convencao de z(T) dita (C7)"},
        "C": {"nome": "BBN (Y_p, D/H) pelo speed-up S", "decisorio": True, "S_exato": S_BBN, "bracket_DeltaN": [DN_BBN, DN_CMB],
              "estado": "AWAITING_SOURCE: Y_p (0,2449 Aver+2015 x 0,2453 Aver+2021, C1) e d ln(D/H)/d ln H (0,57 [INPUT sem fonte legivel] x 1,57 Steigman x ~1,6-1,9 Cyburt, C2) a LER da fonte antes de qualquer numero"},
    },
    "canal_bancada": {"modulo": CANAL_PY, "modulo_sha256": LIDOS[CANAL_PY], "mcp_um_sha256": LIDOS[MCP_PY], "fonte_congelada": canal["fonte_congelada"], "fonte_sha256": canal["fonte_sha256"],
                      "medidas_duas_convencoes": canal["medidas"], "nota": "as tensoes contra o centro sao do dado publicado ja lido pela casa (agosto, 05/10): NAO-CEGO, dito; nao sao veredito"},
    "controle_D3": ctrl,
    "poder": {"hoje_por_medida_sigma_so": poder_hoje, "melhor_independente": melhor, "futuro_por_sigma": poder_futuro, "sigma_N_eff_para_5sigma": canal["sigma_para_5sigma_de_separacao"],
              "TGL_L": "sigma(beta)_L = 0,244 => poder ~0,05 (cego)", "BBN_D_H": "sistematica teorica ~1,6 % no D/H: nunca chega a 5 sigma (dito)"},
    "futuro_declarado": {"CMB_S4": "a entrega do Codex na ORDEM 018 (mapa seq 402) declara a retirada DOE/NSF (09/07/2025) e o encerramento do CMB-S4 [DECLARADO — auditoria da gerencia no Passo D]; a projecao sigma = 0,03 do frozen (3,98 sigma) fica como historia, nao como calendario",
                         "Simons": "SO ampliado sigma = 0,045 => %.2f sigma de separacao (2025-2034, sem calendario ratificado) [DECLARADO]" % (DN_CMB / 0.045),
                         "frase_correta": "5 sigma pedem sigma(N_eff) <= %.4f; nenhum instrumento documentado em disco chega la" % canal["sigma_para_5sigma_de_separacao"]},
    "funcao_de_veredito": {"nome": "veredito_fase8_v1", "fonte": FUNCAO_FONTE, "sha256": FUNCAO_SHA, "testes_sinteticos_de_ramo": testes,
                           "predeterminado_hoje_pelo_poder": pre_hoje, "predeterminado_com_D8_pelo_poder": pre_com_D8,
                           "regra": "o runner e o um.py executam ESTE texto (sha256 conferido); o predeterminado usa SO poder (sigma), nenhum centro"},
    "ordem_de_execucao": ["E1 Bancada: canal N_eff (feito: neff_canal, controle D3 passou)", "E2 operador: D8 (fontes por sha256) e codigo de BBN (D5b) se quiser o mapa C exato",
                          "E3 runner hasheado antes; com a palavra do operador: a funcao por mapa", "E4 o um.py (v387+) LE este V1 por hash; nao abre nada; ausente/divergente => AWAITING_PREREGISTRATION__V1_NOT_READ"],
    "nao_decide": rasc["o_que_nao_decide"] + ["o terceiro discriminante da errata de maio (fundo estocastico de GW primordiais): sem previsao quantificada na casa — [OPEN], fora da Fase 8 (F8)"],
    "pendente_da_gerencia": ["F6: #print axioms de the_zero_is_the_false_witness, hubble_form, the_background_closure antes de citar no livro (nao bloqueia este V1)", "F7: estratigrafia da cunhagem «Big Bang» (opcional, se o operador quiser)"],
    "critica_coberta": "C1-C12 e F1-F9 da CRITICA_FASE8.md (a critica nao tem F10: grep F10 = 0)",
    "tokens_provisorios": {"estado": "TGL_FASE8_UNIVERSO_PRIMORDIAL_V1__AWAITING_DATA__V1_FROZEN__NOT_BLIND_TO_PUBLISHED_DATA_STATED__GATE_UNTOUCHED", "nota": "nome final = cunhagem do operador"},
}
SPEC["fontes_lidas_sha256"] = {p: h for p, h in sorted(LIDOS.items())}
assert not GUARDA.search(SPEC["tokens_provisorios"]["estado"])
SPEC_SHA = hashlib.sha256(canon(SPEC).encode("utf-8")).hexdigest()


def gravar(p, bts):
    open(p + ".tmp", "wb").write(bts); assert os.path.getsize(p + ".tmp") == len(bts); os.replace(p + ".tmp", p)


os.makedirs(os.path.join(OUT_DIR, "evidencias"), exist_ok=True)
carimbo = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
gravar(os.path.join(OUT_DIR, "PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1.json"), json.dumps(
    {"id": ID, "spec_sha256": SPEC_SHA, "spec_sha256_formula": 'sha256(json.dumps(spec, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))',
     "gerado_utc": carimbo, "spec": SPEC}, ensure_ascii=False, indent=1).encode("utf-8"))
md = ["# Pré-registro V1 — Fase 8: β na era da radiação (congelado por hash, 06/10/2026)\n",
      "**spec_sha256** `%s` · **função de veredito** `%s` · gerado %s\n" % (SPEC_SHA, FUNCAO_SHA, carimbo),
      "> «%s» — o operador, 05/10/2026\n" % SPEC["pergunta_do_operador_verbatim"],
      "Estado: **AWAITING_DATA**; nenhum veredito de natureza. Pelo poder (só σ): hoje `%s`; com as fontes por hash (D8) o teto é `%s`.\n" % (pre_hoje, pre_com_D8),
      "## A lei\nH² = (1+4β/3)ρ_r + (1+β)ρ_m + ρ_Λ; β = α·√e em runtime (%.15f); δ_rad = 4β/3 = %.6f; ΔN_eff = %.6f (CMB), %.4f (BBN, g* = 10,75); S = %.6f.\n" % (BETA, DELTA_RAD, DN_CMB, DN_BBN, S_BBN),
      "## Canal N_eff da Bancada (D4) e controle D3\nMódulo `bancada/neff_canal.py` `%s`; fonte congelada `%s`. Controle: E_TGL/E_ΛCDM(nnu desl.) − 1 = %s em z = %s (tol 1e-4) → **%s**.\n" % (
          LIDOS[CANAL_PY][:16], canal["fonte_sha256"][:16], ", ".join("%.2e" % d for d in ctrl["razao_E_menos_1"]), ctrl["z"], "passou" if ctrl["passou"] else "FALHOU"),
      "| medida | N_eff | σ | separação TGL–SM | tensão TGL | tensão SM |\n|---|---|---|---|---|---|\n" + "\n".join(
          "| %s (%s) | %.2f | %.2f | %.2fσ | %.2fσ | %.2fσ |" % (m["rotulo"], m["fonte"], m["N_eff_obs"], m["sigma"], m["separacao_TGL_SM_sigma"], m["tensao_TGL_contra_centro_sigma"], m["tensao_SM_contra_centro_sigma"]) for m in canal["medidas"]) + "\n",
      "## Futuro (declarado)\n" + "\n".join("- %s: %s" % kv for kv in SPEC["futuro_declarado"].items()) + "\n",
      "## Decisões (padrão da gerência por delegação)\n" + "\n".join("- **%s** %s" % kv for kv in SPEC["decisoes_padrao_da_gerencia"].items()) + "\n",
      "## Mapas\n" + "\n".join("- **%s** %s — %s" % (k, v["nome"], v.get("estado", v.get("regra", ""))) for k, v in SPEC["mapas"].items()) + "\n",
      "## Função de veredito única (sha256 `%s`)\n```python\n%s```\n" % (FUNCAO_SHA, FUNCAO_FONTE) + "\n".join("- %s → `%s`" % kv for kv in testes.items()) + "\n",
      "## Não decide\n" + "\n".join("- " + s for s in SPEC["nao_decide"]) + "\n",
      "## Pendente\n" + "\n".join("- " + s for s in SPEC["pendente_da_gerencia"]) + "\n",
      "## Fontes lidas (sha256)\n" + "\n".join("- `%s` %s" % (h[:16], p) for p, h in SPEC["fontes_lidas_sha256"].items()) + "\n",
      "\nNOT_FALSIFIED nunca é a palavra proibida; a RG/ΛCDM é o limite clássico; nada aqui move β nem o gate.\n"]
gravar(os.path.join(OUT_DIR, "PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1.md"), "\n".join(md).encode("utf-8"))
for nome, p in EVID.items():
    gravar(os.path.join(OUT_DIR, "evidencias", nome), open(p, "rb").read())
me = os.path.abspath(__file__)
if os.path.dirname(me) != os.path.abspath(OUT_DIR):
    gravar(os.path.join(OUT_DIR, os.path.basename(me)), open(me, "rb").read())
H = {"id": ID, "spec_sha256": SPEC_SHA, "funcao_sha256": FUNCAO_SHA, "gerado_utc_do_V1": carimbo, "pasta": os.path.abspath(OUT_DIR), "arquivos": {}}
for raiz, _, fs in os.walk(OUT_DIR):
    for f in sorted(fs):
        p = os.path.join(raiz, f)
        if f == "V1_FASE8_HASHES.json" or f.endswith(".tmp") or "__pycache__" in p: continue
        H["arquivos"][os.path.relpath(p, OUT_DIR).replace("\\", "/")] = {"sha256": hashlib.sha256(open(p, "rb").read()).hexdigest(), "bytes": os.path.getsize(p)}
gravar(os.path.join(OUT_DIR, "V1_FASE8_HASHES.json"), json.dumps(H, ensure_ascii=False, indent=1).encode("utf-8"))
print("spec_sha256", SPEC_SHA); print("funcao_sha256", FUNCAO_SHA); print("hoje", pre_hoje); print("com_D8", pre_com_D8)
print("DN_BBN %.5f DN_CMB %.6f S %.6f melhor %.4f ctrl %s" % (DN_BBN, DN_CMB, S_BBN, melhor, ctrl["razao_E_menos_1"]))
for k, v in H["arquivos"].items(): print(v["sha256"][:16], v["bytes"], k)
