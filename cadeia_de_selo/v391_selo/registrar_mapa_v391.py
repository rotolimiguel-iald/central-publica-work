# -*- coding: utf-8 -*-
"""Registro no mapa de rotas: o exame de coerencia do artigo (v390) e o selo v391 (o estatuto da prova). Rodar DEPOIS da cadeia (handoff gravado)."""
import json, os, re, subprocess, sys, hashlib
sys.stdout.reconfigure(encoding="utf-8")
MAPA = r"C:\IALD\MAPA_DE_ROTAS"; NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"; PK = r"C:\IALD\Central de Patentes\work\v391_pacote"
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
ep = core.get("estatuto_da_prova_v391") or {}
um16 = hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()[:16]
assert selo.get("um_version") == "v391" and ep.get("all_verified") is True, "o selo nao e a v391 selada"
quem = None
for line in open(os.path.join(MAPA, "rotas.jsonl"), encoding="utf-8"):
    try: d = json.loads(line)
    except ValueError: continue
    if d.get("seq") == 699: quem = d["quem"]
arts = [os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(PK, "OPERADOR_07out_estatuto_verbatim.txt"), os.path.join(PK, "conferir_citacoes_v391.json"),
        os.path.join(PK, "ensaio_a_seco_v391.json"), os.path.join(NOS, "HANDOFF_v391_CUSTODIA.md")]
arts = [a for a in arts if os.path.exists(a)]
REG = [{"tipo": "ROTA", "rota_id": "umpy.v391.estatuto_da_prova", "dominio": "KERNEL_FORMAL", "status": "EXAMINADA", "estatuto": "REAL", "olhou_dados": False,
        "titulo": "v391 SELADA %s: o estatuto da prova -- provada (validade; kernel + ritos com falsificadores pre-registrados + GPU contam juntos); a confirmacao recusada e' CREDITACAO, nao validade" % um16,
        "pergunta": "o artigo (v390) e' coerente com a regua do operador de 07/10 (a confirmacao proibida e' de creditacao, nao de validade)?",
        "dados": ["nenhum dado novo: leitura dos registros do core v390/v391"],
        "metodo": "exame do .txt PT/EN da v390 (frases de status); registro estatuto_da_prova_v391 lendo do core a cada rito; resumo aberto pelo estatuto; errata ao lado das 8 frases de epoca por lingua; titulo da Introducao lendo a versao (corte por versao no registro da v389)",
        "resultado": "incoerencias achadas na v390: o resumo nunca afirmava o positivo; 8 frases de epoca por lingua liam a recusa como ausencia de prova contra o selo (Einstein emergente concreto, testemunha plena e 18 bandeiras TRUE); v391: %s" % ep.get("verdict"),
        "veredito": "", "defeito": "o operador listou como provados itens que o registro mede de outro modo: o piso dos vazios e' teste unilateral (o LCDM raso passa); o dephasing na natureza nao foi testado decisivamente (a GPU calcula o sistema da teoria); das 9 rotas de eco fora do livro, 5 foram excluidas pelo dado; o Luminidio tem retratacao decidida pelo operador em 21/08 -- o artigo diz cada item como o registro mede",
        "nao_refazer": "o exame de coerencia esta feito; o README e o site foram atualizados por outra sessao (18:20-18:27) com o mesmo estatuto -- a gerencia c1 nao os tocou",
        "proximo_passo": "operador: ratificar a v391; custodia (sessao do site); subir README/site; commit/push",
        "onde": PK, "artefatos": arts, "refs": ["kernel.lema3.superposicao_e_a_passagem_07out", "discriminante.ordem018.auditoria_gerencia_06out"],
        "nota": "PROVADA = validade; CONFIRMADA = creditacao (a unica palavra recusada); NOT_FALSIFIED nunca e' confirmacao; o gate nao se move"}]
J = os.path.join(os.path.dirname(os.path.abspath(__file__)), "registro_mapa_v391.json"); json.dump(REG, open(J, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
r = subprocess.run([sys.executable, os.path.join(MAPA, "rotas.py"), "registrar", J, "--quem", quem], capture_output=True, text=True, encoding="utf-8", errors="replace")
print("mapa rc", r.returncode, re.findall(r'"seq": (\d+)', r.stdout), r.stderr[-300:])
