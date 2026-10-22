# Revisão independente051 — Riccati e controles

[REAL — revisão matemática por leitura e evidência de desenvolvimento; NÃO é selo do lote final]
Emissão UTC: 2026-09-07T03:52:19.301987+00:00

Revisor: agente /root/relative_operator_domains (Newton). A autoria própria do revisor nesta rodada é OpticalVolterraBalance; esta nota não constitui aprovação independente desse módulo. O objeto independente aqui são OpticalRiccatiInvariant e OpticalBalanceControls. Nenhuma fonte ou derivação foi alterada na revisão.

| Fonte efetivamente revista | Bytes | SHA256 medido |
|---|---:|---|
| OpticalRiccatiInvariant.lean | 5504 | 0367a7b0be381cba2012fe28a4229bca36287d09097a94cb94aa7f393d87b526 |
| OpticalBalanceControls.lean | 4697 | f985882ca1a5bec8de2d281a2a3d82ea504fec3c5072b26d0019bdf85ed5a909 |

## Conferência matemática

1. A matriz B=[[x,z],[z,y]] é simétrica. As três equações de opticalRiccatiSystem são exatamente as três componentes independentes de B′=−B²−Rmat para Rmat simétrica. A soma das duas diagonais dá θ′=−(rxx+ryy)−F, com θ=x+y e F=x²+2z²+y². A componente rxy não entra no traço; isso não é hipótese suprimida.

2. A convenção do fonte é opticalShearNormSq=((x−y)/2)²+z², metade da norma quadrática do tensor sem traço. Logo F=θ²/2+2*opticalShearNormSq, com sinal e fator2 corretos. A grandeza shearNorm=2(...) da derivação prévia corresponde a 2*opticalShearNormSq; não deve ser identificada diretamente com o nome Lean sem esse fator.

3. As entradas rotacionadas são precisamente OBOᵀ para O=[[c,s],[-s,c]], c²+s²=1. Os lemas preservam traço, F e a parcela de cisalhamento. Eles não afirmam covariância de toda a equação dinâmica sob bases móveis arbitrárias: nessa extensão apareceriam termos da derivada da base. Tampouco selecionam uma normalização de área.

4. optical_matrix_constant_balance obtém a continuidade de x,z,y das derivadas do sistema, constrói F contínuo e aplica o teorema de Volterra. O traço Ricci constante r, a lei de A, a lei de Q e os dados iniciais continuam hipóteses explícitas. O lema não é uma reconstrução matricial para Ricci variável sem novas hipóteses; essa generalidade é conservada no balanço escalar principal do outro módulo.

5. Para R(t)=r+vt, a primitiva r*t+v*t²/2 e o drift −v*t²/2 estão corretos. O drift é estritamente negativo para v>0 e t≠0, e positivo para v<0. Esse sinal pontual não determina sozinho o sinal do termo integrado no passado, pois a integral exterior também é orientada.

6. A positividade de E usa A≥0 e F≥0. A identidade finita regular inclui as condições de continuidade e integrabilidade correspondentes. Isoladamente, o lema de sinal permite funções não integráveis e usa a integral totalizada do Lean; ele não autoriza interpretação física através de cáusticas.

7. A orientação térmica está correta: de Q−T*eta*(At−A0)=T*eta*E e T≠0 segue eta*(A0−At)=−Q/T+eta*E. Não é assumido nem concluído T>0 no lema algébrico; uma leitura física de temperatura precisa dessa identificação adicional. Para T=0, o controle reduz exatamente a Q=0. Eta*E≥0 requer eta≥0 e E≥0, hipóteses presentes.

## Evidência e alcance

Foi lida a metadata da sonda de desenvolvimento C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO051_DEVELOPMENT_20260907_034329_577118: quatro etapas, OpticalVolterraBalance, OpticalRiccatiInvariant, OpticalBalanceControls e Imports051All, todas exit0/PASS, sem issues, com estabilidade de fontes/inputs e cobertura exata de prints. Os bytes dos dois fontes acima coincidem com as cópias compiladas e com proof_sha256. Riccati tem13 teoremas+4 definições=17prints; Controls tem9 teoremas=9prints. Os prints desses dois módulos usam somente propext, Classical.choice e Quot.sound.

O lote final foi anunciado como em execução; esta nota não executa auditor, não atesta seu término e não substitui o marcador/auditoria finais. As dependências externas e históricas obedecem à fronteira declarada pelo runner; não foram recompiladas nem auditadas transitivamente por esta revisão matemática.

Conclusão: não identifiquei falha matemática nos dois fontes medidos. [INPUT] Setor óptico simétrico, base ortonormal, equações ópticas e casamento Ricci–matéria. [OPEN] Seleção da geometria pelo estado quântico, identificação física da correção, H3 e reconstrução gravitacional geral.
