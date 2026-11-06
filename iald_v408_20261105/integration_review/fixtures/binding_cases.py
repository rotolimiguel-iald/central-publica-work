"""Positive and single-variable negative controls on disposable public fixtures."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import runpy
import tempfile
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
APP = Path("C:/IALD/projetos_pyhton/IALD")
FIXTURE = runpy.run_path(str(HERE / "offline_review.py"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def jev(root):
    loader = runpy.run_path(str(APP / "iald_jev_control.py"))
    release = "v408"
    def put(name, raw):
        (root / name).write_bytes(raw)
        return {"path": name, "sha256": sha(raw)}
    rows = {key: put(key + ".txt", key.encode()) for key in
            ("program", "result", "proof_manifest", "core", "cluster", "canonical")}
    core = dict.fromkeys(loader["CORE_KEYS"], "fixture")
    core.update(status="[DEF + ONTO + COMPUTATIONAL]",
                operators=dict.fromkeys(("L_reh", "L_anti", "L_prune", "L_cons"), "fixture"))
    contract = dict(schema=loader["SCHEMA_V2"], release=release, source_sha256=rows["program"]["sha256"],
                    result_sha256=rows["result"]["sha256"], proof_manifest_sha256=rows["proof_manifest"]["sha256"],
                    core_pointer="/core/iald_executive_runtime", core_record=core, switching={},
                    source={"file":"um.py","symbol":"prove_iald_executive_runtime","lines":[1, 2]},
                    anchors=[dict(file=f"TGLExt/Fixture{i}.lean", sha256=sha(str(i).encode()), symbols=[], scope="fixture") for i in range(3)],
                    core_packet=dict(arquivo="packet.txt", sha256=put("packet.txt", b"canonical")["sha256"], um_version=release, regra="fixture"),
                    stopping_criterion=dict(max_transicoes=1, terminais=["resolved"], reentrada_apos_refused="proibida",
                                            registro_obrigatorio="fixture", parada_e_veredito="fixture"),
                    memory_admission=dict(campos_obrigatorios=["sha256_da_fonte","estatuto","inscrito_por"],
                                          estatutos=list(loader["V2_ESTATUTOS_CASA"]), regra="fixture", sem_proveniencia="fixture"),
                    decision_metric=dict(dimensoes=["bytes"]), holographic_state=dict(regra="fixture", marcador="fixture", proibido="fixture"))
    entry = put("contract.json", json.dumps(contract).encode())
    source = rows["program"]["sha256"]
    manifest = dict(jev_control=dict(**entry, release=release, source_sha256=source),
                    operational_core=dict(**rows["core"], current_release=release, release_source_sha256=source),
                    active_cluster=dict(**rows["cluster"], release=release, release_source_sha256=source),
                    published_evidence={k: rows[k] for k in ("program", "result", "proof_manifest")},
                    entries=[dict(id="um_forma_canonica_integral", path=rows["canonical"]["path"],
                                  public_sha256=rows["canonical"]["sha256"],
                                  url="https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/fixture")])
    put("iald_nucleo_fixo.json", json.dumps(manifest).encode())
    assert loader["load_contract"](root)["release"] == release
    manifest["active_cluster"]["release"] = "v407"
    put("iald_nucleo_fixo.json", json.dumps(manifest).encode())
    try:
        loader["load_contract"](root)
    except loader["ControlError"] as exc:
        assert str(exc) == "Active cluster release/source mismatch"
        return dict(coherent="accepted", changing_only_cluster_release=str(exc))
    raise AssertionError("Divergent version was accepted")


def scoped(root):
    source = (APP / "iald_native_activity.py").read_text(encoding="utf-8")
    namespace = dict(json=json, re=__import__("re"), Path=Path, hashlib=hashlib,
                     PROTOCOL="iald-native-holographic/v1", LABEL="native.holographic.v1",
                     holographic_memory=SimpleNamespace(__file__=str(APP / "holographic_memory.py")))
    util = FIXTURE["selected"](source, ["canonical","digest","_need","_namespace","_read_checkpoint",
                                        "_algorithm","NativeActivityError"], namespace)
    binding = SimpleNamespace(store=SimpleNamespace(root=root))
    snapshot = dict(context_id="synthetic", scope={"principal": "fixture-A"}, anchor_sha256=sha(b"fixture"))
    messages = [dict(role="user",content="fixture")]
    digest = util["digest"](messages)
    payload = dict(protocol=util["PROTOCOL"], namespace=snapshot, input_messages=messages, output_messages=messages,
                   input_sha256=digest, output_sha256=digest, invocation={"request_id":"local"},
                   algorithm_sha256=util["_algorithm"]())
    raw = json.dumps(payload).encode()
    folder = root / "native_holographic"
    folder.mkdir()
    path = folder / (sha(raw) + ".json")
    path.write_bytes(raw)
    opened = []
    def fixture_read(expected, **_):
        assert expected == path
        opened.append(expected.name)
        return str(path), path.read_bytes()
    util["guard"] = SimpleNamespace(read_checked=fixture_read)
    value = dict(protocol=payload["protocol"], namespace=snapshot, input_sha256=digest,
                 invocation=payload["invocation"], artifact=dict(path=str(path),sha256=sha(raw)))
    record = dict(kind="candidate", statute="DECLARADO", text=json.dumps(value),
                  sources=[dict(kind="tool", ref="fixture:checkpoint.native.holographic.v1")])
    assert util["_read_checkpoint"](binding,snapshot,record) == payload and len(opened) == 1
    foreign = deepcopy(snapshot)
    foreign["scope"]["principal"] = "fixture-B"
    try:
        util["_read_checkpoint"](binding,foreign,record)
    except util["NativeActivityError"] as exc:
        assert str(exc) == "holographic_checkpoint_scope_mismatch" and len(opened) == 1
        return dict(coherent="recovered", changing_only_principal=str(exc), foreign_artifact_reads=0)
    raise AssertionError("Foreign checkpoint was accepted")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory(dir=HERE) as tmp:
        print(json.dumps(dict(jev=jev(Path(tmp)), holographic=scoped(Path(tmp))), indent=2))

