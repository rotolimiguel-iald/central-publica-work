#!/bin/sh
# [ADAPTADO v410 PARTE 2, 09/11/2026 (~18h), claude-subagente-adaptacao (Sonnet 5.5, A)] so' comentarios (o corpo e' generico: nenhuma lista nem contagem presa): o bundle e' de DOIS modulos (IALD2 e AEscala) e os registros com funcao sao QUATRO (iald2_v410, a_escala_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410); os testes offline (_teste_h0dn_offline, _teste_aescala_offline, _teste_hms13_offline) NAO correm aqui (o construtor os roda antes, a parte; sao informativos no gerar_relatorio); nenhum arquivo de kimi e' aberto por esta cadeia
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] refaz, na ordem, tudo o que depende do texto do candidato v410 (gerador, comparacao, ensaio, ESPERADOS, conferidor, citacoes, pinos, instalar/rito, p00); conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
# refaz, NA ORDEM, tudo o que depende do texto do candidato v410 (gerador -> comparacao AST -> ensaio a seco [com simular_arvore_do_nos e exame_pontos] -> ESPERADOS -> conferidor [controle negativo e caminho positivo] -> citacoes -> diff e pinos -> conferencia do instalar/reverter/rito -> precondicoes).
# USAR quando mudar qualquer script/texto que entra no candidato (runtime_v410.py, registros_v410.py, artigo_*_v410.pysnip, gerar_candidato_v410.py) ou o kernel (copiar_k410c.sh + preparar_bundle_v410_06nov.py + construir_kernel_v410.sh + pos_build_kernel_v410.py + copiar_insumos_v410.py antes: ver regerar_v410.sh).
# Nao toca o Nos, nao instala, nao roda o rito. Cada passo para na primeira falha (set -e). Saida inteira em refazer_out_v410.txt.   uso: sh ./refazer_candidato_v410.sh [--regerar]   (--regerar autoriza sobrescrever um candidato ja existente)
# [v410, adaptado em 06/11/2026, claude-construtor-v410, fork B] o candidato e' o do BUNDLE PEQUENO (na parte 2, de dois modulos em TGLExt/: IALD2 e AEscala; quatro registros com funcao, iald2_v410, a_escala_v410, h0dn_bg1_v410 e h0dn_fontes_hms13_v410, + specs cunhagens_v410/kh_n1_cobertura_v410); os 2 modulos da v409, os 4 do terminal (v408), os 9 do psion (v407) e os 301 do fecho (v406) ficam no kernel como registro; nenhuma chave antiga muda. O passo 9 (p00) imprime PENDENTE, nao FALHA, para o que so' existe depois do B(n) pre-selo (PINO_RECIBO_PRE_SELO_v410.json, PROVA_PRODUCAO_INTACTA_v410_pre_selo.json), das guardas/harnesses do pos-rito e do MEMORY.md: o p00 final (TODAS PASSARAM) so' vale depois deles.
# O passo 7 grava DIFF_KERNEL_v410.txt, DIFF_v409_v410.diff (diff -u do um.py v409 contra o candidato) e PINOS_BN_v410.json.
set -e
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v410"
cd "$V"
[ "$1" = "--regerar" ] && export V410_REGERAR=1
PY="python -I -B -X utf8"
PYN="python -B -X utf8"   # SEM -I onde o script importa o um.py (precisa do numpy do usuario): o conferidor e o teste dele
echo "== 1. gerar_candidato_v410.py $(date +%T)"; $PY gerar_candidato_v410.py
echo "== 2. comparar_v409_v410.py (nada da v409 perdido)"; $PY comparar_v409_v410.py
echo "== 3. ensaio_a_seco_v410.py (inclui simular_arvore_do_nos, exame_pontos e as guardas ESTATICAS da Bancada sobre o candidato) $(date +%T)"; python -B -X utf8 ensaio_a_seco_v410.py um_v410_candidato.py v410 > ensaio_out.txt 2>&1 || { tail -c 3000 ensaio_out.txt; exit 1; }
tail -2 ensaio_out.txt
echo "== 4. gerar_esperados_v410.py"; $PY gerar_esperados_v410.py
echo "== 5. conferir_rito_v410.py: controle negativo (Nos ainda v409: tudo_bate tem de ser falso) e caminho positivo (Nos FALSO do ensaio)"
$PYN conferir_rito_v410.py _CONTROLE_NEGATIVO_PRE_RITO > /dev/null 2>&1 && { echo "FALHOU: o controle negativo deu TUDO BATE"; exit 1; } || echo "controle negativo: nao bate (esperado)"
$PYN teste_conferidor_positivo_v410.py | tail -1
echo "== 6. conferir_citacoes_v410.py"; $PY conferir_citacoes_v410.py | tail -1
echo "== 7. diff_e_pinos_v410.py"; $PY diff_e_pinos_v410.py | tail -1
echo "== 8. conferir_instalar_rito_v410.py (instalar/reverter/rito: invariantes, sintaxe e a condicao do modulo novo)"; $PY conferir_instalar_rito_v410.py | tail -1
echo "== 9. p00_precondicoes_v410.py $(date +%T)"; $PY p00_precondicoes_v410.py | tail -6
echo "== FIM $(date +%T)"
