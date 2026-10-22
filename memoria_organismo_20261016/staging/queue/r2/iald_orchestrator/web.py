"""Local admin-only Flask extension. Public conversation clients are unaffected."""
from pathlib import Path
from urllib.parse import urlsplit
from .runtime import Runtime
from .coordination import Coordination


def install(app, require_admin):
    from flask import Blueprint, jsonify, request, Response
    runtime = Runtime()
    coordination = Coordination(runtime)
    bp = Blueprint("iald_orchestrator", __name__)
    root = "/admin/api/orchestrator"

    @bp.before_request
    def protect():
        denied = require_admin()
        if denied is not None:
            return denied
        # Same origin on every mutation; localhost alone is not a CSRF defense.
        if request.method == "POST":
            origin = request.headers.get("Origin")
            if not origin or urlsplit(origin).netloc.lower() != request.host.lower() or urlsplit(origin).scheme != request.scheme:
                return jsonify(error="Origem não autorizada."), 403
            if request.headers.get("Sec-Fetch-Site") not in (None, "same-origin", "none"):
                return jsonify(error="Origem não autorizada."), 403
            if not request.is_json or request.content_length is None or request.content_length > 100000:
                return jsonify(error="JSON obrigatório ou corpo excedido."), 400
            if not isinstance(request.get_json(), dict):
                return jsonify(error="O corpo JSON deve ser um objeto."), 400

    @bp.after_request
    def private(response):
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self'; frame-ancestors 'self'; base-uri 'none'; form-action 'self'"
        return response

    @bp.errorhandler(ValueError)
    def invalid(exc):
        return jsonify(error=str(exc)), 400

    @bp.get("/admin/agi/orquestracao")
    def page():
        return Response((Path(__file__).parent / "panel.html").read_text(encoding="utf-8"), mimetype="text/html")

    @bp.get(root + "/panel.js")
    def script():
        return Response((Path(__file__).parent / "panel.js").read_text(encoding="utf-8"), mimetype="application/javascript")

    @bp.get("/admin/agi/orquestracao/mimo")
    def mimo_key_page():
        return Response((Path(__file__).parent / "mimo-key.html").read_text(encoding="utf-8"), mimetype="text/html")

    @bp.get(root + "/mimo-key.js")
    def mimo_key_script():
        return Response((Path(__file__).parent / "mimo-key.js").read_text(encoding="utf-8"), mimetype="application/javascript")

    @bp.post(root + "/connections/mimo/key")
    def store_mimo_key():
        from .secret_store import store_mimo
        try:
            store_mimo(request.get_json().get("key"))
        except ValueError:
            return jsonify(error="Formato de chave inválido."), 400
        except Exception:
            return jsonify(error="Não foi possível guardar a chave no cofre Windows."), 503
        return jsonify(stored=True, storage="WINDOWS_DPAPI_CURRENT_USER", expires_at=None)

    @bp.get("/admin/agi/orquestracao/deepseek")
    def deepseek_key_page():
        return Response((Path(__file__).parent / "deepseek-key.html").read_text(encoding="utf-8"), mimetype="text/html")

    @bp.get(root + "/deepseek-key.js")
    def deepseek_key_script():
        return Response((Path(__file__).parent / "deepseek-key.js").read_text(encoding="utf-8"), mimetype="application/javascript")

    @bp.post(root + "/connections/deepseek/key")
    def store_deepseek_key():
        from .deepseek_secret_store import store_key
        from .deepseek import AUTHORIZATION
        from .safe_files import save_json, utc_now
        body = request.get_json()
        if body.get("authorize_paid_tasks") is not True:
            return jsonify(error="Confirme o uso do saldo para tarefas autorizadas."), 400
        try:
            store_key(body.get("key"))
            save_json(AUTHORIZATION, {"enabled": True, "scope": "IALD_OPERATOR_AUTHORIZED_TASKS",
                "financial_cap_usd": None, "routing_scope": "ALL_COMPLEXITIES_OPERATOR_AUTHORIZED",
                "authorized_at": utc_now(), "provider_improvement_preference": True})
        except ValueError:
            return jsonify(error="Formato de chave inválido."), 400
        except Exception:
            return jsonify(error="Não foi possível guardar a chave no cofre Windows."), 503
        return jsonify(stored=True, storage="WINDOWS_DPAPI_CURRENT_USER", expires_at=None)

    @bp.get("/admin/agi/orquestracao/jev")
    def jev_key_page():
        return Response((Path(__file__).parent / "jev-key.html").read_text(encoding="utf-8"), mimetype="text/html")

    @bp.get(root + "/jev-key.js")
    def jev_key_script():
        return Response((Path(__file__).parent / "jev-key.js").read_text(encoding="utf-8"), mimetype="application/javascript")

    @bp.post(root + "/connections/jev/key")
    def store_jev_key():
        from .jev_secret_store import store_key
        from .jev import ACTIVATION
        from .safe_files import save_json, utc_now
        try:
            store_key(request.get_json().get("key"))
            save_json(ACTIVATION, {"enabled": False, "probe_status": "configured_not_tested",
                "configured_at": utc_now(), "scope": "STRUCTURED_ROUTING_ONLY"})
        except ValueError:
            return jsonify(error="Formato de chave inválido."), 400
        except Exception:
            return jsonify(error="Não foi possível guardar a chave no cofre Windows."), 503
        return jsonify(stored=True, enabled=False, storage="WINDOWS_DPAPI_CURRENT_USER", expires_at=None)

    @bp.get(root + "/status")
    def status():
        return jsonify({**runtime.status(), "coordination_jobs": coordination.listing()})

    @bp.post(root + "/preview")
    def preview():
        body = request.get_json()
        return jsonify(runtime.preview(body.get("prompt"),body.get("execution_constraints")))

    @bp.post(root + "/tasks")
    def submit():
        body = request.get_json()
        return jsonify(runtime.submit(body.get("prompt"), body.get("request_id", ""),execution_constraints=body.get("execution_constraints"))), 202

    @bp.get(root + "/tasks/<task_id>")
    def task(task_id):
        return jsonify(runtime.task(task_id))

    @bp.post(root + "/tasks/<task_id>/cancel")
    def cancel(task_id):
        return jsonify(runtime.cancel(task_id))

    @bp.post(root + "/connections/<provider>/allow-retry")
    def allow_retry(provider):
        return jsonify(runtime.request_recheck(provider))

    @bp.post(root + "/coordination")
    def create_coordination():
        body = request.get_json()
        return jsonify(coordination.create(body.get("prompt"), body.get("request_id", ""),body.get("execution_constraints"))), 201

    @bp.get(root + "/coordination/<job_id>")
    def get_coordination(job_id):
        return jsonify(coordination.get(job_id))

    @bp.post(root + "/coordination/<job_id>/cancel")
    def cancel_coordination(job_id):
        return jsonify(coordination.act(job_id, "cancel"))

    app.register_blueprint(bp)
    app.extensions["iald_orchestrator"] = runtime
    return runtime
