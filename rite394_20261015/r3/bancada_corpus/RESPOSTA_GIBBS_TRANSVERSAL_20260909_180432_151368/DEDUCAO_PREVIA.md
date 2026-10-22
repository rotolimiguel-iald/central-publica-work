# Dedução prévia — perturbação transversal local de Araki

[INPUT] Fixamos um sítio, 0<p<1, ρ₀=diag(p,1−p), W=σx e efeitos E±=(1±σx)/2 ANTES de escolher qualquer tensor T. W não comuta com ρ₀ se e somente se p≠1/2. O caso p=1/2 é o limite tracial e permanece definido.

[DERIVED] Escreva log ρ₀=aI+kσz, com a=(log p+log(1−p))/2 e k=(log p−log(1−p))/2. Para r=√(k²+s²), (kσz+sσx)²=r²I. A expansão da exponencial separada em potências pares/ímpares fornece
ρ_s=1/2[I+(tanh r/r)(kσz+sσx)].
O quociente sinh r/r é continuado em r=0 pelo valor 1. As probabilidades dos efeitos fixos são p±(s)=(1±m(s))/2, m(s)=s tanh r/r. Quando k=0, m(s)=tanh s; esta igualdade remove a singularidade aparente.

[DERIVED] Com χ=tanh(|k|)/|k| para k≠0 e χ(0)=1:
m(0)=0, m′(0)=χ, m″(0)=0;
p±(0)=1/2, p±′(0)=±χ/2, p±″(0)=0.
O Fisher clássico da medição na origem é χ². Shannon tem S(0)=ln 2, S′(0)=0, S″(0)=−χ². Seu coeficiente é −χ²/2. A composição s=velocity·t multiplica Fisher/coeficiente por velocity².

O normalizador físico dessa preparação é Z(s)=Tr exp(logρ₀+sσx)=cosh r/cosh k, com Z(0)=1. Então (log Z)′(0)=0 e (log Z)″(0)=χ. A suscetibilidade quântica χ não é o Fisher clássico χ². Para k≠0, 0<χ<1; no limite tracial χ=1.

[KNOWN + DERIVED — aplicação a justificar em nota final] A referência canônica é estado produto. Uma perturbação num único fator matricial modifica apenas esse fator: no produto finito logρ=soma dos logs e o potencial atua somente no sítio escolhido. A matriz resultante é ρ_s no sítio tensor a cauda original. A aplicação vetorial de Araki, que é única no cone natural, fornece a mesma preparação normal no fator; é preciso mostrar a identificação no objeto canônico por seus produtos locais e normalidade, e não só pelo nome “Gibbs”.

[REAL — APIs lidas] PauliProbabilityModel constrói probabilidades de uma órbita unitária com leitura Y; GibbsTilt faz tilt diagonal por score modular. Nenhum é a perturbação Gibbs transversal acima. Reutilizaremos signOutcome e os tipos DiagonalStateCurve/diagonalFisher, e o limite relativo já provado. A nova folha escalar terá definição efetiva global da curva e derivará regularidade e jets sem receber resposta ou T como campo.

[OPEN/INPUT] Observáveis/direção e relação com espaço-tempo foram fixados como protocolo, não deduzidos de gravitação. Fisher não será chamado tensor de matéria. A lei de área e conservação ficam com a composição da raiz. Não se mede custo de colapso, Meia-Nat ou custo energético nesta conta. Nenhum original ou um.py será executado/modificado.
