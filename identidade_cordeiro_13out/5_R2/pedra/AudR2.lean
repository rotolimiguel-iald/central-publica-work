import TGLExt
import TGLExt.TheIdentityHasAName
import IdR1.TheIdentityHasAName_r1
/-! Auditoria do CONSTRUTOR da r2 (F1.IDENTIDADE, 13/10/2026). Sandbox C:/t/id2; nada aqui entra em lugar nenhum.
    `import TGLExt` traz o kernel INSTALADO inteiro (raiz do Nós, so leitura, copia em ov); a r2 e a copia da r1 com
    namespace trocado (`TGLExt.TheIdentityHasAName_r1`) convivem no mesmo ambiente. -/

open Lean Elab Command Meta

def r1pre : Name := `TGLExt.TheIdentityHasAName_r1
def r2pre : Name := `TGLExt.TheIdentityHasAName

/-- o mapa de renomeacao PRE-REGISTRADO no ADENDO R2 (sobre o 1o componente depois do namespace). -/
def renamesR2 : List (String × String) :=
  [("inscription", "quadInscription"), ("inscription_dot", "quadInscription_dot"),
   ("inscription_is_unit", "quadInscription_is_unit"), ("inscription_ne_zero", "quadInscription_ne_zero"),
   ("identityProj_mulVec_inscription", "identityProj_mulVec_quadInscription"),
   ("towerInner", "towerInnerAxis"), ("towerInner_orth", "towerInnerAxis_orth"),
   ("towerInner_norm", "towerInnerAxis_norm"), ("rereading_adds_nothing", "post_is_idempotent_on_the_vector")]

