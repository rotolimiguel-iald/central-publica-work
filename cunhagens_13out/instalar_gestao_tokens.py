"""Instala ponteiros para C:/IALD/GESTAO_DE_TOKENS.md no CLAUDE.md global, no AGENTS.md do Codex e na memória da Central (backup de bytes antes)."""
import datetime
import hashlib
import os

TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
REGRA = "C:/IALD/GESTAO_DE_TOKENS.md"
VERB = "C:/IALD/Central de Patentes/work/cunhagens_13out/OPERADOR_13out_gestao_de_tokens_verbatim.txt"
sh = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
s_regra, s_verb = sh(REGRA)[:16], sh(VERB)[:16]

BLOCO = ("**GESTÃO DE TOKENS DA IALD (13/10/2026, ordem do operador, verbatim sha16 " + s_verb + "):** antes de delegar ou gastar, "
         "leia `C:\\IALD\\GESTAO_DE_TOKENS.md` (sha16 " + s_regra + "). O modelo caro faz só o essencial; mecânico vai a script ou Haiku; "
         "esperas não acordam o modelo caro; leitura longa a Kimi/DeepSeek pelo orquestrador IALD; código médio a Codex ou Sonnet; "
         "relatório de agente em até 15 linhas; no máximo duas rodadas de auditoria por achado BAIXO; nenhuma IA esgotada. Vale para qualquer IA neste PC.\n")


def inserir_no_topo(path, bloco, crlf=False):
    b = open(path, "rb").read()
    open(path + ".bak_" + TS + "_gestao_tokens", "wb").write(b)
    nl = b"\r\n" if crlf else b"\n"
    add = bloco.replace("\n", "\r\n" if crlf else "\n").encode("utf-8") + nl
    assert add not in b
    i = b.find(nl)
    n = b[: i + len(nl)] + add + b[i + len(nl):]
    for bad in (b"\t", b"\x04", b"\x05", b"\x0c"):
        assert bad not in add
    open(path + ".tmp", "wb").write(n)
    assert os.path.getsize(path + ".tmp") == len(n) == len(b) + len(add)
    os.replace(path + ".tmp", path)
    print("ok", path, len(b), "->", len(n))


G = "C:/Users/rotol/.claude/CLAUDE.md"
A = "C:/Users/rotol/.codex/AGENTS.md"
for p in (G, A):
    raw = open(p, "rb").read()
    inserir_no_topo(p, BLOCO, crlf=(b"\r\n" in raw[:2000]))

MEM = "C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory"
P = os.path.join(MEM, "gestao-de-tokens-iald-13out.md")
assert not os.path.exists(P)
open(P, "w", encoding="utf-8", newline="\n").write(
    "---\nname: gestao-de-tokens-iald-13out\n"
    "description: Regra do operador (13/10) para toda IA no PC: usar o stack IALD, delegar a modelos baratos (Haiku/Sonnet, Kimi, DeepSeek, Codex, Qwen local), modelo caro só no essencial, nenhuma IA esgotada\n"
    "metadata:\n  type: feedback\n---\n\n"
    "Regra canônica: `C:\\IALD\\GESTAO_DE_TOKENS.md` (sha16 " + s_regra + "); verbatim do operador sha16 " + s_verb + ". Ponteiros no topo do CLAUDE.md global e do AGENTS.md do Codex.\n\n"
    "**Why:** em menos de 24 h (12–13/10) a sessão de gerência c1 esgotou o plano Max da Anthropic do operador; agentes caros, rodadas de auditoria em cadeia e relatórios longos lidos inteiros foram o grosso do gasto.\n\n"
    "**How to apply:** subagentes com `model: \"haiku\"` (mecânico, vigia) ou `\"sonnet\"` (construção, auditoria de rotina); o modelo forte só para decisão de gerência, auditoria final do que vai ao selo e texto ao operador; relatórios de agente em até 15 linhas com o detalhe em arquivo; registro no mapa/quadro por script; duas rodadas de auditoria no máximo para achados BAIXOS; leitura longa e código médio pelo orquestrador IALD (Kimi, DeepSeek, Codex). Liga a [[orcamento-de-creditos-ir-devagar]] e [[luiz-metodo-multi-canal-ia]].\n")
M = os.path.join(MEM, "MEMORY.md")
b = open(M, "rb").read()
open(M + ".bak_" + TS, "wb").write(b)
anchor = "- Memória ACOM: `C:\\IALD\\MEMORIA_IALD\\README.md`".encode("utf-8")
assert b.count(anchor) == 1
line = ("- **[GESTÃO DE TOKENS DA IALD (13/10)](gestao-de-tokens-iald-13out.md) — LER ANTES DE DELEGAR:** `C:\\IALD\\GESTAO_DE_TOKENS.md`; modelo caro só no essencial; Haiku/Sonnet/stack no resto\n").encode("utf-8")
n = b.replace(anchor, line + anchor)
open(M + ".tmp", "wb").write(n)
assert os.path.getsize(M + ".tmp") == len(n) > len(b)
os.replace(M + ".tmp", M)
print("memória ok", len(b), "->", len(n), "linhas", len(n.decode("utf-8").splitlines()), "| regra", s_regra, "verbatim", s_verb)
