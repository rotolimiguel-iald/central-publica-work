"""Three CPU-only calls on already materialized synthetic metadata; no AI/I/O in timed region."""
import importlib.util,json,statistics,time,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
MODULE=HERE/'iald_orchestrator/layered_retrieval.py'
spec=importlib.util.spec_from_file_location('ranking_benchmark',MODULE);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
rows=[dict(id=f'fixture:{i:04d}',tipo=['pedra','lean_bancada','entrega_doc','documento_bancada'][i%4],titulo=f'Synthetic geometry control {i}',texto=('geometry algebra identity hypothesis '+str(i%17)+' ')*8,estatuto='DECLARADO_SYNTHETIC',quando=f'2026-10-{1+i%21:02d}',centrality=i%9) for i in range(600)]
measurements=[];output_hashes=[]
for _ in range(3):
 start=time.perf_counter();cpu=time.process_time();result=module.rank_nodes(rows,'geometry algebra');cpu_elapsed=time.process_time()-cpu;elapsed=time.perf_counter()-start
 assert len(result)==600 and len({r['id'] for r in result})==600
 measurements.append(dict(wall_seconds=elapsed,cpu_seconds=cpu_elapsed));output_hashes.append(hashlib.sha256(json.dumps(result,sort_keys=True).encode()).hexdigest())
assert len(set(output_hashes))==1
report=dict(status='MEASURED_CPU_SYNTHETIC_ONLY',candidates=600,runs=3,measurements=measurements,median_wall_seconds=statistics.median(r['wall_seconds'] for r in measurements),median_cpu_seconds=statistics.median(r['cpu_seconds'] for r in measurements),module_sha256=hashlib.sha256(MODULE.read_bytes()).hexdigest(),input_sha256=hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest(),stable_output_sha256=output_hashes[0],cache_scope='Rows reused in memory across 3 calls; existing SQLite FTS index untouched; this timing excludes DB retrieval/source reads, not a new persistent cache.',limits='Synthetic CPU timing only; no relevance/quality benchmark, no provider latency, no production speedup claim.',provider_calls=0,network_calls=0)
(HERE/'RANK600_BENCHMARK_R3.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report))
