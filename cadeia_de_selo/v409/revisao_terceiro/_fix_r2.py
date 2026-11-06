p = "fechar_revisao_r2.py"
t = open(p, encoding="utf-8").read()
marca = "achados = [M1] + B\n"
novo = '''B.append({"sev": "BAIXO", "onde": "RELATORIO_PREPARACAO_v409.md linha 65 (§5, item 2, «Dizer ao operador, na lingua dele (regra do posto), o que a v409 NAO entrega»)", "achado": "O relatorio de preparacao (nao publico, mas e' o roteiro do que a gerencia le ao operador) ainda lista entre o que a v409 «NAO entrega»: «o par na face de Fock segue aberto (D60); o Omega do psion e o uniforme da instancia tem a mesma forma, e que sejam o mesmo segue aberto». O par esta' LIGADO (kernel, registro, artigo) e a identidade esta' PODADA. Se a gerencia ler o roteiro como esta', repete ao operador o [OPEN] errado (regra do posto: a partitura tem de dizer o que o teste decide e nao decide). O texto e' gerado por gerar_relatorio_v409.py e nao foi regenerado com a D60 revista.", "evidencia": "RELATORIO_PREPARACAO_v409.md:65 (mtime 22:37, depois da correcao); h_guardas_out.txt «GUARDA ACHOU em RELATORIO_PREPARACAO_v409.md ... F41».", "correcao": "Corrigir a linha no gerar_relatorio_v409.py («o par na face de Fock esta' ligado nesta versao; a identidade Omega = uniforme esta' podada, a ponte e' a inscricao») e regenerar; nao muda o candidato.", "estado_na_R2": "NOVO (ja' presente na R1, nao anotado por mim)"})
'''
assert marca in t
t = t.replace(marca, novo + marca)
open(p, "w", encoding="utf-8", newline="\n").write(t)
