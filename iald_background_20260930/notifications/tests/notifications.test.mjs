import test from 'node:test';
import assert from 'node:assert/strict';
import { createNativeNotifications, parseNotification, nativePlugins } from '../client/native-notifications.mjs';
import { connectNotifications } from '../client/registration.mjs';

const bindingId = '00000000-0000-4000-8000-000000000001';
const jobId = '00000000-0000-4000-8000-000000000002';
const installationId = '00000000-0000-4000-8000-000000000003';
const payload = (extra = {}) => ({ schema_version: '1', event: 'iald.response_ready',
  event_id: 'event-1', job_id: jobId, binding_id: bindingId, ...extra });
const tap = (extra = {}) => ({ actionId: 'tap', notification: { data: payload(extra) } });
const deferred = () => { let resolve; const promise = new Promise(r => { resolve = r; }); return { promise, resolve }; };

function fixture(overrides = {}) {
  const listeners = new Map(), calls = [], states = [];
  const push = {
    async addListener(name, fn) { listeners.set(name, fn); return { async remove() { listeners.delete(name); } }; },
    async checkPermissions() { return { receive: 'granted' }; },
    async requestPermissions() { calls.push('prompt'); return { receive: 'granted' }; },
    async register() { calls.push('register'); },
    async unregister() { calls.push('unregister'); },
    async removeAllDeliveredNotifications() { calls.push('clear'); },
  };
  const api = {
    async saveToken(data) { calls.push(['save', data.token]); },
    async revoke() { calls.push('revoke'); },
    async getJob() { return { id: jobId, state: 'completed', conversationId: 'own-conversation' }; },
    async reconcile() { calls.push('reconcile'); },
  };
  const app = { addListener: push.addListener };
  Object.assign(push, overrides.push); Object.assign(api, overrides.api);
  const controller = createNativeNotifications({ push, app, api, platform: 'ios', bindingId,
    openJob: async data => calls.push(['open', data.jobId, data.conversationId]),
    onStatus: data => states.push(data), timeoutMs: overrides.timeoutMs ?? 1000 });
  return { controller, push, app, api, calls, states,
    emit: (name, value) => listeners.get(name)?.(value), listeners };
}

test('start does not request permission, enable requires a gesture call', async () => {
  const f = fixture({ push: { async checkPermissions() { return { receive: 'prompt' }; } } });
  await f.controller.start(); assert.equal(f.controller.getState().state, 'permission_required');
  assert.ok(!f.calls.includes('prompt')); assert.ok(!f.calls.includes('register'));
  await f.controller.enable(); assert.deepEqual(f.calls, ['reconcile', 'prompt', 'register']);
  await f.controller.stop();
});

test('denied permission still reconciles durable jobs and never registers', async () => {
  const f = fixture({ push: { async checkPermissions() { return { receive: 'denied' }; } } });
  await f.controller.start(); await f.controller.enable();
  assert.equal(f.controller.getState().state, 'permission_denied');
  assert.deepEqual(f.calls, ['reconcile']); await f.controller.stop();
});

test('token writes are serialized, deduplicated and rotated', async () => {
  const f = fixture(); await f.controller.start();
  for (const token of ['a'.repeat(64), 'a'.repeat(64), 'b'.repeat(64)]) f.emit('registration', { value: token });
  await f.controller.settled();
  assert.deepEqual(f.calls.filter(x => Array.isArray(x)), [['save', 'a'.repeat(64)], ['save', 'b'.repeat(64)]]);
  assert.equal(f.controller.getState().state, 'registered'); await f.controller.stop();
});

test('invalid token and provider exceptions never reach diagnostics', async () => {
  const f = fixture({ api: { async saveToken() { throw new Error('SECRET_BODY'); } } });
  await f.controller.start(); f.emit('registration', { value: 'https://evil.example/key' });
  assert.equal(f.controller.getState().state, 'invalid_token');
  f.emit('registrationError', { error: 'SECRET_BODY' });
  f.emit('registration', { value: 'a'.repeat(64) }); await f.controller.settled();
  assert.equal(f.controller.getState().state, 'token_sync_failed');
  assert.ok(!JSON.stringify(f.states).includes('SECRET')); await f.controller.stop();
});

test('tap opens only conversation from authenticated GET and deduplicates', async () => {
  const f = fixture(); await f.controller.start();
  await f.emit('pushNotificationActionPerformed', tap({ username: 'someone-else', conversation_id: 'evil', url: 'https://evil' }));
  await f.emit('pushNotificationActionPerformed', tap()); await f.controller.settled();
  assert.deepEqual(f.calls.filter(x => Array.isArray(x)), [['open', jobId, 'own-conversation']]);
  await f.controller.stop();
});

test('foreign binding, bad IDs, dismissed and non-completed jobs cannot open', async () => {
  const f = fixture({ api: { async getJob() { return { id: jobId, state: 'running', conversationId: 'own' }; } } });
  await f.controller.start();
  await f.emit('pushNotificationActionPerformed', tap({ binding_id: 'foreign' }));
  await f.emit('pushNotificationActionPerformed', tap({ job_id: '../secret' }));
  await f.emit('pushNotificationActionPerformed', { ...tap(), actionId: 'dismiss' });
  await f.emit('pushNotificationActionPerformed', tap());
  assert.ok(!f.calls.some(Array.isArray)); await f.controller.stop();
});

