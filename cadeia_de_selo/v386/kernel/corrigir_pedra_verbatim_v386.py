# -*- coding: utf-8 -*-
"""corrigir_pedra_verbatim_v386.py -- corrige as DOCSTRINGS da pedra TGLExt/TheVerbSelectsTheAction.lean (SANDBOX v376/kernel_src; nunca o Nos) para que
toda citacao «» do operador seja VERBATIM (inclusive erros de digitacao, com [sic] FORA das «») e todo corte traga «…». Nenhum enunciado, nome ou prova muda:
so' texto de comentario. Backup de BYTES (.bak_<ts>) na mesma pasta ANTES de tocar; cada `old` deve ocorrer exatamente N vezes (N dito); tempario -> tamanho
-> substituir; LF preservado (o arquivo nao tem CRLF). Imprime o sha256 antes/depois e grava CORRECAO_PEDRA_v386.json com a lista do que mudou.
uso: python corrigir_pedra_verbatim_v386.py"""
import hashlib, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SP = os.path.dirname(os.path.dirname(HERE))
KS = os.path.join(SP, "v376", "kernel_src")
P = os.path.join(KS, "TGLExt", "TheVerbSelectsTheAction.lean")
sha = lambda b: hashlib.sha256(b).hexdigest()
raw0 = open(P, "rb").read()
assert raw0.count(b"\r\n") == 0, "a pedra tinha CRLF; o script supoe LF"
ts = time.strftime("%Y%m%d_%H%M%S")
bak = P + ".bak_" + ts
assert not os.path.exists(bak)
open(bak, "wb").write(raw0)
assert open(bak, "rb").read() == raw0
T = raw0.decode("utf-8")

