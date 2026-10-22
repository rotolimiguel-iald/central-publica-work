import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
const source = readFileSync(new URL('./notification_settings.js', import.meta.url), 'utf8');
const { createNotificationSettings } = await import('data:text/javascript;base64,' + Buffer.from(source).toString('base64'));
const A = 'a'.repeat(64), B = 'b'.repeat(64);
const tick = () => new Promise(setImmediate);

function fixture({ configured = false, connect } = {}) {
  const values = new Map(), calls = [], states = [], connections = [];
  let account = A, token = 'synthetic-a', revokeFails = false;
  const storage = { getItem: k => values.get(k) ?? null, setItem: (k, v) => values.set(k, v) };
  const manager = createNotificationSettings({ storage,
    identity: () => ({ account, token }), platform: () => 'ios',
    randomUUID: () => '00000000-0000-4000-8000-000000000001',
    requestFor: captured => async (path, options) => {
      calls.push({ path, options, captured });
      if (path.endsWith('revoke-session')) {
        if (revokeFails) throw new Error('PRIVATE_BODY');
        return { revoked: true };
      }
      return { ios: configured, android: false };
    },
    connect: connect || (async options => {
      connections.push(options);
      return { getState: () => ({ state: 'registered' }), enable: async () => calls.push('prompt'),
        stop: async () => { calls.push('stop'); return { state: 'stopped' }; } };
    }),
    openJob: data => calls.push(['open', data.jobId]), onJobs: () => calls.push('jobs'),
    onChange: state => states.push(state),
  });
  return { manager, values, calls, states, connections,
    change: (a, t) => { account = a; token = t; }, failRevoke: () => { revokeFails = true; },
    restoreRevoke: () => { revokeFails = false; } };
}

test('configuration false stays disabled without native connection', async () => {
  const f = fixture(); await f.manager.refresh();
  assert.equal(f.manager.getState().configured, false); assert.equal(f.connections.length, 0);
});
test('new account is opted out even when configured; only gesture enables', async () => {
  const f = fixture({ configured: true }); await f.manager.refresh();
  assert.equal(f.manager.getState().state, 'off'); assert.equal(f.connections.length, 0);
  await f.manager.toggle(true); assert.equal(f.connections.length, 1); assert.equal(f.connections[0].prompt, true);
  assert.ok([...f.values.keys()].every(k => !k.includes('synthetic-a')));
});
test('restored explicit preference never prompts and foreign account gets no consent', async () => {
  const f = fixture({ configured: true }); f.values.set('iald_native_push_opt_in_v1:' + A, '1');
  await f.manager.refresh(); assert.equal(f.connections[0].prompt, false);
  f.change(B, 'synthetic-b'); await f.manager.refresh();
  assert.equal(f.manager.getState().state, 'off'); assert.equal(f.connections.length, 1);
});
test('turning off revokes session without depending on readiness probe', async () => {
  const f = fixture({ configured: true }); await f.manager.toggle(true);
  const before = f.calls.length; await f.manager.toggle(false);
  assert.deepEqual(f.calls.slice(before).map(x => typeof x === 'string' ? x : x.path), ['stop', '/api/native-push/revoke-session']);
  assert.equal(f.manager.getState().wanted, false);
});
test('logout retains captured bearer and explicit retry can settle revocation', async () => {
  const f = fixture({ configured: true }); await f.manager.toggle(true); f.failRevoke();
  assert.equal((await f.manager.disconnect()).state, 'revocation_pending');
  f.restoreRevoke(); assert.equal((await f.manager.disconnect()).state, 'stopped');
  assert.equal(f.calls.filter(x => x.path?.endsWith('revoke-session')).at(-1).captured, 'synthetic-a');
  assert.ok(!JSON.stringify(f.states).includes('synthetic-a'));
});
test('late connect and tap after account switch cannot navigate', async () => {
  let finish, options, stopped = 0;
  const f = fixture({ configured: true, connect: async value => {
    options = value; await new Promise(r => { finish = r; });
    return { getState: () => ({ state: 'registered' }), stop: async () => { stopped++; return { state: 'stopped' }; } };
  } });
  const enabling = f.manager.toggle(true); await tick();
  f.change(B, 'synthetic-b'); const closing = f.manager.disconnect(); finish();
  await enabling; await closing;
  await options.openJob({ jobId: 'job', signal: new AbortController().signal });
  assert.equal(stopped, 1); assert.ok(!f.calls.some(Array.isArray));
});
test('bound HTTP adapter revokes with old bearer after token clearing', async () => {
  let token = 'new-token'; const calls = [];
  const context = vm.createContext({ AbortController, setTimeout, clearTimeout,
    tokenApp: () => token, BASE: 'https://example.invalid',
    fetch: async (url, options) => { calls.push({ url, options }); return { ok: true, json: async () => ({ revoked: true }) }; } });
  const code = readFileSync(new URL('./native_notifications_integration.js', import.meta.url), 'utf8');
  vm.runInContext(code + '\nglobalThis.bind = boundNativePushRequest;', context);
  const api = context.bind('old-token');
  await api('/api/native-push/revoke-session', { method: 'POST', body: {} });
  assert.equal(calls[0].options.headers.Authorization, 'Bearer old-token');
  await assert.rejects(api('/api/native-push/status', { method: 'GET' }), /notification_request_failed/);
  assert.equal(calls.length, 1);
});

