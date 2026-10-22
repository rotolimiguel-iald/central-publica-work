# Revisão independente — comutação de cortes e médias

2026-09-14T22:10:00.124631-03:00

**A1_CUTOFF_AVERAGE_COMMUTATION_MATH_REVIEW_PASSED__DOCUMENTARY_P2_OPEN**

[REAL] **Sem P0/P1; um P2 documental.** Três teoremas públicos + um helper privado, zero definições. Leitura completa e Lake/auditor próprios rc0: #check com universos e axiomas apenas propext, Classical.choice, Quot.sound. O resultado matemático passou; não se emite aceite documental sem ressalvas.

**P2 — referência CFC trocada no adendo.** [ADENDO_FICHA_COMUTACAO_CFC.md](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ADENDO_FICHA_COMUTACAO_CFC.md:9>) e JSON `$.providers[0]` nomeiam `IsSelfAdjoint.commute_cfc`, mas a linha 67 e o texto são de `commute_cfcHom`. O lema efetivamente usado existe na [linha 87 do mesmo arquivo pinado](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Commute.lean:87>). Corrigir locador e enunciado no MD/JSON, preservando bytes anteriores; não é necessário alterar/recompilar Lean.

[REAL — realização e sinal] O primeiro alvo usa exatamente regularSpectralCoordinates P, o multiplicador por sigmoid e o caráter de parâmetro +2πt. A comutação com todos os caracteres é descarregada pela lei aditiva existente. character_commutation_realScalarMultiplier fornece M C=C M, e o transporte pela equivalência estrela de V entrega o MESMO R e regularUnitary P t, sem hipótese residual nem nova transformação espectral.

[REAL — CFC e raiz] R≥0 fornece IsSelfAdjoint para commute_cfc; a igualdade já provada Bε=cfc(fε)(R), sob ε>0, identifica o corte original. O helper hilbertPositiveSqrt_commutes é genérico em Hilbert complexa completa e consome Commute.cfcₙ_nnreal NNReal.sqrt com as instâncias do wrapper antigo. Nenhuma raiz nova é definida. O helper foi relido e compilado; seus axiomas entram transitivamente nos prints dos alvos públicos, sem alegar #print privado separado.

[REAL — integral e domínio] A última identidade vale para TODO δ real, inclusive zero e negativo; somente ε>0 é exigido. regularAverage_apply mantém δ⁻¹ e o integral orientado de 0 a δ. O CLM B comuta com o escalar e atravessa o integral por intervalIntegral_comp_comm, usado na orientação inversa. A integrabilidade é descarregada pela continuidade forte de λ_t em cada vetor. Integral_congr usa a comutação pontual já provada; nenhuma continuidade em norma do grupo, separabilidade ou seleção de eventos a.e. sobre conjunto não enumerável foi pressuposta.

[REAL — histórico e negativo] A tentativa DEV 220259_446252 rc1 permanece excluída: a reescrita procurava o lado errado do lema de integral. A final 220350_353915 rc0 coincide com a fonte reproduzida, sem avisos; maxHeartbeats 1600000 está explícito. A auditoria autoral standalone e os streams foram relidos com pins. O negativo insere sinal menos na conclusão e é recusado por Type mismatch, com imports resolvidos; não foi reexecutado nesta revisão. A recusa não exclui coincidências especiais, como δ=0.

[REAL — proveniência] 674 objetos próprios anteriores preservados; adicionados apenas módulo e auditor (total 676). Nenhum fornecedor antigo recompilado ou objeto autoral/DEV importado. Pacotes externos são cache pinado herdado da reprodução anterior, sem nova auditoria integral. Run próprio rc0 em 38.387 s; zero avisos do alvo/auditor, 178 mensagens históricas de fornecedores registradas no JSON. LEAN_PATH dos traces só contém V e seus pacotes.

| Artefato | SHA256 lido |
|---|---|
| Fonte final | `bc881ee5df7e027859ef14d7379b27bc9c2a27bea3b08cf42d6604805afa2a66` |
| .olean próprio | `93d331fab3cea3f6b87e159ff5237f010a9cd98c0f36f8e974010d1544b1cc8d` |
| .olean cold autoral, só comparação | `93d331fab3cea3f6b87e159ff5237f010a9cd98c0f36f8e974010d1544b1cc8d` |

Igualdade binária medida: True.

[OPEN — limites] As três conclusões formais passaram, mas o P2 documental de locador/enunciado deve ser corrigido antes de entrega sem ressalvas. Não se afirma que qualquer b∈E comuta com as médias; o resultado é para as raízes dos cortes originais. Extensão da ordem dos pesos a todos os positivos e tracialidade permanecem abertas; nenhum gate é promovido. Nenhuma consulta adicional, edição de fontes autorais/memórias ou execução de monólito/recorder.

Artefatos próprios:

- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_comutacao_cortes_medias\compilation.json>) — SHA256 `95005790296dcd64934702e3d1be698429e35701323601d14404b84e556ef2a9`.
- [run](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_comutacao_cortes_medias\independent_20260914_220558_290545\run.json>) — SHA256 `0614e4067d8ad71dc7a0fb1a119aa6ed793791acecdd25bb977ee2bde9d20c6d`.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_comutacao_cortes_medias\independent_20260914_220558_290545\type_axiom_audit.json>) — SHA256 `0ef359012b34425e3a5fff9e1e9fb496516053eb29416bb8f55c479ddc6471f4`.
- [histórico](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_comutacao_cortes_medias\history_read.json>) — SHA256 `f4a01fbce81ce32e29bf9dfe68ddabb2c6e673c3549a6deced58fb154164b23d`.
- [P2 documental](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_comutacao_cortes_medias\documentary_finding.json>) — SHA256 `0083f87f83d20ffab78d47c18e0ea8eb82f891b452a154aa402de5871b797549`.