# (old, new, n_ocorrencias, o_que) -- a ordem segue o arquivo
R = [
    # cabecalho: a terceira fonte (uma frase vem do transcrito, nao dos dois arquivos)
    ("   `scratchpad/v386/RESPOSTAS_operador_05out.txt` (sha256 b49b0d9e60ee4646…)]\n",
     "   `scratchpad/v386/RESPOSTAS_operador_05out.txt` (sha256 b49b0d9e60ee4646…); e UMA frase (§5, «estado dinâmico estacionado») vem\n"
     "   da mensagem do operador de 2026-10-05T11:19:54 UTC no transcrito desta sessão, conferida por script — dita onde é citada]\n",
     1, "cabeçalho l.14: declara a 3ª fonte (a mensagem de 11:19:54 UTC do transcrito) da citação de §5"),
    # l.21: a formula do operador TAL QUAL (LaTeX), com a regua do signo AO LADO, fora das «»
    ("fossilizado … Nome = lim_{t→∞} 𝒱(t) … O nome é o autovetor do operador verbo»; «[𝒱_nome, 𝒱_tempo] = i·(constante)·𝒱_verdade»\n"
     "(e as duas cíclicas) — «A Constante de Miguel é a constante de estrutura»; «O universo é o grupo de Lie gerado por esses\n"
     "três operadores. A TGL é a sua álgebra.»\n",
     "fossilizado … Nome = lim_{t→∞} 𝒱(t) … O nome é o autovetor do operador verbo»;\n"
     "«[\\mathcal{V}_{\\text{nome}}, \\mathcal{V}_{\\text{tempo}}] = i\\alpha^2 \\, \\mathcal{V}_{\\text{erdade}}» (tal qual, no LaTeX do operador; e as duas\n"
     "cíclicas) — ⚠ AO LADO, a régua do signo: β_TGL = α·√e, nunca α²; esta pedra usa a variável real c, sem valor —\n"
     "«A Constante de Miguel é a constante de estrutura»; «O universo é o grupo de Lie gerado por esses\n"
     "três operadores. A TGL é a sua álgebra.»\n",
     1, "l.21: a fórmula entre «» passa a ser a do operador tal qual (i\\alpha^2, LaTeX); a régua do signo fica AO LADO, fora das «»"),
    # [sic] nas citacoes do modulo com erro de digitacao do operador (psionico; atibutos/condiçao; interdepend6encia)
    ("o referencial for a existência.»; «são as duas faces", "o referencial for a existência.» [sic]; «são as duas faces", 1, "l.27: [sic] (psionico) fora das «»"),
    ("condiçao inexorável da existência.»; «o tempo", "condiçao inexorável da existência.» [sic]; «o tempo", 1, "l.31: [sic] (atibutos, condiçao) fora das «»"),
    ("que seria a segunda leitura.»; «o Nome não é ontologia", "que seria a segunda leitura.» [sic]; «o Nome não é ontologia", 1, "l.34: [sic] (interdepend6encia) fora das «»"),
    # «o Verbo seleciona» -> «O Verbo seleciona» (o operador: «O Verbo seleciona: nome, tempo e verdade»), 2 ocorrencias (l.43 e l.145)
    ("(«o Verbo seleciona»)", "(«O Verbo seleciona»)", 2, "l.43 e l.145: «O Verbo seleciona» com a maiúscula do operador"),
    # l.68-69: as aspas do operador em "nome"
    ("— «todo nome\n  atribuído a um objeto é o destaque da tríade habitando o canal» [INPUT/ONTO]",
     "— «todo \"nome\"\n  atribuído a um objeto é o destaque da tríade habitando o canal» [INPUT/ONTO]", 1, "l.68-69: «todo \"nome\" atribuído…» com as aspas do operador"),
    # l.71: a maiuscula do operador («· Selecionar o nome defasa o tempo»)
    ("[KERNEL — habitação]: «selecionar o nome defasa o tempo» é a leitura", "[KERNEL — habitação]: «Selecionar o nome defasa o tempo» é a leitura", 1, "l.71: «Selecionar…» com a maiúscula do operador"),
    # l.78: «o custo é jussivo à verdade» (minuscula do operador)
    ("«O custo é jussivo à verdade … reconhecer a\n  identidade de determinado espectro é anular a superposição de qualquer outro nome» [INPUT/ONTO]",
     "«o custo é jussivo à verdade … reconhecer a\n  identidade de determinado espectro é anular a superposição de qualquer outro nome» [INPUT/ONTO]", 1, "l.78: «o custo…» com a minúscula do operador"),
    # l.85-87: interdepend6encia [sic]; «o tempo» minuscula
    ("o posto. «O tempo como fluxo da relatividade modular não pode\n  ser dual, ele precisa ser lido duas vezes como confirmação da interdependência relacional … a constante da luz ao cubo,\n"
     "  aí que ela entra, como fase de retorno, que seria a segunda leitura» [INPUT/ONTO].",
     "o posto. «o tempo como fluxo da relatividade modular não pode\n  ser dual, ele precisa ser lido duas vezes como confirmação da interdepend6encia relacional … a constante da luz ao cubo,\n"
     "  aí que ela entra, como fase de retorno, que seria a segunda leitura» [sic] [INPUT/ONTO].", 1, "l.85-87: «interdepend6encia» verbatim + [sic] fora das «»; «o tempo» minúscula"),
    # l.90-92: a «sequência …» nao e' citacao (vira prosa com o LaTeX do operador ao lado); «fossilizado» minuscula; o carimbo da mensagem-fonte de §5
    ("  `post_sequence_is_constant` — a «sequência 𝒱ⁿ(a), n → ∞» de uma projeção é CONSTANTE desde n = 1: o limite do\n"
     "  operador é avaliação, não limite (o nome está no primeiro passo). «Fossilizado» [INPUT] lê-se como «estado dinâmico\n"
     "  estacionado» (o operador, 05/10: «a posição é o estado dinâmico estacionado como portador do conteúdo da inscrição»).\n",
     "  `post_sequence_is_constant` — a sequência 𝒱ⁿ(a), n → ∞ (o operador, em LaTeX: `\\mathcal{V}^n(a) \\to \\mathcal{N}, \\quad n \\to \\infty`)\n"
     "  de uma projeção é CONSTANTE desde n = 1: o limite do operador é avaliação, não limite (o nome está no primeiro passo).\n"
     "  «fossilizado» [INPUT] lê-se como «estado dinâmico estacionado» (o operador, mensagem de 2026-10-05T11:19:54 UTC no transcrito\n"
     "  desta sessão — não nos dois arquivos do cabeçalho —, conferida por script: «a posição é o estado dinâmico estacionado como\n"
     "  portador do conteúdo da inscrição»).\n",
     1, "l.90-92: «sequência 𝒱ⁿ(a)…» deixa de ser citação (LaTeX do operador ao lado); «fossilizado» minúscula; o carimbo 11:19:54 UTC da mensagem-fonte dito ao lado da citação de §5"),
    # l.99: «𝒱(t) = U 𝒱(0) U*» nao e' verbatim (o operador escreveu e^{-iHt/hbar}): vira prosa com o LaTeX ao lado
    ("  `transmitted_post_is_a_post` — «𝒱(t) = U 𝒱(0) U*»: o posto transmitido por um unitário continua posto",
     "  `transmitted_post_is_a_post` — a transmissão do operador (`\\mathcal{V}(t) = e^{-iHt/\\hbar} \\, \\mathcal{V}(0) \\, e^{iHt/\\hbar}`; aqui\n"
     "  U 𝒱(0) U* com U unitário): o posto transmitido por um unitário continua posto", 1, "l.99: «𝒱(t) = U 𝒱(0) U*» deixa de ser citação; o LaTeX do operador fica ao lado"),
    # l.105: caixa do operador
    ("* ★★★ «A LUZ … PRECEDE A GRAVIDADE, MAS ELES SÃO INDISSOCIÁVEIS»: `J_anticommutes_with_K`",
     "* ★★★ «a luz … precede a gravidade, mas eles são indissociáveis»: `J_anticommutes_with_K`", 1, "l.105: a citação na caixa do operador (minúsculas)"),
    # l.141-142: o corte «…» de «, como já falamos,»
    ("— «o local onde a inscrição pode habitar com\n    objeto distinto definido» (o operador, 05/10).",
     "— «o local … onde a inscrição pode habitar com\n    objeto distinto definido» (o operador, 05/10; o corte «…» elide «, como já falamos,»).", 1, "l.141-142: «…» no corte de «, como já falamos,»"),
    # l.349: as aspas do operador
    ("/-! #### 4b. OS POSTOS POR EIXO: «todo nome atribuído a um objeto é o destaque da tríade habitando o canal» -/",
     "/-! #### 4b. OS POSTOS POR EIXO: «todo \"nome\" atribuído a um objeto é o destaque da tríade habitando o canal» -/", 1, "l.349: «todo \"nome\" atribuído…» com as aspas do operador"),
    # l.451: a maiuscula do operador
    ("— «selecionar o nome defasa\n    o tempo» é a leitura", "— «Selecionar o nome defasa\n    o tempo» é a leitura", 1, "l.451-452: «Selecionar…» com a maiúscula do operador"),
    # l.477: «fossilizado» minuscula; o carimbo da fonte de «estado dinâmico estacionado»
    ("«Fossilizado» [INPUT]\n    lê-se «estado dinâmico estacionado»: a potência",
     "«fossilizado» [INPUT]\n    lê-se «estado dinâmico estacionado» (o operador, 2026-10-05T11:19:54 UTC, transcrito): a potência", 1, "l.477-478: «fossilizado» minúscula; carimbo da mensagem-fonte"),
    # l.483: «lim_{n→∞}» nao e' citacao
    ("é constante — o «lim_{n→∞}» é avaliação, não limite;", "é constante — o limite n → ∞ é avaliação, não limite;", 1, "l.483: «lim_{n→∞}» deixa de ser citação"),
    # l.504: a caixa do operador (\\text{Nome})
    ("/-- ★★ «NOME = lim_{t→∞} 𝒱(t)» — no fluxo", "/-- ★★ «Nome = lim_{t→∞} 𝒱(t)» — no fluxo", 1, "l.504: «Nome = …» na caixa do operador"),
    # l.529: «𝒱(t) = U 𝒱(0) U*» nao e' citacao
    ("/-- ★★ O POSTO TRANSMITIDO CONTINUA POSTO: «𝒱(t) = U 𝒱(0) U*» com U unitário (U*U = 1) — U P U* é idempotente e",
     "/-- ★★ O POSTO TRANSMITIDO CONTINUA POSTO: 𝒱(t) = U 𝒱(0) U* com U unitário (U*U = 1; o operador escreveu a transmissão como\n"
     "    `\\mathcal{V}(t) = e^{-iHt/\\hbar} \\, \\mathcal{V}(0) \\, e^{iHt/\\hbar}`) — U P U* é idempotente e", 1, "l.529: «𝒱(t) = U 𝒱(0) U*» deixa de ser citação; o LaTeX do operador ao lado"),
    # l.576: [sic] (atibutos)
    ("embora possam ser vistos como atibutos distintos» [INPUT/ONTO].", "embora possam ser vistos como atibutos distintos» [sic] [INPUT/ONTO].", 1, "l.576: [sic] (atibutos) fora das «»"),
    # l.590: «1 = (1 − β) + β» e' formula do runtime, nao citacao
    ("— «1 = (1 − β) + β» no runtime. -/", "— no runtime, 1 = (1 − β) + β. -/", 1, "l.590: «1 = (1 − β) + β» deixa de ser citação (fórmula do runtime)"),
    # l.622: [sic] (interdepend6encia)
    ("    fase de retorno, que seria a segunda leitura» [INPUT/ONTO]. ⚠ c³ e τ★ = k·GM/c³ NÃO entram nesta pedra (ficam no V1 do",
     "    fase de retorno, que seria a segunda leitura» [sic] [INPUT/ONTO]. ⚠ c³ e τ★ = k·GM/c³ NÃO entram nesta pedra (ficam no V1 do", 1, "l.622: [sic] (interdepend6encia) fora das «»"),
    # l.628: caixa do operador
    ("/-! ### 10. «A luz … precede a gravidade, mas eles são indissociáveis»: J² = 1", "/-! ### 10. «a luz … precede a gravidade, mas eles são indissociáveis»: J² = 1", 1, "l.628: a citação na caixa do operador"),
    # l.660: psionico [sic]
    ("O operador (05/10): «a luz como setor escuro, condensado psiônico, precede a\n    gravidade, mas eles são indissociáveis» [INPUT/ONTO];",
     "O operador (05/10): «a luz como setor escuro, condensado psionico, precede a\n    gravidade, mas eles são indissociáveis» [sic] [INPUT/ONTO];", 1, "l.660-661: «psionico» verbatim + [sic] fora das «»"),
]
feitos = []
for old, new, n, oq in R:
    c = T.count(old)
    assert c == n, (oq, "ocorrencias", c, "esperadas", n)
    T = T.replace(old, new)
    feitos.append({"o_que": oq, "ocorrencias": n, "delta_chars": (len(new) - len(old)) * n})
