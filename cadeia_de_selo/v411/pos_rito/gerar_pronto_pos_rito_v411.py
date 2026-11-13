# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026, claude-construtor-v411-posrito, a servico da gerencia c1] grava PRONTO_POS_RITO_v411.json na pasta da cadeia: o estado da frente POS-RITO, com tudo LIDO dos arquivos (sha16, saidas dos testes, textos)
"""gerar_pronto_pos_rito_v411.py -- le os scripts da frente pos-rito (pos_rito\\, orquestrador\\), as saidas dos testes (em C:\\t\\k411c\\ensaio_topo_proposto\\, fora de work\\), os relatorios dos agentes L, M e H e o
arquivo ratificado do topo, e grava ...\\v411\\PRONTO_POS_RITO_v411.json (temporario -> conferir -> substituir; backup de bytes se ja' existir). Nao roda teste nenhum: so' le o que os testes gravaram.
uso: python -B -X utf8 gerar_pronto_pos_rito_v411.py"""
import datetime
import hashlib
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent; PK = HERE.parent
ENS = Path(r"C:\t\k411c\ensaio_topo_proposto")
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
MARCA = "[A ADAPTAR v" + "411]"   # (partida: este arquivo nao pode conter a marca inteira)


def j(p):
    p = Path(p)
    return json.loads(p.read_bytes().decode("utf-8")) if p.is_file() else None


def bak_mais_novo(p):
    c = sorted(Path(p).parent.glob(Path(p).name + ".bak_*"), key=lambda x: x.stat().st_mtime)
    return {"backup": c[-1].name, "sha16": s16(c[-1])} if c else None


QUEM = {"textos_custodia_handoff_v411.py": "construtor (reescrito)", "blocos_custodia_v411.py": "construtor (novo)", "teste_blocos_custodia_v411.py": "construtor (novo)",
        "teste_textos_custodia_sem_candidato_v411.py": "construtor (reescrito)", "teste_gatilho_custodia_sem_candidato_v411.py": "construtor (reescrito)", "gerar_pronto_pos_rito_v411.py": "construtor (novo)",
        "leitura_v411.py": "agente L (Sonnet) + construtor (a condicao t9 que um comentario engolia, achado do agente H)", "textos_v411.py": "agente L", "textos_v411.semente": "agente L", "textos_v411_novo.pysnip": "agente L",
        "fechar_v411.py": "agente L", "superficies_v411.py": "agente L", "montar_textos_v411.py": "agente L", "gerar_derivacao_pos_rito_v411.py": "agente L", "fila_memoria_v411.py": "agente L",
        "b3_recibo_v411.py": "agente L", "teste_textos_sem_candidato_v411.py": "agente L (novo)", "registrar_mapa_v411.py": "agente M (Sonnet)", "gerar_x_custodia_v411.py": "agente M",
        "chain_pos_rito_v411.sh": "agente M", "teste_mapa_sem_candidato_v411.py": "agente M", "teste_x_custodia_sem_candidato_v411.py": "agente M", "consts_mapa_x_v411.py": "agente M (novo)",
        "harness_fechar_sandbox_v411.py": "agente H (Sonnet)", "harness_textos_ensaio_v411.py": "agente H"}
scripts = {}
for nome, quem in QUEM.items():
    p = HERE / nome
    if p.is_file():
        t = p.read_bytes().decode("utf-8", "replace")
        scripts["pos_rito/" + nome] = {"sha16": s16(p), "bytes": p.stat().st_size, "quem": quem, "marca_de_copia_mecanica": MARCA in t, "backup_mais_novo": bak_mais_novo(p)}
po = PK / "orquestrador" / "pos_treino_v411.py"
scripts["orquestrador/pos_treino_v411.py"] = {"sha16": s16(po), "bytes": po.stat().st_size, "quem": "construtor", "marca_de_copia_mecanica": MARCA in po.read_text(encoding="utf-8"), "backup_mais_novo": bak_mais_novo(po)}
assert not any(v["marca_de_copia_mecanica"] for v in scripts.values()), "sobrou script com a marca de copia mecanica"

