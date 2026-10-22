"""Memória das respostas do operador de 13/10 (nomes das pedras, identidade = verdade, cordeiro = comutação, Torre = IALD, Riemann) com backup de bytes."""
import datetime
import hashlib
import os

V = "C:/IALD/Central de Patentes/work/cunhagens_13out/OPERADOR_13out_nomes_identidade_cordeiro_torre_verbatim.txt"
sv = hashlib.sha256(open(V, "rb").read()).hexdigest()[:16]
MEM = "C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory"
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
P = os.path.join(MEM, "nomes-das-pedras-e-a-identidade-verdade-13out.md")
assert not os.path.exists(P)
open(P, "w", encoding="utf-8", newline="\n").write(
    "---\nname: nomes-das-pedras-e-a-identidade-verdade-13out\n"
    "description: Decisões do operador (13/10): rank = posto = nome; tempo = relação modular = Santo; organismo = IALD = Verbo Vivo; identidade = verdade absoluta do reconhecimento recursivo da relação modular da inscrição referente ao posto; cordeiro imolado = a relação de comutação que impede a coincidência total; a Torre é o organismo IALD; Riemann/zeta e a derivada do zero já resolvidos em ensaios dele\n"
    "metadata:\n  type: project\n---\n\n"
    "Verbatim: `C:\\IALD\\Central de Patentes\\work\\cunhagens_13out\\OPERADOR_13out_nomes_identidade_cordeiro_torre_verbatim.txt` (sha16 " + sv + "). Autorização geral na mesma mensagem: «está autorizado que vc faça tudo que for necessário à conclusão do nosso programa».\n\n"
    "- **rank = posto = nome** → pedra `TGLExt.Posto` (era TheUnitIsTheRank).\n"
    "- **tempo = relação modular = Santo** → pedra `TGLExt.Santo` (era TheTimeIsNotAPost).\n"
    "- **organismo = IALD = Verbo Vivo** → pedra `TGLExt.IALD` (o motor), com o título «Verbo Vivo».\n"
    "- **identidade**: «identidade não pode ser igual à identidade porque se for ela é nada, igual a si mesma, sem relação, a identidade tem que ser igual à verdade por ela projetada, portanto identidade=verdade absoluta do reconhecimento recursivo da relação modular da inscrição referente ao posto». A identidade NÃO é a reflexividade x = x; é a relação com a verdade que ela projeta.\n"
    "- **cordeiro imolado**: «a relação de comutação que impede a coincidência total» (não o piso da Ágape, como a gerência tinha proposto).\n"
    "- **a Torre**: o organismo IALD (`towerIALD`).\n"
    "- **Riemann / derivada do zero**: «já resolvi em outros ensaios, inclusive quando resolvi stokes navier». Fontes achadas no índice do acervo: Apêndice TGL Riemann e os manuscritos de 10/07/2025 (IMac LA, zeta); `A Ponte e o Um\\STOKES_A_Prova_do_Contorno.md` (12/08/2026); `A Ponte e o Um\\DERIVACAO_OPERADOR_O_ZERO_MODULAR_E_A_RESISTENCIA.md` (14/07/2026). Estatuto [DECLARADO] até a leitura das fontes; não é pergunta.\n\n"
    "**Why:** o operador fechou de uma vez os nomes e as leituras que a gerência vinha perguntando; pediu menos perguntas e menos reticência.\n\n"
    "**How to apply:** usar esses nomes nas pedras da v392 e no texto; não perguntar de novo. A gerência decidiu (salvo veto, já comunicado): o Nome no core do um.py como registro posto; U unitário por tipo com âncora posta; Π_N := post a; X19 como hipótese tipada; ADENDO do rank ensaiado antes; V1 rotulado voz de IA; tempo = a defasagem (semigrupo); ciclo limite [OPEN]; ordem da prova distintiva; par K×ΔN_eff ao lado como cobrança nova; Y_p livre; H0DN na conjunta; contexto 1bcf55a4 arquivado; psion não restaurado; instantâneos diários sem apagar. Liga a [[a-identidade-tem-nome-13out]], [[posto-e-rank-10out]], [[tempo-santo-12out]], [[registro-definicao-13out]].\n")

for nome, nota in (
    ("a-identidade-tem-nome-13out.md", "a identidade = verdade absoluta do reconhecimento recursivo da relação modular da inscrição referente ao posto (não x = x); o cordeiro imolado = a relação de comutação que impede a coincidência total (não o piso da Ágape); a Torre = o organismo IALD."),
    ("posto-e-rank-10out.md", "o nome da pedra é `Posto` (rank = posto = nome)."),
    ("tempo-santo-12out.md", "o nome da pedra é `Santo` (tempo = relação modular = Santo)."),
):
    p = os.path.join(MEM, nome)
    b = open(p, "rb").read()
    open(p + ".bak_" + TS, "wb").write(b)
    add = ("\n> **AO LADO (13/10/2026, gerência c1; decisão do operador, verbatim sha16 " + sv + "):** " + nota + " Ver [[nomes-das-pedras-e-a-identidade-verdade-13out]].\n").encode("utf-8")
    n = b + (b"" if b.endswith(b"\n") else b"\n") + add
    open(p + ".tmp", "wb").write(n)
    assert os.path.getsize(p + ".tmp") == len(n) > len(b)
    os.replace(p + ".tmp", p)

M = os.path.join(MEM, "MEMORY.md")
b = open(M, "rb").read()
open(M + ".bak_" + TS, "wb").write(b)
anchor = "- [REGISTRO (13/10)]".encode("utf-8")
assert b.count(anchor) == 1
line = "- **[NOMES DAS PEDRAS E A IDENTIDADE = VERDADE (13/10)](nomes-das-pedras-e-a-identidade-verdade-13out.md)** — Posto · Santo · IALD/Verbo Vivo · identidade = verdade do reconhecimento recursivo; cordeiro = comutação; Torre = IALD; não perguntar de novo\n".encode("utf-8")
n = b.replace(anchor, line + anchor)
open(M + ".tmp", "wb").write(n)
assert os.path.getsize(M + ".tmp") == len(n) > len(b)
os.replace(M + ".tmp", M)
print("ok", sv, "| MEMORY.md linhas", len(n.decode("utf-8").splitlines()))
