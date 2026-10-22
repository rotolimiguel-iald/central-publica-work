"""Standalone monthly IALD wallet. Trusted server integration only; no providers.

Contract
--------
Wallet(path, clock=aware_datetime_callable) uses a file-backed SQLite database,
one connection per transaction, BEGIN IMMEDIATE, and integer nanoUSD throughout.
Owner is an opaque SHA-256 (64 lowercase hex), never a username or email.

ensure_account(owner, anchor=None, exempt=False): immutable account policy;
anchor defaults to now and may be in the past, never in the future. First $3.50
at the anchor, second at cycle start + 15 days. Subsequent cycles use the
ORIGINAL UTC calendar day/time, clipped to month end (Jan31 -> Feb28 -> Mar31).
All positive balance, INCLUDING manual credits, expires at each boundary before
the new first installment. Negative balance ALWAYS carries. No advance button.
Price BRL70 is metadata only, not a checkout, subscription or payment receipt.

begin_task(owner, task_id): only a new receipt with may_dispatch=True permits
dispatch. Duplicate active/terminal IDs NEVER permit another dispatch. A refused
ID is terminal too; a later attempt needs a new ID. Exactly one active task per
owner, including exempt accounts. Admission needs balance > 0 or exemption;
there is no estimated reservation or cost limit on the admitted task.

record_cost(owner, task_id, event_id, amount_usd, provider, model, status): one
immutable measured/estimated/estimated_components event; all providers/tools/JEV
share this ledger. estimated_components requires an explicit positive total for
known usage with estimated cost components; it must not represent unknown usage.
Already-admitted tasks may overrun below zero. Late usage may be recorded after
finish/reconciliation, but does not reopen a task. Record a cost ONCE: reporting
an estimate and then measured usage under different IDs would debit twice.
Matching duplicate events are safe; changed fields or owner/task takeover fail.
USD accepts Decimal/string/int/finite float, rounded HALF_UP to 9 decimal places.
All receipts include exact integer nanoUSD and a fixed-precision USD string.

finish_task(owner, task_id, status): completed/failed/cancelled/interrupted;
does not refund spend, clear debt or reopen IDs. Duplicate identical finish is
idempotent. Unknown, refused or differently-finished tasks cannot be finished.

begin_call(owner, task_id, event_id, cap_usd, provider, model, billing_basis=...): persist a
pending bound BEFORE sending. Requires an active admitted task, NOT a positive
balance. It does not reserve/debit funds. Only may_dispatch=True authorizes the
first send. Pending duplicates/restarts NEVER authorize automatic replay.
settle_call(owner, task_id, event_id, amount_usd=None, status='estimated',
evidence=...): measured requires explicit amount and provider evidence reference;
estimated charges exactly the registered cap for unknown usage.
estimated_components requires an explicit positive total, independent of cap,
for known usage plus estimated charges (for example, measured token usage plus
an estimated container fee). Caller retains the component breakdown/evidence;
the wallet records this status without claiming the total is measured. Missing
usage still requires estimated at full cap, never estimated_components.
Zero cap is admitted ONLY for
provider='kimi' with explicit billing_basis='subscription_included_no_incremental_API_charge';
this is a documented billing basis, not a guessed marginal token tariff. Measured
usage may exceed cap. Settlement and debit are one transaction, immutable and
idempotent. No later measured event may debit an already settled call again.
record_cost cannot bypass this path for registered call IDs. Its unregistered
events are only for already-known costs, not uncertain external calls.
finish_task/reconcile refuse any pending calls. pending_calls(owner, ...) is a
paginated recovery inventory, not a replay queue. Caller verifies evidence;
wallet neither contacts providers nor assumes that a timeout means free usage.
evidence is optional; when omitted the explicit settlement call is recorded as
a caller attestation, not independently verified provider evidence. Measured zero
may represent verified no-dispatch/no-charge. Preserve token evidence externally.

admin_credit(owner, event_id, amount, note): positive manual credit, immutable
and idempotent. Credits offset existing debt first and expire if still positive
at the boundary. This method performs NO authentication: expose ONLY through
trusted admin authorization, never through a model tool/public self-credit API.

reconcile(owner, proven_terminal_tasks, evidence=...): explicit mapping of IDs
to terminal statuses plus a nonempty opaque evidence reference. Caller verifies
the proof; wallet validates ownership/state and records it atomically. Startup
does NOT close, resume or replay tasks. Unknown/cross-owner/conflicting IDs fail
the entire reconciliation. Duplicate terminal confirmations preserve first proof.

snapshot(owner): lazily posts scheduled releases/expiry in the same transaction;
includes cycle, next release, allowance/released/balance/available/debt, exemption
and active task. No credential, username, conversation or prompt is accepted.
Admin notes/evidence must be non-sensitive references; they are not in snapshots.

No old provider-spend backfill. Past anchors replay only calendar entries, never
external calls. Existing anchor/exemption cannot be changed by ensure_account.
All boundaries are UTC; clock regression is refused visibly. No remote I/O.
"""

