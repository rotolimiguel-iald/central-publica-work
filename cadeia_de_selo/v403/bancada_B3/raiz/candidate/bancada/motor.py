# -*- coding: utf-8 -*-
"""motor.py -- o MOTOR da Bancada Um: tabela CAMB + fundo V3 em lote + verossimilhanças, residentes (carregados uma vez, na RAM/VRAM).

Parâmetros: θ = (H0, ω_b, ω_c, β, c). β é livre, fixo em β_TGL = α_CODATA2018 · √e (calculado em runtime, nunca literal) ou 0 (ΛCDM).
Conjuntos de dados: 'planck_comp' (R, l_A, ω_b; Zhai+ 2019), 'desi_dr1' (12 linhas), 'desi_dr2' (13 medidas + cov), 'sh0es', 'pantheon', 'sh0es_local' (30/09, Fase 2: SH0ES lido como H0_local = H0·(1+z*)^β, a lei D1a [CONJECTURE]), 'cc_moresco' (30/09, Fase 4: os 32 cronômetros H(z) de Moresco+ 2022 importados do artigo 1, lidos com a lei acumulada de z* até z). Opções da Fase 4: lei = 'd1a' | 'd1b' (o núcleo derivado do artigo 1); beta_no_fundo = 'sim' | 'nao' (a convenção do artigo: β só na lei).
SH0ES na Bancada (01/10): conjunto 'pantheon_sh0es' (1657 = 1580 de cosmologia + 77 calibradores Cefeida com μ = CEPH_DIST; M profilado); lei_sn = 'nenhuma' |
'sombra' (D_M/K em todo z) | 'acumulada' (K(z) ao longo da integral de D_M); lei_cc = 'acumulada' (a Fase 4) | 'nenhuma' (os relógios leem a face).
O primário do D1 V3 selado é planck_comp + desi_dr1 (sem SH0ES).
"""
import math
import os
import threading

import numpy as np
import torch

from . import fontes
from .camb_tabela import TabelaCAMB
from .fundo_gpu import C_KMS, FundoV3Lote
from .pantheon_cov import PantheonCov
from .regua import numero_finito, inteiro

NOMES_THETA = ("H0", "ombh2", "omch2", "beta", "c")

# Opções de modelo/verossimilhança. O padrão científico é TGL/eff; a REPRODUÇÃO DO SELADO exige modo="selado" explícito. O corrigido corrige os
# defeitos técnicos verificados (D1F-01 DR1 correlacionado; D1F-03 covariância do Planck de Chen+2019; D1F-V1 DM* por razão sobre o CAMB, o
# neutrino massivo contado uma vez). O mapa de R (como Ω_m entra no parâmetro de deslocamento) é ESCOLHA DE MODELO [INPUT] não derivada
# (D1F-02): explícito; presets históricos selado/corrigido conservam nu e TGL usa eff ratificado.
OPCOES_SELADO = dict(planck_cov="pipeline", dr1_cov="diagonal", dm_star="direto", mapa_R="nu", lei="d1a", beta_no_fundo="sim", lei_sn="nenhuma", lei_cc="acumulada", cc_cov="diagonal")
OPCOES_CORRIGIDO = dict(planck_cov="chen2019", dr1_cov="correlacionada", dm_star="razao_camb", mapa_R="nu", lei="d1a", beta_no_fundo="sim", lei_sn="nenhuma", lei_cc="acumulada", cc_cov="diagonal")
# 30/09/2026: o mapa de R RATIFICADO pelo operador («Sim destranque tudo»): a permanência é verbo -- o mesmo ato veste D_M e a raiz de R,
# logo o Ω_m do parâmetro de deslocamento é o EFETIVO (1+β)Ω_m. «selado» e «corrigido» ficam como estavam (reprodução e controle).
OPCOES_TGL = dict(planck_cov="chen2019", dr1_cov="correlacionada", dm_star="razao_camb", mapa_R="eff", lei="d1a", beta_no_fundo="sim", lei_sn="nenhuma", lei_cc="acumulada", cc_cov="diagonal")
# 30/09/2026 (Fase 2): a lei D1a [CONJECTURE] na verossimilhança -- a escada local mede H0_local = H0·(1+z*)^β; z* fixo do pipeline D1a de
# Coma [INPUT] (o z* do modelo difere de menos de 0,2%%, o que muda (1+z*)^β em menos de 3e-5). Em β = 0 a lei devolve H0_local = H0 (ΛCDM).
Z_STAR_D1A = 1089.95
# 30/09/2026 (Fase 4, o desvio): a CONVENÇÃO DO ARTIGO 1 («Haja Luz», predict_H0_zero_free / D1_kernel_discrimination) -- a lei transporta a
# calibração ΛCDM (β NÃO entra no fundo: beta_no_fundo="nao") e o núcleo é o DERIVADO D1b (lei="d1b": 𝒲 = |1+w_eff|, cuja integral no registro
# N = ln(1+z) é (2/3)·ln E_ΛCDM(z) pela equação de Raychaudhuri em FRW plano com ρ+p ≥ 0), logo K = E_ΛCDM(z*)^{2β/3}; lei="d1a" é o caso
# 𝒲 = 1, K = (1+z*)^β. Empilhar a lei sobre um fundo que já carrega β (beta_no_fundo="sim" com mapa eff/E1) conta β duas vezes (achado de 30/09).
OPCOES_ARTIGO = dict(planck_cov="chen2019", dr1_cov="correlacionada", dm_star="razao_camb", mapa_R="nu", lei="d1b", beta_no_fundo="nao", lei_sn="nenhuma", lei_cc="acumulada", cc_cov="diagonal")
_OPCOES_VALIDAS = dict(planck_cov=("pipeline", "chen2019"), dr1_cov=("diagonal", "correlacionada"), dm_star=("direto", "razao_camb"), mapa_R=("nu", "eff"),
                       lei=("d1a", "d1b"), beta_no_fundo=("sim", "nao"),
                       lei_sn=("nenhuma", "sombra", "acumulada"), lei_cc=("acumulada", "nenhuma"),
                       cc_cov=("diagonal", "moresco2020", "moresco2020_todos"))   # Fase 7 (01/10): a covariância dos cronômetros


