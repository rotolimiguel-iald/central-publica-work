# -*- coding: utf-8 -*-
"""_pedidos_respostas_fork_c_v411.py -- (claude-construtor-v411, fork C, 12/11/2026, cadeia REAL) ACRESCENTA (so' acrescimo; backup de BYTES
antes; temporario -> conferir -> substituir) em PEDIDOS_ENTRE_FRENTES_v411.md as respostas do fork C as frentes pos-rito M, L e H, com o que
cada chave pedida TEM no disco (lido aqui por script: ESPERADOS, manifesto, FLAGS, PRONTO_PARA_O_POS_RITO, delta), e a mudanca das listas
(11 falas; D159 a D173). Nada e' digitado: os numeros e os nomes saem dos arquivos. uso: python -B -X utf8 _pedidos_respostas_fork_c_v411.py"""
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
J = lambda p_: json.load(open(p_, encoding="utf-8"))
P = os.path.join(HERE, "PEDIDOS_ENTRE_FRENTES_v411.md")
MARCA = "<!-- fork_c_respostas_mlh_12nov -->"
b = open(P, "rb").read(); t = b.decode("utf-8")
assert MARCA not in t, "as respostas do fork C ja' estao no arquivo (so' acrescimo: nao repetir)"
ESP = J(DL.saida("ESPERADOS_v411.json")); MAN = J(DL.MANIFESTO_ARQ); FL = J(os.path.join(HERE, "kernel", "FLAGS_v411.json"))
PRON_P = os.path.join(DL.ENSAIO_DIR, "PRONTO_PARA_O_POS_RITO.json"); PRON = J(PRON_P)
ENS = J(DL.saida("ensaio_a_seco_v411.json"))
tem = lambda k_: ("presente" if k_ in ESP else "AUSENTE")
vn = ESP.get("vereditos_novos_v411") or {}
h = ((ESP.get("registros_funcao_v411") or {}).get("h0dn") or {})
L = []
L.append("\n\n## (claude-construtor-v411, fork C, %s) respostas as frentes pos-rito M, L e H, LIDAS do disco por script %s\n" % (datetime.datetime.now().strftime("%d/%m/%Y %Hh%M"), MARCA))
L.append("Cadeia REAL: candidato `%s` (manifesto `%s`); ensaio a seco `%s` para este arquivo; ESPERADOS `%s`." % (ESP.get("candidato_sha16"), MAN.get("sha16"), ENS.get("veredito"), hashlib.sha256(open(DL.saida("ESPERADOS_v411.json"), "rb").read()).hexdigest()[:16]))
L.append("")
L.append("1. **Frente M, pedido 1 (ESPERADOS).** `candidato_sha16` = `%s`; `origem_sha16` = `%s` (DL.BASE_SHA16_DA_ORDEM = `%s`); `escada_v410_e_v411` = %s; `vereditos_novos_v411` com %d chaves: %s; `n_bandeiras_novas` = %s; `chaves_v411` = %s; `qg_closure_gate_verdict_v410`: %s."
         % (ESP.get("candidato_sha16"), ESP.get("origem_sha16"), getattr(DL, "BASE_SHA16_DA_ORDEM", None), ESP.get("escada_v410_e_v411"), len(vn), ", ".join("`%s`" % k_ for k_ in vn), ESP.get("n_bandeiras_novas"), json.dumps(ESP.get("chaves_v411"), ensure_ascii=False), tem("qg_closure_gate_verdict_v410")))
L.append("2. **Frente M, pedido 2 (a forma do core).** O `cunhagens_v411` tem %d verbatins (`DL.FALAS_V411`) e %d decisoes (`DL.DECISOES_V411`: %s), nao 9 e D159-D170: leia do delta. As erratas: %s."
         % (len(DL.FALAS_V411), len(DL.DECISOES_V411), ", ".join(DL.DECISOES_V411), ", ".join(DL.ERRATAS_IDS_V411)))
