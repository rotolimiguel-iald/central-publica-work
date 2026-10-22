# Integrador sucessor: instâncias locais nomeadas

[REAL] Dois scripts novos preparados para a CONFIG_COCICLO_COVARIANCIA.json congelada. O integrador anterior permanece idêntico; cada cópia recebeu backup dos bytes antes de ser editada. Nenhuma integração, preparação de overlay, compilação Lean ou execução/importação de um.py ocorreu nesta tarefa.

## Alterações exatas

- **integrate_approved_copy.py:** a função lean_declarations inclui declarações local instance NAME, além de theorem/def/abbrev/structure. Exige nomes únicos e exatamente um #print axioms por declaração. Detecta instâncias anônimas ou com formas não contempladas e falha explicitamente. Preserva a convenção existente de um único namespace por módulo; não pretende ser parser geral de toda a gramática Lean.
- **Metadados do integrador:** acrescenta all_declaration_names, local_instance_names, declaration_counts e audit_policy. Confere os números de measured_counts.total da configuração, quando presentes. O campo theorem_names continua contendo somente teoremas.
- **build_transposed.py:** relê as declarações da fonte transposta e compara exatamente kind/nome qualificado com os metadados congelados. O arquivo dedicado NewModulesAudit.lean passa a auditar todas as declarações. As folhas já auditavam cada declaração e continuam assim.
- **Agregador TGL/Audit.lean:** conserva o padrão anterior de acrescentar apenas os teoremas. As instâncias são auditadas duas vezes no build planejado: na própria folha e no dedicado. Não há nova flag individual, alteração do gate, mudança das sentinelas ou modificação do código externo à tabela embutida.
- As demais rotas de transposição, proteção de AST/bytes, extração de volta, criação de diretório novo, overlay e execução Lean permanecem como no integrador anterior. Os diffs unificados registram o delta completo.

## Verificação executada

[REAL] AST Python válido para ambos os scripts. Executadas exclusivamente as funções puras lean_declarations, extraídas por AST, sem executar o corpo principal dos scripts. Os dois parsers deram resultados iguais nas 63 fontes; hashes e recibos PASS foram relidos e conferidos contra a configuração.

Contagem: **856 teoremas + 207 definições + 17 abreviações + 11 estruturas + 7 instâncias locais = 1.098 termos**. Assim, outras declarações = 242. As sete instâncias têm nomes e prints próprios em UnitaryDuhamel, SpectatorCancellation, FiniteModularHamiltonian e FiniteLevelExponentials.

Foram conferidos quatro casos positivos e oito negativos, além dos dois ASTs e da conservação dos originais/backups. Os negativos cobrem instância anônima, instância global/escopo não revisado, print ausente, print duplicado, print excedente e nome duplicado. O recibo VALIDACAO_INSTANCIAS.json guarda as fontes e os resultados.

## Próxima execução autorizada ao orquestrador

[INPUT] A raiz revisará os scripts e executará a configuração congelada. A invocação do integrador é a mesma: python -B integrate_approved_copy.py CONFIG_COCICLO_COVARIANCIA.json. Depois, python -B build_transposed.py prepare PASTA_GERADA e python -B build_transposed.py run BUILD_PLAN.json.

[OPEN nesta tarefa] Ainda não há cópia63 nem resultado de build conjunto produzido por estes scripts. A validação aqui é sintática, de contagem e de comportamento do parser; não é compilação das 63 folhas ou confirmação de runtime do programa.

## Arquivos entregues

integrate_approved_copy.py, build_transposed.py, respectivos backups imediatos e diffs, PREPARACAO_SCRIPTS.json, VALIDACAO_INSTANCIAS.json e MANIFESTO_INTEGRADOR.json. A configuração original não foi editada; o integrador anterior e as fontes Lean permanecem intactos.
