# -*- coding: utf-8 -*-
"""03/11/2026 06:1x, gerencia c1: o teste (2) do script errata_subir_site_range_v406_03nov.py nao chegou ao verificador: `subir_site.py --verificar` confere ANTES o
manifesto contra o DISCO (um sha256 inventado para' ali, rc 1, «regenerar o manifesto»). Aqui o teste estrito de verdade: manifesto com os bytes LOCAIS da v406
(C:\\IALD\\Site\\tgl\\v3.0, central/api/tgl-core.txt 1.116.245 B) enquanto o AR ainda tem a v405 (1.084.064 B, pela reversao das 05:35): o disco bate, o ar difere,
e o verificador tem de reprovar (rc 1, falhas >= 1) com a coluna Range sem a frase de aviso (o aviso so' vale com bytes e sha256 iguais). Grava o recibo que o
primeiro script nao chegou a gravar. Nada toca o ar. Escrito pelo Write."""
import hashlib, json, os, subprocess, tempfile, time
from pathlib import Path
CEN = Path(r"C:\IALD\Central de Patentes"); SS = Path(r"C:\IALD\Site\tgl\v3.0_bancada\tools\subir_site.py"); BASE = Path(r"C:\IALD\Site\tgl\v3.0")
core = BASE / "central" / "api" / "tgl-core.txt"; info = BASE / "central" / "um_acom_info.json"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()  # noqa: E731
d = {"base": str(BASE), "url_base": "https://teoriadagravitacaoluminodinamica.com/",
     "arquivos": [{"caminho": "central/api/tgl-core.txt", "bytes": core.stat().st_size, "sha256": sha(core)},
                  {"caminho": "central/um_acom_info.json", "bytes": info.stat().st_size, "sha256": sha(info)}]}
fd, p = tempfile.mkstemp(prefix="manif_teste_estrito_", suffix=".json", dir=str(CEN / "work" / "custodia_v406_03nov")); os.close(fd)
Path(p).write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
q = subprocess.run([r"C:\Python314\python.exe", "-X", "utf8", str(SS), "--verificar", "--manifesto", p], cwd=str(SS.parent), capture_output=True, timeout=900)
out = q.stdout.decode("utf-8", "replace") + q.stderr.decode("utf-8", "replace"); os.remove(p)
print("rc", q.returncode); print(out[-1500:])
linha_core = [l for l in out.splitlines() if "tgl-core.txt" in l and l.startswith("| `")]
totais = [l for l in out.splitlines() if l.startswith("falhas = ")]
assert q.returncode == 1 and totais and not totais[-1].startswith("falhas = 0"), "o caminho estrito (ar difere do manifesto) deixou de reprovar"
assert linha_core and "**NAO**" in linha_core[-1] and "AVISO MEDIDO" not in linha_core[-1], "a linha do tgl-core.txt deveria reprovar SEM a frase de aviso"
rec = CEN / "work" / "custodia_v406_03nov" / "RECIBO_ERRATA_SUBIR_SITE_RANGE_v406.json"
rec.write_text(json.dumps({
    "quando": time.strftime("%Y-%m-%dT%H:%M:%S"), "arquivo": str(SS), "backup": "subir_site.py.bak_v406_errata_range_hospedeiro_20261103_054847",
    "patch": "8 trocas (docstring, Range != 206 ao lado, return, modo_verificar x2, modo_subir x3); 29270 -> 31442 bytes; py_compile ok",
    "teste_1_bytes_do_ar_antes": {"rc": 0, "totais": "falhas = 0 · avisos de content-type = 0 · Range nao honrado pelo hospedeiro (aviso medido, 03/11/2026) = 1",
                                   "nota": "manifesto com os bytes de subidas/20261103_052210/antes (o que esta' no ar): passa; o Range 200 aparece como aviso medido"},
    "teste_2_sha_inventado": {"rc": 1, "nota": "parou ANTES do verificador: --verificar confere o manifesto contra o disco primeiro («regenerar o manifesto»); nao testa o caminho estrito"},
    "teste_3_disco_v406_ar_v405": {"rc": q.returncode, "totais": totais[-1:], "linha_tgl_core": linha_core[-1:][0][:160] if linha_core else None,
                                   "nota": "disco bate, ar difere: reprova, e a coluna Range nao traz a frase de aviso"},
    "medicoes": {"02/11/2026 03:54 (20261102_035422, v405)": "tgl-atlas.txt, tgl-core.txt, um.acom: Range 206",
                 "03/11/2026 05:35 (20261103_052210)": "os mesmos: Range 200 com bytes e sha256 iguais; 86 arquivos REVERTIDOS; ar incoerente (site v406, Central v405)",
                 "03/11/2026 ~05:4x (gerencia, UA do script)": "bom.mp3 206,206,200,200 e depois 200 x6; documents/106/file.md 206,206,206,200; documents/128/file.pdf 206 x6; videos mp4 206 x3; .htaccess local == antes (cmp); mesmo no' Lw-X-Id @dinesh0020"},
    "leitura": "parede medida no hospedeiro (nginx/1.24 da Locaweb), nao nos arquivos; o aviso e' escrito na coluna, nos totais e no veredito; bytes/sha256 diferentes seguem reprovando"},
    ensure_ascii=False, indent=1), encoding="utf-8")
print("OK: caminho estrito reprova; recibo gravado em", rec.name)
