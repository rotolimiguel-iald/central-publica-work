/-
  EXTRATOR DA AMPLITUDE DE INSCRIÇÃO — T06 (BANCADA_TOE)
  Pré-registro: PRE_REGISTRO_T06_amplitude.md
  sha256 3a48655430db0bfd1fba72c523f3a7549b59e5a35ec94598e244069e357333e0

  Extrai o grafo de DEPENDÊNCIAS EFETIVAS: para cada teorema, as constantes que
  ocorrem no seu TIPO e no seu VALOR. Não é o grafo de imports (autoral) — é o
  que cada prova de fato consome (necessidade matemática).

  Este arquivo NÃO faz parte do canônico: é instrumento de medida, roda por
  cima do kernel e não dentro dele. β jamais entra aqui.
-/
import TGLExt

open Lean

/-- nomes gerados automaticamente, excluídos pelo pré-registro -/
def T06.isAux (n : Name) : Bool :=
  let s := n.toString
  n.isInternal ||
  ["_proof_", "_aux", ".proof_", "match_", "eq_def", "sizeOf", "noConfusion",
   "injEq", "casesOn", "brecOn", "ndrec", "below", "ipm", ".rec", ".inj",
   "_cstage", "_spec", "_unsafe", "instDecidable"].any
    (fun q => (s.splitOn q).length > 1)

run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  let mut nomes : Std.HashSet Name := {}
  -- 1ª passada: o universo (teoremas não-auxiliares)
  for (n, ci) in env.constants.toList do
    match ci with
    | .thmInfo _ => if !T06.isAux n then nomes := nomes.insert n
    | _ => pure ()
  -- 2ª passada: arestas restritas ao universo
  let mut buf : Array String := #[]
  for (n, ci) in env.constants.toList do
    match ci with
    | .thmInfo ti =>
      if !T06.isAux n then
        let mut deps : Std.HashSet Name := {}
        for c in ti.type.getUsedConstants do
          if nomes.contains c && c != n then deps := deps.insert c
        for c in ti.value.getUsedConstants do
          if nomes.contains c && c != n then deps := deps.insert c
        let ds := deps.toList.map (·.toString)
        let modo := (env.getModuleFor? n).map (fun m => m.toString) |>.getD "?"
        buf := buf.push (n.toString ++ "	" ++ modo ++ "	" ++ String.intercalate " " ds)
    | _ => pure ()
  IO.FS.writeFile "T06_deps_full.tsv" (String.intercalate "\n" buf.toList)
  IO.println s!"T06: universo = {nomes.size} teoremas; linhas = {buf.size}"