def opcoes_de(o):
    """Completa e valida as opções: {"modo": "selado"|"corrigido"} escolhe o preset; as chaves individuais sobrepõem. Chave ou valor
    desconhecido é recusado (falha visível)."""
    if o is not None and not isinstance(o, dict):
        raise ValueError("opcoes deve ser objeto ou None")
    o = dict(o or {})
    modo = o.pop("modo", "tgl")
    if modo not in ("selado", "corrigido", "tgl", "artigo"):
        raise ValueError("modo %r; use 'selado', 'corrigido', 'tgl' ou 'artigo'" % modo)
    base = dict({"selado": OPCOES_SELADO, "corrigido": OPCOES_CORRIGIDO, "tgl": OPCOES_TGL, "artigo": OPCOES_ARTIGO}[modo])
    for k, v in o.items():
        if k not in _OPCOES_VALIDAS:
            raise ValueError("opção desconhecida %r (válidas: %s)" % (k, sorted(_OPCOES_VALIDAS)))
        if v not in _OPCOES_VALIDAS[k]:
            raise ValueError("valor %r para %s (válidos: %s)" % (v, k, _OPCOES_VALIDAS[k]))
        base[k] = v
    return base


def rotulo_opcoes(o):
    """Name a preset only when every option matches it; otherwise show the mix."""
    o = opcoes_de(o)
    if o == OPCOES_ARTIGO:
        modo = "artigo (fundo ΛCDM; β só na lei)"
    elif o == OPCOES_TGL:
        modo = "tgl (corrigido + mapa de R efetivo, ratificado 30/09)"
    elif o == OPCOES_CORRIGIDO:
        modo = "corrigido"
    elif o == OPCOES_SELADO:
        modo = "selado"
    else:
        modo = "misto (não equivale a preset)"
    return modo + " · " + "; ".join(k + "=" + str(v) for k,v in sorted(o.items()))


CONJUNTOS = ("planck_comp", "desi_dr1", "desi_dr2", "sh0es", "pantheon", "sh0es_local", "cc_moresco", "pantheon_sh0es")
CONJUNTOS_PADRAO = ("planck_comp", "desi_dr1")


