import sys,h5py,json
sys.dont_write_bytecode=True
base='/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/'
res={}
for d,lab,nlive,ncall in [('E3_PSEOB_PILOT_V2_S220','GW250114_PILOT_V2_S220',512,3000506),('E3_PSEOB_PILOT_V2_S220_C1','GW250114_PILOT_V2_S220_C1',512,5739196)]:
    p=base+d+'/'+lab+'_result.hdf5'
    with h5py.File(p,'r') as h:
        keys=list(h.keys())
        ns=h['nested_samples']
        ks=list(ns.keys())
        n=len(ns['log_likelihood'][()]) if 'log_likelihood' in ns else None
        ll=ns['log_likelihood'][()]
        res[lab]=dict(keys=keys[:12],nested_cols_n=len(ks),n_nested=int(n),max_lnL=float(ll.max()),min_lnL=float(ll.min()))
        # niter ~ n_nested - nlive (live points added at end are included only if add_live) -> report both
        res[lab]['calls_per_iter_if_add_live']=ncall/max(1,(n-nlive))
        res[lab]['calls_per_iter_if_no_live']=ncall/max(1,n)
print(json.dumps(res,indent=1))