test('received event only reconciles; foreground resumes without another prompt', async () => {
  const f = fixture(); await f.controller.start();
  await f.emit('pushNotificationReceived', { data: payload() });
  await f.emit('appStateChange', { isActive: false });
  await f.emit('appStateChange', { isActive: true }); await f.controller.settled();
  assert.equal(f.calls.filter(x => x === 'reconcile').length, 3);
  assert.ok(!f.calls.includes('prompt')); assert.ok(!f.calls.some(Array.isArray)); await f.controller.stop();
});

test('stop revokes immediately and late authenticated GET cannot navigate', async () => {
  const gate = deferred(); const f = fixture({ api: { getJob: () => gate.promise } });
  await f.controller.start(); const click = f.emit('pushNotificationActionPerformed', tap());
  await Promise.resolve(); const stop = f.controller.stop();
  gate.resolve({ id: jobId, state: 'completed', conversationId: 'own' });
  await click; await stop;
  assert.ok(!f.calls.some(Array.isArray)); assert.ok(f.calls.includes('revoke'));
  assert.equal(f.listeners.size, 0); assert.equal(f.controller.getState().state, 'stopped');
});

test('logout network failure remains visible and stop is idempotent', async () => {
  const f = fixture({ api: { async revoke() { throw new Error('SECRET_BODY'); } } });
  await f.controller.start(); const a = f.controller.stop(), b = f.controller.stop();
  assert.equal(a, b); assert.equal((await a).state, 'revocation_pending');
  assert.ok(!JSON.stringify(f.states).includes('SECRET'));
});

test('late listener handles are removed after initialization races teardown', async () => {
  const gate = deferred(); let removed = 0;
  const f = fixture({ push: { addListener: () => gate.promise } });
  const start = f.controller.start(); await Promise.resolve();
  const stop = f.controller.stop(); gate.resolve({ async remove() { removed++; } });
  await start; await stop; assert.equal(removed, 1);
});

test('registration synchronization has a deadline', async () => {
  const f = fixture({ timeoutMs: 5, api: { saveToken: () => new Promise(() => {}) } });
  await f.controller.start(); f.emit('registration', { value: 'a'.repeat(64) });
  await f.controller.settled(); assert.equal(f.controller.getState().state, 'token_sync_failed');
  await f.controller.stop();
});

test('native adapter fails visibly in ordinary browser', () => {
  assert.throws(() => nativePlugins({ isNativePlatform: () => false }), /native_push_unavailable/);
  assert.equal(parseNotification(payload({ job_id: {} }), bindingId), null);
});

test('registration plumbing uses ChatJobs status and conversation, no payload username', async () => {
  const f = fixture(), requests = [], opened = [];
  const requestJSON = async (path, options) => {
    requests.push({ path, ...options });
    if (path === '/api/native-push/bindings') return { id: bindingId, revoked: false, platform: 'ios' };
    if (path === '/api/chat-jobs') return { jobs: [] };
    if (path === '/api/chat-jobs/' + jobId) return { id: jobId, status: 'completed', conversation_id: 'server-conversation' };
    return {};
  };
  const controller = await connectNotifications({ requestJSON, installationId, consent: true, nativeReady: true,
    plugins: { push: f.push, app: f.app, platform: 'ios' }, onJobs() {}, openJob: data => opened.push(data) });
  await f.emit('pushNotificationActionPerformed', tap()); await controller.settled();
  assert.equal(opened[0].conversationId, 'server-conversation');
  assert.deepEqual(requests[0].body, { installation_id: installationId, platform: 'ios', consent: true });
  await controller.stop();
});

test('plumbing refuses implicit opt in and masks request errors', async () => {
  const f = fixture(); const options = { installationId, nativeReady: true, plugins: { push: f.push, app: f.app, platform: 'ios' },
    onJobs() {}, openJob() {}, requestJSON: async () => { throw new Error('SECRET_BODY'); } };
  await assert.rejects(connectNotifications({ ...options, consent: false }), /notification_opt_in_required/);
  await assert.rejects(connectNotifications({ ...options, consent: true }), /^Error: notification_binding_failed$/);
});

test('disabled rollout does not load plugins, request permissions or call backend', async () => {
  const controller = await connectNotifications({ installationId, consent: true, onJobs() {},
    requestJSON() { throw new Error('must not call'); }, openJob() {} });
  assert.equal(controller.getState().state, 'configuration_disabled');
});

test('Android missing Firebase/readiness stays disabled before getToken', async () => {
  for (const readiness of [undefined, { getStatus: async () => ({ ready: false }) },
    { getStatus: async () => { throw new Error('SECRET'); } }]) {
    const controller = await connectNotifications({ installationId, consent: true, nativeReady: true,
      plugins: { platform: 'android', readiness }, onJobs() {}, openJob() {},
      requestJSON() { throw new Error('must not call'); } });
    assert.equal(controller.getState().state, 'configuration_disabled');
  }
});
