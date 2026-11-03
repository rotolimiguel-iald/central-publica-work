# -*- coding: utf-8 -*-
"""03/11/2026 02:3x, gerencia c1: acrescenta as licoes 43 a 46 da custodia v406 ao livro de licoes da G1 (work/custodia_G1/LICOES_v400_25out.md), com backup de BYTES ao lado,
temporario -> conferir que cresceu -> substituir (regra do backup imediato). Append so', nunca por cima. Escrito pelo Write."""
import datetime, os
from pathlib import Path
P = Path(r"C:\IALD\Central de Patentes\work\custodia_G1\LICOES_v400_25out.md")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
b = P.read_bytes()
assert b"42. **A suite da G1" in b and b"43. **" not in b, "a licao 42 nao esta' no fim ou a 43 ja existe"
nl = b"\r\n" if b"\r\n" in b else b"\n"
itens = [
    "43. **Os sete marcadores da prosa da custódia (TITULO_EN, ENTROU_EN, KERNEL_LEITURA_EN, ABERTOS_EN, ARCO_EN, ARCO_PT, COMMIT) não saem da cadeia de selo** (o `textos_vNNN`/`fechar_vNNN` não os gera): na v405 e na v406 a gerência os anexou à mão no fim do handoff, e sem eles o `planejar` para em 20 (S7 do orquestrador `pos_treino_v406`, 02:03 e de novo só depois do acréscimo). Na v406: `cadeia_de_selo\\v406\\pos_rito\\textos_custodia_handoff_v406_03nov.py` (números lidos do core selado, do selo e do diário e conferidos; guarda de frases da v406 + portão do G1 + forma do ARCO/COMMIT; backup de bytes; releitura pelo `nos.ler_handoff`, 7/7). Conserto na fonte, para a v407: o `fechar` da cadeia gera os sete blocos a partir do registro selado (ou o pré-voo S2 do orquestrador recusa um handoff sem eles), para que o G1 nunca chegue ao S7 sem a prosa.",
    "44. **S8_registro: troca de veredito de LETRA pede `mudados_permitidos` numa revisão da semântica.** A v406 foi a primeira custódia com um veredito que muda fora de «dígitos e pino» (`rede_fock_v394`: `JOINT_CONTRACT_OPEN` → `JOINT_CERTIFICATE_INHABITED_V406__THREE_JOINT_ITEMS_STILL_OPEN`, a troca dita pelo handoff e conferida pelo registro `fechamento_v406`); o rascunho do script traz `mudados_permitidos: []` e a pedra genérica reprovou o C4 (`fora_do_padrao: [rede_fock_v394]`), como a ESPEC §4.3 manda. Conserto: `work\\custodia_v406_03nov\\revisar_semantica_v406_rev1_03nov.py` grava `SEMANTICA_CUSTODIA.rev1.json` AO LADO do rascunho no cofre (revisor distinto do script: a gerência c1, em nome próprio; motivo e fontes por sha256) e só a deixa se a própria pedra passar (pass True, `REVISADA rev1`, os dois céticos reprovando as injeções). Para a v407: quando a cadeia de selo declarar troca dita de letra, a preparação gera a rev1 antes do C4.",
    "45. **`EXCL_RAIZ` não excluía `SEMANTICA_CUSTODIA.rev<n>.json`:** a revisão mora no cofre e não existe no Nós; na custódia SEGUINTE o C3 a tomaria, do cofre base, como artefato fixo e pararia em «falta no Nós». Patch em `tools\\custodia_g1\\central.py` (03/11/2026, backup `central.py.bak_20261103_023005_c1_excl_rev`): `SEMANTICA_CUSTODIA(\\.rev\\d+)?\\.json`.",
    "46. **C8 escrevia «SEMANTICA_DECLARADA_SEM_REVISAO» mesmo com revisão ao lado:** o sufixo do veredito da camada dos 16 era literal; agora lê `veredito_camada_sufixo` do SEMANTICA do cofre, como o C6 já fazia para o runner (ESPEC §709): o número corrige a frase. Patch em `central.py` (backup `central.py.bak_20261103_023126_c1_suf_c8`); a rev1 da v406 traz `SEMANTICA_REVISADA_REV1_PELA_GERENCIA_C1`, que entra no veredito do runner (C6) e do módulo (C8).",
]
add = (nl.decode() + nl.decode().join(itens)).encode("utf-8")
bak = P.with_name(P.name + ".bak_" + TS + "_c1"); open(bak, "xb").write(b); assert bak.read_bytes() == b
novo = b.rstrip(b"\r\n") + add + nl
tmp = P.with_name(P.name + ".tmp_" + TS); open(tmp, "xb").write(novo); os.replace(tmp, P)
assert P.stat().st_size == len(novo) > len(b), "o livro nao cresceu"
print("LICOES: %d -> %d bytes; backup %s" % (len(b), len(novo), bak.name))
