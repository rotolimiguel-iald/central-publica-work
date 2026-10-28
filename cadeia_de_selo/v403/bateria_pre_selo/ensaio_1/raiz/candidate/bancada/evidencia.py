# -*- coding: utf-8 -*-
"""Operations on the resident motor with canonical identity and explicit instrumental
support. Profile approximations, posterior summaries and exploratory corrections
are distinct; none certifies a global significance or broad-prior evidence."""
import math
import threading
import time
import uuid

import numpy as np
import torch

from .amostrador import amostrar, resumo
from .motor import NOMES_THETA, opcoes_de, rotulo_opcoes, conjuntos_validos, validar_modelo_para_conjuntos
from .regua import ESTATUTOS, guarda, p_de_z, numero_finito, inteiro, booleano

CONJUNTOS = ("planck_comp", "desi_dr1", "desi_dr2", "sh0es", "pantheon", "sh0es_local", "cc_moresco", "pantheon_sh0es")   # 30/09: + Pantheon+ (cov completa, M profilado); + sh0es_local (Fase 2, lei D1a)
FIDUCIAL = dict(H0=67.5, ombh2=0.02237, omch2=0.1200, beta=0.0, c=0.0)
ESCALA = dict(H0=1.0, ombh2=0.0005, omch2=0.005, beta=0.005, c=0.005)


def _conj(c):
    return conjuntos_validos(c)


