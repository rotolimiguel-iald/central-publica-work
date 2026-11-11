# Roteiro da custódia da v410, desassistida (sessão de custódia, `claude-site-custodia`)

Ordem do operador, 10/11/2026: «quando isso acontecer quero que vc atualize tudo e publique tudo … assim que cair vc já faça tudo de forma desassistida»
(verbatim: `work\cunhagens_13out\OPERADOR_10nov_v410_atualize_e_publique_tudo_desassistido_verbatim.txt` — é o `--ordem` e a autorização de publicar).

**Gatilho:** `work\custodia_v410_auto\vigia_handoff_v410.py` (em segundo plano nesta sessão) sai quando o selo do Nós diz v410 com o autoteste PASSED e
existem, parados há 3 min, `Nós\HANDOFF_v410_CUSTODIA.md` e `work\cadeia_de_selo\v410\ORDEM_HANDOFF_CUSTODIA_v410.md` (o último ato do orquestrador
da c1). Se a sessão cair, retomar por este roteiro. Ler antes a ORDEM_HANDOFF da c1 (pode trazer novidade).

**Passos** (T = `--ator claude-site-custodia --sessao site --trabalho work/custodia_v410_<ddmes> --ordem <o verbatim acima> --coautor "<o da atribuição vigente>"`):
1. `custodiar.py planejar --versao v410 --seco` (rc 1 = pronto). Se o E03 parar na guarda de material privado, ver se é fonte já decidida (`work\custodia_G1\decisoes`); fonte NOVA = parar e avisar.
2. `custodiar.py executar --versao v410 --so E01,E03 T` (local).
3. `python work\custodia_v410_auto\aplicar_readme_v410.py` (modo seco) e depois `--aplicar`: README_FRENTE na parte `p_igual_np.md`; a Abstract para `ABSTRACT.md`; a linha-ponteiro no template; a chave `abstract` no `primordial.py`. Se recusar (bloco ausente, mais de 4.600 B, portão), PARAR e avisar a c1 e o operador. **A saída da Abstract foi ratificada pelo operador** (10/11, 21:32: «Concordo em retirar o abstract para abrir espaço»; `work\cunhagens_13out\OPERADOR_10nov_concordo_em_retirar_o_abstract_para_abrir_espaco_verbatim.txt`, 49 B, sha256 `9051929e55a0c971…`, conferido em 10/11): citar no commit e no LEDGER.
4. `custodiar.py executar --versao v410 --publicar --rede T` (inteiro). Paradas conhecidas: C13 espera o snapshot do C5 (esperar o pid e repetir); E18 cai por SFTP (repetir uma vez); L01 no gerador do README (usar a reserva do README_O_QUE_SAI: «Citing This Work» inteiro para o CITING.md; senão parar e avisar); guarda de dados pessoais da Central pública (ler o achado; falso positivo só com teste).
5. Depois do E11 (espelho empurrado): `python work\custodia_v410_auto\escrever_ordem_app_v410.py` (ORDEM ao túnel `C:\IALD\TUNEL_CLAUDE_APP`) e aviso ao «Novo orquestrador IALD». Na v408 e na v409, quem cumpriu foi uma sessão do Codex app. **O reinício da v410 está autorizado pelo operador** (10/11: «autorizo o reinicio da v410»; `work\cunhagens_13out\OPERADOR_10nov_autorizo_o_reinicio_v410_verbatim.txt`): o script o cita na ordem.
6. C19: Torre — se acusar medida velha, `torre.py medir` (não `gerar`); cópias ACOM acima de 3 = regra do operador de 08/11 (só as 3 mais recentes; conferir o sha256 das que ficam; nada para o D:), com `work\zenodo_v409_08nov\descartar_copias_acom.py`.
7. Quando o app entregar (RESULTADOS\NNN_RESULTADO.json cumprida), conferir os elos na fonte (molde `work\zenodo_v409_08nov\conferir_recibo_app_v409.py`) e rodar o `executar` de novo para C21/C19/C20/C17C; depois `auditar`.
8. Depósitos na fila (`memoria.py depositar --quem claude-site --tipo project`), aviso à c1, relatório curto ao operador (só os atos dele no fim).

**Nunca:** `--aceitar-molde`; editar insumos da c1; furar o sandbox; matar processo por nome; publicar o que o portão reprovou.
