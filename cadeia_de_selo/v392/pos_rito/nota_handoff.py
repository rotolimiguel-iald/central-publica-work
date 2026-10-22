import datetime
import os

nota = """

> **AO LADO (13/10/2026 19:00, gerência c1) — para a sessão irmã do site, que faz a custódia no GitHub:**
> 1. O selo v392 está COMPLETO no Nós: conferidor TUDO BATE (deve mudar 18/18; não pode mudar 11/11); gate, β, α e ω(I) intocados; o B(3) da Bancada aplicado e o serviço religado servindo v392 (manifesto `6733b9a28c725244`).
> 2. Houve duas tentativas de rito antes desta (registro em `work\\cadeia_de_selo\\v392\\tentativa1_rito_falhou_*`): a 1ª morreu na cobertura KH-N1 (linha de total lida 2×), a 2ª selaria com o índice da IALD não selado; ambas revertidas pelos backups de bytes. Só a 3ª (`b590c0aa80055e2a`) está no Nós. Não publicar artefato das tentativas como se fosse o selo.
> 3. O passo 13 da cadeia (inventário da bancada do ChatGPT) parou: o gerador achou um arquivo com marca de controle FORA das pastas de controle (`work\\inventario_bancada\\gerar_documento.py` l.116). É questão da bancada, não do selo; o inventário de 27/09 segue o vigente até a gerência examinar. O passo 14 (Nós vivo) rodou.
> 4. Os servidores MCP das sessões caíram às 13/10 ~10h (incidente de um subagente); reconectar com /mcp é do operador.
> 5. Ordem do operador de 13/10: «ao terminar escreva o handoff para a custódia do um.py no repositório do github para a sessão irmã». Commit, push e site seguem atos do operador e da sessão do site.
"""
for p in (r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\HANDOFF_v392_CUSTODIA.md",
          r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\handoff-v392-custodia.md"):
    b = open(p, "rb").read()
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    open(p + ".bak_" + ts, "wb").write(b)
    n = b + (b"" if b.endswith(b"\n") else b"\n") + nota.encode("utf-8")
    open(p + ".tmp", "wb").write(n)
    assert os.path.getsize(p + ".tmp") == len(n) > len(b)
    os.replace(p + ".tmp", p)
    print("ok", p, len(b), "->", len(n))
