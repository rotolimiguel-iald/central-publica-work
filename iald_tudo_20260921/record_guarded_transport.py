from pathlib import Path
import json
import record_haiku_preparation as record
W=Path(__file__).resolve().parent
r=json.loads((W/'adversarial_memory_review/FINAL_integration_metadata_20260922_171917_621785.json').read_bytes())
assert r['status']=='APROVADA_OPERACAO_INTEGRACAO_E_METADATA_NO_ESCOPO_DOCUMENTAL'
record.MARKER='IALD_HAIKU_GUARDED_TRANSPORT_PREPARED_20260922'
record.NOTE='''[REAL — revisão final documental] FINAL_integration_metadata_20260922_171917_621785.json aprova operaçãoV6/runtime/metadados por auditor independente sem importar builders/verificadores do pai.38V6+23V5 pinados,22originaisV6/7V5 excluídos intactos,81âncoras,156JSONs compactados;decode estrutural e comparação com serialização original recuperam bytes. Aprovação não prova física/Lean nem entendimento do modelo. Contagem nativa permanece183135/184609 e reserva10271.

[REAL — transporte preparado] claude_guarded_transport.py conecta política autenticada→conversor real→guarda completa→stream nativo→_Fluxo/RespostaClaude existentes, sem reconverter em post_como_openai. RecusaHaiku>4096,parâmetrosSonnet removidos pelo pipeline,nenhumfallback/retry pago. Overflow/errodecontagem não abremstream;gerente fechado se falhaapósentrada. Errosapóstentativa degeração não afirmam falsamente que nadafoienviado.12testes transporte+pipeline passaram semrede/chave,7novoscasos. Auditor existente revisa loader/transporte em paralelo. Código aindaW,nãoimplantado.

[OPEN — integração] Servidor precisa selecionar perfil por conta,Haiku público aprovado/Sonnetluiz,lerpacote,usartransporte novo preservando consentimentoAnthropic/cotas/limites/ferramentas. _opcoes_de_motor hoje retorna[] para conta semacesso_nativa; api_motor_escolha e _chat_externo bloqueiamgratuitoClaude. Essasregras devem mudar apenasparaHaiku sem concederNativa/Sonnet. Prefixo atualmontado com_contexto_externo deve ser substituído pelo pacoteHaiku apenasnesseperfil;saída4k explícita. Rotasstatus/seleção/admin afetadas precisam sincronização. Sonnetteste/cachelogin e T1/T5físicos pendentes. Nenhuma produçãoalterada,nem APIgeração neste turno.
'''
if __name__=='__main__':record.main()
