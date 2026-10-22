"""Offline regression tests: every provider is disabled."""
import copy, hashlib, json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from iald_orchestrator import canonical_memory as m, nos_packet as n

class HistoricalPin(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(dir=WORK); self.addCleanup(self.tmp.cleanup)
  self.root=Path(self.tmp.name); self.releases=self.root/'releases';self.releases.mkdir()
  self.g='a'*64;self.current='b'*64;self.epoch='v392_'+self.g[:16]
  self.directory=self.releases/self.epoch;self.directory.mkdir()
  self.manifest={'generation':self.g,'source_mode':m.SNAPSHOT_MODE}
  raw=json.dumps(self.manifest).encode();(self.directory/'manifest.json').write_bytes(raw)
  self.pointer={'schema':1,'release':'v392','epoch':self.epoch,'generation':self.g,'manifest_sha256':m.digest(raw)}
  self.active=self.root/'ACTIVE.json';self.active.write_text(json.dumps(dict(self.pointer,generation=self.current,release='v393',epoch='v393_'+self.current[:16])))
  self.history=self.root/'ACTIVE.json.bak_20261014_1';self.history.write_text(json.dumps(self.pointer))
  self.ps=[patch.object(m,'ACTIVE',self.active),patch.object(m,'RELEASES',self.releases)]
  for p in self.ps:p.start();self.addCleanup(p.stop)
 def resolve(self):
  with patch.object(m,'load',return_value=(self.manifest,'VERIFIED')) as check:
   answer=m.resolve_generation(self.g)
   check.assert_called_once_with(self.directory,refresh=False)
   return answer
 def test_historical_reference_selected_without_active_change(self):
  before=self.active.read_bytes();self.assertEqual(self.resolve(),self.directory);self.assertEqual(before,self.active.read_bytes())
 def test_same_generation_current_is_supported(self):
  self.active.write_text(json.dumps(self.pointer));self.assertEqual(self.resolve(),self.directory)
 def test_identical_history_references_are_unambiguous(self):
  (self.root/'ACTIVE.json.bak_2').write_text(json.dumps(self.pointer));self.assertEqual(self.resolve(),self.directory)
 def test_missing_history_never_falls_back(self):
  self.history.unlink()
  with self.assertRaisesRegex(ValueError,'sem referência'):m.resolve_generation(self.g)
 def test_invalid_generation_refused(self):
  for value in ('../x','A'*64,'a'*63,1,None):
   with self.subTest(value=value),self.assertRaises(ValueError):m.resolve_generation(value)
 def test_conflicting_history_refused(self):
  (self.root/'ACTIVE.json.bak_2').write_text(json.dumps(dict(self.pointer,manifest_sha256='f'*64)))
  with self.assertRaisesRegex(ValueError,'conflitantes'):m.resolve_generation(self.g)
 def test_manifest_hash_tamper_refused(self):
  (self.directory/'manifest.json').write_bytes(b'{}')
  with self.assertRaises(ValueError):m.resolve_generation(self.g)
 def test_manifest_generation_mismatch_refused(self):
  raw=json.dumps(dict(self.manifest,generation='c'*64)).encode();(self.directory/'manifest.json').write_bytes(raw)
  self.history.write_text(json.dumps(dict(self.pointer,manifest_sha256=m.digest(raw))))
  with self.assertRaises(ValueError):m.resolve_generation(self.g)
 def test_non_snapshot_manifest_refused(self):
  raw=json.dumps(dict(self.manifest,source_mode='LIVE')).encode();(self.directory/'manifest.json').write_bytes(raw)
  self.history.write_text(json.dumps(dict(self.pointer,manifest_sha256=m.digest(raw))))
  with self.assertRaises(ValueError):m.resolve_generation(self.g)
 def test_epoch_traversal_refused(self):
  self.history.write_text(json.dumps(dict(self.pointer,epoch='../outside')))
  with self.assertRaises(ValueError):m.resolve_generation(self.g)
 def test_version_epoch_mismatch_refused(self):
  self.history.write_text(json.dumps(dict(self.pointer,release='v391')))
  with self.assertRaises(ValueError):m.resolve_generation(self.g)
 def test_unknown_pointer_fields_refused(self):
  self.history.write_text(json.dumps(dict(self.pointer,extra=1)))
  with self.assertRaises(ValueError):m.resolve_generation(self.g)
 def test_duplicate_pointer_keys_refused(self):
  self.history.write_text('{"generation":"'+self.g+'","generation":"'+self.g+'"}')
  with self.assertRaises(ValueError):m.resolve_generation(self.g)
 def test_invalid_index_or_source_error_is_not_swallowed(self):
  with patch.object(m,'load',side_effect=ValueError('Integridade fonte/index')):
   with self.assertRaisesRegex(ValueError,'Integridade'):m.resolve_generation(self.g)
 def test_missing_snapshot_error_is_not_swallowed(self):
  with patch.object(m,'load',side_effect=FileNotFoundError('snapshot')):
   with self.assertRaises(FileNotFoundError):m.resolve_generation(self.g)
 def test_loaded_generation_is_rechecked(self):
  with patch.object(m,'load',return_value=(dict(self.manifest,generation='c'*64),'VERIFIED')):
   with self.assertRaises(ValueError):m.resolve_generation(self.g)
 def test_oversize_pointer_refused(self):
  self.history.write_bytes(b' '*100001)
  with self.assertRaisesRegex(ValueError,'excede'):m.resolve_generation(self.g)

class QueuePin(unittest.TestCase):
 def setUp(self):
  self.g='a'*64
  self.c={'branch_id':'F1.REDE','required_provider':'mimo','max_projection_chars':None,'memory_generation':self.g}
  self.mem={'prompt':'original','receipt':{'generation':self.g,'sources':[],'packet_sha256':m.digest(b'original')}}
  self.packet={'prompt':'graph','receipt':{'canonical_memory':{'generation':self.g}}}
 def test_both_passes_use_the_same_historical_directory_and_keep_constraints(self):
  before=copy.deepcopy(self.c)
  with patch.object(m,'resolve_generation',return_value=Path('history')) as resolve,patch.object(m,'prepare',return_value=self.mem) as prep,patch.object(n,'board_unit',return_value={}),patch.object(n,'build',return_value=self.packet):
   # A truthy board record is required for graph augmentation.
   with patch.object(n,'board_unit',return_value={'id':'F1.REDE'}),patch.object(n,'_attach',return_value=self.mem):
    self.assertEqual(n.prepare_queue('task',self.c,'sys'),self.mem)
  resolve.assert_called_once_with(self.g);self.assertEqual(prep.call_count,2)
  self.assertTrue(all(x.kwargs['directory']==Path('history') for x in prep.call_args_list))
  self.assertEqual(self.c,before)
 def test_unpinned_requests_keep_existing_active_resolution(self):
  c=dict(self.c);c.pop('memory_generation')
  with patch.object(m,'resolve_generation') as resolve,patch.object(m,'prepare',return_value=self.mem) as prep,patch.object(n,'board_unit',return_value=None):
   n.prepare_queue('task',c,'sys')
  resolve.assert_not_called();self.assertNotIn('directory',prep.call_args.kwargs)
 def test_unknown_generation_refuses_before_memory_preparation(self):
  with patch.object(m,'resolve_generation',side_effect=ValueError('missing')),patch.object(m,'prepare') as prepare:
   with self.assertRaises(ValueError):n.prepare_queue('task',self.c,'sys')
  prepare.assert_not_called()
 def test_enforcement_still_rejects_a_wrong_packet(self):
  from iald_orchestrator import request_controls
  wrong=copy.deepcopy(self.mem);wrong['receipt']['generation']='b'*64
  with self.assertRaisesRegex(ValueError,'Geração canônica'):request_controls.enforce_packet(wrong,self.c,'sys')
 def test_graph_generation_guard_is_preserved(self):
  wrong=copy.deepcopy(self.packet);wrong['receipt']['canonical_memory']['generation']='b'*64
  with patch.object(m,'resolve_generation',return_value=Path('history')),patch.object(m,'prepare',return_value=self.mem),patch.object(n,'board_unit',return_value={'id':'F1.REDE'}),patch.object(n,'build',return_value=wrong):
   with self.assertRaisesRegex(ValueError,'generation changed'):n.prepare_queue('task',self.c,'sys')
 def test_old_branch_without_graph_still_uses_pinned_generation(self):
  with patch.object(m,'resolve_generation',return_value=Path('history')),patch.object(m,'prepare',return_value=self.mem) as prep,patch.object(n,'board_unit',return_value=None),patch.object(n,'build') as graph:
   self.assertEqual(n.prepare_queue('task',self.c,'sys'),self.mem)
  self.assertEqual(prep.call_args.kwargs['directory'],Path('history'));graph.assert_not_called()
