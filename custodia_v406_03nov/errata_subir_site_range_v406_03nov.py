# -*- coding: utf-8 -*-
"""03/11/2026 06:0x, gerencia c1: o C18 da G1 (Central publica) parou em `subir_site.py --so subir`: a subida 20261103_052210 enviou 86 arquivos, TODOS
chegaram com HTTP 200, bytes e sha256 iguais aos locais, e foi REVERTIDA inteira porque tres arquivos > 1 MB (central/api/tgl-atlas.txt, central/api/tgl-core.txt,
central/um.acom) responderam 200 (arquivo inteiro) ao pedido `Range: bytes=0-1023`, onde a verificacao exige 206. Medido pela gerencia depois da reversao:
(a) em 02/11/2026 03:54 (subida 20261102_035422, v405) os MESMOS tres caminhos responderam 206; (b) o .htaccess local e' byte a byte igual ao que estava no ar;
(c) no mesmo no' do hospedeiro (nginx/1.24, Lw-X-Id ...@dinesh0020) o 206 oscila para 200 em pedidos consecutivos (bom.mp3: 206,206,200,200; documents/106/file.md:
206,206,206,200), independente de idade, tipo e tamanho do arquivo; os videos ainda respondem 206. E' parede do HOSPEDEIRO, nao dos arquivos. Consequencia da
reversao: o ar ficou INCOERENTE (index/llms.txt em v406 pela subida do site das 03:11; central/api/tgl-core.txt e os 16 code.json em v405).
Conserto AO LADO, no molde das erratas da custodia v406: a condicao original fica em comentario, intacta; quando HTTP 200, bytes e sha256 conferem, o Range nao
honrado vira AVISO MEDIDO (contado a parte, escrito na coluna, na linha de totais e no veredito), nunca «ok» silencioso; se bytes ou sha256 nao conferem, o arquivo
segue reprovado como antes. Aplicado por custodia_g1.patches.aplicar_em_arquivo (backup de BYTES, py_compile, os.replace) e CONFERIDO pela interface publica
`--verificar` contra dois manifestos temporarios: (1) os bytes de `antes/` (o que esta' no ar agora) -> rc 0; (2) um sha256 errado em arquivo > 1 MB -> rc 1.
Nada toca o ar, o um.py, o selo, o cofre ou o gate. Escrito pelo Write (o heredoc do Bash colapsa barras)."""
import hashlib, json, os, subprocess, sys, tempfile
from pathlib import Path
CEN = Path(r"C:\IALD\Central de Patentes"); SS = Path(r"C:\IALD\Site\tgl\v3.0_bancada\tools\subir_site.py")
ANTES = Path(r"C:\IALD\Site\tgl\v3.0_bancada\subidas\20261103_052210\antes")
sys.path.insert(0, str(CEN / "tools"))
from custodia_g1 import patches  # noqa: E402

O_DOC = '    """HTTP 200; content-length = bytes; sha256(download) = sha256 local; Range 206 se > 1 MB; content-type esperado (aviso)."""\n    resultados, falhas, avisos = [], 0, 0\n'
N_DOC = ('    """HTTP 200; content-length = bytes; sha256(download) = sha256 local; Range 206 se > 1 MB; content-type esperado (aviso).\n'
         '    [AO LADO, 03/11/2026, gerencia c1, custodia v406: Range != 206 com HTTP 200, bytes e sha256 iguais e\' AVISO MEDIDO (4o valor devolvido), nao falha;\n'
         '    medido em 03/11/2026 que o hospedeiro oscila 206 -> 200 no mesmo caminho e no mesmo no\' (parede do hospedeiro, nao dos arquivos).]"""\n'
         '    resultados, falhas, avisos, avisos_range = [], 0, 0, 0\n')
O_RNG = ("            rng = str(st_r)\n"
         "            if st_r != 206:\n"
         "                ok = False\n")
