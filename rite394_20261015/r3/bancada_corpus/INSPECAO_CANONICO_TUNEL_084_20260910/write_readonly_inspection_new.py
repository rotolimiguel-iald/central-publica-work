from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import os

ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt")
OUT = Path(__file__).resolve().parent
CANON = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
BEFORE = {}
DATA = {}
def pin(path):
    p = Path(path); raw = p.read_bytes(); st = p.stat()
    return {"path": p.as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
            "mtime_utc": datetime.fromtimestamp(st.st_mtime, timezone.utc).isoformat()}
def read(path):
    p = Path(path); raw = p.read_bytes(); info = pin(p)
    assert len(raw) == info["bytes"] and hashlib.sha256(raw).hexdigest() == info["sha256"]
    BEFORE[info["path"]] = info; DATA[info["path"]] = raw
    return raw
def new(name, raw):
    p = OUT / name
    assert p.resolve().is_relative_to(ROOT.resolve()) and not p.exists() and raw
    tmp = p.with_name(p.name + ".tmp_" + datetime.now().strftime("%H%M%S_%f"))
    with tmp.open("xb") as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    assert tmp.read_bytes() == raw
    tmp.rename(p)
    assert p.read_bytes() == raw
    return pin(p)
def listing(path, limit):
    rows = []
    for p in Path(path).iterdir():
        st = p.stat()
        rows.append({"name": p.name, "directory": p.is_dir(), "bytes": st.st_size if p.is_file() else None,
                     "mtime_utc": datetime.fromtimestamp(st.st_mtime, timezone.utc).isoformat()})
    return sorted(rows, key=lambda r: r["mtime_utc"], reverse=True)[:limit]

read(Path(__file__))
prior = json.loads(read(ROOT / "REEXAME_SUFICIENCIA_083_20260910/ESTADO_CANONICO_083.json"))
raw = read(CANON / "um.py"); source = raw.decode("utf-8-sig")
nodes = [n for n in ast.parse(source).body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "_EMBEDDED_KERNEL_FILES" for t in n.targets)]
assert len(nodes) == 1
embedded = ast.literal_eval(nodes[0].value)
seal = json.loads(read(CANON / "um_absoluto_selo.json"))
read(CANON / "tgl_kernel_proof_manifest.json")
stdout = read(CANON / "rodada_v338_stdout.txt").decode("utf-8-sig")
read(Path(r"C:\IALD\Artigo\Haja_Luz\CLAUDE.md"))
read(ROOT / "TUNEL/TUNEL_PROTOCOLO.md")
inventory = {"canonical_recent_entries": listing(CANON, 25),
             "tunnel_to_chatgpt_recent_entries": listing(ROOT / "TUNEL/PARA_CHATGPT", 8),
             "tunnel_from_chatgpt_recent_entries": listing(ROOT / "TUNEL/DO_CHATGPT", 5)}
latest = max((p for p in (ROOT / "TUNEL/PARA_CHATGPT").iterdir() if p.is_file()), key=lambda p: p.stat().st_mtime)
read(latest)
old = {Path(p["path"]).as_posix(): p for p in prior["pins"]}
comparisons = []
for name in ("um.py", "um_absoluto_selo.json", "tgl_kernel_proof_manifest.json", "rodada_v338_stdout.txt"):
    key = (CANON / name).as_posix()
    comparisons.append({"path": key, "bytes_unchanged": BEFORE[key]["bytes"] == old[key]["bytes"],
                        "sha256_unchanged": BEFORE[key]["sha256"] == old[key]["sha256"]})
names = [m["module"] for m in prior["modules"]]
assert len(names) == len(set(names)) == 98
absent = [name for name in names if "TGLExt/" + name + ".lean" not in embedded]
lines = source.splitlines()
entry = next(i for i, line in enumerate(lines, 1) if line.strip() == '"TGLExt/SelectedGravitationalAtlas.lean":')
anchors = []
for i, line in enumerate(lines, 1):
    if entry <= i <= entry + 40 and any(w in line for w in ("[INPUT]", "correspondencia fisica", "alem da classe", "leis de area", "condicionado a area")):
        anchors.append({"artifact": "um.py", "line": i, "text": line.strip()})
    if "GOROFF_SAGNOTTI_WALL_TYPED_OPEN" in line:
        anchors.append({"artifact": "um.py", "line": i, "text": line.strip()})
for i, line in enumerate(DATA[(CANON / "um_absoluto_selo.json").as_posix()].decode("utf-8-sig").splitlines(), 1):
    if any('"' + key + '"' in line for key in ("qg_closure_verdict", "renormalization_wall_verdict", "fail_closed_selftest")):
        anchors.append({"artifact": "um_absoluto_selo.json", "line": i, "text": line.strip()})
for n in (440, 777, 1074, 1159, 1211):
    anchors.append({"artifact": "rodada_v338_stdout.txt", "line": n, "text": stdout.splitlines()[n-1].strip()})
