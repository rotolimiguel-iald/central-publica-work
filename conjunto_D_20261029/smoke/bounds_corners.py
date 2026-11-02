import sys,json,itertools
sys.dont_write_bytecode=True
import lal, lalsimulation as ls
out=[]
fmin=20.0
for (m1,m2) in [(15,10),(15,15),(40,20),(100,10),(100,100)]:
    for (c1,c2) in [(0.99,0.99),(-0.99,-0.99),(0.0,0.0)]:
        for dt in (-0.8,0.0,2.0):
            M1,M2=m1*lal.MSUN_SI,m2*lal.MSUN_SI
            ins=ls.SimInspiralChirpTimeBound(fmin,M1,M2,c1,c2)
            mer=ls.SimInspiralMergeTimeBound(M1,M2)
            sp=ls.SimInspiralFinalBlackHoleSpinBound(c1,c2)
            tail=ls.SimInspiralRingdownTimeBound(M1+M2,sp)*max(1.,1+dt)
            out.append(dict(m1=m1,m2=m2,c1=c1,c2=c2,dtau=dt,inspiral=ins,merger=mer,tail=tail,pre_needed=ins+mer+0.022+0.2,post_needed=tail+0.022+0.2))
worst_pre=max(out,key=lambda r:r['pre_needed']); worst_post=max(out,key=lambda r:r['post_needed'])
print('worst pre',worst_pre); print('worst post',worst_post)
for r in out:
    if r['dtau']==0.0 and r['c1']==r['c2']: print(r['m1'],r['m2'],r['c1'],'pre=%.2f post=%.2f'%(r['pre_needed'],r['post_needed']))
