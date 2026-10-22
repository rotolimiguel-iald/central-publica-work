import record_haiku_preparation as record
record.MARKER='IALD_CLAUDE_SERVER_SELECTION_PREPARED_20260922'
record.NOTE='''[REAL — seleção preparada] claude_server_selection.py separa IDs de interface claude-haiku/claude-sonnet do provedor único claude. Retorna campos motor/modelo_claude para persistência sob trava da rota; não grava usuários. Registroexistente não bloqueado→Haiku;Sonnet exclusivamente username luiz. LegadoLuizclaude preservaSonnet,demaisHaiku. Escolha forjada/indisponível não fazfallback. ConfigclonadaHaiku saída4k/janela200k,sem alterar cotas/exceção global,sem conceder acesso_nativa;exige preço configurado.13testes seleção+política passaram,7novos. Módulo emW,não ligadoàsrotas ainda.

[REAL — contrato de interface lido] app/iald.js listarModelos/escolherMotor já envia id da opção em motor;precisa comparar atual com motor_selecao adicional(ou modelo) para distinguir doisClaude. Servidor normalizará ID em provedor+modelo antesvalidarMOTORES. /api/active-model e /api/motor precisamcfg selecionada;admin/permissões também. Regras Nativa/OpenAI preservadas. PreçoHaiku ausente da tabela produção: ativação deve configurar preço atual verificado antesliberar,semherdarSonnet. Guarda por pedido usa tokenizaçãoAnthropic, não estimativao200k.

[OPEN] Integração rotas/cliente,review loader/transporte,teste realSonnet/cache dependelogin,Centralvisual/exportaçõesfísicas. Nenhuma produçãoalterada nestaetapa. Objetivoativo.
'''
if __name__=='__main__':record.main()
