# -*- coding: utf-8 -*-
"""03/11/2026 06:5x, gerencia c1: a nova regra do orquestrador (o app Claude em modo work, pelo tunel C:\\IALD\\TUNEL_CLAUDE_APP\\) e a ratificacao geral do operador
(verbatim sha16 b89e4c909f37e163) entram na memoria: topico novo (feedback), notas AO LADO nos dois topicos do Codex que ela supera, entrada datada no topico do
fechamento, UMA linha no indice (limites), pino e verificacao; e uma nota AO LADO na instrucao global (~/.claude/CLAUDE.md), na secao do navegador do ChatGPT.
Backup de BYTES antes de tocar cada arquivo; temporario -> os.replace. Escrito pelo Write."""
import os, subprocess, time
from pathlib import Path
MEMD = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"); FILA = MEMD / "fila"; MEM = MEMD / "MEMORY.md"
PY = r"C:\Python314\python.exe"; ENV = dict(os.environ, MEMORIA_GERENCIA="claude-c1"); TS = time.strftime("%Y%m%d_%H%M%S")
GLOBAL = Path(r"C:\Users\rotol\.claude\CLAUDE.md")
VERB = r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_03nov_prossigamos_com_tudo_ratifico_tudo_orquestrador_claude_app_readme_pinado_teste_d_verbatim.txt"


def troca_bytes(p, f, rot):
    b = p.read_bytes(); novo = f(b); assert novo != b
    bak = p.with_name(p.name + ".bak_" + TS + "_c1_" + rot); open(bak, "xb").write(b); assert bak.read_bytes() == b
    tmp = p.with_name(p.name + ".tmp_" + TS); open(tmp, "xb").write(novo); os.replace(tmp, p); assert p.read_bytes() == novo
    print("%s: %d -> %d B; backup %s" % (p.name, len(b), len(novo), bak.name))


def append(p, texto, rot):
    def f(b):
        nl = b"\r\n" if b"\r\n" in b else b"\n"
        return b.rstrip(b"\r\n") + nl + nl + texto.encode("utf-8") + nl
    troca_bytes(p, f, rot)


TOPICO = MEMD / "orquestrador-e-o-app-claude-03nov.md"
assert not TOPICO.exists()
TOPICO.write_text("""---
name: orquestrador-e-o-app-claude-03nov
description: "ORDEM do operador (02 e 03/11/2026): o orquestrador da IALD é o app Claude para Windows em modo work (membro claude-app-orquestrador), pelo túnel C:\\\\IALD\\\\TUNEL_CLAUDE_APP\\\\; herda do Codex a navegação, o X e a coordenação das IAs; as ordens da gerência vão para lá; as regras de 23/10 e 24/10 que diziam Codex leem-se app Claude."
metadata:
  type: feedback
---

# O orquestrador é o app Claude (02 e 03/11/2026, ordem do operador)

**Verbatim de 03/11 (sha16 `b89e4c909f37e163`, `work\\cunhagens_13out\\OPERADOR_03nov_prossigamos_com_tudo_ratifico_tudo_orquestrador_claude_app_readme_pinado_teste_d_verbatim.txt`):** «alteramos o orquestrador que passou a ser o claude, no modo work do app para windows, porque tem todas as funcionalidades do proprio codex, e já está funcionando, portanto, nós mudamos a regra do codex, para utilizar a sua própria estrutura, o que eu achei melhor inclusive. C:\\IALD\\TUNEL_CLAUDE_APP\\. … o orquestrador pode executar o que vc mandar». A ordem de 02/11 que abriu o caminho está em `C:\\IALD\\TUNEL_CLAUDE_APP\\OPERADOR_02nov_novo_orquestrador_verbatim.txt`; o contrato dele é a `ORDEM_001_novo_orquestrador.md` da mesma pasta (membro `claude-app-orquestrador`; não é a gerência; o Escritório fica fora; o que nunca faz sem o operador).

**A regra:** tudo o que antes virava ORDEM ao Codex pela web (GitHub, X, painéis, coordenação das IAs, filmes, vitrine, release do app) vira ORDEM ao app Claude, numerada, nesta pasta: `C:\\IALD\\TUNEL_CLAUDE_APP\\ORDEM_NNN_<slug>.md`, com o verbatim do operador ao lado e o recibo em `RELATORIO_<data>.md`; os depósitos de memória dele vão a `memory\\fila\\depositos\\claude-app\\`. A pasta `Chatgpt\\` segue SÓ LEITURA para toda sessão Claude: o que precisar da estrutura do Codex (memória canônica da fila, túnel do ChatGPT) é feito pela API ou fica dito como parede, nunca editado à mão. A leitura diária das patentes na WIPO continua na automação do Codex até o operador logar na WIPO no navegador do app. O Escritório continua com o seu canal próprio do Codex.

**Ratificação de 03/11 (mesmo verbatim):** «prossigamos com tudo, ratifico tudo»: as decisões D34 a D40 da gerência (handoff v406) estão ratificadas; o README pinado (D39) sai agora; o teste (d) do ramo B entra na v407 com a parametrização terminada; o app e o contrato do JEV passam a ser atualizados a cada versão, automático, pelo orquestrador sob ordem da gerência; o motor contínuo no pilar quântico (D38) e o lema do psíon entram pela v407 com pré-registro.

**Why:** o app Claude tem navegador próprio e as mesmas funcionalidades que o Codex oferecia, e o operador prefere a estrutura própria do Claude. **How to apply:** nunca devolver ao operador «faça você» quando o app pode fazer em modo seguro; a ordem vai escrita no túnel, com gate dito; o app executa e relata; o que ele traz é [DECLARADO] até a gerência conferir na fonte; nunca religar o transporte do Codex. Supera AO LADO [[codex-executa-o-que-eu-pediria-ao-operador-24out]] e a parte «web → Codex» de [[divisao-do-trabalho-iald-23out]]; ver [[publicacao-diaria-no-x-23out]] (o publicador do X já é o app desde 02/11).
""", encoding="utf-8")
print("topico novo:", TOPICO.name)
append(MEMD / "codex-executa-o-que-eu-pediria-ao-operador-24out.md",
       "**AO LADO (03/11/2026, gerência c1):** superada pela ordem do operador de 02 e 03/11: o executor das ordens da web é o app Claude em modo work (`C:\\IALD\\TUNEL_CLAUDE_APP\\`), não mais o Codex. Ver [[orquestrador-e-o-app-claude-03nov]].", "ao_lado_app")
