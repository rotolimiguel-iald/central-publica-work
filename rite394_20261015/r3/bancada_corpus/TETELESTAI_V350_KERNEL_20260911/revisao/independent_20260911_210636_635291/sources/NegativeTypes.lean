import TGLExt.V350GateContract
set_option autoImplicit false
namespace IndependentNegative
theorem nominal : True := True.intro
def rejectTrue : (P : TGLExt.SiteProfile) → TGLExt.ConverseClauseContract P := nominal
noncomputable def conditional (h : False) : TGLExt.ModularRealizationCertificate := False.elim h
noncomputable def rejectHiddenPremise : TGLExt.ModularRealizationCertificate := conditional
end IndependentNegative
