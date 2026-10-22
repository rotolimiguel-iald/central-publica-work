"""Dedicated official-client profiles; credential contents are never inspected."""
import os
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
PROFILES=BASE/'state'/'profiles'

# Sandboxed Codex sessions may not see the Windows user site-packages.
# Use the locally bundled dependency only when no installed YAML is available.
import importlib.util
import sys
if importlib.util.find_spec('yaml') is None:
    local_dependencies = BASE / 'clients/python'
    if (local_dependencies / 'yaml/__init__.py').is_file():
        sys.path.append(str(local_dependencies))


def client_environment(provider):
    env=dict(os.environ)
    for key in list(env):
        if any(word in key.upper() for word in ('API_KEY','AUTH_TOKEN','SECRET')):
            env.pop(key,None)
    profile=PROFILES/("kimi-apple" if provider == "kimi" else provider)
    profile.mkdir(parents=True,exist_ok=True)
    if provider=='gemini':
        env['GEMINI_CLI_HOME']=str(profile)
    elif provider=='kimi':
        env['KIMI_CODE_HOME']=str(profile)
        env.pop('KIMI_DISABLE_TELEMETRY', None)  # Operator opted in to product improvement.
    elif provider=='mimo':
        for name,part in [('XDG_CONFIG_HOME','config'),('XDG_DATA_HOME','data'),('XDG_CACHE_HOME','cache')]:
            env[name]=str(profile/part)
    return env

def login_workspace(provider):
    path=BASE/'state'/'login'/provider
    path.mkdir(parents=True,exist_ok=True)
    (path/'.git').mkdir(exist_ok=True)
    return path
