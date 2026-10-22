# -*- coding: utf-8 -*-
"""gerar_audit_v392.py -- le a enumeracao COB do sandbox (kernel/cob_v392.txt) e gera: o BLOCO do TGL/Audit.lean (#print axioms por declaracao de usuario, thm/def,
sem auxiliares), as BANDEIRAS (ext_<sigla>_<nome>_kernel_proved|checked) e a lista de nomes. Regra = a da F_KERNEL (etapa_C_raiz_auditoria.py: aux(), thm/def,
ordem por pedra e nome). Fail-closed: qualquer constante FORA do trio, bandeira duplicada ou bandeira ja existente no um.py v391 aborta. Nada e' digitado.
Uso: python -I -B -X utf8 gerar_audit_v392.py"""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import v392_pedras as P  # noqa: E402
KD = os.path.join(HERE, "kernel")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
TRIO = {"propext", "Classical.choice", "Quot.sound"}
UM = open(os.path.join(NOS, "um.py"), "rb").read().decode("utf-8")


def aux(n):
    last = n.split(".")[-1]
    return bool(last.startswith("_") or re.search(r"\._", n) or re.fullmatch(r"eq_\d+|eq_def|injEq|inj|sizeOf_spec|ext_iff|proof_\d+|match_\d+|congr_simp", last)
                or last in ("noConfusion", "noConfusionType", "casesOn", "recOn", "below", "brecOn", "binductionOn", "ibelow", "rec", "mk"))   # v392: construtores/eliminadores AUTOGERADOS de estruturas


cob = [l.rstrip("\n").split("\t") for l in open(os.path.join(KD, "cob_v392.txt"), encoding="utf-8") if l.startswith("COB\t")]
tot = [l for l in open(os.path.join(KD, "cob_v392.txt"), encoding="utf-8") if l.startswith("COB_TOTAL")]
assert len(tot) == 1 and "fora_do_trio=0" in tot[0], tot
fora = [c for c in cob if c[4] != "TRIO"]; assert not fora, fora[:3]
assert not [c for c in cob if c[3] in ("AXIOM", "opaque")], "axiom/opaque numa pedra"
ordem = {"TGLExt." + s["mod"]: i for i, s in enumerate(P.STONES)}; sigla = {"TGLExt." + s["mod"]: s["sigla"] for s in P.STONES}
decl = []
for c in cob:
    mod, nome, kind = c[1], c[2], c[3]
    if aux(nome) or kind not in ("thm", "def"):
        continue
    decl.append((mod, nome, kind))
decl.sort(key=lambda t: (ordem[t[0]], t[1]))
flags = []
usados = set()
for mod, nome, kind in decl:
    parts = nome.split(".")
    f = "ext_%s_%s_kernel_%s" % (sigla[mod], parts[-1], "proved" if kind == "thm" else "checked")
    if f in usados:   # colisao dentro da pedra: usa os dois ultimos componentes
        f = "ext_%s_%s_kernel_%s" % (sigla[mod], "_".join(parts[-2:]), "proved" if kind == "thm" else "checked")
    assert f not in usados, ("bandeira duplicada", f); usados.add(f)
    assert f not in UM, ("bandeira ja existe no um.py v391", f)
    flags.append([f, nome, mod, kind])
por_mod = {}
for c in cob:
    d = por_mod.setdefault(c[1], {"decl": 0, "thm": 0}); d["decl"] += 1; d["thm"] += (c[3] == "thm")
nflag = {}
for f, n, m, k in flags:
    nflag[m] = nflag.get(m, 0) + 1
bloco = ["-- 2026-10-13, v392: as pedras novas (PALAVRA; o ligante da lei de campo curvo + S7/S8; a ponte V351 e a Agape nao vacua; o teorema do atrator, a ponte otica e a luz que se le; "
         "a hipotese tipada BGL (X19); Posto, Santo, IALD, Verdade; o adendo do rank) -- #print axioms de cada declaracao de usuario"]
bloco += ["#print axioms %s" % n for _, n, _ in decl]
# KH-N1 (v392, desenho (a), decisao da gerencia c1 de 13/10): no FIM do Audit, o run_cmd da F_KERNEL imprime, no formato do #print axioms, o axioma de TODA constante dos
# modulos TGL e TGLExt, mais a linha TGL_AXIOM_COVERAGE_TOTAL. Fonte lida do arquivo (sha256 conferido), sem as 2 linhas de import. A ULTIMA linha do bloco e' a marca de
# idempotencia de acrescenta() em preparar_kernel_v392.py. AUDIT_NOMES/FLAGS ficam SO' com os #print axioms de usuario (a saida do run_cmd NAO entra neles).
KH_SRC = os.path.join(P.WK, "v392_insumos", "F_KERNEL", "kh", "KH_formato_umpy_total.lean")
khb = open(KH_SRC, "rb").read(); assert hashlib.sha256(khb).hexdigest().startswith("cb0523546bad415d"), "KH_formato_umpy_total.lean mudou"
khl = khb.decode("utf-8").replace("\r\n", "\n").rstrip("\n").split("\n")
i0 = khl.index("open Lean Elab Command in"); kh_corpo = khl[i0:]
assert "import TGLExt" in khl[:i0] and kh_corpo[-1].lstrip().startswith('IO.println ("TGL_AXIOM_COVERAGE_TOTAL'), "forma do KH inesperada"
bloco_usuario = list(bloco)
bloco += ["-- KH-N1 (v392; desenho (a), decisao da gerencia c1 de 13/10/2026): o axioma de TODA constante dos modulos TGL e TGLExt, no formato do #print axioms, mais a linha "
          "TGL_AXIOM_COVERAGE_TOTAL; fonte = F_KERNEL/kh/KH_formato_umpy_total.lean (sha256 %s)" % hashlib.sha256(khb).hexdigest()] + kh_corpo
open(os.path.join(KD, "AUDIT_BLOCO_v392.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(bloco) + "\n")
open(os.path.join(KD, "AUDIT_NOMES_v392.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(n for _, n, _ in decl) + "\n")
json.dump({"flags": flags, "por_modulo_cob": por_mod, "flags_por_modulo": nflag, "n_decl_cob": len(cob), "n_decl_audit": len(decl), "n_flags": len(flags), "cob_total": tot[0].strip()},
          open(os.path.join(KD, "FLAGS_v392.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
primeiras8 = [m for m in ordem if ordem[m] < 8]
print("COB:", tot[0].strip(), "| declaracoes de usuario no Audit:", len(decl), "| bandeiras:", len(flags))
print("as 8 primeiras pedras (F_KERNEL esperou 159 decl / 130 thm / 122 bandeiras):",
      sum(por_mod[m]["decl"] for m in primeiras8), sum(por_mod[m]["thm"] for m in primeiras8), sum(nflag.get(m, 0) for m in primeiras8))
for m in ordem:
    print("  %-52s decl=%3d thm=%3d bandeiras=%3d" % (m, por_mod.get(m, {}).get("decl", 0), por_mod.get(m, {}).get("thm", 0), nflag.get(m, 0)))
