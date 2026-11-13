# -*- coding: utf-8 -*-
"""_adapt_rito_v411.py -- (claude-construtor-v411, retomada, fork A, 12/11/2026) troca SO' o CABECALHO do rito_v411.sh (a subida mecanica de rotulo do rito_v410.sh, cujo CORPO e' generico e foi conferido linha a linha contra o molde:
so' rotulos 409->410 e 410->411) pelo texto da v411 (nenhum modulo novo; o registro com funcao h0dn_bg1_v411; o tempo MEDIDO no sandbox k411c, LIDO de kernel/construir_marcas.txt e de kernel/KH_N1_v411.json, nunca digitado).
Confere: o corpo (da linha «# O SERVIDOR DO MODELO NATIVO» ao fim, menos a linha do TEMPO ESPERADO) == o corpo do molde v410 com a subida de rotulo; sh -n depois. Backup de BYTES antes; LF respeitado. uso: python -B -X utf8 _adapt_rito_v411.py"""
import datetime, json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
P = os.path.join(HERE, "rito_v411.sh"); M = os.path.join(os.path.dirname(HERE), "v410", "rito_v410.sh")
b = open(P, "rb").read(); t = b.decode("utf-8"); assert "\r" not in t
ls = t.split("\n"); lm = open(M, "rb").read().decode("utf-8").split("\n")
i0 = next(i for i, l in enumerate(ls) if l.startswith("# O SERVIDOR DO MODELO NATIVO")); j0 = next(i for i, l in enumerate(lm) if l.startswith("# O SERVIDOR DO MODELO NATIVO"))
corpo, corpo_m = ls[i0:], lm[j0:]
assert len(corpo) == len(corpo_m)
sobe = lambda s: re.sub(r"(?<![0-9])410(?![0-9])", "411", re.sub(r"(?<![0-9])409(?![0-9])", "410", s.replace("410", "\x00"))).replace("\x00", "411") if False else re.sub(r"(?<![0-9])(409|410)(?![0-9])", lambda m: "410" if m.group(1) == "409" else "411", s).replace("k410c", "k411c")
dif = [(i, a, c) for i, (a, c) in enumerate(zip(corpo, corpo_m)) if a != sobe(c) and not a.startswith("# TEMPO ESPERADO")]
assert not dif, ("o corpo do rito_v411.sh difere do molde alem dos rotulos", dif[:3])
mm = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", open(os.path.join(HERE, DL.KERNEL_DIR, "construir_marcas.txt"), encoding="utf-8").read(), re.M)}
KH = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, DL.KH_N1_INSUMO), encoding="utf-8"))
b_s = mm["epoch_build_fim"] - mm["epoch_inicio"]; a_s = mm["epoch_audit_fim"] - mm.get("epoch_audit_inicio", mm["epoch_build_fim"])
assert b_s == KH["duracao_build_s"] and a_s == KH["duracao_audit_s"] and KH["n_modulos_novos"] == 0, (b_s, a_s, KH.get("duracao_build_s"), KH.get("duracao_audit_s"))
_dec = "%s a %s" % (sorted(DL.DECISOES_V411, key=lambda k_: int(k_[1:]))[0], sorted(DL.DECISOES_V411, key=lambda k_: int(k_[1:]))[-1])
CAB = ["#!/bin/sh",
       "# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork A)] o rito da v411 (ato da gerencia): o CORPO e' o do rito da v410 subido de rotulo (o pacote v411, a guarda v410/v411, ESPERADOS_v411, rodada_v411_stdout, carimbar_stdout_v411.py; conferido linha a linha contra o molde por _adapt_rito_v411.py: so' rotulos); o cabecalho reescrito: NENHUM modulo novo de kernel, o registro com FUNCAO h0dn_bg1_v411 e o tempo MEDIDO no sandbox k411c (lido dos arquivos)",
       "# O RITO v411 (ato da gerencia c1): roda o um.py v411 instalado no Nos -- NENHUM modulo novo de kernel (o kernel embutido e' o da v410 byte a byte; a raiz TGLExt.lean e o TGL/Audit.lean NAO mudam; o proprio um.py materializa o corpo embutido, identico ao do Nos), o registro com FUNCAO h0dn_bg1_v411 "
       "(chamado no main logo depois do bloco do h0dn_fontes_hms13_v410 e dos registros por spec da v410, antes de emit_figures: o teste H0DN x BG1 aberto uma vez em 12/11/2026, RECALCULADO neste rito a partir dos bytes embutidos pela rotina pinada; %d checagens; sob o modelo de erros publicado o primario e, ao lado, as Cefeidas livres; "
       "retrodicao sem ajuste, emenda posterior a guarda, teste nao cego; provado e' validade, nao creditacao) e os registros por spec cunhagens_v411 (as %d falas de 11 e 12/11 por sha256; as decisoes %s e as erratas %s vao nos registros) e kh_n1_cobertura_v411; os registros anteriores (os quatro com funcao da v410 inclusive) sao RECRIADOS; NENHUMA chave antiga muda; o gate nao se move."
       % (DL.N_CHECKS_FECHO, DL.N_FALAS_V411, _dec, ", ".join(DL.ERRATAS_IDS_V411[:-1]) + " e " + DL.ERRATAS_IDS_V411[-1]),
       "# O PILAR QUANTICO NAO roda de novo: reaproveitado pela chave do cache (a mesma da v410; as decisoes D38/D45 das cadeias anteriores seguem, nenhuma decisao da v411 as muda); TGL_RITE_CHECKPOINT DESLIGADO; o executor da abertura do H0DN NUNCA roda de novo (a abertura foi uma vez: o registro executa, dos bytes embutidos, a rotina pinada; nenhum arquivo de kimi\\ e' lido);",
       "# guarda do marcador anterior: echo 1 | python um.py no Nos, stdout canonico em rodada_v411_stdout.txt, trailer RITO_RC=<rc>, horarios no pacote. RODADA COMPLETA."]
TEMPO = ("# TEMPO ESPERADO (v411, parametro lido de kernel/construir_marcas.txt e kernel/KH_N1_v411.json, MEDIDO em 12/11/2026 no sandbox k411c: NENHUM modulo novo, build incremental sem nada a compilar; a soma dos tempos por modulo e' %s s, o maximo de um modulo %s s): "
         "o `lake build` (a v410 selada ja' esta' compilada em .lake/build; a raiz e o Audit nao mudam) = %d s e 1 Audit = %d s" % (KH["build_modulos_s_soma"], KH["build_modulos_s_max"], b_s, a_s))
novo = CAB + [(TEMPO if l.startswith("# TEMPO ESPERADO") else l) for l in corpo]
assert sum(1 for l in novo if l.startswith("# TEMPO ESPERADO")) == 1
T = "\n".join(novo)
bk = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_cab"; open(bk, "wb").write(b); assert open(bk, "rb").read() == b
nb = T.encode("utf-8"); open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
r = subprocess.run(["sh", "-n", P], capture_output=True, text=True); assert r.returncode == 0, r.stderr
print("rito_v411.sh: cabecalho trocado | corpo == molde com a subida (%d linhas) | tempo build %d s, Audit %d s | sh -n ok" % (len(corpo), b_s, a_s))
