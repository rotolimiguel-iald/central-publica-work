"""T3: estrutura da covariancia local C publicada (sem vetor observado)."""
import numpy as np
B = "C:/IALD/Central de Patentes/work/astra_bell_fock_tt_05nov/h0dn_bg1_06nov/"
with np.load(B + "network/network.npz", allow_pickle=False) as d:
    C = d["C"].copy(); FA = d["factor_anchor"].copy(); FM = d["factor_MAS"].copy(); FH = d["factor_HMS"].copy()
n = C.shape[0]; nh = 166
Ch = C[:nh, :nh]
anchor = FA[:nh] @ FA[:nh].T
mas = FM[:nh] @ FM[:nh].T
hms = FH[:nh] @ FH[:nh].T; hms_off = hms - np.diag(np.diag(hms))
res = Ch - anchor - mas - hms_off
off = res - np.diag(np.diag(res))
print("host block: residual apos tirar anchor+MAS+HMS(offdiag): max|offdiag| = %.3e ; diag min = %.4e max = %.4e ; #diag==0: %d ; #diag<0: %d" %
      (np.max(np.abs(off)), np.diag(res).min(), np.diag(res).max(), int(np.sum(np.diag(res) == 0)), int(np.sum(np.diag(res) < 0))))
print("  (diag residual = mu_error^2 de cada linha de host, unica contribuicao 'por linha')")
# fatores nao tocam fora do bloco host?
print("factor rows outside hosts nonzero: anchor %s MAS %s HMS %s" % (bool(np.any(FA[nh:])), bool(np.any(FM[nh:])), bool(np.any(FH[nh:]))))
# blocos fora do host: so diagonal?
R = C.copy(); R[:nh, :nh] = 0
print("fora do bloco host: max|offdiag| = %.3e ; #linhas com C_ii=0 (total) = %d ; #linhas diag>0 fora do host = %d de %d" %
      (np.max(np.abs(R - np.diag(np.diag(R)))), int(np.sum(np.diag(C) == 0)), int(np.sum(np.diag(R)[nh:] > 0)), n - nh))
# cruzado host x resto
print("cruzado host x nao-host: max|C| = %.3e" % np.max(np.abs(C[:nh, nh:])))
# bloco do G42 / 13 / HF
print("G42 (179:221) offdiag max %.3e; EXTRA13 (221:234) offdiag max %.3e; G42xHF(248) max %.3e; EXTRA13xHF max %.3e" % (
    np.max(np.abs(C[179:221, 179:221] - np.diag(np.diag(C[179:221, 179:221])))),
    np.max(np.abs(C[221:234, 221:234] - np.diag(np.diag(C[221:234, 221:234])))),
    np.max(np.abs(C[179:221, 248])), np.max(np.abs(C[221:234, 248]))))
# onde mora o posto deficiente: autovalores de C
w = np.linalg.eigvalsh(0.5 * (C + C.T)); tol = 1e-9 * w[-1]
print("rank(C)=%d nullity=%d ; linhas host com mu_error^2==0: %d" % (int(np.sum(w > tol)), int(np.sum(w <= tol)), int(np.sum(np.diag(res) == 0))))
