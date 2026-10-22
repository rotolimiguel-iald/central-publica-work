# -*- coding: utf-8 -*-
"""resultado_d19c.py -- DELTA 19/10 (rodada d19c): as secoes do RESULTADO_DELTA_19OUT.md que mudaram na rodada final (0.1, 7 e 8), como funcoes que LEEM o contexto montado por gerar_resultado.py (nenhum numero ou hash digitado aqui).
Importado por gerar_resultado.py."""
br = lambda n: format(n, ",").replace(",", ".")


def secao_0_1(c):
    L = []; a = L.append
    tx, HA, HD, bg, dv, ESP, ENS, SIM, EXM, CN, POS = c["tx"], c["HA"], c["HD"], c["bg"], c["dv"], c["ESP"], c["ENS"], c["SIM"], c["EXM"], c["CN"], c["POS"]
    a("## 0.1 A rodada final (d19c): as quatro ordens da gerência")
    a("")
    a("1. **Proposta de `pos_rito` APLICADA** (ordem expressa da gerência; backup de bytes `textos_v394.py.bak_..._c1d19c`, na mesma pasta; o outro agente terminou): `pos_rito\\textos_v394.py` `%s` → `%s` (%s → %s B). O passo (`aplicar_pos_rito_d19c.py`) só vale se o arquivo atual é o ORIGINAL da proposta e o resultado é IDÊNTICO, byte a byte, ao `.PROPOSTA` que a gerência revisou; só depois entra a frase do item 2. **Harness dos textos em modo ensaio** (`harness_textos_ensaio.py`, só leitura: importa os `textos_v394` e `leitura_v394` REAIS e os executa contra um Nós emulado a partir do ensaio a seco; emulados e ditos: o stdout do rito, o aplicado e a conferência do rito; nada de `pos_rito` é escrito, `derivar_cadeia_v394.py` NÃO rodou): no ORIGINAL reprova (`%s`; %d problemas, todos da mesma soma; a leitura da rodada sem problema); no aplicado **%s** — %d funções de texto rendem, guarda P18 limpa, soma por grupo %d + %d + %d + %d = %d (= bandeiras novas = ESPERADOS) e a errata presente nos %d textos que embutem `_num` (%s). Evidência: `HARNESS_TEXTOS_ENSAIO_ANTES_original.json`, `HARNESS_TEXTOS_ENSAIO_DEPOIS_aplicado.json` e os textos renderizados em `harness_textos_saida\\`." % (
        tx["sha16_antes"], tx["sha16_depois"], br(tx["bytes_antes"]), br(tx["bytes_depois"]), c["erro_antes"], len(HA["problemas"]), "TUDO PASSOU" if HD["tudo_passou"] else "NAO PASSOU", c["ntexto"], bg["tempo"], bg["quadratica"], bg["rede"], bg["outros"], sum(bg.values()), len(c["com_errata"]), ", ".join("`%s`" % k for k in c["com_errata"])))
    a("2. **Errata AO LADO da palavra «teoremas»**: os módulos novos têm %s declarações e %s teoremas (%s não-teoremas) [REAL: `kernel\\KH_N1_v394.json::delta_vs_v393`, a linha TOTAL do Audit do sandbox menos a da v393; a gerência contou 3864 e 3167 sem a pedra do delta, que acrescenta uma declaração e um teorema: [DECLARADO pela gerência]]. UMA frase, nas mesmas palavras, no artigo PT (`artigo_pt_v394.pysnip` `%s` → `%s`), no artigo EN (`artigo_en_v394.pysnip` `%s` → `%s`), no parágrafo «O que entra» da seção da v394 (logo depois da frase da escada e da cobertura, a primeira ocorrência da palavra) e no texto do kernel de `textos_v394.py` (`_num`): «%s». O token de máquina `teoremas limpos: N/M` do stdout FICA (o pós-rito o lê por regex); a frase não tem número (a fonte única é `delta19_v394.ERRATA_TEOREMAS_*`); T e D vêm do kernel por script e citam a fonte. Guarda P18 limpa nos dois `.pysnip` e em `textos_v394.py`; o ensaio compilou o artigo PT/EN de novo (pdflatex ×2 rc 0, sem erro)." % (
        br(dv["decl"]), br(dv["thm"]), br(c["nao_thm"]), c["ap_"]["sha16_antes"], c["ap_"]["sha16_depois"], c["ae"]["sha16_antes"], c["ae"]["sha16_depois"], c["ERR"]))
    a("3. **Adendo no `ESTADO_V394.md`** (ao fim; backup de bytes; correção ao lado, nada acima foi alterado): «ADENDO 19/10 (delta)» com o que mudou, sha antes/depois, a escada %s, o h8 %s, a política de bandeiras e as erratas; gerado por `gerar_adendo_estado_d19.py` a partir dos artefatos (recusa-se a escrever se a guarda P18 achar violação ou se o harness não estiver no estado esperado). `ESTADO_V394.md` `%s` → `%s` (%s → %s B)." % (
        br(ESP["escada"][1]), ESP["h8_entradas"], c["es_"]["sha16_antes"], c["es_"]["sha16_depois"], br(c["es_"]["bytes_antes"]), br(c["es_"]["bytes_depois"])))
    a("4. **Regeneração completa, sem mão** (`V394_REGERAR=1 gerar_candidato_v394.py` e a cadeia inteira): candidato **`%s`** (%s B, %d patches). O candidato intermediário `%s` (o da primeira entrega do delta) foi SUPERADO: a errata muda o artigo; os bytes dele estão em `%s` e a evidência dele em `superado_7abb7ba986c098c7\\`. Ensaio a seco inteiro **%s**, com as etapas obrigatórias `simular_arvore_do_nos` (%d entradas == pino %d) e `exame_pontos_v394` (`algum_falso = %s`); `gerar_esperados_v394.py`; conferidor: controle negativo (`tudo_bate = %s`, deve-mudar %d de %d, não-pode-mudar %d de %d) e caminho positivo contra o Nós falso (**%s**); `diff_e_pinos`, `comparar_v393`, `comparar_r8` (sem explicação pendente), `conferir_citacoes` e `p00_precondicoes` (%s). Escada %s; h8 %s; o kernel NÃO mudou (sandbox `C:\\t\\k394d\\final`, recibo da primeira entrega)." % (
        c["S16"], br(c["CM"]["bytes"]), len(c["CM"]["patches"]), c["INTER"], c["INTER_BAK"], ENS["veredito"], SIM["formal_files_n_no_rito_real"], ENS["simular_arvore_do_nos"]["pino_h8_entradas"], EXM["algum_falso"], CN["tudo_bate"],
        sum(1 for v in CN["deve_mudar"].values() if v), len(CN["deve_mudar"]), sum(1 for v in CN["nao_pode_mudar"].values() if v), len(CN["nao_pode_mudar"]), "TUDO BATE" if POS["tudo_bate"] else "NAO BATE", "TODAS PASSARAM" if c["PRE"]["ok"] else "FALHOU", br(ESP["escada"][1]), ESP["h8_entradas"]))
    a("")
    return L


