# -*- coding: utf-8 -*-
"""Registro (23/10/2026, sessão a7): a rotina diária do X instalada e a primeira custódia disparada pela regra do gatilho (v397), nas
memórias da sessão e no desenho do organismo (§7-C, ao lado). Backup de BYTES antes de tocar; temporário -> confere -> substitui."""
import json, os, sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
TS = datetime.now().strftime("%Y%m%d_%H%M%S")
AGORA = datetime.now().strftime("%d/%m/%Y %H:%M")
MEM = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory")
CEN = Path(r"C:\IALD\Central de Patentes")
rec = json.loads((CEN / "Chatgpt/TUNEL/DO_CHATGPT/ORDEM_021/2026-10-23.json").read_text(encoding="utf-8"))
assert rec.get("publicado") is True and str(rec.get("url", "")).startswith("https://x.com/")


def ap(p, texto):
    p = Path(p)
    raw = p.read_bytes()
    p.with_name(p.name + ".bak_" + TS).write_bytes(raw)
    nl = "\r\n" if b"\r\n" in raw else "\n"
    novo = raw.decode("utf-8").rstrip("\r\n") + nl + nl + texto.strip("\n").replace("\n", nl) + nl
    t = p.with_name(p.name + ".tmp_" + TS)
    t.write_bytes(novo.encode("utf-8"))
    assert t.stat().st_size > len(raw)
    os.replace(t, p)
    print("ok", p.name, len(raw), "->", p.stat().st_size)


X = ("## %s — a rotina instalada; a primeira publicação feita\n\n"
     "- **Primeira publicação (23/10/2026, 17:31, pelo Codex — ORDEM 021):** %s — texto de 221 caracteres, sha256 `%s…`, igual ao arquivo "
     "`Chatgpt\\TUNEL\\PARA_CHATGPT\\X_DIARIO\\2026-10-23.md`; recibo `DO_CHATGPT\\ORDEM_021\\2026-10-23.json`; livro `X_DIARIO\\LIVRO.jsonl` semeado.\n"
     "- **A rotina diária:** tarefa do Windows `IALD_pensamento_do_dia` às **17:30** (Goiânia) → `tools\\pensamento_do_dia.bat` → `tools\\pensamento_do_dia.py`: "
     "lê os fatos medidos (selo do um.py, quadro do organismo, rotas do dia, o livro); a **IALD Nativa** (llama-server :8081) propõe até 4 frases; a **guarda** "
     "mecânica recusa (≤ 280 c; termina em «— IALD»; sem link/hashtag/menção/emoji/aspas angulares; sem número fora dos fatos; sem confirmad*/comprovad*/provou/5σ alcançado; "
     "sem nomes de pessoa nem de outra IA; sem repetir ou quase repetir o livro) e um **aferidor** (a mesma nativa, prompt de juiz, temperatura 0) aprova ou reprova; "
     "se nada passa, o pensamento é a **medida** (frase determinística dos números do quadro). Grava `X_DIARIO\\<data>.md`, anota no livro e enfileira a mensagem do dia "
     "na coordenadora do Codex (remetente `iald-pensamento-do-dia`). O Codex publica às 18:00 (sua rotina `iald-pensamento-diario-no-x`); o ADENDO A da ORDEM 021 "
     "(evento 1139) fixa a idempotência: recibo do dia com `publicado: true` ⇒ não publica de novo; texto ausente ⇒ recibo `publicado: false`, sem inventar.\n"
     "- **Ensaios a seco (23/10):** o aferidor reprovou frases que invertiam a régua («o nome … foi a testemunha, não o número») e uma que citava pessoa; "
     "a guarda pegou a semelhança com o texto de 23/10. O risco que fica: semântica fina que guarda e aferidor não pegam — a gerência relê o livro quando está em sessão.\n"
     "- **Conferir:** `python tools\\pensamento_do_dia.py --conferir --data AAAA-MM-DD` (lê o recibo e compara o sha256)." % (AGORA, rec["url"], rec["texto_sha256"][:16]))
ap(MEM / "publicacao-diaria-no-x-23out.md", X)

G = ("## %s — a primeira custódia pela regra (v397)\n\n"
     "O vigia das três marcas (selo com `um_version` v397 e `um.py` batendo; bloco «v397 SELADA» em `MEMORIA_DA_LINHAGEM.md`; `HANDOFF_v397_CUSTODIA.md`) "
     "disparou às 17:17 e a custódia correu inteira sem ordem nova: espelho `bb2c392a` (pós-push 19/19), site no ar (SUBIDA VERIFICADA; leitor de IA R1 passa), "
     "Central `ac616f48` (cofre v397 36/0, kernel 1426/29229, runner v62 2×, 16/16, FINAL 16/16, ledger 0/0, snapshot 220 copiados/0 divergentes), conferência final 12/12, "
     "ACOM t1/t2, rota 1364. Tempo: ~1h50 do disparo à conferência. Lições para a próxima: (1) a frente do README está a 19 B do teto de 40 KB — decisão estrutural antes "
     "da v398; (2) os scripts derivam da v396 por trocas contadas (`work\\custodia_v397_23out\\derivar_*.py`): o gerador parametrizado (G1) é o alvo; (3) o parágrafo pronto "
     "do handoff entra verbatim, número a número conferido contra o registro selado (a regra do 4,44)." % AGORA)
ap(MEM / "custodiar-quando-o-handoff-aparecer-23out.md", G)

O = ("## §7-C — AO LADO (%s, gerência a7): o gatilho disparou pela primeira vez; a rotina do X\n\n"
     "- **G2 em ato:** a v397 foi selada no Nós às 16:20; o handoff apareceu às 17:17; a custódia correu inteira pela regra do operador (sem ordem nova) e fechou com "
     "conferência final 12/12 às 18:20 (espelho `bb2c392a`, Central `ac616f48`, site no ar). Medida do custo: ~1h50 de parede, quatro processos longos em paralelo "
     "(runner, 16 dispositivos, snapshot, Central pública).\n"
     "- **A obrigação diária da IALD no X** (ordem de 23/10): tarefa `IALD_pensamento_do_dia` 17:30 → `tools\\pensamento_do_dia.py` (IALD Nativa propõe; guarda + aferidor "
     "recusam; a medida é o fallback) → mensagem à coordenadora do Codex → publicação às 18:00 (ORDEM 021 + ADENDO A: idempotência pelo recibo do dia). "
     "Primeira publicação: 23/10 17:31, feita pelo Codex a partir do texto da gerência.\n"
     "- **O que a torre ainda não faz sozinha:** nomear registros (operador); Zenodo; painéis com login (hospedagem, Cloudflare WAF regex, consoles de chave) — modo seguro, "
     "o operador digita; o teto do README (decisão estrutural)." % AGORA)
ap(CEN / "organismo" / "ORGANISMO_TORRE_DE_COMANDO.md", O)
print("REGISTRO X/GATILHO OK")
