import * as THREE from "../web/vendor/three.module.js";
import {Pass,FullScreenQuad} from "../web/vendor/addons/postprocessing/Pass.js";
export const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
export const smooth=x=>{x=clamp(x);return x*x*x*(x*(x*6-15)+10);};
export const ramp=(t,a,b)=>smooth((t-a)/(b-a));
export const mix=(a,b,p)=>a+(b-a)*p;
export const gate=(t,a,b,c,d)=>ramp(t,a,b)*(1-ramp(t,c,d));
export function randomGenerator(seed=71973){let state=seed;return()=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return state/4294967296;};}
export function glowTexture(){
 const c=document.createElement("canvas");c.width=c.height=128;const x=c.getContext("2d"),g=x.createRadialGradient(64,64,0,64,64,64);
 g.addColorStop(0,"rgba(255,244,210,1)");g.addColorStop(.06,"rgba(255,231,173,.9)");g.addColorStop(.22,"rgba(255,196,107,.25)");g.addColorStop(1,"rgba(255,156,70,0)");
 x.fillStyle=g;x.fillRect(0,0,128,128);return new THREE.CanvasTexture(c);
}
export function surfaceTexture(){
 const c=document.createElement("canvas");c.width=c.height=512;const x=c.getContext("2d"),im=x.createImageData(512,512),rng=randomGenerator(41137);
 for(let y=0;y<512;y++)for(let i=0;i<512;i++){
  const at=(y*512+i)*4,grain=(rng()-.5)*48,lines=6*Math.sin(i*.42+3*Math.sin(y*.026))+5*Math.cos(y*.23);
  const v=clamp(130+grain+lines,0,255);im.data[at]=im.data[at+1]=im.data[at+2]=v;im.data[at+3]=255;
 }
 x.putImageData(im,0,0);const t=new THREE.CanvasTexture(c);t.wrapS=t.wrapT=THREE.RepeatWrapping;t.repeat.set(9,5);t.anisotropy=8;return t;
}
export function cloudTexture(){
 const c=document.createElement("canvas");c.width=c.height=256;const x=c.getContext("2d"),im=x.createImageData(256,256);
 for(let y=0;y<256;y++)for(let i=0;i<256;i++){
  const px=(i-128)/128,py=(y-128)/128,r=px*px+py*py;
  const v=clamp((Math.sin(px*7+Math.sin(py*5))*Math.cos(py*8-px*3)*.25+.5)*Math.exp(-r*3.7),0,1);
  const at=(y*256+i)*4;im.data[at]=85;im.data[at+1]=130;im.data[at+2]=158;im.data[at+3]=v*85;
 }
 x.putImageData(im,0,0);return new THREE.CanvasTexture(c);
}
export class CameraShutterPass extends Pass{
 constructor(amount=.14){
  super();this.amount=amount;this.valid=false;
  const params={type:THREE.HalfFloatType,depthBuffer:false};this.history=new THREE.WebGLRenderTarget(1,1,params);this.next=new THREE.WebGLRenderTarget(1,1,params);
  this.material=new THREE.ShaderMaterial({uniforms:{current:{value:null},previous:{value:null},amount:{value:0}},vertexShader:"varying vec2 vUv;void main(){vUv=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}",fragmentShader:"uniform sampler2D current,previous;uniform float amount;varying vec2 vUv;void main(){gl_FragColor=mix(texture2D(current,vUv),texture2D(previous,vUv),amount);}"});
  this.copy=new THREE.ShaderMaterial({uniforms:{image:{value:null}},vertexShader:this.material.vertexShader,fragmentShader:"uniform sampler2D image;varying vec2 vUv;void main(){gl_FragColor=texture2D(image,vUv);}"});
  this.quad=new FullScreenQuad(this.material);this.copyQuad=new FullScreenQuad(this.copy);
 }
 reset(){this.valid=false;}
 setSize(w,h){this.history.setSize(w,h);this.next.setSize(w,h);this.reset();}
 render(renderer,write,read){
  this.material.uniforms.current.value=read.texture;this.material.uniforms.previous.value=this.history.texture;this.material.uniforms.amount.value=this.valid?this.amount:0;
  renderer.setRenderTarget(this.next);this.quad.render(renderer);
  this.copy.uniforms.image.value=this.next.texture;renderer.setRenderTarget(this.renderToScreen?null:write);this.copyQuad.render(renderer);
  const t=this.history;this.history=this.next;this.next=t;this.valid=true;
 }
 dispose(){this.history.dispose();this.next.dispose();this.material.dispose();this.copy.dispose();this.quad.dispose();this.copyQuad.dispose();}
}
export const FinishShader={
 uniforms:{tDiffuse:{value:null},time:{value:0},grain:{value:.016},vignette:{value:.18}},
 vertexShader:"varying vec2 vUv;void main(){vUv=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}",
 fragmentShader:`uniform sampler2D tDiffuse;uniform float time,grain,vignette;varying vec2 vUv;
 float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7))+time*17.73)*43758.5453);}
 void main(){vec3 col=texture2D(tDiffuse,vUv).rgb;float lum=dot(col,vec3(.2126,.7152,.0722));
 float noise=hash(gl_FragCoord.xy)-.5;col+=noise*grain*(.24+sqrt(max(0.,lum)));
 vec2 q=(vUv-.5)*vec2(1.,.9);col*=1.-vignette*smoothstep(.2,.64,length(q));
 col*=vec3(1.015,1.004,.988);gl_FragColor=vec4(max(col,vec3(0.)),1.);}`
};
export function makeSurface(radial=104,angular=144){
 const position=new Float32Array((radial+1)*(angular+1)*3),normal=new Float32Array(position.length),uv=new Float32Array((radial+1)*(angular+1)*2),indices=[];
 for(let j=0;j<=radial;j++)for(let k=0;k<=angular;k++){
  const n=j*(angular+1)+k;uv[n*2]=j/radial;uv[n*2+1]=k/angular;
  if(j<radial&&k<angular){const a=n,b=n+1,c=n+angular+1,d=c+1;indices.push(a,b,c,b,d,c);}
 }
 const g=new THREE.BufferGeometry();g.setAttribute("position",new THREE.BufferAttribute(position,3));g.setAttribute("normal",new THREE.BufferAttribute(normal,3));g.setAttribute("uv",new THREE.BufferAttribute(uv,2));g.setIndex(indices);
 g.userData={radial,angular};return g;
}
export function updateSurface(g,s,angle){
 const {radial,angular}=g.userData,p=g.attributes.position.array,n=g.attributes.normal.array;
 const cosPhase=Math.cos(angle*2),sinPhase=Math.sin(angle*2),cut=s.cut*1.55,origin=.88+cut/2;
 for(let j=0;j<=radial;j++){
  const v=j/radial,r=.12+v*(s.radius-.12),base=Math.exp(-r*r/5.2),wave=Math.exp(-(((r-3.4)/1.9)**2));
  for(let k=0;k<=angular;k++){
   const a=origin+k/angular*(Math.PI*2-cut)+s.twist*base*.28,ca=Math.cos(a),sa=Math.sin(a);
   const harmonic=Math.sin(a*2)*cosPhase-Math.cos(a*2)*sinPhase;
   const height=-s.depth*base+s.spin*.10*wave*harmonic,index=(j*(angular+1)+k)*3;
   p[index]=r*ca;p[index+1]=height;p[index+2]=r*sa;
   const slope=s.depth*base*2*r/5.2,len=Math.sqrt(1+slope*slope);
   n[index]=-slope*ca/len;n[index+1]=1/len;n[index+2]=-slope*sa/len;
  }
 }
 g.attributes.position.needsUpdate=true;g.attributes.normal.needsUpdate=true;g.computeBoundingSphere();
}
