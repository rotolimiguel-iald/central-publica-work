"""Material review regressions; exclusively synthetic residuals and inputs."""
from pathlib import Path
import importlib.util
import sys
import unittest
from unittest.mock import Mock, patch
import numpy as np
import torch

sys.dont_write_bytecode=True
UNIT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location("motor_fixture_review",UNIT/"tests_motor/test_motor_synthetic.py")
fixture=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=fixture
spec.loader.exec_module(fixture)
motor,evidencia,fontes=fixture.motor,fixture.evidencia,fixture.fontes

class Material(unittest.TestCase):
    def test_default_tgl_planck_desi_is_preserved(self):
        opts=motor.validar_modelo_para_conjuntos(["planck_comp","desi_dr1"])
        self.assertEqual(opts,motor.OPCOES_TGL)

    def test_double_count_combinations_refused_only_for_consumers(self):
        cases=[(["cc_moresco"],None),(["sh0es_local"],None),
               (["pantheon_sh0es"],{"lei_sn":"sombra"}),(["pantheon_sh0es"],{"lei_sn":"acumulada"})]
        for selected,options in cases:
            with self.subTest(selected=selected,options=options),self.assertRaisesRegex(ValueError,"dupla contagem"):
                motor.validar_modelo_para_conjuntos(selected,options)
        motor.validar_modelo_para_conjuntos(["planck_comp"],{"lei_sn":"sombra"})
        motor.validar_modelo_para_conjuntos(["cc_moresco"],{"lei_cc":"nenhuma"})
        motor.validar_modelo_para_conjuntos(["pantheon_sh0es"],None)

    def test_article_local_combinations_are_allowed(self):
        for selected,options in [(["cc_moresco"],{"modo":"artigo"}),(["sh0es_local"],{"modo":"artigo"}),
                                 (["pantheon_sh0es"],{"modo":"artigo","lei_sn":"sombra"})]:
            self.assertEqual(motor.validar_modelo_para_conjuntos(selected,options)["beta_no_fundo"],"nao")

    def test_unused_pantheon_law_is_refused(self):
        for mode in ("tgl","artigo"):
            with self.assertRaisesRegex(ValueError,"não implementada"):
                motor.validar_modelo_para_conjuntos(["pantheon"],{"modo":mode,"lei_sn":"sombra"})

    def test_facade_and_direct_motor_refuse_before_fit(self):
        e=fixture.ev()
        with patch.object(e,"_ajuste",side_effect=AssertionError("fit must not start")):
            with self.assertRaisesRegex(ValueError,"dupla contagem"):
                e.ajustar(["cc_moresco"])
        m=object.__new__(motor.Motor)
        m.predizer=Mock(side_effect=AssertionError("prediction must not start"))
        for method in (m.chi2,m.residuos):
            with self.assertRaisesRegex(ValueError,"dupla contagem"):
                method([[67.5,.02237,.12,.01,0]],["sh0es_local"])
        m.predizer.assert_not_called()

    def test_profiled_m_consumes_one_degree_of_freedom(self):
        m=fixture.DummyMotor()
        m.n_dados=lambda selected:6
        design=np.array([[1,0,0],[0,1,0],[0,0,1],[-1,0,0],[0,-1,0],[0,0,-1]],float)
        target=np.array([67.5,.02237,.12])
        scale=np.array([1.,.0005,.005])
        def residual(th,selected,options):
            y=(np.asarray(th)[:,:3]-target)/scale
            return torch.tensor(y@design.T,dtype=torch.float64),{}
        m.residuos=residual
        e=evidencia.Evidencia(m,Mock(),canonical_guard=fixture.receipt)
        for selected in (["pantheon"],["pantheon_sh0es"]):
            result=e._ajuste(selected,0.,False)
            self.assertEqual(result["n_parametros_perfilados"],1)
            self.assertEqual(result["parametros_perfilados"],["M_supernova"])
            self.assertEqual(result["gl"],2)
        other=e._ajuste(["planck_comp"],0.,False)
        self.assertEqual(other["gl"],3)

    def test_mixed_options_do_not_claim_article_preset(self):
        self.assertTrue(motor.rotulo_opcoes({"modo":"artigo"}).startswith("artigo"))
        label=motor.rotulo_opcoes({"modo":"selado","beta_no_fundo":"nao","mapa_R":"eff"})
        self.assertTrue(label.startswith("misto"),label)
        self.assertIn("lei=d1a",label)
        self.assertIn("planck_cov=pipeline",label)

    def test_dr1_primary_origin_is_explicitly_declared(self):
        rows=[(z,t,1.) for z in fontes.DR1_CORRELACOES for t in (0,1)] + [(0.3,2,1.),(1.5,2,1.)]
        _,provenance=fontes.desi_dr1_covariancia(rows)
        self.assertEqual(provenance["estatuto_origem"],"DECLARADO")
        self.assertIsNone(provenance["fonte_primaria_sha256"])
        self.assertFalse(provenance["admissao_primaria_verificada"])

if __name__=="__main__":
    unittest.main(verbosity=2)
