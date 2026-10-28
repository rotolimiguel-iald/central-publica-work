import pathlib
p = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes\finalizar.py')
s = p.read_text(encoding='utf-8')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a))
    s = s.replace(a, b)


rep("subprocess.run([sys.executable, '-X', 'utf8', str(W / 'fontes' / 'montar_conferencia.py')], check=True)",
    "subprocess.run([sys.executable, '-X', 'utf8', str(W / 'fontes' / 'montar_conferencia.py'), '050576'], check=True)   # MQC congelado: nao se regenera")
rep("ts = (W / '_tmp' / 'ts_backup.txt').read_text().strip()", "ts = (W / '_tmp' / 'ts_backup.txt').read_text().strip()\nts3 = (W / '_tmp' / 'ts_backup_r3.txt').read_text().strip()\nmqc_antes = (W / '_tmp' / 'mqc_hashes_antes_r3.txt').read_text().split()")
rep("nomes += ['ALTERNATIVA_FOLHA_1_050576_PHOT.pdf', 'CARTA_REGRA_26_4_050576_PHOT.md', 'CARTA_REGRA_26_4_050576_PHOT.pdf']",
    "nomes += ['ALTERNATIVA_FOLHA_1_050576_PHOT.pdf', 'FOLHAS_SUBSTITUTIVAS_050576_VARIANTE_PHOT.pdf', 'CARTA_REGRA_26_4_050576_PHOT.md', 'CARTA_REGRA_26_4_050576_PHOT.pdf']")
rep("for nome in ('prancha_antes_depois_050576.png', 'prancha_antes_depois_050579.png', 'reparos_rodada2.json', 'mqc_legendas_do_depositado.json'):",
    "for nome in ('prancha_antes_depois_050576.png', 'prancha_antes_depois_050579.png', 'reparos_rodada2.json', 'mqc_legendas_do_depositado.json', 'contato_texto_grafico_r3.json'):")
rep("old_bak = {f:", "bak3 = {f: sha(W / (f + '.bak_' + ts3))[:16] for f in ('FOLHAS_SUBSTITUTIVAS_050576.pdf', 'ALTERNATIVA_FOLHA_1_050576_PHOT.pdf', 'CARTA_REGRA_26_4_050576.pdf', 'CARTA_REGRA_26_4_050576_PHOT.pdf', 'CONFERENCIA_050576.json', 'README.md', 'ESTADO.json')}\nmqc_depois = [sha(W / n)[:16] for n in ('FOLHAS_SUBSTITUTIVAS_050579.pdf', 'CARTA_REGRA_26_4_050579.pdf', 'CONFERENCIA_050579.json')]\nct3 = json.load(open(W / 'conferencia' / 'contato_texto_grafico_r3.json', encoding='utf-8'))\nold_bak = {f:")
rep("    'estado': 'REPAROS_DA_REVISAO_APLICADOS__AGUARDA_SEGUNDA_RODADA_DE_REVISAO__NADA_ENVIADO',",
    "    'estado': 'RODADA_3_R2-1_REPARADO__050576_AGUARDA_RECONFERENCIA_SO_DO_R2-1__050579_ACEITA_E_CONGELADA__NADA_ENVIADO',")
rep("    'backups_da_rodada_1': {'sufixo': '.bak_' + ts, 'sha16': old_bak},",
    "    'backups_da_rodada_1': {'sufixo': '.bak_' + ts, 'sha16': old_bak},\n    'backups_da_rodada_3': {'sufixo': '.bak_' + ts3, 'sha16': bak3},\n    'MQC_050579_congelado': {'sha16_antes_da_rodada_3 (FOLHAS, CARTA.pdf, CONFERENCIA)': [x for x in mqc_antes], 'sha16_depois': mqc_depois, 'inalterado': [a[:16] == b[:16] for a, b in zip(mqc_antes, mqc_depois)] if False else (mqc_antes == mqc_depois)},\n    'revisao_rodada_2': {'050579': 'ACEITA (congelado)', '050576': 'ACEITA COM REPAROS: unico bloqueio R2-1 (grade tocava o pe do V de VACUUM); reparado na rodada 3'},")
rep("    'testes_novos': {", "    'testes_novos': {'contato texto x grafico (pixel a pixel, 600 dpi; rodada 3)': {'050576_rodada2_antes': ct3['rodada2_050576 (a266d4a46594b3b2, antes do reparo R2-1)']['total_de_contatos'], '050576_principal_depois': ct3['rodada3_050576_principal']['total_de_contatos'], 'variante_PHOT_depois': ct3['rodada3_050576_variante_PHOT']['total_de_contatos'], 'MQC_so_leitura': ct3['MQC_050579_congelado (so leitura)']['total_de_contatos']},\n                     ")
rep("        'SEGUNDA RODADA DE REVISÃO, só dos pontos reparados (README, seção «Rodada 2»); a B4 do operador segue bloqueada até ACEITA',",
    "        'RECONFERÊNCIA só do R2-1 (README, seção «Rodada 3») para o Aprendizado; a B4 do operador segue bloqueada até ACEITA (050576); o MQC já está ACEITA',")
