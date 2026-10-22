"""Synthetic filesystem only. Never invokes production preparer main or Git."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import prepare_mobile as mobile


class PrepareMobileTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent)
        self.addCleanup(temp.cleanup)
        base = Path(temp.name)
        self.work, self.root = base / 'work', base / 'root'
        self.repo = self.root / 'iald-app'
        (self.work / 'stage').mkdir(parents=True)
        (self.root / 'app').mkdir(parents=True)
        raw = {'www/iald.js': b'old js\r\n', 'www/iald.css': b'old css\r\n',
               mobile.IOS: b'CURRENT_PROJECT_VERSION = 27;\r\nMARKETING_VERSION = 4.1;\r\n' * 2,
               mobile.ANDROID: b'versionCode 24\r\nversionName "4.1"\r\n'}
        for name, content in raw.items():
            target = self.repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        for name in mobile.ASSETS:
            content = ('new ' + name + '\n').encode()
            (self.work / 'stage' / name).write_bytes(content)
            (self.root / 'app' / name).write_bytes(content)
        self.state = dict(head='synthetic-head', branch='synthetic-branch', status='')
        self.baseline = dict(head=self.state['head'], branch=self.state['branch'],
                             sha256={name: mobile.sha(content) for name, content in raw.items()})
        patched = patch.object(mobile, 'git_state', side_effect=lambda repo: dict(self.state))
        patched.start()
        self.addCleanup(patched.stop)

    def plan(self):
        return mobile.make_plan(self.work, self.root, self.baseline)

    def test_check_only_does_not_write(self):
        before = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.plan()
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()})
        self.assertFalse((self.work / 'backups').exists())

    def test_web_must_match_staged_bytes(self):
        (self.root / 'app/iald.css').write_bytes(b'not deployed')
        with self.assertRaisesRegex(RuntimeError, 'Deploy web'): self.plan()

    def test_head_branch_and_dirty_worktree_are_rejected(self):
        for field in ('head', 'branch', 'status'):
            old = self.state[field]
            self.state[field] = 'changed'
            with self.subTest(field=field), self.assertRaises(RuntimeError): self.plan()
            self.state[field] = old

    def test_each_target_baseline_is_checked(self):
        for relative in mobile.TARGETS:
            path = self.repo / relative
            old = path.read_bytes()
            path.write_bytes(old + b'changed')
            with self.subTest(relative=relative), self.assertRaisesRegex(RuntimeError, 'Baseline changed'):
                self.plan()
            path.write_bytes(old)

    def test_wrong_version_refused_even_when_hash_matches(self):
        for relative, old, new in ((mobile.IOS, b'= 27;', b'= 29;'),
                                   (mobile.ANDROID, b'Code 24', b'Code 26')):
            path = self.repo / relative
            raw = path.read_bytes()
            path.write_bytes(raw.replace(old, new))
            self.baseline['sha256'][relative] = mobile.sha(path.read_bytes())
            with self.subTest(relative=relative), self.assertRaisesRegex(RuntimeError, 'Expected exactly'):
                self.plan()
            path.write_bytes(raw)
            self.baseline['sha256'][relative] = mobile.sha(raw)

    def test_apply_changes_only_four_targets_and_backups_stay_in_work(self):
        plan = self.plan()
        before = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        receipt = mobile.apply_plan(plan, self.work)
        changed = {p for p in before if p.read_bytes() != before[p]}
        self.assertEqual(changed, {self.repo / relative for relative in mobile.TARGETS})
        self.assertEqual(set(before), {p for p in self.root.rglob('*') if p.is_file()})
        backup_dir = Path(receipt['backups'])
        self.assertTrue(backup_dir.is_relative_to(self.work))
        for row in plan['files']:
            self.assertEqual((backup_dir / (row['relative'].replace('/', '__') + '.before')).read_bytes(), row['before'])
        self.assertEqual((self.repo / mobile.IOS).read_bytes().count(b'= 28;'), 2)
        self.assertIn(b'versionCode 25\r\n', (self.repo / mobile.ANDROID).read_bytes())
        self.assertEqual(json.loads((self.work / 'mobile_prepared.json').read_bytes())['status'], 'prepared')
        self.assertFalse((self.work / '.prepare_mobile.lock').exists())
        with self.assertRaisesRegex(RuntimeError, 'Baseline changed'): self.plan()

    def test_destination_and_source_changes_after_plan_prevent_all_writes(self):
        for path in (self.repo / mobile.IOS, self.root / 'app/iald.js', self.work / 'stage/iald.css'):
            plan = self.plan()
            raw = path.read_bytes()
            path.write_bytes(raw + b'concurrent')
            before = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
            with self.subTest(path=path), self.assertRaisesRegex(RuntimeError, 'Preparation failed'):
                mobile.apply_plan(plan, self.work)
            self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()})
            path.write_bytes(raw)

    def test_partial_failure_reports_changes_and_retains_backups(self):
        plan = self.plan()
        actual_replace = mobile.os.replace
        calls = []
        def replace(source, target):
            calls.append(target)
            if len(calls) == 2: raise OSError('synthetic write failure')
            actual_replace(source, target)
        with patch.object(mobile.os, 'replace', side_effect=replace):
            with self.assertRaisesRegex(RuntimeError, "changed=\\['www/iald.js'\\]"):
                mobile.apply_plan(plan, self.work)
        self.assertEqual(len(list((self.work / 'backups').rglob('*.before'))), 4)
        self.assertFalse((self.work / 'mobile_prepared.json').exists())
        self.assertFalse((self.work / '.prepare_mobile.lock').exists())


if __name__ == '__main__': unittest.main(verbosity=2)
