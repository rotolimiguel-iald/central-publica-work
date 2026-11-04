# -*- coding: utf-8 -*-
"""Revisor independente da INSTALACAO v406 - D7 e D8 em processo NOVO, com os carregadores de producao.
Escrito pelo revisor; nao importa verify_installed.py. Bloqueia rede e abertura de .env por gancho de auditoria."""
import sys, os
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
RUNTIME = "C:/IALD/projetos_pyhton/IALD"
os.environ["TIKTOKEN_CACHE_DIR"] = RUNTIME + "/.iald_runtime/tokenizer_cache"
# nenhuma credencial no ambiente deste processo (nao impressas)
for _k in list(os.environ):
    if any(s in _k.upper() for s in ("KEY", "TOKEN", "SECRET", "PASSWORD")) and _k != "TIKTOKEN_CACHE_DIR":
        del os.environ[_k]

BLOQUEADOS = {"rede": [], "env": []}


def _hook(event, args):
    try:
        if event in ("socket.connect", "socket.getaddrinfo", "socket.gethostbyname", "socket.gethostbyaddr", "socket.sendto"):
            BLOQUEADOS["rede"].append(event)
            raise OSError("rede bloqueada pelo revisor: " + event)
        if event == "open":
            p = args[0]
            if isinstance(p, (str, bytes, os.PathLike)):
                name = os.path.basename(os.fsdecode(p)).lower()
                if name == ".env" or name.startswith(".env.") or name.endswith(".env"):
                    BLOQUEADOS["env"].append(name)
                    raise PermissionError(".env bloqueado pelo revisor")
    except (OSError, PermissionError):
        raise
    except Exception:
        pass


sys.addaudithook(_hook)
sys.path.append(RUNTIME)

import json, hashlib, dataclasses, time
from pathlib import Path

W = Path("C:/IALD/Central de Patentes/work/iald_v406_20261103")
OUT = W / "review/revisor_sonnet-app-v406-revisor-d"
ROOT = Path(RUNTIME)
MANIFEST = ROOT / "iald_nucleo_fixo.json"
PIN = "ddcb91930982d6143f47127d43020ab97cb9f5275331f470f2d0e4caaffd1fc0"  # dado pelo orquestrador; conferido abaixo contra o um.py do cofre


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def asdict(o):
    if dataclasses.is_dataclass(o):
        return dataclasses.asdict(o)
    if hasattr(o, "_asdict"):
        return o._asdict()
    return dict(vars(o))


R = {"pid_deste_processo": os.getpid(), "python": sys.version.split()[0]}
t0 = time.time()

# pino do um.py recalculado do cofre
try:
    vault_um = Path("C:/IALD/Central de Patentes/vault/originals_copy/um_unificado_v406/um.py")
    R["sha_um_py_do_cofre_v406"] = sha_file(vault_um)
    R["pino_confere_com_cofre"] = (R["sha_um_py_do_cofre_v406"] == PIN)
except Exception as e:  # noqa
    R["sha_um_py_do_cofre_v406"] = "ERRO:" + repr(e)
    R["pino_confere_com_cofre"] = None

from claude_memory_package import load_package
from claude_profiles import HAIKU
from iald_kernel import KernelCatalog
from iald_release_binding import load_release
from iald_jev_control import load_contract

mf = json.loads(MANIFEST.read_bytes())
cluster = mf["active_cluster"]
R["manifesto_cluster"] = {k: cluster[k] for k in ("release", "kernel_bundle", "kernel_verification", "commit") if k in cluster}

# kernel (o mesmo que o filho web carrega ao subir)
catalog = KernelCatalog(cluster["kernel_bundle"], cluster.get("kernel_verification"))
st = catalog.status()
R["kernel"] = {"source_sha256": catalog.source_sha, "igual_ao_pino": catalog.source_sha == PIN,
               "files": st.get("files"), "lean_files": st.get("lean_files"), "lean_toolchain": st.get("lean_toolchain")}

# release
rel = load_release(MANIFEST, source_sha=catalog.source_sha)
R["release"] = dict(rel.identity)
R["release_e_v406"] = rel.identity["release"] == "v406" and rel.identity["source_sha256"] == PIN