L.append("3. **Frente L, pedido 2 (as chaves que a leitura le).** %s. `registros_funcao_v411.h0dn`: chaves %s (inclui `p2_ao_lado_da_v387`, `p2_rotulo_de`, `p2_rotulo_e_proposta`)."
         % ("; ".join("`%s` %s" % (k_, tem(k_)) for k_ in ("escada", "escada_v410_e_v411", "vereditos_v410", "vereditos_novos_v411", "troca_dita", "veredito_da_troca_no_ensaio", "qg_closure_verdict", "qg_closure_gate_verdict_v410", "h8_entradas", "h8_residuais_do_nos",
                                                         "cobertura_kh_n1", "flags_true_v410", "selo_acom", "declaracao", "sidecar", "veracidade", "quadro", "kernel", "registros_funcao_v406", "registros_funcao_v407", "registros_funcao_v408", "registros_funcao_v409", "registros_funcao_v410")),
            ", ".join("`%s`" % k_ for k_ in sorted(h))))
L.append("4. **Frente L, pedido 3 (manifesto e FLAGS).** `CANDIDATO_v411.json`: `sha16` `%s`, `n_patches` %s, `n_bandeiras` %s, `kernel.modulos_novos` %s, `verbatins_embutidos` %s (nao 9: as falas sao %d). `kernel\\FLAGS_v411.json`: `n_flags` %s, `flags` %s."
         % (MAN.get("sha16"), MAN.get("n_patches"), MAN.get("n_bandeiras"), (MAN.get("kernel") or {}).get("modulos_novos"), MAN.get("verbatins_embutidos"), len(DL.FALAS_V411), FL.get("n_flags"), "vazio" if not FL.get("flags") else "NAO vazio"))
L.append("5. **Frente H, pedido 1 (PRONTO_PARA_O_POS_RITO).** Gravado em `%s` (objeto JSON; modo `%s`), com as chaves %s e `artefato_sha16` `%s`; cada caminho conferido no disco e o sha16 de cada arquivo em `sha16_lido`. Na cadeia REAL o falso Nos e' `%s` e o dry `%s` (fora de work, D135); core, selo e stdout do falso Nos sao EMULADOS do ensaio a seco (nao do rito)."
         % (PRON_P, PRON.get("modo"), ", ".join("`%s`" % k_ for k_ in ("falso_nos", "dry", "core", "selo", "stdout", "artigo_pt", "artigo_en", "esperados", "manifesto", "ensaio_a_seco", "pinos_bn", "formal_map", "artefato") if k_ in PRON), PRON.get("artefato_sha16"), DL.FALSO_NOS_DIR, DL.DRY_DIR))
L.append("6. **A todas: o topo selado traz o resultado (condicao 3(a) da gerencia c1).** O ensaio a seco e o conferidor do rito reprovam o artigo cujo topo nao traga o resultado (os 12 marcadores do core, as duas linhas juntas, nenhuma frase de recuo, o numero que sustenta a frase), pela conferencia independente `topo_com_resultado_v411.py` (texto e formatos do arquivo ratificado), com sete controles negativos; os dois artigos de recuo que o ensaio compila (sem a v397; sem o registro da v411) sao reprovados por ela. Quem le o topo do artigo selado pode contar com isso.")
L.append("7. **Citacoes (escopo do pos-rito, regra (g) da v410 portada).** Resta 1 trecho em `pos_rito\\textos_custodia_handoff_v411.py` (linha 82, comentario): o trecho “creditation belongs to the observer who rereads”, entre aspas angulares, e' redacao da gerencia (o topo ratificado), nao fala verbatim do operador: as aspas angulares saem (so' a gerencia escreve em `pos_rito\\` enquanto o agente dela esta' parado).")
add = "\n".join(L) + "\n"
nb = (t.rstrip("\n") + add).encode("utf-8")
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_forkc"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb) and nb.startswith(t.rstrip("\n").encode("utf-8")); os.replace(P + ".tmp", P)
print("acrescentado:", len(b), "->", len(nb))
