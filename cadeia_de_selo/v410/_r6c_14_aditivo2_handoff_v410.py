# -*- coding: utf-8 -*-
"""_r6c_14_aditivo2_handoff_v410.py -- ADITIVO 2 a ordem do conserto unico (gerencia c1, 10/11/2026; substitui o A1 e o A2 do ADITIVO 1; o B e o C ficam), FORA do candidato, em pos_rito\\textos_custodia_handoff_v410.py:
 1. o TEXTO PRONTO dos dois blocos do README vem do ARQUIVO da gerencia (conserto_r3\\ADITIVO_2_README_FRENTE_E_O_QUE_SAI_v410.pysnip; sha256 conferido aqui contra o da ordem) e entra, byte a byte (so' o fim de linha vira o do gerador, CRLF),
    DEPOIS da definicao de README_EVIDENTE, no lugar das definicoes do construtor (README_FRENTE e README_O_QUE_SAI do ADITIVO 1); nada e' redigido nem copiado da mensagem;
 2. a adaptacao do _r6c_12 e' DESFEITA: cada bloco e' lido SOZINHO pela guarda das frases e pelo portao do G1, como todo texto;
 3. os dois blocos vao ao handoff cada um no seu marcador (o mesmo formato dos sete, sobre BLOCOS_README, SEM o prefixo PARAGRAFO_), depois do paragrafo README_EVIDENTE; o assert de marcador ja' existente cobre os dois;
    a re-leitura pelo leitor do G1 exige os NOVE corpos (os sete e estes dois, cada corpo igual a constante) e zero problemas; o recibo do S6d guarda os bytes do README_FRENTE.
Do construtor ficam so' a funcao montar_blocos e dois controles a mais (os tres teoremas da escala citados sao nomes da secao 7 ratificados pelo operador; o bloco nao anuncia limiar). Idempotente; backup de BYTES; CRLF; temporario + os.replace; ast.parse."""
import ast, hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = time.strftime("%Y%m%d_%H%M%S")
SNIP_P = os.path.join(HERE, "conserto_r3", "ADITIVO_2_README_FRENTE_E_O_QUE_SAI_v410.pysnip"); SNIP_SHA = "1cbbddea52705b023943033a53a8cd61e65fe54cdf647bcbce6ce96237ef1c58"   # (o sha256 da ORDEM do ADITIVO 2: o que vale e' o LIDO do arquivo, que tem de ser igual)
sb = open(SNIP_P, "rb").read(); assert hashlib.sha256(sb).hexdigest() == SNIP_SHA and len(sb) == 6668 and b"\r" not in sb, ("PARE: o texto pronto do ADITIVO 2 nao tem o sha256 da ordem", hashlib.sha256(sb).hexdigest())
SNIP = sb.decode("utf-8"); assert SNIP.endswith("\n")
p = os.path.join(HERE, "pos_rito", "textos_custodia_handoff_v410.py"); b0 = open(p, "rb").read(); t = b0.decode("utf-8")
assert t.count("\r\n") == t.count("\n") > 0, "o gerador do handoff deixou de ser CRLF"
t = t.replace("\r\n", "\n"); log = []
BS = chr(92)


def tr(a, b, n=1):
    global t
    c = t.count(a)
    if c == 0 and b in t:
        log.append("ja' feito: " + a[:50]); return
    assert c == n, ("contagem", c, "esperado", n, a[:140])
    t = t.replace(a, b); log.append("trocado x%d: %s" % (c, a[:50]))


CONTROLES = ("# (do construtor, ao lado do texto pronto da gerencia) dois controles a mais: os tres teoremas da escala citados no bloco sao nomes da secao 7 RATIFICADOS pelo operador (lidos do recibo dos nomes pelo delta), uma vez no ingles e uma no portugues; e o bloco NAO anuncia limiar (por isso nao leva a clausula do limite)\n"
             "_RF_NOMES = (\"sem_escala_nao_ha_fita\", \"a_constante_da_luz_e_a_escala_do_tempo\", \"o_nome_e_a_singularidade_da_informacao\")\n"
             "assert set(_RF_NOMES) <= set(DL.NOMES_RATIFICADOS_R6_AESCALA) and all(README_FRENTE.count(\"`\" + n_ + \"`\") == 2 for n_ in _RF_NOMES), \"os tres teoremas da escala do README_FRENTE nao sao nomes da secao 7 ratificados pelo operador (ou nao estao uma vez no ingles e uma no portugues)\"\n"
             "assert not re.search(r\"limiar|threshold|ln 2\", README_FRENTE) and DL.CLAUSULA_Z_PT not in README_FRENTE and DL.CLAUSULA_Z_EN not in README_FRENTE, \"o README_FRENTE nao anuncia limiar (por isso nao leva a clausula do limite)\"\n"
             "\n\n")
