import numpy as np
B="C:/IALD/Central de Patentes/work/astra_bell_fock_tt_05nov/h0dn_bg1_06nov/"
with np.load(B+"network/network.npz",allow_pickle=False) as d:
    rn=d["row_names"]; c=d["c_cepheid"]; C=d["C"]; A=d["A"]; pn=d["param_names"]
print(len(rn))
# summarize contiguous runs of identical description
runs=[]; s=0
for i in range(1,len(rn)+1):
    if i==len(rn) or rn[i]!=rn[s]:
        runs.append((s,i-1,rn[s])); s=i
for r in runs: print(r)
print("params tail:", list(pn[-12:]), "h_index idx name:", pn[int(d['h_index']) if False else 0])
