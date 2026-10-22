import TGLExt.TheTimeIsNotAPost
import Lean

open Lean Elab Command

partial def serA : Expr → String
  | .bvar i => s!"#{i}"
  | .fvar f => s!"F{f.name}"
  | .mvar m => s!"M{m.name}"
  | .sort u => s!"(S {u})"
  | .const n us => s!"{n}.{us}"
  | .app f a => s!"({serA f} {serA a})"
  | .lam _ t b bi => s!"(L{repr bi} {serA t}, {serA b})"
  | .forallE _ t b bi => s!"(P{repr bi} {serA t}, {serA b})"
  | .letE _ t v b nd => s!"(LET{nd} {serA t} := {serA v}; {serA b})"
  | .lit (.natVal n) => s!"N{n}"
  | .lit (.strVal s) => s!"Str{repr s}"
  | .mdata _ e => serA e
  | .proj s i e => s!"(PROJ {s} {i} {serA e})"

partial def serN : Expr → String
  | .bvar i => s!"#{i}"
  | .fvar f => s!"F{f.name}"
  | .mvar m => s!"M{m.name}"
  | .sort u => s!"(S {u})"
  | .const n us => s!"{n}.{us}"
  | .app f a => s!"({serN f} {serN a})"
  | .lam n t b bi => s!"(L{repr bi} {repr n} : {serN t}, {serN b})"
  | .forallE n t b bi => s!"(P{repr bi} {repr n} : {serN t}, {serN b})"
  | .letE n t v b nd => s!"(LET{nd} {repr n} : {serN t} := {serN v}; {serN b})"
  | .lit (.natVal n) => s!"N{n}"
  | .lit (.strVal s) => s!"Str{repr s}"
  | .mdata d e => s!"(MD {d.size} {serN e})"
  | .proj s i e => s!"(PROJ {s} {i} {serN e})"

#eval show CommandElabM Unit from do
  let env ← getEnv
  let target : Name := `TGLExt.TheTimeIsNotAPost
  let some idx := env.header.moduleNames.findIdx? (· == target) | throwError "modulo nao achado"
  let names := env.header.moduleData[idx]!.constNames
  let mut out : Array String := #[]
  out := out.push s!"MODULO\t{target}\t{names.size}"
  for n in names do
    let some ci := env.find? n | throwError s!"constante sem info: {n}"
    let kind := match ci with
      | .thmInfo _ => "thm" | .defnInfo _ => "def" | .axiomInfo _ => "AXIOM" | .opaqueInfo _ => "opaque"
      | .inductInfo _ => "induct" | .ctorInfo _ => "ctor" | .recInfo _ => "rec" | .quotInfo _ => "quot"
    let extra := match ci with
      | .defnInfo d =>
        let h := match d.hints with
          | .opaque => "opaque" | .abbrev => "abbrev" | .regular k => s!"regular {k}"
        let sf := match d.safety with
          | .safe => "safe" | .unsafe => "unsafe" | .partial => "partial"
        s!"hints={h};safety={sf}"
      | _ => ""
    let axs ← liftCoreM (Lean.collectAxioms n)
    let axS := ",".intercalate (axs.toList.map toString)
    let lps := ",".intercalate (ci.levelParams.map toString)
    let doc ← liftCoreM (findDocString? env n)
    let docS := match doc with
      | some d => toString (hash d)
      | none => "-"
    let (vA, vN) := match ci.value? (allowOpaque := true) with
      | some v => (serA v, serN v)
      | none => ("-", "-")
    out := out.push s!"DECL\t{n}\t{kind}\t{n.isInternal}\t{lps}\t{extra}\t{axS}\t{docS}"
    out := out.push s!"TYPEA\t{n}\t{serA ci.type}"
    out := out.push s!"TYPEN\t{n}\t{serN ci.type}"
    out := out.push s!"VALA\t{n}\t{vA}"
    out := out.push s!"VALN\t{n}\t{vN}"
  IO.FS.writeFile "C:/t/nm1/meta/meta_time_old.txt" ("\n".intercalate out.toList ++ "\n")
  logInfo m!"meta time_old gravado: {names.size} constantes"