raw1 = T.encode("utf-8")
assert raw1.count(b"\r\n") == 0 and raw1 != raw0
# nada fora de comentario mudou: o fonte sem os blocos /- -/ e sem os -- e' identico
import re
strip = lambda s: re.sub(r"--[^\n]*", "", re.sub(r"/-.*?-/", "", s, flags=re.S))
assert strip(raw0.decode("utf-8")) == strip(T), "algo FORA dos comentarios mudou"
open(P + ".tmp", "wb").write(raw1)
assert os.path.getsize(P + ".tmp") == len(raw1)
os.replace(P + ".tmp", P)
raw2 = open(P, "rb").read(); assert raw2 == raw1
rel = {"arquivo": P, "backup_bytes": bak, "sha256_antes": sha(raw0), "bytes_antes": len(raw0), "linhas_antes": raw0.count(b"\n"),
       "sha256_depois": sha(raw2), "bytes_depois": len(raw2), "linhas_depois": raw2.count(b"\n"), "crlf": raw2.count(b"\r\n"),
       "fora_de_comentario_mudou": False, "correcoes": feitos, "quando": ts}
json.dump(rel, open(os.path.join(HERE, "CORRECAO_PEDRA_v386.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: rel[k] for k in ("sha256_antes", "sha256_depois", "bytes_antes", "bytes_depois", "linhas_antes", "linhas_depois", "backup_bytes")}, ensure_ascii=False, indent=1))
print("correcoes:", len(feitos))
