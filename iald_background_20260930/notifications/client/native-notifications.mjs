/** Native-only notifications. No fetch, storage, provider credentials or job execution.
 * Dependencies must be bound to ONE authenticated backend binding; see CONTRACT.md.
 */
const ID = /^[A-Za-z0-9_-]{1,128}$/;
export const CHANNEL_ID = 'iald_responses_v1';
export const EVENT = 'iald.response_ready';

export function parseNotification(data, bindingId) {
  if (!data || typeof data !== 'object' || Array.isArray(data) ||
      data.schema_version !== '1' || data.event !== EVENT ||
      data.binding_id !== bindingId || !ID.test(data.event_id ?? '') ||
      !ID.test(data.job_id ?? '') || typeof data.event_id !== 'string' ||
      typeof data.job_id !== 'string') return null;
  // Deliberately discard URLs, titles, text, owner IDs and every other field.
  return { eventId: data.event_id, jobId: data.job_id };
}

export function nativePlugins(capacitor = globalThis.Capacitor) {
  if (!capacitor?.isNativePlatform?.() ||
      !['ios', 'android'].includes(capacitor.getPlatform()) ||
      !capacitor.isPluginAvailable('PushNotifications') ||
      !capacitor.isPluginAvailable('App')) throw new Error('native_push_unavailable');
  return {
    platform: capacitor.getPlatform(),
    push: capacitor.registerPlugin('PushNotifications'),
    app: capacitor.registerPlugin('App'),
    readiness: capacitor.isPluginAvailable('IaldPushReadiness')
      ? capacitor.registerPlugin('IaldPushReadiness') : undefined,
  };
}