# controle negativo: o carregador recusa fonte errada (prova que a conferencia pode falhar)
try:
    load_release(MANIFEST, source_sha="0" * 64)
    R["controle_negativo_release"] = "NAO_RECUSOU"
except ValueError as e:
    R["controle_negativo_release"] = "RECUSOU:" + str(e)[:80]

# pacotes
pk = {}
for name in ("haiku55", "haiku"):
    d = ROOT / ".iald_runtime" / name
    p = load_package(d, canonical_manifest=MANIFEST, source_sha=catalog.source_sha, expected_model=HAIKU.model)
    meas = asdict(p.measurement)
    mj = json.loads((d / "manifest.json").read_bytes())
    nc = json.loads((d / "native_count.json").read_bytes())
    prefix_file = d / "prefix.md"
    row = {"permanent_tokens_load_package": meas.get("permanent_tokens", meas.get("tokens")), "measurement": meas,
           "prefix_bytes_utf8_do_pacote": len(p.prefix.encode("utf-8")), "prefix_bytes_arquivo": prefix_file.stat().st_size,
           "prefix_sha256_arquivo": sha_file(prefix_file), "manifest.prefix_sha256": mj["prefix_sha256"],
           "manifest.budget.permanent_tokens": mj["budget"]["permanent_tokens"],
           "native_count.budget.permanent_tokens": nc["budget"]["permanent_tokens"],
           "native_count.prefix_sha256": nc["prefix_sha256"], "native_count.status": nc["status"],
           "native_count.count_requests": nc["count_requests"], "native_count.generation_requests": nc["generation_requests"],
           "reserved_output_tokens": p.reserved_output_tokens, "available_dynamic_tokens": p.available_dynamic_tokens,
           "deployment_do_manifesto_igual_a_release": mj["deployment"] == rel.identity}
    pk[name] = row
    # controle negativo do pacote
    try:
        load_package(d, canonical_manifest=MANIFEST, source_sha="f" * 64, expected_model=HAIKU.model)
        row["controle_negativo"] = "NAO_RECUSOU"
    except ValueError as e:
        row["controle_negativo"] = "RECUSOU:" + str(e)[:80]
R["pacotes"] = pk

# contrato JEV
c = load_contract(ROOT)
R["jev"] = {"release": c["release"], "schema": c.get("schema"), "source_sha256": c["source_sha256"],
            "igual_ao_pino": c["source_sha256"] == PIN, "core_packet": {k: c.get("core_packet", {}).get(k) for k in ("um_version", "arquivo", "sha256")}}

# extras de D8 (mesmos numeros que o construtor grava); falha aqui nao derruba D7
extras = {}
try:
    from iald_native_memory import load_native_context
    native, ident = load_native_context(MANIFEST, catalog)
    extras["native_bytes"] = len(native.encode())
    extras["native_identity_igual_release"] = (ident == rel.identity)
except Exception as e:  # noqa
    extras["native_erro"] = repr(e)[:200]
try:
    from iald_memoria_canonica import CanonicalMemory
    public, meta = CanonicalMemory(Path("C:/IALD/Central de Patentes/memory/TGL_ATLAS.md"), "nucleo_kernel",
                                   nucleus_manifest=MANIFEST).prompt("", catalog, public=True)
    extras["public_prompt_bytes"] = len(public.encode())
    extras["private_atlas_included"] = meta.get("private_atlas_included")
except Exception as e:  # noqa
    extras["public_prompt_erro"] = repr(e)[:200]
R["extras"] = extras

