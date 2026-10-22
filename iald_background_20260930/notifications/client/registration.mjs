import { createNativeNotifications, nativePlugins } from './native-notifications.mjs';

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;

/** Call from the authenticated host after a user gesture (or restored explicit opt-in).
 * requestJSON is the existing app's HTTPS/auth/CSRF adapter; it must reject non-2xx,
 * support AbortSignal, and have its own timeout. Do not create another auth mechanism.
 * installationId is a random, persistent local UUID, never a user name or credential.
 */
export async function connectNotifications({ requestJSON, installationId, consent,
  openJob, onJobs, onStatus, plugins, nativeReady = false, prompt = false }) {
  if (consent !== true || !UUID.test(installationId ?? '') ||
      typeof requestJSON !== 'function' || typeof onJobs !== 'function')
    throw new Error('notification_opt_in_required');
  const disabled = () => ({ state: 'configuration_disabled' });
  const inactive = { getState: disabled, start: async () => disabled(), enable: async () => disabled(),
    stop: async () => disabled(), settled: async () => disabled() };
  // Rollout flag is false by default. Do not even load/register a native plugin until ready.
  if (nativeReady !== true) return inactive;
  plugins ??= nativePlugins();
  if (plugins.platform === 'android') {
    let readiness;
    try { readiness = await plugins.readiness?.getStatus(); }
    catch { return inactive; }
    if (readiness?.ready !== true) return inactive;
  }
  let binding;
  try {
    binding = await requestJSON('/api/native-push/bindings', { method: 'POST',
      body: { installation_id: installationId, platform: plugins.platform, consent: true } });
  } catch { throw new Error('notification_binding_failed'); }
  if (!binding || !UUID.test(binding.id ?? '') || binding.revoked !== false ||
      binding.platform !== plugins.platform) throw new Error('invalid_notification_binding');
  const path = '/api/native-push/bindings/' + binding.id;
  const api = {
    saveToken: ({ token, provider, signal }) => requestJSON(path + '/token', {
      method: 'PUT', body: { token, provider }, signal }),
    revoke: () => requestJSON(path, { method: 'DELETE', body: {} }),
    getJob: async ({ jobId, signal }) => {
      const job = await requestJSON('/api/chat-jobs/' + encodeURIComponent(jobId), { method: 'GET', signal });
      return { id: job?.id, state: job?.status, conversationId: job?.conversation_id };
    },
    reconcile: async ({ signal }) => {
      const result = await requestJSON('/api/chat-jobs', { method: 'GET', signal });
      if (signal.aborted) return;
      if (!Array.isArray(result?.jobs)) throw new Error('invalid_jobs_response');
      await onJobs(result.jobs, { signal });
    },
  };
  const controller = createNativeNotifications({ ...plugins, bindingId: binding.id,
    api, openJob, onStatus });
  const initial = await controller.start();
  if (initial.state === 'startup_failed') {
    await controller.stop();
    throw new Error('notification_startup_failed');
  }
  if (prompt) await controller.enable();
  return controller;
}
