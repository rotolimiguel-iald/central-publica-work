import time, a_lib
t=time.time(); f=a_lib.Fonte(a_lib.CAND,"cand"); print(len(f.idx), "%.1fs"%(time.time()-t))
for n in ["_V411_H0DN_INSUMOS","_V411_H0DN_CONTRACT","h0dn_bg1_v411","v411_h0dn_mechanics","_V411_FONTES","_V411_VERBATINS2","_V411_SPECS","_V411_TOPO","_V411_H0DN_TEXT","veredito_h0dn","_V410_H0DN_INSUMOS","_V410_H0DN_CONTRACT","_v398_beta","_v392_guarda_texto","_v410_guarda_frases","_v410_h0dn_vigia_arquivos","main"]:
    print(n, f.idx.get(n))
