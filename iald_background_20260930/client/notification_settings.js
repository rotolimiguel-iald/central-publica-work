// Dependency-injected settings lifecycle; tokens stay in memory only.
export function createNotificationSettings({ connect, storage, identity, platform,
  requestFor, openJob, onJobs, onChange, randomUUID }) {
  let epoch = 0, controller = null, tail = Promise.resolve(), lastScope = '';
  let revokedScope = '';
  let view = { configured: false, wanted: false, busy: false, state: 'signed_out' };
  const key = account => 'iald_native_push_opt_in_v1:' + account;
  const publish = change => {
    view = { ...view, ...change };
    try { onChange({ ...view }); } catch { /* UI errors cannot expose request data. */ }
    return { ...view };
  };
  const valid = value => value && /^[a-f0-9]{64}$/.test(value.account) &&
    typeof value.token === 'string' && value.token.length > 0;
  const current = (snapshot, version) => {
    const now = identity();
    return version === epoch && valid(now) && now.account === snapshot.account && now.token === snapshot.token;
  };
  const queue = fn => {
    tail = tail.then(fn, fn).catch(() => publish({ busy: false, state: 'unavailable' }));
    return tail;
  };
  const stop = async () => {
    const previous = controller; controller = null;
    return previous ? previous.stop() : { state: 'stopped' };
  };
  const revokeSession = async snapshot => {
    if (!valid(snapshot)) return { state: 'stopped' };
    const scope = snapshot.account + ':' + snapshot.token;
    if (scope === revokedScope) return { state: 'stopped' };
    try {
      const result = await requestFor(snapshot.token)('/api/native-push/revoke-session', { method: 'POST', body: {} });
      if (result?.revoked !== true) throw new Error();
      revokedScope = scope;
      return { state: 'stopped' };
    } catch { return { state: 'revocation_pending' }; }
  };
  function installation() {
    const idKey = 'iald_native_push_installation_v1';
    let value = storage.getItem(idKey);
    if (value == null) { value = randomUUID(); storage.setItem(idKey, value); }
    if (!/^[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}$/.test(value) || storage.getItem(idKey) !== value)
      throw new Error('notification_storage_failed');
    return value;
  }
  async function run(force, prompt) {
    const snapshot = identity(), version = epoch;
    if (!valid(snapshot)) { await stop(); lastScope = ''; return publish({ configured: false, wanted: false, busy: false, state: 'signed_out' }); }
    const scope = snapshot.account + ':' + snapshot.token; // Never persisted or returned.
    if (!force && scope === lastScope) return { ...view };
    if (lastScope && scope !== lastScope) await stop();
    if (!current(snapshot, version)) return { ...view };
    lastScope = scope;
    const wanted = storage.getItem(key(snapshot.account)) === '1';
    publish({ busy: true, wanted });
    const requestJSON = requestFor(snapshot.token);
    const readiness = await requestJSON('/api/native-push/status', { method: 'GET' });
    if (!current(snapshot, version)) return { ...view };
    const configured = readiness?.[platform()] === true;
    if (!configured || !wanted) {
      const result = await stop();
      if (!current(snapshot, version)) return { ...view };
      return publish({ configured, wanted, busy: false, state: result.state === 'revocation_pending'
        ? result.state : configured ? 'off' : 'configuration_disabled' });
    }
    publish({ configured: true, busy: true });
    if (!controller) {
      revokedScope = '';
      const next = await connect({ requestJSON, installationId: installation(), consent: true,
        nativeReady: true, prompt,
        openJob: async data => { if (current(snapshot, version) && !data.signal?.aborted) await openJob(data, snapshot.account); },
        onJobs: async (jobs, options) => { if (current(snapshot, version) && !options.signal?.aborted) await onJobs(jobs); },
        onStatus: result => { if (current(snapshot, version)) publish({ state: result.state }); },
      });
      if (!current(snapshot, version)) { await next.stop(); return { ...view }; }
      controller = next;
    } else if (prompt) await controller.enable();
    const result = controller.getState();
    if (result.state === 'configuration_disabled') { controller = null; return publish({ configured: false, busy: false, state: result.state }); }
    return publish({ busy: false, state: result.state });
  }
  return {
    refresh(force = false) { return queue(() => run(force, false)); },
    toggle(enabled) {
      const snapshot = identity();
      if (!valid(snapshot) || typeof enabled !== 'boolean') return Promise.resolve({ ...view });
      // Preference is per authenticated opaque account. New accounts are always opted out.
      try {
        storage.setItem(key(snapshot.account), enabled ? '1' : '0');
        if (storage.getItem(key(snapshot.account)) !== (enabled ? '1' : '0')) throw new Error();
      } catch { return Promise.resolve(publish({ state: 'storage_unavailable', busy: false })); }
      if (!enabled) {
        epoch++; // Invalidate in-flight taps immediately, before queued teardown.
        const closing = stop();
        publish({ wanted: false, busy: true });
        return queue(async () => {
          await closing;
          const result = await revokeSession(snapshot);
          return publish({ wanted: false, busy: false, state: result.state === 'stopped' ? 'off' : result.state });
        });
      }
      return queue(() => run(true, enabled));
    },
    disconnect() {
      const snapshot = identity();
      epoch++; lastScope = '';
      publish({ configured: false, wanted: false, busy: false, state: 'signed_out' });
      // Keep the captured request adapter so DELETE uses the old bearer during logout.
      const closing = stop();
      return queue(async () => { await closing; return revokeSession(snapshot); });
    },
    getState() { return { ...view }; },
    settled() { return tail; },
  };
}
