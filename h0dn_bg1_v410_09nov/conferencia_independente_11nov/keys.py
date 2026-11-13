import numpy as np
B="C:/IALD/Central de Patentes/work/astra_bell_fock_tt_05nov/h0dn_bg1_06nov/"
for f in ["estimator_frozen.npz","network/network.npz"]:
    with np.load(B+f,allow_pickle=False) as d:
        print(f)
        for k in d.files:
            print("  ",k,d[k].shape,d[k].dtype)
