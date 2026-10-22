# Adjunto máximo e S†S no GNS do ideal finito

[REAL — compilação Lean DEV; revisão da integração ainda pendente]

O pacote preserva H_I=ScalarGNSHilbert P e o operador S fechado construído
do gráfico {(Λ(A),Λ(A*)) : A∈I∩I*}. São sete módulos e 53 declarações
novas auditadas. Nenhuma foi somada aos números da integração anterior.

O domínio do adjunto antilinear é exatamente o conjunto dos y para os
quais existe z com <Sx,y>=<z,x> para todo x∈D(S). A densidade de D(S)
garante unicidade. O gráfico do adjunto é a interseção das igualdades
contínuas desse pareamento, logo fechado. A regra de escala é conjugada.

A densidade de D(S†) não é postulada. O adjunto limitado T* do transporte
gaussiano produz T*BΩg∈D(S†), com valor T*B*Ωg, para B∈ρ(N)'. A órbita
do comutante é densa e T é injetivo. Por ortogonalidade, isso força
D(S†) denso em H_I. Não se inverte T, não se muda o peso nem o ideal.
A involução S²=I permite provar (S†)²=I no domínio invariante do adjunto.

O operador composto A=S†S é complexo-linear, com domínio exatamente
{x∈D(S):Sx∈D(S†)}. Seu pareamento é
<Ax,y>=<Sy,Sx>, daí <x,Ax>=||Sx||² na parte real e simetria.

Para auto-adjunticidade, usa-se a projeção de (z,0) sobre o gráfico
REAL fechado de S em WithLp 2 (H_I×H_I). A equação variacional real,
testada também em iu, produz <Su,Sx>=<z−x,u> para todo u∈D(S).
A maximalidade do adjunto dá Sx∈D(S†) e S†Sx=z−x. Portanto I+A é
sobrejetivo. Positividade e essa sobrejetividade dão D(A) denso;
simetria e o adjunto máximo da Mathlib eliminam qualquer extensão
própria e provam A*=A. O núcleo de A é trivial porque S é involutivo.

Essas provas não pressupõem D(S)=H_I, operador S limitado, inversa
gaussiana limitada, nem que o gráfico antilinear seja complexo-linear
com escala idêntica nas duas coordenadas. O gráfico de S é lido como
submódulo REAL no produto de Hilbert; a composição A é complexo-linear.

[OPEN] Núcleo trivial NÃO é gap espectral. A raiz positiva, a decomposição
polar no mesmo H_I e sua identificação como dados modulares do peso ν
continuam pendentes. Não se afirma I=n_ν. Ainda faltam a ponte de domínio
ou núcleo necessária à identificação do peso, KMS, o traço canônico
fiel normal semifinito e sua escala dual. Three Locks/H1, H2/H3, o setor
quântico interagente e o certificado completo consumido pelo gate
permanecem abertos. A auto-adjunticidade aqui não altera essas flags.

O um.py original e a cópia integrada anterior não foram executados
nem modificados durante a construção DEV. Logs de todas as tentativas
falhas permanecem em logs/; só as compilações rc0 e suas fontes/binários
coincidentes são aceitas no manifesto associado.
