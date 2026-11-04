# -*- coding: utf-8 -*-
"""_adapt_pos_build_v407.py -- adapta pos_build_kernel_v407.py (subida mecanica do molde v406) ao bundle de 9 modulos de TGLExt/ da v407. Substituicoes de contagem EXATA; backup de bytes; retira a marca [A ADAPTAR v407]."""
import datetime
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "pos_build_kernel_v407.py")
raw = open(P, "rb").read()
open(P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"), "wb").write(raw)
t = raw.decode("utf-8")
crlf = "\r\n" in t
assert not crlf


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:90], t.count(old), n)
    t = t.replace(old, new)


# marca
t = re.sub(r"(?m)^# \[A ADAPTAR v407\][^\n]*\n", "# [ADAPTADO v407] o bundle e' de 9 modulos de TGLExt/ (PsionCanto, Par e as sete pedras de 02/11); ancoras = os #print axioms das candidatas; bandeiras ext_psi407_*\n", t, count=1)
sub('chk("a lista dos modulos novos (kernel_modulos_novos_v407.json) == os 301 do delta (300 da bancada + a candidata), sem repeticao",\n        N_NOVOS == 301 and len(NEWMODS) == 301 and',
    'chk("a lista dos modulos novos (kernel_modulos_novos_v407.json) == os 9 do delta (PsionCanto, Par e as sete pedras de 02/11), sem repeticao",\n        N_NOVOS == 9 and len(NEWMODS) == 9 and')
sub('a raiz do sandbox == a raiz do Nos (v406 selada) + os DOIS imports do delta (ROOT_SUFFIX), em bytes', 'a raiz do sandbox == a raiz do Nos (v406 selada) + os NOVE imports do delta (ROOT_SUFFIX), em bytes')
sub('# ------------------------------------------------------------------ a raiz e o Audit: o sandbox == o Nos v406 selado + os dois imports', '# ------------------------------------------------------------------ a raiz e o Audit: o sandbox == o Nos v406 selado + os nove imports')
sub('# ------------------------------------------------------------------ as 8 ANCORAS do fecho', '# ------------------------------------------------------------------ as ANCORAS das 9 pedras (os #print axioms das candidatas)')
sub('chk("as %d ANCORAS do fecho (delta_v407.ANCORAS) existem no Audit, no trio, com proveniencia TGL_DECL_SOURCE == o modulo esperado" % len(DL.ANCORAS), not anc_bad and len(DL.ANCORAS) == 8, anc_bad[:3])',
    'chk("as %d ANCORAS das 9 pedras (delta_v407.ANCORAS) existem no Audit, no trio, com proveniencia TGL_DECL_SOURCE == o modulo esperado" % len(DL.ANCORAS), not anc_bad and len(DL.ANCORAS) == sum(len(v_) for v_ in DL.ANCORAS_POR_MODULO.values()) > 0, anc_bad[:3])')
