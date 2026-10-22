"""Offline read-only preflight tests; actual SQLite guard, no server/config imports."""
from datetime import datetime, timedelta, timezone
import math
from pathlib import Path
import sqlite3
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from test_public_budgets import WORK, SpendingGuard, BudgetError, router


class BudgetRemainingTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(dir=WORK)
        self.addCleanup(temp.cleanup)
        self.now = datetime(2026, 10, 1, 1, 0, tzinfo=timezone.utc)
        self.guard = SpendingGuard(Path(temp.name) / 'audit.sqlite3', clock=lambda: self.now)
        self.sequence = 0

    def row(self, user='alice', cap=.25, actual=None, key='alice', group=None, day=None):
        self.sequence += 1
        with self.guard._connect() as db:
            db.execute('INSERT INTO calls (id,user,day,model,cap,actual,status,quota_key,group_name) '
                       'VALUES (?,?,?,?,?,?,?,?,?)', (str(self.sequence), user,
                       day or self.now.astimezone(timezone.utc).date().isoformat(), 'synthetic',
                       cap, actual, 'reserved' if actual is None else 'settled', key, group))

    def remaining(self, user='alice', own=1., total=5., **kwargs):
        return router.budget_remaining(self.guard, user, own, total, **kwargs)

    def test_empty_ledger_and_repeated_reads_do_not_create_calls(self):
        with patch.object(self.guard, 'reserve', side_effect=AssertionError('Must not reserve')):
            self.assertTrue(self.remaining())
            self.assertTrue(self.remaining())
        with self.guard._connect() as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM calls').fetchone()[0], 0)

    def test_active_hold_exhausts_own_quota_at_exact_limit(self):
        self.row(cap=1.)
        self.assertFalse(self.remaining())
        self.assertTrue(self.remaining('bob'))

    def test_settled_cost_replaces_cap_and_zero_is_valid(self):
        self.row(cap=3., actual=.25)
        self.row(cap=3., actual=0.)
        self.assertTrue(self.remaining())
        self.assertFalse(self.remaining(own=.25))

    def test_global_includes_other_users_and_active_holds(self):
        self.row(user='bob', key='bob', cap=5.)
        self.assertFalse(self.remaining())

    def test_group_counts_all_accounts_but_not_other_groups(self):
        self.row(user='bob', key='bob', cap=.5, group='haiku_public')
        self.row(user='carol', key='carol', cap=2., group='other')
        self.assertFalse(self.remaining(group='haiku_public', group_limit=.5))
        self.assertTrue(self.remaining(group='haiku_public', group_limit=.75))

    def test_identity_uses_union_without_double_counting(self):
        self.row(cap=.25, key='shared')
        self.row(user='old-name', cap=.25, key='shared')
        self.row(cap=.25, key='older-identity')
        self.assertFalse(self.remaining(own=.75, quota_key='shared'))
        self.assertTrue(self.remaining(own=1., quota_key='shared'))

    def test_legacy_null_key_is_attributed_without_writing(self):
        self.row(cap=.75, key=None, group='old-group')
        with self.guard._connect() as db:
            before = db.execute('SELECT * FROM calls').fetchall()
        self.assertFalse(self.remaining(quota_key='shared', group='haiku_public', group_limit=.75))
        with self.guard._connect() as db:
            self.assertEqual(db.execute('SELECT * FROM calls').fetchall(), before)
        # Match the existing reserve's migration semantics, using the real guard.
        with self.assertRaises(BudgetError):
            self.guard.reserve('alice', 'synthetic', .01, 1., 5., quota_key='shared',
                               group='haiku_public', group_limit=.75)

    def test_other_users_legacy_rows_are_not_migrated_into_this_group(self):
        self.row(user='bob', cap=1., key=None)
        self.assertTrue(self.remaining(group='haiku_public', group_limit=.5))
        self.assertFalse(self.remaining(total=1., group='haiku_public', group_limit=.5))

    def test_omitted_and_empty_quota_key_match_reserve_fallback(self):
        self.row(user='old-name', key='alice', cap=1.)
        self.assertFalse(self.remaining())
        self.assertFalse(self.remaining(quota_key=''))

    def test_previous_day_cost_does_not_exhaust_current_day(self):
        self.row(cap=10., day='2026-09-30')
        self.assertTrue(self.remaining())

    def test_utc_day_comes_from_guard_clock_not_machine_clock(self):
        self.now = datetime(2026, 9, 30, 22, 0, tzinfo=timezone(timedelta(hours=-3)))
        self.row(cap=1., day='2026-10-01')
        self.assertFalse(self.remaining())

    def test_naive_or_invalid_clock_fails_visibly(self):
        for now in (datetime(2026, 10, 1), '2026-10-01'):
            # check() uses the real default guard clock; isolate this reader's clock contract.
            with self.subTest(now=now), patch.object(self.guard, 'check'), patch.object(self.guard, 'clock', return_value=now):
                with self.assertRaises(ValueError): self.remaining()

    def test_existing_guard_pause_is_respected(self):
        key = self.guard.reserve('alice', 'synthetic', .1, 1., 5.)
        self.guard.settle(key, amount=.2)
        with self.assertRaises(BudgetError): self.remaining()
        self.assertTrue(self.remaining('bob'))

    def test_invalid_limits_fail_closed(self):
        for bad in (0., -1., float('nan'), float('inf'), True, '1', None, 10 ** 1000):
            for field in ('own', 'total', 'group_limit'):
                if field == 'group_limit' and bad is None: continue
                with self.subTest(field=field, bad=str(bad)[:30]), self.assertRaises(ValueError):
                    self.remaining(**{field: bad})

    def test_negative_infinite_and_text_costs_fail_closed(self):
        for field in ('cap', 'actual'):
            for value in (-1., math.inf, 'unreadable'):
                with self.guard._connect() as db: db.execute('DELETE FROM calls')
                self.row(**{field: value})
                with self.subTest(field=field, value=value), self.assertRaises(ValueError): self.remaining()

    def test_nonfinite_total_is_not_accepted(self):
        self.row(cap=1e308)
        self.row(user='bob', cap=1e308)
        with self.assertRaises(ValueError): self.remaining(own=1.7e308, total=1.7e308)

    def test_database_read_failure_is_visible(self):
        with self.guard._connect() as db: db.execute('DROP TABLE calls')
        with self.assertRaises(sqlite3.Error): self.remaining()

    def test_positive_balance_does_not_admit_an_oversized_next_call(self):
        self.row(cap=.75)
        self.assertTrue(self.remaining())
        with self.assertRaises(BudgetError):
            self.guard.reserve('alice', 'synthetic', .5, 1., 5.)


if __name__ == '__main__': unittest.main(verbosity=2)
