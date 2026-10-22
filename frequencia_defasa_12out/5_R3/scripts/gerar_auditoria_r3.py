# -*- coding: utf-8 -*-
r"""RODADA 3 — gera, a partir da lista de declaracoes da rodada 2 (3_KERNEL\rodada2\DECLARACOES.json, 190 nomes) e das
tres renomeacoes, os arquivos Lean de auditoria do sandbox:
  5_R3\sandbox\AuditTheUnitIsTheRank.lean        — #print axioms de CADA uma das 190 declaracoes de r3;
  5_R3\sandbox\TiposTheUnitIsTheRank.lean        — para cada declaracao de r3: nome, hash estrutural do TIPO, hash do
                                                   VALOR (prova/definicao) e o tipo impresso (uma linha), via run_cmd;
  5_R3\sandbox_r2\TiposTheUnitIsTheRank.lean     — o mesmo para r2 (nomes antigos), no sandbox de reproducao.
Tambem grava 5_R3\DECLARACOES_R3.json (a lista de r3, com a correspondencia r2 -> r3). Nao escreve fora de 5_R3."""
import json, os, hashlib, re

R3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNID = os.path.dirname(R3)
DECL2 = os.path.join(UNID, "3_KERNEL", "rodada2", "DECLARACOES.json")
PEDRA3 = os.path.join(R3, "sandbox", "TGLExt", "TheUnitIsTheRank.lean")
NS = "TGLExt.TheUnitIsTheRank"
REN = {"nothing_branch": "zero_angle_pole",
       "reading_of_the_attractor_state": "selective_reading_of_half_identity",
       "transmission_dephases_reexport": "axiomFlow_complement_decay_reexport"}

d2 = json.load(open(DECL2, encoding="utf-8"))
nomes2 = [x["nome"] for x in d2["declaracoes"]]
if len(nomes2) != 190 or len(set(nomes2)) != 190:
    raise SystemExit("FALHA VISIVEL: lista da rodada 2 nao tem 190 nomes distintos")
for a in REN:
    if a not in nomes2:
        raise SystemExit("FALHA VISIVEL: nome a renomear ausente na rodada 2: " + a)
nomes3 = [REN.get(n, n) for n in nomes2]

# confere contra o fonte r3: cada `theorem X`/`def X` no codigo, na ordem
src = open(PEDRA3, encoding="utf-8").read()
achados = re.findall(r"^(?:theorem|def|noncomputable def) ([A-Za-z0-9_']+)", src, flags=re.M)
if achados != nomes3:
    faltam = [n for n in nomes3 if n not in achados]
    sobram = [n for n in achados if n not in nomes3]
    raise SystemExit("FALHA VISIVEL: a lista de declaracoes do fonte r3 difere: faltam %r sobram %r ordem_igual=%s"
                     % (faltam, sobram, sorted(achados) == sorted(nomes3)))

sha = hashlib.sha256(open(PEDRA3, "rb").read()).hexdigest()


def audit(nomes, pedra_sha, rodada):
    L = ["/- AUDITORIA da pedra candidata TGLExt.TheUnitIsTheRank, RODADA %s (gerada por gerar_auditoria_r3.py; nao e pedra)."
         % rodada, "   pedra sha256 %s -/" % pedra_sha, "import TheUnitIsTheRank", ""]
    L += ["#print axioms %s.%s" % (NS, n) for n in nomes]
    return "\n".join(L) + "\n"


def tipos(nomes, pedra_sha, rodada):
    L = ["/- TIPOS E VALORES da pedra candidata TGLExt.TheUnitIsTheRank, RODADA %s (gerado por gerar_auditoria_r3.py;"
         % rodada,
         "   nao e pedra). Para cada declaracao: DECL <tab> nome <tab> hash(tipo) <tab> hash(valor) <tab> tipo impresso.",
         "   pedra sha256 %s -/" % pedra_sha,
         "import TheUnitIsTheRank", "", "open Lean Elab Command Meta", "",
         "set_option maxHeartbeats 2000000", "",
         "def nomesAuditados : List Name := ["]
    L += ["  `%s.%s%s" % (NS, n, "," if i < len(nomes) - 1 else "") for i, n in enumerate(nomes)]
    L += ["]", "",
          "run_cmd do",
          "  let env ← getEnv",
          "  for n in nomesAuditados do",
          "    match env.find? n with",
          "    | none => logError m!\"AUSENTE\\t{n}\"",
          "    | some ci =>",
          "      let s ← liftTermElabM do",
          "        let fmt ← Meta.ppExpr ci.type",
          "        pure (toString fmt)",
          "      let hv : UInt64 := match ci.value? with | some v => v.hash | none => 0",
          "      let one := (s.replace \"\\n\" \" \").replace \"\\t\" \" \"",
          "      logInfo m!\"DECL\\t{n}\\t{ci.type.hash}\\t{hv}\\t{one}\"",
          ""]
    return "\n".join(L) + "\n"


sb3 = os.path.join(R3, "sandbox")
sb2 = os.path.join(R3, "sandbox_r2")
sha2 = hashlib.sha256(open(os.path.join(sb2, "TGLExt", "TheUnitIsTheRank.lean"), "rb").read()).hexdigest()
saidas = {
    os.path.join(sb3, "AuditTheUnitIsTheRank.lean"): audit(nomes3, sha, "3"),
    os.path.join(sb3, "TiposTheUnitIsTheRank.lean"): tipos(nomes3, sha, "3"),
    os.path.join(sb2, "TiposTheUnitIsTheRank.lean"): tipos(nomes2, sha2, "2 (reproducao em 5_R3\\sandbox_r2)"),
}
for p, txt in saidas.items():
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(txt)
dec = {"pedra_r3": PEDRA3, "pedra_r3_sha256": sha, "n": len(nomes3),
       "declaracoes": [{"r2": a, "r3": b, "renomeada": a != b, "nome_completo_r3": NS + "." + b}
                       for a, b in zip(nomes2, nomes3)]}
with open(os.path.join(R3, "DECLARACOES_R3.json"), "w", encoding="utf-8") as fh:
    json.dump(dec, fh, ensure_ascii=False, indent=1)
print(json.dumps({"n": len(nomes3), "renomeadas": [n for n in nomes3 if n in REN.values()],
                  "arquivos": list(saidas.keys())}, ensure_ascii=False, indent=1))