def secao_7_8(c):
    L = []; a = L.append
    SOMA, bg, ESP = c["SOMA"], c["bg"], c["ESP"]
    a("## 7. Os textos do pós-rito (`pos_rito\\textos_v394.py`): a soma que eles esperavam NÃO fechava com a política nova; a proposta foi APLICADA e fecha")
    a("")
    a("- Diagnóstico: `textos_v394.py::_d` calculava `n_out_flags = n_bandeiras_novas − (tempo + quadrática + rede)` com os números de CONTRATO do Codex (108 + 18 + 3581). Com a política só-nomeadas dava **%d** e o `assert n_out_flags >= 0` recusava (`SOMA_TEXTOS_POS_RITO.json`; o harness reproduz a recusa no arquivo ORIGINAL)." % SOMA["formula_original"]["n_out_flags"])
    a("- Correção aplicada (a proposta da gerência, 36 linhas): `_d` lê `ESPERADOS.n_bandeiras_por_grupo` (tempo %d, quadrática %d, rede %d, outros %d; soma %d) e a frase das bandeiras usa esses números; o grupo \"outros\" (a pedra) sai do mesmo campo. As demais somas fecham: módulos %d = %d tempo + %d quadrática + %d rede + %d de outro grupo (`%s`); `cdx.decl == n_formais.tempo`; escada %d + %d = %d; h8 %d = %d + %d." % (
        bg["tempo"], bg["quadratica"], bg["rede"], bg["outros"], sum(bg.values()), SOMA["modulos"]["total"], SOMA["modulos"]["tempo"], SOMA["modulos"]["quadratica"], SOMA["modulos"]["rede"], len(SOMA["modulos"]["outros"]), SOMA["modulos"]["outros"][0],
        SOMA["escada"]["v393"], SOMA["escada"]["bandeiras_novas"], SOMA["escada"]["soma"], SOMA["h8"]["entradas"], SOMA["h8"]["embutidos"], len(SOMA["h8"]["residuais"])))
    a("- **Achado do harness, NÃO corrigido (fora do que foi autorizado):** o texto `_num` diz «nenhum registro novo além dos cinco fixos», mas o candidato final tem um SEXTO registro novo, `criterio_binario_de_parada_v394` (`_extras` compara os registros do core com `V[\"reg_todos\"]`, que já o inclui). O `_criterio` também não cita a pedra nova nem o registro (diz «correspondências no kernel [REAL, já existentes]», que é verdade para os oito teoremas). Proposta de UMA linha, NÃO aplicada: `delta_19out\\pos_rito_PROPOSTA2_delta19.diff` (`_extras` passa a comparar com `V[\"reg394\"]`, os cinco fixos; o sexto sai pelo nome); o harness sobre ela: ver `HARNESS_TEXTOS_ENSAIO_PROPOSTA2.json` (passa, guarda limpa).")
    a("")
    a("## 8. Decisões que ficam com a gerência / o operador")
    a("")
    a("1. **Nome da pedra** (o operador nomeia; `TheBinaryReadingAtTheFixedPoint` é provisório) e a leitura «critério binário de parada» (ONTO).")
    a("2. (Feito nesta rodada, por ordem: a proposta de `pos_rito`, a errata da palavra «teoremas» e o adendo do `ESTADO_V394.md`; ver a seção 0.1.) Resta decidir a PROPOSTA 2 da seção 7 (uma linha: o sexto registro dito pelo nome).")
    a("3. As duas falas de 19/10 também estão em `cunhagens_v394` (o artigo diz «%d falas embutidas»); o registro novo as lê separadamente." % len(ESP["cunhagens"]))
    a("4. B(n) segue como estava: três pedras sem declaração nomeada (`NetworkProofAuditR3/R7/R8`), `x19 = nao`, recibo pré-selo inutilizável; o delta não os altera.")
    a("5. O risco das fontes fora do selo que o rito lê (exame, §Riscos) continua o mesmo.")
    a("")
    return L
