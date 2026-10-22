# -*- coding: utf-8 -*-
"""Correcao da correcao (gerencia, 03/10): o certificado a priori pela faixa numerica e' frouxo demais (tau * [(E_max - E_min) + 2 sum ||L_k||^2] ~ 7,7 > pi em d = 64
com gamma_diss = 10) e reprovaria logaritmos CERTOS. O certificado exato: o ARNES conhece o gerador verdadeiro S e compara ||L^ - S||_F / ||S||_F (o estimador continua
cego: so recebe M, k e gamma_anti). sigma = 0: desvio <= 1e-8 e Choi projetada >= -tol; sigma > 0: desvio <= 1e-3 (um enrolamento da desvio de ordem 1)."""
import ast, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "pilar_quantico_worker.py")
s = open(P, encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, (c, old[:120])
    s = s.replace(old, new)


rep('''    def generator_from_propagator(self, Phi, tau, d, checks=True):''', '''    def generator_from_propagator(self, Phi, tau, d, checks=True, S_true=None):''')
rep('''            info["ccp_min_rel"] = float(wk.min().item()) / mx if mx > 0 else 0.0''', '''            info["ccp_min_rel"] = float(wk.min().item()) / mx if mx > 0 else 0.0
        if S_true is not None:
            # o certificado do ramo pelo ARNES (que conhece o gerador verdadeiro): o logaritmo principal reproduziu S?
            info["gen_rel_dev"] = float((t.linalg.vector_norm(Lh - S_true) / t.linalg.vector_norm(S_true)).item())''')
rep('''    Phi = E.propagator(S, s1["tau"]); del S
    # o CERTIFICADO A PRIORI do ramo (o arnes, nao o estimador): |Im lambda(L)| <= (E_max - E_min) + 2 sum ||L_k||^2 (faixa numerica); se tau vezes isto < pi, o
    # logaritmo principal de Phi E' tau*L -- certificado, nao condicao necessaria (achado 20 da 2a passada)
    eH = np.linalg.eigvalsh((H + H.conj().T) / 2)
    bound = float(eH.max() - eH.min()) + 2.0 * sum(float(np.linalg.norm(L, 2)) ** 2 for L in Ls.values())
    apriori_ok = bool(s1["tau"] * bound < math.pi - s1["branch_margin"])
''', '''    Phi = E.propagator(S, s1["tau"])        # S fica: o arnes certifica o ramo comparando L^ com o gerador verdadeiro (o estimador NAO ve S)
''')
rep('''        dg, inf = E.generator_from_propagator(Phin, s1["tau"], d)''', '''        dg, inf = E.generator_from_propagator(Phin, s1["tau"], d, S_true=S)''')
rep('''        branch_ok = bool(apriori_ok and (inf["ccp_min_rel"] >= -tol["ccp_rel"] if sigma == 0 else True))''',
    '''        branch_ok = bool((inf["gen_rel_dev"] <= s1["branch_dev_sigma0"] and inf["ccp_min_rel"] >= -tol["ccp_rel"]) if sigma == 0
                         else inf["gen_rel_dev"] <= s1["branch_dev_noisy"])''')
rep('''"branch_ok": branch_ok, "tau_apriori_bound": s1["tau"] * bound, **inf})''', '''"branch_ok": branch_ok, **inf})''')
rep('''    del Phi
    return {"d": d, "nc": nc, "idx": idx, "law_power_injected": law_power''', '''    del Phi, S
    return {"d": d, "nc": nc, "idx": idx, "law_power_injected": law_power''')
# E4: o mesmo certificado
rep('''    dg, inf = E.generator_from_propagator(E.propagator(S, tau), tau, d)''', '''    dg, inf = E.generator_from_propagator(E.propagator(S, tau), tau, d, S_true=S)''')
rep('''and inf["tau_antiherm_norm"] < math.pi - 0.1 and inf["ccp_min_rel"] >= -1e-9)''', '''and inf["gen_rel_dev"] <= 1e-8 and inf["ccp_min_rel"] >= -1e-9)''')
# a sonda de tempo com o mesmo caminho (o custo da comparacao entra)
rep('''            dg, inf = E.generator_from_propagator(Phi, 0.05, d)
            fit_root_law(Cc @ dg.reshape(d, d).cpu().numpy() @ Cc, kk, 1.0); E.sync(); t1.append(time.time() - a)''',
    '''            dg, inf = E.generator_from_propagator(Phi, 0.05, d, S_true=S)
            fit_root_law(Cc @ dg.reshape(d, d).cpu().numpy() @ Cc, kk, 1.0); E.sync(); t1.append(time.time() - a)''')
rep('''            S = E.superop(E.T(H), [E.T(L) for L in Ls]); Phi = E.propagator(S, 0.05); del S
            kk = np.r_[np.zeros(2), np.linspace(0.5, 2.5, d - 2)]; Cc = np.eye(d) - np.ones((d, d)) / d''',
    '''            S = E.superop(E.T(H), [E.T(L) for L in Ls]); Phi = E.propagator(S, 0.05)
            kk = np.r_[np.zeros(2), np.linspace(0.5, 2.5, d - 2)]; Cc = np.eye(d) - np.ones((d, d)) / d''')
rep('''            dg, inf = E.generator_from_propagator(Phi + 1e-8 * E.T(rg.standard_normal(Phi.shape)), 0.05, d)
            fit_root_law(Cc @ dg.reshape(d, d).cpu().numpy() @ Cc, kk, 1.0); E.sync(); t1n.append(time.time() - a)
            del Phi''', '''            dg, inf = E.generator_from_propagator(Phi + 1e-8 * E.T(rg.standard_normal(Phi.shape)), 0.05, d, S_true=S)
            fit_root_law(Cc @ dg.reshape(d, d).cpu().numpy() @ Cc, kk, 1.0); E.sync(); t1n.append(time.time() - a)
            del Phi, S''')
ast.parse(s)
open(P + ".tmp", "w", encoding="utf-8", newline=chr(10)).write(s); os.replace(P + ".tmp", P); print("ok")
