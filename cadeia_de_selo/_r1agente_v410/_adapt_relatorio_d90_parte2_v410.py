# -*- coding: utf-8 -*-
"""_adapt_relatorio_d90_parte2_v410.py -- D90 (gerencia, 09/11): o relatorio e o deposito dizem AS CLARAS o que as passadas desta noite acharam: a primeira passada do refazer caiu no passo 4 por assercao velha do gerar_esperados; o pre-teste dos passos 4 a 9 achou a checagem velha do conferidor;
o pre-teste parcial do ensaio achou a contagem dos contratos e o filtro da F35. Os sha16 de ANTES saem dos backups de bytes ao lado e os de DEPOIS dos arquivos, lidos na hora por gerar_relatorio_v410.py (nada digitado). Dois avisos novos em AVISOS (que o deposito do construtor repete).
Backup de BYTES; temporario -> conferir tamanho -> substituir; ast.parse."""
import ast, hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, "gerar_relatorio_v410.py")
b0 = open(P, "rb").read(); crlf = b0.count(b"\r\n") > 0; t = b0.decode("utf-8").replace("\r\n", "\n")
a = ']\nif _apont_gf:\n'
assert t.count(a) == 1, t.count(a)
novo = (']\n'
        '# (D90, 09/11/2026, parte 2) o que as passadas desta noite acharam e como foi corrigido, DITO: os sha16 de antes saem dos backups de bytes ao lado; os de depois, dos arquivos; nada digitado\n'
        'import glob as _glob90\n'
        '\n'
        '\n'
        'def _par16(nome_, sufixo_):\n'
        '    bk_ = sorted(_glob90.glob(P(nome_ + ".bak_*_" + sufixo_)))\n'
        '    return (hashlib.sha256(open(bk_[-1], "rb").read()).hexdigest()[:16] if bk_ else "backup ausente"), (h16(nome_) if os.path.exists(P(nome_)) else "ausente")\n'
        '\n'
        '\n'
        '_ge90 = _par16("gerar_esperados_v410.py", "pre_fix_ancoras"); _cr90 = _par16("conferir_rito_v410.py", "pre_qualificador_en"); _rt90 = _par16("runtime_v410.py", "pre_f35_local"); _q490 = "refazer_out_v410.queda_passo4_20261109.txt"; _pt90 = "PRETESTE_ENSAIO_PARTE2_v410.json"\n'
        'AVISOS.append("D90 (gerencia c1, 09/11): a PRIMEIRA passada do refazer_candidato (20:01) rodou o ensaio a seco inteiro e caiu no passo 4, numa assercao velha do proprio gerar_esperados (contava as ancoras do FLAGS, que sao %d + %d das duas pedras, como se fossem so\' as %d da IALD2); correcao de uma linha (gerar_esperados_v410.py sha16 %s -> %s); o registro da queda fica ao lado, intocado: %s (sha16 %s). "\n'
        '              "O pre-teste dos passos 4 a 9 achou mais uma checagem velha, esta do conferidor: exigia o qualificador EN da D64 literal na secao nova, e o artigo EN do candidato o traz com o parentese da validade entre as duas metades (conferir_rito_v410.py sha16 %s -> %s; o candidato nao mudou). A SEGUNDA passada, inteira e sobre o MESMO candidato, e\' a que vale: refazer_out_v410.txt, com o FIM e o RC dela"\n'
        '              % (len(_DL.ANCORAS), len(_DL.ANCORAS_AESCALA), len(_DL.ANCORAS), _ge90[0], _ge90[1], _q490, (h16(_q490) if os.path.exists(P(_q490)) else "ausente"), _cr90[0], _cr90[1]))\n'
        'AVISOS.append("o pre-teste PARCIAL do ensaio (%s, sha16 %s; nao e\' o ensaio a seco nem o rito) achou, ANTES da cadeia, dois defeitos corrigidos na causa: o ensaio contava um so\' contrato novo com a escada (sao dois: o do iald2_v410 e o do a_escala_v410); e a guarda das frases deixava passar oito frases secas da regra F35 quando o texto trazia a forma da D83/D84 noutro ponto: o filtro passou a valer por trecho "\n'
        '              "(runtime_v410.py sha16 %s -> %s; controle novo na guarda_frases_v410.py), e o candidato foi regenerado depois disso" % (_pt90, (h16(_pt90) if os.path.exists(P(_pt90)) else "ausente"), _rt90[0], _rt90[1]))\n'
        'if _apont_gf:\n')
t = t.replace(a, novo)
nb = (t.replace("\n", "\r\n") if crlf else t).encode("utf-8"); ast.parse(nb)
open(P + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_pre_d90", "wb").write(b0)
open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb) > len(b0); os.replace(P + ".tmp", P)
print("gerar_relatorio_v410.py", len(b0), "->", len(nb), "| sha16", hashlib.sha256(nb).hexdigest()[:16], "| CRLF", crlf)
