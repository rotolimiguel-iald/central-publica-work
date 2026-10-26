"""Only synthetic inputs; never constructs Motor or reads observed datasets."""
from pathlib import Path
import sys, unittest, tempfile, hashlib, json, math, io, types, threading
from unittest.mock import patch, Mock
import numpy as np
import torch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'candidate'))
from bancada import motor, evidencia, regua, fontes, camb_tabela, pantheon_cov, amostrador
from bancada.fundo_gpu import FundoV3Lote

def receipt(op):
    return dict(ok=True, canonical_manifest_sha256='synthetic-manifest', um_py_sha256='synthetic-program', seal_sha256='synthetic-seal', operation=op)

class DummyMotor:
    def __init__(self):
        self.raiz=str(ROOT/'candidate'); self.dev=torch.device('cpu'); self.lock=threading.Lock()
        self.beta_tgl=(1/137.035999084)*math.sqrt(math.e)
        self.limites=dict(H0=(60.,76.),ombh2=(.02025,.02475),omch2=(.102,.138),beta=(-.05,.05),c=(-.05,.05))
        self.suporte={'estatuto':'SUPORTE_INSTRUMENTAL_DIAGNOSTICO','limites_efetivos':self.limites,'evidencia_prior_amplo_autorizada':False}
        self.fundo=FundoV3Lote('cpu',n_grade=801,n_j1=101)
    def _t(self,a):return torch.as_tensor(a,dtype=torch.float64)
    def tab(self,h,b,c):
        v={k:torch.full_like(h,x) for k,x in dict(r_drag=147.,z_drag=1060.,r_star=144.,z_star=1090.,DM_star=14000.).items()}
        return v,torch.ones_like(h,dtype=torch.bool)
    def n_dados(self,c):return 7
    def residuos(self,th,cj,o):
        t=np.asarray(th); target=np.array([67.5,.02237,.120,0.,0.]); scale=np.array([1.,.0005,.005,.005,.005])
        r=(t-target)/scale
        return torch.tensor(r,dtype=torch.float64),{}

def ev():return evidencia.Evidencia(DummyMotor(),Mock(),canonical_guard=receipt)

