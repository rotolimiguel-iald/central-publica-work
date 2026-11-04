# -*- coding: utf-8 -*-
"""03/11/2026 08:3x, gerencia c1: entrada datada no topico construir-tudo-o-fechamento-02nov.md sobre a pedra candidata PsionCantoR1 (sem linha nova no indice:
MEMORY.md esta a 166 B do teto de 24.000; o indice ja aponta para o topico). Backup de bytes; temporario -> os.replace. Escrito pelo Write."""
import json, os, time
from pathlib import Path
MEMD = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"); TOP = MEMD / "construir-tudo-o-fechamento-02nov.md"; TS = time.strftime("%Y%m%d_%H%M%S")
rec = json.loads(Path(r"C:\IALD\Central de Patentes\work\pedras_candidatas_03nov\RECIBO_PSION_CANTO_R1_03nov.json").read_text(encoding="utf-8"))
ENTRADA = ("**03/11, 08:2x — A CONDIÇÃO SOB COMPRESSÃO É TEOREMA NO HABITANTE; o lema das duas faces do psíon existe (pedra candidata `PsionCantoR1`, nome provisório, sha16 `%s`).** "
           "O operador matemático da condição dele (sha16 `9978862f60cfbf29`) é a LEITURA DE JONES (`TGLExt.IALDJones.jonesReading`, `e·x·e`, a compressão pela projeção), nomeada pela gerência em 02/11. "
           "Provado no sandbox da v406 (`C:\\t\\k406c\\final`, `lake env lean`, LEAN_RC 0, 8/8 declarações só no trio, 0 sorry; recibo `work\\pedras_candidatas_03nov\\RECIBO_PSION_CANTO_R1_03nov.json`; "
           "rota `kernel.psion_canto_r1_03nov`): (A) o canto do psíon na face de Fock `P = PFmic C = P_{ℂ·Ω}` escalariza (`P y P = ⟪ψ, yψ⟫ P`), lê o fluxo da luz como 1 (`⟪ψ, Δ^{it}ψ⟫ = 1`) e a leitura de Jones "
           "do fluxo pelo canto devolve o canto (`P Δ^{it} P = P`); a contração de Jones `U_s` e o fluxo unitário leem o mesmo no canto (o espelhamento); tudo SEM hipótese no `physicalFockCertificate` da v406: "
           "a face do psíon deixa de ser condicional («virar a chave de conjectura para provado», como VALIDADE). (B) `psionCorner.p = |Φ⁺⟩⟨Φ⁺|`; nas duas faces o psíon é o vetor de norma 1 cujo canto é o projetor "
           "sobre ele, escalariza, pesa 1 e devolve o canto sob o motor comprimido. O que NÃO afirma: não identifica Ω com Φ⁺ (elo de ESTRUTURA); o par = gráviton segue [OPEN]; não é teste com a natureza; "
           "o motor contínuo no pilar (D38) é pré-registro à parte; gate intocado; creditação recusada. Instalar, nomear a pedra e as declarações: decisão do operador (v407); a chave "
           "`linked_to_the_corner_by_a_lemma` passa a ser lida do kernel na v407, com o conteúdo do elo dito." % rec["sha16"])
b = TOP.read_bytes(); nl = b"\r\n" if b"\r\n" in b else b"\n"; novo = b.rstrip(b"\r\n") + nl + nl + ENTRADA.encode("utf-8") + nl
bak = TOP.with_name(TOP.name + ".bak_" + TS + "_c1_pedra_psion"); open(bak, "xb").write(b); assert bak.read_bytes() == b
tmp = TOP.with_name(TOP.name + ".tmp_" + TS); open(tmp, "xb").write(novo); os.replace(tmp, TOP); assert TOP.read_bytes() == novo
print("%s: %d -> %d B; backup %s" % (TOP.name, len(b), len(novo), bak.name))