after = {key: pin(key) for key in BEFORE}
assert all(after[key] == info for key, info in BEFORE.items())
unchanged = all(p["bytes_unchanged"] and p["sha256_unchanged"] for p in comparisons)
stamp = datetime.now(timezone.utc).isoformat()
md = f"""# Inspeção dirigida do canônico e do túnel

[REAL — leitura estática, {stamp}] Os quatro artefatos canônicos examinados têm os mesmos bytes/hash do snapshot083: **{unchanged}**. A leitura AST/literal_eval encontrou **{len(embedded)} arquivos embutidos** e **{98-len(absent)}/98 módulos** da lista de comparação; permanecem **{len(absent)} ausentes**. O selo confere com o hash atual de um.py: **{seal['sha256']['um.py'] == hashlib.sha256(raw).hexdigest()}**.

A conclusão é limitada ao caminho C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós e às duas vias conhecidas do túnel. Nenhuma sucessora da v338 nem rodada posterior apareceu nos nomes/metadados pertinentes consultados. Isso não nega avanços em outra cópia ou em preparação na sessão codificadora. Não houve busca por outras casas, processos, árvores recursivas de build ou pelo computador inteiro.

## Instruções e acesso

Foram lidas as instruções iniciais (160 linhas) de C:/IALD/Artigo/Haja_Luz/CLAUDE.md, as instruções globais fornecidas pelo operador e o protocolo do túnel. O hash integral de CLAUDE é apenas pin de proveniência; não representa leitura integral de seus adendos. As tentativas de ler C:/IALD/AGENTS.md e C:/IALD/Artigo/Haja_Luz/AGENTS.md retornaram caminho inexistente, inclusive com leitura escalada. A enumeração posterior localizou CLAUDE.md. O primeiro inventário da casa foi negado pelo sandbox; a repetição escalada somente leitura teve sucesso. Nenhuma falha foi convertida em resultado favorável.

## Fonte e execução histórica

[REAL — fonte] O bloco SelectedGravitationalAtlas começa na linha **{entry}** de um.py. Seu cabeçalho explicita registro/origem física como INPUT e mantém correspondência seletor-registro, matéria/conservação/área dos mesmos dados, atlas físico compatível, anomalias e UV como OPEN. A reconstrução de Einstein é condicionada às leis de área e conservação. A ausência de delta não paga qualquer dessas hipóteses.

[DECLARADO — vereditos existentes] O selo mantém:
- {seal['qg_closure_verdict']}
- {seal['renormalization_wall_verdict']}

[REAL — evidência histórica lida] rodada_v338_stdout.txt é a saída mais recente identificada no diretório pertinente. Seu mtime UTC está no recibo. Contém afirmações estratificadas por versão: as cinco flags aparecem imóveis em passagens antigas e mudam posteriormente na linha1211. Essas passagens não são tratadas isoladamente como estado corrente. Avisos de interações/anomalias na linha440 e de perturbações gerais na linha1159 são lidos junto ao cabeçalho atual e ao selo. A inspeção não recompilou Lean nem reproduziu a rodada. Não apareceu nova evidência de QME, cancelamento universal de anomalias ou solução UV na comparação desses arquivos idênticos; não se pretende uma auditoria matemática completa desses programas.

[REAL — engenharia] Permanecem ausentes no embutido os módulos abaixo. Isso é diferente de ausência dos resultados na bancada ou de falta de compilações em cópias verificadas:
""" + "\n".join("- " + name for name in absent) + """

## Túnel e preparação

A via PARA_CHATGPT termina por mtime em ORDEM_010_horizontes_concretos_aperiodico_e_o_relogio_apos_a_obstrucao.md, de 06/09. A via DO_CHATGPT contém entregas recentes da bancada, incluindo a083. Entrega de bancada não é recibo de incorporação pela gerência. Os inventários do recorte e os mtimes UTC estão no recibo. A lista de 25 entradas canônicas recentes inclui capturas de build/auditoria da rodada v338 e memórias posteriores por um segundo; não apresenta preparação nova nesse recorte. Não foram procuradas cópias alternativas fora dos caminhos pertinentes.

## Referências verificadas
""" + "\n".join(f"- {a['artifact']}:{a['line']} — {a['text']}" for a in anchors) + """

[REAL — custódia] Todos os arquivos lidos e pinados permaneceram idênticos antes/depois nesta inspeção. Só foram criados novos artefatos nesta pasta Chatgpt. Nenhum um.py, fonte congelada, memória canônica, Atlas, selo ou saída histórica foi executado, importado ou alterado. O recibo registra controles documentais e AST; zero controles matemáticos, CAS ou Lean novos.
"""
note = new("PARECER_CANONICO_E_TUNEL_084.md", md.encode("utf-8"))
record = {"status": "READ_ONLY_STABLE_NO_CANONICAL_DELTA_VS_083" if unchanged else "CANONICAL_DELTA_DETECTED",
          "created_utc": stamp, "comparisons": comparisons, "embedded_files": len(embedded),
          "baseline_modules": 98, "present": 98-len(absent), "absent": absent, "anchors": anchors,
          "inventory": inventory, "sources_before": list(BEFORE.values()), "sources_after": list(after.values()),
          "all_sources_unchanged": True, "note": note, "um_executed_or_imported": False,
          "originals_written": False, "new_math_or_lean_runs": 0,
          "scope": "Bounded canonical and two tunnel directories; no recursive scan of builds or other houses."}
receipt = new("REGISTRO_INSPECAO_CANONICO_084.json", (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"status": record["status"], "present": record["present"], "absent_count": len(absent),
                  "sources_preserved": len(BEFORE), "note": note, "receipt": receipt}, ensure_ascii=False))