class Contracts(unittest.TestCase):
    def test_modes(self):
        self.assertEqual(motor.opcoes_de(None),motor.OPCOES_TGL)
        self.assertEqual(motor.opcoes_de({'modo':'selado'}),motor.OPCOES_SELADO)
        self.assertEqual(motor.opcoes_de({'modo':'artigo'})['beta_no_fundo'],'nao')
        for x in ([],True,'tgl'):
            with self.assertRaises(ValueError):motor.opcoes_de(x)
    def test_sets(self):
        self.assertEqual(evidencia._conj(None),['planck_comp','desi_dr1'])
        for c in ([],['sh0es','sh0es'],['desi_dr1','desi_dr2'],['pantheon','pantheon_sh0es'],['sh0es','sh0es_local'],['pantheon','sh0es'],'sh0es',[True],['bad']):
            with self.subTest(c=c),self.assertRaises(ValueError):motor.conjuntos_validos(c)
        self.assertEqual(motor.conjuntos_validos(['planck_comp','desi_dr2','cc_moresco']),['planck_comp','desi_dr2','cc_moresco'])
    def test_numeric_attacks(self):
        for x in (True,False,np.bool_(True),float('nan'),float('inf'),-float('inf'),'1',None):
            with self.subTest(x=str(x)),self.assertRaises(ValueError):regua.numero_finito(x)
        for x in (True,1.1,1e40):
            with self.assertRaises(ValueError):regua.inteiro(x,'n',0,10)
        for x in (float('nan'),True,'5'):
            with self.assertRaises(ValueError):regua.p_de_z(x)
        with self.assertRaises(ValueError):regua.guarda({'x':float('nan')})
    def test_beta_numeric_attacks(self):
        e=ev()
        for x in (True,float('nan'),float('inf'),'0.012'):
            with self.assertRaises(ValueError):e._beta(x)
    def test_numeric_before_motor(self):
        e=ev()
        for theta in ({'H0':True},{'beta':float('nan')},{'H0':57},{'bad':1}):
            with self.assertRaises(ValueError):e.avaliar(theta,curvas=False)
        for args in ({'walkers':True},{'walkers':17},{'passos':float('nan')},{'queima':True},{'semente':False},{'c_livre':1}):
            with self.assertRaises(ValueError):e.amostrar(**args)
        self.assertFalse(e.tarefas)
    def test_motor_rejects_before_predict(self):
        m=object.__new__(motor.Motor);m.dev=torch.device('cpu')
        for theta in ([[True,1,1,1,1]],[[float('nan'),1,1,1,1]],[[1,2]],[],[[1,2,3,4,5,6]]):
            with self.assertRaises(ValueError):m.predizer(theta)
        with self.assertRaises(ValueError):m.chi2([[1,2,3,4,5]],['sh0es','sh0es'])
    def test_curves_same_article_background(self):
        e=ev();th=np.array([[67.5,.02237,.120,e.m.beta_tgl,0.]])
        out=e._curvas(th,{'modo':'artigo'})
        self.assertEqual(out['opcoes'],motor.OPCOES_ARTIGO)
        for k in ('DM_rd','DH_rd','DV_rd'):
            np.testing.assert_allclose(out[k],out['lcdm'][k],rtol=1e-13,atol=1e-13)
        alt=e._curvas(th,{'modo':'tgl'})
        self.assertGreater(np.max(np.abs(np.array(alt['DM_rd'])-np.array(alt['lcdm']['DM_rd']))),1e-7)
    def test_guard_changed_identity(self):
        e=ev();e._receipt('first');r=receipt('new');r['um_py_sha256']='changed';e._canonical_guard=lambda op:r
        with self.assertRaises(ValueError):e._receipt('second')
    def test_missing_guard_receipt(self):
        e=ev();e._canonical_guard=lambda op:{'ok':True}
        with self.assertRaises(ValueError):e._receipt('first')
    def test_effective_fit_synthetic(self):
        e=ev();r=e._ajuste(['planck_comp'],None,True,opcoes={'modo':'tgl'})
        self.assertTrue(r['sucesso']);self.assertLess(r['chi2'],1e-20)
        self.assertFalse(r['suporte_instrumental']['evidencia_prior_amplo_autorizada'])
        with self.assertRaises(ValueError):e._ajuste(['planck_comp'],.1,False)
    def test_sidak_not_global(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'tests_motor') as t:
            l=regua.Livro(str(Path(t)/'book.sqlite'))
            out=l.corrige(.01,'synthetic-family')
            self.assertIsNone(out['p_global']);self.assertIsNone(out['z_global'])
            self.assertFalse(out['global_certificado'])
            self.assertAlmostEqual(out['p_sidak_exploratorio'],.01)
            for p in (True,float('nan'),-1,2):
                with self.assertRaises(ValueError):l.corrige(p)
    def test_async_identity_change_fails(self):
        e=ev();e._receipt('accepted');bad=receipt('changed');bad['seal_sha256']='different';e._canonical_guard=lambda op:bad
        task={};e._roda(task,'synthetic');self.assertEqual(task['estado'],'falhou')
    def test_posterior_is_not_p_value(self):
        e=ev();rng=np.random.default_rng(4)
        chain=rng.normal(size=(120,16,4))*.001+np.array([67.5,.02237,.12,0])
        task=dict(c_livre=False,conjuntos=['planck_comp'],opcoes=motor.opcoes_de(None),modo='tgl',walkers=16,passos=120,queima=20,semente=42)
        with patch.object(evidencia,'amostrar',return_value=(chain,np.zeros((120,16)),np.full(16,.4),.1)):
            e._roda(task,'synthetic')
        self.assertEqual(task['estado'],'pronta',task.get('erro'))
        out=task['resultado'];self.assertIsNone(out['significancia'])
        self.assertNotIn('p_bilateral',out['beta_tgl_pela_cauda'])
        self.assertIsNone(out['beta_tgl_pela_cauda']['p_frequentista'])
        self.assertIsNone(e.livro.registra.call_args.args[-1])
    def test_sampler_gaussian_only(self):
        p0=torch.tensor(np.random.default_rng(8).normal(size=(16,2)),dtype=torch.float64)
        ch,lp,ac,_=amostrador.amostrar(lambda p:-.5*(p*p).sum(1),p0,120,semente=8)
        res,tau,flat=amostrador.resumo(ch,20,['a','b'])
        self.assertTrue(np.isfinite(ch).all());self.assertTrue(all(t>=1 for t in tau))
        self.assertLess(abs(res['a']['mean']),.5)
        with self.assertRaises(ValueError):amostrador.amostrar(lambda p:torch.full((16,),float('nan')),p0,2)
        with self.assertRaises(ValueError):amostrador.autocorr_integrada(np.ones((50,16)))

