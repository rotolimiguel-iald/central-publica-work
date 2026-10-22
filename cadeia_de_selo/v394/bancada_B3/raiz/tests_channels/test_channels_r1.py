"""Candidate-only custody/parser tests and synthetic numeric tests; no data fit."""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
STAGE = HERE.parent / "candidate"
PACKAGE = "channel_fixture"
pkg = types.ModuleType(PACKAGE)
pkg.__path__ = [str(STAGE / "bancada")]
sys.modules[PACKAGE] = pkg
canonical = types.ModuleType(PACKAGE+".canonical")
canonical.require_current = lambda operation,root=None: {"operation":operation,"mode":"UNIT_TEST_CANONICAL_MOCK"}
canonical.read_alpha = lambda root=None: (0.005,{"um_py_sha256":"SYNTHETIC_TEST_VALUE","scope":"UNIT_TEST_CANONICAL_MOCK"})
sys.modules[canonical.__name__] = canonical

def load(name, *, virtual_root=None, suffix=""):
    source_path = STAGE / "bancada" / (name+".py")
    fullname = PACKAGE+"."+name+suffix
    module = types.ModuleType(fullname)
    module.__package__ = PACKAGE
    module.__file__ = str(source_path if virtual_root is None else virtual_root / "bancada" / (name+".py"))
    sys.modules[fullname] = module
    exec(compile(source_path.read_bytes(),module.__file__,"exec"),module.__dict__)
    return module

neff, neutrino = load("neff_canal"), load("neutrino_canal_v2")
legacy = load("neutrino_canal")
original_read = Path.read_bytes
counters = Counter()
toy_frozen = {"NEFF_SM":3.0,"MEDIDAS":[(3.2,0.2,"SYNTHETIC","TEST",True),(999.0,999.0,"CMB-SPA","OLD",False)],"PROJECOES":[]}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

