# -*- coding: utf-8 -*-
"""Custódia v393+v394 (19/10/2026, sessão a7): a guarda do selo ganha a regra das FONTES PINADAS. Uma cópia de selo antigo que mora em
fontes_pinadas/ (insumo que um registro do um.py relê por sha256, p.ex. a bateria pré-selo da v392 guarda o selo da v391) não é o selo
DESTA pasta: não descreve artefatos ao lado. A guarda deixa de lê-la como selo e passa a exigir dela o que vale para insumo pinado —
estar no MAPA_FONTES_PINADAS.json com publicado=True, e o disco E o blob do git iguais ao sha256 do pino. Fail-closed: cópia fora do mapa,
ou com outro byte, é erro. Backup de bytes; temporário; compile; troca."""
import os, time

P = r"C:\IALD\Artigo\the_boundary\tools\guarda_do_selo.py"
raw = open(P, "rb").read()
s = raw.decode("utf-8")
MARCA = "v3 (19/10/2026) — a terceira licao"
if MARCA in s:
    print("já aplicado"); raise SystemExit
pares = [
    ("Uso:  python tools/guarda_do_selo.py\n\"\"\"",
     "v3 (19/10/2026) — a terceira licao (custodia v393+v394): o espelho passou a publicar as FONTES PINADAS que os\n"
     "registros do um.py releem por caminho absoluto (fontes_pinadas/, com mapa). Uma delas e' uma COPIA do selo da\n"
     "v391 (insumo da bateria pre-selo da v392). Copia de selo dentro de fontes_pinadas/ nao e' o selo da pasta: a\n"
     "guarda a confere como insumo pinado — no MAPA_FONTES_PINADAS.json, publicada, disco E blob = o sha256 do pino.\n"
     "\n"
     "Uso:  python tools/guarda_do_selo.py\n\"\"\""),
    ("    selos = sorted(RAIZ.rglob(\"um_grande_atrator_selo.json\")) + sorted(\n"
     "        RAIZ.rglob(\"um_absoluto_selo.json\"))  # renome v209: os dois nomes valem\n",
     "    selos = sorted(RAIZ.rglob(\"um_grande_atrator_selo.json\")) + sorted(\n"
     "        RAIZ.rglob(\"um_absoluto_selo.json\"))  # renome v209: os dois nomes valem\n"
     "    # v3 (19/10/2026): copia de selo em fontes_pinadas/ e' insumo pinado, nao selo da pasta — conferida pelo mapa\n"
     "    pinadas = [s_ for s_ in selos if \"fontes_pinadas\" in s_.relative_to(RAIZ).parts]\n"
     "    selos = [s_ for s_ in selos if s_ not in pinadas]\n"
     "    for s_ in pinadas:\n"
     "        partes = s_.relative_to(RAIZ).parts\n"
     "        mapa_p = RAIZ.joinpath(*partes[:partes.index(\"fontes_pinadas\") + 1]) / \"MAPA_FONTES_PINADAS.json\"\n"
     "        rel_s = s_.relative_to(RAIZ).as_posix()\n"
     "        try:\n"
     "            ents = [e for e in json.loads(mapa_p.read_text(encoding=\"utf-8\"))[\"fontes\"]\n"
     "                    if e.get(\"publicado\") and e.get(\"caminho_no_espelho\") == rel_s]\n"
     "        except (OSError, KeyError, json.JSONDecodeError) as e:\n"
     "            print(f\"  ! mapa das fontes pinadas ilegivel para {rel_s}: {e}\")\n"
     "            erros += 1\n"
     "            continue\n"
     "        pinos = {e.get(\"sha256\") for e in ents}\n"
     "        if len(pinos) != 1 or None in pinos:\n"
     "            print(f\"  ! COPIA DE SELO EM fontes_pinadas FORA DO MAPA (ou com pinos divergentes): {rel_s}\")\n"
     "            erros += 1\n"
     "            continue\n"
     "        pino = pinos.pop()\n"
     "        if sha256(s_) != pino or sha256_blob(rel_s) != pino:\n"
     "            print(f\"  ! COPIA DE SELO EM fontes_pinadas DIVERGE DO PINO (disco ou blob): {rel_s}\")\n"
     "            erros += 1\n"
     "            continue\n"
     "        print(f\"[insumo pinado] {rel_s}: copia de selo conferida contra o pino do mapa (disco E blob do git)\")\n"),
]
crlf = b"\r\n" in raw   # a guarda está em CRLF no disco: as trocas respeitam o fim de linha do arquivo
for a, b in pares:
    if crlf:
        a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert s.count(a) == 1, (s.count(a), a[:70])
    s = s.replace(a, b)
compile(s, P, "exec")
open(P + ".bak_" + time.strftime("%Y%m%d_%H%M%S"), "wb").write(raw)
open(P + ".tmp", "wb").write(s.encode("utf-8"))
assert os.path.getsize(P + ".tmp") > len(raw)
os.replace(P + ".tmp", P)
print("ok", len(raw), "->", os.path.getsize(P))
