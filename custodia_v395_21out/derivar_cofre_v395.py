# -*- coding: utf-8 -*-
"""Deriva cofre_v395.py do cofre_v394.py por trocas CONTADAS (custódia v395, 21/10/2026, sessão a7)."""
from pathlib import Path

W = Path(r"C:\IALD\Central de Patentes\work")
src = (W / "custodia_v394_19out" / "cofre_v394.py").read_text(encoding="utf-8")


def rep(a, b, n=1):
    global src
    c = src.count(a)
    assert c == n, (a[:90], c, n)
    src = src.replace(a, b)


rep('"""CUSTÓDIA CONJUNTA v392→v394 — O COFRE DA CENTRAL (19/10/2026, sessão a7, por ordem do operador).',
    '"""CUSTÓDIA v395 — O COFRE DA CENTRAL (21/10/2026, sessão a7, por ordem do operador; molde: cofre_v394.py, base = o cofre v394).\n'
    'Do molde: CUSTÓDIA CONJUNTA v392→v394 — O COFRE DA CENTRAL (19/10/2026, sessão a7, por ordem do operador).')
rep('V = OC / "um_unificado_v394"\nKV = OC / "tgl_kernel_v394"\nV391 = OC / "um_unificado_v391"\nKV391 = OC / "tgl_kernel_v391"',
    'V = OC / "um_unificado_v395"\nKV = OC / "tgl_kernel_v395"\nV391 = OC / "um_unificado_v394"   # (nome herdado do molde: é a BASE, o cofre v394)\nKV391 = OC / "tgl_kernel_v394"')
rep('ORDEM = CEN / "work" / "custodia_v394_19out" / "OPERADOR_19out_custodia_verbatim.txt"',
    'ORDEM = CEN / "work" / "custodia_v395_21out" / "OPERADOR_21out_custodia_v395_verbatim.txt"')
rep('"o cofre v394 já existe — PARAR (nada se sobrescreve)"', '"o cofre v395 já existe — PARAR (nada se sobrescreve)"')
rep('pin.startswith("972e81f22dd8cc68") and selo.get("um_version") == "v394"', 'pin.startswith("8918b17803792cf2") and selo.get("um_version") == "v395"')
rep('"gate != cofre v391 — PARAR"', '"gate != cofre v394 — PARAR"')
rep('st = (NOS / "rodada_v394_stdout.txt")', 'st = (NOS / "rodada_v395_stdout.txt")')
rep('assert "9332/9332" in st, "a escada 9332/9332 não está no stdout da v394 — PARAR"', 'assert "9451/9451" in st, "a escada 9451/9451 não está no stdout da v395 — PARAR"')
rep('p.name not in ("CUSTODY_MANIFEST.json", "NOTA_DE_CUSTODIA.md", "HANDOFF_v391_CUSTODIA.md", "rodada_v391_stdout.txt")]',
    'p.name not in ("CUSTODY_MANIFEST.json", "NOTA_DE_CUSTODIA.md", "HANDOFF_v392_CUSTODIA.md", "HANDOFF_v393_CUSTODIA.md", '
    '"HANDOFF_v394_CUSTODIA.md", "rodada_v392_stdout.txt", "rodada_v393_stdout.txt", "rodada_v394_stdout.txt")]')
rep('extra = ["rodada_v392_stdout.txt", "rodada_v393_stdout.txt", "rodada_v394_stdout.txt",\n         "HANDOFF_v392_CUSTODIA.md", "HANDOFF_v393_CUSTODIA.md", "HANDOFF_v394_CUSTODIA.md"]',
    'extra = ["rodada_v395_stdout.txt", "HANDOFF_v395_CUSTODIA.md"]')
rep('"estatuto": "DOCUMENTO (do cofre v391)"})', '"estatuto": "DOCUMENTO (do cofre v394)"})')
rep('worker e spec do cofre v391 == Nós', 'worker e spec do cofre v394 == Nós')
rep('for n in ("v392_incorporacao_manifesto.json", "v394_incorporacao_manifesto.json"):', 'for n in ("v395_incorporacao_manifesto.json",):')
rep('bancada_B3_ensaio_|delta_19out$|imp$)")', 'bancada_B3_ensaio_|delta_19out$|imp$|arvore_simulada|falso_nos$)")')
rep('"tentativas, rascunhos, cópias do kernel (o kernel vai inteiro em tgl_kernel_v394) e todo arquivo > 5 MB — ficam em "',
    '"tentativas, rascunhos, árvores simuladas e o falso Nós de teste, cópias do kernel (o kernel vai inteiro em tgl_kernel_v395) e todo arquivo > 5 MB — ficam em "')
