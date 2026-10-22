package br.ia.iald.app;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

@CapacitorPlugin(name = "IaldPushReadiness")
public class IaldPushReadinessPlugin extends Plugin {
    @PluginMethod
    public void getStatus(PluginCall call) {
        boolean ready = false;
        if (getContext().getResources().getBoolean(R.bool.iald_push_enabled)) {
            try {
                // No Firebase dependency required in disabled builds; never creates a token.
                Class<?> firebase = Class.forName("com.google.firebase.FirebaseApp");
                ready = firebase.getMethod("getInstance").invoke(null) != null;
            } catch (Exception | LinkageError ignored) {
                // No exception body, config or credential goes to JavaScript/logs.
            }
        }
        JSObject result = new JSObject();
        result.put("ready", ready);
        call.resolve(result);
    }
}