export function createNativeNotifications({ push, app, platform, bindingId,
  api, openJob, onStatus = () => {}, timeoutMs = 15000 }) {
  if (!['ios', 'android'].includes(platform) || typeof bindingId !== 'string' ||
      !ID.test(bindingId) || !Number.isInteger(timeoutMs) || timeoutMs < 1 ||
      timeoutMs > 60000 || !push?.addListener || !app?.addListener ||
      !['saveToken', 'revoke', 'getJob', 'reconcile'].every(k => typeof api?.[k] === 'function') ||
      typeof openJob !== 'function') throw new Error('invalid_notification_configuration');

  let active = false, started = false, state = 'idle', stopPromise;
  let operation = Promise.resolve(), writes = Promise.resolve();
  let lastSavedToken = null;
  const abort = new AbortController(), handles = [], seen = new Set(), opening = new Set();
  const tasks = new Set();
  const status = next => {
    state = next;
    try { onStatus({ state: next }); } catch { /* UI cannot leak or break cleanup. */ }
    return { state: next };
  };
  const bounded = work => new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('notification_timeout')), timeoutMs);
    Promise.resolve().then(work).then(resolve, reject).finally(() => clearTimeout(timer));
  });
  const guarded = (fn, failure) => {
    const task = Promise.resolve().then(fn).catch(() => {
      if (active) status(failure);
    });
    tasks.add(task);
    task.finally(() => tasks.delete(task));
    return task;
  };
  const serial = fn => {
    operation = operation.then(fn, fn).catch(() => active ? status('operation_failed') : { state });
    return operation;
  };
  const options = () => ({ bindingId, signal: abort.signal });

  function saveToken(value) {
    const valid = typeof value === 'string' && (platform === 'ios'
      ? /^[A-Fa-f0-9]{32,512}$/.test(value) && value.length % 2 === 0
      : /^[A-Za-z0-9_:.-]{16,4096}$/.test(value));
    if (!active) return;
    if (!valid) { status('invalid_token'); return; }
    writes = writes.then(async () => {
      if (!active || value === lastSavedToken) return;
      await bounded(() => api.saveToken({ ...options(), token: value,
        provider: platform === 'ios' ? 'apns' : 'fcm' }));
      if (active) { lastSavedToken = value; status('registered'); }
    }).catch(() => { if (active) status('token_sync_failed'); });
  }

  async function openNotification(action) {
    if (!active || action?.actionId !== 'tap') return;
    const event = parseNotification(action.notification?.data, bindingId);
    if (!event || seen.has(event.eventId) || opening.has(event.eventId)) return;
    if (opening.size >= 16) { status('notification_busy'); return; }
    opening.add(event.eventId);
    try {
      const job = await bounded(() => api.getJob({ ...options(), jobId: event.jobId }));
      // The authenticated endpoint enforces ownership. Payload never authorizes access.
      if (!active) return;
      if (!job || job.id !== event.jobId || job.state !== 'completed' ||
          typeof job.conversationId !== 'string' || !/^[A-Za-z0-9_-]{1,64}$/.test(job.conversationId)) {
        status('response_unavailable'); return;
      }
      await bounded(() => openJob({ jobId: event.jobId, conversationId: job.conversationId,
        signal: abort.signal }));
      if (!active) return;
      seen.add(event.eventId);
      if (seen.size > 128) seen.delete(seen.values().next().value);
      status('response_opened');
    } finally { opening.delete(event.eventId); }
  }

  async function add(plugin, name, callback) {
    // If teardown races a delayed listener creation, remove that late handle too.
    const pending = Promise.resolve().then(() => plugin.addListener(name, callback));
    pending.then(handle => {
      if (active) handles.push(handle);
      else Promise.resolve().then(() => handle.remove()).catch(() => {});
    }, () => {});
    await bounded(() => pending);
  }

  async function register(prompt) {
    if (!active) return { state };
    let permission = await bounded(() => push.checkPermissions());
    if (!active) return { state };
    if (prompt && ['prompt', 'prompt-with-rationale'].includes(permission?.receive)) {
      permission = await bounded(() => push.requestPermissions());
    }
    if (!active) return { state };
    if (permission?.receive !== 'granted') return status(
      permission?.receive === 'denied' ? 'permission_denied' : 'permission_required');
    status('awaiting_token');
    await bounded(() => push.register());
    return { state };
  }

  async function resume() {
    if (!active) return;
    // Always reconcile durable jobs, including when push is denied or lost.
    await bounded(() => api.reconcile(options()));
    if (active) await register(false);
  }

  async function cleanup() {
    const results = await Promise.allSettled(handles.splice(0).map(h => bounded(() => h.remove())));
    return results.every(r => r.status === 'fulfilled');
  }

  return {
    start() {
      if (started || stopPromise) return operation.then(() => ({ state }));
      started = true; active = true;
      return serial(async () => {
        try {
          // Capacitor retains a cold-start tap until this listener is attached.
          await add(push, 'pushNotificationActionPerformed', action =>
            guarded(() => openNotification(action), 'response_open_failed'));
          if (!active) return { state };
          await add(push, 'registration', token => saveToken(token?.value));
          await add(push, 'registrationError', () => { if (active) status('registration_failed'); });
          await add(push, 'pushNotificationReceived', notification => {
            if (active && parseNotification(notification?.data, bindingId))
              guarded(() => bounded(() => api.reconcile(options())), 'reconcile_failed');
          });
          await add(app, 'appStateChange', change => {
            if (active && change?.isActive === true)
              guarded(() => serial(resume), 'resume_failed');
          });
          if (active) await resume();
          return { state };
        } catch {
          if (active) status('startup_failed');
          return { state };
        }
      });
    },
    enable() {
      // Call ONLY from the authenticated user's explicit enable-notifications gesture.
      return serial(async () => {
        if (!active || !started) return { state };
        try { return await register(true); }
        catch { return active ? status('registration_failed') : { state }; }
      });
    },
    stop() {
      if (stopPromise) return stopPromise;
      active = false; abort.abort(); lastSavedToken = null;
      // Revoke immediately; a backend tombstone rejects already-in-flight token writes.
      const revocation = bounded(() => api.revoke({ bindingId })).then(() => true, () => false);
      stopPromise = serial(async () => {
        const removed = await cleanup();
        let unregistered = true;
        try { await bounded(() => push.unregister()); } catch { unregistered = false; }
        try { await bounded(() => push.removeAllDeliveredNotifications()); }
        catch { unregistered = false; }
        seen.clear(); opening.clear();
        const revoked = await revocation;
        return status(!revoked ? 'revocation_pending' :
          !removed || !unregistered ? 'native_cleanup_failed' : 'stopped');
      });
      return stopPromise;
    },
    getState() { return { state }; },
    async settled() { // Bounded local queues, useful for host coordination and fake tests.
      await operation; await writes; await Promise.allSettled([...tasks]);
      return { state };
    },
  };
}
