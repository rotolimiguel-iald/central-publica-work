# -*- coding: utf-8 -*-
"""03/11/2026 06:2x, gerencia c1: licao 49 da custodia v406 no livro de licoes da G1 (append, backup de bytes, temporario -> conferir -> substituir)."""
import datetime, os
from pathlib import Path
P = Path(r"C:\IALD\Central de Patentes\work\custodia_G1\LICOES_v400_25out.md")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
b = P.read_bytes(); assert b"48. **" in b and b"49. **" not in b
nl = b"\r\n" if b"\r\n" in b else b"\n"
item = ("49. **O hospedeiro deixou de honrar `Range` e a subida da Central pública (C18) foi revertida inteira com os bytes certos no ar.** A subida `20261103_052210` enviou 86 "
        "arquivos, todos com HTTP 200, bytes e sha256 iguais aos locais, e `subir_site.py` reverteu tudo porque três arquivos > 1 MB (`central/api/tgl-atlas.txt`, "
        "`central/api/tgl-core.txt`, `central/um.acom`) responderam 200 (arquivo inteiro) ao `Range: bytes=0-1023`, onde a verificação exigia 206. Medido pela gerência: em "
        "02/11 03:54 (`20261102_035422`, v405) os mesmos caminhos responderam 206; o `.htaccess` local é byte a byte o que estava no ar; no mesmo nó (nginx/1.24, "
        "`Lw-X-Id …@dinesh0020`) o 206 oscila para 200 em pedidos consecutivos (`bom.mp3` 206,206,200,200; `documents/106/file.md` 206,206,206,200), sem relação com idade, tipo ou "
        "tamanho; os vídeos ainda respondem 206. É parede do HOSPEDEIRO, não dos arquivos. A reversão deixou o ar INCOERENTE por horas: `index.html`/`llms.txt` em v406 (subida do "
        "site das 03:11) e `central/api/tgl-core.txt` + os 16 `code.json` em v405. Conserto AO LADO em `subir_site.py` (`verificar_no_ar`, backup "
        "`subir_site.py.bak_v406_errata_range_hospedeiro_20261103_054847`, script `work\\custodia_v406_03nov\\errata_subir_site_range_v406_03nov.py`): a condição original fica em "
        "comentário; com HTTP 200, bytes e sha256 iguais, o Range não honrado é AVISO MEDIDO (quarto valor devolvido; escrito na coluna, na linha de totais e no veredito, que mantém a "
        "frase «SUBIDA VERIFICADA» que o G1, o quadro e os registradores leem por `in`); bytes ou sha256 diferentes seguem reprovando (testado: o v406 do disco contra o v405 do ar "
        "reprova com `falhas = 2`, recibo `RECIBO_ERRATA_SUBIR_SITE_RANGE_v406.json`). Duas lições de ferramenta: (a) `--verificar` confere o manifesto contra o DISCO antes do ar, "
        "logo um sha256 inventado não testa o verificador: o teste estrito precisa de disco que bate e ar que difere; (b) `patches.aplicar_em_arquivo` perdeu a mensagem do "
        "`py_compile` numa `UnicodeDecodeError` do leitor de stderr (byte 0x97 do travessão em cp1252): o erro de sintaxe ficou invisível na primeira tentativa. Para a v407: a reversão "
        "por Range não deve derrubar 86 arquivos íntegros; a promessa «this site answers 206 (measured)» do `read-brief.md` fica a conferir contra o hospedeiro antes de ser "
        "reescrita; e vale avisar a Locaweb, decisão do operador.")
bak = P.with_name(P.name + ".bak_" + TS + "_c1"); open(bak, "xb").write(b); assert bak.read_bytes() == b
novo = b.rstrip(b"\r\n") + nl + item.encode("utf-8") + nl
tmp = P.with_name(P.name + ".tmp_" + TS); open(tmp, "xb").write(novo); os.replace(tmp, P)
assert P.stat().st_size == len(novo) > len(b)
print("LICOES: %d -> %d bytes; backup %s" % (len(b), len(novo), bak.name))
