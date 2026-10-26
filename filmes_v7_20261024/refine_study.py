from pathlib import Path
import time

ROOT = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')

def write(p, text):
    raw = text.encode('utf-8')
    if p.exists():
        p.with_name(p.name + '.bak_' + str(time.time_ns())).write_bytes(p.read_bytes())
    q = p.with_name(p.name + '.tmp')
    q.write_bytes(raw)
    assert q.stat().st_size == len(raw)
    q.replace(p)

module = '''// Curves are sampled constructions from the sealed export, not physical time series.
export function studyCurve(F,S,key,progress){
 const p=Math.max(0,Math.min(1,progress));let local=p;
 if(key==='gravity'){const sub=Math.min(2,Math.floor(p*3));key=['transport','throat','spin'][sub];local=Math.min(1,p*3-sub);}
 let series=[],title='',statute='',labels=[],domain=null,axis='amostra';
 if(key==='mirror'&&F?.mirror){series=[F.mirror.refl,F.mirror.trans];domain=F.mirror.theta;axis='θ (rad)';labels=['reflexão','transmissão'];title='Repartição do peso · matriz S';statute='[DERIVED] Leitura angular; a face pertence ao regime hiperbólico.';}
 else if(key==='modular'&&F?.breuer){series=[F.breuer.density];domain=F.breuer.k;axis='κ';labels=['densidade'];title='Densidade do modo zero · perfil modular';statute='[DERIVED] Perfil de estado no parâmetro κ; não é densidade de massa medida nem uma série temporal.';}
 else if(key==='light'&&F?.light_J){const f=F.light_J;series=[f.Kx,f.JKJx];domain=f.d;axis='parâmetro';labels=['K · x','J K J · x'];title='Espelhamento do gerador · componentes';statute='[DERIVED] Componentes da construção numérica; o sinal se inverte sob J K J.';}
 else if(key==='sheet'&&S?.optical?.rows){series=[S.optical.rows.map(x=>x.area)];labels=['A/A₀'];title='Área óptica · construção de Jacobi';statute='[DERIVED] Concentração óptica com parâmetros INPUT; não é densidade de massa medida.';}
 else if(key==='transport'&&F?.solder?.path){series=[F.solder.path.map(x=>x[0]),F.solder.path.map(x=>x[1])];labels=['componente x','componente y'];title='Transporte na plaqueta · vetor transportado';statute='[DERIVED] Caminho numérico da fonte; a falta de fechamento deixa o defeito de holonomia.';}
 else if(key==='throat'&&F?.schwarzschild){series=[F.schwarzschild.rays_Et,F.schwarzschild.rays_Er];labels=['Eₜ','Eᵣ'];title='Schwarzschild · resíduos nas amostras';statute='[DERIVED] Exemplo estático esférico; o gráfico percorre amostras numéricas, não a formação temporal de um buraco negro.';}
 else if(key==='spin'&&F?.spin2){series=[F.spin2.h_plus,F.spin2.h_cross];domain=F.spin2.theta;axis='θ (rad)';labels=['h₊','h×'];title='Duas polarizações · ângulo dobrado';statute='[DERIVED] Representação sob hipóteses; a hélice desenhada é um diagrama [ONTO].';}
 else if(key==='identity'&&F?.identity){series=[F.identity.resid_true,F.identity.resid_false];labels=['membro verdadeiro','controle negativo'];title='Identidade · resíduos e controle';statute='[DERIVED] Amostras do teste numérico da fonte; não é uma medição da natureza.';}
 return {series,labels,title,statute,domain,axis,progress:local};
}
'''
write(ROOT/'web/study-curves.mjs',module)
p=ROOT/'web/filmes.mjs';text=p.read_text(encoding='utf-8')
text="import {studyCurve} from './study-curves.mjs';\n"+text
a=text.index(' const key=String(chapters[index]?.key');b=text.index(' series=series.filter',a)
text=text[:a]+" const selection=studyCurve(F,S,String(chapters[index]?.key??''),p);let {series,title,statute}=selection;p=selection.progress;\n"+text[b:]
text=text.replace("if(!series.length){$('#chartLabel').textContent='Curva não disponível nesta fonte.';$('#statute').textContent='Sem inferência de valores ausentes.';return;}","if(!series.length){ctx.fillStyle='#b6cbd2';ctx.font='22px Outfit';ctx.fillText('Examine os valores e as hipóteses deste capítulo abaixo.',50,150);$('#chart').setAttribute('aria-label','Este capítulo apresenta relações e valores; não há curva evolutiva.');$('#chartLabel').textContent='Relações e valores da fonte';$('#statute').textContent='A navegação muda o instante da apresentação; não acrescenta uma simulação física.';return;}")
old="$('#chart').setAttribute('aria-label',title+'; amostra sincronizada: '+sample);$('#chartLabel').textContent=title;$('#statute').textContent=statute;"
new="const at=Math.round(p*(series[0].length-1)),coordinate=selection.domain?.[at];const domain=Number.isFinite(coordinate)?`${selection.axis} = ${coordinate.toPrecision(5)}`:`amostra ${at+1}/${series[0].length}`;$('#chart').setAttribute('aria-label',title+'; '+domain+'; valores: '+sample);$('#chartLabel').textContent=title+' · '+selection.labels.join(' / ')+' · '+domain;$('#statute').textContent=statute;"
assert old in text;text=text.replace(old,new)
write(p,text)
print('Updated study curves; renderer sources unchanged.')
