# Consulta — aproximação direita do comutante e o J original

2026-09-12T21:47:53.756651-03:00 — consulta matemática de rota, sem revisão formal, compilação ou novo certificado. Fontes locais lidas e hipóteses conferidas; os enunciados propostos abaixo ainda exigem implementação e auditoria. Nenhum parecer custodiado, código, memória ou monólito foi alterado.

**Diagnóstico:** a rota R_h proposta é concreta e não circular. Para avançar até a álgebra direita com adjunto, convém usar **K_h(T)=R_h* T R_h**. O unilateral T R_h fornece um vetor direito; a existência do vetor que representa seu adjunto não decorre só dessa conta. O sanduíche fornece os dois, com fórmulas explícitas, e ainda aproxima todo o comutante fortemente com cota uniforme.

Escreva H=H_I, M=π(N), Λ=scalarWeightGNSEmbedding P, X_h=regularAverage P h, F=S†. Trabalhe com h>0 e h→0 pela direita, sem vetor Λ(1).

1. **Construção limitada no mesmo H.** Para a∈nν, o produto aX_h continua em nν e a aplicação a↦aX_h é complexa-linear. [ScalarRightAverage:70](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarRightAverage.lean:70>) fornece ν((aX_h)*(aX_h))≤ν(a*a). Com [ScalarWeightAction:44](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarWeightAction.lean:44>), isso dá ‖Λ(aX_h)‖≤‖Λ(a)‖, sem usar `toReal` sobre infinito. A extensão de norma ao fecho denso de Λ(nν) fornece R_h∈B(H), ‖R_h‖≤1 e R_hΛ(a)=Λ(aX_h). A densidade é a de [ScalarWeightAction:54](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarWeightAction.lean:54>); a convergência nas inscrições é [ScalarWeightCompletion:16](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarWeightCompletion.lean:16>). Pela cota uniforme, R_h→1 fortemente em todo H. Não se exige I=nν nem que Λ(nν) seja fechada.

2. **Comutação e vetor de inscrição.** Para b∈N e a∈nν, associatividade e [ScalarWeightAction:38](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarWeightAction.lean:38>) dão R_hπ(b)Λ(a)=Λ(baX_h)=π(b)R_hΛ(a). Por densidade, R_h∈M'. Para h>0, X_h∈I⊆nν, então η_h=Λ(X_h) existe e R_hΛ(a)=π(a)η_h. Para T∈M', segue T R_hΛ(a)=π(a)Tη_h. Isto já prova aproximação de qualquer T por operadores direitos limitados com norma ≤‖T‖. Não se afirma convergência de η_h; suas normas podem crescer quando h↓0.

3. **Versão que controla o adjunto.** Defina

   K_h(T)=R_h* T R_h,    η_h,T=R_h* Tη_h,    ζ_h,T=R_h* T*η_h.

   Como R_h* e T comutam com π(a), para TODO a∈nν:

   K_h(T)Λ(a)=π(a)η_h,T,    K_h(T)*Λ(a)=π(a)ζ_h,T.

   Não se permutam T e R_h: ambos pertencerem a M' não implica comutarem entre si. O adjunto é K_h(T)*=R_h* T* R_h, exatamente a ordem acima. A cota é ‖K_h(T)‖≤‖T‖. [ContractionAdjointLimit:15](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ContractionAdjointLimit.lean:15>) dá R_h*→1 fortemente, pois R_h são contrações convergindo a 1. Portanto

   ‖K_h(T)x−Tx‖ ≤ ‖T‖ ‖R_hx−x‖ + ‖(R_h*−1)Tx‖ → 0.

   O mesmo vale para os adjuntos, substituindo T por T*. Assim obtém-se aproximação forte-* uniforme do comutante por operadores direitos com os DOIS vetores testemunhas. Não foi usada continuidade geral de star na SOT.

4. **Próximo lema ligado diretamente ao F original.** Para h>0 e T∈M', provar

   η_h,T∈D(F),    Fη_h,T=ζ_h,T.

   Há uma prova curta com a infraestrutura existente. Em a∈nν∩nν*, R_h×R_h leva (Λ(a),Λ(a*)) a (π(a)η_h,π(a*)η_h). Por continuidade limitada e [ScalarWeightTomitaIdentification:58](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarWeightTomitaIdentification.lean:58>), leva TODO graph(S) ao fecho do gráfico vetorial de η_h. Pode-se tomar a álgebra ambiente gerada M''; não é preciso identificar M=M'' neste passo. T∈M' também pertence ao comutante dessa álgebra gerada. [VectorTomitaClosability:24](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/VectorTomitaClosability.lean:24>) não exige vetor separante e fornece, para TODO x∈D(S),

   ⟨R_h Sx,Tη_h⟩ = ⟨T*η_h,R_h x⟩,
   ⟨Sx,R_h* Tη_h⟩ = ⟨R_h* T*η_h,x⟩.

   A última igualdade está na convenção complexa do código e é exatamente a premissa de [ScalarTomitaAdjoint:27](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarTomitaAdjoint.lean:27>). Não se inverte R_h, não se pressupõe continuidade de S e não se redefine F. Este padrão reaproveita o transporte de gráfico já empregado para o mapa gaussiano, mas o novo testemunho é inteiramente construído a partir do peso original.