# D8: comparacao com a evidencia do construtor
iv = json.loads((W / "INSTALLED_VERIFICATION.json").read_bytes())
d14 = json.loads((OUT / "d1_d4_result.json").read_bytes())
d2_ok = d14["checks"]["D2"]["ok_no_disco"]
rel_json = json.loads((W / "app/RELEASE.json").read_bytes())
cmp = {
    "status_PASS": iv["status"] == "PASS",
    "files_verified_igual_D2": (iv["files_verified"] == d2_ok == 1773),
    "identity_igual_release_medida": (iv["identity"] == rel.identity),
    "haiku55_tokens": (iv["packages"]["haiku55"]["permanent_tokens"] == pk["haiku55"]["permanent_tokens_load_package"] == pk["haiku55"]["native_count.budget.permanent_tokens"] == 841257),
    "haiku55_bytes": (iv["packages"]["haiku55"]["prefix_bytes"] == pk["haiku55"]["prefix_bytes_utf8_do_pacote"] == pk["haiku55"]["prefix_bytes_arquivo"] == 1575137),
    "haiku_tokens": (iv["packages"]["haiku"]["permanent_tokens"] == pk["haiku"]["permanent_tokens_load_package"] == pk["haiku"]["native_count.budget.permanent_tokens"] == 401802),
    "haiku_bytes": (iv["packages"]["haiku"]["prefix_bytes"] == pk["haiku"]["prefix_bytes_utf8_do_pacote"] == pk["haiku"]["prefix_bytes_arquivo"] == 812335),
    "public_commit_igual_cluster_e_RELEASE": (iv["public_commit"] == cluster.get("commit") == rel_json["espelho_commit"]),
    "JEV_release": (iv["JEV_release"] == c["release"] == "v406"),
    "provider_calls_zero": (iv["provider_calls"] == 0),
    "science_executed_false": (iv["science_executed"] is False),
    "native_bytes_igual": (extras.get("native_bytes") == iv["native_bytes"]) if "native_bytes" in extras else None,
    "public_prompt_bytes_igual": (extras.get("public_prompt_bytes") == iv["public_prompt_bytes"]) if "public_prompt_bytes" in extras else None,
}
R["D8_comparacao"] = cmp
R["bloqueios_do_gancho"] = {"tentativas_de_rede": len(BLOQUEADOS["rede"]), "aberturas_de_env_bloqueadas": len(BLOQUEADOS["env"]), "env_nomes": sorted(set(BLOQUEADOS["env"]))}
R["segundos"] = round(time.time() - t0, 1)

d7_ok = (R["release_e_v406"] and R["jev"]["release"] == "v406" and R["jev"]["igual_ao_pino"] and R["kernel"]["igual_ao_pino"]
         and pk["haiku55"]["permanent_tokens_load_package"] == 841257 == pk["haiku55"]["native_count.budget.permanent_tokens"]
         and pk["haiku"]["permanent_tokens_load_package"] == 401802 == pk["haiku"]["native_count.budget.permanent_tokens"]
         and all(v["deployment_do_manifesto_igual_a_release"] for v in pk.values())
         and R["pino_confere_com_cofre"] is True
         and R["controle_negativo_release"].startswith("RECUSOU") and all(v["controle_negativo"].startswith("RECUSOU") for v in pk.values()))
d8_core = all(v is True for k, v in cmp.items() if v is not None)
d9_ok = (len(BLOQUEADOS["rede"]) == 0 and len(BLOQUEADOS["env"]) == 0 and iv["provider_calls"] == 0)
R["PASS_D7"] = bool(d7_ok)
R["PASS_D8"] = bool(d8_core)
R["PASS_D9_parcial_este_script"] = bool(d9_ok)
(OUT / "d7_d8_result.json").write_text(json.dumps(R, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
print("D7", "PASS" if d7_ok else "FAIL", "| D8", "PASS" if d8_core else "FAIL", "| D9(script)", "PASS" if d9_ok else "FAIL")
print(json.dumps({k: R[k] for k in ("pino_confere_com_cofre", "kernel", "release", "release_e_v406", "controle_negativo_release", "jev", "extras", "D8_comparacao", "bloqueios_do_gancho", "segundos")}, ensure_ascii=False, indent=1, default=str)[:6000])
for n, v in pk.items():
    print(n, {k: v[k] for k in ("permanent_tokens_load_package", "prefix_bytes_utf8_do_pacote", "prefix_bytes_arquivo", "manifest.budget.permanent_tokens", "native_count.budget.permanent_tokens", "native_count.count_requests", "native_count.generation_requests", "controle_negativo", "deployment_do_manifesto_igual_a_release")})