if SNIP not in t:
    i0 = t.index("# ------------------------------------------------------------------ (ADITIVO 1 a ordem do conserto unico, gerencia c1, 10/11/2026: a custodia da v410 e' automatica) os DOIS BLOCOS do README")
    i1 = t.index("def montar_blocos(textos, readme_evidente, readme_blocos, v):"); assert 0 < i0 < i1 and t.count("README_FRENTE = (") == 1
    t = t[:i0] + SNIP + CONTROLES + t[i1:]; log.append("o texto pronto do ADITIVO 2 (do arquivo da gerencia) no lugar das definicoes do ADITIVO 1")
assert t.count(SNIP) == 1 and t.count("README_FRENTE = (") == 1 and t.count("README_O_QUE_SAI = (") == 1 and t.count("BLOCOS_README = [") == 1
if "README_BLOCOS" in t:
    n_ = t.count("README_BLOCOS"); t = t.replace("README_BLOCOS", "BLOCOS_README"); log.append("README_BLOCOS -> BLOCOS_README x%d" % n_)
# 2. a adaptacao do _r6c_12, DESFEITA: cada bloco e' lido sozinho
tr("        v1 = [list(x) for x in GF.violacoes((README_FRENTE + \"" + BS + "n" + BS + "n\" + t) if ident == \"README_O_QUE_SAI\" else t)]   # (ADITIVO 1) o README_O_QUE_SAI cita o titulo do bloco de hoje do README e remete ao bloco pronto acima: "
   "a guarda das frases o le JUNTO do README_FRENTE, que traz o qualificador (a obrigacao F34 e' do MESMO texto); o portao do G1 e as demais regras leem o bloco sozinho\n",
   "        v1 = [list(x) for x in GF.violacoes(t)]\n")
# 3. a re-leitura pelo leitor do G1: os NOVE corpos (os sete e os dois blocos do README), cada um igual a constante, e zero problemas
tr("faltam = [i for i, _ in TEXTOS if (\"%s_%s\" % (i, V)) not in h.corpos]", "faltam = [i for i, _ in TEXTOS + BLOCOS_README if (\"%s_%s\" % (i, V)) not in h.corpos]   # (ADITIVO 2) os NOVE corpos: os sete textos e os dois blocos do README")
tr("for i, t in TEXTOS:\n    assert h.corpos[\"%s_%s\" % (i, V)].strip(\"" + BS + "n\") == t, \"corpo lido difere do escrito: \" + i", "for i, t in TEXTOS + BLOCOS_README:\n    assert h.corpos[\"%s_%s\" % (i, V)].strip(\"" + BS + "n\") == t, \"corpo lido difere do escrito: \" + i")
tr("for i, t in BLOCOS_README:   # (ADITIVO 1) os dois blocos do README, relidos entre os marcadores pelo parser do G1: iguais aos escritos\n"
   "    assert h.corpos.get(\"%s_%s\" % (i, V), \"\").strip(\"" + BS + "n\") == t, \"bloco do README lido difere do escrito: \" + i\n", "")
tr("print(\"parser do G1: os dois blocos do README lidos entre os marcadores, iguais aos escritos; README_FRENTE: %d bytes em UTF-8, sha256 %s\" % (len(README_FRENTE.encode(\"utf-8\")), hashlib.sha256(README_FRENTE.encode(\"utf-8\")).hexdigest()))",
   "print(\"parser do G1: os dois blocos do README lidos entre os seus marcadores (sem o prefixo PARAGRAFO_), iguais as constantes; README_FRENTE: %d bytes em UTF-8 (teto %d), sha256 %s\" % (len(README_FRENTE.encode(\"utf-8\")), README_FRENTE_TETO_B, hashlib.sha256(README_FRENTE.encode(\"utf-8\")).hexdigest()))")
tr("print(\"parser do G1: 7/7 corpos lidos, 0 problemas; marcadores:\", sorted(h.marcadores))", "print(\"parser do G1: %d/%d corpos lidos (os sete textos e os dois blocos do README), 0 problemas; marcadores:\" % (len(TEXTOS + BLOCOS_README) - len(faltam), len(TEXTOS + BLOCOS_README)), sorted(h.marcadores))")
tr("\"readme_frente_sha256\": hashlib.sha256(README_FRENTE.encode(\"utf-8\")).hexdigest(), \"readme_o_que_sai\": README_O_QUE_SAI,", "\"readme_frente_sha256\": hashlib.sha256(README_FRENTE.encode(\"utf-8\")).hexdigest(), \"readme_frente_teto_b\": README_FRENTE_TETO_B, \"readme_o_que_sai\": README_O_QUE_SAI, \"readme_ponteiro_abstract\": README_PONTEIRO_ABSTRACT,")
ast.parse(t)
b1 = t.replace("\n", "\r\n").encode("utf-8")
if b1 != b0:
    bak = p + ".bak_" + TS + "_aditivo2"; open(bak, "wb").write(b0); assert open(bak, "rb").read() == b0
    tmp = p + ".tmp_r6c"; open(tmp, "wb").write(b1); assert os.path.getsize(tmp) == len(b1) > 0; os.replace(tmp, p); assert open(p, "rb").read() == b1
print("pos_rito/textos_custodia_handoff_v410.py:", "MUDOU" if b1 != b0 else "igual", log)
