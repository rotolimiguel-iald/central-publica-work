-- SONDA P (exame F_KERNEL, 12/10/2026, so sandbox): PALAVRA usa ou duplica a letra (ExactWitness/WordExistence)?
-- e o que as pedras do F1.ATRATOR usam do kernel. (Na 1a execucao uma versao lia so o TIPO: ConstantInfo.value? nao
-- devolve o valor de teorema importado; esta le .thmInfo v => v.value.)
import TGLExt.Palavra
import TGLExt.TheSingularityReadsTheAttractorAdendo1
import TGLExt.TheLightReadsItself
import TGLExt.OpticalPopulationBridgeR2
open Lean Elab Command

-- (P2) os tres «reler nao acrescenta» tem o MESMO enunciado de TGLExt.observing_adds_nothing (rfl so fecha se os tipos coincidem)
example : @TGLExt.Palavra.rereading_adds_nothing = @TGLExt.observing_adds_nothing := rfl
example : @TGLExt.TheSingularityReadsTheAttractor.A3_angular_rereading_only = @TGLExt.observing_adds_nothing := rfl
example : @TGLExt.TheLightReadsItself.A5_angular_rereading_only = @TGLExt.observing_adds_nothing := rfl
example : @TGLExt.Palavra.the_first_reading_identifies = @TGLExt.the_observer_reads_the_angle := rfl

run_cmd do
  let env ← getEnv
  let alvo : List Name := [`TGLExt.Palavra.the_face_does_not_close, `TGLExt.Palavra.the_reading_creates_the_contour,
    `TGLExt.Palavra.the_read_face_closes, `TGLExt.Palavra.the_contour_gives_the_temperature,
    `TGLExt.Palavra.the_first_reading_identifies, `TGLExt.Palavra.rereading_adds_nothing,
    `TGLExt.Palavra.the_reading_creates_the_object,
    `TGLExt.TheSingularityReadsTheAttractor.A3_normalized_letter, `TGLExt.TheSingularityReadsTheAttractor.A3_letter_exists_finite,
    `TGLExt.TheSingularityReadsTheAttractor.A3_angular_rereading_only, `TGLExt.TheLightReadsItself.A5_angular_rereading_only,
    `F1Atrator.OpticalPopulation.normalized_letter, `F1Atrator.OpticalPopulation.annihilating_polynomial]
  for n in alvo do
    match env.find? n with
    | some ci =>
      let vs : Array Name := match ci with
        | .thmInfo v => v.value.getUsedConstants
        | .defnInfo v => v.value.getUsedConstants
        | _ => #[]
      let us := ci.type.getUsedConstants ++ vs
      let ks := us.toList.eraseDups.filter (fun c => c.getRoot == `TGLExt || c.getRoot == `TGL || c.getRoot == `ChatgptAudit)
      IO.println ("USA\t" ++ n.toString ++ "\t" ++ String.intercalate "," (ks.map Name.toString))
    | none => IO.println ("AUSENTE\t" ++ n.toString)
