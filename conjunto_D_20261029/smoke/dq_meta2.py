import sys,json,os
sys.dont_write_bytecode=True
import h5py,numpy as np
man=json.load(open('/mnt/c/IALD/Bancada_Um/fontes_externas/gwosc_o4/GWOSC_O4_32S_V1.manifest.json'))
ev=["GW230919_215712","GW240513_183302","GW240920_073424","GW240923_204006","GW241111_111552","GW241130_034908","GW241210_060606","GW250104_015122","GW250109_010541","GW250118_170523"]
REQ_DQ=['DATA','CBC_CAT1','CBC_CAT2','CBC_CAT3']; REQ_INJ=['NO_CBC_HW_INJ','NO_BURST_HW_INJ','NO_DETCHAR_HW_INJ']
res={}
for e in ev:
    for s in [x for x in man['series'] if x['event']==e]:
        with h5py.File(s['hdf5'],'r') as h:
            gps=float(h['meta/GPSstart'][()])
            dqn=[x.decode() if isinstance(x,bytes) else str(x) for x in h['quality/simple/DQShortnames'][()]]
            inn=[x.decode() if isinstance(x,bytes) else str(x) for x in h['quality/injections/InjShortnames'][()]]
            dq=h['quality/simple/DQmask'][()]; inj=h['quality/injections/Injmask'][()]
        i0=int(s['t0']-gps); i1=i0+32
        flagfrac={n:float(((dq>>dqn.index(n))&1).mean()) for n in dqn}
        flagfrac.update({n:float(((inj>>inn.index(n))&1).mean()) for n in inn})
        m1=sum(1<<dqn.index(n) for n in REQ_DQ); m2=sum(1<<inn.index(n) for n in REQ_INJ)
        ok=((dq&m1)==m1)&((inj&m2)==m2)
        ev_idx=int(s['t0']+16.0-gps)
        pre=ok[:max(0,ev_idx-8)]
        run=0;best=0;bests=0
        for k,v in enumerate(pre):
            run=run+1 if v else 0
            if run>best: best=run; bests=k-run+1
        res[e+'_'+s['det']]=dict(win32_ok=float(ok[i0:i1].mean()),file_ok=float(ok.mean()),longest_ok_run_before_event_s=int(best),longest_run_start_idx=int(bests),event_idx=ev_idx,flag_fractions_file={k:round(v,4) for k,v in flagfrac.items() if v<0.9999})
        r=res[e+'_'+s['det']]
        print(e+'_'+s['det'],'win32=%.2f file=%.3f longest_pre=%d ev_idx=%d'%(r['win32_ok'],r['file_ok'],r['longest_ok_run_before_event_s'],ev_idx),r['flag_fractions_file'])
json.dump(res,open('/mnt/c/IALD/Central de Patentes/work/conjunto_D_20261029/smoke/dq_meta_D_v2.json','w'),indent=1)