class Custody(unittest.TestCase):
    def test_read_same_bytes(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'tests_motor') as td:
            p=Path(td)/'s.txt';p.write_bytes(b'synthetic')
            seen=[]
            def verify(path,data):seen.append(data);return {'sha256':hashlib.sha256(data).hexdigest()}
            with patch('bancada.canonical.verify_source_bytes',side_effect=verify):
                raw,h=fontes.read_checked(p)
            self.assertEqual(seen,[raw]);self.assertEqual(h,hashlib.sha256(raw).hexdigest())
            with patch('bancada.canonical.verify_source_bytes',side_effect=ValueError('pin mismatch')):
                with self.assertRaises(ValueError):fontes.read_checked(p)
    def fixture_table(self,path):
        axes=[np.linspace(58,78,7),np.linspace(.02,.025,7),np.linspace(.1,.14,7)]
        mesh=np.meshgrid(*axes,indexing='ij');v=mesh[0]+mesh[1]*100+mesh[2]*10
        q=dict(zip(('grade_H0','grade_ombh2','grade_omch2'),axes));q['teste_pontos']=np.array([[68,.0225,.12]])
        for j,n in enumerate(camb_tabela.NOMES):q[n]=v+j+1;q['teste_'+n]=np.array([68+2.25+1.2+j+1])
        np.savez(path,**q);man={'sha256':hashlib.sha256(path.read_bytes()).hexdigest()};path.with_suffix('.json').write_text(json.dumps(man))
        return axes
    def test_table_pin_support_interpolation(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'tests_motor') as td:
            p=Path(td)/'s.npz';axes=self.fixture_table(p)
            def read(path):b=Path(path).read_bytes();return b,hashlib.sha256(b).hexdigest()
            def js(path):b,h=read(path);return json.loads(b),h
            with patch.object(fontes,'read_checked',side_effect=read),patch.object(fontes,'json_checked',side_effect=js):
                table=camb_tabela.TabelaCAMB(str(p),'cpu')
                self.assertEqual(table.suporte['H0'],(axes[0][1],axes[0][-2]))
                t=[torch.tensor([68.,57.]),torch.tensor([.0225,.0225]),torch.tensor([.12,.12])]
                out,valid=table(*[x.to(torch.float64) for x in t]);self.assertEqual(valid.tolist(),[True,False])
                self.assertTrue(torch.isnan(out['r_drag'][1]));self.assertLess(table.erro_no_teste()['r_drag']['max'],1e-12)
                bad=json.loads(p.with_suffix('.json').read_text());bad['sha256']='0'*64;p.with_suffix('.json').write_text(json.dumps(bad))
                with self.assertRaises(ValueError):camb_tabela.TabelaCAMB(str(p),'cpu')
    def test_legacy_cov_cache_no_write(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'tests_motor') as td:
            d=Path(td);src=d/'cov.dat';src.write_text('2\n1\n0\n0\n2\n')
            npy=d/'pantheon_cov_v1.npy';np.save(npy,np.eye(2)*900)
            meta=npy.with_suffix('.npy.json');meta.write_text(json.dumps({'fonte_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'n':2}))
            before={x.name:x.read_bytes() for x in d.iterdir()}
            def read(path):b=Path(path).read_bytes();return b,hashlib.sha256(b).hexdigest()
            def js(path):b,h=read(path);return json.loads(b),h
            with patch.object(fontes,'PANTHEON_COV',str(src)),patch.object(fontes,'read_checked',side_effect=read),patch.object(fontes,'json_checked',side_effect=js):
                c,m=pantheon_cov.carregar_cov(str(d));np.testing.assert_array_equal(c,np.diag([1,2]));self.assertFalse(m['escrita_em_disco'])
                self.assertEqual(before,{x.name:x.read_bytes() for x in d.iterdir()})
                dat=json.loads(meta.read_text());dat['cache_sha256']='0'*64;meta.write_text(json.dumps(dat))
                with self.assertRaises(ValueError):pantheon_cov.carregar_cov(str(d))

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
