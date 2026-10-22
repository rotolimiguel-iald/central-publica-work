# Reaproveitamento A1 — transporte antiunitário da fase

[OPEN — ficha escrita antes de qualquer Lean novo desta subtarefa]

Consumidor: `regular_dual_weight_modular_implementation`. Autoria desta ponte: sidecar; revisão independente posterior pelo principal.

Alvo genérico: H Hilbert complexo completo, T limitado positivo contrativo, T e I−T injetivos, J antiunitário e JTJ⁻¹=I−T. Construir JU_tJ⁻¹=U_t para o grupo já entregue. Não receber essa igualdade como premissa nem pressupor J²=I na camada genérica.

Reuso: `antiunitaryConjugate`/multiplicatividade, positividade/raiz conjugada, `antiunitary_inner_conj`, o grupo pela imagem densa de b(T), e o flip do J/T original. A busca local encontrou transporte de raiz, mas não transporte geral antiunitário de CFC; a API `StarAlgHom.map_cfc` sobre ℝ fornece a ponte econômica, decompondo a fase complexa em partes real e imaginária. Identidade escalar prevista: conjugate(g_t(1−x))=g_t(x), inclusive pontas amortecidas.

Plano: representar conjugação como homomorfismo real de *-álgebras; transportar CFC real; compor x↦1−x; recompor re/im com conjugação de i. Transportar b(T) e C_t e cancelar pela imagem densa de b(T). Especializar ao `scalarTomitaPolarFactor` e `scalarTomitaResolvent` já construídos.

Fornecedores, locadores e hashes lidos estão no JSON. Os cinco módulos anteriores permanecem protegidos. Nenhum arquivo de escala/intertwining do principal será editado. Só um ou dois novos V351; tentativas com `compile_a1.py` serão preservadas, somente rc0/trio aceito. Sem nova raiz, GNS ou PVM. A1(b), ação AdΛ, h e traço continuam OPEN.
