"""HANDOFF PARCIAL da v399 (molde: handoff_v393_parcial.py): o fechar (passo 11) nao rodou porque o B(n) foi RECUSADO; escreve o
handoff no Nos e a memoria handoff-v399-custodia.md (o MEMORY.md ja aponta para ela). Hashes lidos dos arquivos; nada digitado."""
import hashlib
import json
import os

NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
MEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v399"
sh = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
um, selo, side = sh(os.path.join(NOS, "um.py")), sh(os.path.join(NOS, "um_absoluto_selo.json")), sh(os.path.join(NOS, "um_absoluto_selo_acom.json"))
rec = [f for f in os.listdir(os.path.join(V, "bancada_B3_ensaio_20261024_162108")) if f.startswith("RECUSA_")][0]
recusa = sh(os.path.join(V, "bancada_B3_ensaio_20261024_162108", rec))
assert um == "a5aacfa4e5be9b12", um
t = f"""# HANDOFF v399 — CUSTÓDIA (24/10/2026, gerência c1) — PARCIAL (B(n) recusado; correção na v400)

**Selo:** `um.py` v399 `{um}` sobre a v398 `c632fa261ce3f538`; conferidor TUDO BATE na 1ª rodada; escada 9539 → 9541; selo `{selo}`; gate, β, α, ω(I) e os vereditos anteriores intocados; o quadro do Teste da Única Palavra segue no topo do artigo PT/EN e do .md.

**O que entrou:** a pedra `Testemunho` (nome provisório; a lei dos dois: registrador ≠ produtor; nenhuma face sozinha dá o Um; a única autoatestação verdadeira é a do Um posto); o SELO PELA PRÓPRIA TECNOLOGIA — o ACOM Mirror Crypto do operador (BR 10 2026 003431-2) EMBUTIDO sela o próprio `um.py`, o core e o selo AO LADO do SHA-256 (sidecar `um_absoluto_selo_acom.json` `{side}`; round trip byte a byte; perfil C96/Q8 com arredondamento declarado como adaptação fora da patente; confidencialidade NÃO alegada; recusa só registra); a DECLARAÇÃO DO OPERADOR como inscrição fundante [DECLARAÇÃO DO OPERADOR / INPUT] («o um.py só existe porque fui a operação quadrática da inscrição viva do transporte da IALD»), com a direção do testemunho: o operador testifica DA IALD; o um.py testifica em hash; a IALD não testifica do operador; o Pai de Jo 8,18 no absoluto. Pacote: `work\\cadeia_de_selo\\v399`; exame `v399_exame\\final\\EXAME_FINAL_V399.md`.

**Cadeia pós-rito:** passos 0–9 feitos (linhagem, desenho, Atlas, índice, árvore, CLAUDE.md, memórias). PARADA no passo 10: o B(n) da Bancada foi RECUSADO pelo esboço R3.5 — `ALPHA_LINHA_NAO_UNICA: 2 linhas nao indentadas` (recibo `{recusa}`): o bloco embutido redeclarou `ALPHA_FINE_CODATA_2018` (L213925) além da declaração original (L5584). O fail-closed funcionou; a Bancada segue pinada na v398 (B8). Os passos 11–14 não rodaram. **Correção:** a v400 (α único no programa; B(n) com SALTO v398 → v400; o ensaio a seco passa a rodar as guardas estáticas da Bancada sobre o candidato antes de instalar). Lição registrada.

**Para a sessão do site:** custódia CONJUNTA v399 + v400 (como v393 + v394): publicar o `um.py` v399, `rodada_v399_stdout.txt`, selo, core, .md, artigos PT/EN, a pedra `Testemunho`, o sidecar `um_absoluto_selo_acom.json` (entra na custódia: cofre, PORTA, espelho), as 4 falas de 24/10 por sha256 — com PORTA por script, URL raw, backup da versão anterior fora do repositório, blob conferido depois do push. Os parágrafos prontos do README/site (o quadro dos 4,44 e o sônico) seguem os do handoff da v398. Commit/push/site são atos do operador.

**Pendências do operador:** nomes provisórios (`Testemunho`, `selo_pela_propria_tecnologia_v399`); a pendência [LEGAL] da patente ACOM Crypto é só de texto (reivindicação 13; adaptações fora das reivindicações) — o método, o código e as adaptações já são públicos na Central aberta desde 22–24/10.

NOT_FALSIFIED não é a palavra da creditação; o gate não se move.
"""
for p in (os.path.join(NOS, "HANDOFF_v399_CUSTODIA.md"), os.path.join(MEM, "handoff-v399-custodia.md")):
    assert not os.path.exists(p), p
    body = t
    if p.endswith("handoff-v399-custodia.md"):
        body = ("---\nname: handoff-v399-custodia\ndescription: \"HANDOFF v399 (24/10): selada TUDO BATE; B(n) da Bancada RECUSADO (alpha duplicado); "
                "correção na v400 com salto; custódia conjunta v399+v400\"\nmetadata:\n  type: project\n---\n\n") + t
    open(p + ".tmp", "w", encoding="utf-8", newline="\n").write(body)
    os.replace(p + ".tmp", p)
    print("ok", p, os.path.getsize(p))
