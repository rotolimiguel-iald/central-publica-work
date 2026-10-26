from pathlib import Path
import json,os,datetime,re
R=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um');V=R/'delivery_v7'
def save(p,data):
 if isinstance(data,str):data=data.encode('utf-8')
 if p.exists():p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')).write_bytes(p.read_bytes())
 t=p.with_name(p.name+'.tmp');t.write_bytes(data);assert t.stat().st_size==len(data)>0;os.replace(t,p)
keys1=['one','boundary','mirror','modular','light','gravity','horizon','identity','nature']
keys2=['one','boundary','mirror','light','sheet','transport','throat','spin','einstein','identity']
names1=['O Um','A fronteira','O espelho','A face hiperbólica','A luz atravessa','A gravidade se forma','Einstein no horizonte','A identidade permanece','A natureza decide']
names2=['O Um','A fronteira se abre','O espelho e a projeção','A luz J atravessa','As faces tornam-se lençol','O transporte deixa curvatura','A garganta e o horizonte','Duas polarizações','Einstein no horizonte','O Um permanece']
metrics1=[['omega_I'],['half','S_boundary','sqrt_e'],['beta','theta_M','tau_trans'],['powers_ratio','breuer_gap','zero_mode_weight'],['J_cross','J_inv'],['R_rec','sch_Et','pol'],['einstein','flags','proof_ladder_clean'],['id_true'],['z_disc','p_disc','threshold_sigma']]
metrics2=[['omega_I'],['half','S_boundary','sqrt_e'],['beta','theta_M','breuer_gap'],['J_cross','J_inv','J_id'],['wigner','KK'],['R_rec','plaq'],['sch_Et','sch_Er'],['hel','pol'],['einstein','proof_ladder_clean','flags'],['id_true','z_disc','p_disc','threshold_sigma']]
for film,keys,names,metrics,step in [(1,keys1,names1,metrics1,16),(2,keys2,names2,metrics2,24)]:
 chapters=[{'key':key,'title':title,'start':i*step,'end':(i+1)*step,'metrics':metrics[i]} for i,(key,title) in enumerate(zip(keys,names))]
 d={'film':film,'total_seconds':len(keys)*step,'duration':len(keys)*step,'scenes':chapters,'chapters':chapters}
 save(V/f'data/film{film}.json',json.dumps(d,ensure_ascii=False,indent=2))
# Module-relative imports, including all vendor dependencies.
for p in (V/'web/vendor').rglob('*.js'):
 s=p.read_text(encoding='utf-8');target=os.path.relpath(V/'web/vendor/three.module.js',p.parent).replace('\\','/')
 if not target.startswith('.'):target='./'+target
 changed=re.sub(r'''(from\s*|import\s*)(['"])three\2''',lambda m:m.group(1)+m.group(2)+target+m.group(2),s)
 if changed!=s:save(p,changed)
save(V/'cinema/timeline.mjs', '''import {clamp,smooth} from './render-support.mjs';
export async function loadProduction(){
 const get=async n=>{let r=await fetch(new URL('../data/'+n,import.meta.url));if(!r.ok)throw Error('Source absent: '+n);return r.json();};
 const [H,F,S,T1,T2]=await Promise.all(['hud.json','frames.json','scene.json','film1.json','film2.json'].map(get));
 const V=Object.fromEntries(H.items.map(x=>[x.id,x]));if(H.seal_pin.slice(0,16)!==V.um_sha16.text)throw Error('NOT_SEALED');return {H,F,S,T1,T2,V};
}
const ranges1=[[0,18],[18,36],[36,54],[54,63],[63,82],[82,143],[143,162],[162,174],[174,180]];
const ranges2=[[0,18],[18,36],[36,54],[54,72],[72,90],[90,108],[108,126],[126,144],[144,162],[162,180]];
const en1=['The One','The self-conjugate boundary','The mirror reads','The hyperbolic face','Light crosses','Gravity takes form','Einstein at the horizon','Identity remains','Nature decides'];
const en2=['The One','The boundary opens','The mirror and the face','Light crosses the mirror','Two faces become geometry','Transport leaves curvature','Inside the throat','Two polarizations','Einstein at the horizon','The One remains'];
const formulas1=['ω(I) = 1','x = 1 − x  ⇒  ½  →  S∂  →  √e','β = α√e  →  θM = asin √β  →  S(θ)','σt · hyperbolic face / compact reading','J² = I   ·   JKJ = −K','[K₁,K₂] = −J₃   →   R = 2c₁c₂','δQ = κ δA / (8πG)   ·   H1 ∧ H2 ∧ H3','1 = 1','The calibrated test / nature decides'];
const formulas2=['ω(I) = 1','x = 1 − x  ⇒  ½  →  S∂ = ½ nat','β = α√e   ·   |R|² = β   ·   |T|² = 1 − β','J² = I   ·   JKJ = −K','[K₁,K₂] = −J₃','R = 2c₁c₂   ·   holonomy','Schwarzschild · static example','h₊ , h×   ·   θ → 2θ','δQ = κ δA / (8πG)   →   Einstein','1 = 1   ·   nature decides'];
export function shotState(film,time,d){
 const chs=film===1?d.T1.scenes:d.T2.chapters,total=film===1?d.T1.total_seconds:d.T2.duration;
 let index=chs.findIndex(c=>time<c.end);if(index<0)index=chs.length-1;
 const ch=chs[index],local=clamp(time-ch.start,0,ch.end-ch.start),p=local/(ch.end-ch.start),range=(film===1?ranges1:ranges2)[index];
 return {film,time,total,index,key:ch.key,local,p,phase:range[0]+(range[1]-range[0])*smooth(p),jProgress:((film===1&&index===4)||(film===2&&index===3))?p:0,start:ch.start,end:ch.end,title:(film===1?en1:en2)[index],formula:(film===1?formulas1:formulas2)[index],metrics:ch.metrics.map(id=>d.V[id]),closing:index===chs.length-1,transition:time<2||time>total-3};
}
export function panelData(s,d){
 const {F,S}=d;
 if(['gravity','transport','throat'].includes(s.key))return {title:'OPTICAL AREA',axis:'A / A₀ · declared Jacobi example',rows:[{color:'#70cfdb',values:S.optical.rows.map(x=>x.area)}]};
 if(s.key==='spin')return {title:'SPIN TWO',axis:'two transverse modes · θ → 2θ',rows:[{color:'#70cfdb',values:F.spin2.h_plus},{color:'#e9bd7c',values:F.spin2.h_cross}]};
 if(s.key==='mirror')return {title:'SCATTERING WEIGHTS',axis:'|R|² + |T|² = 1',rows:[{color:'#e9bd7c',values:F.mirror.refl},{color:'#70cfdb',values:F.mirror.trans}]};
 return {title:'MODULAR DENSITY',axis:'¼ sech²(κ/2) · state density',rows:[{color:'#70cfdb',values:F.breuer.density}]};
}
''')
print('TIMELINES_AND_VENDOR_READY')