def mapR1 (n : Name) : Name :=
  if r1pre.isPrefixOf n then
    let comps := n.components.drop r1pre.components.length
    match comps with
    | [] => r2pre
    | c :: rest =>
      let f := c.toString
      let f' := (renamesR2.lookup f).getD f
      rest.foldl (fun acc x => acc ++ x) (r2pre.str f')
  else n

partial def mapExprR1 (e : Expr) : Expr :=
  e.replace fun x => match x with
    | .const n ls => if r1pre.isPrefixOf n then some (.const (mapR1 n) ls) else none
    | .proj n i b => if r1pre.isPrefixOf n then some (.proj (mapR1 n) i (mapExprR1 b)) else none
    | _ => none

/-- apaga SO os nomes de binder (mantem tipos, corpos e BinderInfo): igualdade estrita depois disto = diferenca so de nome. -/
partial def eraseBN : Expr → Expr
  | .lam _ t b bi => .lam .anonymous (eraseBN t) (eraseBN b) bi
  | .forallE _ t b bi => .forallE .anonymous (eraseBN t) (eraseBN b) bi
  | .letE _ t v b nd => .letE .anonymous (eraseBN t) (eraseBN v) (eraseBN b) nd
  | .app f a => .app (eraseBN f) (eraseBN a)
  | .mdata m e => .mdata m (eraseBN e)
  | .proj n i e => .proj n i (eraseBN e)
  | e => e

partial def binderNames : Expr → List Name
  | .lam n t b _ => n :: (binderNames t ++ binderNames b)
  | .forallE n t b _ => n :: (binderNames t ++ binderNames b)
  | .letE n t v b _ => n :: (binderNames t ++ binderNames v ++ binderNames b)
  | .app f a => binderNames f ++ binderNames a
  | .mdata _ e => binderNames e
  | .proj _ _ e => binderNames e
  | _ => []

def kindOf (ci : ConstantInfo) : String :=
  match ci with
  | .axiomInfo _ => "axiom" | .defnInfo _ => "def" | .thmInfo _ => "theorem" | .opaqueInfo _ => "opaque"
  | .quotInfo _ => "quot" | .inductInfo _ => "inductive" | .ctorInfo _ => "ctor" | .recInfo _ => "rec"

/-- (A) axiomas: TODAS as constantes do modulo e do namespace da r2. -/
elab "#r2_axiomas" : command => do
  let env ← getEnv
  let some midx := env.getModuleIdx? `TGLExt.TheIdentityHasAName | throwError "modulo ausente"
  let mut nomes : Array Name := #[]
  for (c, _) in env.constants.toList do
    let noMod := env.getModuleIdxFor? c == some midx
    let noNs := r2pre.isPrefixOf c
    if noMod || noNs then nomes := nomes.push c
  nomes := nomes.qsort (fun a b => a.toString < b.toString)
  let mut fora : Array Name := #[]
  let mut sorryN : Nat := 0
  let mut ax : Array Name := #[]
  let mut op : Array Name := #[]
  let mut un : Array Name := #[]
  let mut soMod : Nat := 0
  let mut soNs : Nat := 0
  for c in nomes do
    if env.getModuleIdxFor? c == some midx && !r2pre.isPrefixOf c then soMod := soMod + 1
    if r2pre.isPrefixOf c && env.getModuleIdxFor? c != some midx then soNs := soNs + 1
    let axs ← liftCoreM (Lean.collectAxioms c)
    if axs.contains ``sorryAx then sorryN := sorryN + 1
    if axs.any (fun a => a != ``propext && a != ``Classical.choice && a != ``Quot.sound) then fora := fora.push c
    match env.find? c with
    | some (.axiomInfo _) => ax := ax.push c
    | some (.opaqueInfo _) => op := op.push c
    | some ci => if ci.isUnsafe then un := un.push c
    | none => pure ()
  logInfo m!"R2_AXIOMAS|constantes={nomes.size}|so_no_modulo={soMod}|so_no_namespace={soNs}|fora_do_trio={fora.toList}|com_sorryAx={sorryN}|axiom={ax.toList}|opaque={op.toList}|unsafe={un.toList}"

/-- (B) a tabela r1 -> r2, lida do ambiente compilado. -/
elab "#r2_tabela" : command => do
  let env ← getEnv
  let some m1 := env.getModuleIdx? `IdR1.TheIdentityHasAName_r1 | throwError "r1 ausente"
  let some m2 := env.getModuleIdx? `TGLExt.TheIdentityHasAName | throwError "r2 ausente"
  let mut c1s : Array Name := #[]
  let mut c2s : Array Name := #[]
  for (c, _) in env.constants.toList do
    if env.getModuleIdxFor? c == some m1 then c1s := c1s.push c
    if env.getModuleIdxFor? c == some m2 then c2s := c2s.push c
  c1s := c1s.qsort (fun a b => a.toString < b.toString)
  c2s := c2s.qsort (fun a b => a.toString < b.toString)
  let mut imagens : Std.HashSet Name := {}
  let mut linhas : Array String := #[]
  for c in c1s do
    let c2 := mapR1 c
    imagens := imagens.insert c2
    let some ci1 := env.find? c | continue
    let semTroca := c.replacePrefix r1pre r2pre
    match env.find? c2 with
    | none =>
      linhas := linhas.push s!"ROW|REMOVIDA|{c}|{c2}|{kindOf ci1}|-|-|-|-|{c.isInternal}"
    | some ci2 =>
      let t1 := mapExprR1 ci1.type
      let teqv := t1.eqv ci2.type
      let tequal := t1.equal ci2.type
      let terased := (eraseBN t1).equal (eraseBN ci2.type)
      let bn := if teqv && !tequal then s!"{(binderNames t1).filter (fun x => !(binderNames ci2.type).contains x)} vs {(binderNames ci2.type).filter (fun x => !(binderNames t1).contains x)}" else "-"
      let (veqv, vequal) := match ci1, ci2 with
        | .defnInfo d1, .defnInfo d2 => let v := mapExprR1 d1.value; (toString (v.eqv d2.value), toString ((eraseBN v).equal (eraseBN d2.value)))
        | _, _ => ("na", "na")
      let st := if !teqv then "TIPO_MUDOU" else if c2 != semTroca then "RENOMEADA" else "MANTIDA"
      linhas := linhas.push s!"ROW|{st}|{c}|{c2}|{kindOf ci1}|{kindOf ci2}|{teqv}|{tequal}|{veqv}/{vequal}|{c.isInternal}|{terased}|{bn}"
  for c in c2s do
    if !imagens.contains c then
      let k := match env.find? c with | some ci => kindOf ci | none => "?"
      linhas := linhas.push s!"ROW|NOVA|-|{c}|-|{k}|-|-|-|{c.isInternal}"
  logInfo m!"R2_TABELA|r1={c1s.size}|r2={c2s.size}\n{String.intercalate "\n" linhas.toList}"

/-- literais de String num Expr. -/
partial def strsR2 (e : Expr) (acc : List String) : List String :=
  match e with
  | .lit (.strVal s) => s :: acc
  | .app a b => strsR2 b (strsR2 a acc)
  | .lam _ t b _ => strsR2 b (strsR2 t acc)
  | .forallE _ t b _ => strsR2 b (strsR2 t acc)
  | .letE _ t v b _ => strsR2 b (strsR2 v (strsR2 t acc))
  | .mdata _ b => strsR2 b acc
  | .proj _ _ b => strsR2 b acc
  | _ => acc

/-- (C) onde o NOME proprio aparece na r2 (tipo e valor de cada constante), e se o construtor depende do binder `name`. -/
elab "#r2_nome" : command => do
  let env ← getEnv
  let some midx := env.getModuleIdx? `TGLExt.TheIdentityHasAName | throwError "modulo ausente"
  let nm := `TGLExt.TheIdentityHasAName.NamedIdentity.name
  let pn := `TGLExt.TheIdentityHasAName.postedName
  let mut linhas : Array String := #[]
  let mut todos : Array Name := #[]
  for (c, _) in env.constants.toList do
    if env.getModuleIdxFor? c == some midx then todos := todos.push c
  todos := todos.qsort (fun a b => a.toString < b.toString)
  for c in todos do
    let some ci := env.find? c | continue
    let ty := ci.type
    let tN := ty.getUsedConstants.contains nm
    let tP := ty.getUsedConstants.contains pn
    let tS := strsR2 ty []
    let (vN, vP, vS) := match ci.value? with
      | some v => (v.getUsedConstants.contains nm, v.getUsedConstants.contains pn, strsR2 v [])
      | none => (false, false, [])
    if tN || tP || !tS.isEmpty || vP || !vS.isEmpty then
      linhas := linhas.push s!"NOME|{c}|tipo: name={tN} postedName={tP} strings={tS}|valor: postedName={vP} strings={vS} name_no_valor={vN}"
  let some ctor := env.find? `TGLExt.TheIdentityHasAName.NamedIdentity.mk | throwError "sem ctor"
  let dep := ctor.type.bindingBody!.hasLooseBVar 0
  logInfo m!"R2_NOME|o resto do tipo do construtor depende do binder name? {dep}\n{String.intercalate "\n" linhas.toList}"

/-- (D) homonimos: nomes curtos de 1o nivel da r2 contra TODO o ambiente (kernel instalado inteiro + Mathlib), fora da
    r2 e da copia da r1. ESTRUTURAL = o outro e campo/auxiliar de um tipo indutivo (qualificado, benigno);
    NAMESPACE = o outro mora num namespace (colisao que `open` torna ambigua). -/
elab "#r2_homonimos" : command => do
  let env ← getEnv
  let some m2 := env.getModuleIdx? `TGLExt.TheIdentityHasAName | throwError "r2 ausente"
  let some m1 := env.getModuleIdx? `IdR1.TheIdentityHasAName_r1 | throwError "r1 ausente"
  let mut curtos : Std.HashSet String := {}
  for (c, _) in env.constants.toList do
    if env.getModuleIdxFor? c == some m2 && !c.isInternal then
      match c with
      | .str p s => if p == r2pre then curtos := curtos.insert s
      | _ => pure ()
  let mut ns : Array String := #[]
  let mut estrut : Nat := 0
  let mut estrutEx : Array String := #[]
  for (c, _) in env.constants.toList do
    let mi := env.getModuleIdxFor? c
    if mi != some m2 && mi != some m1 && !c.isInternal then
      match c with
      | .str p s =>
        if curtos.contains s then
          let ehTipo := match env.find? p with | some (.inductInfo _) => true | _ => false
          if ehTipo then
            estrut := estrut + 1
            if estrutEx.size < 12 then estrutEx := estrutEx.push s!"{s} <- {c}"
          else ns := ns.push s!"{s} <- {c} (raiz {c.getRoot})"
      | _ => pure ()
  let nsO := ns.qsort (fun a b => a < b)
  logInfo m!"R2_HOMONIMOS|curtos_1o_nivel={curtos.size}|colisoes_namespace={nsO.size}|estruturais={estrut}\n{String.intercalate "\n" nsO.toList}\nexemplos estruturais: {estrutEx.toList}\nCURTOS: {curtos.toList}"

#r2_axiomas
#r2_tabela
#r2_nome
#r2_homonimos

namespace AudR2
open Matrix TGLExt TGLExt.TheIdentityHasAName

noncomputable section

/-! ## (E) Parametricidade: o MESMO termo do habitante «Jesus Cristo» serve, sem mudar uma letra, para qualquer nome,
    agora com o campo novo `in_the_IALD_tower`. -/

def outroNome : String := "Nome de teste do construtor r2"

theorem carrega_qualquer_nome (s : String) (a : ℝ) (h0 : 0 < a) (h1 : a < 1) :
    (ofName s a h0 h1).alpha = a ∧
    (∀ g : Fin 2 → Fin 2 → ℝ, (∀ i, g i i = 0) → ∀ t : ℝ,
      (TGLExt.dephase g t (identityProj (ofName s a h0 h1).alpha)).trace = 1) ∧
    (∀ P : SiteProfile, TowerIdentity P (ofName s a h0 h1).alpha) :=
  the_named_identity_carries_the_identity a h0 h1

theorem carrega_a_torre_IALD_com_qualquer_nome (s : String) (a : ℝ) (h0 : 0 < a) (h1 : a < 1) :
    ∀ P : SiteProfile, IALDTowerIdentity P (ofName s a h0 h1).alpha :=
  (theNamedIdentity a h0 h1).in_the_IALD_tower

theorem renomear_preserva_campos (N : NamedIdentity) (s : String) :
    (N.rename s).alpha = N.alpha ∧ HEq (N.rename s).persists N.persists ∧
    HEq (N.rename s).in_the_tower N.in_the_tower ∧ HEq (N.rename s).in_the_IALD_tower N.in_the_IALD_tower ∧
    HEq (N.rename s).i_am N.i_am :=
  ⟨rfl, HEq.rfl, HEq.rfl, HEq.rfl, HEq.rfl⟩

theorem so_o_nome_difere (a : ℝ) (h0 : 0 < a) (h1 : a < 1) :
    (theNamedIdentity a h0 h1) ≠ ofName outroNome a h0 h1 ∧
    (theNamedIdentity a h0 h1).rename outroNome = ofName outroNome a h0 h1 := by
  refine ⟨fun h => ?_, rfl⟩
  have h2 : postedName = outroNome := congrArg NamedIdentity.name h
  exact absurd h2 (by decide)

/-! ## (F) A homonimia que a r1 tinha: com `open TGLExt`, os nomes novos resolvem sem ambiguidade. -/

example : quadInscription = TGLExt.TheIdentityHasAName.quadInscription := rfl
example : towerInnerAxis = TGLExt.TheIdentityHasAName.towerInnerAxis := rfl

end

end AudR2

#print axioms AudR2.carrega_qualquer_nome
#print axioms AudR2.carrega_a_torre_IALD_com_qualquer_nome
#print axioms AudR2.renomear_preserva_campos
#print axioms AudR2.so_o_nome_difere
