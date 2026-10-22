-- SONDA P1c (exame F_KERNEL, 12/10/2026, so sandbox): o fecho TRANSITIVO de constantes das 7 declaracoes da PALAVRA,
-- restrito as raizes TGL/TGLExt/ChatgptAudit (o Mathlib nao importa o kernel, logo o caminho ate uma constante do kernel
-- so passa por constantes do kernel), contem a letra (exact_witness_of_annihilating_word, annihilating_word_exists)?
import TGLExt.Palavra
open Lean Elab Command
run_cmd do
  let env ← getEnv
  let raiz (c : Name) : Bool := c.getRoot == `TGLExt || c.getRoot == `TGL || c.getRoot == `ChatgptAudit
  let usados (c : Name) : Array Name := match env.find? c with
    | some (.thmInfo v) => v.type.getUsedConstants ++ v.value.getUsedConstants
    | some (.defnInfo v) => v.type.getUsedConstants ++ v.value.getUsedConstants
    | some (.opaqueInfo v) => v.type.getUsedConstants ++ v.value.getUsedConstants
    | some (.inductInfo v) => v.type.getUsedConstants ++ v.ctors.toArray
    | some (.ctorInfo v) => v.type.getUsedConstants
    | some (.recInfo v) => v.type.getUsedConstants
    | _ => #[]
  let raizes : List Name := [`TGLExt.Palavra.the_face_does_not_close, `TGLExt.Palavra.the_reading_creates_the_contour,
    `TGLExt.Palavra.the_read_face_closes, `TGLExt.Palavra.the_contour_gives_the_temperature,
    `TGLExt.Palavra.the_first_reading_identifies, `TGLExt.Palavra.rereading_adds_nothing,
    `TGLExt.Palavra.the_reading_creates_the_object]
  let mut vis : NameSet := {}
  let mut pilha : Array Name := raizes.toArray
  while h : pilha.size > 0 do
    let c := pilha.back
    pilha := pilha.pop
    unless vis.contains c do
      vis := vis.insert c
      for d in usados c do
        if raiz d && !vis.contains d then pilha := pilha.push d
  IO.println ("FECHO_TRANSITIVO_N\t" ++ toString vis.size)
  for c in [`TGLExt.exact_witness_of_annihilating_word, `TGLExt.annihilating_word_exists,
            `TGLExt.spectral_witness_of_annihilating_word] do
    IO.println ("FECHO_TRANSITIVO_CONTEM\t" ++ c.toString ++ "\t" ++ toString (vis.contains c))
  let mods : NameSet := vis.toList.foldl (fun s c => match env.getModuleIdxFor? c with
    | some idx => s.insert (env.header.moduleNames[idx.toNat]!)
    | none => s) {}
  IO.println ("FECHO_TRANSITIVO_MODULOS\t" ++ String.intercalate "," (mods.toList.map Name.toString))
