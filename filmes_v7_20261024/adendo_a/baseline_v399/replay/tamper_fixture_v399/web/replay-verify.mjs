export async function sha256(bytes) {
 const hash=await crypto.subtle.digest('SHA-256',bytes);
 return Array.from(new Uint8Array(hash),b=>b.toString(16).padStart(2,'0')).join('');
}
export async function verifyBytes(bytes,expected,label) {
 if(typeof expected!=='string'||!/^[0-9a-f]{64}$/.test(expected)||await sha256(bytes)!==expected)
  throw new Error(`NOT_SEALED: integridade de ${label}`);
 return bytes;
}
export function compareAnchors(values,anchors,hud,manifest) {
 if(!Array.isArray(anchors)||anchors.length!==manifest.anchor_count||anchors.length<20) throw new Error('NOT_SEALED: conjunto de âncoras');
 const seen=new Set(), rows=[];
 function row(key,expected,tol,kind) {
  const actual=values[key],finite=n=>typeof n==='number'&&Number.isFinite(n);
  const valid=finite(expected)&&finite(actual)&&finite(tol)&&tol>=0;
  const residual=valid?Math.abs(actual-expected):null;
  rows.push({key,expected,actual:finite(actual)?actual:null,residual,atol:tol,kind,ok:valid&&residual<=tol});
 }
 for(const a of anchors) {
  if(seen.has(a.key))throw new Error('NOT_SEALED: âncora duplicada');seen.add(a.key);row(a.key,a.value,a.atol,'core');
 }
 if(!hud||!Array.isArray(hud.items))throw new Error('NOT_SEALED: HUD ausente');
 for(const m of manifest.hud_compared) {
  const matches=hud.items.filter(x=>x.id===m.id&&x.key===m.key),a=anchors.find(x=>x.key===m.key);
  if(matches.length!==1||!a)throw new Error('NOT_SEALED: âncora HUD ausente/duplicada');
  row(m.key,matches[0].value,a.atol,'hud');
 }
 return {status:rows.every(x=>x.ok)?'OK':'NOT_SEALED',rows};
}