from __future__ import annotations

from calendar import monthrange
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, localcontext
from pathlib import Path
import re
import sqlite3

NANO_USD = 1_000_000_000
INSTALLMENT_NANO_USD = 3_500_000_000
MONTHLY_ALLOWANCE_NANO_USD = 7_000_000_000
PLAN_PRICE_BRL = "70.00"
POLICY = "EXPIRE_ALL_POSITIVE_CARRY_ALL_DEBT"
API_CHARGE = "api_charge"
SUBSCRIPTION_INCLUDED = "subscription_included_no_incremental_API_charge"
SCHEMA_VERSION = 1
MAX_MONEY = 9_223_372_036_854_775_807
TERMINAL_STATUSES = frozenset({"completed", "failed", "cancelled", "interrupted"})
COST_STATUSES = frozenset({"measured", "estimated", "estimated_components"})
_OWNER = re.compile(r"[0-9a-f]{64}\Z")
_LABEL = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:/-]{0,159}\Z")


class WalletError(ValueError):
    """Fail-closed wallet error, never a dispatch authorization."""


class InvalidArgument(WalletError):
    pass


class AccountNotFound(WalletError):
    pass


class IdentityConflict(WalletError):
    """Existing identity belongs to a different owner or immutable payload."""


class TaskStateError(WalletError):
    pass


class ClockRegression(WalletError):
    pass


def _owner(value):
    if type(value) is not str or not _OWNER.fullmatch(value):
        raise InvalidArgument("owner must be a lowercase SHA-256")
    return value


def _text(value, name, maximum=200):
    if (type(value) is not str or not value or value != value.strip()
            or len(value) > maximum or any(ord(c) < 32 or ord(c) == 127 for c in value)):
        raise InvalidArgument(f"Invalid {name}")
    return value


def _identifier(value, name):
    value = _text(value, name)
    if value.startswith("wallet:"):
        raise InvalidArgument("Reserved wallet identity namespace")
    return value


def _label(value, name):
    if type(value) is not str or not _LABEL.fullmatch(value):
        raise InvalidArgument(f"Invalid {name}")
    return value


def _time(value):
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise InvalidArgument("Invalid timestamp") from exc
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise InvalidArgument("An aware datetime or ISO timestamp is required")
    return value.astimezone(timezone.utc)


def _iso(value):
    return value.isoformat(timespec="microseconds")


def _money(value, *, positive=False):
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise InvalidArgument("USD amount must be decimal numeric data")
    try:
        if len(str(value)) > 100:
            raise InvalidArgument("USD amount is too long")
        with localcontext() as ctx:
            ctx.prec = 80
            amount = Decimal(str(value))
            if not amount.is_finite() or amount < 0 or amount > Decimal(MAX_MONEY) / NANO_USD:
                raise InvalidArgument("USD amount is outside the admitted range")
            nano = int((amount * NANO_USD).to_integral_value(rounding=ROUND_HALF_UP))
    except (InvalidOperation, OverflowError, ValueError) as exc:
        if isinstance(exc, WalletError):
            raise
        raise InvalidArgument("Invalid USD amount") from exc
    if nano > MAX_MONEY or (positive and nano <= 0):
        raise InvalidArgument("Manual credit must be positive in nanoUSD")
    return nano


def _usd(nano):
    sign = "-" if nano < 0 else ""
    value = abs(nano)
    return f"{sign}{value // NANO_USD}.{value % NANO_USD:09d}"


def _month(anchor, index):
    absolute = anchor.year * 12 + anchor.month - 1 + index
    year, month0 = divmod(absolute, 12)
    if not 1 <= year <= 9999:
        raise InvalidArgument("Calendar outside supported datetime range")
    month = month0 + 1
    return anchor.replace(year=year, month=month,
                          day=min(anchor.day, monthrange(year, month)[1]))