N_RNG = ("            rng = str(st_r)\n"
         "            # ERRATA AO LADO (03/11/2026, gerencia c1, custodia v406): o original (abaixo, intacto) reprovava o arquivo quando o Range nao devolvia 206:\n"
         "            #     if st_r != 206:\n"
         "            #         ok = False\n"
         "            # Em 02/11/2026 03:54 (subida 20261102_035422) tgl-atlas.txt, tgl-core.txt e um.acom responderam 206; em 03/11/2026 05:35 (subida 20261103_052210)\n"
         "            # o hospedeiro (nginx/1.24, Lw-X-Id) respondeu 200 com o arquivo INTEIRO, bytes e sha256 iguais aos locais, e a subida (86 arquivos) foi revertida,\n"
         "            # deixando o ar incoerente (site v406, Central v405). Medido depois, no mesmo no', o 206 oscila para 200 em pedidos consecutivos (bom.mp3, file.md),\n"
         "            # com .htaccess byte a byte igual: e' parede do HOSPEDEIRO, nao dos arquivos. Leitura vigente: HTTP 200 + bytes + sha256 iguais e Range != 206 e'\n"
         "            # AVISO MEDIDO (contado em avisos_range, escrito na coluna, nos totais e no veredito), nao falha; bytes ou sha256 diferentes seguem reprovando.\n"
         "            if st_r != 206:\n"
         "                if ok:\n"
         "                    avisos_range += 1\n"
         "                    rng = '%s (AVISO MEDIDO: Range nao honrado pelo hospedeiro; HTTP 200, bytes e sha256 conferem)' % st_r\n"
         "                else:\n"
         "                    ok = False\n")
O_RET = "    return resultados, falhas, avisos\n\n\ndef rodar_guarda():"
N_RET = "    return resultados, falhas, avisos, avisos_range\n\n\ndef rodar_guarda():"
O_V1 = "    res, falhas, avisos = verificar_no_ar(man, tentativas=1, espera=0)\n"
N_V1 = "    res, falhas, avisos, avisos_range = verificar_no_ar(man, tentativas=1, espera=0)\n"
O_V2 = "                     relatorio_verificacao(res), '', 'falhas = %d · avisos de content-type = %d' % (falhas, avisos), ''])\n"
N_V2 = "                     relatorio_verificacao(res), '', 'falhas = %d · avisos de content-type = %d · Range nao honrado pelo hospedeiro (aviso medido, 03/11/2026) = %d' % (falhas, avisos, avisos_range), ''])\n"
O_S1 = "    res, falhas, avisos = verificar_no_ar(sub_man) if enviados else ([], 0, 0)\n"
N_S1 = "    res, falhas, avisos, avisos_range = verificar_no_ar(sub_man) if enviados else ([], 0, 0, 0)\n"
O_S2 = "        '', 'falhas = %d · avisos de content-type = %d' % (falhas, avisos),\n"
N_S2 = "        '', 'falhas = %d · avisos de content-type = %d · Range nao honrado pelo hospedeiro (aviso medido, 03/11/2026) = %d' % (falhas, avisos, avisos_range),\n"
O_S3 = "        '', '## 6. Veredito', '', ('**SUBIDA VERIFICADA** — o ar diz o que o manifesto descreve.' if sucesso else\n"
N_S3 = ("        '', '## 6. Veredito', '', (('**SUBIDA VERIFICADA** — o ar diz o que o manifesto descreve.'\n"
        "                                    + ((' AVISO MEDIDO: o hospedeiro respondeu 200 (nao 206) ao Range em %d arquivo(s) > 1 MB; HTTP 200, bytes e sha256 conferem '\n"
        "                                        '(parede do hospedeiro, medida em 03/11/2026; em 02/11/2026 os mesmos caminhos respondiam 206). A promessa de 206 ao leitor de IA fica a conferir.'\n"
        "                                       % avisos_range) if avisos_range else '')) if sucesso else\n")
PARES = [(O_DOC, N_DOC, "1 docstring + avisos_range"), (O_RNG, N_RNG, "2 Range != 206: errata ao lado (aviso medido)"), (O_RET, N_RET, "3 return com avisos_range"),
         (O_V1, N_V1, "4 modo_verificar: 4 valores"), (O_V2, N_V2, "5 modo_verificar: totais"), (O_S1, N_S1, "6 modo_subir: 4 valores"), (O_S2, N_S2, "7 modo_subir: totais"),
         (O_S3, N_S3, "8 modo_subir: veredito com o aviso medido")]


