# -*- coding: utf-8 -*-
"""r3 (a r2 nao chegou a ser submetida): a receita de recuperacao medida vai na capsula; a r2 e guardada em superseded_r2/ (movida, nao apagada);
nasce a evidencia irma do estado da custodia (achado F3 do parecer r1). sources_verified.json e app/PUBLIC_GIT_BINDING.json ficam: as fontes nao mudaram."""
import hashlib
import json
import shutil
from pathlib import Path

W = Path(__file__).resolve().parent
S = W / "superseded_r2"

p = W / "app" / "build" / "haiku_codec.py"
t = p.read_bytes().decode("utf-8")
a = ("'O critério é o nome, não o conteúdo. Para recuperar um nome: search_tgl com o nome exato e limit 5; fetch_tgl '\n"
     "                   'id=resultado_publicado_integral no offset de cada resultado dessa fonte. Não são contagem de teoremas.'}\n")
b = ("'O critério é o nome, não o conteúdo. Para recuperar um nome: search_tgl com o nome exato e limit 5; depois, para cada resultado '\n"
     "                   'dessa fonte, fetch_tgl id=resultado_publicado_integral com offset igual ao do resultado menos 2000. Nome muito genérico '\n"
     "                   'pode exigir outra consulta. Não são contagem de teoremas.'}\n")
assert t.count(a) == 1
p.write_bytes(t.replace(a, b).encode("utf-8"))

p = W / "exercita_busca.py"
t = p.read_bytes().decode("utf-8")
pares = [("que a capsula ensina: nome exato, limit 5, fetch_tgl no offset de cada resultado da fonte.",
          "que a capsula ensina: nome exato, limit 5, fetch_tgl no offset de cada resultado da fonte menos 2000."),
         ("amostra = random.Random(1102).sample(nomes, 120)\n", "amostra = random.Random(20261102).sample(nomes, 700)\n"),
         ('{"id": x["id"], "offset": x["offset"], "max_chars": 4500}', '{"id": x["id"], "offset": max(0, x["offset"] - 2000), "max_chars": 4500}'),
         ('"semente 1102"', '"semente 20261102"')]
for x, y in pares:
    assert t.count(x) == 1, x
    t = t.replace(x, y)
p.write_bytes(t.encode("utf-8"))

ITENS = ["app/BUILT.json", "app/DATA_PLAN.json", "app/DELIVERY_PREPARED.json", "app/NATIVE_COUNTS_COMPLETE.json", "app/PREPARED_BINDING.json",
         "app/RUNTIME_BASELINE.json", "app/packages", "app/science", "install_plan.json", "BUILDER_MEASUREMENTS.json", "validation/final_checks.json"]
ITENS += [q.name for q in W.glob("*_stdout.txt")] + [q.name for q in W.glob("*_stderr.txt")]
ITENS += [q.relative_to(W).as_posix() for q in (W / "app").glob("native_prefix*")]
assert not S.exists()
for rel in ITENS:
    d = S / rel
    d.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(W / rel), str(d))
(S / "MOVED_MANIFEST.json").write_text(json.dumps({"reason": "r2 nunca submetida; superada pela r3 so na frase de recuperacao da capsula, medida (1 falha em 700)", "moved_items": ITENS}, ensure_ascii=False, indent=1), encoding="utf-8")

plano = Path(r"C:\IALD\Central de Patentes\work\custodia_G1\PLANO_v405.json")
d = json.loads(plano.read_bytes())
passos = d.get("passos") or []
estado = {
    "status": "CUSTODIA_V405_EM_CURSO_NAO_CONCLUIDA",
    "plano_g1": {"path": str(plano), "sha256": hashlib.sha256(plano.read_bytes()).hexdigest()},
    "leitura": "O selo, o cofre e o commit do espelho da v405 estao custodiados e conferidos (sources_verified.json). A custodia como processo segue em curso: o plano da G1 nao esta completo.",
    "campos_do_plano": {k: d.get(k) for k in ("versao", "corrente", "relacao_espelho", "contagem", "completo", "pendentes", "pendentes_do_operador") if k in d},
}
(W / "CUSTODIA_EM_CURSO_v405.json").write_text(json.dumps(estado, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(estado["campos_do_plano"], ensure_ascii=False)[:500])
print("R3_PRONTA", len(ITENS))
