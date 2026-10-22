"""Persist independent review and targeted repairs without claiming full acceptance."""
import record_haiku_preparation as record

record.MARKER = 'IALD_HAIKU_ADVERSARIAL_HYPOTHESES_REPAIR_20260922'
record.NOTE = '''[REAL — parecer independente concluído] Cicero finalizou revisão: adversarial_memory_review/PARECER.md. NÃO aprovou orçamento nem cobertura semântica completa. Mediu proposta estrutural de8410o200k de economia (variante não medidaAnthropic), insuficiente por si só para cortar40kAnthropic. Encontrou P1 em statement ausente do filtro e perda de filhos com nomes genéricos sob hypothesis/assumptions. Alertou que verificador importando seletor do construtor não comprova suficiência semântica; referência @EXPOSITION ainda exige unicidade/resolução mais forte.

[REAL — reparo focal aplicado somente no preparo] build_haiku_candidate.py agora protege statement/enunciado e o valor inteiro de hipótese/premissa/assumption estruturada. /core/external_ladder/per_theorem só é externalizado se TODOS os valores forem bool; guarda ponteiro e contagenstrue/false, sem anunciar contagem de provas. Backup imediato de bytes. Novo candidato001ef61bae3c42eec7998742a6b6ec98d2cf2fd6cee50fe5f4ad265975882ed2:175644o200k, redução líquida3160em relação ao anterior, apesar de restaurar hipóteses. NÃO é contagemHaiku;220651Anthropic refere-se ao candidato anterior.

[REAL — verificação independente focal] test_haiku_source_contract.py NÃO importa o construtor. Decodifica a representação do candidato e cruza campos pela coordenada de origem: hipótese inteira gw_echo_kms_rite/record/hypothesis, cinco statement encontrados pela auditoria independente e auditoria booleana externa.3testespassaram. Isso cobre os casos identificados, não todos os325tópicos. Verificador de preservação também passou: kernel/Core integrais,5Leaninteiros,7321refs,652linhasexposição preservadas exceto metadados.

[OPEN] Ainda é necessário reduzir substância redundante por revisão semântica tópico–exposição, sem amputar fórmulas/limites ou usar enchimento. Não ativar perfil antes de medir pedido completoAnthropic com>=180kpermanentes e≤200kcomsaída. Mínimo já exigido pelo módulo de orçamento preparado (7testes). RecuperaçãoJSONpointer segue sem autorização específica após bloqueio; nãoexecutada. Sonnetlogin/cache e testesfísicos pendentes. iOS18emtestesnosdoisgrupos;Android17compiladolocal. Nenhum novo servidor alterado ou reiniciado nesta etapa.
'''

if __name__ == '__main__':
    record.main()