class Evidencia:
    def __init__(self, motor, livro, canonical_guard=None):
        self.m = motor
        self.livro = livro
        self.tarefas = {}
        from .canonical import require_current
        self._canonical_guard = canonical_guard or (lambda operation: require_current(operation, root=self.m.raiz))
        self._loaded_identity = None

    def _receipt(self, operation):
        receipt = self._canonical_guard(operation)
        if not isinstance(receipt, dict) or receipt.get("ok") is not True:
            raise ValueError("identidade canônica não validada")
        keys = ("canonical_manifest_sha256", "um_py_sha256", "seal_sha256")
        identity = tuple(receipt.get(k) for k in keys)
        if any(not isinstance(x, str) or not x for x in identity):
            raise ValueError("recibo de identidade incompleto")
        if self._loaded_identity is not None and identity != self._loaded_identity:
            raise ValueError("identidade mudou: recarga e revalidação necessárias")
        self._loaded_identity = identity
        return receipt

    def _support(self):
        return self.m.suporte

    def _beta(self, beta):
        if beta in (None, "livre"):
            return None
        if beta == "tgl":
            return self.m.beta_tgl
        if beta in ("zero", "lcdm"):
            return 0.0
        return numero_finito(beta, "beta")

    # ---------- avaliar ----------
    def avaliar(self, theta, conjuntos=None, curvas=True, opcoes=None):
        receipt = self._receipt("avaliar")
        booleano(curvas, "curvas")
        cj = _conj(conjuntos)
        o = validar_modelo_para_conjuntos(cj, opcoes)
        if not isinstance(theta, dict) or set(theta) - set(NOMES_THETA):
            raise ValueError("theta deve ser objeto com parâmetros conhecidos")
        vals = []
        for k in NOMES_THETA:
            v = theta.get(k, FIDUCIAL[k])
            vals.append(self.m.beta_tgl if k == "beta" and v == "tgl" else numero_finito(v, k))
        th = np.array([vals])
        for k, v in zip(NOMES_THETA, vals):
            lo, hi = self.m.limites[k]
            if not lo < v < hi:
                raise ValueError("%s fora do suporte instrumental explícito %s" % (k, (lo, hi)))
        with self.m.lock:
            tot, partes, p = self.m.chi2(th, cj, o)
            curv = self._curvas(th, o) if curvas else None
        out = dict(theta=dict(zip(NOMES_THETA, th[0].tolist())), conjuntos=cj, opcoes=o, modo=rotulo_opcoes(o), chi2_total=float(tot[0]),
                   chi2=dict((k, float(v[0])) for k, v in partes.items()), n_dados=self.m.n_dados(cj),
                   predito=dict(planck=p["planck"][0].tolist(), desi_dr1=p["dr1"][0].tolist(), desi_dr2=p["dr2"][0].tolist(), H0=float(p["H0"][0]), H0_local=float(p["H0_local"][0]), K_lei=float(p["K_lei"][0]), I_lei=float(p["I_lei"][0]),
                                pantheon=dict(n=self.m.pantheon.n, M_hat=float(self.m.pantheon.M_hat(p["pantheon_mu"])[0])),
                                pantheon_sh0es=dict(n=self.m.pantheon_sh0es.n, M_hat=float(self.m.pantheon_sh0es.M_hat(p["pantheon_sh0es_mu"])[0]))),
                   derivados=dict(Omega_L=float(p["OL"][0]), r_drag=float(p["r_drag"][0]), r_star=float(p["r_star"][0]), z_star=float(p["z_star"][0]),
                                  E0_menos_1=float(p["E0"][0]) - 1.0, residuo_fecho=float(p["res_fecho"][0]), autoverif_DM_camb=float(p["selfcheck"][0]),
                                  dentro_dos_limites=bool(p["dentro"][0])),
                   curvas=curv, gate_effect="NONE", estatuto="DIAGNOSTICO_DE_AVALIACAO", estatuto_texto=ESTATUTOS["DIAGNOSTICO_DE_AVALIACAO"])
        out["canonical"] = self._receipt("avaliar:done")
        out["suporte_instrumental"] = self._support()
        return guarda(out)

    def _curvas(self, th, opcoes=None):
        o = opcoes_de(opcoes)
        z = torch.linspace(0.02, 2.6, 160, device=self.m.dev, dtype=torch.float64)
        T = self.m._t(th)
        H0, ombh2, omch2, beta, c = [T[:, j] for j in range(5)]
        cam, _ = self.m.tab(H0, ombh2, omch2)
        beta_f = torch.zeros_like(beta) if o["beta_no_fundo"] == "nao" else beta
        fd = self.m.fundo.fundo(H0, ombh2, omch2, beta_f, c)
        z0 = torch.zeros_like(beta)
        fl = self.m.fundo.fundo(H0, ombh2, omch2, z0, z0)
        rd = cam["r_drag"] * self.m.fundo.rs_int(fd, cam["z_drag"]) / self.m.fundo.rs_int(fl, cam["z_drag"])
        zz = z[None, :]
        DM = self.m.fundo.DM(fd, zz)[0]
        DH = 299792.458 / (H0[:, None] * self.m.fundo.Ez(fd, zz))[0]
        DV = (z * DM * DM * DH) ** (1.0 / 3.0)
        # a curva ΛCDM de referência com os MESMOS (H0, ω_b, ω_c): mostra só o efeito de β e c
        rdl = cam["r_drag"]
        DMl = self.m.fundo.DM(fl, zz)[0]
        DHl = 299792.458 / (H0[:, None] * self.m.fundo.Ez(fl, zz))[0]
        DVl = (z * DMl * DMl * DHl) ** (1.0 / 3.0)
        f = lambda t: [float(v) for v in t.cpu()]
        Phi = fd["Phi"][0]
        xg = self.m.fundo.x2
        sel = (xg <= 0.0) & (xg >= -math.log(1.0 + 3.0))
        return dict(opcoes=o, escopo="CURVAS_GEOMETRICAS_BAO; leis SN/CC e R não são estes eixos", z=f(z), DM_rd=f(DM / rd[0]), DH_rd=f(DH / rd[0]), DV_rd=f(DV / rd[0]),
                    lcdm=dict(DM_rd=f(DMl / rdl[0]), DH_rd=f(DHl / rdl[0]), DV_rd=f(DVl / rdl[0])),
                    Phi=dict(z=f(torch.expm1(-xg[sel])), Phi=f(Phi[sel])))

    # ---------- ajustar ----------
    def _ajuste(self, cj, beta_fixo, c_livre, x0=None, opcoes=None):
        from scipy.optimize import least_squares
        cj = _conj(cj)
        o = validar_modelo_para_conjuntos(cj, opcoes)
        livres = ["H0", "ombh2", "omch2"] + (["beta"] if beta_fixo is None else []) + (["c"] if c_livre else [])
        base = np.array([FIDUCIAL[k] for k in NOMES_THETA])
        if beta_fixo is not None:
            base[3] = beta_fixo
        esc = np.array([ESCALA[k] for k in livres])
        idx = [NOMES_THETA.index(k) for k in livres]
        lim = self.m.limites
        for k, v in zip(NOMES_THETA, base):
            if k not in livres and not lim[k][0] < v < lim[k][1]:
                raise ValueError("parâmetro fixo fora do suporte: " + k)
        lo = np.array([(lim[k][0] - base[i]) / e for k, i, e in zip(livres, idx, esc)]) * 0.999
        hi = np.array([(lim[k][1] - base[i]) / e for k, i, e in zip(livres, idx, esc)]) * 0.999
        ini = np.zeros(len(livres)) if x0 is None else (np.asarray(x0)[idx] - base[idx]) / esc
        if not np.isfinite(ini).all() or not np.all((ini > lo) & (ini < hi)):
            raise ValueError("início do ajuste fora do suporte instrumental")

        def monta(Y):
            T = np.tile(base, (Y.shape[0], 1))
            T[:, idx] = base[idx] + Y * esc
            return T

        cache = {}

        def residuos_e_jac(y):
            key = tuple(np.round(y, 14))
            if key in cache:
                return cache[key]
            hstep = np.minimum(1e-3, np.minimum(y - lo, hi - y) * 0.25)
            if np.any(hstep <= 1e-14):
                raise ValueError("ajuste na borda: derivada central não resolvida")
            Y = np.vstack([y] + [y + hstep[i] * np.eye(len(y))[i] for i in range(len(y))] + [y - hstep[i] * np.eye(len(y))[i] for i in range(len(y))])
            with self.m.lock:
                R, _ = self.m.residuos(monta(Y), cj, o)
            R = R.cpu().numpy()
            n = len(y)
            if not np.isfinite(R).all():
                raise ValueError("resíduo não finito no ajuste")
            J = (R[1:1 + n] - R[1 + n:]).T / (2 * hstep)
            cache.clear(); cache[key] = (R[0], J)
            return R[0], J

        res = least_squares(lambda y: residuos_e_jac(y)[0], ini, jac=lambda y: residuos_e_jac(y)[1], bounds=(lo, hi), method="trf",
                            x_scale=1.0, xtol=1e-12, ftol=1e-12, gtol=1e-12, max_nfev=200)
        if not res.success:
            raise ValueError("ajuste não convergiu: " + str(res.message))
        th = monta(res.x[None, :])[0]
        r0, J = residuos_e_jac(res.x)
        chi2 = float(r0 @ r0)
        try:
            cov = np.linalg.inv(J.T @ J) * np.outer(esc, esc)
            sig = {k: float(math.sqrt(cov[i, i])) for i, k in enumerate(livres)}
        except np.linalg.LinAlgError:
            sig = {}
        profiled = ["M_supernova"] if set(cj) & {"pantheon", "pantheon_sh0es"} else []
        return dict(theta=dict(zip(NOMES_THETA, th.tolist())), chi2=chi2, livres=livres, sigma_JtJ=sig, sucesso=bool(res.success),
                    suporte_instrumental=self._support(), nfev=int(res.nfev), n_dados=self.m.n_dados(cj), gl=self.m.n_dados(cj) - len(livres) - len(profiled),
                    n_parametros_perfilados=len(profiled), parametros_perfilados=profiled, opcoes=o)

    def ajustar(self, conjuntos=None, beta="livre", c_livre=False, cliente="?", opcoes=None):
        self._receipt("ajustar")
        booleano(c_livre, "c_livre")
        cj = _conj(conjuntos)
        o = validar_modelo_para_conjuntos(cj, opcoes)
        bf = self._ajuste(cj, self._beta(beta), bool(c_livre), opcoes=o)
        modelo = dict(beta=str(beta), c_livre=bool(c_livre), opcoes=o)
        out = dict(conjuntos=cj, beta=beta, c_livre=bool(c_livre), opcoes=o, modo=rotulo_opcoes(o), ajuste=bf, beta_tgl=self.m.beta_tgl,
                   estatuto="AJUSTE_DE_MAXIMA_VEROSSIMILHANCA", estatuto_texto=ESTATUTOS["AJUSTE_DE_MAXIMA_VEROSSIMILHANCA"])
        if self._beta(beta) is None and "beta" in bf["sigma_JtJ"]:
            s = bf["sigma_JtJ"]["beta"]; b = bf["theta"]["beta"]
            if not math.isfinite(s) or s <= 0:
                raise ValueError("sigma local não resolvido")
            z = (self.m.beta_tgl - b) / s
            out["beta_tgl_em_sigma_JtJ"] = z
            out["significancia"] = self.livro.corrige(p_de_z(z), self.livro.familia("ajustar", cj, modelo))
        out["canonical"] = self._receipt("ajustar:done")
        out["suporte_instrumental"] = self._support()
        guarda(out)
        self.livro.registra(cliente, "ajustar", cj, modelo, dict(conjuntos=cj), out, out["estatuto"],
                            bf["chi2"], out.get("significancia", {}).get("p_local"))
        return out

    def comparar(self, conjuntos=None, c_livre=False, cliente="?", opcoes=None):
        self._receipt("comparar")
        booleano(c_livre, "c_livre")
        cj = _conj(conjuntos)
        o = validar_modelo_para_conjuntos(cj, opcoes)
        l = self._ajuste(cj, 0.0, bool(c_livre), opcoes=o)
        t = self._ajuste(cj, self.m.beta_tgl, bool(c_livre), x0=[l["theta"][k] for k in NOMES_THETA], opcoes=o)
        f = self._ajuste(cj, None, bool(c_livre), x0=[l["theta"][k] for k in NOMES_THETA], opcoes=o)
        d_tgl_livre = t["chi2"] - f["chi2"]
        d_lcdm_livre = l["chi2"] - f["chi2"]
        if min(d_tgl_livre, d_lcdm_livre) < -1e-6:
            raise ValueError("ajuste livre pior que modelo aninhado: comparação não resolvida")
        p_tgl = float(math.erfc(math.sqrt(max(d_tgl_livre, 0.0) / 2.0)))
        modelo = dict(c_livre=bool(c_livre), opcoes=o)
        out = dict(conjuntos=cj, c_livre=bool(c_livre), opcoes=o, modo=rotulo_opcoes(o), lcdm=l, tgl_beta_fixo=t, beta_livre=f, beta_tgl=self.m.beta_tgl,
                   delta_chi2=dict(tgl_menos_lcdm=t["chi2"] - l["chi2"], tgl_menos_livre=d_tgl_livre, lcdm_menos_livre=d_lcdm_livre),
                   leitura=("Δχ²(β = α√e contra β livre) = %.3f ⇒ z_local = %.2f (Wilks, 1 g.l.); Δχ²(β = 0 contra β livre) = %.3f [%s]"
                            % (d_tgl_livre, math.sqrt(max(d_tgl_livre, 0.0)), d_lcdm_livre, rotulo_opcoes(o))),
                   significancia=self.livro.corrige(p_tgl, self.livro.familia("comparar", cj, modelo)),
                   estatuto="COMPARACAO_DE_MODELOS_DELTA_CHI2", estatuto_texto=ESTATUTOS["COMPARACAO_DE_MODELOS_DELTA_CHI2"])
        out["canonical"] = self._receipt("comparar:done")
        out["suporte_instrumental"] = self._support()
        guarda(out)
        self.livro.registra(cliente, "comparar", cj, modelo, dict(conjuntos=cj), out, out["estatuto"], d_tgl_livre, p_tgl)
        return out

    # ---------- amostrar (tarefa assíncrona) ----------
    def amostrar(self, conjuntos=None, c_livre=False, walkers=256, passos=2000, queima=500, semente=42, cliente="?", opcoes=None):
        cj = _conj(conjuntos)
        o = validar_modelo_para_conjuntos(cj, opcoes)
        receipt = self._receipt("amostrar")
        booleano(c_livre, "c_livre")
        walkers = inteiro(walkers, "walkers", 16, 4096)
        if walkers % 2:
            raise ValueError("walkers deve ser par")
        passos = inteiro(passos, "passos", 100, 20000)
        queima = inteiro(queima, "queima", 0, passos - 50)
        semente = inteiro(semente, "semente", 0, 2**32 - 1)
        tid = uuid.uuid4().hex[:12]
        t = dict(id=tid, estado="na_fila", progresso=0, conjuntos=cj, c_livre=bool(c_livre), opcoes=o, modo=rotulo_opcoes(o), walkers=walkers,
                 passos=passos, queima=queima, semente=int(semente), criada=time.strftime("%H:%M:%S"), resultado=None, erro=None)
        self.tarefas[tid] = t
        threading.Thread(target=self._roda, args=(t, cliente), daemon=True).start()
        return dict(tarefa=tid, canonical=receipt, suporte_instrumental=self._support())

    def _roda(self, t, cliente):
        try:
            self._receipt("amostrar:start")
            t["estado"] = "rodando"
            nd = 5 if t["c_livre"] else 4
            nomes = list(NOMES_THETA[:nd])
            fid = np.array([FIDUCIAL[k] for k in nomes]); larg = np.array([ESCALA[k] for k in nomes]); larg[0] = 1.0
            rng = np.random.default_rng(t["semente"])
            low = np.array([self.m.limites[k][0] for k in nomes])
            high = np.array([self.m.limites[k][1] for k in nomes])
            p0 = fid + rng.normal(0, 1, size=(t["walkers"], nd)) * larg
            for _ in range(100):
                bad = ~np.all((p0 > low) & (p0 < high), axis=1)
                if not bad.any():
                    break
                p0[bad] = fid + rng.normal(0, 1, size=(int(bad.sum()), nd)) * larg
            if not np.all((p0 > low) & (p0 < high)):
                raise ValueError("não foi possível inicializar dentro do suporte instrumental")

            def logp(tt):
                th = tt if nd == 5 else torch.cat([tt, torch.zeros_like(tt[:, :1])], 1)
                with self.m.lock:
                    tot, _, _ = self.m.chi2(th, t["conjuntos"], t["opcoes"])
                return -0.5 * tot

            def ao_passo(s, n, seg):
                t["progresso"] = s / n; t["segundos"] = round(seg, 1)

            cadeia, lps, acc, seg = amostrar(logp, torch.tensor(p0, device=self.m.dev, dtype=torch.float64), t["passos"], t["semente"], ao_passo=ao_passo)
            res, taus, plano = resumo(cadeia, t["queima"], nomes)
            b = plano[:, 3]
            frac = float(np.mean(b >= self.m.beta_tgl)); frac0 = float(np.mean(b >= 0.0))
            cauda = 2.0 * min(frac, 1.0 - frac)
            hb, eb = np.histogram(b, bins=70)
            h2, ex, ey = np.histogram2d(b, plano[:, 0], bins=48)
            modelo = dict(c_livre=t["c_livre"], opcoes=t["opcoes"])
            out = dict(conjuntos=t["conjuntos"], c_livre=t["c_livre"], opcoes=t["opcoes"], modo=t["modo"], walkers=t["walkers"], passos=t["passos"],
                       queima=t["queima"], semente=t["semente"],
                       segundos=round(seg, 1), aceitacao_media=float(acc.mean()), tau=dict(zip(nomes, taus)),
                       amostras_efetivas=float(plano.shape[0] / max(taus)), resumo=res, beta_tgl=self.m.beta_tgl,
                       fracao_beta_acima_de_beta_tgl=frac, fracao_beta_acima_de_zero=frac0,
                       beta_tgl_pela_cauda=dict(massa_bilateral_empirica=cauda, n_amostras=int(plano.shape[0]),
                           p_frequentista=None, z_frequentista=None,
                           nota="massa posterior; zero amostras na cauda não mede probabilidade zero; não é p-valor"),
                       significancia=None, suporte_instrumental=self._support(),
                       hist_beta=dict(contagens=hb.tolist(), bordas=eb.tolist()),
                       hist_beta_H0=dict(contagens=h2.tolist(), bordas_beta=ex.tolist(), bordas_H0=ey.tolist()),
                       estatuto="POSTERIOR_CONDICIONAL_AO_MODELO_E_AOS_DADOS", estatuto_texto=ESTATUTOS["POSTERIOR_CONDICIONAL_AO_MODELO_E_AOS_DADOS"])
            out["canonical"] = self._receipt("amostrar:done")
            guarda(out)
            self.livro.registra(cliente, "amostrar", t["conjuntos"], modelo,
                                dict(walkers=t["walkers"], passos=t["passos"], queima=t["queima"], semente=t["semente"]), out, out["estatuto"],
                                res["beta"]["median"], None)
            t["resultado"] = out; t["estado"] = "pronta"; t["progresso"] = 1.0
        except Exception as e:  # falha visível, nunca «ok» falso
            t["estado"] = "falhou"; t["erro"] = repr(e)
