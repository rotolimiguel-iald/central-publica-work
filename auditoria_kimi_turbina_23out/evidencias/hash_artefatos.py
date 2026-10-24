"""sha256 (lido do arquivo, nunca de memoria) of every artifact the audit cites. Writes sha256_dos_artefatos.json next to this file."""
import hashlib
import json
from pathlib import Path

K = Path(r"C:\Users\rotol\Documents\kimi\workspace\estudo_iald_qg")
O = Path(r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\iald_orchestrator")
U = Path(r"C:\IALD\Central de Patentes\work\kimi_stack_upgrade_20261021")
B = Path(r"C:\IALD\PROGRAMA_IALD")
N = Path(r"C:\IALD\NOS_VIVO")
items = {
    "kimi/PRE_REGISTRO_BENCHMARK_TURBINA.md": K / "PRE_REGISTRO_BENCHMARK_TURBINA.md",
    "kimi/ferramentas/benchmark_turbina.py": K / "ferramentas" / "benchmark_turbina.py",
    "kimi/ferramentas/teste_dobra_envelope.py": K / "ferramentas" / "teste_dobra_envelope.py",
    "kimi/ferramentas/grep_acom_camadas.py": K / "ferramentas" / "grep_acom_camadas.py",
    "kimi/grep_acom_camadas_medicao.json": K / "grep_acom_camadas_medicao.json",
    "kimi/corpus_f9_9.json": K / "corpus_f9_9.json",
    "kimi/gabarito_f9_9.json": K / "gabarito_f9_9.json",
    "kimi/gabarito_vivo_20261020.json": K / "gabarito_vivo_20261020.json",
    "kimi/pacote_corrida_turbina.json": K / "pacote_corrida_turbina.json",
    "kimi/MODO_DE_USO_BANCADA_KIMI.md": K / "MODO_DE_USO_BANCADA_KIMI.md",
    "kimi/briefing_claude_v2_enxuto.txt": K / "briefing_claude_v2_enxuto.txt",
    "orq/canonical_memory.py pre-Kimi (.bak_20261020_191500_dobra_envelope)": O / "canonical_memory.py.bak_20261020_191500_dobra_envelope",
    "orq/canonical_memory.py Kimi (.bak_20261021_133553_...)": O / "canonical_memory.py.bak_20261021_133553_500586_b50dfd4dd6b34fe282f6257a852a7375",
    "orq/canonical_memory.py producao atual": O / "canonical_memory.py",
    "orq/nos_packet.py producao atual": O / "nos_packet.py",
    "orq/layered_retrieval.py": O / "layered_retrieval.py",
    "codex/OPERADOR.txt": U / "OPERADOR.txt",
    "codex/envelope/FINDINGS.json": U / "envelope" / "FINDINGS.json",
    "codex/envelope/test_envelope.py": U / "envelope" / "test_envelope.py",
    "codex/ranking/POLICY_PREREGISTERED_R1.json": U / "ranking" / "POLICY_PREREGISTERED_R1.json",
    "codex/benchmark_voice/ADENDO_BENCHMARK_V2.md": U / "benchmark_voice" / "ADENDO_BENCHMARK_V2.md",
    "codex/benchmark_voice/HEADER_V2.txt": U / "benchmark_voice" / "HEADER_V2.txt",
    "quadro/PROGRAMA.json.bak_20261021_kimi_titulo_f99": B / "PROGRAMA.json.bak_20261021_kimi_titulo_f99",
    "quadro/PROGRAMA.json.bak_20261021_101233_avanc": B / "PROGRAMA.json.bak_20261021_101233_avanc",
    "nos_vivo/nos_vivo.sqlite3.bak_20261021_093151": N / "nos_vivo.sqlite3.bak_20261021_093151",
    "nos_vivo/nos_vivo.sqlite3.bak_20261021_094237": N / "nos_vivo.sqlite3.bak_20261021_094237",
}
out = {}
for k, p in items.items():
    b = p.read_bytes()
    out[k] = dict(path=str(p), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
(Path(__file__).resolve().parent / "sha256_dos_artefatos.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
for k, v in out.items():
    print("%-72s %11d %s" % (k, v["bytes"], v["sha256"][:16]))
