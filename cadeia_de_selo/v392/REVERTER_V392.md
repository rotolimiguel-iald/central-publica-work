# REVERTER_V392 -- receita de reversão da instalação (escrita em 13/10/2026; atende B2 da auditoria c1)

Quando usar: o `instalar_v392.py` rodou e o rito falhou no meio (ou a gerência decidiu voltar). Não é ato automático: é ato da gerência, com o `um.py` parado.

Nó = `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós`. `<ts>` = o carimbo do `APLICADO_AO_CANONICO_<ts>.json` (na pasta desta cadeia), igual ao sufixo `.bak_<ts>` dos 8 backups.

1. Conferir que nenhum `um.py` nem trabalhador do pilar roda (nada de `rito_v392`; ver `.rito_v392.pid`). Se o servidor do modelo ficou parado pelo rito, o marcador `.servidor_parado_pelo_rito` na pasta da cadeia diz se ele deve ser religado (`Start-ScheduledTask 'IALD Llama Server'`).
2. Restaurar os 8 backups de BYTES (cópia de bytes, nunca texto reencodado; conferir o sha256 contra `APLICADO_AO_CANONICO_<ts>.json`), cada `X.bak_<ts>` sobre `X`:
   - `um.py`
   - `um_absoluto.json`
   - `um_absoluto_selo.json`
   - `um_absoluto_forma_canonica.md`
   - `um_absoluto_manifest.md`
   - `um_absoluto_pilar_quantico.json`
   - `tgl_kernel\TGLExt.lean`
   - `tgl_kernel\TGL\Audit.lean`
   Para cada um: `copy` do `.bak_<ts>` para um temporário na mesma pasta, conferir tamanho e sha256, `os.replace`. Depois confirmar que o `um.py` voltou a `8e7b9927ceae64b8` (sha16, a v391).
3. As 14 pedras novas em `tgl_kernel\TGLExt\*.lean` (as chaves de `ESPERADOS_v392.json` em `pedras_sha256`) ficam no disco sem import: inofensivas para a v391, mas um novo `instalar_v392.py` RECUSA se alguma já existir. Antes de reinstalar, mover as 14 (e só elas) para uma quarentena datada fora do Nós, por exemplo `...\cadeia_de_selo\v392\quarentena_pedras_<ts2>\`; não apagar.
4. Os `.olean` correspondentes em `tgl_kernel\.lake\build` são regenerados pelo build; se o próximo rito for da v391, o `lake build` os ignora (sem import). Não é preciso apagá-los.
5. O `pilar_anterior_v391_<ts>\` (cópia de bytes do resultado do pilar) fica guardado na pasta da cadeia; o cache do pilar não é alterado pelo instalar.
6. Se o rito chegou a gravar `rodada_v392_stdout.txt` (e tentativas) no Nós, guardá-las com a pasta da cadeia como registro; não apagar.
7. Conferir: `um.py` v391 sha16 `8e7b9927ceae64b8`, as 8 releituras iguais aos backups, e `python -I -B -X utf8 conferir_rito_v392.py` deve dar `tudo_bate: false` (é o controle negativo: a v391 é o que está instalado).