_DDL = (
    "CREATE TABLE IF NOT EXISTS wallet_meta (id INTEGER PRIMARY KEY CHECK(id=1), version INTEGER NOT NULL, policy TEXT NOT NULL)",
    """CREATE TABLE IF NOT EXISTS accounts (
        owner TEXT PRIMARY KEY, anchor TEXT NOT NULL, exempt INTEGER NOT NULL CHECK(exempt IN(0,1)),
        balance INTEGER NOT NULL CHECK(typeof(balance)='integer'),
        cycle_index INTEGER NOT NULL CHECK(cycle_index>=0),
        released INTEGER NOT NULL CHECK(released IN(3500000000,7000000000)),
        phase INTEGER NOT NULL CHECK(phase IN(1,2)), created_at TEXT NOT NULL, last_seen TEXT NOT NULL)""",
    """CREATE TABLE IF NOT EXISTS tasks (
        task_id TEXT PRIMARY KEY, owner TEXT NOT NULL REFERENCES accounts(owner),
        admitted INTEGER NOT NULL CHECK(admitted IN(0,1)),
        status TEXT NOT NULL CHECK(status IN('active','completed','failed','cancelled','interrupted','rejected_balance','rejected_active')),
        created_at TEXT NOT NULL, finished_at TEXT, evidence TEXT,
        UNIQUE(owner,task_id))""",
    "CREATE UNIQUE INDEX IF NOT EXISTS wallet_one_active ON tasks(owner) WHERE status='active'",
    """CREATE TABLE IF NOT EXISTS calls (
        seq INTEGER PRIMARY KEY AUTOINCREMENT, event_id TEXT NOT NULL UNIQUE,
        owner TEXT NOT NULL, task_id TEXT NOT NULL,
        cap INTEGER NOT NULL CHECK(typeof(cap)='integer' AND cap>=0),
        provider TEXT NOT NULL, model TEXT NOT NULL,
        billing_basis TEXT NOT NULL,
        status TEXT NOT NULL CHECK(status IN('pending','settled')),
        created_at TEXT NOT NULL, settled_at TEXT, evidence TEXT,
        FOREIGN KEY(owner,task_id) REFERENCES tasks(owner,task_id),
        CHECK((billing_basis='api_charge' AND cap>0) OR
              (billing_basis='subscription_included_no_incremental_API_charge' AND cap=0 AND provider='kimi')))""",
    "CREATE INDEX IF NOT EXISTS wallet_calls_pending ON calls(owner,status,seq)",
    """CREATE TRIGGER IF NOT EXISTS wallet_calls_no_delete BEFORE DELETE ON calls
       BEGIN SELECT RAISE(ABORT,'Provider calls are permanent'); END""",
    """CREATE TRIGGER IF NOT EXISTS wallet_calls_settle_only BEFORE UPDATE ON calls
       WHEN OLD.status!='pending' OR NEW.status!='settled' OR NEW.owner!=OLD.owner
         OR NEW.task_id!=OLD.task_id OR NEW.event_id!=OLD.event_id OR NEW.cap!=OLD.cap
         OR NEW.provider!=OLD.provider OR NEW.model!=OLD.model OR NEW.created_at!=OLD.created_at
         OR NEW.billing_basis!=OLD.billing_basis
       BEGIN SELECT RAISE(ABORT,'Call identity/state transition refused'); END""",
    """CREATE TABLE IF NOT EXISTS entries (
        seq INTEGER PRIMARY KEY AUTOINCREMENT, event_id TEXT NOT NULL UNIQUE,
        owner TEXT NOT NULL REFERENCES accounts(owner), task_id TEXT,
        kind TEXT NOT NULL CHECK(kind IN('installment','expiry','cost','admin_credit')),
        delta INTEGER NOT NULL CHECK(typeof(delta)='integer'),
        balance_after INTEGER NOT NULL CHECK(typeof(balance_after)='integer'),
        provider TEXT, model TEXT, cost_status TEXT, note TEXT,
        effective_at TEXT NOT NULL, recorded_at TEXT NOT NULL,
        FOREIGN KEY(owner,task_id) REFERENCES tasks(owner,task_id))""",
    "CREATE INDEX IF NOT EXISTS wallet_entries_owner ON entries(owner,seq)",
    "CREATE INDEX IF NOT EXISTS wallet_entries_task ON entries(task_id,seq)",
    """CREATE TRIGGER IF NOT EXISTS wallet_entries_no_update BEFORE UPDATE ON entries
       BEGIN SELECT RAISE(ABORT,'Wallet entries are immutable'); END""",
    """CREATE TRIGGER IF NOT EXISTS wallet_entries_no_delete BEFORE DELETE ON entries
       BEGIN SELECT RAISE(ABORT,'Wallet entries are immutable'); END""",
    """CREATE TRIGGER IF NOT EXISTS wallet_tasks_no_delete BEFORE DELETE ON tasks
       BEGIN SELECT RAISE(ABORT,'Task identities are permanent'); END""",
    """CREATE TRIGGER IF NOT EXISTS wallet_tasks_finish_only BEFORE UPDATE ON tasks
       WHEN OLD.status!='active' OR NEW.owner!=OLD.owner OR NEW.task_id!=OLD.task_id
         OR NEW.admitted!=OLD.admitted OR NEW.created_at!=OLD.created_at
         OR NEW.status NOT IN('completed','failed','cancelled','interrupted')
       BEGIN SELECT RAISE(ABORT,'Task identity/state transition refused'); END""",
    """CREATE TRIGGER IF NOT EXISTS wallet_account_policy_immutable BEFORE UPDATE ON accounts
       WHEN NEW.owner!=OLD.owner OR NEW.anchor!=OLD.anchor OR NEW.exempt!=OLD.exempt
       BEGIN SELECT RAISE(ABORT,'Account policy is immutable'); END""",
)