class Channels(unittest.TestCase):
    def test_01_table5_exact_documentary_extraction(self):
        raw,source,_ = neff._sources()
        rows = neff._table5(raw["table5_v1"],"v1",source["table5_v1"])+neff._table5(raw["table5_v2"],"v2",source["table5_v2"])
        self.assertEqual([(r["N_eff_obs"],r["sigma_plus"],r["sigma_minus"]) for r in rows],
                         [(2.81,0.12,0.12),(2.99,0.22,0.26),(2.82,0.12,0.12),(2.96,0.21,0.24)])
        self.assertTrue(all(r["selected_for_verdict"] is False for r in rows))

    def test_02_synthetic_neff_runtime_and_unselected_yp(self):
        with patch.object(neff,"_frozen",return_value=toy_frozen):
            result = neff.canal(sigmas_extra=[0.1])
        self.assertEqual(result["beta_runtime"],0.005*math.sqrt(math.e))
        self.assertEqual(result["escolha_Yp"],"OPEN_X16_NO_SELECTION")
        self.assertIsNone(result["primary_observation"])
        self.assertEqual(len(result["medidas"]),1)
        self.assertEqual(result["medidas"][0]["rotulo"],"SYNTHETIC")
        self.assertEqual(result["calendar"],None)
        self.assertNotIn("quando_declarado",json.dumps(result))
        self.assertEqual(result["gate_effect"],"NONE")
        json.dumps(result,allow_nan=False)

    def test_03_invalid_numeric_inputs_refused_before_canonical(self):
        invalid = (True,False,float("nan"),float("inf"),float("-inf"),-1.0,"0.1",None,{},0.0)
        for value in invalid:
            with self.subTest(sigma=repr(value)),patch.object(neff,"require_current") as guard:
                with self.assertRaises(neff.FonteRecusada):
                    neff.canal(sigmas_extra=[value])
                guard.assert_not_called()
                counters["invalid_numeric_refusals"] += 1
        for value in invalid[:-1]:
            if value is None:
                continue
            with self.subTest(base=repr(value)),patch.object(neff,"require_current") as guard:
                with self.assertRaises(neff.FonteRecusada):
                    neff.canal(N_base=value)
                guard.assert_not_called()
                counters["invalid_numeric_refusals"] += 1

    def test_04_source_bytes_read_once_per_call(self):
        reads=Counter()
        def counted(path):
            reads[str(path.resolve())] += 1
            return original_read(path)
        with patch.object(Path,"read_bytes",counted),patch.object(neff,"_frozen",return_value=toy_frozen):
            neff.canal()
        self.assertEqual(len(reads),4)
        self.assertTrue(all(n==1 for n in reads.values()),reads)
        reads.clear()
        with patch.object(Path,"read_bytes",counted):
            neutrino.canal()
        self.assertTrue(all(n==1 for n in reads.values()),reads)

    def test_05_all_neff_source_mutations_refused(self):
        manifest=json.loads(original_read(neff.MANIFEST))
        paths=[neff.MANIFEST]+[(STAGE/e["relative_path"]).resolve() for e in manifest["sources"].values()]
        for target in paths:
            def altered(path):
                data=original_read(path)
                return bytes([data[0]^1])+data[1:] if path.resolve()==target.resolve() else data
            with self.subTest(target=target.name),patch.object(Path,"read_bytes",altered):
                with self.assertRaises(neff.FonteRecusada):
                    neff._sources()
                counters["neff_byte_mutations_refused"] += 1

    def test_06_all_neutrino_source_mutations_refused(self):
        manifest=json.loads(original_read(neutrino.MANIFEST))
        entries=manifest["scripts"]+list(manifest["documents"].values())+manifest["primary_pdfs"]+manifest["context_sources"]
        paths=[neutrino.MANIFEST]+[(STAGE/e["relative_path"]).resolve() for e in entries]
        for target in paths:
            def altered(path):
                data=original_read(path)
                return bytes([data[0]^1])+data[1:] if path.resolve()==target.resolve() else data
            with self.subTest(target=target.name),patch.object(Path,"read_bytes",altered):
                with self.assertRaises(neutrino.FonteRecusada):
                    neutrino._load_sources()
                counters["neutrino_byte_mutations_refused"] += 1

    def test_07_canonical_refusal_propagates(self):
        for module in (neff,neutrino):
            with patch.object(module,"require_current",side_effect=ValueError("CANONICAL_DRIFT")):
                with self.assertRaisesRegex(ValueError,"CANONICAL_DRIFT"):
                    module.canal()

    def test_08_legacy_alias_current_contract(self):
        current=neutrino.canal()
        old=legacy.canal()
        self.assertEqual(current["rows"],old["rows"])
        self.assertTrue(old["legacy_alias"])
        self.assertEqual(old["requested_endpoint"],"neutrino_canal_f72")
        self.assertEqual(old["served_contract"],"F7_2_B2_SELF_CONTAINED")
        self.assertEqual(old["overall_verdict"],"SEM_LIMITE_TGL")
        self.assertFalse(old["likelihood_available"])
        self.assertTrue(all(row["tau_star_limit_s"] is None for row in old["rows"]))

    def test_09_corrected_juno_anchor_and_historical_clock(self):
        result=neutrino.canal()
        juno=next(r for r in result["rows"] if r["channel"]=="JUNO_2026_EQUAL_21_31")
        self.assertIn("Sec. III.B",juno["citation_anchor"])
        self.assertEqual(juno["published_model_limit"]["gamma_channel"],"Gamma_21=Gamma_31; Gamma_32=0")
        clock=result["clock_v369_context"]
        self.assertFalse(clock["observed_measurement"])
        self.assertEqual(clock["kind"],"CONDITIONAL_5SIGMA_PROJECTION")
        self.assertTrue(clock["source_basis"]["path"].endswith("historical_clock_v369.json"))

    def test_10_sources_are_relative_and_contained(self):
        for module in (neff,neutrino):
            manifest=json.loads(original_read(module.MANIFEST))
            def walk(value):
                if isinstance(value,dict):
                    if "relative_path" in value:
                        p=Path(value["relative_path"])
                        self.assertFalse(p.is_absolute())
                        self.assertNotIn("..",p.parts)
                    for child in value.values():
                        walk(child)
                elif isinstance(value,list):
                    for child in value:
                        walk(child)
            walk(manifest)
        for module,method in ((neff,"_read_entry"),(neutrino,"_source")):
            with self.assertRaises(module.FonteRecusada):
                getattr(module,method)({"relative_path":"../../outside","sha256":"0"*64,"bytes":10})

    def test_11_missing_source_refused(self):
        for module in (neff,neutrino):
            target=module.MANIFEST
            def missing(path):
                if path.resolve()==target.resolve():
                    raise FileNotFoundError("synthetic missing source")
                return original_read(path)
            with patch.object(Path,"read_bytes",missing),self.assertRaises(module.FonteRecusada):
                module._sources() if module is neff else module._load_sources()

    def test_12_duplicate_frozen_field_and_table_anchor_refused(self):
        with self.assertRaises(neff.FonteRecusada):
            neff._frozen(b"NEFF_SM=3\nNEFF_SM=4\nMEDIDAS=[]\nPROJECOES=[]")
        with self.assertRaises(neff.FonteRecusada):
            neff._table5(b'<table id="S7.T5.2"></table><table id="S7.T5.2"></table>',"v2",{})

    def test_13_relocation_without_original_paths(self):
        virtual=(HERE/"virtual_relocated_root").resolve()
        relocated_neff=load("neff_canal",virtual_root=virtual,suffix="_relocated")
        relocated_neutrino=load("neutrino_canal_v2",virtual_root=virtual,suffix="_relocated")
        def mapped(path):
            resolved=path.resolve()
            if not resolved.is_relative_to(virtual):
                raise AssertionError("unexpected original-path read: "+str(path))
            return original_read(STAGE/resolved.relative_to(virtual))
        with patch.object(Path,"read_bytes",mapped),patch.object(relocated_neff,"_frozen",return_value=toy_frozen):
            n=relocated_neff.canal()
            v=relocated_neutrino.canal()
        self.assertEqual(n["escolha_Yp"],"OPEN_X16_NO_SELECTION")
        self.assertEqual(v["overall_verdict"],"SEM_LIMITE_TGL")
        self.assertTrue(all(str(virtual) in s["path"] for s in v["primary_pdfs"].values()))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--run",default="R1")
    args=parser.parse_args()
    if not args.run.isascii() or not args.run.replace("_","").isalnum():
        raise ValueError("invalid run identifier")
    log=HERE/("TEST_CHANNELS_"+args.run+".log")
    receipt=HERE/("TEST_CHANNELS_"+args.run+".json")
    if log.exists() or receipt.exists():
        raise FileExistsError("test evidence already exists")
    started=datetime.now(timezone.utc).isoformat()
    output=io.StringIO()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Channels)
    result=unittest.TextTestRunner(stream=output,verbosity=2).run(suite)
    raw=output.getvalue().encode("utf-8")
    with log.open("xb") as stream:
        stream.write(raw)
    sources={}
    for p in sorted((STAGE/"bancada").glob("*")):
        if p.name in {"neff_canal.py","neff_fontes_f52.json","neutrino_canal.py","neutrino_canal_v2.py","neutrino_fontes_f72_b2.json"}:
            content=p.read_bytes()
            sources[p.name]={"sha256":sha(content),"bytes":len(content)}
    record={"unit":"F0.3.B2","claim_event":632,"started_utc":started,"ended_utc":datetime.now(timezone.utc).isoformat(),
            "tests":result.testsRun,"success":result.wasSuccessful(),"failures":len(result.failures),"errors":len(result.errors),
            "counters":dict(counters),"canonical":"API mocked with synthetic alpha; end-to-end current contract is root's integration test",
            "scientific_scope":"Documentary extraction of pinned Table5; numerical comparison only synthetic centers; source inventory is not an observed likelihood run",
            "log":{"path":str(log),"sha256":sha(raw),"bytes":len(raw)},"candidate_sources":sources,
            "test_script_sha256":sha(Path(__file__).read_bytes()),"writes_bancada":False,"nature_verdict":None}
    with receipt.open("xb") as stream:
        stream.write((json.dumps(record,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
    print(output.getvalue())
    print(json.dumps(record,ensure_ascii=False,indent=2))
    return 0 if result.wasSuccessful() else 1

if __name__=="__main__":
    raise SystemExit(main())
