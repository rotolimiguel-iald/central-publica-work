# ERRATA AO LADO — R2.2 na produção (13/10/2026, gerência c1)

A primeira execução real (RECIBO_IMPLANTACAO_20261013_114349_958018.json) parou em parar_app sem mudança nenhuma. Causa [REAL]: a lib lia habilitada = (State != 'Disabled'); com o app rodando, uma tarefa desabilitada continua com State 'Running'. Conserto: habilitada = Settings.Enabled (3f42bf41edf2c6d0 -> 795d724cba17a484; backup .bak_20261013_115044_settings_enabled).