**Relação precisa com a fonte primária.** §5.2 exige representação limitada tanto da multiplicação direita como de seu adjunto. Em 5.11 a densidade do comutante usa sanduíches; 5.12 identifica o subespaço real da álgebra direita com o complemento simplético do anterior, garantindo o mesmo J. A simetria de 5.13 usa essa identificação e 5.10: não é consequência formal de uma inclusão isolada. Conferidas também visualmente as páginas impressas 216–217. [Rieffel–Van Daele, 1977, §5](https://msp.org/pjm/1977/69-1/pjm-v69-n1-p17-s.pdf).

**O que falta, sem renomear a conclusão.** O resultado dos itens 1–4 é novo conteúdo verificável: contrações construídas, dois vetores direitos explícitos, pertencimento ao adjunto máximo original e aproximação de operadores arbitrários do comutante. Ele ainda não prova K_h(T)∈JMJ. Provar a reconstrução desses operadores direitos na forma Jπ(b)J é a obrigação substantiva seguinte; tomá-la como hipótese e chamar a inversa de resolvida seria circular. Densidade SOT de operadores direitos não é densidade em H dos seus vetores nem densidade de gráfico em D(F). Para a via de §5, será necessário justificar a álgebra direita completa, os fechos de suas involuções e a identificação do J com o polar ORIGINAL. [ScalarTomitaStandardSubspace:18](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarTomitaStandardSubspace.lean:18>) identifica Fix S e D(S)=Fix S+i Fix S; não fornece automaticamente essas novas identificações. Os lemas [ScalarRightClosedTomita:31](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarRightClosedTomita.lean:31>) e [ScalarRightTomitaAdjoint:59](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarRightTomitaAdjoint.lean:59>) continuam específicos dos dados homogêneos e não autorizam substituí-los por um T arbitrário.

**Alternativa topológica, independente e útil.** Provar que M=π(N) é VN continua sendo uma tarefa separada. Há uma rota mais direta que usar ξ: [DualOrbitVonNeumann:69](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualOrbitVonNeumann.lean:69>) identifica exatamente a álgebra ambiente ρ(N) como VN; [ScalarGNSRepresentation:14](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarGNSRepresentation.lean:14>) é sua restrição redutora a H_I, e [ScalarGNSRepresentation:60](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarGNSRepresentation.lean:60>) prova fidelidade. A isometria de *-homomorfismo injetivo está disponível em Mathlib `Analysis/CStarAlgebra/Hom.lean`, lema `NonUnitalStarAlgHom.isometry`. Um lema genérico de imagem VN sob restrição redutora fiel pode usar compactação WOT da bola unitária ambiente, continuidade WOT da compressão e Kaplansky para a álgebra C* imagem. Essas pontes topológicas não foram verificadas por compilação aqui e não devem ser declaradas prontas só por nome. Norm-isometria sozinha dá fechamento em norma; transferência SOT limitada sozinha só transfere um limite já localizado no domínio. Não se deve assumir que qualquer rede SOT convergente seja uniformemente limitada em todos os índices.

M ser VN tornaria JMJ fechado na SOT, permitindo passar de uma futura reconstrução dos K_h(T) à inclusão inversa. Isso não identifica J com o Tomita do vetor ξ e não resolve por si a reconstrução. A rota sugerida para implementar AGORA é a dos itens 1–4, com enunciados novos de extensão direita, comutação, pareamento máximo e aproximação forte-*; nenhuma condição KMS é necessária para esses quatro passos.

Leituras e estatuto: pins individuais em [consultation_pins.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/consulta_right_bounded_20260912_214127_316501/consultation_pins.json>). Mãe gaussiana SHA `f7b09a7206bd2ddd54afb843588668b7d58d934b6ace2fec6c8dceb4836b4931`; PDF SHA `21cec65bb6967994ea899839514396601b716df0f980b3929a5fcd7a988999bb`. Nenhum novo DEV em elaboração foi aceito por esta consulta, nenhum build ou programa autoral foi executado. KMS, fluxo modular identificado, traço, gate e runtime permanecem fora do resultado.
