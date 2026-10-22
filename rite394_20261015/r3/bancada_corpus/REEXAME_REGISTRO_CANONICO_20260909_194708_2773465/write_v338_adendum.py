from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, os

BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
OUT = Path(__file__).resolve().parent
HOUSE = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")

def pin(p):
    b = p.read_bytes()
    return {"path": p.as_posix(), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}

def new(p, b):
    assert OUT.is_relative_to(BASE) and not p.exists()
    t = p.with_name(p.name + ".tmp")
    with t.open("xb") as f:
        f.write(b); f.flush(); os.fsync(f.fileno())
    assert t.read_bytes() == b
    os.rename(t, p)
    assert p.read_bytes() == b

def table(p):
    tree = ast.parse(p.read_bytes().decode("utf-8"))
    return next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "_EMBEDDED_KERNEL_FILES" for t in n.targets))

cp = HOUSE / "um.py"
op = BASE / "COPIA_INTEGRADA_20260909_192248_937671/um.py"
pp = BASE / "INTEGRADOR_SELETOR_LOCALIDADE_20260909_174443_581582/BUILD_SUCCESSOR_20260909_174751_385895/BUILD_PLAN.json"
start = pin(cp)
a, b = table(cp), table(op)
plan = json.loads(pp.read_bytes())
bodies = {}
for module in plan["modules"]:
    key = module["key"]
    x, y = a[key], b[key]
    bodies[key] = x[x.index("import "):] == y[y.index("import "):]
assert len(bodies) == 77 and all(bodies.values())
missing = sorted(set(b) - set(a))
assert len(missing) == 6 and not set(a) - set(b)
proof_path = HOUSE / "tgl_kernel_proof_manifest.json"
seal_path = HOUSE / "um_absoluto_selo.json"
proof = json.loads(proof_path.read_bytes())
seal = json.loads(seal_path.read_bytes())
log = HOUSE / "rodada_v338_stdout.txt"
log_pin = pin(log) if log.exists() else None
log_excerpt = log.read_text(encoding="utf-8", errors="replace")[-1000:] if log.exists() else None
assert pin(cp) == start
note = f'''# Adendo: atualização v338 apareceu depois do reexame

[REAL — fonte medida] Às19:52:32 de09/09 surgiu o novo canônico: **{start['bytes']} bytes**, SHA256 `{start['sha256']}`. A versão é identificada como **v338** no `um.py:9504`. Este adendo atualiza a observação anterior, que havia lido o arquivo antes dessa escrita; a nota anterior fica preservada como histórico.

A comparação por AST com a cópia83 mede **683 arquivos embutidos**, sem nenhuma chave inédita em relação à83. Faltam exatamente as seis folhas da entrega063: `TransverseGibbsResponse`, `MixedQuadraticGibbsResponse`, `ProbeResponseRecord`, `MixedGibbsGravitationalBridge`, `FiniteCommutatorEvolution` e `SmallTimeLocalDynamics`.

Os **77 corpos Lean**, do primeiro import até o fim, são idênticos aos da bancada incorporados até entrega062. Os cabeçalhos são novos. Isso inclui `SelectionOutcomeRecord`, `SelectedGravitationalAtlas`, `GeneralAngularTensorCodec`, `CanonicalSelectorBorn`, `SelectorRecordReconstruction` e `RelativePhaseCharacter`. A fonte agora contém identificação explícita do ramo, reconstrução por seletor e fase relativa; não contém novas hipóteses de estabilidade que afastem a obstrução escrita. A codificação global e suas hipóteses permanecem as que foram examinadas.

[DECLARADO — cabeçalho] A gerência declara recompilação independente77/77, datada de10/09 no comentário. Não foi localizado nesta leitura um recibo específico dessa execução. O manifesto principal ainda traz timestamp `{proof.get('timestamp')}`, e o selo `{seal.get('timestamp')}`. Não aplicar esses recibos v337 ao código v338 novo. O arquivo `rodada_v338_stdout.txt` apareceu às19:57 e, na primeira leitura, continha somente o pedido de inscrição; a leitura desta nota registra seu pin no manifesto sem presumir estado terminal por conteúdo parcial.

Portanto, há **incorporação nova comprovada na fonte**, mas a rodada338 e a alegada compilação independente precisam de seus próprios recibos. A entrega063 permanece fora desse canônico. Nenhum original foi alterado nem qualquer `um.py` executado/importado nesta revisão.
'''
np = OUT / "ADENDO_V338_APOS_REEXAME.md"
new(np, note.encode("utf-8"))
manifest = {"created_utc": datetime.now(timezone.utc).isoformat(), "status": "V338_SOURCE_OBSERVED_NOT_RUNTIME_CERTIFIED",
            "canonical": start, "copy83": pin(op), "plan77": pin(pp), "body_equal_after_first_import": bodies,
            "missing_vs83": missing, "extra_vs83": sorted(set(a) - set(b)), "embedded_count": len(a),
            "proof_manifest": pin(proof_path), "proof_timestamp": proof.get("timestamp"),
            "seal": pin(seal_path), "seal_timestamp": seal.get("timestamp"), "observed_v338_log": log_pin,
            "observed_v338_log_tail": log_excerpt, "note": pin(np), "script": pin(Path(__file__).resolve()),
            "um_executed_or_imported": False, "originals_written": False, "compiler_executed": False}
new(OUT / "MANIFESTO_ADENDO_V338.json", (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"note": pin(np), "all77_bodies_equal": all(bodies.values()), "canonical": start, "missing": missing}))
