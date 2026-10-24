# -*- coding: utf-8 -*-
"""gerar_resultado.py -- monta RESULTADO.md a partir de RESULTADO.md.tmpl, LENDO os numeros e os hashes dos recibos e dos arquivos (nada de numero nem hash de memoria).
So escreve em C:\\IALD\\Central de Patentes\\work\\v399_selo_e_testemunho (RESULTADO.md, com backup de BYTES do anterior). Uso: python -I -B -X utf8 gerar_resultado.py"""
import hashlib
import json
import os
import re
import time

W = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(W, "recibos")


def J(*p):
    return json.load(open(os.path.join(W, *p), encoding="utf-8"))


def b_(p):
    return open(os.path.join(W, p), "rb").read()


def h16(p):
    return hashlib.sha256(b_(p)).hexdigest()[:16]


def pt(x, d=2):
    return ("%.*f" % (d, x)).replace(".", ",")


def mi(n):
    return "{:,}".format(int(n)).replace(",", ".")


proto = J("recibos", "RECIBO_PROTOTIPO_um_py_v398.json")
sel = proto["selo"]["acom"]
aud = sel["auditoria_de_separacao"]
cl = proto["caminho_literal"]
tr = proto["transporte_verbatim"]
ex = {(p["centro"], p["angular_bits"]): p for p in J("recibos", "RECIBO_EXATIDAO_ALFABETO.json")["perfis"]}
ct = J("recibos", "RECIBO_CONTROLES.json")
cf = J("recibos", "RECIBO_CONFORMIDADE.json")
rp = J("recibos", "RECIBO_REPRODUTIBILIDADE.json")
sim = J("recibos", "RECIBO_SIMULACAO_COLADA.json")
col = J("recibos", "RECIBO_COLISOES_DE_NOMES.json")
ops = J("recibos", "RECIBO_TESTES_DO_OPERADOR.json")
resumo = J("recibos", "RECIBO_RESUMO.json")
axi = J("AXIOMAS.json")
cab = J("conferencia_cabecalho.json")
sbx = J("conferencia_sandbox.json")
fon = J("fontes_sha.json")
man = J("EMBUTIDO_MANIFESTO.json")
mapa = J("recibos", "mapa_consultas.json")
sc = J("recibos", "um_absoluto_selo_acom.json")
sem = ct["perfil_sem_sinal_controle_do_veredito"]
ver = sem["veredito_real_da_funcao_selar"]
sonda = cf["torch_legado"]["_sonda_de_empates_m_par_e_valor_m_sobre_2"]
objs = {o["nome"]: o for o in sc["objetos"]}
nctl = ct["objeto_inteiro_um_py"]["n_controles"]
ctl_txt = "\n".join("| %s | %s | %s |" % (r["id"], r["descricao"], r["obtido"].replace("|", "/")) for r in ct["objeto_inteiro_um_py"]["controles"])
n_objeto = proto["objeto"]["bytes"]

