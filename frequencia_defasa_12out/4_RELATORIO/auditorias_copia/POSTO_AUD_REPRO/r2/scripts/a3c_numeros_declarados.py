# -*- coding: utf-8 -*-
"""A3c -- confere os NUMEROS que o construtor otico declarou no resumo (texto da ordem) contra o RESULTADO_OPTICO.json
REPRODUZIDO pelo auditor (copia em <r2>/otico). Cada declarado e comparado com o valor medido, arredondado como foi
escrito (2 algarismos significativos para residuos)."""
import json, math, os

R2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = os.path.join(R2, "otico", "2_OPTICO", "RESULTADO_OPTICO.json")
d = json.load(open(M, encoding="utf-8"))
P = {x["id"]: x for x in d["por_parte"]}


def chk(pid, idx=None, nome_contem=None):
    cs = P[pid]["checks"]
    if nome_contem is not None:
        cs = [c for c in cs if nome_contem in c["nome"]]
    return cs[idx or 0]["numeros"] if cs else None


def sig2(x):
    if x is None or isinstance(x, str):
        return x
    if x == 0:
        return 0.0
    e = math.floor(math.log10(abs(x)))
    return round(x / 10 ** e, 1) * 10 ** e


linhas = []
def comp(rot, declarado, medido, tol_rel=0.051):
    if isinstance(declarado, (int, float)) and isinstance(medido, (int, float)):
        ok = (declarado == medido) or (declarado != 0 and abs(medido - declarado) <= tol_rel * abs(declarado)) or \
             (declarado == 0 and medido == 0)
    else:
        ok = (declarado == medido)
    linhas.append(dict(item=rot, declarado=declarado, medido=medido, confere=bool(ok)))


ex = P["P1.a"]["extra"]
comp("P1.a max|pureza-1| puros", 2.2e-15, sig2(ex["max_abs_pureza_menos_1_puros"]))
comp("P1.a max sigma2 puros", 2.3e-16, sig2(ex["max_sigma2_puros"]))
comp("P1.a max pureza mistos", 0.868, round(ex["max_pureza_mistos"], 3))
comp("P1.a menor sigma nao nulo mistos", 0.0287, round(ex["min_menor_sigma_nao_nulo_mistos"], 4))
n = chk("P1.b", nome_contem="Tr M^2 = (Tr M)^2")
comp("P1.b residuo identidade", 7.3e-15, sig2(n["max_residuo"]))
comp("P1.b residuo/tolerancia", 3.4e-4, sig2(n["max_residuo_sobre_tolerancia"]))
n = chk("P1.b", nome_contem="=> det M = 0")
comp("P1.b n matrizes implicacao", 1013, n["n"])
comp("P1.b n nao hermitianas", 1000, n["n_nao_hermitianas"])
comp("P1.b max|det|/tol", 9.8e-5, sig2(n["max_det_sobre_tolerancia"]))
n = chk("P1.d", nome_contem="|psi| = 1")
comp("P1.d desvio traco", 4.4e-16, sig2(n["max_desvio_traco"]))
comp("P1.d desvio idempotencia", 3.3e-16, sig2(n["max_desvio_idempotencia"]))
comp("P1.d desvio pureza", 8.9e-16, sig2(n["max_desvio_pureza"]))
comp("P3.a n pares", "P X P = <a,Xa> P (TOL_ID) em 60502 pares",
     [c["nome"] for c in P["P3.a"]["checks"] if c["nome"].startswith("P X P")][0])
