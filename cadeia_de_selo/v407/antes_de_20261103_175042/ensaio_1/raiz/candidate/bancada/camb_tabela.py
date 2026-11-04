# -*- coding: utf-8 -*-
"""camb_tabela.py -- a tabela do CAMB (ferramentas/gerar_tabela_camb.py, WSL, camb 2.0.4) interpolada na GPU.

Interpolação de Lagrange SEPARÁVEL de ordem k (4 = cúbica, 6 = quíntica) em grade uniforme (H0, ω_b, ω_c). O erro é MEDIDO contra os
pontos de teste do CAMB direto (fora da grade) antes de qualquer uso (`erro_no_teste`). Fora do interior da grade: NaN -- a Bancada
recusa o ponto (log-verossimilhança −∞ e contagem), nunca extrapola em silêncio.
"""
import json
import io
import os

import numpy as np
import torch

NOMES = ("z_star", "z_drag", "r_star", "r_drag", "DM_star")


class TabelaCAMB:
    def __init__(self, caminho_npz, dispositivo="cuda", ordem=6):
        from .fontes import read_checked, json_checked
        from .regua import inteiro
        self.caminho = caminho_npz
        man, manifest_sha = json_checked(caminho_npz.replace(".npz", ".json"))
        raw, h = read_checked(caminho_npz)
        if h != man["sha256"]:
            raise ValueError("tabela CAMB sha256 %s != manifesto %s" % (h, man["sha256"]))
        self.manifesto = man
        d = np.load(io.BytesIO(raw), allow_pickle=False)
        self.dev = torch.device(dispositivo)
        self.eixos = [d["grade_H0"], d["grade_ombh2"], d["grade_omch2"]]
        self.x0 = [float(e[0]) for e in self.eixos]
        self.h = [float(e[1] - e[0]) for e in self.eixos]
        self.n = [len(e) for e in self.eixos]
        self.V = torch.tensor(np.stack([d[k] for k in NOMES], -1), device=self.dev, dtype=torch.float64)   # (n1,n2,n3,5)
        self.teste_x = d["teste_pontos"]
        self.teste_y = np.stack([d["teste_" + k] for k in NOMES], -1)
        self.ordem = inteiro(ordem, "ordem", 2, min(self.n))
        for axis in self.eixos:
            if not np.all(np.isfinite(axis)) or not np.all(np.diff(axis) > 0) or not np.allclose(np.diff(axis), axis[1] - axis[0], rtol=1e-10, atol=1e-14):
                raise ValueError("grade CAMB não uniforme/finita")
        if not bool(torch.isfinite(self.V).all()) or not np.all(np.isfinite(self.teste_x)) or not np.all(np.isfinite(self.teste_y)):
            raise ValueError("tabela CAMB não finita")
        self.suporte = {name: (float(axis[1]), float(axis[-2])) for name, axis in zip(("H0", "ombh2", "omch2"), self.eixos)}
        self.proveniencia = dict(npz_sha256=h, manifesto_sha256=manifest_sha, suporte=self.suporte, extrapolacao=False)
        d.close()

    def _pesos(self, pos, n):
        k = self.ordem
        base = torch.floor(pos).long() - (k // 2 - 1)
        base = torch.clamp(base, 0, n - k)
        t = pos - base.to(pos.dtype)                        # posição relativa ao primeiro nó da janela
        nos = torch.arange(k, device=pos.device, dtype=pos.dtype)
        W = torch.ones(pos.shape[0], k, device=pos.device, dtype=pos.dtype)
        for j in range(k):
            for m in range(k):
                if m != j:
                    W[:, j] = W[:, j] * (t - nos[m]) / (nos[j] - nos[m])
        return base, W

    def __call__(self, H0, ombh2, omch2):
        """(B,) × 3 -> dict de (B,) com z*, z_drag, r*, r_drag, D_M(z*) de ΛCDM; NaN fora do interior da grade."""
        pts = [H0, ombh2, omch2]
        dentro = torch.ones_like(H0, dtype=torch.bool)
        bases, Ws = [], []
        for i in range(3):
            pos = (pts[i] - self.x0[i]) / self.h[i]
            dentro &= (pos >= 1.0) & (pos <= self.n[i] - 2.0)
            b, W = self._pesos(pos, self.n[i])
            bases.append(b); Ws.append(W)
        k = self.ordem
        ar = torch.arange(k, device=self.dev)
        i1 = (bases[0][:, None] + ar)[:, :, None, None]
        i2 = (bases[1][:, None] + ar)[:, None, :, None]
        i3 = (bases[2][:, None] + ar)[:, None, None, :]
        bloco = self.V[i1, i2, i3]                           # (B,k,k,k,5)
        w = Ws[0][:, :, None, None] * Ws[1][:, None, :, None] * Ws[2][:, None, None, :]
        out = (bloco * w[..., None]).sum((1, 2, 3))
        out[~dentro] = float("nan")
        return {n: out[:, j] for j, n in enumerate(NOMES)}, dentro

    def erro_no_teste(self):
        """Erro RELATIVO máximo e mediano da interpolação contra o CAMB direto, por grandeza."""
        x = torch.tensor(self.teste_x, device=self.dev, dtype=torch.float64)
        r, dentro = self(x[:, 0], x[:, 1], x[:, 2])
        y = torch.tensor(self.teste_y, device=self.dev, dtype=torch.float64)
        if not bool(dentro.any()):
            raise ValueError("nenhum ponto de validação CAMB dentro do suporte")
        res = {}
        for j, n in enumerate(NOMES):
            e = torch.abs(r[n][dentro] / y[dentro, j] - 1.0)
            res[n] = dict(max=float(e.max()), mediana=float(e.median()))
        res["n_teste"] = int(dentro.sum())
        res["ordem"] = self.ordem
        return res
