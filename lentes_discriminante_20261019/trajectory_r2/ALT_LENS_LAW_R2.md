# Lei alternativa de lentes — complemento R2

[REAL documental] /root/r69_locality_bridge. Unidade F8.LENTES_5SIGMA_20261019, claim1009; mesma referência própria/revisão2. Continuação de leitura dirigida, sem novos cálculos, execução do programa, dados ou alterações canônicas.

## Distância ANGULAR explicitamente escrita, encontrada

Em `tgl_paper_unified.py:3401–3404`, angular_diameter_distance(z,H0,Om0,beta) retorna D_C(z)/(1+z). Não é inferência nossa a partir de distância de luminosidade: o consumidor angular está escrito.
D_C é a integral de c/H_TGL em3374–3385. H_TGL_arr:3358–3371 usa o fundo plano com radiação: H_LCDM=H0 sqrt[Om0(1+z)^3+Or0(1+z)^4+OL0], multiplicado por sqrt[1+response(w,beta)], com w=(rho_r/3−rho_L)/rho_tot. A variante escalar:3335–3344 contém a mesma estrutura. O docstring da família e a errata imediatamente subsequente identificam response=beta|1+w|.
[DERIVED de leitura] É uma lei de distância cosmológica distinta do acoplamento fotônico q RicciFF. Não contém correção local do potencial de Fermat, slip ou deflexão adicional. O intervalo lente-fonte não está implementado nessa função de um redshift: um consumidor precisa usar a mesma geometria plana para os dois extremos, sem colar o fator endpoint da leitura D1b.
Essa implementação pertence ao fundo local H_LCDM sqrt[1+beta|1+w|]. NÃO é automaticamente a leitura acumulada A(z)=K*/k(z) examinada pela ORDEM018. Não misturar parametrização H0/Om0 dessa função com os valores efetivos de outro motor, sobretudo a normalização emz=0. Este complemento apenas recupera a fonte; não fixa qual fundo do teste empírico deve governar nem apresenta amplitude discriminante.

## Massa e G local: correção explícita já existente

`um.py:155651–155674`,155725–155745 e221143–221158 preserva e retira a lei antiga M=2beta²(c²/4πG)R. A auditoria explica que ela confundia coeficiente de reflexão com amplitude de fonte; implicava velocidade circular universal e falhava fora da faixa de aglomerados.
A leitura vigente é M_TGL^linear=M_RG, CONDICIONAL à Face C linear (P1)–(P4)+T1; beta não renormaliza G local. Não há autorização documental para multiplicar massa de lente porbeta ou acrescentar G_eff=G(1+beta) por analogia.
O Atlas:2289–2291 remete ao crescimento stealth/G_eff cancelando a expansão; esse resumo não é um fechamento de duas equações para potenciais de lente Phi/Psi. Nas fontes e padrões consultados não localizei uma lei de slip ou relação massa dinâmica/massa de lente com coeficiente TGL fixo que suplante a correção linear acima.

## Homônimo que não serve como potencial de lente

Custo:14485–14500 contém energia de membrana E=integral[kappa/2(grad z)²−tau z], equação−kappa laplaciano z=tau e solução logarítmica de profundidade. O próprio texto define z como coordenada perpendicular da dobra de fronteira. Não há nesse trecho identificação de z com potencial gravitacional fraco Phi/Psi ou potencial de Fermat; usar o logaritmo como lei de atraso seria uma identificação nova.

## Cobertura e resultado

Buscas focais por slip, G_eff/G_{eff}, Phi/Psi, massa dinâmica/lente, angular distance e Poisson nos três artigos (Custo/Ponte/um.py) e remissões Atlas; complemento nos dois TeX indexados de acoplamento/luz. Fontes gigantes incorporadas/base64 de um.py não foram descompactadas nesta busca. Uma consulta de globPowerShell falhou por sintaxe; repetida com rg -g no diretório de lotes, sem sucesso oculto. Nenhum corpus amplo reextraído.
Resultado: uma lei ANGULAR de fundo realmente existe e foi recuperada. Para massa/potencial local, a correção explícita é stealth linear, não uma nova amplitude beta. Falta, neste recorte, uma previsão extra de slip/lente que permaneça distinguível após os parâmetros de fundo/massa já admitidos; isso não é uma declaração sobre todo o acervo.