comp("P3.a res PXP", 3.3e-16, sig2(chk("P3.a", nome_contem="P X P = <a,Xa> P")["max_residuo"]))
comp("P3.a res Tr", 3.3e-16, sig2(chk("P3.a", nome_contem="Tr(P X)")["max_residuo"]))
n = chk("P3.a", nome_contem="=> P X P / <a,Xa>")
comp("P3.a res divisao", 7.7e-15, sig2(n["max_residuo"]))
comp("P3.a min|<a,Xa>|", 2.3e-3, sig2(n["min_abs_w"]))
n = chk("P3.b", nome_contem="diag(1-b, b)")
comp("P3.b res |t|^2", 1.1e-16, sig2(n["res_t"]))
comp("P3.b res |r|^2", 0.0, n["res_r"])
n = chk("P3.b", nome_contem="mpmath")
comp("P3.b mp res_t (1.3e-51)", "1.3e-51", ("%.1e" % float(n["res_t"])) if n else None)
n4 = [c["numeros"] for c in P["P4"]["checks"]]
comp("P4 idem", 1.2e-15, sig2(n4[1]["max_idem"]))
comp("P4 herm", 0.0, n4[1]["max_herm"])
comp("P4 |TrP-d|", 3.1e-15, sig2(n4[2]["max_tr"]))
comp("P4 |Tr rho-1|", 8.9e-16, sig2(n4[2]["max_trrho"]))
comp("P4 |Tr rho^2-1/d|", 1.8e-15, sig2(n4[2]["max_pureza_menos_1_sobre_d"]))
n = chk("B1.b")
comp("B1.b n", 204, n["n"])
comp("B1.b max|TrP-posto|", 3.1e-15, sig2(n["max_residuo"]))
n = chk("B2.b", nome_contem="!= 0")
comp("B2.b |{Q,rho*}|_F", 0.156, round(n["norma"], 3))
n = chk("B2.b", nome_contem="Tr = 2 beta")
comp("B2.b res soma", 3.5e-18, sig2(n["res_soma"]))
comp("B2.b res traco", 0.0, n["res_traco"])
comp("B4.a u^H u", 1.3e-15, sig2(chk("B4.a", nome_contem="u^H u")["max_residuo"]))
comp("B4.a traco", 1.8e-15, sig2(chk("B4.a", nome_contem="Tr(u rho")["max_residuo"]))
comp("B4.a projecao", 1.1e-15, sig2(chk("B4.a", nome_contem="projecao")["max_residuo"]))
n = chk("B5.b", nome_contem="posto 2 e pureza")
comp("B5.b sigma1", 0.98797, round(n["sigmas"][0], 5))
comp("B5.b pureza", 0.97622690, round(n["pureza"], 8))
comp("B5.b res diag", 1.1e-16, sig2(chk("B5.b", nome_contem="D_inf F_thM(1) = diag")["residuo"]))
comp("B5.c res det", 5.6e-17, sig2(chk("B5.c", nome_contem="det D_t")["max_residuo"]))
comp("B5.c res traco", 2.2e-16, sig2(chk("B5.c", nome_contem="traco preservado")["max_residuo"]))
comp("B5.c menor sigma_min", 1.4e-4, sig2(chk("B5.c", nome_contem="t > 0: posto 2")["menor_sigma_min_entre_postos_2"]))
n = chk("B7.a1")
comp("B7.a1 max res", 2.0e-13, sig2(n["max_residuo"]))
comp("B7.a1 res/tol", 2.2e-4, sig2(n["max_residuo_sobre_tolerancia"]))
n = chk("B7.a2", nome_contem="toda janela")
comp("B7.a2 n janelas", 99970, n["n_janelas"])
comp("B7.a2 min amplitude", 0.99646, round(n["min_amplitude"], 5))
comp("B7.a2 cota", 0.99397, round(n["cota"], 5))
x2 = d["varredura"]["X2_t_denso_em_thM"]["maior_t_sem_posto_2_por_gamma"]
comp("A3 maior t sem posto 2 (gamma=1)", 4.0e-5, sig2(x2["1"]))
comp("A3 maior t sem posto 2 (gamma=beta)", 3.2e-3, sig2(x2["beta"]))
x1 = d["varredura"]["X1_theta_denso"]
comp("X1 n theta", 2010, x1["n_th"])
comp("X1 violacoes+ambiguos", 0, x1["ambiguos"] + x1["violacoes_B2a"] + x1["violacoes_B5a"] + x1["violacoes_B8b_B9b"] + x1["violacoes_B3a"])
comp("B3.d |beta - numero do operador (V4 l.16)|", 3.0e-7, sig2(chk("B3.d")["diferenca"]))
comp("B5.e(ii) contraexemplos (9 theta)", 9, len(P["B5.e(ii)"]["extra"]["contraexemplos"]))
comp("B9.a contraexemplos", ["0", "pi"], P["B9.a"]["extra"]["contraexemplos"])
comp("B9.a' contraexemplos", ["pi/2"], P["B9.a'"]["extra"]["contraexemplos"])
out = dict(fonte=M, n=len(linhas), n_confere=sum(1 for l in linhas if l["confere"]), linhas=linhas)
with open(os.path.join(R2, "saidas", "A3c_NUMEROS_DECLARADOS_v2.json"), "x", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
for l in linhas:
    print("%-5s %-38s declarado=%-14s medido=%s" % ("OK" if l["confere"] else "DIFF", l["item"], l["declarado"], l["medido"]))
print("confere:", out["n_confere"], "/", out["n"])