test('logout waits for revocation and keeps login on uncertain revocation', async () => {
  const notices = []; let finish;
  const context = vm.createContext({ avisar: message => notices.push(message) });
  const code = readFileSync(new URL('./native_notifications_integration.js', import.meta.url), 'utf8');
  vm.runInContext(code + '\nglobalThis.logout = prepareNativePushLogout; globalThis.setManager = value => { nativeNotificationSettings = value; };', context);
  context.setManager({ disconnect: () => new Promise(resolve => { finish = resolve; }) });
  let settled = false;
  const pending = context.logout().then(value => { settled = true; return value; });
  await tick(); assert.equal(settled, false);
  finish({ state: 'revocation_pending' }); assert.equal(await pending, false);
  assert.equal(notices.length, 1);
  const retry = context.logout(); await tick(); finish({ state: 'stopped' });
  assert.equal(await retry, true);
});

test('HTTP 410 preserves pending until safe notice is saved, then removes without ACK or resend', async () => {
  const code = readFileSync(new URL('./chat_jobs.js', import.meta.url), 'utf8');
  const { createDurableChatJobs } = await import('data:text/javascript;base64,' + Buffer.from(code).toString('base64'));
  const values = new Map(), calls = [];
  const id = '00000000-0000-4000-8000-000000000001';
  const jobs = createDurableChatJobs({
    storage: { getItem: k => values.get(k) ?? null, setItem: (k, v) => values.set(k, v) },
    randomUUID: () => id,
    request: async (path, options) => {
      calls.push({ path, method: options.method || 'GET' });
      if (path.endsWith('/session')) return { ok: true, status: 200, json: async () => ({ account: A }) };
      if (path === '/api/chat-jobs') return { ok: true, status: 202, json: async () => ({ id, conversation_id: 'conv', status: 'running' }) };
      return { ok: false, status: 410, json: async () => { throw Error('PRIVATE_BODY_MUST_NOT_BE_READ'); } };
    }
  });
  jobs.setOwner(A); const record = await jobs.begin({ iald_conv: 'conv' });
  await assert.rejects(async () => { for await (const ignored of jobs.stream(record)) {} }, e => e.terminal && e.status === 'expired');
  assert.equal(jobs.pending()[0].status, 'expired');
  await assert.rejects(jobs.delivered(record, async () => { throw Error('storage unavailable'); }));
  assert.equal(jobs.pending().length, 1);
  const count = calls.length; let saved = false;
  await jobs.delivered(record, async () => { saved = true; });
  assert.equal(saved, true); assert.equal(jobs.pending().length, 0); assert.equal(calls.length, count);
});
