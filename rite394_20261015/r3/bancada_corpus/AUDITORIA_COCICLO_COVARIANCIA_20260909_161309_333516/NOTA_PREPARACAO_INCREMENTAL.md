# Auditoria da preparação incremental

[REAL] PASS_STATIC_INCREMENTAL_PREPARATION_SCOPE: 8.608 verificações aprovadas, sem falhas; 2.292 arquivos medidos. Este é o parecer de preparação e compatibilidade do cache, sem antecipar o resultado da corrida.

[REAL] As 45 fontes reutilizadas são byte a byte iguais às fontes do build anterior com 48 processos PASS. Seus 90 artefatos .olean/.ilean foram medidos no reuso e copiados sem alteração. Os 1.247 pins comuns de dependências coincidem entre os planos antigo e novo.

[REAL] O plano contém exatamente 21 comandos: as 18 fontes novas, TGLExt, TGL/Audit e NewModulesAudit. O dedicado carrega os 1.098 termos, incluindo as 7 instâncias locais nomeadas. Cada comando deriva do plano aprovado por troca exclusiva do diretório de saída; seus arquivos de entrada estão no novo build e todos os destinos de saída ficam nesse diretório.

[REAL] Nenhum output parcial da compilação atual serve de origem ao cache. Do plano atual foram reaproveitados apenas arquivos Lean preparados e o overlay predeterminado de dependências canônicas, conferidos por hashes. Os 45 binários vêm exclusivamente do build anterior PASS.

[REAL] O runner foi lido sem execução. Ele confere os registros de entrada e cache antes da primeira compilação e novamente depois da última; o status PASS exige ambos os controles, os 21 resultados válidos e os axiomas admitidos. O seu resultado de execução deve ser lido separadamente quando disponível.

[REAL — limite de custódia] O recibo PASS anterior não continha hashes históricos dos binários que gerou. Os hashes usados agora são medições no reuso, preservadas nas cópias e no novo plano. Esta auditoria não afirma que o recibo anterior já possuía esses hashes na hora da compilação.

[REAL] Nenhum um.py, adapter, runner ou compilador foi executado pelo auditor. Nenhum original ou arquivo existente foi editado.

Recibo detalhado: AUDITORIA_PREPARACAO_INCREMENTAL.json.
