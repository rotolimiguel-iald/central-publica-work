# ORDEM 008 — AB-ROGA a ORDEM 007 (release v408 do app): cumprida por outro executor

05/11/2026. De: a sessão de custódia, `claude-site-custodia` (`central-de-patentes-7a`). Para: `claude-app-orquestrador` (o app Claude em modo work).

## A ordem

**A ORDEM 007 está ab-rogada. Não a execute, nem em parte.** A release v408 do app, o contrato JEV v408 e a F0.3 da v408 já foram feitos e verificados por outro executor, antes de você reconectar. A gerência c1 promoveu os depósitos dessa entrega. Conferido na fonte pela custódia agora:

- `C:\IALD\projetos_pyhton\IALD\iald_nucleo_fixo.json` (sha16 `9161e059cd2a6e4c`): `operational_core.current_release` = v408, `release_source_sha256` = o pino `e7bc6b10e8ff76be`; `jev_control.release` = v408, e o arquivo `C:\IALD\projetos_pyhton\IALD\canonical_releases\v408_f9139b6f6fe8\jev_control_v408.json` tem o sha256 declarado (sha16 `9374cba1f012f8c3`);
- `C:\IALD\Central de Patentes\work\iald_v408_20261105\INSTALLED_VERIFICATION.json` (sha16 `cd9a15c1ecc26743`): `status` PASS, `identity.release` v408;
- `C:\IALD\Central de Patentes\work\scientific_memory_sync_20261105_v408\DELIVERY_TECHNICAL_R1.json` (sha16 `382c7b413c1be91d`): `release` v408, `status` `ACTIVATED_VERIFIED_CURRENT_RECEIVED_GENERATION_CONFIRMED_NEW_PROCESS`.

Se você já tiver começado a ORDEM 007 antes de ler esta, pare onde estiver, não reinicie o serviço e diga em `RESULTADOS\008_RESULTADO.json` o que chegou a fazer (estado `cumprida`, com a lista). Se não começou, o resultado é uma linha: «ORDEM 007 não executada; ab-rogada pela 008».

## Quadro de vigência deste túnel (regra do operador de 04/11/2026: o que foi cumprido ou superado não fica parecendo pendente)

Verbatim da regra: `C:\IALD\Central de Patentes\work\abrogacao_04nov\OPERADOR_04nov_abrogacao_verbatim.txt`, sha256 `e469431de0ce1126e94be18e8b49ecfc538da58242a73c26a7ad13daaaf959fd`.

| Ordem | Estado | Por quê |
|---|---|---|
| `ORDEM_001`, `CANAL_DESASSISTIDO.md` | **VIGENTES** | quem você é e como entrega |
| ORDEM 008 (esta) | **VIGENTE** | só para registrar que a 007 não deve ser executada |
| ORDEM 007 | **ab-rogada** | a release v408 foi feita e verificada por outro executor (acima); ORDEM 007 sha16 `83416f691e4ee6f0` |
| ORDEM 006 | cumprida | a release v407 (`RESULTADOS\006_RESULTADO.json`) |
| ORDEM 005 | cumprida | `RESULTADOS\005_RESULTADO.json` |
| ORDEM 004 | cumprida ou superada | como diz o quadro da ORDEM 006 |
| ORDENS 002 e 003 | esta ordem não as muda | o filme da v406 aguarda o operador escutar e decidir a voz |

— `claude-site-custodia`, em nome próprio, 05/11/2026.
