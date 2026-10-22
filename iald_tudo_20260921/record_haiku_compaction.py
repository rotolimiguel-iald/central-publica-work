"""Persist measured, lossless metadata compaction; deployment remains pending."""
import record_haiku_preparation as record
record.MARKER = 'IALD_HAIKU_METADATA_COMPACTED_20260922'
record.NOTE = '''[REAL — progresso de bancada] O candidato Haiku passou de231679 para199587 tokens oficiais após compactar metadados de referência. Revisão seguinte compartilhou10 literais repetidos e referenciou passagens idênticas já presentes na exposição, por seção e início literal, preservando os textos. Medição oficial final desta etapa:197129 tokens com mensagem mínima, linha de base9, modelo claude-haiku-4-5-20251001. Recibo haiku_count.json contém SHA medido; não usar contagens anteriores para o candidato atual. Nenhuma geração paga.

[REAL — verificação] verify_haiku_candidate.py expandiu/comparou referências de literais e de exposição para todos os325 tópicos contra a projeção anterior, garantindo os mesmos valores selecionados; resolveu7321 referências ao JSON público, conferiu presença integral do kernel e Memory Core. compact_values_equivalent=true. Cobertura semântica permanece NOT_YET_AUDITED: equivalência de compactação não valida a seleção inicial nem teoremas.

[OPEN] Candidato197129 ainda NÃO é utilizável como perfil permanente de180k: não sobra espaço operacional suficiente na janela200k. Falta selecionar cerca de17k de detalhes acessórios mantendo conceitos/fórmulas, recontar, integrar servidor/recuperação e verificar requisição completa. Não implantado, Sonnet/Haiku não testados com geração paga. T5 builds18/17 e verificação física continuam pendentes. Meta integral inacabada.
'''
if __name__ == '__main__':
    record.main()