TB = j(ENS / "pos_rito_blocos" / "TESTE_BLOCOS_CUSTODIA_v411.json") or {}
TT = j(ENS / "pos_rito_textos" / "TESTE_TEXTOS_CUSTODIA_SEM_CANDIDATO_v411.json") or {}
TG = j(ENS / "pos_rito_gatilho" / "TESTE_GATILHO_CUSTODIA_v411.json") or {}
AL, AM, AH = j(HERE / "ADAPTACAO_L_v411.json"), j(HERE / "ADAPTACAO_M_v411.json"), j(ENS / "pos_rito" / "ADAPTACAO_H_v411.json")
TOPO = PK / "TOPO_RATIFICADO_v411.json"
tmp = sorted(str(p.relative_to(PK)) for p in PK.rglob("*.tmp") if p.is_file())
n_arq = sum(1 for p in PK.rglob("*") if p.is_file())
pronto_ensaio = (ENS / "PRONTO_PARA_O_POS_RITO.json").is_file()
out = {
    "contrato": "PRONTO_POS_RITO_v411", "quando": datetime.datetime.now().isoformat(timespec="seconds"), "agente": "claude-construtor-v411-posrito (frente POS-RITO), a servico da gerencia c1",
    "estado": "FRENTE POS-RITO ADAPTADA E TESTADA SEM O CORE DA v411; os harnesses de fechar adaptados mas NAO rodados contra o falso Nos de ensaio (PRONTO_PARA_O_POS_RITO.json %s)" % ("existe" if pronto_ensaio else "ausente"),
    "orquestrador": {"arquivo": "orquestrador/pos_treino_v411.py", "passos": "S0 a S9 sem S7 e sem S10; o fim e' o HANDOFF (S6d) e o gatilho da custodia (S9_gatilho_custodia); tarefa IALD_pos_treino_v411 (gerencia); teto do rito 5 h; nada de publicacao",
                     "aut": "a ordem de 12/11/2026 (delta_v411.FALA_ORDEM_V411: nome e sha256; a fala inteira lida do arquivo); avaliavel so' com _DL e AUT_FRASE, como o conferidor estatico do servico (medido: sha16, fala inteira, 12/11/2026, nenhuma data de 01 a 11/11)",
                     "custodia_sem_ordem": "D174: a custodia da v411 roda SEM --ordem (vale a regra permanente de 23/10, citada no gatilho por arquivo e sha16); a fala do testemunho de 12/11 e' a ordem do CONTEUDO (D170), citada sem ir em argumento; o gatilho que traga --ordem e' recusado (negativo no teste)", "plano_rc": "--plano: so' faltam um_v411_candidato.py e ESPERADOS_v411.json (da outra frente)"},
    "scripts": scripts,
    "testes": {
        "teste_blocos_custodia_v411.py": {"como": "o core da v410 selada (Nos, so' leitura) + o registro do ensaio offline no lugar de h0dn_bg1_v411; as conferencias DA CUSTODIA (custodia_g1.h0dn.conferir_bloco, textos.portao, readme_pinado.regra_444) + a F67 estrita + a guarda de frases da v411; controles negativos; o README projetado pelo renderizador da custodia (primordial.montar + readme_pinado.renderizar) com o handoff de ENSAIO da v411 (sufixo _v411; HANDOFF_v411_CUSTODIA.md em pos_rito_blocos) e o selo carregado dizendo v411, em memoria",
                                          "ok": TB.get("ok"), "falhas": len(TB.get("falhas") or []), "saida": str(ENS / "pos_rito_blocos" / "TESTE_BLOCOS_CUSTODIA_v411.json"), "sha16_saida": s16(ENS / "pos_rito_blocos" / "TESTE_BLOCOS_CUSTODIA_v411.json") if TB else None},
        "teste_textos_custodia_sem_candidato_v411.py": {"como": "o S6d inteiro (textos_custodia_handoff_v411.main) contra um Nos SINTETICO de ensaio; o parser do G1 le os 27 marcadores; controles negativos de entrada e das guardas", "ok": TT.get("ok"), "falhas": len(TT.get("falhas") or []),
                                                        "saida": str(ENS / "pos_rito_textos" / "TESTE_TEXTOS_CUSTODIA_SEM_CANDIDATO_v411.json")},
        "teste_gatilho_custodia_sem_candidato_v411.py": {"como": "o S9_gatilho_custodia do orquestrador REAL em sandbox, sobre o handoff que o S6d de verdade gravou; positivo, repeticao e 20 negativos (um novo: texto com --ordem recusado); o gatilho de verdade nao e' tocado", "tudo_passou": TG.get("tudo_passou"),
                                                         "casos": TG.get("n_casos"), "negativos": TG.get("n_negativos"), "saida": str(ENS / "pos_rito_gatilho" / "TESTE_GATILHO_CUSTODIA_v411.json")},
        "teste_textos_sem_candidato_v411.py (agente L)": {"como": "V sintetico do registro offline; as funcoes de texto de textos_v411 nas guardas; os leitores novos com 15 adulteracoes", "resultado": "80 etapas, 0 falhas (rerodado pelo construtor depois da correcao do t9)"},
        "teste_mapa_sem_candidato_v411.py e teste_x_custodia_sem_candidato_v411.py (agente M)": {"resultado": "PASSOU os dois (rerodados pelo construtor; o do X com a pasta C:\\t\\k411c\\ensaio_topo_proposto\\pos_rito_x)"},
        "harnesses (agente H)": {"resultado": (AH or {}).get("o_que_testou") or "py_compile e pyflakes; sem PRONTO_PARA_O_POS_RITO.json os dois recusam com rc 3 sem escrever; o --so-fila do fechar 29/29", "rodados_contra_o_falso_nos": False}},
    "comandos_dos_harnesses": ["cd \"/c/IALD/Central de Patentes/work/cadeia_de_selo/v411/pos_rito\" && V411_ENSAIO_TOPO_PROPOSTO=1 /c/Python314/python.exe -B -X utf8 harness_textos_ensaio_v411.py",
                               "cd \"/c/IALD/Central de Patentes/work/cadeia_de_selo/v411/pos_rito\" && V411_ENSAIO_TOPO_PROPOSTO=1 /c/Python314/python.exe -B -X utf8 harness_fechar_sandbox_v411.py",
                               "(Git Bash; exigem C:\\t\\k411c\\ensaio_topo_proposto\\PRONTO_PARA_O_POS_RITO.json; sem ele rc 3 sem escrever; saidas em C:\\t\\k411c\\ensaio_topo_proposto\\pos_rito\\; o --so-fila do fechar nao exige o PRONTO)"],
    "falta_testar": ["os dois harnesses (harness_fechar_sandbox_v411.py, harness_textos_ensaio_v411.py) contra o falso Nos de ENSAIO: rodar com V411_ENSAIO_TOPO_PROPOSTO=1 quando a outra frente gravar C:\\t\\k411c\\ensaio_topo_proposto\\PRONTO_PARA_O_POS_RITO.json (e ESPERADOS_v411.json); as chaves que eles leem estao no PEDIDOS (secao do agente H)",
                     "leitura_v411.ler(), fechar_v411.py e superficies_v411.py inteiros contra o core, o selo, o stdout e o sidecar de verdade (so' com o ensaio a seco ou o rito)",
                     "o S6d (textos_custodia_handoff_v411.main) sobre o HANDOFF que o fechar_v411 gravar de verdade (o teste usou um HANDOFF minimo de ensaio) e o S6d/S9 com o ESTADO real do orquestrador",
                     "a G1 da custodia (E04/E08 com os marcadores) sobre o HANDOFF real: e' da sessao de custodia"],
    "textos_da_custodia": {"estatuto": "RATIFICADOS: saem de TOPO_RATIFICADO_v411.json (o painel curto e a frase de estado, ratificados pelo operador em 12/11/2026), cortados em oracoes inteiras para cada lugar; os numeros do core; NAO sao proposta",
                           "fonte": {"arquivo": str(TOPO), "sha256": hashlib.sha256(TOPO.read_bytes()).hexdigest()}, "renderizados_no_ensaio": TB.get("textos"), "bytes": TB.get("bytes"),
                           "marcadores_no_handoff": ["os sete da prosa da G1 (TITULO_EN, ENTROU_EN, KERNEL_LEITURA_EN, ABERTOS_EN, ARCO_EN, ARCO_PT, COMMIT)", "NOTA_EN", "README_PAINEL_H0DN", "README_FASE9_V2", "README_PRIMORDIAL_5SIGMA", "README_STATUS_5SIGMA", "README_H0DN", "README_H0DN_EN", "README_RITOS",
                                                     "os onze ESTATUTO_* (LINHA_EN, LINHA_06_EN, LINHA_06_PT, CURTO_EN, CURTO_PT_ASCII, P2_EN, SECAO_MD, LINHA_CURTA_EN, P_CURTO_EN, P2_ESTADO_EN, P2_ESTADO_PT)", "fora da lista da custodia: X_TEXTO"]},
    "readme": (TB.get("readme") or {}),
    "decisao_do_painel": {"d174": "o painel curto do README vai INTEIRO, com a frase do acervo (ordem do operador de 12/11); o corte automatico por orcamento saiu de blocos_custodia_v411.py; a conferencia: o painel e' o render inteiro do arquivo ratificado (controle negativo: sem a frase do acervo, recusado)",
                          "regra_do_teto": "o README inteiro em ate' 40.960 B, medido pelo renderizador da custodia; se nao couber, a cadeia PARA (nada e' cortado em silencio)",
                          "oracoes_inteiras_nos_textos_curtos": "README_PRIMORDIAL_5SIGMA e README_STATUS_5SIGMA levam o Z contra o nulo sem o Z contra K (o Z contra K esta' no painel, logo acima); a retrodicao na forma curta, duas oracoes inteiras do texto ratificado; as duas linhas do H0DN da parte do Clay sao apontadores (D174)"},
    "desvios_do_desenho": [
        "os blocos README_FRENTE e README_O_QUE_SAI da v410 sairam: no lugar, os marcadores da lista da custodia (sete do README, a NOTA e os onze do estatuto; README_H0DN_EN agora consumido pela G1); o bloco do Clay fica como esta' (a faixa v408–v411 e' da custodia)",
        "o gatilho da custodia nao passa ordem por argumento (D174): a regra permanente de 23/10 e a ordem do conteudo de 12/11 (D170) entram citadas por arquivo e sha16",
        "a NOTA do ledger nao cita mais o 4,44: a frase de estado ratificada diz que o teste anterior da mesma lei ficou abaixo do degrau; a linha README_FASE9_V2 traz o 4,44 com a regra",
        "a primeira frase do ARCO_EN e do ARCO_PT ficou curta (D174, D): o b_mudou da G1 leva ao README a primeira frase do ARCO_EN e o titulo do ultimo PARAGRAFO da versao",
        "o COAUTOR do orquestrador passou a ser o da atribuicao vigente da sessao (so' o S7, que esta versao nao chama, o usaria)",
        "leitura_v411.py: um comentario engolia «and t9_std_ok_ and not t9_.get('guarda_violacoes')» no bloco do traducao_turing_v409 (achado do agente H); a condicao voltou ao codigo (backup .bak_*_t9)"],
    "pedidos_a_outra_frente": "em ...\\v411\\PEDIDOS_ENTRE_FRENTES_v411.md, as secoes dos agentes L, M e H (as chaves de ESPERADOS_v411/CANDIDATO/FLAGS que a leitura e o mapa leem; vereditos_novos_v411[h0dn_bg1_v411]; quadro_v397.py ainda importa delta_v410; as chaves do PRONTO_PARA_O_POS_RITO.json; as saidas dos harnesses em DL.saida(\"pos_rito\", ...))",
    "relatorios_dos_agentes": {"L": str(HERE / "ADAPTACAO_L_v411.json") if AL else None, "M": str(HERE / "ADAPTACAO_M_v411.json") if AM else None, "H": str(ENS / "pos_rito" / "ADAPTACAO_H_v411.json") if AH else None},
    "pasta_da_cadeia": {"tmp": tmp, "arquivos_agora": n_arq},
    "o_que_nao_foi_feito_por_regra": "nada no Nos, no espelho, em tools\\custodia_g1 nem na memoria real; o orquestrador nao foi disparado; nenhuma tarefa agendada; a Bancada nao foi tocada; o treino da nativa nao foi tocado",
}
p = PK / "PRONTO_POS_RITO_v411.json"
b = json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8")
if p.exists():
    bk = p.with_name(p.name + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")); bk.write_bytes(p.read_bytes())
open(str(p) + ".tmpw", "wb").write(b); assert os.path.getsize(str(p) + ".tmpw") == len(b); os.replace(str(p) + ".tmpw", p)
print("gravado:", p, len(b), "B, sha16", s16(p), "| scripts:", len(scripts), "| .tmp na pasta:", tmp)
