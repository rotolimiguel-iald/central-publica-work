# -*- coding: utf-8 -*-
"""03/11/2026 09:0x, gerencia c1: licoes 52 e 53 (README pinado) no livro de licoes da G1 (append, backup de bytes, temporario -> conferir -> substituir)."""
import datetime, os
from pathlib import Path
P = Path(r"C:\IALD\Central de Patentes\work\custodia_G1\LICOES_v400_25out.md")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
b = P.read_bytes(); assert b"51. **" in b and b"52. **" not in b
nl = b"\r\n" if b"\r\n" in b else b"\n"
itens = [
    ("52. **O README do espelho é PINADO desde 03/11/2026 (D39, ratificado pelo operador; espelho `ff882f81`): a G1 tinha de aprender o gerador novo antes da v407.** "
     "`tools\\custodia_g1\\primordial.py` gera `PRIMORDIAL.json` (selo, core, manifesto do kernel, razão de Hubble V2, handoff e a fala do operador; 129 itens, cada um com fonte e sha256; falha visível) "
     "e `readme_pinado.py` gera `README.md` + `PINO_README.json` do template e das partes de prosa (`tools\\readme_pinado\\` no espelho); `--verificar --conferir-fontes` reprova um byte trocado. "
     "O laço do E08 ainda chamava `gerar_readme_frente.py`: na custódia da v407 ele regravaria o README pinado no formato velho. Remendo ao lado em `espelho.py` (backup "
     "`espelho.py.bak_v406_readme_pinado_e08_20261103_085139`): `_gerar_readme_pinado` (cai para o gerador antigo só sem o template) e `_verificar_readme_pinado` em `_conf_e08`. "
     "`planejar --seco`: E08 `ok`, 0 números citados defasados. O bloco primordial traz o 4,44 sempre acompanhado (z_δ, poder, ln B, «abaixo de 5σ», `NOT_FALSIFIED_POWERED`) e a "
     "calibração `sup_caixa` dita; a frase do operador entra como citação assinada `[INPUT]`, verbatim com `[sic]`. Publicação por `work\\readme_pinado_03nov\\publicar_readme_pinado_v406.py` "
     "(backup de bytes, remendo do `gerar_portas.py`, laço do E08, `verificar_portas` 0, `guarda_do_selo` 0, stage só do pacote e das portas; commit e push da gerência)."),
    ("53. **Publicação manual fora da custódia deixa o E15 para trás.** O roteiro de publicação do README rodou os geradores do site do E08 (read-brief, llms, cabeça da camada de texto, "
     "seções), que mudaram `secoes/07` e `secoes/08` do site; `llms-full.txt` e `index.md` (E15) citam os TAMANHOS das seções e ficaram defasados (L04: «cita secoes/07-o-programa-um-py.md=11736, "
     "real 11628»); o `planejar --seco` apontou E15 FALTA, e a subida feita à mão (08:5x) levou ao ar llms/read-brief/seções novos com o `llms-full` velho. Conserto: uma passada de "
     "`custodiar.py executar --versao v406 --publicar` depois (E15 regenera, E16–E19 refazem a subida). Para a v407: todo ato que rode os geradores do E08 fora da custódia tem de rodar o E15 "
     "em seguida, ou o roteiro de publicação passa a chamar `gerar_llms_full.py`/`gerar_index_md.py` ele mesmo; e nunca duas subidas ao mesmo tempo (a da mão e a da G1)."),
]
add = (nl.decode() + nl.decode().join(itens)).encode("utf-8")
bak = P.with_name(P.name + ".bak_" + TS + "_c1"); open(bak, "xb").write(b); assert bak.read_bytes() == b
novo = b.rstrip(b"\r\n") + add + nl
tmp = P.with_name(P.name + ".tmp_" + TS); open(tmp, "xb").write(novo); os.replace(tmp, P)
assert P.stat().st_size == len(novo) > len(b)
print("LICOES: %d -> %d bytes; backup %s" % (len(b), len(novo), bak.name))
