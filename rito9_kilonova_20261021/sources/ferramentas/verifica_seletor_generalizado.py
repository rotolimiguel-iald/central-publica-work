#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verificacao numerica do lema do seletor generalizado (rito 9, Elo 1), 21/10/2026, membro Kimi.

Lema: para B = Z (carga de setor) e A simetrico [[a,b],[b,c]],
    [A, alpha_theta(Z)] = 0  <=>  tan(2 theta) = 2b / (c - a)  <=>  theta = -phi_A (mod 90 graus),
onde phi_A e o angulo proprio de A. alpha_theta(Z) = R(theta) Z R(theta)^T com R da familia de Miguel.
Grade de 0,1 grau; residuos de grade <= 2e-3, exatos ~1e-16 nos pontos finos.
"""
import numpy as np

BETA = 0.012031300400803142  # beta runtime do contrato B4-v394 (referencia; aqui so define theta_M)
TH_M = np.arcsin(np.sqrt(BETA))


def R(t):
    return np.array([[np.cos(t), np.sin(t)], [-np.sin(t), np.cos(t)]])


Z = np.array([[1.0, 0.0], [0.0, -1.0]])


def comm_norm(A, t):
    Bt = R(t) @ Z @ R(t).T
    return np.linalg.norm(A @ Bt - Bt @ A)


def predicted(A):
    a, b, c = A[0, 0], A[0, 1], A[1, 1]
    return 0.5 * np.arctan2(2 * b, c - a)


GRID = np.linspace(0.001, np.pi / 2 - 0.001, 899)


def first_zero(A):
    vals = [comm_norm(A, t) for t in GRID]
    i = int(np.argmin(vals))
    return GRID[i], vals[i]


def projetor(phi):
    v = np.array([np.cos(phi), np.sin(phi)])
    return np.outer(v, v)


if __name__ == "__main__":
    print(f"beta={BETA:.15f}  theta_M={np.degrees(TH_M):.4f} deg")
    casos = [
        ("par da pedra A=X (espera pi/4)", np.array([[0.0, 1.0], [1.0, 0.0]])),
        ("projetor em theta_M (espera 90-theta_M)", projetor(TH_M)),
        ("projetor em 20 graus (espera 70)", projetor(np.radians(20))),
        ("A arbitrario [[0.3,0.7],[0.7,1.9]]", np.array([[0.3, 0.7], [0.7, 1.9]])),
        ("projetor em pi/4 (ponto fixo)", projetor(np.pi / 4)),
    ]
    for nome, A in casos:
        z, res = first_zero(A)
        print(f"{nome}: zero={np.degrees(z):.4f} deg | lema prediz {np.degrees(predicted(A)):.4f} | residuo {res:.2e}")
