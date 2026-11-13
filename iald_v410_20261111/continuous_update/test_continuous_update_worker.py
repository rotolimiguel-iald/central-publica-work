import tempfile
import unittest
from pathlib import Path
from continuous_update_worker import Worker

class Adapter:
    def __init__(self):
        self.current={'release':'v409'}
        self.candidate={'identity':{'release':'v410'},'seal':'fixture'}
        self.accepted=False
        self.allowed=True
        self.idle=True
        self.prepares=0
        self.deploys=0
        self.crash=False
        self.receipt=None
    def detect(self): return self.candidate
    def active(self): return self.current
    def prepare(self,c,d): self.prepares+=1
    def verify_package(self,d): return {'identity':self.candidate['identity'],'manifest_sha256':'0'*64,'files':[]}
    def review(self,d,p): return self.accepted
    def authorize(self,c): return self.allowed
    def quiet(self): return self.idle
    def deploy(self,d,b):
        self.deploys+=1
        if self.crash: raise RuntimeError('fixture crash')
        self.current=self.candidate['identity']
        self.receipt='ACTIVE'
    def reconcile(self,d): return self.receipt

class Tests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=Path(__file__).parent)
        self.addCleanup(self.temp.cleanup)
        self.a=Adapter()
        self.w=Worker(self.temp.name,self.a)
    def test_review_required_and_preparation_once(self):
        for _ in range(3): self.assertEqual(self.w.tick()['phase'],'REVIEW_PENDING')
        self.assertEqual((self.a.prepares,self.a.deploys),(1,0))
    def test_success_then_current(self):
        self.a.accepted=True
        self.assertEqual(self.w.tick()['phase'],'ACTIVE')
        self.assertEqual(self.w.tick()['phase'],'CURRENT')
        self.assertEqual(self.a.deploys,1)
    def test_crash_no_retry_even_new_candidate(self):
        self.a.accepted=True; self.a.crash=True
        self.assertTrue(self.w.tick()['uncertain'])
        self.a.candidate={'identity':{'release':'v411'},'seal':'other'}
        self.w.tick()
        self.assertEqual(self.a.deploys,1)
    def test_busy_wait(self):
        self.a.accepted=True; self.a.idle=False
        self.assertEqual(self.w.tick()['phase'],'REVIEW_PENDING')
        self.assertEqual(self.a.deploys,0)
        self.a.idle=True
        self.assertEqual(self.w.tick()['phase'],'ACTIVE')
    def test_cas_preserved_across_poll(self):
        self.w.tick()
        self.a.current={'release':'v409-altered'}; self.a.accepted=True
        self.assertEqual(self.w.tick()['reason'],'Active baseline changed')
        self.assertEqual(self.a.deploys,0)
    def test_auth_fail_closed(self):
        self.a.accepted=True; self.a.allowed=False
        self.assertEqual(self.w.tick()['phase'],'BLOCKED')
        self.assertEqual(self.a.deploys,0)
    def test_interrupted_prepare_not_repeated(self):
        self.w.save({'phase':'PREPARING'})
        self.assertTrue(self.w.tick()['uncertain'])
        self.assertEqual(self.a.prepares,0)

if __name__=='__main__': unittest.main()