append(MEMD / "divisao-do-trabalho-iald-23out.md",
       "**AO LADO (03/11/2026, gerência c1):** onde diz «navegação na internet → ChatGPT/Codex», leia-se «→ app Claude em modo work (`C:\\IALD\\TUNEL_CLAUDE_APP\\`)», por ordem do operador de 02 e 03/11; Kimi (desenho) e Claude (a subida) seguem. Ver [[orquestrador-e-o-app-claude-03nov]].", "ao_lado_app")
append(MEMD / "construir-tudo-o-fechamento-02nov.md",
       "**03/11, 06:5x — RATIFICAÇÃO GERAL e as frentes abertas (verbatim sha16 `b89e4c909f37e163`).** «prossigamos com tudo, ratifico tudo»: D34–D40 ratificadas. Ordens: testar a condição dele (sha16 `9978862f60cfbf29`: «deixa de ser conjectura sob hipótese se funcionar sob compressão elevando o potencial do resultado do código final em 1=1=HAJA_LUZ») com o operador matemático que a gerência nomeou em 02/11 (motor contínuo, D38, v407 com pré-registro); derivar o lema que liga `psion C` ao `psionCorner` (`linked_to_the_corner_by_a_lemma`), com o acervo de `C:\\IALD\\IMac LA\\Física - TGL`; o orquestrador passa a ser o app Claude (`C:\\IALD\\TUNEL_CLAUDE_APP\\`; [[orquestrador-e-o-app-claude-03nov]]); README pinado agora (D39); parametrização do teste (d) do ramo B para a v407; app e contrato JEV atualizados a cada versão, automáticos, pelo orquestrador. Frentes abertas em `work\\readme_pinado_03nov`, `work\\conjunto_D_20261029\\parametrizacao_03nov`, `work\\psion_lema_03nov`; ORDEM_004 ao app.", "ratificacao_03nov")
LINHA = ("- **[O ORQUESTRADOR É O APP CLAUDE (03/11)](orquestrador-e-o-app-claude-03nov.md)** — **ordem do operador**: o app Claude em modo work, pelo túnel `C:\\IALD\\TUNEL_CLAUDE_APP\\`, herda do Codex a web, o X e a coordenação; "
         "ordens da gerência numeradas lá; `Chatgpt\\` segue só leitura; regras de 23/10 e 24/10 superadas ao lado · **03/11: «ratifico tudo» (D34–D40)**")
ANC = b"- **[A DIVIS\xc3\x83O DO TRABALHO (23/10)](divisao-do-trabalho-iald-23out.md)**"


def f_mem(b):
    assert b.count(ANC) == 1
    nl = b"\r\n" if b"\r\n" in b else b"\n"
    novo = b.replace(ANC, LINHA.encode("utf-8") + nl + ANC)
    n_lin = novo.count(b"\n") + (0 if novo.endswith(b"\n") else 1)
    assert len(novo) <= 24000 and n_lin <= 195, "o indice estouraria: %d B, %d linhas" % (len(novo), n_lin)
    return novo


troca_bytes(MEM, f_mem, "linha_orquestrador_app")
for args in (["pinar"], ["verificar"]):
    q = subprocess.run([PY, "-X", "utf8", str(FILA / "memoria.py"), *args], cwd=str(FILA), env=ENV, capture_output=True, timeout=300)
    print("memoria.py %s -> rc %d" % (args[0], q.returncode)); assert q.returncode == 0, (q.stdout or q.stderr).decode("utf-8", "replace")[:400]
# a instrucao global: nota AO LADO na secao do navegador do ChatGPT (antes do separador que precede «O NÚCLEO DA TGL»)
ANC_G = "---\n\n## O NÚCLEO DA TGL"
NOTA_G = ("> ⚠ **AO LADO (03/11/2026, gerência c1, por ordem do operador de 02 e 03/11, verbatim sha16 `b89e4c909f37e163`):** o ORQUESTRADOR da IALD passou a ser o **app Claude para Windows em modo work** "
          "(membro `claude-app-orquestrador`, túnel `C:\\IALD\\TUNEL_CLAUDE_APP\\`, contrato `ORDEM_001_novo_orquestrador.md`): ele herda do Codex a navegação, a publicação no X e a coordenação das IAs, e executa o que a gerência "
          "mandar por ORDEM numerada naquela pasta. O que acima diz «pede-se ao ChatGPT» lê-se «pede-se ao app Claude»; a pasta `Chatgpt\\` segue só leitura; o canal do Escritório não muda. Memória: `orquestrador-e-o-app-claude-03nov.md`. <!-- orquestrador_app_claude_03nov -->\n\n")


def f_glob(b):
    s = b.decode("utf-8"); assert s.count(ANC_G) == 1 and "orquestrador_app_claude_03nov" not in s
    return s.replace(ANC_G, NOTA_G + ANC_G).encode("utf-8")


troca_bytes(GLOBAL, f_glob, "orquestrador_app")
print("OK: memoria e instrucao global atualizadas")
