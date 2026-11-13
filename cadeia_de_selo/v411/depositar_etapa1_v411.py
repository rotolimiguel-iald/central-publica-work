# -*- coding: utf-8 -*-
"""depositar_construtor_v411.py -- o deposito do claude-construtor-v411 na FILA DA MEMORIA (memory\\fila\\depositos\\claude-construtor-v411\\), no formato de memory\\fila\\README.md: so' acrescimo (nunca edita deposito
existente); as fontes com sha256 LIDO. O construtor NAO escreve MEMORY.md nem topicos (so' a gerencia c1). uso: python -B -X utf8 depositar_construtor_v411.py"""
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
FILA = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "fila", "depositos", "claude-construtor-v411")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
P = json.load(open(os.path.join(HERE, "PRONTO_PARA_CANDIDATO_v411.json"), encoding="utf-8"))
fontes = [os.path.join(HERE, n_) for n_ in ("PRONTO_PARA_CANDIDATO_v411.json", "TESTE_H0DN_OFFLINE_v411.json", "PREVOO_GERADOR_v411.json", "PRECONDICOES_v411.json")] + [os.path.join(HERE, "kernel", "KERNEL_RECIBO_v411.json")]
agora = datetime.datetime.now()
o = P["registro_h0dn_bg1_v411"]["offline"]; k = P["kernel_k411c"]
txt = ("v411 (o teste decisivo: H0DN x BG1 aberto; a emenda e o resultado recalculado no rito) em preparacao por claude-construtor-v411 para a gerencia c1, 12/11/2026: ETAPA 1 concluida; o candidato NAO foi gerado porque "
       "TOPO_RATIFICADO_v411.json nao existe (DESENHO 5.1 b: sem a palavra do operador sobre o texto do topo o candidato nao e' gerado). Nada instalado; o rito nao rodou; o Nos so' lido.\n\n"
       "[REAL, lido dos artefatos] Kernel: sandbox C:\\t\\k411c\\final (copia do k410c, robocopy sem /PURGE; fontes = as do Nos v410, 1764 de 1764); build incremental %s s sem compilar nada; Audit %s s com o log de MESMOS bytes "
       "que o da v410; TOTAL decl %s, thm %s, fora do trio %s; escada %s (a da v410); nenhuma bandeira nova; recibo do kernel sha16 %s.\n\n"
       "Registro h0dn_bg1_v411 (16 checagens; os tres modulos pinados executados dos bytes embutidos, na ordem do executor): offline %s/16, o recalculo IDENTICO ao resultado da abertura (max dif 0,0); sob o modelo de erros publicado, "
       "o primario le Z nulo %.4f e Z K %.4f (ramo %s); ao lado, no mesmo item, as Cefeidas livres leem Z nulo %.4f e Z K %.4f (ramo %s); retrodicao sem ajuste, com emenda posterior a guarda; teste nao cego; provado e' validade, "
       "nao creditacao; o gate nao se move. Cada um dos 10 controles negativos recusa so' a checagem visada. Pre-voo do gerador com a PROPOSTA do topo: 25 patches, todas as assercoes e as guardas (tambem no texto renderizado) "
       "limpas; nenhum candidato gravado. Guarda de material privado da E03 da G1 sobre os 78 insumos e copias: limpa (D133).\n\n"
       "Avisos para a gerencia: (1) %d scripts ainda com a marca de copia mecanica (o corpo da v410): ensaio a seco, esperados, conferidores, relatorio, orquestrador e pos-rito; o p00 da v411 (reescrito) FALHA so' por isso; "
       "(2) a guarda de frases da v411 tira duas regras da v410 superadas pela abertura (a F54; da F56 so' o teste aberto) e acrescenta F60 a F67 (a F67: as quatro obrigacoes no mesmo bloco do resultado); "
       "(3) a cabeca exata do teste traz o par de tokens que a P18 da v392 recusa: no texto renderizado ela aparece inteira e a P18 e' aplicada com ela retirada; quem passar a P18 crua no artigo, no handoff ou no selo tera' de dizer a mesma excecao; "
       "(4) o gerador ainda nao faz a troca das seis aberturas da secao da Escala (medidas: 6) nem a medida do A2; (5) o titulo EN do quadro e a frase EN ao lado do estatuto sao traducao do construtor.\n\n"
       "Quem constroi nao aprova: a revisao de terceiro, fechar_preparacao, acom_inscrever_prep, o pino do memoria.py e a folga do MEMORY.md, a tarefa agendada, o rito e a custodia sao da gerencia. Mapa de Rotas: cadeia.preparacao_v411 (seq 2020).\n") % (
    k["duracao_build_s"], k["duracao_audit_s"], k["linha_TOTAL"]["decl"], k["linha_TOTAL"]["thm"], k["linha_TOTAL"]["fora_do_trio"], k["escada"][0], k["recibo"]["sha16"],
    o["n_ok"], o["primario"]["z_null"], o["primario"]["z_tgl"], o["primario"]["ramo"], o["cefeidas_livres"]["z_null"], o["cefeidas_livres"]["z_tgl"], o["cefeidas_livres"]["ramo"], P["n_scripts_a_adaptar"])
cab = ("---\nquem: claude-construtor-v411\ncasa: Central de Patentes\ntipo: project\nestatuto: REAL\nalvo_sugerido: novo:v411-preparacao-etapa1-12nov\ndepositado_em: %s\nfontes:\n" % agora.astimezone().isoformat(timespec="seconds")
       + "".join("  - %s  sha256:%s\n" % (p_, sha(p_)) for p_ in fontes) + "---\n")
os.makedirs(FILA, exist_ok=True)
dst = os.path.join(FILA, agora.strftime("%Y%m%d_%H%M%S") + "_v411-preparacao-etapa1-12nov.md")
assert not os.path.exists(dst)
b = (cab + txt).encode("utf-8"); open(dst + ".tmp", "wb").write(b); assert os.path.getsize(dst + ".tmp") == len(b); os.replace(dst + ".tmp", dst)
print(dst, hashlib.sha256(b).hexdigest()[:16], len(b))