sub('UMA serie ext_fch407_NNNN ordenada por (modulo, nome)', 'UMA serie ext_psi407_NNNN ordenada por (modulo, nome)')
# o bloco F1Fecho394
i0 = t.index("    # (a pasta TGLExt/F1Fecho394 JA' tem 184 modulos antigos")
i1 = t.index("    sem_decl_prov = sorted(NEWRELS - set(por_rel))")
novo_bloco = '''    # (os 9 modulos do bundle moram em TGLExt/ (nao ha subpasta nova): o invariante e' que os 9 NAO existiam no Nos v406 e que todo modulo emitido pelo compilador fora do bundle e' ANTIGO, isto e', existe no Nos)
    nos_k = os.path.join(DL.NOS, "tgl_kernel")
    ja_no_nos = sorted(r for r in nov if os.path.exists(os.path.join(nos_k, *r.split("/"))))
    chk("nenhum dos %d modulos do bundle existia no kernel do Nos v406 (todos NOVOS: nada e' sobrescrito)" % N_NOVOS, not ja_no_nos, ja_no_nos[:3])
    fora_do_bundle = sorted(rel for rel in set(srcm.values()) if rel not in NEWRELS)
    novos_fora = [r for r in fora_do_bundle if not os.path.exists(os.path.join(nos_k, *r.split("/")))]
    chk("o compilador so' emite declaracoes dos %d modulos do bundle ou de modulos ANTIGOS (os %d fora do bundle existem todos no Nos v406)" % (N_NOVOS, len(fora_do_bundle)), not novos_fora, novos_fora[:3])
'''
t = t[:i0] + novo_bloco + t[i1:]
sub('flags_v407.append(["%s%04d" % (DL.FLAG_PREFIX, i_), n, mod, "fecho_nomeada"])', 'flags_v407.append(["%s%04d" % (DL.FLAG_PREFIX, i_), n, mod, DL.ORIGEM_DE_BANDEIRA])')
sub('chk("as duas declaracoes da testemunha (canonicalFullTGLWitness e canonical_full_witness_inhabited) tem bandeira", all(bandeira_testemunha.values()), bandeira_testemunha)',
    'chk("o lema das duas faces (the_psion_is_the_corner_on_both_faces) e o par (o_par_de_psions_e_o_graviton) tem bandeira", all(bandeira_testemunha.values()), bandeira_testemunha)')
sub('"UMA serie de chaves %sNNNN, ordenada por (modulo, nome), para os %d modulos do bundle de TGLExt/F1Fecho394 (decisao da gerencia c1, v407: bundle como a v394; o numero e\' MEDIDO do Audit desta geracao)"',
    '"UMA serie de chaves %sNNNN, ordenada por (modulo, nome), para os %d modulos do bundle de TGLExt/ (decisao da gerencia c1, v407: bundle como a v406; o numero e\' MEDIDO do Audit desta geracao)"')
sub('"por_origem": {"fecho_nomeada": len(flags_v407)}', '"por_origem": {DL.ORIGEM_DE_BANDEIRA: len(flags_v407)}')
sub('(informativo) duracao do `lake build` a frio dos 301 modulos < 2400 s', '(informativo) duracao do `lake build` a frio dos 9 modulos < 2400 s')
sub('"delta_vs_v405": {"decl": j1[0], "thm": j1[1]}', '"delta_vs_v406": {"decl": j1[0], "thm": j1[1]}')
sub('"| delta_vs_v405:", j1[:2]', '"| delta_vs_v406:", j1[:2]')
sub('"o build do sandbox C:/t/k407c/final foi INCREMENTAL no que e\' antigo (copia do kernel do NOS v406 compilado pelo rito de 01/11) e A FRIO nos " + str(N_NOVOS) + " modulos novos (300 da bancada do ChatGPT + a candidata CanonicalFullTGLWitnessR1; linha Built em cada um); logs em kernel\\\\; o rito real do Nos compila tudo a frio"',
    '"o build do sandbox C:/t/k407c/final foi INCREMENTAL no que e\' antigo (copia do kernel do NOS v406 compilado pelo rito de 03/11) e A FRIO nos " + str(N_NOVOS) + " modulos novos (PsionCanto, Par e as sete pedras de 02/11; linha Built em cada um); logs em kernel\\\\; o rito real do Nos compila tudo a frio"')
sub("o recibo v407 lista os \" + str(N_NOVOS) + \" modulos NOVOS de TGLExt/F1Fecho394 (300 da bancada do ChatGPT + CanonicalFullTGLWitnessR1) e a \"", "o recibo v407 lista os \" + str(N_NOVOS) + \" modulos NOVOS de TGLExt/ (PsionCanto, Par e as sete pedras de 02/11) e a \"")
sub("preparacao, 02/11/2026)", "preparacao, 03/11/2026)")
open(P, "wb").write(t.encode("utf-8"))
import ast
ast.parse(t)
print("ok", len(t))
