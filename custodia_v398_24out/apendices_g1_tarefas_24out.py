# -*- coding: utf-8 -*-
r"""Apêndices (24/10/2026, 15h): §7-E do organismo (G1 instalado em modo sombra; L17), a lição das tarefas do Windows (caminho com espaço),
a memória de referência nova e a linha do índice. Backup de bytes; temporário → confere → substitui."""
import os, sys
from datetime import datetime
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
TS = datetime.now().strftime("%Y%m%d_%H%M%S"); AGORA = datetime.now().strftime("%d/%m/%Y %H:%M")
MEM = Path("C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory"); CEN = Path("C:/IALD/Central de Patentes")
BS = chr(92)
FORMA = 'schtasks --% /Create ... /TR "' + BS + '"C:' + BS + '...' + BS + 'x.bat' + BS + '""'   # a forma que funciona, montada sem escapes


def ap(p, texto):
    raw = p.read_bytes(); p.with_name(p.name + ".bak_" + TS).write_bytes(raw)
    nl = "\r\n" if b"\r\n" in raw else "\n"
    t = p.with_name(p.name + ".tmp_" + TS); t.write_bytes((raw.decode("utf-8").rstrip("\r\n") + nl + nl + texto.strip("\n").replace("\n", nl) + nl).encode("utf-8"))
    assert t.stat().st_size > len(raw); os.replace(t, p); print("ok", p.name, len(raw), "->", p.stat().st_size)


ap(CEN / "organismo" / "ORGANISMO_TORRE_DE_COMANDO.md", "## §7-E — AO LADO (%s, gerência a7): G1 entregue e instalado em modo sombra; a decisão L17\n\n"
   "- **G1** (`tools/custodiar.py` + `tools/custodia_g1`, commit `574b4683`; G1.0 `979f5937`): uma ordem por versão — `vigiar · sondar · planejar --seco · executar · auditar`; 46/46 testes; "
   "códigos 0/5/10/20/30; commit/push/`--publicar` só com `--publicar`. O vigia roda a cada 30 min como tarefa do Windows (`IALD_vigia_da_custodia` → `vigia.bat`) em **MODO SOMBRA**: "
   "lê as três marcas, grava `work/custodia_G1/VIGIA_ULTIMO.json` e, quando uma versão nova estiver selada, o `PLANO_vNNN.json` — nunca executa, nunca publica. Hoje: v398 custodiada; o Nós EM_OBRA (v399).\n"
   "- **L17 (decisão do operador):** se o vigia pode ligar `executar` e `--publicar` sozinho. Proposta da gerência: a v399 corre `planejar → executar` supervisionada pela gerência, depois `--publicar`; "
   "a partir de N = 2 custódias sem erro, o vigia executa sozinho e a gerência só confere o quadro.\n"
   "- **Lição medida:** tarefas do Windows criadas do PowerShell com `/TR '\"caminho com espaço\"'` ficam com a ação truncada (resultado 0x80070002: a tarefa do HSTS de 23/10 e, até hoje às 15:07, "
   "a do pensamento do dia e a do vigia). A forma certa: `%s` — e conferir com `/Run` + o arquivo regravado." % (AGORA, FORMA))
ap(MEM / "publicacao-diaria-no-x-23out.md", "## %s — a tarefa das 17:30 estava QUEBRADA (caminho truncado); refeita e conferida\n\n"
   "A tarefa `IALD_pensamento_do_dia`, criada ontem do PowerShell com `/TR '\"...\"'`, tinha a ação truncada no espaço de «Central de Patentes» (o mesmo defeito derrubou a tarefa do HSTS às 21:15 de 23/10, "
   "resultado 0x80070002). Recriada hoje com a forma `%s`; a do vigia, criada do mesmo jeito, foi disparada com `/Run` e regravou o seu arquivo (prova de que o caminho chega inteiro). "
   "Primeira rodada real do pensamento: hoje 17:30." % (AGORA, FORMA))
p = MEM / "schtasks-caminhos-com-espaco-24out.md"
p.write_text("---\nname: schtasks-caminhos-com-espaco-24out\ndescription: Tarefas agendadas do Windows criadas pelo PowerShell com caminho com espaço ficam com a ação truncada (0x80070002); usar schtasks --% com o caminho entre aspas escapadas e conferir com /Run + arquivo regravado\nmetadata:\n  type: reference\n---\n\n"
   "# schtasks + PowerShell + caminho com espaço (24/10/2026)\n\n"
   "**Defeito medido:** `schtasks /Create ... /TR '\"C:/IALD/Central de Patentes/x.bat\"'` (PowerShell) grava a ação truncada no primeiro espaço; a tarefa «executa» e devolve `-2147024894` (0x80070002, arquivo não encontrado), "
   "sem log. Derrubou: `IALD_HSTS_fase2_20261023` (21:15 de 23/10), e teria derrubado `IALD_pensamento_do_dia` (17:30) e `IALD_vigia_da_custodia`.\n\n"
   "**Forma que funciona (conferida com /Run e o arquivo de saída regravado):**\n\n```powershell\n" + FORMA.replace("...", "Central de Patentes/tools").replace("x.bat", "pensamento_do_dia.bat") + "\n```\n\n"
   "(o `--%` manda o PowerShell passar o resto verbatim; cada aspa interna vai escapada com barra invertida.)\n\n"
   "**Como conferir sempre:** `schtasks /Run /TN <nome>`, esperar, e medir o efeito (mtime do arquivo que o .bat escreve); `schtasks /Query /TN <nome> /V /FO LIST` → «Último resultado» (0 ou o rc do script; 0x80070002 = caminho errado). "
   "Relacionado: [[publicacao-diaria-no-x-23out]], [[custodiar-g1-24out]].\n", encoding="utf-8")
print("criado", p.name)
M = MEM / "MEMORY.md"; raw = M.read_bytes(); s = raw.decode("utf-8"); nl = "\r\n" if "\r\n" in s else "\n"
anc = [l for l in s.split(nl) if l.startswith("- [Bash tool: heredoc colapsa barras")]; assert len(anc) == 1, anc
nova = "- [schtasks + caminho com espaço (24/10)](schtasks-caminhos-com-espaco-24out.md) — do PowerShell, `--%` e aspas escapadas no /TR; conferir com `/Run` + arquivo regravado (0x80070002 = ação truncada)"
assert nova not in s
s = s.replace(anc[0], anc[0] + nl + nova, 1); M.with_name(M.name + ".bak_" + TS).write_bytes(raw)
t = M.with_name(M.name + ".tmp"); t.write_bytes(s.encode("utf-8")); assert t.stat().st_size < 24 * 1024, t.stat().st_size; os.replace(t, M); print("MEMORY.md:", len(raw), "->", M.stat().st_size)
