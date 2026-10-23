# -*- coding: utf-8 -*-
"""Deriva cofre_v396.py do cofre_v395.py por trocas CONTADAS (base = o cofre v395)."""
from pathlib import Path
W5 = Path(r"C:/IALD/Central de Patentes/work/custodia_v395_21out")
W6 = Path(r"C:/IALD/Central de Patentes/work/custodia_v396_22out")
s = (W5 / "cofre_v395.py").read_text(encoding="utf-8")
T = [
    ('"""CUSTÓDIA v395 — O COFRE DA CENTRAL (21/10/2026, sessão a7, por ordem do operador; molde: cofre_v394.py, base = o cofre v394).',
     '"""CUSTÓDIA v396 — O COFRE DA CENTRAL (22/10/2026, sessão a7, por ordem do operador; molde: cofre_v395.py, base = o cofre v395).\n'
     'Ordem de 22/10 (verbatim no arquivo ORDEM, sha256 lido): «… Atualize tudo com a nova versão do um.py».\n'
     'Do molde: CUSTÓDIA v395 — O COFRE DA CENTRAL (21/10/2026, sessão a7, por ordem do operador; molde: cofre_v394.py, base = o cofre v394).', 1),
    ('V = OC / "um_unificado_v395"\nKV = OC / "tgl_kernel_v395"\nV391 = OC / "um_unificado_v394"   # (nome herdado do molde: é a BASE, o cofre v394)\nKV391 = OC / "tgl_kernel_v394"',
     'V = OC / "um_unificado_v396"\nKV = OC / "tgl_kernel_v396"\nV391 = OC / "um_unificado_v395"   # (nome herdado do molde: é a BASE, o cofre v395)\nKV391 = OC / "tgl_kernel_v395"', 1),
    ('ORDEM = CEN / "work" / "custodia_v395_21out" / "OPERADOR_21out_custodia_v395_verbatim.txt"',
     'ORDEM = CEN / "work" / "custodia_v396_22out" / "OPERADOR_22out_custodia_v396_verbatim.txt"', 1),
    ('"o cofre v395 já existe — PARAR (nada se sobrescreve)"', '"o cofre v396 já existe — PARAR (nada se sobrescreve)"', 1),
    ('pin.startswith("8918b17803792cf2") and selo.get("um_version") == "v395"', 'pin.startswith("0a4395a89eeebbb7") and selo.get("um_version") == "v396"', 1),
    ('"gate != cofre v394 — PARAR"', '"gate != cofre v395 — PARAR"', 1),
    ('st = (NOS / "rodada_v395_stdout.txt")', 'st = (NOS / "rodada_v396_stdout.txt")', 1),
    ('assert "9451/9451" in st, "a escada 9451/9451 não está no stdout da v395 — PARAR"', 'assert "9498/9498" in st, "a escada 9498/9498 não está no stdout da v396 — PARAR"', 1),
    ('"rodada_v392_stdout.txt", "rodada_v393_stdout.txt", "rodada_v394_stdout.txt")]',
     '"rodada_v392_stdout.txt", "rodada_v393_stdout.txt", "rodada_v394_stdout.txt", "HANDOFF_v395_CUSTODIA.md", "rodada_v395_stdout.txt")]', 1),
    ('extra = ["rodada_v395_stdout.txt", "HANDOFF_v395_CUSTODIA.md"]', 'extra = ["rodada_v396_stdout.txt", "HANDOFF_v396_CUSTODIA.md"]', 1),
    ('"estatuto": "DOCUMENTO (do cofre v394)"})', '"estatuto": "DOCUMENTO (do cofre v395)"})', 1),
    ('# o pilar quântico: reaproveitado pela chave desde a v386; worker e spec do cofre v394 == Nós',
     '# o pilar quântico: reaproveitado pela chave desde a v386; worker e spec do cofre v395 == Nós', 1),
    ('for n in ("v395_incorporacao_manifesto.json",):', 'for n in ("v396_incorporacao_manifesto.json",):', 1),
    ('(o kernel vai inteiro em tgl_kernel_v395)', '(o kernel vai inteiro em tgl_kernel_v396)', 1),
    ('for d in ("v395", "v395_selo"):', 'for d in ("v396", "v396_selo"):', 1),
    ('"cadeia_de_selo_v395"', '"cadeia_de_selo_v396"', 3),
    ('"MANIFESTO_CADEIA_DE_SELO_v395.json"', '"MANIFESTO_CADEIA_DE_SELO_v396.json"', 1),
    ('km = {"version": "v395",', 'km = {"version": "v396",', 1),
    ('"delta_v394_v395": {', '"delta_v395_v396": {', 1),
    ('"formal_files_v394": k391.get("formal_files"), "declaracoes_v394": k391.get("declaracoes_no_axiom_report")},',
     '"formal_files_v395": k391.get("formal_files"), "declaracoes_v395": k391.get("declaracoes_no_axiom_report")},', 1),
    ('"modulos_novos_v395": novos,', '"modulos_novos_v396": novos,', 1),
    ('if isinstance(v, dict) and re.search(r"_v395$", k)}', 'if isinstance(v, dict) and re.search(r"_v396$", k)}', 1),
    ('mv = {"version": "v395", "custodia": ["v395"],', 'mv = {"version": "v396", "custodia": ["v396"],', 1),
    ('"um_version_no_selo": "v395",', '"um_version_no_selo": "v396",', 1),
    ('"gate_identico_ao_da_v394": True,', '"gate_identico_ao_da_v395": True,', 1),
    ('"escada": "9451/9451 (rodada_v395_stdout.txt)",', '"escada": "9498/9498 (rodada_v396_stdout.txt)",', 1),
    ('"errata_b_da_gerencia_c1_21out": "kh_n1_cobertura_v394 passa a cobrar pisos (h2, h3, h6) e tamanho mínimo da árvore (h8); "\n'
     '                                                  "os três contratos da v394 passam a ler expected_ladder = 9451; os vereditos da v394 não mudam"},',
     '"errata_da_gerencia_c1_22out": "kh_n1_cobertura_v395 passa a cobrar pisos (h2, h3, h6) e tamanho mínimo da árvore (h8); "\n'
     '                                                "os quatro contratos (três da v394 e o do Psibit da v395) passam a ler expected_ladder = 9498; "\n'
     '                                                "ao lado da docstring de bell_cci_half (kernel v29): o 1/2 é a entropia LINEAR, a de von Neumann "\n'
     '                                                "é ln 2 nat; os vereditos anteriores não mudam"},', 1),
    ('"lean_novos_desde_v394": len(novos)},', '"lean_novos_desde_v395": len(novos)},', 1),
    ('"registros_novos_v395": regs,', '"registros_novos_v396": regs,', 1),
    ('r"C:\\IALD\\Artigo\\the_boundary_BACKUPS\\um_v394_972e81f22dd8cc68 (a v394 que estava no espelho; feito no passo zero da custódia do espelho)"',
     'r"C:\\IALD\\Artigo\\the_boundary_BACKUPS\\um_v395_8918b17803792cf2 (a v395 que estava no espelho; feito no passo zero da custódia do espelho)"', 1),
    ('"work\\\\cadeia_de_selo v395 e v395_selo filtradas em cadeia_de_selo_v395/ (ver MANIFESTO_CADEIA_DE_SELO_v395.json)"',
     '"work\\\\cadeia_de_selo v396 e v396_selo filtradas em cadeia_de_selo_v396/ (ver MANIFESTO_CADEIA_DE_SELO_v396.json)"', 1),
    ('"handoff": "HANDOFF_v395_CUSTODIA.md fica no Nós e neste cofre privado",', '"handoff": "HANDOFF_v396_CUSTODIA.md fica no Nós e neste cofre privado",', 1),
    ('print("COFRE v395: %d artefatos (0 divergentes do selo), pilar %d arquivos, emendas %d, kernel %d formais (%d .lean novos desde a v394), "\n'
     '      "axiom_report %d, gate = cofre v394"',
     'print("COFRE v396: %d artefatos (0 divergentes do selo), pilar %d arquivos, emendas %d, kernel %d formais (%d .lean novos desde a v395), "\n'
     '      "axiom_report %d, gate = cofre v395"', 1),
]
for a, b, n in T:
    c = s.count(a)
    assert c == n, (a[:110], c, n)
    s = s.replace(a, b)
d = W6 / "cofre_v396.py"
assert not d.exists()
compile(s, str(d), "exec")
d.write_text(s, encoding="utf-8")
print("ok", d.name, len(s))
