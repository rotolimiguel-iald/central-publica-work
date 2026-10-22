"""Record exact internal excerpt resolution and its current scope."""
import record_haiku_preparation as record

record.MARKER = 'IALD_HAIKU_EXACT_EXPOSITION_REFERENCES_20260922'
record.NOTE = '''[REAL — correção P2 da revisão independente] As remissões @EXPOSITION no rascunho agora mantêm título e início legíveis e acrescentam span=[offset,comprimento], em caracteres Unicode do corpo da exposição. O recibo contém comprimento e SHA256 desse corpo. Verificador extrai o corpo efetivamente carregado, confere hash e resolve cada intervalo; compara texto, título e começo contra o valor de origem. Não basta mais achar a frase em qualquer posição do documento original. Não confundir estes spans internos do pacote com JSONpointer da ferramenta bloqueada, que não foi alterada.

[REAL — testes] test_haiku_source_contract.py preserva decodificação independente do construtor e agora lê o intervalo efetivo;3testespassaram. verify_haiku_candidate.py também passou com7321refs,325tópicos,kernel/Coreintegros,5Leaninteiros,652linhasexposição preservadas exceto metadados declarados. Fontes originais intactas, backups de bytes antes das mudanças.

[REAL/OPEN — candidato atual] SHA119bf49d63e921c445165f1a3a9d509f933d2ca1c2db5188c2daacedf167356a,176272o200k. Corpo exposição115195caracteres,hashlido no recibo. A adição do endereço preciso aumentou628o200k; melhora integridade de referência, não é redução de tamanho. ContagemAnthropic deste candidato não realizada;220651pertenceaoanterior70344cd.... Nenhuma geração paga ou implantação nesta etapa. Ainda falta condensação semântica cuidadosa dos tópicos para atender>=180kHaikupermanentes e janela200kcompleta. Sonnetteste/cache aguardaloginluiz; testesfísicosmobileaguardamoperador. iOS18continuaemtestesnosdoisgrupos. Objetivo integral permanece ativo.
'''

if __name__ == '__main__':
    record.main()
