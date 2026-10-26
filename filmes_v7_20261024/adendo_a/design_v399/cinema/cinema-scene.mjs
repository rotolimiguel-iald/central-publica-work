import * as THREE from "../web/vendor/three.module.js";
import {EffectComposer} from "../web/vendor/addons/postprocessing/EffectComposer.js";
import {RenderPass} from "../web/vendor/addons/postprocessing/RenderPass.js";
import {UnrealBloomPass} from "../web/vendor/addons/postprocessing/UnrealBloomPass.js";
import {BokehPass} from "../web/vendor/addons/postprocessing/BokehPass.js";
import {ShaderPass} from "../web/vendor/addons/postprocessing/ShaderPass.js";
import {OutputPass} from "../web/vendor/addons/postprocessing/OutputPass.js";
import {clamp,mix,ramp,gate,randomGenerator,glowTexture,surfaceTexture,cloudTexture,CameraShutterPass,FinishShader,makeSurface,updateSurface} from "./render-support.mjs";
export function sceneState(phase,data,{closingCollapse=null}={}){
 const p=clamp(phase,0,180),ret=ramp(p,162,180),focus=ramp(p,86,123),rows=data.optical.rows,x=focus*(rows.length-1),i=Math.floor(x),j=Math.min(i+1,rows.length-1);
 const collapse=closingCollapse===null?ret:clamp(closingCollapse),sample=mix(rows[i].area,rows[j].area,x-i),area=mix(sample,1,ret),depth=5.4*(1-area)/(1-rows.at(-1).area);
 return {phase:p,ret,collapse,focus,area,concentration:1/area,depth,twist:depth*.42,
 radius:mix(6.2,6.4,ramp(p,5,36))*(1-.985*collapse),sheet:ramp(p,58,82)*(1-collapse),face:1-ramp(p,62,84),
 split:ramp(p,6,28)*1.10,flow:ramp(p,29,44)*(1-ret),spin:gate(p,124,130,150,156),
 cut:gate(p,87,109,158,169),under:gate(p,115,119,124,132),horizon:gate(p,143,149,160,174),beta:data.alpha*Math.sqrt(Math.E)};
}
const rayVertex=`
uniform float uPhase,uRadius,uDepth,uTwist,uFlow,uSpin,uTime;
attribute float aU,aSeed,aSide;varying float vU,vSeed;varying vec3 vNormal;
const float PI=3.141592653589793;
vec3 path(float u,float seed){
 float radial=pow(1.-u,.82),r=mix(.12,uRadius,radial),a=seed*2.3999632297+uTwist*pow(u,1.3);
 float h=-uDepth*exp(-r*r/5.2)+.08;
 h+=uSpin*.10*sin(a*2.-uTime*2.)*exp(-((r-3.4)/1.9)*((r-3.4)/1.9));
 if(seed<.5){r=mix(.65,uRadius,abs(u*2.-1.));a+=u>.5?-.40*(u-.5):0.;h=-uDepth*exp(-r*r/5.2)+.15+(u>.5?sin((u-.5)*PI)*.35:0.);}
 return vec3(r*cos(a),h,r*sin(a));
}
void main(){
 vec3 p=path(aU,aSeed),t=normalize(path(min(.99999,aU+.001),aSeed)-path(max(.00001,aU-.001),aSeed));
 vec3 n=normalize(cross(t,vec3(0.,1.,0.))),b=normalize(cross(t,n));vec3 normal=cos(aSide)*n+sin(aSide)*b;
 p+=normal*.014*(.4+.6*uFlow);vNormal=normalMatrix*normal;vU=aU;vSeed=aSeed;gl_Position=projectionMatrix*modelViewMatrix*vec4(p,1.);
}`;
const rayFragment=`uniform float uTime,uFlow;varying float vU,vSeed;varying vec3 vNormal;
void main(){
 float phase=fract(vU*4.-uTime/(6.28318530718)*2.+vSeed*.137),pulse=pow(max(0.,1.-abs(phase-.5)*2.),20.);
 vec3 c=vSeed<.5?vec3(1.0,.48,.08):vec3(.05,.66,.80);
 float light=.42+.45*abs(dot(normalize(vNormal),normalize(vec3(.5,.7,1.))))+pulse*1.7;
 gl_FragColor=vec4(c*light,uFlow*(.28+.66*pulse));
 #include <tonemapping_fragment>
 #include <colorspace_fragment>
}`;
function rayGeometry(count){
 const segments=100,sides=5,positions=[],us=[],seeds=[],angles=[],indices=[];
 for(let k=0;k<count;k++)for(let i=0;i<=segments;i++)for(let j=0;j<sides;j++){
  const n=(k*(segments+1)+i)*sides+j;positions.push(0,0,0);us.push(i/segments);seeds.push(k);angles.push(j/sides*Math.PI*2);
  if(i<segments){const b=(k*(segments+1)+i)*sides+(j+1)%sides;indices.push(n,n+sides,b,b,n+sides,b+sides);}
 }
 const g=new THREE.BufferGeometry();g.setAttribute("position",new THREE.Float32BufferAttribute(positions,3));g.setAttribute("aU",new THREE.Float32BufferAttribute(us,1));g.setAttribute("aSeed",new THREE.Float32BufferAttribute(seeds,1));g.setAttribute("aSide",new THREE.Float32BufferAttribute(angles,1));g.setIndex(indices);return g;
}
export class CinemaScene{
 constructor(canvas,data,{background=false}={}){
  this.canvas=canvas;this.data=data;this.background=background;this.width=1920;this.height=1080;this.quality=1;this.lastTime=null;this.pointer=[0,0];
  this.renderer=new THREE.WebGLRenderer({canvas,alpha:true,antialias:true,preserveDrawingBuffer:true,powerPreference:"high-performance"});
  this.renderer.setClearColor(0x03070e,1);this.renderer.toneMapping=THREE.ACESFilmicToneMapping;this.renderer.toneMappingExposure=1.06;this.renderer.outputColorSpace=THREE.SRGBColorSpace;
  this.renderer.shadowMap.enabled=true;this.renderer.shadowMap.type=THREE.PCFShadowMap;
  this.scene=new THREE.Scene();this.camera=new THREE.PerspectiveCamera(38,16/9,.1,180);
  this.model=new THREE.Group();this.sky=new THREE.Group();this.scene.add(this.sky,this.model);this.textures=[];
  const envScene=new THREE.Scene();envScene.background=new THREE.Color("#23303a");
  for(let k=0;k<4;k++){const box=new THREE.Mesh(new THREE.PlaneGeometry(10,14),new THREE.MeshBasicMaterial({color:k%2?0x647987:0xcfad80,side:THREE.DoubleSide}));box.position.set(Math.cos(k*1.57)*16,6,Math.sin(k*1.57)*16);box.lookAt(0,0,0);envScene.add(box);}
  const pmrem=new THREE.PMREMGenerator(this.renderer);this.environment=pmrem.fromScene(envScene,.09,.1,100);this.scene.environment=this.environment.texture;pmrem.dispose();envScene.traverse(o=>{o.geometry?.dispose();o.material?.dispose();});
  const rng=randomGenerator();
  for(let layer=0;layer<3;layer++){
   const positions=[],colors=[];
   for(let k=0;k<800;k++){const a=rng()*Math.PI*2,z=rng()*2-1,r=45+layer*28+rng()*16,c=Math.sqrt(1-z*z);positions.push(r*c*Math.cos(a),r*z,r*c*Math.sin(a));const h=rng();colors.push(.42+h*.4,.54+h*.3,.72+h*.25);}
   const g=new THREE.BufferGeometry();g.setAttribute("position",new THREE.Float32BufferAttribute(positions,3));g.setAttribute("color",new THREE.Float32BufferAttribute(colors,3));
   const stars=new THREE.Points(g,new THREE.PointsMaterial({size:.09+layer*.025,vertexColors:true,transparent:true,opacity:.74,sizeAttenuation:true,depthWrite:false}));this.sky.add(stars);
  }
  const cloud=cloudTexture();this.textures.push(cloud);
  for(let k=0;k<14;k++){const c=new THREE.Sprite(new THREE.SpriteMaterial({map:cloud,transparent:true,opacity:.105,blending:THREE.AdditiveBlending,depthWrite:false}));c.position.set((rng()-.5)*75,(rng()-.5)*40,-28-rng()*50);c.scale.set(22+rng()*30,12+rng()*24,1);c.material.rotation=rng()*6.28;this.sky.add(c);}
  this.scene.add(new THREE.HemisphereLight(0x98bfcc,0x6c4228,1.55));
  const key=new THREE.DirectionalLight(0xbde8f4,3.2);key.position.set(-7,12,6);key.castShadow=true;key.shadow.mapSize.set(2048,2048);Object.assign(key.shadow.camera,{left:-10,right:10,top:10,bottom:-10,near:.5,far:45});key.shadow.bias=-.0004;key.shadow.normalBias=.025;key.shadow.radius=3;this.scene.add(key);
  const rim=new THREE.DirectionalLight(0xf6ba77,2.1);rim.position.set(5,-4,-9);this.scene.add(rim);
  const warm=new THREE.PointLight(0xffbd6d,15,18,2);this.scene.add(warm);this.warm=warm;
  const texture=surfaceTexture();this.textures.push(texture);
  this.material=new THREE.MeshPhysicalMaterial({color:0x437581,metalness:.52,roughness:.31,clearcoat:.68,clearcoatRoughness:.23,sheen:.15,sheenColor:0xa7cfce,side:THREE.DoubleSide,bumpMap:texture,bumpScale:.045,envMapIntensity:1.1,transparent:true});
  this.material.onBeforeCompile=shader=>{shader.fragmentShader=shader.fragmentShader.replace("#include <color_fragment>","#include <color_fragment>\nif(!gl_FrontFacing)diffuseColor.rgb*=vec3(1.32,.89,.65);");};
  this.sheet=new THREE.Mesh(makeSurface(),this.material);this.sheet.castShadow=true;this.sheet.receiveShadow=true;this.model.add(this.sheet);
  this.faces=[];
  for(const sign of [-1,1]){
   const mat=new THREE.MeshPhysicalMaterial({color:sign>0?0x3a6e7b:0x9e7747,metalness:.42,roughness:.32,clearcoat:.5,bumpMap:texture,bumpScale:.035,transparent:true});
   const face=new THREE.Mesh(new THREE.SphereGeometry(1,96,32),mat);face.castShadow=true;face.receiveShadow=true;this.model.add(face);this.faces.push({face,sign});
  }
  this.core=new THREE.Mesh(new THREE.SphereGeometry(.15,48,32),new THREE.MeshBasicMaterial({color:0xffe5aa}));this.model.add(this.core);
  const glow=glowTexture();this.textures.push(glow);this.coreGlow=new THREE.Sprite(new THREE.SpriteMaterial({map:glow,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false}));this.model.add(this.coreGlow);
  this.beam=new THREE.Mesh(new THREE.CylinderGeometry(.16,.38,5,40,1,true),new THREE.ShaderMaterial({transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,side:THREE.DoubleSide,uniforms:{strength:{value:0}},vertexShader:"varying vec2 vUv;void main(){vUv=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}",fragmentShader:"varying vec2 vUv;uniform float strength;void main(){float edge=pow(sin(vUv.y*3.14159265),1.2);gl_FragColor=vec4(1.,.63,.24,edge*strength*.08);}"}));this.model.add(this.beam);
  this.count=Math.round(1/(data.alpha*Math.sqrt(Math.E)));this.uniforms={};for(const name of ["Phase","Radius","Depth","Twist","Flow","Spin","Time"])this.uniforms["u"+name]={value:0};
  this.rays=new THREE.Mesh(rayGeometry(this.count),new THREE.ShaderMaterial({uniforms:this.uniforms,vertexShader:rayVertex,fragmentShader:rayFragment,transparent:true,depthWrite:false}));this.rays.frustumCulled=false;this.rays.renderOrder=3;this.model.add(this.rays);
  this.horizon=new THREE.Mesh(new THREE.TorusGeometry(3.9,.023,12,180),new THREE.MeshBasicMaterial({color:0xd9b56d,transparent:true}));this.horizon.rotation.x=Math.PI/2;this.model.add(this.horizon);
  const rt=new THREE.WebGLRenderTarget(1,1,{type:THREE.HalfFloatType,samples:4});this.composer=new EffectComposer(this.renderer,rt);this.composer.addPass(new RenderPass(this.scene,this.camera));
  this.hdrLimit=new ShaderPass({uniforms:{tDiffuse:{value:null}},vertexShader:"varying vec2 vUv;void main(){vUv=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}",fragmentShader:"uniform sampler2D tDiffuse;varying vec2 vUv;void main(){vec4 c=texture2D(tDiffuse,vUv);if(!(c.r>=0.))c.r=0.;if(!(c.g>=0.))c.g=0.;if(!(c.b>=0.))c.b=0.;gl_FragColor=vec4(clamp(c.rgb,vec3(0.),vec3(16.)),1.);}"});this.composer.addPass(this.hdrLimit);
  this.bloom=new UnrealBloomPass(new THREE.Vector2(1,1),.28,.42,1.03);this.composer.addPass(this.bloom);
  this.bokeh=new BokehPass(this.scene,this.camera,{focus:24,aperture:.000015,maxblur:.006});this.composer.addPass(this.bokeh);
  this.shutter=new CameraShutterPass(.12);this.composer.addPass(this.shutter);
  this.finish=new ShaderPass(FinishShader);this.composer.addPass(this.finish);this.composer.addPass(new OutputPass());
  this.maskTarget=new THREE.WebGLRenderTarget(480,270);this.maskMaterial=new THREE.MeshBasicMaterial({color:0xffffff,side:THREE.DoubleSide});this.maskPixels=new Uint8Array(480*270*4);
  this.resize(1920,1080,1);
 }
 resize(width,height,quality=1){
  this.width=width;this.height=height;this.quality=quality;this.renderer.setPixelRatio(quality);this.renderer.setSize(width,height,false);this.composer.setPixelRatio(quality);this.composer.setSize(width,height);this.camera.aspect=width/height;this.camera.updateProjectionMatrix();
 }
 setPointer(x,y){this.pointer=[clamp(x,-1,1),clamp(y,-1,1)];}
 render(phase,time=phase,{loop=false,jProgress=null,closingCollapse=null}={}){
  const s=this.state=sceneState(phase,this.data,{closingCollapse}),angle=loop?time/24*Math.PI*2:time*.32;
  if(this.lastTime===null||Math.abs(time-this.lastTime)>.08)this.shutter.reset();this.lastTime=time;
  this.sheet.visible=s.sheet>.002;this.material.opacity=s.sheet;updateSurface(this.sheet.geometry,s,angle);
  this.faces.forEach(({face,sign})=>{face.visible=s.face>.002;face.scale.set(s.radius,.10+s.radius*.025,s.radius);face.position.y=sign*Math.max(.012,s.split*s.face);face.material.opacity=s.face;});
  const j=jProgress===null?gate(phase,54,57,68,72):Math.sin(Math.PI*clamp(jProgress));
  this.core.position.set(0,-s.depth+.13,0);
  if(j>.01)this.core.position.y=Math.cos((jProgress===null?(phase-54)/18:jProgress)*Math.PI*2)*s.split;
  this.coreGlow.position.copy(this.core.position);this.coreGlow.scale.setScalar(1.25+.3*s.focus);this.coreGlow.material.opacity=.8;
  this.warm.position.copy(this.core.position);this.warm.position.y+=.4;
  this.beam.material.uniforms.strength.value=j;this.beam.position.y=-s.depth*.45;this.beam.scale.y=.6+s.depth*.16;
  for(const key of ["Phase","Radius","Depth","Twist","Flow","Spin"])this.uniforms["u"+key].value=s[key[0].toLowerCase()+key.slice(1)];this.uniforms.uTime.value=angle;
  this.rays.visible=s.flow>.002;this.horizon.visible=s.horizon>.002;this.horizon.material.opacity=s.horizon*.85;this.horizon.position.y=-s.depth*Math.exp(-3.9*3.9/5.2)+.14;
  const azimuth=.65+.075*Math.sin(loop?angle:angle*.25)+this.pointer[0]*.035,elevation=mix(.52,-.09,s.under)+this.pointer[1]*.018;
  const fitRadius=Math.max(3.5,s.radius),distance=fitRadius/(Math.tan(this.camera.fov*Math.PI/360)*this.camera.aspect*.76);
  const target=new THREE.Vector3(0,-s.depth*.35,0);
  this.camera.position.set(Math.sin(azimuth)*Math.cos(elevation)*distance,Math.sin(elevation)*distance+target.y,Math.cos(azimuth)*Math.cos(elevation)*distance);
  this.camera.lookAt(target);this.camera.updateMatrixWorld();this.bokeh.uniforms.focus.value=distance;
  this.sky.rotation.y=loop?.003*Math.sin(angle):.0004*time;
  this.finish.uniforms.time.value=loop?Math.floor((time%24)*24):Math.floor(time*24);this.finish.uniforms.grain.value=loop?.006:.016;
  this.composer.render();
  this.canvas.dataset.phase=phase.toFixed(4);this.canvas.dataset.coreY=this.core.position.y.toFixed(4);this.canvas.dataset.cameraY=this.camera.position.y.toFixed(4);this.canvas.dataset.rays=String(this.count);
  return s;
 }
 measureCoverage(){
  const oldOverride=this.scene.overrideMaterial,oldBackground=this.scene.background,color=this.renderer.getClearColor(new THREE.Color()),alpha=this.renderer.getClearAlpha();
  const visible=[this.sky.visible,this.rays.visible,this.coreGlow.visible,this.beam.visible,this.horizon.visible];this.sky.visible=this.rays.visible=this.coreGlow.visible=this.beam.visible=this.horizon.visible=false;
  this.scene.overrideMaterial=this.maskMaterial;this.scene.background=null;this.renderer.setClearColor(0x000000,1);this.renderer.setRenderTarget(this.maskTarget);this.renderer.clear();this.renderer.render(this.scene,this.camera);this.renderer.readRenderTargetPixels(this.maskTarget,0,0,480,270,this.maskPixels);
  let left=480,right=-1,top=270,bottom=-1,count=0;
  for(let y=0;y<270;y++)for(let x=0;x<480;x++){const at=(y*480+x)*4;if(this.maskPixels[at]>80){left=Math.min(left,x);right=Math.max(right,x);top=Math.min(top,y);bottom=Math.max(bottom,y);count++;}}
  this.scene.overrideMaterial=oldOverride;this.scene.background=oldBackground;[this.sky.visible,this.rays.visible,this.coreGlow.visible,this.beam.visible,this.horizon.visible]=visible;this.renderer.setClearColor(color,alpha);this.renderer.setRenderTarget(null);
  return {width_fraction:right>=left?(right-left+1)/480:0,pixel_bounds:[left,top,right,bottom],pixels:count,mask_size:[480,270],transition:this.state.collapse>0};
 }
 destroy(){
  this.scene.traverse(o=>{o.geometry?.dispose();if(o.material)for(const m of Array.isArray(o.material)?o.material:[o.material])m.dispose();});
  for(const t of this.textures)t.dispose();this.environment.dispose();this.maskTarget.dispose();this.maskMaterial.dispose();this.bokeh.dispose();this.shutter.dispose();this.composer.dispose();this.renderer.dispose();
 }
}