def conjuntos_validos(conjuntos=None):
    """Known overlap is refused until a joint likelihood is specified."""
    if conjuntos is None:
        conjuntos = CONJUNTOS_PADRAO
    if not isinstance(conjuntos, (list, tuple)) or not conjuntos or any(type(x) is not str for x in conjuntos):
        raise ValueError("conjuntos deve ser lista não vazia de nomes")
    c = list(conjuntos)
    if len(set(c)) != len(c):
        raise ValueError("conjuntos duplicados")
    if any(x not in CONJUNTOS for x in c):
        raise ValueError("conjunto desconhecido")
    for grupo in ({"desi_dr1", "desi_dr2"}, {"pantheon", "pantheon_sh0es", "sh0es", "sh0es_local"}):
        if len(set(c) & grupo) > 1:
            raise ValueError("sobreposição sem likelihood conjunta: " + ", ".join(sorted(set(c) & grupo)))
    return c


def validar_modelo_para_conjuntos(conjuntos, opcoes=None):
    """Validate interacting model choices only when their consumer is selected.

    TGL/eff with Planck+DESI remains the default. Accumulated/local transport
    and a beta-modified background cannot be charged together in one reader.
    The plain Pantheon implementation does not consume lei_sn.
    """
    cj = conjuntos_validos(conjuntos)
    o = opcoes_de(opcoes)
    if "pantheon" in cj and o["lei_sn"] != "nenhuma":
        raise ValueError("lei_sn não implementada no Pantheon só-cosmologia; opção sem consumidor")
    conflicts = []
    if o["beta_no_fundo"] == "sim":
        if "cc_moresco" in cj and o["lei_cc"] == "acumulada":
            conflicts.append("cc_moresco/lei_cc=acumulada")
        if "sh0es_local" in cj:
            conflicts.append("sh0es_local/transporte")
        if "pantheon_sh0es" in cj and o["lei_sn"] != "nenhuma":
            conflicts.append("pantheon_sh0es/lei_sn=" + o["lei_sn"])
    if conflicts:
        raise ValueError("dupla contagem de β: fundo modificado e transporte no mesmo leitor: " + ", ".join(conflicts))
    return o