def f(s):
    assert "ERRATA AO LADO (03/11/2026, gerencia c1, custodia v406)" not in s, "a errata ja esta' no subir_site.py"
    for o, _, nome in PARES:
        assert s.count(o) == 1, "trecho original nao esta' UMA vez (%d): %s" % (s.count(o), nome)
    for o, n, _ in PARES:
        s = s.replace(o, n)
    return s, [p[2] for p in PARES]


r = patches.aplicar_em_arquivo(SS, f, "v406_errata_range_hospedeiro")
print("patch:", json.dumps(r, ensure_ascii=False)); assert r["estado"] == "aplicado"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def manifesto(entradas):
    d = {"base": str(ANTES), "url_base": "https://teoriadagravitacaoluminodinamica.com/", "arquivos": entradas}
    fd, p = tempfile.mkstemp(prefix="manif_teste_range_", suffix=".json", dir=str(CEN / "work" / "custodia_v406_03nov")); os.close(fd)
    Path(p).write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8"); return p


def verificar(p):
    q = subprocess.run([r"C:\Python314\python.exe", "-X", "utf8", str(SS), "--verificar", "--manifesto", p], cwd=str(SS.parent), capture_output=True, timeout=900)
    out = q.stdout.decode("utf-8", "replace") + q.stderr.decode("utf-8", "replace")
    return q.returncode, out


core = ANTES / "central" / "api" / "tgl-core.txt"; info = ANTES / "central" / "um_acom_info.json"
assert core.is_file() and info.is_file(), "antes/ nao tem os bytes de referencia"
# (1) o que esta' no ar agora (bytes de antes/): deve passar; o Range, se 200, aparece como aviso medido
p1 = manifesto([{"caminho": "central/api/tgl-core.txt", "bytes": core.stat().st_size, "sha256": sha(core)},
                {"caminho": "central/um_acom_info.json", "bytes": info.stat().st_size, "sha256": sha(info)}])
rc1, out1 = verificar(p1); print("(1) rc", rc1); print(out1[-1200:])
# (2) sha256 errado em arquivo > 1 MB: deve reprovar (rc 1), com ou sem 206
p2 = manifesto([{"caminho": "central/api/tgl-core.txt", "bytes": core.stat().st_size, "sha256": "0" * 64}])
rc2, out2 = verificar(p2); print("(2) rc", rc2); print(out2[-500:])
assert rc1 == 0 and "falhas = 0" in out1 and "Range nao honrado pelo hospedeiro (aviso medido, 03/11/2026) = " in out1, "o caminho do aviso medido nao passou"
assert rc2 == 1 and "falhas = 1" in out2, "o caminho estrito (sha256 errado) deixou de reprovar"
for p in (p1, p2):
    os.remove(p)
Path(CEN / "work" / "custodia_v406_03nov" / "RECIBO_ERRATA_SUBIR_SITE_RANGE_v406.json").write_text(json.dumps({
    "quando": __import__("time").strftime("%Y-%m-%dT%H:%M:%S"), "arquivo": str(SS), "patch": r, "teste_1_bytes_do_ar_rc": rc1, "teste_2_sha_errado_rc": rc2,
    "linha_totais_1": [l for l in out1.splitlines() if l.startswith("falhas = ")][-1:], "linha_totais_2": [l for l in out2.splitlines() if l.startswith("falhas = ")][-1:],
    "medicoes": {"02/11/2026 03:54 (20261102_035422)": "tgl-atlas.txt, tgl-core.txt, um.acom: Range 206", "03/11/2026 05:35 (20261103_052210)": "os mesmos: Range 200, bytes e sha256 iguais; REVERTIDO",
                 "03/11/2026 ~06:0x (gerencia)": "bom.mp3 206,206,200,200; documents/106/file.md 206,206,206,200; documents/128/file.pdf 206 x6; videos mp4 206 x3; .htaccess local == antes (cmp)"}},
    ensure_ascii=False, indent=1), encoding="utf-8")
print("OK: subir_site.py com a errata ao lado; (1) rc %d, (2) rc %d; recibo gravado" % (rc1, rc2))
