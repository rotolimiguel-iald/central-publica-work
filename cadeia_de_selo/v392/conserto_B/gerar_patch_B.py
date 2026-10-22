# -*- coding: utf-8 -*-
"""gerar_patch_B.py -- escreve PATCH_B_v392.txt (o trecho Python EXATO do conserto B: 4 substituicoes no candidato) e PROVA que ele se aplica: cada ancora ocorre UMA vez no
um_v392_candidato.py (que e' CRLF), o fonte remendado faz ast.parse, e a constante do rodape reproduz o sha256 do RODAPE_B_v392.lean. NAO edita o candidato nem o gerar_candidato.
Uso: python -I -B -X utf8 gerar_patch_B.py"""
import ast, hashlib, json, os
HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(HERE)
cand = open(os.path.join(V, "um_v392_candidato.py"), "rb").read().decode("utf-8")
foot = open(os.path.join(HERE, "RODAPE_B_v392.lean"), "rb").read().decode("utf-8")
assert '"""' not in foot and "\\" not in foot
fsha = hashlib.sha256(foot.encode("utf-8")).hexdigest()
I = "            "   # indentacao de run_one
A1 = I + 'src = re.sub(r"^import\\s+(\\S+)", _sub, src, flags=re.M)'
A2 = I + 'ok = (pr.returncode == 0 and not errs and not sorry) if kind == "POSITIVO" else (pr.returncode != 0 and bool(sem) and not envbad)'
A3 = I + 'sorry_ax = any("sorryAx" in v_ for v_ in ax_seen.values()); bad_ax = sorted({a_ for v_ in ax_seen.values() for a_ in v_ if a_ not in ("propext", "Classical.choice", "Quot.sound")})'
A4 = '"sorry_message": sorry_msg, "sorryAx_in_print_axioms": sorry_ax, "axioms_outside_trio": bad_ax, "print_axioms_read": len(ax_seen)})'
A5 = "def prove_bench_lean_controls(ONE, core):"
N1 = A1 + "\n" + "\n".join(I + l if l else l for l in [
    "# v392, conserto B: nos POSITIVOS (a) cada `example` vira `theorem _bench_example_N` (um `example` nao deixa constante no ambiente: o rodape nao o veria) e (b) o rodape le o axioma de TODA",
    "# declaracao do modulo. O sha256 CONFERIDO acima e' o do corpus; o fonte transposto muda e isso fica REGISTRADO no campo `footer` (como a transposicao `TGLV350. -> TGLExt.V350`).",
    "footer_b = (kind == \"POSITIVO\"); ex_n = 0",
    "if footer_b:",
    "    _cnt = [0]",
    "    def _ex_b(m_):",
    "        _cnt[0] += 1; return \"theorem _bench_example_%d\" % _cnt[0]",
    "    src = re.sub(r\"(?m)^example\\b\", _ex_b, src); ex_n = _cnt[0]",
    "    src = src.rstrip(\"\\n\") + \"\\n\" + _V392_FOOTER_B"])
N2 = I + 'ftot_b = re.search(r"TGL_FOOTER_B_TOTAL decl=(\\d+) fora_do_trio=(\\d+)", out); footer_ok = (not footer_b) or bool(ftot_b)   # v392: o rodape tem de ter RODADO (a linha total)\n' + \
     I + 'ok = (pr.returncode == 0 and not errs and not sorry and not bad_ax and footer_ok) if kind == "POSITIVO" else (pr.returncode != 0 and bool(sem) and not envbad)'
N3 = I + 'sorry_ax = any("sorryAx" in v_ for v_ in ax_seen.values())\n' + \
     I + '# v392: `#print axioms` de constante com universos escreve `Classical.choice.{u}`; o nome do axioma e o que vem antes de `.{`\n' + \
     I + 'bad_ax = sorted({a_ for v_ in ax_seen.values() for a_ in v_ if a_.split(".{")[0] not in ("propext", "Classical.choice", "Quot.sound")})'