rep("Preparado em 27/10/2026 por `sonnet-ro106-preparador`, por decisão do operador: *«a Central prepara as folhas substitutivas e a carta da Regra 26.4 para eu liberar»*.\n**Rodada 2:**",
    "Preparado em 27/10/2026 por `sonnet-ro106-preparador`, por decisão do operador: *«a Central prepara as folhas substitutivas e a carta da Regra 26.4 para eu liberar»*.\n**Rodada 3 (só Aprendizado 050576):** a segunda revisão deu ACEITA ao MQC 050579 (congelado: nada dele foi tocado) e ACEITA COM REPAROS ao Aprendizado, com **um** bloqueio (R2-1); está reparado e há duas sugestões aplicadas (seção «Rodada 3»).\n**Rodada 2:**")
rep("    ('ALTERNATIVA_FOLHA_1_050576_PHOT.pdf', 'só a folha 1/6 com «PHOT» inteiro, para o agente de PI escolher (as folhas 2-6 são as mesmas)'),",
    "    ('ALTERNATIVA_FOLHA_1_050576_PHOT.pdf', 'só a folha 1/6 com «PHOT» inteiro, para o agente de PI escolher (as folhas 2-6 são as mesmas)'),\n    ('FOLHAS_SUBSTITUTIVAS_050576_VARIANTE_PHOT.pdf', 'VARIANTE PHOT completa: 6 folhas (1/6 alternativa + 2/6 a 6/6 iguais às principais), para ser enviada sozinha'),")
rep("## Numeração das folhas (achado da coordenação, registrado)", '''## Rodada 3 (Aprendizado 050576; o MQC 050579 está ACEITA e congelado)

* **R2-1 (único bloqueio):** na Fig. 3 (folha 2/6) a linha horizontal da grade em θ = 20 tocava o pé do «V» de «VACUUM 6 bits» (28 px a 600 dpi, segundo a revisão). **Reparo:** lacuna da grade ampliada (θ = 20 interrompida entre x = 0,036 e 0,104; a vertical x = 0,1 interrompida entre θ = 15 e 75; o rótulo ocupa θ 18,7-71,6 e x 0,044-0,087 em unidades do eixo). **Medida antes -> depois:** teste de contato texto x gráfico (novo, abaixo) {ct3['rodada2_050576 (a266d4a46594b3b2, antes do reparo R2-1)']['total_de_contatos']} componente(s), {ct3['rodada2_050576 (a266d4a46594b3b2, antes do reparo R2-1)']['pixels_em_contato']} px (folha 2, «VACUUM») -> **0** nas 6 folhas principais, nas 6 da variante PHOT e na folha alternativa; palavras cruzadas por traço (vetorial, ajustado): {res['050576']['palavras_cruzadas_por_traco_total']}; oclusões: {res['050576']['oclusoes_total']}; marcação do RO livre: {res['050576']['folhas_com_marcacao_do_RO_livre']}/6.
* **O teste agora pega o caso.** (1) *Contato texto x gráfico* (`conferir.py: contato_texto_grafico`): texto e gráfico renderizados em separado (600 dpi, sem antialias; redação em cópia na memória) e contato = pixel de tinta comum, componentes >= 3 px, excluída a régua do radical. Sobre o PDF da rodada 2 acusa a folha 2 («VACUUM», 25 px); sobre os PDFs desta rodada, 0 em todas as folhas. (2) O teste vetorial «palavras cruzadas por traço» **não via** o caso porque reduzia a caixa da palavra em 4% ao longo do texto e o pé do «V» fica na ponta de «VACUUM»; a redução ao longo do texto agora é 0% (a perpendicular segue 22%): acusa a folha 2 da rodada 2 e passa nas reparadas. Rodado sobre todas as folhas de ambas as variantes: 0. O MQC foi rodado só para leitura no teste de contato: 0 (`conferencia/contato_texto_grafico_r3.json`).
* **Sugestão 1 aplicada:** `FOLHAS_SUBSTITUTIVAS_050576_VARIANTE_PHOT.pdf` (6 folhas: 1/6 alternativa + 2/6 a 6/6 iguais às principais — texto e pixels a 100 dpi conferidos), passa em todos os testes; a carta da variante PHOT cita esse arquivo como anexo.
* **Sugestão 2 aplicada:** item 3(c) das duas cartas do Aprendizado: «algarismos, maiúsculas e letras com haste com altura mínima de 0,32 cm (inclusive nos sinais de referência)». A carta do MQC não foi tocada.
* **Sugestão da revisão (linha da Fig. 3, aplicada):** «VACUUM 6 bits» passou da horizontal para a vertical (mesmo texto).
* **MQC congelado:** hashes antes e depois desta rodada iguais ({', '.join(mqc_antes)} -> {', '.join(mqc_depois)}); `CONFERENCIA_050579.json`, folhas e carta do MQC não foram regenerados.
* Backups desta rodada: `*.bak_{ts3}`.

## Numeração das folhas (achado da coordenação, registrado)''')
rep("python fontes\\\\carta.py ; python fontes\\\\prancha.py ; python fontes\\\\finalizar.py", "python fontes\\\\contato_json.py ; python fontes\\\\carta.py ; python fontes\\\\prancha.py 050576 ; python fontes\\\\finalizar.py     # rodada 3: carta.py so gera o Aprendizado (use `carta.py mqc` para o MQC)")
p.write_text(s, encoding='utf-8')
print('ok')
