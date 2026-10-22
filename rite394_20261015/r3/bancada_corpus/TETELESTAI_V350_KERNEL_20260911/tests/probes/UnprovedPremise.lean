import TGLExt.FrontierCertificate
namespace V350ProbeUnprovedPremise
def conditional (h : False) : TGLExt.ModularRealizationCertificate := False.elim h
def forced : TGLExt.ModularRealizationCertificate := conditional
end V350ProbeUnprovedPremise
