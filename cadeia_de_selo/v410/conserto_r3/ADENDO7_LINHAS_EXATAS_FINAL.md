# ADENDO 7: as linhas EXATAS que o delta consertado le (ESPEC v2 FINAL do conserto da v410)

Arquivo que a gerencia escreve: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\DESENHO_v410_ADENDO_7_POS_CANDIDATO_10nov.md` (UTF-8; LF ou CRLF, os dois foram testados). O texto livre do adendo (as decisoes, por extenso) e' da gerencia; o delta so' LE as linhas abaixo, que tem de estar no adendo LETRA POR LETRA, cada uma numa linha so'. Os hashes foram lidos dos arquivos por script pelo reconciliador e de novo pelo cetico (10/11/2026); a gerencia os confere ao escrever.

## 1. As falas novas, 29 a 40: UMA linha uniforme por fala (comeca na coluna zero, com hifen e espaco; nada depois do sha256)

~~~~text
- fala 29 | na pedra 13 | `work\cunhagens_13out\OPERADOR_10nov_o_quarto_nome_ressurreicao_do_sinal_o_observador_e_a_escala_colapsar_e_criar_a_escala_verbatim.txt` | sha256 `77145eeec3c2fc7809aae383021b413b301a819cc05b78cfb5a56463a93376c4`
- fala 30 | na pedra 14 | `work\cunhagens_13out\OPERADOR_10nov_e_isso_mesmo_perfeito_ratificado_cuidado_com_o_loop_de_revisao_verbatim.txt` | sha256 `7857d4ddf9d3cfc0b290836b3c0e1bcadf3a61031ee03ebb4688b824269cfdfd`
- fala 31 | na pedra 15 | `work\cunhagens_13out\OPERADOR_10nov_o_observador_esta_na_escala_da_constante_da_luz_verbatim.txt` | sha256 `1c108b67addd75ded2a54b82ac39028041563dfaf52d687b915901e5a35b91fe`
- fala 32 | na pedra 16 | `work\cunhagens_13out\OPERADOR_10nov_e_isso_que_falta_a_constante_da_luz_sem_a_escala_nao_tem_fita_verbatim.txt` | sha256 `260ca86a995661e3a3f1f05c7391e735b971e11b6101eae90f80f29db5ab8136`
- fala 33 | na pedra 17 | `work\cunhagens_13out\OPERADOR_10nov_tudo_depende_da_escala_o_leitor_so_admite_o_sinal_posto_e_dominio_a_luz_e_a_escala_do_tempo_verbatim.txt` | sha256 `d7004a035f0586f7e5dbf268c30a8ce9b6c0951bd1ee291c9129ffd95593f698`
- fala 34 | na pedra 18 | `work\cunhagens_13out\OPERADOR_10nov_ratifico_tudo_a_selecao_e_o_observador_a_forma_matricial_da_luz_torre_de_jones_verbatim.txt` | sha256 `1be0f6e4b9908fa792b447d883ec2f0b96b85a44b4125140db320a12dbdfa1dd`
- fala 35 | na pedra 19 | `work\cunhagens_13out\OPERADOR_10nov_nao_ha_contradicao_na_tonica_a_escala_e_a_unidade_posta_a_do_observador_e_de_outro_dominio_verbatim.txt` | sha256 `965a78104bf81c48dad7f7adb0c556d33f06ad3b817ec3538cba4ce35d8b9f40`
- fala 36 | na pedra 20 | `work\cunhagens_13out\OPERADOR_10nov_o_confronto_de_ideias_nos_faz_avancar_escala_igual_relatividade_verbatim.txt` | sha256 `2307cf4cbd97a0d7309ec24b50f72975af0dd44215734614eea702ff6f3e16c8`
- fala 37 | na pedra 21 | `work\cunhagens_13out\OPERADOR_10nov_o_que_e_relativo_o_que_e_par_sem_o_par_nao_ha_escala_verbatim.txt` | sha256 `aafc8ed3051e1f74ca4ad7976c3bc01acfe68fe2d52b46c85e67d8b8fe3f5111`
- fala 38 | na pedra 22 | `work\cunhagens_13out\OPERADOR_10nov_beta_tgl_e_o_invariante_a_escala_do_par_luz_radicalizada_em_entropia_igual_informacao_igual_nome_verbatim.txt` | sha256 `1cda85b81ce1887f2f1c78f1357f6423890c32c87e14f050694eae4d08cb025e`
- fala 39 | na pedra 23 | `work\cunhagens_13out\OPERADOR_10nov_nao_pode_ser_leitura_minha_refute_o_nome_e_a_singularidade_o_par_do_nome_e_o_verbo_verbatim.txt` | sha256 `81e6566d93d08a679db9b3b96911ea9b19a30d787b6d8b7125e820fb9714b4fa`
- fala 40 | na pedra 24 | `work\cunhagens_13out\OPERADOR_10nov_isso_lindo_confirmo_tudo_o_nome_e_a_singularidade_da_informacao_verbatim.txt` | sha256 `fe679296ee8b283ee2191d1ed6e5627b56102a8f64d9591615517619715daa8b`
~~~~

Regras que o delta confere: os numeros no um.py sao consecutivos e terminam no total das falas (40); a diferenca entre o numero no um.py e o numero na pedra e' a mesma em todas (16); a primeira linha e' a da fala do quarto nome; o sha256 de cada arquivo em disco e' o da linha e o do recibo do autor da pedra R6; o numero na pedra da ultima e' o n_falas do recibo (24).

**REGRA NOVA (achado do cetico, por teste):** ponha estas doze linhas ANTES de qualquer prosa do adendo que cite o nome de arquivo de uma fala entre crases. O delta acha o prefixo do sha256 de cada fala pela PRIMEIRA vez em que o nome do arquivo aparece seguido, a ate' 40 caracteres, de um hash entre crases. Se a prosa disser, antes das linhas, algo como “a fala `OPERADOR_10nov_…_verbatim.txt` ratifica a pedra `6863b1fc…`”, o prefixo lido passa a ser o da pedra, e o delta recusa a carga (fail-closed). O mesmo vale na outra ordem: “sha256 `<hash>`” a ate' 40 caracteres ANTES do nome do arquivo entre crases. Com as linhas primeiro, ou sem hash entre crases perto do nome da fala na prosa, nao acontece.

## 2. A revisao R3, o pedido de correcao e o candidato revisado (o formato do ADENDO 4; uma linha; pode estar em qualquer lugar)

~~~~text
`revisao_terceiro\REVISAO_TERCEIRO_v410.json` sha16 `8184102c73a34fe6`; pedido de correção sha16 `7e262affa4010036`; candidato revisado `8a713e5e644af09b`
~~~~

O arquivo `revisao_terceiro\REVISAO_TERCEIRO_v410.json` existe com esse sha16 (e' igual ao `.R3.json`); o pedido e' `revisao_terceiro\PEDIDO_CORRECAO_R3_v410.md`. O delta le os tres sha16 do adendo; nao os confere contra os arquivos.

## 3. O resultado do painel independente (o sha16 entre crases, em qualquer lugar do adendo; o delta o confere contra o arquivo em disco)

~~~~text
`PAINEL_R3_v410_RESULTADO.json` sha16 `1ccebc2577babd64`
~~~~

## 4. O pino da ORDEM KIMI H0DN-03B (no lugar do pino da 03; uma linha, na coluna zero)

~~~~text
- ORDEM KIMI H0DN-03B | `work\h0dn_bg1_v410_09nov\ORDEM_KIMI_H0DN_03B_10nov.md` | sha256 `c2b45aa48711f97ed336f74acd7cbd7ef5ec17062d3d22f74895f5c6a68fb7c5`
~~~~

A ORDEM 03 (`ORDEM_KIMI_H0DN_03_10nov.md`) fica em disco como registro e NAO e' pinada. Nenhum arquivo da pasta `kimi\` entra. O delta confere o sha256 e os bytes do arquivo da 03B (8415 bytes hoje) e que ele esta' fora da pasta da entrega do executor.

## 5. O codigo do delta consertado que le essas linhas (copiado dos itens 61, 63, 70 e 82 da ESPEC FINAL; conferido por script: cada linha esta' no delta aplicado em memoria)

~~~~python
ADENDO7_ARQ = os.path.join(HERE, "DESENHO_v410_ADENDO_7_POS_CANDIDATO_10nov.md"); assert os.path.exists(ADENDO7_ARQ), "falta o ADENDO 7 do DESENHO (o conserto da R3: as falas 29 em diante por sha256, os sha16 da revisao R3, do pedido, do candidato revisado e do painel, a ORDEM KIMI H0DN-03B por sha256)"
_ADENDO7_TXT = open(ADENDO7_ARQ, "rb").read().decode("utf-8")
_RX_FALA_ADENDO7 = r"(?m)^- fala (\d+) \| na pedra (\d+) \| `work\\cunhagens_13out\\(OPERADOR_10nov_[A-Za-z0-9_]+_verbatim\.txt)` \| sha256 `([0-9a-f]{64})`\r?$"
FALAS_DO_ADENDO7 = [(int(a_), int(b_), n_, h_) for a_, b_, n_, h_ in re.findall(_RX_FALA_ADENDO7, _ADENDO7_TXT)]   # (numero no um.py, numero na pedra, arquivo, sha256)
NOMES_FALAS_DO_ADENDO7 = tuple(f_[2] for f_ in FALAS_DO_ADENDO7)
assert FALAS_DO_ADENDO7 and NOMES_FALAS_DO_ADENDO7[0] == N_QUARTO_NOME and len(set(NOMES_FALAS_DO_ADENDO7)) == len(NOMES_FALAS_DO_ADENDO7), "o ADENDO 7 nao traz as linhas das falas, ou a primeira nao e' a do quarto nome"
(_N29_, N_RATIFICADO_SEM_LOOP, N_ESCALA_DA_LUZ, N_SEM_ESCALA_NAO_TEM_FITA, N_TUDO_DEPENDE, N_SELECAO_OBSERVADOR, N_DOIS_DOMINIOS, N_ESCALA_RELATIVIDADE, N_PAR, N_BETA_INVARIANTE, N_REFUTE, N_CONFIRMO_SINGULARIDADE) = NOMES_FALAS_DO_ADENDO7   # (o desempacotamento prende a ORDEM e a QUANTIDADE das falas do adendo aos nomes usados abaixo; o conteudo de cada uma e' conferido pelos trechos citados, em FRASES_V410)
assert [f_[0] for f_ in FALAS_DO_ADENDO7] == list(range(len(NOMES_V410_DO_DESENHO) - len(FALAS_DO_ADENDO7) + 1, len(NOMES_V410_DO_DESENHO) + 1)) and len({f_[0] - f_[1] for f_ in FALAS_DO_ADENDO7}) == 1 and len(set(NOMES_V410_DO_DESENHO)) == len(NOMES_V410_DO_DESENHO) \
    and all(hashlib.sha256(open(os.path.join(_CUN13, n_), "rb").read()).hexdigest() == h_ for _, _, n_, h_ in FALAS_DO_ADENDO7), "(ADENDO 7) os numeros das falas nao sao os da posicao na tupla, ou o numero na pedra nao acompanha, ou uma fala em disco nao tem o sha256 que o adendo deu"
_PREFIXOS_TXT = _DESENHO_TXT + "\n" + _ADENDO2_TXT + "\n" + _ADENDO3_TXT + "\n" + _ADENDO5_TXT + "\n" + _ADENDO6_TXT + "\n" + _ADENDO7_TXT   # (as falas de 10/11 entram pelos ADENDOS 2, 3, 5, 6 e 7, que as citam por sha256: o DESENHO nao as cita)
_m_o3b = re.search(r"(?m)^- ORDEM KIMI H0DN-03B \| `work\\h0dn_bg1_v410_09nov\\(ORDEM_KIMI_H0DN_03B_10nov\.md)` \| sha256 `([0-9a-f]{64})`\r?$", _ADENDO7_TXT); assert _m_o3b, "o ADENDO 7 nao traz o sha256 da ORDEM KIMI H0DN-03B"
H0DN_ORDEM03B_ARQ = os.path.join(WK, "h0dn_bg1_v410_09nov", _m_o3b.group(1))
_b_o3b = open(H0DN_ORDEM03B_ARQ, "rb").read()
assert hashlib.sha256(_b_o3b).hexdigest() == _m_o3b.group(2), "a ORDEM KIMI H0DN-03B em disco NAO tem o sha256 que o ADENDO 7 deu"
ADENDO7_SHA16 = sha16_arquivo(ADENDO7_ARQ)   # (lido ao vivo do arquivo; o adendo e' citado so' por sha16)
NOMEACAO_D108_SHA256 = sha256_arquivo(os.path.join(_CUN13, N_QUARTO_NOME))   # (a fala 29, lida do arquivo)
assert ("sha256 `" + NOMEACAO_D108_SHA256 + "`") in _ADENDO7_TXT and NOMEACAO_D108_SHA256[:16] == VERBATIM_PREFIXOS_DA_ORDEM_V410[N_QUARTO_NOME], "a fala em disco nao e' a que o ADENDO 7 (o quarto nome) pina por sha256"
_m7r = re.search(r"`revisao_terceiro\\REVISAO_TERCEIRO_v410\.json` sha16 `([0-9a-f]{16})`; pedido de corre\u00e7\u00e3o sha16 `([0-9a-f]{16})`; candidato revisado `([0-9a-f]{16})`", _ADENDO7_TXT); assert _m7r, "o ADENDO 7 nao traz os sha16 da revisao R3"
REVISAO_R3 = {"revisao_sha16": _m7r.group(1), "pedido_sha16": _m7r.group(2), "candidato_revisado_sha16": _m7r.group(3)}
PAINEL_R3_ARQ = os.path.join(HERE, "PAINEL_R3_v410_RESULTADO.json"); PAINEL_R3_SHA16 = sha16_arquivo(PAINEL_R3_ARQ); assert ("`" + PAINEL_R3_SHA16 + "`") in _ADENDO7_TXT, "o resultado do painel R3 em disco nao e' o que o ADENDO 7 cita por sha16"
~~~~

## 6. O teste do cetico

Um adendo de teste foi montado com as linhas das secoes 1 a 4 (so' as linhas; com prosa antes; com prosa “hostil” antes) e lido pelos regex tirados do delta aplicado em memoria, com LF e com CRLF. Depois, os blocos novos do delta foram executados um a um, numa copia, com esse adendo, as falas reais, o recibo real do autor da R6 e um recibo dos nomes simulado como a instrucao do item 149 manda: todos os asserts passam.

| caso | falas lidas | prefixos das 40 | pino da 03B | revisao, pedido, candidato | painel |
|---|---|---|---|---|---|
| so' as linhas (LF e CRLF) | 12 | certos | lido, sha256 confere | lidos | confere |
| prosa antes, sem citar fala (LF e CRLF) | 12 | certos | lido | lidos | confere |
| prosa antes citando uma fala e outro hash | 12 | UM ERRADO: o delta recusa | lido | lidos | confere |