class Wallet:
    def __init__(self, path, clock=None):
        if str(path) == ":memory:" or str(path).startswith("file:"):
            raise InvalidArgument("Use a local file-backed SQLite path")
        self.path = Path(path).resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.clock = clock or (lambda: datetime.now(timezone.utc))
        with self._transaction() as db:
            for statement in _DDL:
                db.execute(statement)
            db.execute("INSERT OR IGNORE INTO wallet_meta VALUES(1,?,?)", (SCHEMA_VERSION, POLICY))
            row = db.execute("SELECT version,policy FROM wallet_meta WHERE id=1").fetchone()
            if tuple(row) != (SCHEMA_VERSION, POLICY):
                raise WalletError("Unsupported wallet schema or policy")

    @contextmanager
    def _transaction(self):
        db = sqlite3.connect(self.path, timeout=30, isolation_level=None)
        db.row_factory = sqlite3.Row
        try:
            db.execute("PRAGMA foreign_keys=ON")
            db.execute("PRAGMA synchronous=FULL")
            db.execute("PRAGMA busy_timeout=30000")
            db.execute("BEGIN IMMEDIATE")
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    def _now(self):
        return _time(self.clock())

    @staticmethod
    def _account(db, owner):
        row = db.execute("SELECT * FROM accounts WHERE owner=?", (owner,)).fetchone()
        if row is None:
            raise AccountNotFound("Wallet account does not exist")
        return dict(row)

    @staticmethod
    def _task(db, owner, task_id):
        row = db.execute("SELECT * FROM tasks WHERE task_id=?", (task_id,)).fetchone()
        if row is None:
            raise TaskStateError("Task does not exist")
        if row["owner"] != owner:
            raise IdentityConflict("Task owner mismatch")
        return dict(row)

    @staticmethod
    def _entry(db, account, event_id, delta, kind, effective_at, now,
               *, task_id=None, provider=None, model=None, cost_status=None, note=None):
        balance = account["balance"] + delta
        if not -MAX_MONEY <= balance <= MAX_MONEY:
            raise InvalidArgument("Wallet integer balance overflow")
        db.execute("""INSERT INTO entries(event_id,owner,task_id,kind,delta,balance_after,
            provider,model,cost_status,note,effective_at,recorded_at)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
            (event_id, account["owner"], task_id, kind, delta, balance,
             provider, model, cost_status, note, _iso(effective_at), _iso(now)))
        account["balance"] = balance
        db.execute("UPDATE accounts SET balance=? WHERE owner=?", (balance, account["owner"]))
        return dict(db.execute("SELECT * FROM entries WHERE event_id=?", (event_id,)).fetchone())

    def _advance(self, db, account, now):
        if now < _time(account["last_seen"]):
            raise ClockRegression("Clock moved before this account's last transaction")
        anchor = _time(account["anchor"])
        while True:
            cycle = account["cycle_index"]
            due = (_month(anchor, cycle) + timedelta(days=15)
                   if account["phase"] == 1 else _month(anchor, cycle + 1))
            if now < due:
                break
            if account["phase"] == 2:
                cycle += 1
                self._entry(db, account, f"wallet:{account['owner']}:{cycle}:expiry",
                            -max(0, account["balance"]), "expiry", due, now)
                account.update(cycle_index=cycle, phase=1, released=INSTALLMENT_NANO_USD)
                installment = 1
            else:
                account.update(phase=2, released=MONTHLY_ALLOWANCE_NANO_USD)
                installment = 2
            self._entry(db, account, f"wallet:{account['owner']}:{cycle}:installment:{installment}",
                        INSTALLMENT_NANO_USD, "installment", due, now)
        account["last_seen"] = _iso(now)
        db.execute("UPDATE accounts SET cycle_index=?,phase=?,released=?,last_seen=? WHERE owner=?",
                   (account["cycle_index"], account["phase"], account["released"], account["last_seen"], account["owner"]))
        return account

    @staticmethod
    def _snapshot(db, account):
        anchor = _time(account["anchor"])
        start = _month(anchor, account["cycle_index"])
        end = _month(anchor, account["cycle_index"] + 1)
        next_release = start + timedelta(days=15) if account["phase"] == 1 else end
        active = db.execute("SELECT task_id,status,created_at FROM tasks WHERE owner=? AND status='active'",
                            (account["owner"],)).fetchone()
        pending = db.execute("SELECT cap FROM calls WHERE owner=? AND status='pending'", (account["owner"],)).fetchall()
        snap = {"schema": SCHEMA_VERSION, "owner": account["owner"], "currency": "USD",
                "money_unit": "nanoUSD", "policy": POLICY,
                "plan": {"price_brl": PLAN_PRICE_BRL, "checkout_implemented": False},
                "exempt": bool(account["exempt"]),
                "cycle": {"index": account["cycle_index"], "anchor": account["anchor"],
                          "starts_at": _iso(start), "ends_at": _iso(end), "timezone": "UTC"},
                "next_release": {"at": _iso(next_release), "amount_nano_usd": INSTALLMENT_NANO_USD,
                                 "amount_usd": _usd(INSTALLMENT_NANO_USD),
                                 "installment": 2 if account["phase"] == 1 else 1},
                "active_task": dict(active) if active else None,
                "pending_call_count": len(pending),
                "pending_bound_nano_usd": sum(row["cap"] for row in pending),
                "pending_bound_is_reservation": False,
                "can_begin_task": active is None and (bool(account["exempt"]) or account["balance"] > 0)}
        for name, value in (("balance", account["balance"]), ("available", max(0, account["balance"])),
                            ("debt", max(0, -account["balance"])), ("released", account["released"]),
                            ("monthly_allowance", MONTHLY_ALLOWANCE_NANO_USD)):
            snap[name + "_nano_usd"] = value
            snap[name + "_usd"] = _usd(value)
        return snap

    def ensure_account(self, owner, anchor=None, exempt=False):
        owner = _owner(owner)
        if type(exempt) is not bool:
            raise InvalidArgument("exempt must be a server-owned boolean")
        requested_anchor = _time(anchor) if anchor is not None else None
        with self._transaction() as db:
            now = self._now()
            old = db.execute("SELECT * FROM accounts WHERE owner=?", (owner,)).fetchone()
            if old:
                if bool(old["exempt"]) != exempt or (requested_anchor is not None and _iso(requested_anchor) != old["anchor"]):
                    raise IdentityConflict("Existing account anchor/exemption cannot be changed")
                account = dict(old)
            else:
                anchor_time = requested_anchor or now
                if anchor_time > now:
                    raise InvalidArgument("Account anchor cannot be in the future")
                db.execute("INSERT INTO accounts VALUES(?,?,?,?,?,?,?,?,?)",
                           (owner, _iso(anchor_time), int(exempt), 0, 0, INSTALLMENT_NANO_USD, 1, _iso(now), _iso(now)))
                account = self._account(db, owner)
                self._entry(db, account, f"wallet:{owner}:0:installment:1", INSTALLMENT_NANO_USD,
                            "installment", anchor_time, now)
            self._advance(db, account, now)
            return {"operation": "ensure_account", "created": old is None,
                    "wallet": self._snapshot(db, account)}

    def snapshot(self, owner):
        owner = _owner(owner)
        with self._transaction() as db:
            account = self._advance(db, self._account(db, owner), self._now())
            return self._snapshot(db, account)

    def _task_receipt(self, db, account, task, operation, *, idempotent, may_dispatch=False):
        return {"operation": operation, "owner": account["owner"], "task_id": task["task_id"],
                "status": task["status"], "admitted": bool(task["admitted"]),
                "may_dispatch": may_dispatch, "idempotent": idempotent,
                "created_at": task["created_at"], "finished_at": task["finished_at"],
                "wallet": self._snapshot(db, account)}

    def begin_task(self, owner, task_id):
        owner, task_id = _owner(owner), _identifier(task_id, "task_id")
        with self._transaction() as db:
            now = self._now()
            account = self._advance(db, self._account(db, owner), now)
            old = db.execute("SELECT * FROM tasks WHERE task_id=?", (task_id,)).fetchone()
            if old:
                task = self._task(db, owner, task_id)
                return self._task_receipt(db, account, task, "begin_task", idempotent=True)
            busy = db.execute("SELECT 1 FROM tasks WHERE owner=? AND status='active'", (owner,)).fetchone()
            status = ("rejected_active" if busy else "active" if account["exempt"] or account["balance"] > 0
                      else "rejected_balance")
            admitted = status == "active"
            db.execute("INSERT INTO tasks VALUES(?,?,?,?,?,?,?)",
                       (task_id, owner, int(admitted), status, _iso(now), None if admitted else _iso(now), None))
            return self._task_receipt(db, account, self._task(db, owner, task_id), "begin_task",
                                      idempotent=False, may_dispatch=admitted)

    @staticmethod
    def _matching_event(db, event_id, expected):
        old = db.execute("SELECT * FROM entries WHERE event_id=?", (event_id,)).fetchone()
        if old is None:
            return None
        if any(old[k] != value for k, value in expected.items()):
            raise IdentityConflict("Event identity/payload mismatch")
        return dict(old)

    def _cost_receipt(self, db, account, entry, operation, idempotent):
        sign = -1 if entry["kind"] == "cost" else 1
        return {"operation": operation, "idempotent": idempotent,
                "event": {**entry, "amount_nano_usd": sign * entry["delta"],
                          "amount_usd": _usd(sign * entry["delta"]),
                          "delta_nano_usd": entry["delta"], "balance_after_nano_usd": entry["balance_after"]},
                "wallet": self._snapshot(db, account)}

    def record_cost(self, owner, task_id, event_id, amount_usd, provider, model, status):
        owner, task_id = _owner(owner), _identifier(task_id, "task_id")
        event_id = _identifier(event_id, "event_id")
        amount = _money(amount_usd)
        provider, model = _label(provider, "provider"), _label(model, "model")
        if type(status) is not str or status not in COST_STATUSES:
            raise InvalidArgument("Cost status must be measured, estimated or estimated_components")
        if amount == 0 and status == "estimated_components":
            raise InvalidArgument("Estimated components require an explicit positive amount")
        if amount == 0 and status == "estimated":
            raise InvalidArgument("Zero estimated cost needs an explicit subscription-included call")
        expected = dict(owner=owner, task_id=task_id, kind="cost", delta=-amount,
                        provider=provider, model=model, cost_status=status, note=None)
        with self._transaction() as db:
            now = self._now()
            account = self._advance(db, self._account(db, owner), now)
            task = self._task(db, owner, task_id)
            if not task["admitted"]:
                raise TaskStateError("Costs require a previously admitted task")
            if db.execute("SELECT 1 FROM calls WHERE event_id=?", (event_id,)).fetchone():
                raise TaskStateError("Registered provider calls require settle_call with evidence")
            old = self._matching_event(db, event_id, expected)
            entry = old or self._entry(db, account, event_id, -amount, "cost", now, now,
                                      task_id=task_id, provider=provider, model=model, cost_status=status)
            return self._cost_receipt(db, account, entry, "record_cost", old is not None)

    def _finish(self, db, owner, task_id, status, now, evidence=None):
        if type(status) is not str or status not in TERMINAL_STATUSES:
            raise InvalidArgument("Invalid terminal task status")
        task = self._task(db, owner, task_id)
        if not task["admitted"]:
            raise TaskStateError("A refused task cannot be finished")
        if db.execute("SELECT 1 FROM calls WHERE owner=? AND task_id=? AND status='pending'",
                      (owner, task_id)).fetchone():
            raise TaskStateError("Pending provider calls require explicit settlement before finish")
        if task["status"] != "active":
            if task["status"] != status:
                raise TaskStateError("Terminal task status is immutable")
            return task, True
        db.execute("UPDATE tasks SET status=?,finished_at=?,evidence=? WHERE owner=? AND task_id=?",
                   (status, _iso(now), evidence, owner, task_id))
        return self._task(db, owner, task_id), False

    def finish_task(self, owner, task_id, status):
        owner, task_id = _owner(owner), _identifier(task_id, "task_id")
        with self._transaction() as db:
            now = self._now()
            account = self._advance(db, self._account(db, owner), now)
            task, repeated = self._finish(db, owner, task_id, status, now)
            return self._task_receipt(db, account, task, "finish_task", idempotent=repeated)

    def admin_credit(self, owner, event_id, amount, note):
        owner, event_id = _owner(owner), _identifier(event_id, "event_id")
        nano, note = _money(amount, positive=True), _text(note, "admin note", 500)
        expected = dict(owner=owner, task_id=None, kind="admin_credit", delta=nano,
                        provider=None, model=None, cost_status=None, note=note)
        with self._transaction() as db:
            now = self._now()
            account = self._advance(db, self._account(db, owner), now)
            if db.execute("SELECT 1 FROM calls WHERE event_id=?", (event_id,)).fetchone():
                raise IdentityConflict("Manual credit cannot take over a provider call ID")
            old = self._matching_event(db, event_id, expected)
            entry = old or self._entry(db, account, event_id, nano, "admin_credit", now, now, note=note)
            return self._cost_receipt(db, account, entry, "admin_credit", old is not None)

    @staticmethod
    def _call_receipt(call, *, idempotent, may_dispatch=False):
        return {"operation": "begin_call", "event_id": call["event_id"],
                "owner": call["owner"], "task_id": call["task_id"], "status": call["status"],
                "provider": call["provider"], "model": call["model"],
                "billing_basis": call["billing_basis"],
                "cap_nano_usd": call["cap"], "cap_usd": _usd(call["cap"]),
                "created_at": call["created_at"], "settled_at": call["settled_at"],
                "idempotent": idempotent, "may_dispatch": may_dispatch}

    def begin_call(self, owner, task_id, event_id, cap_usd, provider, model, *, billing_basis=API_CHARGE):
        owner, task_id = _owner(owner), _identifier(task_id, "task_id")
        event_id, cap = _identifier(event_id, "event_id"), _money(cap_usd)
        provider, model = _label(provider, "provider"), _label(model, "model")
        if not ((billing_basis == API_CHARGE and cap > 0) or
                (billing_basis == SUBSCRIPTION_INCLUDED and provider == "kimi" and cap == 0)):
            raise InvalidArgument("A positive cap or explicit Kimi subscription-included zero is required")
        expected = dict(owner=owner, task_id=task_id, cap=cap, provider=provider, model=model, billing_basis=billing_basis)
        with self._transaction() as db:
            now = self._now()
            account = self._advance(db, self._account(db, owner), now)
            task = self._task(db, owner, task_id)
            old = db.execute("SELECT * FROM calls WHERE event_id=?", (event_id,)).fetchone()
            if old:
                if any(old[k] != value for k, value in expected.items()):
                    raise IdentityConflict("Provider call identity/payload mismatch")
                receipt = self._call_receipt(old, idempotent=True)
            else:
                if task["status"] != "active" or not task["admitted"]:
                    raise TaskStateError("New provider calls require an active admitted task")
                if db.execute("SELECT 1 FROM entries WHERE event_id=?", (event_id,)).fetchone():
                    raise IdentityConflict("Provider call ID already used by another event")
                db.execute("""INSERT INTO calls(event_id,owner,task_id,cap,provider,model,billing_basis,status,created_at)
                              VALUES(?,?,?,?,?,?,?,'pending',?)""",
                           (event_id, owner, task_id, cap, provider, model, billing_basis, _iso(now)))
                call = db.execute("SELECT * FROM calls WHERE event_id=?", (event_id,)).fetchone()
                receipt = self._call_receipt(call, idempotent=False, may_dispatch=True)
            return {**receipt, "wallet": self._snapshot(db, account)}

    def settle_call(self, owner, task_id, event_id, amount_usd=None, status="estimated", *, evidence=None):
        owner, task_id = _owner(owner), _identifier(task_id, "task_id")
        event_id = _identifier(event_id, "event_id")
        if type(status) is not str or status not in COST_STATUSES:
            raise InvalidArgument("Settlement must be measured, estimated or estimated_components")
        evidence = (_text(evidence, "provider evidence reference", 200) if evidence is not None
                    else "caller_attested_" + status)
        if status != "estimated" and amount_usd is None:
            raise InvalidArgument("Measured/components settlement requires an explicit amount")
        requested = (_money(amount_usd, positive=status == "estimated_components")
                     if amount_usd is not None else None)
        with self._transaction() as db:
            now = self._now()
            account = self._advance(db, self._account(db, owner), now)
            self._task(db, owner, task_id)
            call = db.execute("SELECT * FROM calls WHERE event_id=?", (event_id,)).fetchone()
            if call is None:
                raise TaskStateError("Provider call was not registered")
            if call["owner"] != owner or call["task_id"] != task_id:
                raise IdentityConflict("Provider call owner/task mismatch")
            amount = call["cap"] if status == "estimated" else requested
            if status == "estimated" and requested is not None and requested != call["cap"]:
                raise InvalidArgument("Unknown usage must settle the full registered cap")
            if call["billing_basis"] == SUBSCRIPTION_INCLUDED and amount != 0:
                raise InvalidArgument("Subscription-included call has no incremental API charge")
            expected = dict(owner=owner, task_id=task_id, kind="cost", delta=-amount,
                            provider=call["provider"], model=call["model"], cost_status=status, note=None)
            old = self._matching_event(db, event_id, expected)
            if call["status"] == "settled":
                if old is None or call["evidence"] != evidence:
                    raise IdentityConflict("Settled call payload/evidence mismatch")
            else:
                if old is not None:
                    raise IdentityConflict("Pending call already has a debit")
                old = self._entry(db, account, event_id, -amount, "cost", now, now,
                                  task_id=task_id, provider=call["provider"], model=call["model"], cost_status=status)
                db.execute("UPDATE calls SET status='settled',settled_at=?,evidence=? WHERE event_id=?",
                           (_iso(now), evidence, event_id))
            return {**self._cost_receipt(db, account, old, "settle_call", call["status"] == "settled"),
                    "evidence_reference": evidence, "proof_verified_by_wallet": False,
                    "may_dispatch": False}

    def pending_calls(self, owner, *, after=0, limit=100):
        owner = _owner(owner)
        if type(after) is not int or after < 0 or type(limit) is not int or not 1 <= limit <= 1000:
            raise InvalidArgument("Invalid pending-call page")
        with self._transaction() as db:
            self._account(db, owner)
            rows = db.execute("SELECT * FROM calls WHERE owner=? AND status='pending' AND seq>? ORDER BY seq LIMIT ?",
                              (owner, after, limit + 1)).fetchall()
            page = rows[:limit]
            return {"operation": "pending_calls", "owner": owner, "may_dispatch": False,
                    "calls": [{**self._call_receipt(row, idempotent=True), "sequence": row["seq"]} for row in page],
                    "next_after": page[-1]["seq"] if len(rows) > limit else None,
                    "recovery": "Inspect provider evidence and settle explicitly; never replay uncertain calls."}

    def reconcile(self, owner, proven_terminal_tasks, *, evidence):
        owner = _owner(owner)
        evidence = _text(evidence, "terminal evidence reference", 200)
        if type(proven_terminal_tasks) is not dict or not 1 <= len(proven_terminal_tasks) <= 1000:
            raise InvalidArgument("Explicit nonempty mapping of at most 1000 proven terminal tasks required")
        for task_id, status in proven_terminal_tasks.items():
            _identifier(task_id, "task_id")
            if type(status) is not str or status not in TERMINAL_STATUSES:
                raise InvalidArgument("Invalid terminal task status")
        with self._transaction() as db:
            now = self._now()
            account = self._advance(db, self._account(db, owner), now)
            receipts = []
            for task_id, status in proven_terminal_tasks.items():
                task, repeated = self._finish(db, owner, task_id, status, now, evidence)
                receipts.append({"task_id": task_id, "status": task["status"], "idempotent": repeated})
            return {"operation": "reconcile", "owner": owner, "evidence_reference": evidence,
                    "proof_verified_by_wallet": False, "tasks": receipts, "may_dispatch": False,
                    "wallet": self._snapshot(db, account)}


__all__ = ["Wallet", "WalletError", "InvalidArgument", "AccountNotFound", "IdentityConflict",
           "TaskStateError", "ClockRegression", "NANO_USD", "INSTALLMENT_NANO_USD",
           "MONTHLY_ALLOWANCE_NANO_USD", "PLAN_PRICE_BRL", "POLICY", "TERMINAL_STATUSES",
           "API_CHARGE", "SUBSCRIPTION_INCLUDED"]
