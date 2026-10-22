# Entrega — entrelaçamento canônico e caráter por fase relativa

2026-09-09T17:42:58-03:00.

[REAL — compilação] Duas folhas congeladas/PASS: 48 teoremas, 15 definições, 63 auditorias de termos; quatro processos Lean com exit 0, saída limpa e apenas propext, Classical.choice e Quot.sound nos termos auditados. Cada folha e seu importador foram compilados em pasta nova. A segunda usou cópia byte a byte da primeira folha aprovada. Não houve execução/importação de um.py nem alteração de originais.

## 1. Projetores realmente entrelaçados

[DERIVED — núcleo formal] E(v)=r(v₀−iv₁)e₀+r(v₀+iv₁)e₁, com r=√(1/2), e₀=firstInscription e e₁=inscriptions 1. E tem inversa à esquerda explícita e é injetiva. Os projetores canônicos satisfazem:

- P E(v)=E(P₊v), com P=ialdSelector.
- (I−P)E(v)=E(P₋v).
- W(θ)=exp(iθ)P+exp(−iθ)(I−P) é unitário.
- W(θ)E(v)=E(angFamily(θ)v).

Referências: [angular_embedding_coordinates](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/AngularSelectorIntertwining.lean:61>), [angular_embedding_injective](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/AngularSelectorIntertwining.lean:69>), [selector_intertwines_plus](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/AngularSelectorIntertwining.lean:73>), [selector_intertwines_minus](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/AngularSelectorIntertwining.lean:85>), [selector_flow_unitary](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/AngularSelectorIntertwining.lean:146>) e [selector_flow_intertwines](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/AngularSelectorIntertwining.lean:153>).

Não se identifica um operador de ellTwo com uma matriz 2×2 por homonímia. E explicita a relação no subespaço gerado pelas duas inscrições. O complemento I−P atua no Hilbert inteiro; a comparação matricial é sobre a imagem de E.

A segunda folha prova [angular_embedding_inner](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/RelativePhaseCharacter.lean:41>): ⟨Ev,Ew⟩=conj(v₀)w₀+conj(v₁)w₁. É preservação da forma hermitiana euclidiana. O domínio foi tipado como espaço algébrico Fin 2 → ℂ; não se afirma Isometry para sua norma sup padrão. Equipado com a norma euclidiana indicada por essa forma, E preserva a norma correspondente.

## 2. Referência, probabilidades e fase relativa

[DERIVED — leitura matemática com referência] São usadas as referências normalizadas rₓ=(e₀+e₁)/√2 e rᵧ=(e₀−ie₁)/√2, mantidas fixas na leitura. O estado ψθ=W(θ)rₓ também é normalizado. As duas probabilidades de projeção, definidas por módulos quadráticos dos produtos internos, são:

pₓ(θ)=|⟨rₓ,ψθ⟩|²=cos²θ;
pᵧ(θ)=|⟨rᵧ,ψθ⟩|²=(1+sin(2θ))/2.

Logo (2pₓ−1)+i(2pᵧ−1)=exp(2iθ). O sinal positivo da segunda quadratura corresponde exatamente à referência com −i e₁.

Referências: [reference_state_normalized](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/RelativePhaseCharacter.lean:56>), [quadrature_reference_normalized](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/RelativePhaseCharacter.lean:69>), [relative_phase_state_normalized](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/RelativePhaseCharacter.lean:103>), [interference_x_formula](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/RelativePhaseCharacter.lean:184>), [interference_y_formula](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/RelativePhaseCharacter.lean:189>) e [reconstructed_phase_formula](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/RelativePhaseCharacter.lean:196>).

[DERIVED — controles de fase] O produto cruzado 2ψ₀conj(ψ₁) é exp(2iθ) e é invariável sob fase global unitária: [cross_readout_relative_phase](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/RelativePhaseCharacter.lean:120>) e [cross_readout_global_phase_invariant](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/RelativePhaseCharacter.lean:133>). Em contraste, W(θ)e₀ tem sempre a mesma densidade pura; isso foi demonstrado coordenada a coordenada em [selected_ray_density_unchanged](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/RelativePhaseCharacter.lean:142>). Não se vende a fase global do vetor selecionado isolado como observável físico.

