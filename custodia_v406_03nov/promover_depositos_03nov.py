# -*- coding: utf-8 -*-
"""03/11/2026 06:5x, gerencia c1 (a unica que escreve no indice): triagem da fila da memoria.
(1) A troca da linha da custodia v406 no MEMORY.md (CUSTODIADO -> PUBLICADA), ato manual da gerencia como na v405: a ANTIGA e a NOVA sao lidas do proprio deposito do G1
    (claude-site/20261103_031248_custodia_v406_indice_publicada), a ANTIGA tem de estar UMA vez, o indice fica <= 195 linhas e <= 24.000 B, backup de BYTES, temporario -> os.replace,
    e `memoria.py pinar` re-pina. A ANTIGA vai ao MEMORY_2.md verbatim pela promocao dos dois depositos de indice para la' (o corpo deles traz ANTIGA e NOVA), como na v405.
(2) `memoria.py promover` para cada deposito pendente, no alvo que o depositante sugeriu (precedente: os 9 da v405 foram PROMOVIDOS), mais os de 02/11 que ficaram:
    a regra do operador «as patentes sao lidas em conjunto» ganha topico novo e UMA linha no indice (secao Escritorio e PI); as decisoes do ACOM vao ao epct-protocolo-15.md;
    a release v405 do app ao topico do app; a preparacao da v406 ao topico do fechamento. Cada promocao exige MEMORIA_GERENCIA=claude-c1 e o indice igual ao pino; para em qualquer rc != 0.
Nada aqui toca um.py, selo, cofre, gate ou o ar. Escrito pelo Write."""
import json, os, re, subprocess, sys, time
from pathlib import Path
MEMD = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"); FILA = MEMD / "fila"; MEM = MEMD / "MEMORY.md"
PY = r"C:\Python314\python.exe"; ENV = dict(os.environ, MEMORIA_GERENCIA="claude-c1")
TS = time.strftime("%Y%m%d_%H%M%S")


def memoria(*args):
    q = subprocess.run([PY, "-X", "utf8", str(FILA / "memoria.py"), *args], cwd=str(FILA), env=ENV, capture_output=True, timeout=300)
    out = (q.stdout or b"").decode("utf-8", "replace").strip(); err = (q.stderr or b"").decode("utf-8", "replace").strip()
    print("memoria.py %s -> rc %d %s" % (" ".join(args[:2]), q.returncode, (out or err)[:260].replace("\n", " ")))
    return q.returncode, out, err


# ---------- (1) a troca da linha no indice ----------
dep = (FILA / "depositos" / "claude-site" / "20261103_031248_custodia_v406_indice_publicada.md").read_text(encoding="utf-8")
m_a = re.search(r"^ANTIGA:\r?\n(- .+)$", dep, re.M); m_n = re.search(r"^NOVA:\r?\n(- .+)$", dep, re.M)
assert m_a and m_n, "o deposito nao traz ANTIGA/NOVA"
ANTIGA, NOVA = m_a.group(1).rstrip("\r"), m_n.group(1).rstrip("\r")
assert "PUBLICADA" in NOVA and "42f3b0c9" in NOVA and "a381c4d1" in NOVA and "ddcb91930982d614" in NOVA
b = MEM.read_bytes(); txt = b.decode("utf-8")
assert txt.count(ANTIGA) == 1, "a linha ANTIGA nao esta' UMA vez no MEMORY.md (%d)" % txt.count(ANTIGA)
novo = txt.replace(ANTIGA, NOVA).encode("utf-8")
n_lin = novo.count(b"\n") + (0 if novo.endswith(b"\n") else 1)
assert len(novo) <= 24000 and n_lin <= 195, "o indice estouraria: %d B, %d linhas" % (len(novo), n_lin)
bak = MEM.with_name(MEM.name + ".bak_" + TS + "_c1_troca_v406"); open(bak, "xb").write(b); assert bak.read_bytes() == b
tmp = MEM.with_name(MEM.name + ".tmp_" + TS); open(tmp, "xb").write(novo); os.replace(tmp, MEM)
assert MEM.read_bytes() == novo
print("MEMORY.md: %d -> %d B, %d linhas; backup %s" % (len(b), len(novo), n_lin, bak.name))
rc, out, err = memoria("pinar"); assert rc == 0, "pinar falhou: %s %s" % (out, err)

