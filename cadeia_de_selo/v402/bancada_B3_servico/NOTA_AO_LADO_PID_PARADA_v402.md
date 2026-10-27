# NOTA AO LADO — o PID parado em 27/10/2026 (gerência c1, em nome próprio)

O `RECIBO_PARADA_v402.json` (sha256 e12a9e476a2b04aa834815f81f1034f86dc46ceb60bfaaac86251c49ea1d1f87) traz no campo `pid` o valor 67648, que o próprio script descreve como «último PID conhecido do serviço (religamento da v401, 25/10)». Esse não foi o processo parado hoje. Medido na hora pela gerência, antes da parada, por `Get-CimInstance Win32_Process -Filter "ProcessId=59072"`:

- PID **59072**, linha de comando `"C:\Python314\pythonw.exe" -X utf8 C:\IALD\Bancada_Um\um_bancada.py`, criado em 26/10/2026 22:13:33 (o serviço voltou nesse horário depois da queda de energia relatada pelo operador às 22:08).
- Parado por `Stop-Process -Id 59072` (pelo PID, nunca por nome), 27/10/2026 ~02:45; conferido em seguida: zero processos `um_bancada.py`, porta 18777 fechada. O recibo confere essas duas últimas condições e está correto nelas.
- Religado em 27/10/2026 02:48:19 com PID **892** (`RECIBO_RELIGAMENTO_v402.json`), pronta em 8 s, `B11-v402-20261027-R1`.

O recibo original não foi alterado (a cadeia já o leu no passo 10a com o sha256 acima). A correção vai ao lado, como manda a régua. Autorização: a ordem geral do operador para a conclusão do programa (a mesma da v401); o ato de parar foi da gerência, não do operador.
