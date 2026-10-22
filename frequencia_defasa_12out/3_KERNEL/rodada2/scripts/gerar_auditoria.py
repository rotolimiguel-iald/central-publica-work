# -*- coding: utf-8 -*-
"""[rodada 2: copia do gerar_auditoria.py da rodada 1, so com a pasta base trocada para 3_KERNEL\rodada2]
Gera sandbox\\AuditTheUnitIsTheRank.lean a partir da pedra candidata (somente leitura da pedra):
(1) um `#print axioms` para CADA declaracao explicita (theorem/def) da pedra, na ordem do arquivo;
(2) uma varredura do ambiente (MetaM) sobre TODAS as constantes do modulo da pedra (no sandbox o modulo se chama
    `TheUnitIsTheRank`, raiz de pacote propria; o namespace e TGLExt.TheUnitIsTheRank):
    axiomas por `collectAxioms`; para cada teorema, as hipoteses (binders de tipo Prop) que NAO ocorrem no termo de
    prova («nome sem peso»), e se o enunciado e literalmente `True`.
Grava tambem DECLARACOES.json (nome, tipo, linha, enunciado-fonte normalizado)."""
import hashlib, json, os, re

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # rodada2
SB = os.path.join(AQUI, "sandbox")
PEDRA = os.path.join(SB, "TGLExt", "TheUnitIsTheRank.lean")
NS = "TGLExt.TheUnitIsTheRank"

src_b = open(PEDRA, "rb").read()
src = src_b.decode("utf-8")
linhas = src.split("\n")
decl_re = re.compile(r"^(theorem|lemma|def|abbrev|noncomputable def)\s+([A-Za-z_][A-Za-z0-9_'.]*)")
decls = []
for i, ln in enumerate(linhas, start=1):
    m = decl_re.match(ln)
    if m:
        # enunciado-fonte: da linha da declaracao ate o primeiro ':=' de nivel superior (heuristica textual)
        bloco = []
        j = i - 1
        while j < len(linhas):
            bloco.append(linhas[j])
            if ":=" in linhas[j]:
                break
            j += 1
        txt = " ".join(x.strip() for x in bloco)
        txt = txt.split(":=")[0].strip()
        decls.append({"nome": m.group(2), "nome_completo": NS + "." + m.group(2), "tipo": m.group(1),
                      "linha": i, "enunciado_fonte": txt})

nomes = [d["nome_completo"] for d in decls]
if len(set(nomes)) != len(nomes):
    raise SystemExit("FALHA VISIVEL: nomes repetidos")

out = ["/- AUDITORIA da pedra candidata TGLExt.TheUnitIsTheRank (gerada por gerar_auditoria.py; nao e pedra).",
       "   pedra sha256 " + hashlib.sha256(src_b).hexdigest() + " -/",
       "import TheUnitIsTheRank", ""]
for n in nomes:
    out.append("#print axioms " + n)
out += ["",
        "open Lean Meta in",
        "#eval show MetaM Unit from do",
        "  let env ← getEnv",
        "  let some idx := env.getModuleIdx? `TheUnitIsTheRank | throwError \"modulo ausente\"",
        "  let names := (env.header.moduleData[idx.toNat]!).constNames",
        "  IO.println s!\"VARREDURA|{names.size}\"",
        "  for n in names do",
        "    let axs ← collectAxioms n",
        "    IO.println s!\"AX|{n}|{axs.toList}\"",
        "    let some ci := env.find? n | continue",
        "    match ci with",
        "    | .thmInfo ti =>",
        "      let r ← forallTelescope ti.type fun xs body => do",
        "        let v := ti.value.beta xs",
        "        let mut unused : Array String := #[]",
        "        let mut nprop := 0",
        "        for x in xs do",
        "          let ty ← inferType x",
        "          if ← isProp ty then",
        "            nprop := nprop + 1",
        "            if !(v.containsFVar x.fvarId!) then",
        "              unused := unused.push (toString (← x.fvarId!.getUserName))",
        "        return (nprop, unused, body.isConstOf ``True)",
        "      IO.println s!\"HYP|{n}|{r.1}|{r.2.1.toList}|{r.2.2}\"",
        "    | _ => pure ()",
        ""]
alvo = os.path.join(SB, "AuditTheUnitIsTheRank.lean")
with open(alvo + ".tmp", "wb") as f:
    f.write("\n".join(out).encode("utf-8"))
os.replace(alvo + ".tmp", alvo)
dj = os.path.join(AQUI, "DECLARACOES.json")
with open(dj + ".tmp", "wb") as f:
    f.write(json.dumps({"pedra": PEDRA, "pedra_sha256": hashlib.sha256(src_b).hexdigest(), "n": len(decls),
                        "declaracoes": decls}, ensure_ascii=False, indent=1).encode("utf-8") + b"\n")
os.replace(dj + ".tmp", dj)
print(json.dumps({"declaracoes": len(decls), "teoremas": sum(1 for d in decls if d["tipo"] == "theorem"),
                  "defs": sum(1 for d in decls if d["tipo"] != "theorem"), "auditoria": alvo}, ensure_ascii=False))