class Motor:
    def __init__(self, raiz, dispositivo=None, n_grade=20001):
        n_grade = inteiro(n_grade, "n_grade", 5, 1000001)
        if dispositivo is None:
            dispositivo = "cuda" if torch.cuda.is_available() else "cpu"
        self.dev = torch.device(dispositivo)
        self.lock = threading.Lock()
        self.alpha, self.prov_alpha = fontes.alpha_codata_2018()
        self.beta_tgl = self.alpha * math.sqrt(math.e)
        self.d1, self.prov_d1 = fontes.d1_v3_primario()
        self.dr2, self.prov_dr2 = fontes.desi_dr2()
        self.pan, self.prov_pan = fontes.pantheon_plus()
        self.cc, self.prov_cc = fontes.cronometros_moresco2022()   # Fase 4 (30/09): os 32 cronômetros, importados do artigo 1
        self.cc_cov_sets, self.prov_cc_cov = fontes.cronometros_covariancia_moresco2020()   # Fase 7 (01/10): a covariância completa de Moresco+2020
        self.raiz = raiz
        self.tab = TabelaCAMB(raiz + r"\tabelas\camb_lcdm_v1.npz", dispositivo)
        self.erro_tabela = self.tab.erro_no_teste()
        self.fundo = FundoV3Lote(dispositivo, n_grade=n_grade)
        self.limites_declarados = {k: tuple(v) for k, v in self.d1["limites"].items()}
        self.limites = dict(self.limites_declarados)
        for k, (lo, hi) in self.tab.suporte.items():
            a, b = self.limites[k]
            self.limites[k] = (max(a, lo), min(b, hi))
            if self.limites[k][0] >= self.limites[k][1]:
                raise ValueError("prior e suporte CAMB sem interseção: " + k)
        self.suporte = dict(estatuto="SUPORTE_INSTRUMENTAL_DIAGNOSTICO",
                            limites_declarados=self.limites_declarados, limites_efetivos=self.limites,
                            tabela=self.tab.suporte, intervalos="abertos",
                            prior_amplo_coberto=False, evidencia_prior_amplo_autorizada=False,
                            nota="Ajuste restrito e posterior diagnóstico uniforme na interseção; não é prior científico novo.")
        self._prepara()

    def _t(self, a):
        if torch.is_tensor(a):
            return a.to(device=self.dev, dtype=torch.float64)
        return torch.as_tensor(np.asarray(a, float), device=self.dev, dtype=torch.float64)

    def _prepara(self):
        d1 = self.d1
        self.planck_mean = self._t(d1["planck_mean"])
        self.planck_Linv = torch.linalg.inv(torch.linalg.cholesky(self._t(d1["planck_cov"])))
        self.planck_cov_chen, self.prov_planck_chen = fontes.planck_chen2019(d1["planck_mean"])
        self.planck_Linv_chen = torch.linalg.inv(torch.linalg.cholesky(self._t(self.planck_cov_chen)))
        self.dr1_cov_corr, self.prov_dr1_corr = fontes.desi_dr1_covariancia(d1["desi_rows"])
        self.dr1_Linv_corr = torch.linalg.inv(torch.linalg.cholesky(self._t(self.dr1_cov_corr)))
        self.dr1_z = self._t([r[0] for r in d1["desi_rows"]])
        self.dr1_tipo = [int(r[1]) for r in d1["desi_rows"]]            # 0 DM/rd, 1 DH/rd, 2 DV/rd
        self.dr1_sig = self._t([r[2] for r in d1["desi_rows"]])
        self.dr1_val = self._t(d1["desi_vals"])
        q = self.dr2["grandeza"]
        self.dr2_z = self._t(self.dr2["z"])
        self.dr2_tipo = [{"DM_over_rs": 0, "DH_over_rs": 1, "DV_over_rs": 2}[g] for g in q]
        self.dr2_val = self._t(self.dr2["valor"])
        self.dr2_Linv = torch.linalg.inv(torch.linalg.cholesky(self._t(self.dr2["cov"])))
        # 30/09: Pantheon+ ligado -- covariância STAT+SYS completa, amostra só-cosmologia, M profilado
        self.pantheon = PantheonCov(self.pan, self.dev, os.path.join(self.raiz, "tabelas"))
        self.pantheon_sh0es = PantheonCov(self.pan, self.dev, os.path.join(self.raiz, "tabelas"), calibradores=True)   # 01/10: SH0ES na Bancada (1657; μ = CEPH_DIST nos calibradores)
        self.cc_z = self._t(self.cc["z"]); self.cc_H = self._t(self.cc["H"]); self.cc_sig = self._t(self.cc["sigma"])   # Fase 4 (30/09)
        # Fase 7 (01/10): os conjuntos de cronômetros por covariância -- 'diagonal' (os 32 do artigo, erros diagonais) e as variantes de Moresco+2020 ((z, H) da fonte nos 15 pontos)
        self.cc_sets = {"diagonal": dict(z=self.cc_z, H=self.cc_H, Linv=torch.diag(1.0 / self.cc_sig))}
        for v, S in self.cc_cov_sets.items():
            self.cc_sets[v] = dict(z=self._t(S["z"]), H=self._t(S["H"]), Linv=torch.linalg.inv(torch.linalg.cholesky(self._t(S["cov"]))))

    # ---------- predições ----------
    def _chunk(self):
        """Tamanho de lote que cabe na VRAM livre agora (a GPU é compartilhada com o llama-server)."""
        if self.dev.type != "cuda":
            return 64
        livre, _ = torch.cuda.mem_get_info(self.dev)
        por_linha = 16 * self.fundo.n * 8
        return int(max(8, min(4096, 0.5 * livre // por_linha)))

    def predizer(self, theta, opcoes=None):
        """θ (B,5) -> dict de tensores (B,...) com os observáveis de todos os conjuntos, e máscara de validade. `opcoes`: ver opcoes_de."""
        o = opcoes_de(opcoes)
        if torch.is_tensor(theta):
            if theta.dtype == torch.bool or theta.is_complex():
                raise ValueError("theta deve ser real não booleano")
        else:
            for v in np.asarray(theta, dtype=object).flat:
                numero_finito(v, "theta")
        theta = self._t(theta)
        if theta.ndim not in (1, 2) or theta.shape[-1] != 5 or theta.numel() == 0 or not bool(torch.isfinite(theta).all()):
            raise ValueError("theta deve ter forma (B,5), B>0, com valores finitos")
        theta = theta.reshape(-1, 5)
        passo = self._chunk()                                   # calculado UMA vez por chamada (a VRAM muda; o lote não)
        saidas = [self._predizer_bloco(theta[i:i + passo], o) for i in range(0, theta.shape[0], passo)]
        out = {k: torch.cat([s[k] for s in saidas]) for k in saidas[0]}
        assert out["H0"].shape[0] == theta.shape[0]
        return out

    def _obs_bao(self, fd, z, tipos, rd):
        zz = z[None, :].expand(fd["H0"].shape[0], -1)
        DM = self.fundo.DM(fd, zz)
        DH = C_KMS / (fd["H0"][:, None] * self.fundo.Ez(fd, zz))
        DV = (zz * DM * DM * DH) ** (1.0 / 3.0)
        pilha = torch.stack([DM, DH, DV], -1)
        t = torch.as_tensor(tipos, device=self.dev)
        return torch.gather(pilha, 2, t[None, :, None].expand(pilha.shape[0], -1, 1))[..., 0] / rd[:, None]

    def _predizer_bloco(self, th, o=None):
        o = opcoes_de(o)
        H0, ombh2, omch2, beta, c = [th[:, j] for j in range(5)]
        cam, dentro = self.tab(H0, ombh2, omch2)
        for j, nm in enumerate(NOMES_THETA):
            lo, hi = self.limites[nm]
            dentro = dentro & (th[:, j] > lo) & (th[:, j] < hi)
        zs = torch.where(dentro, cam["z_star"], torch.full_like(H0, 1090.0))
        zd = torch.where(dentro, cam["z_drag"], torch.full_like(H0, 1060.0))
        zero = torch.zeros_like(beta)
        beta_f = zero if o["beta_no_fundo"] == "nao" else beta   # Fase 4 (30/09): na convenção do artigo o fundo é ΛCDM e β entra só na lei
        tgl = self.fundo.fundo(H0, ombh2, omch2, beta_f, c)
        lcdm = self.fundo.fundo(H0, ombh2, omch2, zero, zero)
        r_star = cam["r_star"] * self.fundo.rs_int(tgl, zs) / self.fundo.rs_int(lcdm, zs)
        r_drag = cam["r_drag"] * self.fundo.rs_int(tgl, zd) / self.fundo.rs_int(lcdm, zd)
        DM_star = self.fundo.DM(tgl, zs[:, None])[:, 0]
        DM_star_lcdm = self.fundo.DM(lcdm, zs[:, None])[:, 0]
        selfcheck = DM_star_lcdm / cam["DM_star"]
        if o["dm_star"] == "razao_camb":
            # D1F-V1 (auditoria 28/09): o integrador conta o neutrino massivo duas vezes (N_eff inteiro como radiação + m_ν como matéria);
            # como já se faz com r_* e r_drag, D_M(z*) entra por RAZÃO TGL/ΛCDM sobre o D_M do CAMB, e o viés cancela.
            DM_star = cam["DM_star"] * DM_star / DM_star_lcdm
        Om = (ombh2 + omch2 + 0.06 / 93.14) / (H0 / 100.0) ** 2
        R = torch.sqrt(Om) * H0 / C_KMS * DM_star
        if o["mapa_R"] == "eff":
            # D1F-02: o Ω_m EFETIVO na era da matéria, (1+β)Ω_m (Φ ≈ 1 + β) -- a escolha do pré-registro do Nível 2 S; [INPUT] não derivado
            R = R * torch.sqrt(1.0 + beta)
        lA = math.pi * DM_star / r_star
        # Fase 4 (30/09): a lei no registro N = ln(1+z). D1a: I(z) = ln(1+z). D1b: I(z) = ∫₀^N |1+w_eff| dN' = (2/3)·ln E_ΛCDM(z) (Raychaudhuri, FRW
        # plano, ρ+p ≥ 0; conferido por trapézio no runner da Fase 4). O fator da escada é K = exp(β I(z*)); um cronômetro em z lê
        # H0·E(z)·exp(β[I(z*) − I(z)]) -- a resposta acumulada desde a recombinação, como em D1_kernel_discrimination do artigo 1.
        zsl = torch.full_like(H0, Z_STAR_D1A)
        zcc = self.cc_sets[o["cc_cov"]]["z"][None, :].expand(H0.shape[0], -1)   # Fase 7 (01/10): os z do conjunto da covariância escolhida
        if o["lei"] == "d1b":
            I_lei = (2.0 / 3.0) * torch.log(self.fundo.Ez(lcdm, zsl[:, None])[:, 0])
            I_cc = (2.0 / 3.0) * torch.log(self.fundo.Ez(lcdm, zcc))
        else:
            I_lei = torch.log1p(zsl)
            I_cc = torch.log1p(zcc)
        K_lei = torch.exp(beta * I_lei)
        cc_H = H0[:, None] * self.fundo.Ez(tgl, zcc) * torch.exp(beta[:, None] * (I_lei[:, None] - I_cc))
        if o["lei_cc"] == "nenhuma":   # SH0ES (01/10): na leitura «sombra» os relógios leem a face (sem fator)
            cc_H = H0[:, None] * self.fundo.Ez(tgl, zcc)
        # SH0ES (01/10): o Pantheon+SH0ES com calibradores e a lei nas DISTÂNCIAS: 'nenhuma' (H0 de fundo), 'sombra' (D_M/K, o fator constante em todo z),
        # 'acumulada' (K(z) = exp(β[I(z*) − I(z)]) dentro da integral de D_M; K = 1 além de z*). O núcleo (d1a/d1b) é o de `lei`, sobre o ΛCDM.
        zsn = self.pantheon_sh0es.zHD[None, :].expand(H0.shape[0], -1)
        if o["lei_sn"] == "sombra":
            DM_sn = self.fundo.DM(tgl, zsn) / K_lei[:, None]
        elif o["lei_sn"] == "acumulada":
            x2 = self.fundo.x2[None, :]
            if o["lei"] == "d1b":
                logK2 = beta[:, None] * (I_lei[:, None] - (2.0 / 3.0) * torch.log(lcdm["E"]))
            else:
                logK2 = beta[:, None] * (I_lei[:, None] + x2)
            logK2 = torch.where(x2 >= -math.log1p(Z_STAR_D1A), logK2, torch.zeros_like(logK2))
            DM_sn = self.fundo.DM_com_boost(tgl, zsn, logK2)
        else:
            DM_sn = self.fundo.DM(tgl, zsn)
        mu_sh0es = self.pantheon_sh0es.mu(DM_sn)
        mu_sn = self.pantheon.mu(self.fundo.DM(tgl, self.pantheon.zHD[None, :].expand(H0.shape[0], -1)))   # 30/09: Pantheon+
        out = dict(planck=torch.stack([R, lA, ombh2], 1), dr1=self._obs_bao(tgl, self.dr1_z, self.dr1_tipo, r_drag),
                   dr2=self._obs_bao(tgl, self.dr2_z, self.dr2_tipo, r_drag), H0=H0, r_drag=r_drag, r_star=r_star, z_star=zs,
                   OL=tgl["OL"], res_fecho=tgl["res_fecho"], selfcheck=selfcheck, dentro=dentro,
                   E0=self.fundo.Ez(tgl, torch.zeros_like(H0)[:, None])[:, 0], pantheon_mu=mu_sn,
                   H0_local=H0 * K_lei, K_lei=K_lei, I_lei=I_lei, cc_H=cc_H,   # Fase 2/4 (30/09): o setor local pela lei (d1a ou d1b); os cronômetros com a lei acumulada
                   pantheon_sh0es_mu=mu_sh0es)   # SH0ES (01/10): o Pantheon+SH0ES com calibradores e a lei nas distâncias
        del tgl, lcdm
        return out

    # ---------- verossimilhança ----------
    def _r_planck(self, p, o):
        Linv = self.planck_Linv_chen if o["planck_cov"] == "chen2019" else self.planck_Linv
        return (p["planck"] - self.planck_mean[None, :]) @ Linv.T

    def _r_dr1(self, p, o):
        if o["dr1_cov"] == "correlacionada":
            return (p["dr1"] - self.dr1_val[None, :]) @ self.dr1_Linv_corr.T
        return (p["dr1"] - self.dr1_val[None, :]) / self.dr1_sig[None, :]

    def _r_cc(self, p, o):
        """Fase 7 (01/10): resíduos BRANQUEADOS dos cronômetros pela covariância escolhida (cc_cov): diagonal (1/σ) ou Moresco+2020 (L⁻¹ de Cholesky)."""
        S = self.cc_sets[o["cc_cov"]]
        return (p["cc_H"] - S["H"][None, :]) @ S["Linv"].T

    def chi2(self, theta, conjuntos=("planck_comp", "desi_dr1"), opcoes=None):
        """χ² por conjunto e total, (B,). Pontos fora dos limites/tabela: +inf (recusados, contados). `opcoes`: ver opcoes_de."""
        conjuntos = conjuntos_validos(conjuntos)
        o = validar_modelo_para_conjuntos(conjuntos, opcoes)
        p = self.predizer(theta, o)
        partes = {}
        if "planck_comp" in conjuntos:
            r = self._r_planck(p, o)
            partes["planck_comp"] = (r * r).sum(1)
        if "desi_dr1" in conjuntos:
            r = self._r_dr1(p, o)
            partes["desi_dr1"] = (r * r).sum(1)
        if "desi_dr2" in conjuntos:
            r = (p["dr2"] - self.dr2_val[None, :]) @ self.dr2_Linv.T
            partes["desi_dr2"] = (r * r).sum(1)
        if "sh0es" in conjuntos:
            partes["sh0es"] = ((p["H0"] - self.d1["sh0es_mean"]) / self.d1["sh0es_sigma"]) ** 2
        if "sh0es_local" in conjuntos:   # Fase 2 (30/09): dois setores -- a escada compara-se com H0_local = H0 (1+z*)^β
            partes["sh0es_local"] = ((p["H0_local"] - self.d1["sh0es_mean"]) / self.d1["sh0es_sigma"]) ** 2
        if "cc_moresco" in conjuntos:   # Fase 4 (30/09): os cronômetros com a lei acumulada
            r = self._r_cc(p, o)   # Fase 7 (01/10): pela covariância escolhida
            partes["cc_moresco"] = (r * r).sum(1)
        if "pantheon" in conjuntos:
            partes["pantheon"] = self.pantheon.chi2_prof(p["pantheon_mu"])
        if "pantheon_sh0es" in conjuntos:   # SH0ES (01/10)
            partes["pantheon_sh0es"] = self.pantheon_sh0es.chi2_prof(p["pantheon_sh0es_mu"])
        tot = sum(partes.values())
        if bool((p["dentro"] & ~torch.isfinite(tot)).any()):
            raise ValueError("chi2 não finito dentro do suporte instrumental")
        tot = torch.where(p["dentro"], tot, torch.full_like(tot, float("inf")))
        return tot, partes, p

    def residuos(self, theta, conjuntos, opcoes=None):
        """Resíduos BRANQUEADOS (B, n) na ordem planck_comp, desi_dr1, desi_dr2, sh0es, sh0es_local, cc_moresco, pantheon, pantheon_sh0es -- χ² = |r|²; +inf fora dos limites."""
        conjuntos = conjuntos_validos(conjuntos)
        o = validar_modelo_para_conjuntos(conjuntos, opcoes)
        p = self.predizer(theta, o)
        r = []
        if "planck_comp" in conjuntos:
            r.append(self._r_planck(p, o))
        if "desi_dr1" in conjuntos:
            r.append(self._r_dr1(p, o))
        if "desi_dr2" in conjuntos:
            r.append((p["dr2"] - self.dr2_val[None, :]) @ self.dr2_Linv.T)
        if "sh0es" in conjuntos:
            r.append(((p["H0"] - self.d1["sh0es_mean"]) / self.d1["sh0es_sigma"])[:, None])
        if "sh0es_local" in conjuntos:
            r.append(((p["H0_local"] - self.d1["sh0es_mean"]) / self.d1["sh0es_sigma"])[:, None])
        if "cc_moresco" in conjuntos:
            r.append(self._r_cc(p, o))
        if "pantheon" in conjuntos:
            r.append(self.pantheon.residuos_brancos(p["pantheon_mu"]))
        if "pantheon_sh0es" in conjuntos:
            r.append(self.pantheon_sh0es.residuos_brancos(p["pantheon_sh0es_mu"]))
        R = torch.cat(r, 1)
        if bool((~torch.isfinite(R[p["dentro"]])).any()):
            raise ValueError("resíduo não finito dentro do suporte instrumental")
        R[~p["dentro"]] = float("inf")
        return R, p

    def n_dados(self, conjuntos):
        conjuntos = conjuntos_validos(conjuntos)
        return sum({"planck_comp": 3, "desi_dr1": 12, "desi_dr2": 13, "sh0es": 1, "sh0es_local": 1, "cc_moresco": int(self.cc_z.shape[0]), "pantheon": self.pantheon.n, "pantheon_sh0es": self.pantheon_sh0es.n}[c] for c in conjuntos)