[DERIVED — casamento escalar direto] As duas leituras algébricas pedidas também estão demonstradas:
2(P₊angFamilyθ)₀₀=exp(iθ) e tr(P₊angFamilyθ)=exp(iθ).
Fontes: [matrix_selected_entry_reads_phase](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/RelativePhaseCharacter.lean:246>) e [matrix_selected_trace_reads_phase](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/RelativePhaseCharacter.lean:252>).
Essas identidades de operador são distintas de afirmar uma probabilidade que meça diretamente sua fase global.

## 3. Caráter e reconstrução

[DERIVED — registro dado] Para R admissível, define-se θ=s·recordCharacter(t,R)/2. A combinação das duas probabilidades passa a ser exp(i·s·recordCharacter(t,R)).

A derivada em s=0 identifica o coeficiente real. Para t diferente de zero, igualdade da família completa de leituras equivale à igualdade da classe de R. Portanto os campos g e T coincidem no domínio U.

Fontes: [character_readout_formula](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/RelativePhaseCharacter.lean:218>), [phase_family_derivative](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/RelativePhaseCharacter.lean:203>), [phase_family_injective](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/RelativePhaseCharacter.lean:209>), [character_readouts_same_iff](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/RelativePhaseCharacter.lean:225>) e [character_readouts_reconstruct_fields](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/RelativePhaseCharacter.lean:239>).

[INPUT — alcance informacional] O teorema usa probabilidades exatas para uma família inteira de s. Uma leitura em um único s pode apresentar periodicidade. Não foi demonstrada recuperação por duas frequências, estimativas finitas, dados ruidosos ou protocolo experimental de precisão finita. O parâmetro t do caráter é distinto do parâmetro s usado na família de leitura.

[OPEN — correspondência física] R é entrada. O operador W foi construído a partir do caráter desse registro. O resultado reduz a lacuna de tipos entre projetores nomeados, leitura angular e classe reconstruída; não demonstra que um estado físico específico ou uma interação de Araki produza R ou implemente esse W. Não se identifica W com o cociclo dinâmico da torre ou com o cociclo perturbado por simples igualdade de nome.

O registro admissível, a condição de área o(t²), a conservação total, as telas, o atlas e as transições físicas mantêm seus estatutos anteriores. Nenhuma equação de Einstein é recebida como hipótese escondida nestas duas folhas; elas estabelecem a ligação informacional por leitura.

## 4. Revisão independente

[REAL — parecer recebido] A raiz /root leu integralmente as duas fontes e deu parecer semântico FAVORÁVEL.

Na primeira: aplicação linear explícita e injetiva evita ligar homônimos; a unitariedade de W foi separada de qualquer afirmação de norma de E.

Na segunda: parecer favorável às duas probabilidades, à preservação da forma hermitiana, ao sinal +sin(2θ), ao controle de fase global e à identificação da família por derivada em zero. O parecer exige manter explícitos a família completa de s, as probabilidades exatas e R como entrada; esses limites estão acima.

A revisão independente foi semântica, em leitura. A compilação foi conduzida pelo construtor e os recibos não são apresentados como recompilação independente.

## 5. Recibos e custódia

- AngularSelectorIntertwining: 8706 bytes; SHA-256 7538ba1b9e471d52cb55ca8a63989f007be125d3647af05b14259dc0d2c1b9fd; [recibo PASS](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/BUILD_20260909_173327_687034/BUILD_RESULT.json>).
- RelativePhaseCharacter: 12163 bytes; SHA-256 e7e2219b0fd1629e064cab1b1d3e789208d244a0fa526cae9c3b153a153d3057; [recibo PASS](<C:/IALD/Central de Patentes/Chatgpt/ENTRELACAMENTO_SELETOR_20260909_172718_478310/BUILD_20260909_173940_076834/BUILD_RESULT.json>).

A fronteira de leitura foi medida antes e depois. As fontes canônicas e os caches permanecem inalterados; o alcance de hashes/recompilação transitivos é o que cada recibo declara, não uma recompilação integral da biblioteca. Todas as tentativas anteriores e backups imediatos de bytes permanecem na pasta.

As alterações em arquivos próprios utilizaram backup imediato em bytes, arquivo temporário exclusivo, sincronização, verificação e substituição atômica. Os documentos finais são arquivos novos. Não foram alterados Atlas, índice, memórias canônicas ou o um.py. A entrega não move o gate nem afirma gravidade quântica confirmada ou resolvida.