rep('for d in ("v392", "v392_selo", "v393", "v393_exame", "v394", "v394_selo"):', 'for d in ("v395", "v395_selo"):')
rep('cadeia_de_selo_v394', 'cadeia_de_selo_v395', 4)
rep('MANIFESTO_CADEIA_DE_SELO_v394.json', 'MANIFESTO_CADEIA_DE_SELO_v395.json', 2)
rep('        copia(NOS / "tgl_kernel" / n, KV / n)\n',
    '        copia(NOS / "tgl_kernel" / n, KV / n)\n'
    '# lição da v394: o manifesto de prova também na raiz do cofre do kernel (o módulo comum dos 16 dispositivos o lê dali)\n'
    'h_pm = copia(NOS / "tgl_kernel_proof_manifest.json", KV / "tgl_kernel_proof_manifest.json")\n'
    'assert h_pm == selo["sha256"]["tgl_kernel_proof_manifest.json"], "o manifesto de prova não confere com o selo — PARAR"\n')
rep('km = {"version": "v394",', 'km = {"version": "v395",')
rep('"delta_v391_v394": {"lean_novos": len(novos), "lean_removidos": len(antes - agora),\n'
    '                          "formal_files_v391": k391.get("formal_files"), "declaracoes_v391": k391.get("teoremas_auditados")},\n'
    '      "modulos_novos_v392_v394": novos}',
    '"delta_v394_v395": {"lean_novos": len(novos), "lean_removidos": len(antes - agora),\n'
    '                          "formal_files_v394": k391.get("formal_files"), "declaracoes_v394": k391.get("declaracoes_no_axiom_report")},\n'
    '      "modulos_novos_v395": novos, "tgl_kernel_proof_manifest_sha256": h_pm}')
rep('re.search(r"_v39[234]$", k)}', 're.search(r"_v395$", k)}')
rep('mv = {"version": "v394", "custodia_conjunta": ["v392 (o cofre ficou pendente em 13/10)", "v393 (nunca custodiada)", "v394"],',
    'mv = {"version": "v395", "custodia": ["v395"],')
rep('"um_version_no_selo": "v394",', '"um_version_no_selo": "v395",')
rep('"gate_identico_ao_da_v391": True,', '"gate_identico_ao_da_v394": True,')
rep('"rodada": {"tipo": "COMPLETA", "escada": "9332/9332 (rodada_v394_stdout.txt)",', '"rodada": {"tipo": "COMPLETA", "escada": "9451/9451 (rodada_v395_stdout.txt)",')
rep('"trio; o rótulo «teoremas limpos» fica como registro de máquina"},',
    '"trio; o rótulo «teoremas limpos» fica como registro de máquina",\n'
    '                 "errata_b_da_gerencia_c1_21out": "kh_n1_cobertura_v394 passa a cobrar pisos (h2, h3, h6) e tamanho mínimo da árvore (h8); "\n'
    '                                                  "os três contratos da v394 passam a ler expected_ladder = 9451; os vereditos da v394 não mudam"},')
rep('"lean_novos_desde_v391": len(novos)},', '"lean_novos_desde_v394": len(novos)},')
rep('"registros_novos_v392_v394": regs,', '"registros_novos_v395": regs,')
rep('um_v392_b590c0aa80055e2a (a v392 que está no espelho; feito no passo zero da custódia do espelho)',
    'um_v394_972e81f22dd8cc68 (a v394 que estava no espelho; feito no passo zero da custódia do espelho)')
rep('cadeia_de_selo v392/v393/v394 filtrada em cadeia_de_selo_v395/', 'cadeia_de_selo v395 e v395_selo filtradas em cadeia_de_selo_v395/')
rep('"handoff": "HANDOFF_v392/v393/v394_CUSTODIA.md ficam no Nós e neste cofre privado",', '"handoff": "HANDOFF_v395_CUSTODIA.md fica no Nós e neste cofre privado",')
rep('print("COFRE v394: %d artefatos (0 divergentes do selo), pilar %d arquivos, emendas %d, kernel %d formais (%d .lean novos desde a v391), "',
    'print("COFRE v395: %d artefatos (0 divergentes do selo), pilar %d arquivos, emendas %d, kernel %d formais (%d .lean novos desde a v394), "')
rep('"axiom_report %d, gate = cofre v391"', '"axiom_report %d, gate = cofre v394"')
compile(src, "cofre_v395.py", "exec")
(W / "custodia_v395_21out" / "cofre_v395.py").write_text(src, encoding="utf-8")
print("ok cofre_v395.py", len(src))
