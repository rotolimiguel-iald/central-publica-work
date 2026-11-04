# -*- coding: utf-8 -*-
"""Ajustes da v406 sobre as ferramentas copiadas da v405 (registro do que mudou; cada troca exige exatamente uma ocorrencia).
R3-1, R3-2 (LICOES_v405.md), janela P2 deslizada com limites/diz/nao_diz mantidos na capsula compacta (ORDEM_004), rotulos de ator, textos de versao.
Hash e commit lidos por script: o pino do um.py vem do selo do cofre; o commit foi dado pela gerencia (ORDEM_004) e e' conferido pelo preflight."""
import hashlib
import json
import shutil
from pathlib import Path

W = Path(__file__).resolve().parent
VAULT = Path(r"C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v406")
COMMIT = "a381c4d147099b04dfceecf9c7db4a8cea47fb42"
OPERADOR = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_03nov_prossigamos_com_tudo_ratifico_tudo_orquestrador_claude_app_readme_pinado_teste_d_verbatim.txt")
feito = []


def troca(arq, pares):
    p = W / arq
    t = p.read_bytes().decode("utf-8")
    for velho, novo in pares:
        assert t.count(velho) == 1, (arq, t.count(velho), velho[:90])
        t = t.replace(velho, novo)
    p.write_bytes(t.encode("utf-8"))
    feito.append(arq)


# RELEASE.json (release, commit, pino do um.py lido do selo do cofre)
seal = json.loads((VAULT / "um_absoluto_selo.json").read_bytes())
assert seal["um_version"] == "v406" and seal["fail_closed_selftest"] == "FAIL_CLOSED_SELFTEST_PASSED"
pino = seal["sha256"]["um.py"]
assert hashlib.sha256((VAULT / "um.py").read_bytes()).hexdigest() == pino
(W / "app" / "RELEASE.json").write_text(json.dumps({"release": "v406", "espelho_commit": COMMIT, "um_py_sha256": pino}, indent=2), encoding="utf-8")
feito.append("app/RELEASE.json")

troca("release_cfg.py", [
    ("OWNER = 'claude-gerencia-a7'", "OWNER = 'claude-app-orquestrador'"),
    ("BUILDER = 'opus-app-v405-construtor'", "BUILDER = 'claude-app-orquestrador'"),
    ("SHARED_P2_SUFFIXES = ('_v401', '_v402', '_v403', '_v404', '_v405')",
     "# 03/11/2026 (v406, decisao da gerencia c1, ORDEM_004): a janela DESLIZA. Sai _v401 (o mais antigo); entram os novos _v406. _v402 so' sai se o shared nao couber na menor folga medida\n"
     "# (DeepSeek, reserva declarada 148656). Os topicos que SAEM da janela viram capsula compacta, mas MANTEM os literais limites/diz/nao_diz (a recusa F2 da v404 foi pela perda deles):\n"
     "# P2_RETIRED_LITERAL_SUFFIXES e' lido por prepare.py e aplicado em fit_memory.compact.\n"
     "SHARED_P2_SUFFIXES = ('_v402', '_v403', '_v404', '_v405', '_v406')\n"
     "P2_RETIRED_LITERAL_SUFFIXES = ('_v401',)"),
])
troca("app/build/haiku_codec.py", [
    ("KEEP_FLAG = re.compile(r'(?:^|_)H[123](?:_|$)|discharg|condition|verified|verification', re.I)",
     "KEEP_FLAG = re.compile(r'H[123]|discharg|condition|verif', re.I)  # R3-1 (v406): sem delimitadores; medido em v406: 16 nomes voltam ao literal (905 B), 2 deles 'th2' por causa de re.I"),
    ("'dessa fonte, fetch_tgl id=resultado_publicado_integral com offset igual ao do resultado menos 2000. Nome muito genérico '",
     "'dessa fonte, fetch_tgl id=resultado_publicado_integral com offset igual ao do resultado menos 2000 e max_chars 4500. Nome muito genérico '"),
])
troca("app/build/fit_memory.py", [
    ("def compact(text, source, unchanged):", "def compact(text, source, unchanged, literal_suffixes=()):"),
    ("        for key in ('theorem','all_verified','does_not_gate_core'):\n",
     "        # v406: topicos que saem da janela P2 (literal_suffixes) mantem limites/diz/nao_diz literais na capsula (criterio da revisao, F2 da v404)\n"
     "        for key in ('theorem','all_verified','does_not_gate_core')+(('limites','diz','nao_diz') if literal_suffixes and name.endswith(tuple(literal_suffixes)) else ()):\n"),
])
troca("app/prepare.py", [
    ("shared,pr=compact(shared,result,sr['reused_identical_topics']+_extra)",
     "shared,pr=compact(shared,result,sr['reused_identical_topics']+_extra,literal_suffixes=getattr(release_cfg,'P2_RETIRED_LITERAL_SUFFIXES',()))"),
    ("'extra_compaction_requested':len(_extra)}})",
     "'extra_compaction_requested':len(_extra),'retired_literal_suffixes':list(getattr(release_cfg,'P2_RETIRED_LITERAL_SUFFIXES',()))}})"),
])
troca("task.py", [
    ("Mapa de rotas: consulta \"app ciencia v405 haiku55 compactacao base\" (0 rotas) em 02/11 (1629 registros). Pipeline de referencia: work/iald_v404_20261029 (instalada v404, aceita por revisor independente). Mudanca desta release: base compacta do haiku55 redesenhada no codec (licao da v404).",
     "Mapa de rotas: consulta \"app release v406 ciencia haiku55 janela P2 shared\" (0 rotas) em 03/11 (1748 registros). Pipeline de referencia: work/iald_v405_20261102 (instalada v405, aceita por revisores distintos do construtor). Mudancas desta release: R3-1 e R3-2 da LICOES_v405, janela P2 do shared deslizada (ORDEM_004 da gerencia c1) com limites/diz/nao_diz mantidos na capsula compacta."),
])
troca("run_construcao.sh", [
    ("Construcao da release do app (v405)", "Construcao da release do app (v406)"),
    ("BLD=opus-app-v405-construtor", "BLD=claude-app-orquestrador"),
])

# builder_measurements.py nao se remenda: foi reescrito (parametrizado por app/RELEASE.json) em builder_measurements.py; exercita_busca.py muda so' a semente
troca("exercita_busca.py", [
    ("random.Random(20261102)", "random.Random(20261103)"),
    ('"semente 20261102"', '"semente 20261103"'),
])

# a ordem do operador, byte a byte, como ORDEM_DO_OPERADOR.txt e ORIGINAL.txt (task.py exige bytes identicos)
raw = OPERADOR.read_bytes()
for n in ("ORDEM_DO_OPERADOR.txt", "ORIGINAL.txt"):
    with (W / n).open("xb") as f:
        f.write(raw)
    assert (W / n).read_bytes() == raw
feito += ["ORDEM_DO_OPERADOR.txt", "ORIGINAL.txt"]
print(json.dumps({"ajustados": feito, "pino_um_py": pino[:16], "commit": COMMIT[:12], "ordem_do_operador_sha16": hashlib.sha256(raw).hexdigest()[:16]}, ensure_ascii=False))
