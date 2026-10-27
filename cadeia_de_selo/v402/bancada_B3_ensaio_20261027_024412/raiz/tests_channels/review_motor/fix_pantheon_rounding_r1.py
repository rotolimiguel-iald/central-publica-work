"""Candidate-only covariance format correction and synthetic regression tests."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import io
import json
import sys
import unittest
from unittest.mock import patch
import numpy as np

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]/"candidate"
TARGET=ROOT/"bancada/pantheon_cov.py"
RESULT=HERE/"PANTHEON_ROUNDING_R1.json"
if RESULT.exists():raise FileExistsError(RESULT)
before=TARGET.read_bytes()
def sha(raw):return hashlib.sha256(raw).hexdigest()
def write_new(path,raw):
    with path.open("xb") as stream:stream.write(raw)
    if path.read_bytes()!=raw:raise OSError("written bytes differ")
    return {"path":str(path),"sha256":sha(raw),"bytes":len(raw)}
source=before.decode("utf-8")
marker="\ndef carregar_cov(dir_tabelas):"
helper='''
SYMMETRY_MAX_ABS = 1.0e-7
SYMMETRY_MAX_REL_FROBENIUS = 1.0e-6


def _covariance_format(C):
    """Accept only bounded decimal-rounding asymmetry; do not alter source C.

    The existing consumer still symmetrizes its selected Cm as (Cm+Cm.T)/2.
    These are format tolerances, not a new covariance model or statistical fit.
    """
    if C.ndim != 2 or C.shape[0] != C.shape[1] or C.shape[0] == 0 or not np.isfinite(C).all():
        raise ValueError("covariância Pantheon: forma/valores inválidos")
    difference = C - C.T
    max_abs = float(np.max(np.abs(difference)))
    norm = float(np.linalg.norm(C, ord="fro"))
    relative = float(np.linalg.norm(difference, ord="fro") / norm) if norm else 0.0
    if (not np.isfinite(max_abs) or not np.isfinite(relative)
            or max_abs > SYMMETRY_MAX_ABS or relative > SYMMETRY_MAX_REL_FROBENIUS):
        raise ValueError("covariância Pantheon: assimetria excede limites de formato "
                         + repr(dict(max_abs=max_abs, rel_frobenius=relative,
                                     max_abs_limit=SYMMETRY_MAX_ABS, rel_frobenius_limit=SYMMETRY_MAX_REL_FROBENIUS)))
    return dict(max_abs=max_abs, rel_frobenius=relative,
                max_abs_limit=SYMMETRY_MAX_ABS, rel_frobenius_limit=SYMMETRY_MAX_REL_FROBENIUS,
                policy="BOUNDED_PUBLISHED_DECIMAL_ROUNDING", source_modified=False,
                consumer_symmetrization="Cm = 0.5 * (C_selected + C_selected.T)")

'''
if source.count(marker)!=1:raise ValueError("format helper anchor differs")
source=source.replace(marker,"\n"+helper+marker,1)
old='''            if C.shape != (m["n"], m["n"]) or not np.isfinite(C).all() or not np.allclose(C, C.T):
                raise ValueError("cache Pantheon inválido")
            return C, m'''
new='''            if C.shape != (m["n"], m["n"]):
                raise ValueError("cache Pantheon inválido")
            symmetry = _covariance_format(C)
            return C, dict(m, simetria_formato=symmetry, escrita_em_disco=False)'''
if source.count(old)!=1:raise ValueError("cache guard anchor differs")
source=source.replace(old,new,1)
old='''    if not np.allclose(C, C.T):
        raise ValueError("covariância Pantheon assimétrica")
    m = dict(fonte=src, fonte_sha256=h, n=n, cache="LEGACY_IGNORED_OR_ABSENT_PARSED_IN_RAM",
             simetrica_max_abs=float(np.max(np.abs(C - C.T))), escrita_em_disco=False)'''
new='''    symmetry = _covariance_format(C)
    m = dict(fonte=src, fonte_sha256=h, n=n, cache="LEGACY_IGNORED_OR_ABSENT_PARSED_IN_RAM",
             simetrica_max_abs=symmetry["max_abs"], simetria_formato=symmetry, escrita_em_disco=False)'''
if source.count(old)!=1:raise ValueError("source guard anchor differs")
source=source.replace(old,new,1)
compile(source,str(TARGET),"exec")
write_new(HERE/"pantheon_cov.py.before_rounding_r1",before)
temp=TARGET.with_name(TARGET.name+".rounding_r1.tmp")
write_new(temp,source.encode("utf-8"));temp.replace(TARGET)

sys.path.insert(0,str(ROOT))
from bancada import pantheon_cov as pc

class Rounding(unittest.TestCase):
    def test_small_published_rounding_accepted_and_measured(self):
        C=np.array([[.39,.001],[.001+3e-8,.20]])
        original=C.copy()
        meta=pc._covariance_format(C)
        self.assertLessEqual(meta["max_abs"],1e-7)
        self.assertLessEqual(meta["rel_frobenius"],1e-6)
        self.assertAlmostEqual(meta["max_abs"],3e-8)
        self.assertFalse(meta["source_modified"])
        np.testing.assert_array_equal(C,original)
    def test_absolute_limit_refuses(self):
        with self.assertRaises(ValueError):pc._covariance_format(np.array([[10.,0.],[2e-7,10.]]))
    def test_relative_limit_refuses_even_below_absolute_limit(self):
        with self.assertRaises(ValueError):pc._covariance_format(np.array([[1e-5,0.],[5e-8,1e-5]]))
    def test_source_read_once_metadata_and_no_rewrite(self):
        raw=b"2\n0.39\n0.001\n0.00100003\n0.2\n"
        with patch.object(pc.fontes,"read_checked",return_value=(raw,sha(raw))) as read,patch.object(pc.os.path,"isfile",return_value=False):
            C,meta=pc.carregar_cov("SYNTHETIC_NO_DIRECTORY")
        read.assert_called_once()
        self.assertEqual(meta["simetria_formato"]["max_abs_limit"],1e-7)
        self.assertFalse(meta["escrita_em_disco"])
        self.assertNotEqual(C[0,1],C[1,0])
    def test_cache_hash_still_refused_before_shape(self):
        source=b"2\n1\n0\n0\n1\n"
        cache=b"not the pinned bytes"
        meta={"fonte_sha256":sha(source),"cache_sha256":"0"*64,"n":2}
        with patch.object(pc.os.path,"isfile",return_value=True),patch.object(pc.fontes,"json_checked",return_value=(meta,"meta")),patch.object(pc.fontes,"read_checked",side_effect=[(source,sha(source)),(cache,sha(cache))]):
            with self.assertRaisesRegex(ValueError,"cache Pantheon difere"):
                pc.carregar_cov("SYNTHETIC_NO_DIRECTORY")

stream=io.StringIO()
started=datetime.now(timezone.utc).isoformat()
result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Rounding))
log=write_new(HERE/"PANTHEON_ROUNDING_R1.log",stream.getvalue().encode("utf-8"))
record={"unit":"F0.3.B2","claim_event":632,"start_utc":started,"end_utc":datetime.now(timezone.utc).isoformat(),
        "tests":result.testsRun,"success":result.wasSuccessful(),"before_sha256":sha(before),"after_sha256":sha(TARGET.read_bytes()),
        "bytes":TARGET.stat().st_size,"log":log,"max_abs_limit":pc.SYMMETRY_MAX_ABS,"rel_frobenius_limit":pc.SYMMETRY_MAX_REL_FROBENIUS,
        "integration_measurement_reported_by_root":{"statute":"DECLARADO nesta subunidade; root mediu a fonte pinada",
            "max_abs":3.0000000000038676e-8,"rel_frobenius":1.441433305656265e-7,"max_C":.3910331},
        "source_modified":False,"consumer_symmetrization_changed":False,"bancada_modified":False,
        "observed_fit":False,"script_sha256":sha(Path(__file__).read_bytes())}
rec=write_new(RESULT,(json.dumps(record,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
print(stream.getvalue());print(json.dumps({"receipt":rec,**record},ensure_ascii=False,indent=2))
raise SystemExit(0 if result.wasSuccessful() else 1)
