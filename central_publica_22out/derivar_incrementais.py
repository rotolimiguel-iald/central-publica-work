# -*- coding: utf-8 -*-
"""Deriva os construtores INCREMENTAIS dos públicos (22/10/2026, custódia v396: «Atualize tudo com a nova versão do um.py»), por trocas
CONTADAS a partir dos construtores que fizeram a abertura — a mesma lógica arquivo a arquivo (guarda pública, máscara, filtro das notas,
regra do Escritório), com um único acréscimo: um arquivo JÁ VISTO pelo preparo (no índice ou na lista local de exclusões) e não modificado
desde IALD_PUBLICO_DESDE (epoch) é pulado. O resto (o que mudou e o que nunca foi visto) passa pela esteira inteira, numa pasta NOVA; a
mescla no preparo é de mesclar_incremento.py. Os construtores originais não mudam."""
from pathlib import Path

W = Path(__file__).resolve().parent
CAB = ('# (DERIVADO por derivar_incrementais.py em 22/10/2026 — construtor INCREMENTAL: pula o que o preparo já viu e não mudou desde\n'
       '#  IALD_PUBLICO_DESDE; IALD_PUBLICO_JA_VISTOS = lista JSON dos caminhos já vistos. Tudo o mais é a esteira original, intacta.)\n')


def derivar(orig, novo, trocas):
    s = (W / orig).read_text(encoding="utf-8")
    for a, b, n in trocas:
        c = s.count(a)
        assert c == n, (novo, a[:90], c, n)
        s = s.replace(a, b)
    s = s.replace("# -*- coding: utf-8 -*-\n", "# -*- coding: utf-8 -*-\n" + CAB, 1)
    assert not (W / novo).exists(), novo
    compile(s, novo, "exec")
    (W / novo).write_text(s, encoding="utf-8")
    print("ok", novo, len(s))


JA = ('DESDE = float(os.environ["IALD_PUBLICO_DESDE"])\n'
      'JA = set(json.loads(Path(os.environ["IALD_PUBLICO_JA_VISTOS"]).read_text(encoding="utf-8")))\n')

derivar("construir_nucleo_publico.py", "construir_nucleo_incremental.py", [
    ('DST = Path(sys.argv[1])\n', 'DST = Path(sys.argv[1])\n' + JA, 1),
    ('    if not p.is_file():\n        continue\n    m = motivo(t)\n',
     '    if not p.is_file():\n        continue\n    if t in JA and p.stat().st_mtime < DESDE:\n        continue\n    m = motivo(t)\n', 1),
])
derivar("construir_regiao_publica.py", "construir_regiao_incremental.py", [
    ('DST = Path(sys.argv[2])\n', 'DST = Path(sys.argv[2])\n' + JA, 1),
    ('            e = p.suffix.lower()\n',
     '            e = p.suffix.lower()\n'
     '            if rel in JA:\n'
     '                try:\n'
     '                    if os.stat(lp(p)).st_mtime < DESDE:\n'
     '                        continue\n'
     '                except OSError:\n'
     '                    pass\n', 1),
])
