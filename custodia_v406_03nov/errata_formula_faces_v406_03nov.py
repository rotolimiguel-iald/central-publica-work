# -*- coding: utf-8 -*-
"""03/11/2026 02:4x, gerencia c1: o C8 da G1 aplicou a camada v406 ao modulo comum dos 16 dispositivos (patents/_formula_completa/tgl_formula_completa.py) e o modulo
deixou de rodar (fail-closed): as camadas v395 e v396, escritas a mao na epoca, congelaram «a face do psion e' dita condicional» (status CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE)
e «a face de Fock e' dita condicional» (status CONDITIONAL... e inhabitant_exhibited False). Era o estado de v395 a v405. Desde a v406 as duas faces sao LIDAS do kernel do rito:
status INHABITED_BY_physicalFockCertificate_V406, inhabitant_exhibited True, com reading_v395/reading_v396 guardando a leitura antiga e errata E14 ao lado no um.py; o registro
selado fechamento_v406 confere (certificate_inhabited True). Conserto AO LADO, no molde da ERRATA AO LADO da custodia v389 (l.746 do mesmo modulo): a linha original fica em
comentario, intacta; aceita-se TAMBEM o estado lido do kernel, com as condicoes ditas; os nomes das checagens nao mudam (os results.json dos dispositivos os citam); o estatuto
ganha a frase ao lado. Aplicado pelo mecanismo do G1 (custodia_g1.patches.aplicar_em_arquivo: backup de BYTES, CRLF, py_compile, os.replace) e CONFERIDO rodando o modulo como
o C8 faz; se nao rodar, rc 1 (os backups ficam; a gerencia decide). Nada toca um.py, selo, core, cofre ou gate; validade no kernel nao e' creditacao. Escrito pelo Write."""
import json, subprocess, sys
from pathlib import Path
CEN = Path(r"C:\IALD\Central de Patentes"); MOD = CEN / "patents" / "_formula_completa" / "tgl_formula_completa.py"
sys.path.insert(0, str(CEN / "tools"))
from custodia_g1 import patches  # noqa: E402

O395 = '        "face_do_psion_dita_condicional": str(co.get("status") or "").startswith("CONDITIONAL"),\n'
N395 = ('        # ERRATA AO LADO (03/11/2026, Central, custódia v406, gerência c1 em nome próprio): o original (abaixo, intacto) exigia o status CONDITIONAL…, o estado de v395 a v405\n'
        '        # (o kernel não exibia habitante do certificado de Fock):\n'
        '        #     "face_do_psion_dita_condicional": str(co.get("status") or "").startswith("CONDITIONAL"),\n'
        '        # desde a v406 a face é LIDA do kernel do rito (physicalFockCertificate, F1Fecho.CanonicalFockModularCoreInputR1; errata E14 no um.py; registro fechamento_v406):\n'
        '        # aceita-se TAMBÉM o status INHABITED_BY_physicalFockCertificate_V406 com inhabitant_exhibited True, a leitura antiga guardada em reading_v395 e o fechamento_v406\n'
        '        # selado no mesmo core com certificate_inhabited True. O nome da checagem não muda (os results.json dos dispositivos o citam); validade no kernel não é creditação.\n'
        '        "face_do_psion_dita_condicional": str(co.get("status") or "").startswith("CONDITIONAL")\n'
        '                                          or (co.get("status") == "INHABITED_BY_physicalFockCertificate_V406" and co.get("inhabitant_exhibited") is True\n'
        '                                              and bool(co.get("reading_v395")) and (core.get("fechamento_v406") or {}).get("certificate_inhabited") is True),\n')
