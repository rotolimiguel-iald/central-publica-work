import numpy as np
B = "C:/IALD/Central de Patentes/work/astra_bell_fock_tt_05nov/h0dn_bg1_06nov/"
with np.load(B + "network/network.npz", allow_pickle=False) as d:
    C = d["C"]; FA = d["factor_anchor"][:166]; FM = d["factor_MAS"][:166]; FH = d["factor_HMS"][:166]
Ch = C[:166, :166]
hms_full = FH @ FH.T
rem = Ch - FA @ FA.T - FM @ FM.T - hms_full   # o que sobra se o HMS entra INTEIRO (diag incluida)
dg = np.diag(rem); off = rem - np.diag(dg)
print("sobra diag apos tirar HMS inteiro: min=%.3e max=%.3e ; #|diag|<1e-15 = %d ; max|offdiag|=%.2e" % (dg.min(), dg.max(), int(np.sum(np.abs(dg) < 1e-15)), np.max(np.abs(off))))
mu2 = np.diag(Ch - FA @ FA.T - FM @ FM.T - (hms_full - np.diag(np.diag(hms_full))))
print("mu_error^2 - HMS_ii: min=%.3e ; #zero(<1e-15)=%d de 166" % ((mu2 - np.diag(hms_full)).min(), int(np.sum(np.abs(mu2 - np.diag(hms_full)) < 1e-15))))
