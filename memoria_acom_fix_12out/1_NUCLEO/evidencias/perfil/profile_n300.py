import cProfile, pstats, sys, time, tempfile, statistics, io
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'copia' / 'MEMORIA_IALD' / 'lib'))
from iald_memory import MemoryStore
SCOPE = {'house': 'IALD', 'principal': 'operator'}
OPERATOR = {'id': 'operator', 'kind': 'operator'}
AGENT = {'id': 'coordinator', 'kind': 'agent'}
TEXT = ('heartbeat sample response text ' * 40)[:1200]
def changes_for(i):
    return {'candidates': [{'id': f'c{i}', 'text': TEXT, 'statute': 'DECLARADO', 'source': {'kind': 'executor', 'ref': 'job:c%d' % i}}], 'flow': {'phase': f'cycle-{i}'}}
tmp = tempfile.mkdtemp(dir=str(Path(__file__).resolve().parents[2] / "tmp"))
root = Path(tmp) / 'state'
store = MemoryStore(root, snapshot_archive_dir=Path(tmp) / 'arq')
store.ensure_context('ctx', objective='obj', scope=SCOPE, actor=OPERATOR)
for i in range(250):
    store.transition('ctx', SCOPE, i, f'e{i}', AGENT, changes_for(i))
pr = cProfile.Profile()
times = []
pr.enable()
for i in range(250, 300):
    t = time.perf_counter(); store.transition('ctx', SCOPE, i, f'e{i}', AGENT, changes_for(i)); times.append(time.perf_counter() - t)
pr.disable()
print('median ms last 50:', round(statistics.median(times) * 1000, 2))
s = io.StringIO(); pstats.Stats(pr, stream=s).sort_stats('cumulative').print_stats(28); print(s.getvalue()[:6000])