O396 = '        "face_de_fock_dita_condicional": str(fo.get("status") or "").startswith("CONDITIONAL") and fo.get("inhabitant_exhibited") is False,\n'
N396 = ('        # ERRATA AO LADO (03/11/2026, Central, custódia v406, gerência c1 em nome próprio): o original (abaixo, intacto) exigia o status CONDITIONAL… e inhabitant_exhibited\n'
        '        # False, o estado de v396 a v405:\n'
        '        #     "face_de_fock_dita_condicional": str(fo.get("status") or "").startswith("CONDITIONAL") and fo.get("inhabitant_exhibited") is False,\n'
        '        # desde a v406 a face é LIDA do kernel do rito (physicalFockCertificate; errata E14 no um.py; registro fechamento_v406): aceita-se TAMBÉM o status\n'
        '        # INHABITED_BY_physicalFockCertificate_V406 com inhabitant_exhibited True, a leitura antiga em reading_v396, linked_to_the_corner_by_a_lemma AINDA False (nenhum lema\n'
        '        # liga psion C ao psionCorner) e o fechamento_v406 selado no mesmo core com certificate_inhabited True. O nome da checagem não muda.\n'
        '        "face_de_fock_dita_condicional": (str(fo.get("status") or "").startswith("CONDITIONAL") and fo.get("inhabitant_exhibited") is False)\n'
        '                                         or (fo.get("status") == "INHABITED_BY_physicalFockCertificate_V406" and fo.get("inhabitant_exhibited") is True\n'
        '                                             and bool(fo.get("reading_v396")) and fo.get("linked_to_the_corner_by_a_lemma") is False\n'
        '                                             and (core.get("fechamento_v406") or {}).get("certificate_inhabited") is True),\n')
E395 = 'Mirror é decisão do operador [LEGAL]; nada disto muda número de dispositivo"}'
E395N = ('Mirror é decisão do operador [LEGAL]; nada disto muda número de dispositivo [AO LADO, v406, 03/11/2026: desde a v406 a face do psíon lê o habitante do kernel do rito '
         '(physicalFockCertificate), com errata E14; o literal condicional de v395 a v405 fica como registro em reading_v395]"}')
E396 = 'do operador [INPUT/ONTO]; o 1/2 de bell_cci_half é a entropia linear (a de von Neumann é ln 2 nat); nada disto muda "\n                        "número de dispositivo"}'
E396N = ('do operador [INPUT/ONTO]; o 1/2 de bell_cci_half é a entropia linear (a de von Neumann é ln 2 nat); nada disto muda "\n                        "número de dispositivo [AO LADO, v406, 03/11/2026: desde a v406 a face de Fock lê o habitante do kernel do rito (physicalFockCertificate), '
         'com errata E14; o lema que liga psion C ao psionCorner segue faltando; o literal condicional de v396 a v405 fica como registro em reading_v396]"}')


def f(s):
    for o in (O395, O396, E395, E396):
        assert s.count(o) == 1, "trecho original nao esta' UMA vez no modulo: %r" % o[:70]
    assert "ERRATA AO LADO (03/11/2026, Central, custódia v406" not in s, "a errata ja esta' no modulo"
    s = s.replace(O395, N395).replace(O396, N396).replace(E395, E395N).replace(E396, E396N)
    return s, ["1 v395 face_do_psion_dita_condicional: errata ao lado", "2 v396 face_de_fock_dita_condicional: errata ao lado", "3 estatuto v395 ao lado", "4 estatuto v396 ao lado"]


r = patches.aplicar_em_arquivo(MOD, f, "v406_errata_faces")
print("patch:", json.dumps(r, ensure_ascii=False)); assert r["estado"] == "aplicado"
q = subprocess.run([r"C:\Python314\python.exe", "-X", "utf8", str(MOD)], cwd=str(MOD.parent), capture_output=True, timeout=600)
out = q.stdout.decode("utf-8", "replace") + q.stderr.decode("utf-8", "replace")
print("modulo rc", q.returncode); print(out[-900:])
assert q.returncode == 0, "o modulo comum ainda nao roda"
print("OK: o modulo comum dos 16 roda com a camada v406 e as erratas ao lado")
