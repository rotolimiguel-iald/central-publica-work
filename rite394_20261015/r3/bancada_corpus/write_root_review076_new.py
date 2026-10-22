from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os
ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT=ROOT/'REVISOES_RAIZ_076_20260910'
assert not OUT.exists()
OUT.mkdir()
pins=[]
def pin(p):
    b=p.read_bytes()
    r={'path':p.as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    pins.append(r)
    return r
def new(p,text):
    assert p.resolve().is_relative_to(ROOT) and not p.exists()
    b=text.encode('utf-8')
    temp=p.with_name(p.name+'.tmp_'+datetime.now().strftime('%H%M%S_%f'))
    with temp.open('xb') as f:
        f.write(b)
        f.flush()
        os.fsync(f.fileno())
    assert temp.read_bytes()==b
    temp.rename(p)
    assert p.read_bytes()==b
    return pin(p)

sources=["MODULOS_BRST_EBAR_076_20260910/MODULOS_H3_H4_E_SETOR_CALCULADO.md","MODULOS_BRST_EBAR_076_20260910/LEVANTAMENTO_BRST_CORRENTES_KILLING_076.md","REVISAO_MODULOS_EBAR_076_20260910_024011_189592/PARECER_MODULOS_EBAR_076.md","REVISAO_CORRENTES_KILLING_076_20260910_024518_164234/PARECER_CORRENTES_KILLING_076.md"]
text="# Revisão da raiz: setor K, homotopia do alvo e correntes076\n\n10/09/2026. [DERIVED — revisão escrita]. Li integralmente a nota de módulos, o adendo de correntes e os dois pareceres de Herschel. Parecer favorável aos enunciados delimitados, sem promover a lista de representantes a uma classificação dos módulos completos.\n\nNo setor K, aplicar b_N à derivada de Lie equivale à derivada covariante de B0 em cada fator. Incluem-se pesos de densidade. A conexão cancela nas contrações escalares; C_N aniquila c não derivado e os demais fatores. As partes KT e seus prolongamentos não contêm ghosts. O parecer independente explicita também o antifield do ghost c*, que é covetor densidade e possui transporte de Lie mais o termo de Noether sem ghosts. Portanto E_N=C_N=0 está demonstrado nesse setor; não se estende por nome a ∇̄c.\n\nA família A_L=ρ_L c⁰c¹c²c³ é s-fechada pelo cancelamento da divergência e pela ausência de cinco ghosts não derivados independentes. Isso constrói ciclos; não afirma classes não nulas.\n\nA homotopia do volume do alvo usa F_u=Exp_(φ0)(utξ), V_u=sF_u e W_u=∂uF_u. Cartan dá ∂u[Ω(V,V,V)/6]=s[Ω(W,V,V)/2]. A extremidade u=0 desaparece porque sφ0=0, mesmo quando d_Hφ0≠0. Assim τ3=sK2 na classe formal declarada. O termo inicial K2=t³Ω(φ0)ξ(s_tξ)²/6 tem a normalização correta. A avaliação ξ=0 não é mapa de complexos para o BRST ativo; não apaga seu derivado.\n\nA construção é intrínseca sobre φ0*TS³, natural e finita em jatos por coeficiente. Não define uma primitiva global de de Rham do volume de S³. O fator topológico global GL⁺4 e os polinômios CE de Lorentz também não são identificados automaticamente com classes formais. A condição de classe e a curvatura no diferencial permanecem necessárias.\n\nPara as correntes de Killing, conferi diretamente ∂μ𝒥_X^μ=−𝔈_iX^i, com 𝔈_i=−cσ√|g| h_ij τ^j. A derivada de Euler e o antifield são densitizados uma única vez. Com η=c⁰c¹c²c³ e η_μ=∂_Lη/∂c^μ, as identidades\ns(𝒥^μη_μ)=(∂μ𝒥^μ)η e s[(φ*·X)η]=(𝔈·X)η\nproduzem sα_X=0 para α_X=𝒥^μη_μ+(φ*·X)η. O segundo sinal é positivo na convenção efetiva sφ*=+𝔈+Lie_cφ*. Os dois sinais ímpares, na variação de φ*X e na multiplicação por η, são necessários.\n\nA escrita ambiente usa P_A=φ_i*h^{ij}∂jY_A tangente, com Y·P=0; não acrescenta um quarto antifield livre. Os seis geradores AB são campos de Killing globais e as expressões formam o módulo Λ²R⁴ do alvo. Cada componente não é, por si, um escalar O(4) invariante. Também não se provou dim H³=6.\n\nA precisão Rees do parecer independente é consumida: a expansão deve transportar antifields pelo lift cotangente completo, φ*=tA_t^-T ξ*, além de φ=Exp_(φ0)(tξ). A identidade s_t(α∘Ψ_t)=0 vale para a série inteira. O termo de corrente pode começar em t³ e o de antifield em t⁵; graus distintos não impedem que a série pertença à mesma completação. Isso não faz cada coeficiente isolado um ciclo de s_t.\n\n[OPEN] A geração e as relações de H³/H⁴, os dois canais de Ebar_N, a primitiva admissível da anomalia e a carga/QME não foram concluídas. A nova transgressão característica da raiz tem sua revisão própria pendente; não é aprovada por este parecer. Zero CAS/Lean e nenhuma fonte alterada.\n"
for rel in sources:
    pin(ROOT/rel)
new(OUT/'PARECER_SETOR_E_CORRENTES_076.md',text)
for r in pins:
    b=Path(r['path']).read_bytes()
    assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
new(OUT/'REGISTRO_REVISAO_SETOR_076.json',json.dumps({
 'status':'FAVORABLE_LIMITED_WRITTEN_REVIEW',
 'created_utc':datetime.now(timezone.utc).isoformat(),'files':list(pins),
 'sources_stable':True,'originals_written':False,'new_lean_compilations':0,'new_cas_controls':0
},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(pins,ensure_ascii=True))

