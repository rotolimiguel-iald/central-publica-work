[REAL — patch de staging, Goodall] Router: host_followup/iald_auto_router.py. Averroes mantém posse exclusiva dos arquivos do host. Nenhuma edição em runtime ou no plano18 congelado.

Contrato: host oferece apenas uma política para pedido efetivamente audio-only, considerando todas as mídias do histórico atual (novas referências e inline legado). Se existir vídeo histórico, fps/resolução continuam relevantes. Router usa routing_options para contar somente planos admissíveis: com1, omite pergunta media_policy e registra seleção determinística; com>=2, pergunta JEV e mantém gate>=0.70; com0, recusa existente.

JEV ainda recebe/decide executor e demais perguntas originais. Não há deduplicação heurística de IDs/políticas pelo router; isso cabe ao host. Recibo registra media_policy_selection.mode/admissible_options/confidence_gate_applied e conserva orçamento e validação final obrigatória do host. Não altera permissões, carteira, consentimento ou retry.

9 testes offline passam: áudio120s/750tokens sem resposta de policy; executor preservado; único admissível+REFUSED; dois planos iguais ainda requerem host collapse; .68 recusa e .70 passa em>=2; zero recusa; texto/API/no-retry preservados. Execução por AST de blocos reais; sem nova chamada JEV ou MiMo, sem repetir pedido live falho.

Encaminhamento ao pai/Averroes via este arquivo e ROUTER_SINGLE_POLICY_HANDOFF.json; não há handle direto disponível nem envio de mensagem alegado. Integrar com a correção do host em novo plano delta, revisar e executar somente pelo pai. O plano18 anterior permanece imutável.