F = {
    "UMPY_SHA16": proto["objeto"]["sha16"], "UMPY_BYTES": mi(n_objeto),
    "PROTO_SHA16": h16("selo_acom_prototipo.py"), "PROTO_BYTES": mi(os.path.getsize(os.path.join(W, "selo_acom_prototipo.py"))), "PROTO_LINHAS": mi(b_("selo_acom_prototipo.py").count(b"\n")),
    "SECAO_SHA16": h16(os.path.join("patch_proposto", "secao_colavel_v399.py")), "SECAO_BYTES": mi(sim["secao_colavel"]["bytes"]), "SECAO_LINHAS": str(sim["secao_colavel"]["linhas"]),
    "TRECHOS_SHA16": h16(os.path.join("patch_proposto", "trechos_v399_para_o_um_py.py")), "TRECHOS_BYTES": mi(sim["trechos"]["bytes"]),
    "BLOCO_SHA16": man["bloco_embutido_completo_sha256"][:16], "BLOCO_LINHAS": "%d + %d" % (man["blocos"]["mirror"]["linhas_embutidas"], man["blocos"]["crypto"]["linhas_embutidas"]),
    "SUBST_N": str(sum(len(v["substituicoes"]) for v in man["blocos"].values())),
    "STONE_SHA16": h16("Testemunho.lean"), "STONE_BYTES": mi(os.path.getsize(os.path.join(W, "Testemunho.lean"))), "STONE_LINHAS": str(axi["fonte"]["linhas"]),
    "OLEAN_SHA16": axi["olean"]["sha16"], "OLEAN_BYTES": mi(axi["olean"]["bytes"]), "BUILD_LINHA": axi["build"]["linha_built"], "BUILD_TAREFAS": axi["build"]["tarefas"],
    "SBX_ARQ_A": mi(sbx["k398c_final"]["arquivos"]), "SBX_ARQ_B": mi(sbx["k399_final"]["arquivos"]), "SBX_NOVOS": str(sbx["n_so_em_k399"]),
    "V_SINAPSE": fon["verbatim_sinapse"]["sha16"], "V_JOAO": fon["verbatim_joao"]["sha16"], "V_TESTIFICO": fon["verbatim_testifico"]["sha16"], "V_QUADRATICA": fon["verbatim_quadratica"]["sha16"],
    "V_QUADRATICA_FULL": fon["verbatim_quadratica"]["sha256"], "V_TESTIFICO_FULL": fon["verbatim_testifico"]["sha256"],
    "LOCK_LINHA": str(fon["um_py"]["linha_EXECUTION_LOCKED_NOT_ONE"]),
    "CAB_CITACOES": str(len(cab["citacoes"])), "CAB_SHA16": str(len(cab["sha16_citados"])),
    "SELAR_S": pt(proto["selar_total_s"]), "VERIF_S": pt(proto["verificar_s"]), "PARTES_S": pt(proto["selo"]["_medicao_s"]["partes"]), "RECON_S": pt(proto["selo"]["_medicao_s"]["reunir_e_reconstruir"]),
    "LIT_REFLECT_S": pt(cl["reflect_embutido_s"]), "LIT_MANIFEST_S": pt(cl["manifest_embutido_s"]),
    "PSI_B": mi(sel["psi"]["bytes"]), "THETA_B": mi(sel["theta"]["bytes"]), "KAPPA_B": mi(sel["kappa"]["bytes"]), "TOTAL_B": mi(proto["tamanho_das_partes_cruas_bytes"]["psi_mais_theta_mais_kappa"]),
    "RAZAO_TOTAL": pt(proto["tamanho_das_partes_cruas_bytes"]["psi_mais_theta_mais_kappa"] / n_objeto, 3),
    "PSI_SHA": sel["psi"]["sha256"][:16], "THETA_SHA": sel["theta"]["sha256"][:16], "KAPPA_SHA": sel["kappa"]["sha256"][:16],
    "M_UMPY": str(sel["kappa"]["campos"]["m_max_abs"]), "ERRO_UMPY": pt(sel["prova_de_reconstrucao"]["erro_real_maximo_antes_do_rint"], 4),
    "FEXP": pt(sel["estrutura"]["f_exp"], 4), "ENTROPIA": pt(sel["estrutura"]["entropia_dos_estados_bits"], 3),
    "NEG_PCT": pt(100 * aud["fracao_de_L_negativo"], 1), "POS_PCT": pt(100 - 100 * aud["fracao_de_L_negativo"], 1),
    "TK_ERRA": pt(100 * aud["theta_mais_kappa_com_sinal_unico"]["fracao_errada"], 1), "TK_ACERTA": pt(100 - 100 * aud["theta_mais_kappa_com_sinal_unico"]["fracao_errada"], 1),
    "PSI_ERRA": pt(100 * aud["psi_ou_psi_mais_kappa_sem_magnitudes"]["fracao_errada"], 1), "KAP_ERRA": pt(100 * aud["kappa_sozinho_melhor_chute_constante"]["fracao_errada"], 1),
    "N_E6": mi(cl["bytes_em_que_o_real_difere_do_inteiro_por_mais_de_1e-6"]), "N_E2": mi(cl["bytes_em_que_o_real_difere_do_inteiro_por_mais_de_1e-2"]),
    "PCT_E6": pt(100 * cl["bytes_em_que_o_real_difere_do_inteiro_por_mais_de_1e-6"] / n_objeto, 1), "PCT_E2": pt(100 * cl["bytes_em_que_o_real_difere_do_inteiro_por_mais_de_1e-2"] / n_objeto, 1),
    "C96_CASOS": mi(ex[(96, 8)]["casos"]), "C96_FALHAS": str(ex[(96, 8)]["falhas_apos_rint"]), "C96_ERRO": pt(ex[(96, 8)]["erro_real_max"], 4), "C96_MARGEM": ("%.1e" % ex[(96, 8)]["margem_min_ate_fronteira_de_arredondamento"]).replace(".", ","),
    "C128_CASOS": mi(ex[(128, 8)]["casos"]), "C128_ERRO": pt(ex[(128, 8)]["erro_real_max"], 4),
    "C0Q8_CASOS": mi(ex[(0, 8)]["casos"]), "C0Q8_FALHAS": mi(ex[(0, 8)]["falhas_apos_rint"]), "C0Q8_NAOINJ": str(ex[(0, 8)]["valores_nao_injetivos_em_m"]), "C0Q8_ERRO": pt(ex[(0, 8)]["erro_real_max"], 4),
    "C0Q12_ERRO": pt(ex[(0, 12)]["erro_real_max"], 4), "C64_FALHAS": str(ex[(64, 8)]["falhas_apos_rint"]),
    "SEM_Q8_ERRADOS": mi(sem["Q8"]["bytes_errados_so_com_theta_e_kappa"]), "SEM_N": mi(sem["Q8"]["n"]),
    "VER_C0_REAL": ver["centro_0_sem_sinal__objeto_real_4MB"], "VER_C0_ASCII": ":".join(ver["centro_0_sem_sinal__ASCII_puro"].split(":")[:2]),
    "VER_C128_ASCII": ":".join(ver["centro_128__ASCII_puro (todo L negativo: Psi e' redundante)"].split(":")[:2]), "VER_C96_ASCII": ver["centro_96__ASCII_puro (o perfil escolhido)"], "VER_C96_REAL": ver["centro_96__um_py_4MB (o perfil escolhido)"],
    "CTL_N": str(nctl), "CTL_TEMPO": pt(ct["objeto_inteiro_um_py"]["tempo_s"], 1), "CTL_TABELA": ctl_txt,
    "REG_S": pt(resumo["registro_core"]["tempo_total_s"]), "SIDECAR_S": pt(sim["sidecar_s"]), "SEL_S": pt(sim["selo_acom_v399_s"]), "DECL_S": pt(sim["declaracao_s"]),
    "SIM_BYTES": mi(sim["um_v399_simulado"]["bytes"]), "SIM_INS": mi(sim["um_v399_simulado"]["bytes_inseridos"]), "SIM_SHA16": sim["um_v399_simulado"]["sha16"],
    "CORE_BYTES": mi(objs["um_absoluto.json"]["bytes"]), "SELO_BYTES": mi(objs["um_absoluto_selo.json"]["bytes"]),
    "CORE_TK": pt(100 * objs["um_absoluto.json"]["acom"]["auditoria_de_separacao"]["theta_mais_kappa_com_sinal_unico"]["fracao_errada"], 1),
    "SELO_TK": pt(100 * objs["um_absoluto_selo.json"]["acom"]["auditoria_de_separacao"]["theta_mais_kappa_com_sinal_unico"]["fracao_errada"], 1),
    "SIDECAR_BYTES": mi(os.path.getsize(os.path.join(R, "um_absoluto_selo_acom.json"))),
    "OPS_PASS": str(ops["resultado"]["PASS"]), "OPS_FAIL": str(ops["resultado"]["FAIL"]),
    "SONDA_DIF": str(sonda["ms_em_que_o_codigo_difere"]), "SONDA_N": str(sonda["ms_testados"]),
    "TR_RAZAO": pt(tr["razao_de_tempo_encrypt_1024KiB_sobre_512KiB"]), "TR_MIN": pt(tr["extrapolacao_para_o_um_py_inteiro_se_quadratico"]["segundos"] / 60.0, 1), "TR_1M": pt(tr["amostras"][-1]["encrypt_s"], 3),
    "REPRO": "TODOS IGUAIS" if rp["todos_iguais"] else "DIVERGEM",
    "REPRO_T1": pt(list(rp["interpretes"].values())[0]["tempo_s"]), "REPRO_T2": pt(list(rp["interpretes"].values())[1]["tempo_s"]),
    "COL_NOMES": ", ".join(sorted(col["colisoes_com_o_um_py_v398"].keys())), "COL_N": str(col["n_nomes"]),
    "MAPA_CABECA": mapa["cabeca_da_cadeia_na_consulta"], "MAPA_N": str(mapa["n_registros"]),
    "MAPA_TABELA": "\n".join("| %s | %s | %s |" % (t, v["n"], ", ".join("`%s`" % x["rota_id"] for x in v["rotas_relevantes"][:3]) or "—") for t, v in mapa["consultas"].items()),
}
tmpl = open(os.path.join(W, "RESULTADO.md.tmpl"), "rb").read().decode("utf-8")
for k, v in F.items():
    tmpl = tmpl.replace("@@" + k + "@@", str(v))
restos = re.findall(r"@@[A-Z0-9_]+@@", tmpl)
assert not restos, restos
assert tmpl.split("\n")[0] == "v399 — SELO PELA PRÓPRIA TECNOLOGIA E TESTEMUNHO — estudo", tmpl.split("\n")[0]
out = os.path.join(W, "RESULTADO.md")
if os.path.exists(out):
    with open(out + ".bak_" + time.strftime("%Y%m%d_%H%M%S"), "xb") as f:
        f.write(open(out, "rb").read())
with open(out + ".tmp", "w", encoding="utf-8", newline="\n") as f:
    f.write(tmpl)
os.replace(out + ".tmp", out)
print("RESULTADO.md", h16("RESULTADO.md"), os.path.getsize(out), "bytes", tmpl.count("\n"), "linhas")
