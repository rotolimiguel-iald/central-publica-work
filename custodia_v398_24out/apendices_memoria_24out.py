# -*- coding: utf-8 -*-
"""Apêndices datados (24/10/2026): a rodada pública da v398 com a Etapa 1 do Kimi; a segunda custódia pela regra; o §7-D do organismo. Backup de bytes."""
import os, sys
from datetime import datetime
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
TS = datetime.now().strftime("%Y%m%d_%H%M%S"); AGORA = datetime.now().strftime("%d/%m/%Y %H:%M")
MEM = Path("C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory"); CEN = Path("C:/IALD/Central de Patentes")
def ap(p, texto):
    raw = p.read_bytes(); p.with_name(p.name + ".bak_" + TS).write_bytes(raw)
    nl = "\r\n" if b"\r\n" in raw else "\n"
    t = p.with_name(p.name + ".tmp_" + TS); t.write_bytes((raw.decode("utf-8").rstrip("\r\n") + nl + nl + texto.strip("\n").replace("\n", nl) + nl).encode("utf-8"))
    assert t.stat().st_size > len(raw); os.replace(t, p); print("ok", p.name, len(raw), "->", p.stat().st_size)
ap(MEM / "central-publica-22out.md", "## %s — a Central pública na v398 + a Etapa 1 do Kimi no ar\n\nRodada 20261024_095558 (27 passos, ~1h20): três repositórios publicados e conferidos; um.acom 88 arquivos (3.892.848 B, sha256 9eebda7db3d2fd4f); "
   "/central/ 1112 arquivos (76,9 MB), APROVADO — com a **Etapa 1 da leitura pública do Kimi** (home «A Central aberta», download de um.acom em um clique, descompactador, "
   "coleção por linhas; build `VITE_CENTRAL_PUBLICA=1 vite build --base=/central/ --outDir dist_publica`, feito no **PowerShell** porque o Git Bash converte `--base=/central/` "
   "em caminho do Windows). O painel do organismo (`Organismo.tsx`) só existe no cockpit privado (:8765, `/api/organismo`, admin). Quadro depois: 86 OK · 1 defasado (app v395). "
   "Regra que fica: antes de montar, conferir `src=\"/central/assets/` no `dist_publica/index.html`." % AGORA)
ap(MEM / "custodiar-quando-o-handoff-aparecer-23out.md", "## %s — a segunda custódia pela regra (v398) e as lições para o G1\n\n"
   "Disparo às 08:40 (quadro: 32 defasadas); espelho `35e8cdf6` 09:10; site 09:32; Central `df5f5ef0` 10:05; conferência 12/12; pública 11:20. ~2h40 de parede com "
   "quatro frentes em paralelo (G1, app, Kimi, pública). Método: scripts da Central **deslocados** da v397 por trocas ordenadas e protegidas (`derivar_central_v398.py`: "
   "versões, pinos, contagens, datas, base do snapshot; nomes protegidos: a pasta da ordem verbatim e `php_e_v396_22out`); espelho por trocas contadas; geradores com os "
   "DOIS parágrafos prontos do handoff (o quadro v397 conferido byte a byte igual ao do handoff v397). Defeitos do molde achados: `registro_vNNN_publicada` escreve «))» na linha do "
   "MEMORY.md; o patch do módulo dos dispositivos pede barra simples no USOS; `--base=/central/` só no PowerShell. **A Bancada Um e a memória canônica da fila já vêm com o selo (c1)**; "
   "o **app** não vinha (v395): a release virou perna da cadeia (fase A/B feitas; a troca do serviço ficou para o operador — o classificador barra matar/relançar o filho web)." % AGORA)
ap(CEN / "organismo" / "ORGANISMO_TORRE_DE_COMANDO.md", "## §7-D — AO LADO (%s, gerência a7): a segunda custódia pela regra, as pernas que faltavam e o limite da automação\n\n"
   "- **G2, segunda vez:** v398 (00:26) → custódia inteira pela regra, sem ordem nova; conferência 12/12; pública com a Etapa 1 do Kimi; quadro 86 OK · 1 defasado.\n"
   "- **Pernas medidas que não estavam no desenho:** a Bancada Um (recibo B(n)) e a memória canônica da fila (ACTIVE.json) vêm com o SELO (ato da c1 ao selar) — o quadro só confere; "
   "o **app** tem ciência própria (`iald_nucleo_fixo.json`) e estava em v395: a release do app (pipeline `work/iald_vNNN_*/app`, sem geração paga, construtor ≠ revisor) é perna da cadeia desde hoje.\n"
   "- **O limite:** a troca do serviço do app (terminar o filho web pelo PID e deixar o supervisor relançar) é ato que o classificador do modo automático barra à gerência; fica para o operador "
   "(rodar ou dar regra de permissão). Tudo até ali (build, contagem, revisão distinta, aceites, claim) é automático.\n"
   "- **G1 em construção** (fluxo woavllq66): `tools/custodiar.py` com vigia, sondar, planejar --seco e executar; validação por replay na v397/v398; lições do dia registradas no ACOM (p3)." % AGORA)
print("APÊNDICES OK")
