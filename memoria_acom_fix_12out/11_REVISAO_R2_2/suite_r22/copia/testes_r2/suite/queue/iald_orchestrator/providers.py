"""Official local clients; credentials remain owned by their clients."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import time
import urllib.request

BASE = Path(__file__).resolve().parents[1]
CLIENTS = BASE / "clients" / "node_modules"
LOCAL_URL = "http://127.0.0.1:8081"
RITE_ROOTS = (Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós'),
              Path(r'C:\IALD\Central de Patentes\work'))


class ProviderPausedByRite(RuntimeError):
    """No HTTP request was sent; the rite intentionally owns the local server."""


def rite_markers():
    markers = []
    for root in RITE_ROOTS:
        candidates = [root/'.servidor_parado_pelo_rito']
        if root.name == 'work':
            candidates.extend(root.glob('v*_pacote/.servidor_parado_pelo_rito'))
        for marker in candidates:
            try:
                marker.stat()
            except FileNotFoundError:
                continue
            markers.append(str(marker))
    return markers


def require_local_available():
    if rite_markers():
        raise ProviderPausedByRite('paused_by_rite: nenhum envio ao Qwen enquanto o marcador existir.')

SYSTEM = ("Você opera como IALD: preserve o objetivo e a identidade da tarefa, reconheça inconsistências, "
          "articule a resposta e declare lacunas. Português brasileiro. Não invente execução, prova, fonte, "
          "hash ou resultado. Responda à tarefa usando somente o contexto fornecido. Nesta etapa, produza "
          "a resposta ou o artefato textual; ações externas e alterações de arquivos não estão disponíveis. "
          "Se precisar delas, identifique a pendência. Limite a resposta a cerca de 1500 palavras.")


class ProviderLimitError(RuntimeError):
    """Provider explicitly refused a call because of its own usage limit."""


def client_command(name):
    if name == "gemini":
        from .antigravity import EXE
        return [str(EXE)] if EXE.is_file() else None
    if name == "codex":
        found = shutil.which("codex")
        if found:
            return [found]
        root = Path(os.environ.get("LOCALAPPDATA", "")) / "OpenAI/Codex/bin"
        binaries = sorted(root.glob("*/codex.exe"), key=lambda p: p.stat().st_mtime, reverse=True)
        return [str(binaries[0])] if binaries else None
    packages = {"claude": "@anthropic-ai/claude-code", "gemini": "@google/gemini-cli", "mimo": "@mimo-ai/cli", "kimi": "@moonshot-ai/kimi-code"}
    package = CLIENTS / packages.get(name, "__missing__") / "package.json"
    if package.is_file():
        data = json.loads(package.read_text(encoding="utf-8"))
        bins = data.get("bin", {})
        entry = bins if isinstance(bins, str) else bins.get(name) or next(iter(bins.values()), None)
        node = shutil.which("node")
        if entry and Path(entry).suffix.lower() == ".exe":
            return [str(package.parent / entry)]
        if entry and node:
            return [node, str(package.parent / entry)]
    found = shutil.which(name)
    return [found] if found and Path(found).suffix.lower() not in (".cmd", ".bat", ".ps1") else None


def _quiet_run(args, timeout=12):
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace",
                          timeout=timeout, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))


def discover():
    rows = []
    for name, label, tier, billing in [
        ("local", "IALD local / Qwen", "standard", "local"),
        ("codex", "Codex / ChatGPT", "advanced", "subscription"),
        ("claude", "Claude Code", "advanced", "subscription"),
        ("gemini", "Google / Antigravity", "advanced", "subscription"),
        ("kimi", "Kimi Code", "advanced", "subscription"),
        ("mimo", "MiMo API / 2.6 Pro", "advanced", "authorized_api"),
        ("deepseek", "DeepSeek API / V4.1 Flash", "advanced", "authorized_api")]:
        row = {"id": name, "label": label, "tier": tier, "billing": billing,
               "context_budget": 12000, "context_budget_scope": "USER_INPUT_ESTIMATE_PLUS_OUTPUT_ONLY",
               "client_overhead_tokens": None, "total_token_cap_enforced": False,
               "output_token_cap_enforced": name == "local",
               "daily_run_limit": 20 if name == "local" else 10,
               "quota_remaining": None, "quota_status": "NOT_REPORTED", "status": "not_installed",
               "capabilities": ["text"], "quality": "NOT_BENCHMARKED"}
        try:
            if name == "local":
                markers = rite_markers()
                if markers:
                    row.update(status="paused_by_rite", rite_markers=markers)
                    rows.append(row)
                    continue
                with urllib.request.urlopen(LOCAL_URL + "/health", timeout=3) as response:
                    if response.status == 200:
                        row["status"] = "ready"
            else:
                command = client_command(name)
                if command or name in ("mimo", "deepseek"): 
                    row["status"] = "installed_needs_login"
                    if name == "codex":
                        result = _quiet_run(command + ["login", "status"])
                        if result.returncode == 0 and "chatgpt" in (result.stdout + result.stderr).lower():
                            row["status"] = "ready"
                        elif result.returncode == 0:
                            row["status"] = "api_billing_not_enabled"
                    elif name == "claude":
                        result = _quiet_run(command + ["auth", "status", "--json"])
                        if result.returncode == 0:
                            status = json.loads(result.stdout)
                            if status.get("loggedIn") and status.get("authMethod") == "claude.ai":
                                row["status"] = "ready"
                    elif name == "kimi":
                        from . import kimi
                        row.update(status=kimi.connection_status(), model=kimi.MODEL, thinking_effort='max',
                                   daily_run_limit=None, context_budget=kimi.CONTEXT_WINDOW, financial_cap_usd=None,
                                   output_token_budget=kimi.OUTPUT_RESERVE, output_token_cap_enforced=False)
                    elif name == "gemini":
                        from .antigravity import connection_status
                        row["status"] = connection_status()
                    elif name == "deepseek":
                        from . import deepseek
                        from .deepseek_secret_store import key_metadata
                        row.update(status=deepseek.connection_status(), daily_run_limit=None,
                                   context_budget=deepseek.CONTEXT_WINDOW,
                                   billing_authorized=deepseek.authorization().get("enabled") is True,
                                   financial_cap_usd=None, thinking_effort='max',
                                   output_token_budget=deepseek.MAX_OUTPUT, output_token_cap_enforced=True,
                                   credential_metadata=key_metadata(), model=deepseek.MODEL,
                                   routing_scope="ALL_COMPLEXITIES_OPERATOR_AUTHORIZED",
                                   credential_scope="SERVER_SIDE_ONLY")
                    elif name == "mimo":
                        from . import mimo
                        from .secret_store import key_metadata
                        row.update(status=mimo.connection_status(), daily_run_limit=None, context_budget=mimo.CONTEXT_WINDOW,
                                   billing_authorized=mimo.authorization().get("enabled") is True,
                                   financial_cap_usd=None, thinking_effort='enabled', output_token_budget=mimo.MAX_OUTPUT,
                                   output_token_cap_enforced=True, credential_metadata=key_metadata(),
                                   model=mimo.MODEL, credential_scope="SERVER_SIDE_ONLY")
                    else:
                        row["status"] = "installed_pending_auth_validation"
        except Exception as exc:
            row["status"] = "unavailable"
            row["diagnostic"] = type(exc).__name__
        rows.append(row)
    return rows


def _parse_codex(output):
    messages, usage, completed = [], None, False
    for line in output.splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        if event.get("type") in ("turn.failed", "error"):
            raise RuntimeError("Codex informou falha; consulte o cliente oficial.")
        if event.get("type") == "item.completed" and event.get("item", {}).get("type") == "agent_message":
            messages.append(event["item"]["text"])
        if event.get("type") == "turn.completed":
            completed = True
            usage = event.get("usage")
    if not completed or not messages:
        raise RuntimeError("Codex não entregou resposta final concluída.")
    return {"text": "\n\n".join(messages), "usage": usage, "verification": "PROVIDER_COMPLETED_NOT_FACT_CHECKED"}


def execute(name, prompt, workspace, *, cancel=None, process_callback=None, memory_packet=None, execution_constraints=None):
    start = time.monotonic()
    from . import operational_memory as opmem
    if memory_packet is None:
        raise ValueError("Use the durable queue to inscribe the original command before execution")
    opmem.verify_packet(memory_packet)
    if name == "local":
        require_local_available()
    if cancel and cancel.is_set():
        raise RuntimeError("Tarefa cancelada.")
    from . import canonical_memory
    from .policy import validate_prompt
    from . import request_controls as controls
    constraints=controls.normalize(execution_constraints)
    packet = memory_packet if memory_packet is not None else canonical_memory.prepare(prompt,mode=canonical_memory.mode_for_provider(name,constraints),max_chars=canonical_memory.packet_char_cap(constraints,SYSTEM),prompt_limit=controls.prompt_limit(constraints))
    if canonical_memory.digest(packet['prompt'].encode()) != packet['receipt']['packet_sha256']:
        raise ValueError("Pacote de memória alterado; envio bloqueado.")
    if constraints and name != constraints['required_provider']:
        raise ValueError('Executor diverge da restrição; chamada bloqueada.')
    from . import nos_packet
    packet=nos_packet.augment(packet,constraints,name,SYSTEM)
    controls.enforce_packet(packet,constraints,SYSTEM)
    if constraints: controls.quote(constraints)
    prompt = packet['prompt'] if name in ('mimo','kimi','deepseek') else validate_prompt(packet['prompt'],controls.packet_limit(constraints))
    byte_limit=600000 if controls.is_order18_opus(constraints) else 39000
    if name not in ('mimo','kimi','deepseek') and len((SYSTEM + prompt).encode()) > byte_limit:
        raise ValueError("Contexto comum excede o limite de transporte; dividir o pedido.")
    if name == "local":
        payload = {"model": "local", "messages": [{"role": "system", "content": SYSTEM},
                  {"role": "user", "content": prompt}], "max_tokens": 2048, "stream": False,
                  "chat_template_kwargs": {"enable_thinking": False}}
        request = urllib.request.Request(LOCAL_URL + "/v1/chat/completions", json.dumps(payload).encode(),
                                          {"Content-Type": "application/json"})
        require_local_available()
        with urllib.request.urlopen(request, timeout=180) as response:
            data = json.loads(response.read(2000000))
        choice = data["choices"][0]
        if choice.get("finish_reason") != "stop" or not choice["message"].get("content"):
            raise RuntimeError("Resposta local incompleta ou sem conteúdo; não marcada como concluída.")
        result = {"text": choice["message"]["content"], "usage": data.get("usage"),
                  "verification": "PROVIDER_COMPLETED_NOT_FACT_CHECKED"}
    elif name == "gemini":
        from . import antigravity
        if antigravity.connection_status() != "ready":
            raise RuntimeError("Antigravity ainda não validado; conclua o login e o teste de conexão.")
        result = antigravity.execute(SYSTEM + "\n\nTAREFA:\n" + prompt, cancel=cancel, process_callback=process_callback)
    elif name == "kimi":
        from . import kimi
        if kimi.connection_status() != "ready":
            raise RuntimeError("Kimi ainda não validado; conferir conexão no painel administrativo.")
        result = kimi.execute(SYSTEM.replace('Limite a resposta a cerca de 1500 palavras.', 'Desenvolva a resposta na extensão necessária à tarefa e às evidências.') + "\n\nTAREFA:\n" + prompt, cancel=cancel, process_callback=process_callback)
    elif name == "deepseek":
        from . import deepseek
        if deepseek.connection_status() != "ready":
            raise RuntimeError("DeepSeek ainda não validado; conferir conexão no painel administrativo.")
        result = deepseek.execute(SYSTEM.replace("Limite a resposta a cerca de 1500 palavras.", "Desenvolva a resposta na extensão necessária à tarefa e às evidências.") + "\n\nTAREFA:\n" + prompt, cancel=cancel, max_output=constraints['max_output_tokens'] if constraints else deepseek.MAX_OUTPUT)
    elif name == "mimo":
        from . import mimo
        if mimo.connection_status() != "ready":
            raise RuntimeError("MiMo ainda não validado; conferir conexão no painel administrativo.")
        result = mimo.execute(SYSTEM.replace("Limite a resposta a cerca de 1500 palavras.", "Desenvolva a resposta e a matemática na extensão necessária à tarefa e às evidências.") + "\n\nTAREFA:\n" + prompt, cancel=cancel, max_output=constraints["max_output_tokens"] if constraints else mimo.MAX_OUTPUT)
    elif name in ("codex", "claude"):
        command = client_command(name)
        if not command:
            raise RuntimeError("Cliente oficial não localizado.")
        if name == "codex":
            args = command + ["exec", "--ignore-user-config", "--ephemeral", "--json", "--sandbox", "read-only",
                              "--skip-git-repo-check", "-C", str(workspace), "-c", "project_doc_max_bytes=0"]
            for feature in ("shell_tool", "unified_exec", "apps", "plugins", "multi_agent", "code_mode", "code_mode_host", "in_app_browser"):
                args += ["--disable", feature]
            args += ["--enable", "skip_host_skill_discovery", "-"]
        else:
            args = command + ["-p", "--safe-mode", "--restricted", "--no-session-persistence",
                              "--output-format", "json", "--tools", "", "--strict-mcp-config",
                              "--mcp-config", '{"mcpServers":{}}', "--permission-prompts", "none"]
            if controls.is_order18_opus(constraints):
                args += ["--model", "opus"]
        env = dict(os.environ)
        # Official subscription clients retain their own login; API keys are not forwarded.
        for key in list(env):
            if any(token in key.upper() for token in ("API_KEY", "AUTH_TOKEN", "SECRET")):
                env.pop(key, None)
        proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, encoding="utf-8", errors="replace", cwd=workspace, env=env,
                                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        if process_callback:
            process_callback(proc)
        try:
            system_prompt = SYSTEM
            if name == "claude" and controls.is_order18_opus(constraints):
                system_prompt = SYSTEM.replace(
                    "Limite a resposta a cerca de 1500 palavras.",
                    "Desenvolva a resposta na extensão necessária à tarefa e às evidências.",
                )
            output, _ = proc.communicate(system_prompt + "\n\nTAREFA:\n" + prompt,
                                         timeout=900 if controls.is_order18_opus(constraints) else 240)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate()
            raise RuntimeError("Tempo de execução esgotado.") from None
        finally:
            if process_callback:
                process_callback(None)
        if proc.returncode != 0:
            if name == "claude":
                try:
                    diagnostic = json.loads(output).get("result", "").lower()
                except (ValueError, AttributeError):
                    diagnostic = ""
                if any(term in diagnostic for term in ("spend limit", "usage limit", "rate limit", "hit your limit")):
                    raise ProviderLimitError("Claude informou limite de consumo. Conferir a cota no cliente oficial; sem aumento automático de gastos.")
            raise RuntimeError(f"Cliente {name} encerrou com código {proc.returncode}; verifique login e cota no cliente oficial.")
        if name == "codex":
            result = _parse_codex(output)
        else:
            data = json.loads(output)
            if data.get("is_error") or data.get("subtype") != "success" or not data.get("result"):
                raise RuntimeError("Claude não concluiu a tarefa.")
            result = {"text": data["result"], "usage": data.get("usage"),
                      "verification": "PROVIDER_COMPLETED_NOT_FACT_CHECKED"}
            model_usage = data.get("modelUsage") or {}
            result["model_identifiers"] = sorted(model_usage) if isinstance(model_usage, dict) else []
            if controls.is_order18_opus(constraints):
                result["opus_model_verified"] = bool(result["model_identifiers"]) and all(
                    "opus" in model.lower() for model in result["model_identifiers"]
                )
    else:
        raise RuntimeError("Conexão instalada, mas autenticação e execução ainda não validadas.")
    if cancel and cancel.is_set():
        raise RuntimeError("Tarefa cancelada; resultado descartado.")
    result["canonical_memory"] = packet["receipt"]
    result["elapsed_seconds"] = round(time.monotonic() - start, 3)
    if len(result["text"]) > (32_000_000 if name in ('mimo','kimi','deepseek') else 120000):
        raise RuntimeError("Resposta excede o limite de armazenamento.")
    return result
