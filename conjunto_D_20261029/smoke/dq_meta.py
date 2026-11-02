import sys,json,glob,os
sys.dont_write_bytecode=True
import h5py,numpy as np
base='/mnt/c/IALD/Bancada_Um/fontes_externas/gwosc_o4/hdf5/'
man=json.load(open('/mnt/c/IALD/Bancada_Um/fontes_externas/gwosc_o4/GWOSC_O4_32S_V1.manifest.json'))
ev=["GW230919_215712","GW240513_183302","GW240920_073424","GW240923_204006","GW241111_111552","GW241130_034908","GW241210_060606","GW250104_015122","GW250109_010541","GW250118_170523"]
# GPS from the 32 s NPZ window centre (t0 + 16) is metadata; also the cataloged GPS from the proposal (read-only)
prop=json.load(open('/mnt/c/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/PROPOSTA_MANIFESTO_METADATA_D.json'))
print('PROPOSTA keys',list(prop.keys())[:20])
out={}
first=True
for e in ev:
    for s in [x for x in man['series'] if x['event']==e]:
        p=s['hdf5'].replace('/mnt/c/','/mnt/c/')
        with h5py.File(p,'r') as h:
            gps=float(h['meta/GPSstart'][()]); dur=float(h['meta/Duration'][()])
            dqn=[x.decode() if isinstance(x,bytes) else str(x) for x in h['quality/simple/DQShortnames'][()]]
            inn=[x.decode() if isinstance(x,bytes) else str(x) for x in h['quality/injections/InjShortnames'][()]]
            dq=h['quality/simple/DQmask'][()]; inj=h['quality/injections/Injmask'][()]
            fs=1/float(h['strain/Strain'].attrs['Xspacing'])
            if first: print('DQ names',dqn); print('INJ names',inn); first=False
            out[e+'_'+s['det']]=dict(file=os.path.basename(p),GPSstart=gps,Duration=dur,fs=fs,n_dq=len(dq),
                 evt_t0_npz=s['t0'],evt_gps_est=s['t0']+16.0,evt_offset_in_file=s['t0']+16.0-gps,dqnames=dqn,injnames=inn)
            # fraction of seconds in 32 s window around the event satisfying CBC_CAT1..3 + DATA and no injection flags
            req=[n for n in ('DATA','CBC_CAT1','CBC_CAT2','CBC_CAT3') if n in dqn]
            m=sum(1<<dqn.index(n) for n in req)
            okdq=((dq&m)==m)
            minj=sum(1<<inn.index(n) for n in inn if n.startswith('NO_'))
            okinj=((inj&minj)==minj)
            ok=okdq&okinj
            i0=int(s['t0']-gps); i1=i0+32
            out[e+'_'+s['det']].update(req_dq=req,frac_ok_window32=float(ok[i0:i1].mean()),
                 frac_ok_whole_file=float(ok.mean()),
                 longest_ok_run_before_event_s=None)
            # longest contiguous OK run ending before event-? s
            run=0;best=0;pre=ok[:max(0,int(s['t0']+16.0-gps)-8)]
            for v in pre:
                run=run+1 if v else 0; best=max(best,run)
            out[e+'_'+s['det']]['longest_ok_run_before_event_s']=best
            # first >=? s block start (like strain_io.offsource_psd with 512 s?) -> first run length
            fr=0
            for v in pre:
                if v: fr+=1
                else: break
            out[e+'_'+s['det']]['first_ok_run_from_file_start_s']=fr
for k,v in out.items():
    print(k,v['file'][:40],'off_in_file=%.1f'%v['evt_offset_in_file'],'win32_ok=%.2f'%v['frac_ok_window32'],'file_ok=%.2f'%v['frac_ok_whole_file'],'longest_pre=%d'%v['longest_ok_run_before_event_s'])
json.dump(out,open('/mnt/c/IALD/Central de Patentes/work/conjunto_D_20261029/smoke/dq_meta_D.json','w'),indent=1)
