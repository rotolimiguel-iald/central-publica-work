"""Identidades ALGEBRICAS do modelo otico ja existente (F1.ATRATOR: S unitaria com |R|^2 = beta; populacoes T = |S|^2),
recalculadas com beta em runtime (lido de BETA_RUNTIME.json, que leu os bytes do um.py). Nao e teste, nao e pre-registro,
nao abre dado: so explicita o que a familia ja contem para a trilha TEMPO (Liouville x dissipacao). Sem numpy (2x2 explicito).
Uso: python -I identidades_oticas.py <BETA_RUNTIME.json> <saida.json>"""
import json
import math
import sys


def det2(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def sv2(m):
    # valores singulares de 2x2 real: raizes dos autovalores de M^T M
    a = m[0][0] ** 2 + m[1][0] ** 2
    b = m[0][0] * m[0][1] + m[1][0] * m[1][1]
    d = m[0][1] ** 2 + m[1][1] ** 2
    tr, de = a + d, a * d - b * b
    disc = math.sqrt(max(tr * tr / 4 - de, 0.0))
    return [math.sqrt(tr / 2 + disc), math.sqrt(max(tr / 2 - disc, 0.0))]


def main(bfile, out):
    b = json.load(open(bfile, encoding="utf-8"))
    beta = b["beta_runtime"]
    c, s = math.sqrt(1 - beta), math.sqrt(beta)
    S = [[c, s], [-s, c]]                                  # S(theta_M), theta_M = arcsin sqrt(beta)
    T = [[S[i][j] ** 2 for j in range(2)] for i in range(2)]  # populacoes do canal dephased D Ad(S) D
    lam = 1 - 2 * beta
    a = -math.log(lam) / 2
    n_beta = 1 / beta
    d = dict(beta_runtime=beta, fonte_beta=b["um_py_sha256"][:16] + " l." + str(b["linha_alpha"]),
             S=S, det_S=det2(S), valores_singulares_S=sv2(S),
             leitura_S="S unitaria: det = 1 e valores singulares 1 -- nada se perde, nada pousa (face 'Liouville' do canal) [DERIVED]",
             T=T, det_T=det2(T), lambda_1_menos_2beta=lam, det_T_menos_lambda=det2(T) - lam,
             valores_singulares_T=sv2(T),
             taxa_hiperbolica_a=a, a_menos_beta=a - beta,
             leitura_T="T = |S|^2 estocastica dupla: det T = 1 - 2 beta < 1 -- o 'volume' populacional contrai por travessia (face dissipativa) [DERIVED]",
             contracao_apos_1_sobre_beta_travessias=lam ** n_beta, referencia_e_menos_2=math.exp(-2.0),
             nota="identidades algebricas da familia ja construida na F1.ATRATOR (RELATORIO_F1_ATRATOR_R1.md: T = R + lambda(I-R), lambda = 1-2beta, a = -log(lambda)/2); nao sao teste nem evidencia")
    with open(out, "w", encoding="utf-8") as fo:
        json.dump(d, fo, ensure_ascii=False, indent=1)
    print(json.dumps(d, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