# ---------- (2) as promocoes ----------
PATENTES_LINHA = ("- **[AS PATENTES SÃO LIDAS EM CONJUNTO (02/11)](patentes-leitura-em-conjunto-02nov.md)** — **regra do operador**: a proteção é da família; o que falta num pedido "
                  "procura-se nos demais antes de qualquer ato; limite medido: primeiro o próprio depósito original [LEGAL]")
PLANO = [
    ("claude-site/20261103_031248_custodia_v406_indice_publicada", ["--para", "MEMORY_2.md"]),
    ("claude-site/20261103_031123_custodia_v406_indice_custodiado", ["--para", "MEMORY_2.md"]),
    ("claude-site/20261103_031121_custodia_v406_site_sessao_estado", ["--para", "site-sessao-estado.md"]),
    ("claude-site/20261103_031122_custodia_v406_central_estado", ["--para", "central-de-patentes-estado.md"]),
    ("claude-site/20261103_031122_custodia_v406_dispositivos", ["--para", "dispositivos-formula-completa.md"]),
    ("claude-site/20261103_031122_custodia_v406_fronteira_teorica", ["--para", "tgl-fronteira-teorica.md"]),
    ("claude-site/20261103_031123_custodia_v406_handoff_custodiado", ["--para", "handoff-v406-custodia.md"]),
    ("claude-site/20261103_031248_custodia_v406_publicada_handoff", ["--para", "handoff-v406-custodia.md"]),
    ("claude-site/20261103_031248_custodia_v406_publicada_central", ["--para", "central-de-patentes-estado.md"]),
    ("claude-site/20261102_093552_patentes-leitura-em-conjunto-02nov", ["--para", "novo:patentes-leitura-em-conjunto-02nov", "--linha-indice", PATENTES_LINHA, "--secao", "Escritório e PI",
                                                                        "--descricao", "Regra do operador (02/11/2026): as patentes da casa são lidas em conjunto, como família; o que falta num pedido procura-se nos demais antes de tratar como desprotegido; limite medido (ACOM, 02/11): primeiro o próprio depósito original, depois a família [LEGAL]"]),
    ("claude-site/20261102_110401_decisoes-patentes-02nov", ["--para", "epct-protocolo-15.md"]),
    ("claude-site/20261102_110857_acom-primeira-patente-02nov", ["--para", "epct-protocolo-15.md"]),
    ("claude-site/20261102_111357_acom-pedido-posterior-02nov", ["--para", "epct-protocolo-15.md"]),
    ("claude-site/20261102_084707_app-v405-instalado-02nov", ["--para", "app-ciencia-propria-v395-24out.md"]),
    ("claude-prep-v406/20261102_232631_v406-preparada-02nov", ["--para", "construir-tudo-o-fechamento-02nov.md"]),
]
feitos = []
for dep_id, args in PLANO:
    rc, out, err = memoria("promover", dep_id, *args)
    if rc != 0:
        print("PAROU em", dep_id, "\n", out[-800:], "\n", err[-800:]); break
    feitos.append(dep_id)
print("promovidos: %d de %d" % (len(feitos), len(PLANO)))
rc, out, err = memoria("verificar"); print("verificar rc", rc)
b2 = MEM.read_bytes(); print("MEMORY.md agora: %d B, %d linhas" % (len(b2), b2.count(b"\n")))
Path(r"C:\IALD\Central de Patentes\work\custodia_v406_03nov\RECIBO_TRIAGEM_FILA_03nov.json").write_text(json.dumps({
    "quando": time.strftime("%Y-%m-%dT%H:%M:%S"), "troca_indice": {"antiga": ANTIGA, "nova": NOVA, "backup": bak.name, "bytes": len(novo), "linhas": n_lin},
    "promovidos": feitos, "faltaram": [d for d, _ in PLANO if d not in feitos], "verificar_rc": rc, "memory_bytes_final": len(b2)}, ensure_ascii=False, indent=1), encoding="utf-8")
sys.exit(0 if len(feitos) == len(PLANO) and rc == 0 else 1)