N4 = '"sorry_message": sorry_msg, "sorryAx_in_print_axioms": sorry_ax, "axioms_outside_trio": bad_ax, "print_axioms_read": len(ax_seen),\n' + \
     I + '            "footer": {"applied": footer_b, "sha256": (_V392_FOOTER_B_SHA256 if footer_b else None), "examples_rewritten": ex_n, "total_line": (list(map(int, ftot_b.groups())) if ftot_b else None)}})'
N5 = ('_V392_FOOTER_B = r"""' + foot + '"""\n_V392_FOOTER_B_SHA256 = "' + fsha + '"   # sha256 de RODAPE_B_v392.lean (conserto_B); conferido por assert abaixo\n'
      'assert hashlib.sha256(_V392_FOOTER_B.encode("utf-8")).hexdigest() == _V392_FOOTER_B_SHA256, "rodape B adulterado"\n\n\n' + A5)
subs = [(A1, N1), (A2, N2), (A3, N3), (A4, N4), (A5, N5)]
crlf = "\r\n" in cand
patched = cand
for a, n in subs:
    aa = a.replace("\n", "\r\n") if crlf else a
    assert patched.count(aa) == 1, ("ancora nao unica", patched.count(aa), a[:80])
    patched = patched.replace(aa, n.replace("\n", "\r\n") if crlf else n)
ast.parse(patched)   # o remendo compila
# a constante do rodape no fonte remendado reproduz o sha
ns = {}
i = patched.index('_V392_FOOTER_B = r"""'); j = patched.index('_V392_FOOTER_B_SHA256 =')
exec(patched[i:j].replace("\r\n", "\n"), ns); assert hashlib.sha256(ns["_V392_FOOTER_B"].encode("utf-8")).hexdigest() == fsha
txt = ["PATCH B v392 (conserto B da PROPOSTA_V392): rodape que le o axioma de toda declaracao do modulo + `example` -> `theorem` nos controles POSITIVOS",
       "Aplicacao: 5 substituicoes EXATAS em prove_bench_lean_controls / run_one de um_v392_candidato.py (o candidato e' CRLF; cada ancora ocorre UMA vez; verificado por gerar_patch_B.py:",
       "o fonte remendado faz ast.parse e a constante reproduz o sha256 %s)." % fsha,
       "NAO e' edicao de gerar_candidato_v392.py: a gerencia o encaixa como patch novo (ancoras = as linhas ANTES abaixo, sem o fim de linha).",
       "Efeito medido (RESULTADO_B_v392.json): todos os 52 positivos compilam; os 10 pedidos passam a ter linha(s) de axioma lida(s) pelo regex do um.py; o negativo artificial `by sorry` revela sorryAx;",
       "os 2 negativos de controle mantem o veredito. SEM o `example`->`theorem`, 7 dos 10 pedidos (os Good*, so `example`) NAO deixam constante: o rodape sozinho nao os cobre.",
       "Campos novos no registro de cada controle: `footer` {applied, sha256, examples_rewritten, total_line}. `ok` do POSITIVO passa a exigir `not bad_ax` (com o nome normalizado) e `footer_ok`.",
       "Cuidado: `#print axioms` de constante com universos escreve `Classical.choice.{u}` / `Quot.sound.{u}` (28 dos 52 positivos): sem a normalizacao `split('.{')[0]`, `bad_ax` acusaria falso positivo.",
       "", "=" * 100]
for k, (a, n) in enumerate(subs, 1):
    txt += ["", "--- SUBSTITUICAO %d: ANTES (uma ocorrencia; indentacao exata) ---" % k, a, "--- DEPOIS ---", n]
txt += ["", "=" * 100, "RODAPE_B_v392.lean sha256 " + fsha]
open(os.path.join(HERE, "PATCH_B_v392.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(txt) + "\n")
json.dump({"patch_aplica": True, "ancoras_unicas": True, "ast_parse_ok": True, "crlf": crlf, "rodape_sha256": fsha, "candidato_sha256": hashlib.sha256(cand.encode("utf-8")).hexdigest()},
          open(os.path.join(HERE, "PATCH_B_VERIFICACAO.json"), "w", encoding="utf-8"), indent=1)
print("ok: patch aplica; ast.parse ok; crlf=%s" % crlf)
