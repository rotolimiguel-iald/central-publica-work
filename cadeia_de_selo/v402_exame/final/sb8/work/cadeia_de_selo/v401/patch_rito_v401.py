# -*- coding: utf-8 -*-
"""patch_rito_v401.py -- cabecalho e tempo esperado do rito_v401.sh (derivado do rito da v399, a cadeia de CONTEUDO): o modulo novo e' a FalsidadeDaInercia (nome dado pelo operador); os numeros do tempo sao LIDOS de kernel/construir_marcas.txt. Recusa rodar duas vezes."""
import os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
P = sys.argv[1] if len(sys.argv) > 1 else "rito_v401.sh"
t = open(P, encoding="utf-8", newline="").read()
assert "FalsidadeDaInercia" not in t, "o patch ja foi aplicado"
mm = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", open(os.path.join("kernel", "construir_marcas.txt"), encoding="utf-8").read(), re.M)}
build_s = mm["epoch_build_fim"] - mm["epoch_inicio"]; audit_s = mm["epoch_audit_fim"] - mm["epoch_build_fim"]
lines = t.split("\n")
i0 = next(i for i, l in enumerate(lines) if l.startswith("# O RITO v401 (ato da gerencia c1"))
i1 = next(i for i, l in enumerate(lines) if l.startswith("# guarda do marcador anterior"))
novo = [
    "# O RITO v401 (ato da gerencia c1, 25/10/2026): roda o um.py v401 instalado no Nos -- 1 modulo novo de kernel (TGLExt/FalsidadeDaInercia: o nome «falsidade (simulacro) da inercia» e' do operador; o numero e' lido de kernel_modulos_novos_v401.json) materializado a partir do corpo embutido, kernel e Audit",
    "# construidos pelo proprio um.py, o registro com FUNCAO falsidade_da_inercia_v401 (a inercia e' o proprio zero absoluto; um posto inercial daria 1 = 0; chamado no main logo depois da declaracao do operador), os registros por spec novos do core v401 (cunhagens_v401, com as cinco inscricoes de 25/10, as ratificacoes",
    "# e a errata ao lado da leitura do escriba no adendo; kh_n1_cobertura_v401) e os registros da v399 RECRIADOS (selo_pela_propria_tecnologia_v399, declaracao_do_operador_v399, cunhagens_v399, kh_n1_cobertura_v399), o SIDECAR um_absoluto_selo_acom.json (depois da ultima escrita do selo). O QUADRO do Teste da Unica Palavra segue no topo.",
    "# O PILAR QUANTICO NAO roda de novo: reaproveitado pela chave do cache (a mesma da v400); TGL_RITE_CHECKPOINT DESLIGADO. Molde: rito_v399.sh herdado com as afericoes dele (a cadeia de CONTEUDO que rodou em 24/10), trocados os nomes, o pacote (a propria pasta da cadeia v401) e a",
]
lines[i0:i1] = novo
j = next(i for i, l in enumerate(lines) if l.startswith("# TEMPO ESPERADO (v401"))
lines[j] = ("# TEMPO ESPERADO (v401, parametro lido de kernel/construir_marcas.txt): no sandbox k401c, 1 lake build INCREMENTAL (a v400 e a pedra nova, FalsidadeDaInercia, ja' estao compiladas em .lake/build, a pedra isolada; mudam a raiz TGLExt e o Audit) = %d s e 1 Audit = %d s (%d s por passagem); "
            "o rito faz 3 passagens de build + Audit (ordem de grandeza %.1f min so' de lake, fora o resto do um.py; no Nos o primeiro build compila a pedra a frio, dezenas de segundos a mais). O timeout do lake build DENTRO do um.py (candidato) tem de caber nisso: conferir no candidato." % (build_s, audit_s, build_s + audit_s, 3 * (build_s + audit_s) / 60.0))
t = "\n".join(lines)
open(P + ".tmp", "w", encoding="utf-8", newline="").write(t); os.replace(P + ".tmp", P)
print("patch aplicado:", P, "| lake por passagem", build_s + audit_s, "s")
