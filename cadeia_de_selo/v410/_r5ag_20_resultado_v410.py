# -*- coding: utf-8 -*-
"""_r5ag_20_resultado_v410.py -- R5, agente de adaptacao: junta o RESULTADO da rodada (V\\_r5ag_RESULTADO_v410.json): os arquivos mudados com o sha16 antes -> depois (o antes e' o do backup MAIS ANTIGO da R5 de cada arquivo: `<arquivo>.bak_<AAAAMMDD_HHMMSS>_r5`, `_pre_r5`, `_pre_r5b`),
os scripts criados, cada pre-teste com o RC e a ultima linha (os rapidos sao RODADOS aqui, em subprocesso; os demorados sao LIDOS das saidas que o agente guardou, com a marca RC_*=), o sha16 do candidato de trabalho, as listas do comparar (mudados e novos),
as decisoes tomadas e as duvidas, e a comparacao dos intocados (sha16 antes do agente, guardado no scratchpad, contra agora). Todo numero e todo hash sao LIDOS aqui; nada digitado de memoria. Nao toca nenhum arquivo da cadeia: so' escreve o JSON do resultado (temporario -> os.replace).
uso: python -B -X utf8 _r5ag_20_resultado_v410.py [--sem-rodar]"""
import glob, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v410 as DL  # noqa: E402

SEM_RODAR = "--sem-rodar" in sys.argv
PY = [sys.executable, "-B", "-X", "utf8"]
S16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
SCRATCH = r"C:\Users\rotol\AppData\Local\Temp\claude\b4ca26c934d2167f\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\intocados_antes.json"


def ultima_linha(txt):
    ls = [l.rstrip() for l in txt.splitlines() if l.strip()]
    ls = [l for l in ls if not re.match(r"^RC_[A-Z0-9_]+=-?\d+$", l)]
    return (ls[-1] if ls else "")[:400]


def rc_marca(txt, marca):
    m = re.findall(r"^" + marca + r"=(-?\d+)\s*$", txt, re.M)
    return int(m[-1]) if m else None


def lido(arq, marca, pref=None):
    """pref: regex da linha-veredito (a ultima que casar), para as saidas cuja ultima linha e' so' um caminho ou um '== FIM'."""
    p = os.path.join(HERE, arq)
    if not os.path.exists(p):
        return {"saida": arq, "rc": None, "ultima_linha": "(saida ausente)"}
    t = open(p, encoding="utf-8", errors="replace").read()
    ul = ultima_linha(t)
    if pref:
        c = [l.strip() for l in t.splitlines() if re.search(pref, l)]
        if c:
            ul = c[-1][:400]
    return {"saida": arq, "rc": rc_marca(t, marca), "ultima_linha": ul}


def rodar(nome, args, cwd=None, entrada=None):
    if SEM_RODAR:   # modo de LEITURA: usa a saida que o agente guardou na ultima vez que rodou
        return lido("_r5ag_pre_" + nome + "_out.txt", "RC_PRE")
    t0 = time.time()
    r = subprocess.run(PY + args, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1800, cwd=cwd or HERE)
    t = (r.stdout or "") + (r.stderr or "")
    open(os.path.join(HERE, "_r5ag_pre_" + nome + "_out.txt"), "w", encoding="utf-8").write(t + "\nRC_PRE=%d\n" % r.returncode)
    return {"saida": "_r5ag_pre_" + nome + "_out.txt", "rc": r.returncode, "ultima_linha": ultima_linha(t), "s": round(time.time() - t0)}


R = {"contrato": "R5ag_RESULTADO_v410", "quando": time.strftime("%d/%m/%Y %H:%M:%S"), "agente": "agente de adaptacao da rodada R5 (D100 e D101; ADENDOS 5 e 6), a servico do claude-construtor-v410 e da gerencia c1",
     "pasta": HERE}

# ---- candidato de trabalho
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v410.json"), encoding="utf-8"))
cand_p = os.path.join(HERE, DL.CANDIDATO)
R["candidato_de_trabalho"] = {"arquivo": DL.CANDIDATO, "sha16": S16(cand_p), "sha16_no_CANDIDATO_json": CM["sha16"], "bytes": os.path.getsize(cand_p), "bate_com_o_json": S16(cand_p) == CM["sha16"],
                              "nota": "o candidato intermediario 28b54cf5e560beeb (gerado antes da 02c, que tirou o hash das frases) ficou VELHO em relacao ao delta; o ensaio e o pre-teste rodados sobre ele falharam em 3 partes (r5_a_clausula_do_tetelestai_no_registro, o controle r5_frase_da_ratificacao_d101_retirada_do_texto e a mensagem do ponto_aescala); o candidato foi REGERADO (V410_REGERAR=1) e tudo foi refeito sobre ele"}

# ---- arquivos mudados: antes (backup mais antigo da R5) -> depois
rx = re.compile(r"^(?P<base>.+)\.bak_(?P<ts>\d{8}_\d{6})_(?:pre_)?r5b?$")
# o INICIO do agente: a hora do primeiro arquivo dele (_r5ag_lib_v410.py); os backups `_pre_r3`, `_pre_r4` e o `_pre_r5` das 09:13 (a instalacao da pedra R5 pela gerencia) sao ANTERIORES e ficam fora da conta
INICIO = time.strftime("%Y%m%d_%H%M%S", time.localtime(os.path.getmtime(os.path.join(HERE, "_r5ag_lib_v410.py"))))
R["inicio_do_agente"] = INICIO
grupos = {}
for p in glob.glob(os.path.join(HERE, "**", "*.bak_*_*r5*"), recursive=True):
    rel = os.path.relpath(p, HERE).replace("\\", "/")
    m = rx.match(rel)
    if m and m.group("ts") >= INICIO:
        grupos.setdefault(m.group("base"), []).append((m.group("ts"), rel))
ts_min = min((min(v)[0] for v in grupos.values()), default="")
mudados, fora_da_conta = [], []
for base, v in sorted(grupos.items()):
    v.sort(); antes_rel = v[0][1]; ap = os.path.join(HERE, base)
    if not os.path.exists(ap):
        continue
    a16, d16 = S16(os.path.join(HERE, antes_rel)), S16(ap)
    mudados.append({"arquivo": base, "sha16_antes": a16, "sha16_depois": d16, "mudou": a16 != d16, "backup_mais_antigo": antes_rel, "n_backups_da_r5": len(v)})
R["arquivos_mudados"] = [m for m in mudados if m["mudou"]]
R["arquivos_com_backup_sem_mudanca_de_bytes"] = [m["arquivo"] for m in mudados if not m["mudou"]]
R["n_arquivos_mudados"] = len(R["arquivos_mudados"])
R["nota_dos_antes"] = "o sha16 'antes' e' o do backup MAIS ANTIGO da R5 do arquivo (a regra do backup imediato); os arquivos de saida regenerados (ensaio_a_seco_v410.json, PRETESTE_..., ensaio_out.txt, preteste_out_v410.txt) entram so' se tinham backup; os demais regenerados por script (ESPERADOS_v410.json, DERIVACAO_v410.json, MANIFESTO_INSUMOS_v410.json, EXAME_PONTOS_*, SIMULACAO_ARVORE_NOS_*, dry_*, imp_*, sim_*) sao SAIDA de ferramenta"

# ---- scripts criados
sc = sorted(glob.glob(os.path.join(HERE, "_r5ag_*"))) + sorted(glob.glob(os.path.join(HERE, "pos_rito", "_r5ag_*")))
R["scripts_criados"] = [os.path.relpath(p, HERE).replace("\\", "/") for p in sc if re.search(r"\.(py|sh)$", p)]
R["saidas_do_agente"] = [os.path.relpath(p, HERE).replace("\\", "/") for p in sc if p.endswith(".txt")] + sorted(os.path.relpath(p, HERE).replace("\\", "/") for p in glob.glob(os.path.join(HERE, "*_r5ag*.txt")) if not os.path.basename(p).startswith("_r5ag_"))

# ---- pre-testes (os rapidos RODAM aqui; os demorados sao LIDOS)
P = {}
if True:
    P["previa_exame_e_arvore (exame_pontos + simular_arvore)"] = rodar("previa", ["_previa_exame_e_arvore_parte2_v410.py", "ambos"])
    P["guarda_frases_v410 (limpas e controles)"] = rodar("guarda_frases", ["guarda_frases_v410.py"])
    P["_teste_aescala_offline_v410 (13 checagens e os controles negativos)"] = rodar("offline", ["_teste_aescala_offline_v410.py"])
    P["pos_rito/teste_textos_custodia_sem_candidato_v410"] = rodar("textos_custodia", [os.path.join("pos_rito", "teste_textos_custodia_sem_candidato_v410.py")])
    P["comparar_v409_v410 (nos mudados e novos)"] = rodar("comparar", ["comparar_v409_v410.py"])
    P["conferir_citacoes_v410"] = rodar("citacoes", ["conferir_citacoes_v410.py"])
    P["teste_conferidor_positivo_v410"] = rodar("conf_pos", ["teste_conferidor_positivo_v410.py"])
P["ensaio_a_seco_v410 (candidato corrente)"] = lido("ensaio_out.txt", "RC_ENSAIO")
P["_preteste_ensaio_parte2_v410"] = lido("preteste_out_v410.txt", "RC_PRETESTE")
P["refazer_do_passo4_v410.sh (gerar_esperados, conferir_rito controle e positivo, conferir_citacoes, diff_e_pinos, conferir_instalar_rito, p00)"] = lido("refazer4_out_r5ag.txt", "RC_REFAZER4", r"^PRECONDICOES v410")
P["pos_rito/harness_textos_ensaio_v410 (--nao-exigir-refazer; --out harness_saida_v410_r5ag_textos)"] = lido("harness_textos_out_r5ag.txt", "RC_HARNESS_TEXTOS", r"^VEREDITO DO HARNESS")
P["pos_rito/harness_fechar_sandbox_v410 (--nao-exigir-refazer; --out harness_saida_v410_r5ag_fechar)"] = lido("harness_fechar_out_r5ag.txt", "RC_HARNESS_FECHAR", r"^VEREDITO \(fechar")
P["gerar_relatorio_v410 --seco"] = lido("relatorio_seco_out_r5ag.txt", "RC_RELATORIO")
R["pretestes"] = P

# ---- comparar: as listas
txt_cmp = open(os.path.join(HERE, "_r5ag_pre_comparar_out.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(HERE, "_r5ag_pre_comparar_out.txt")) else open(os.path.join(HERE, "comparar_out_r5ag.txt"), encoding="utf-8").read()
j1 = json.loads(txt_cmp.splitlines()[0])
mud = None
for l in txt_cmp.splitlines()[1:]:
    mm = re.match(r"^mudados: (\[.*\])\s*$", l)
    if mm:
        mud = eval(mm.group(1), {}, {})
R["comparar"] = {"n_mudados": j1["n_mudados"], "n_novos": len(j1["novos"]), "n_removidos": len(j1["removidos"]), "mudados": mud, "novos": j1["novos"], "removidos": j1["removidos"], "iguais": j1["iguais"], "nos_nomeados_v409": j1["nos_nomeados_v409"]}
R["comparar"]["mesmas_listas_da_r4"] = bool(j1["n_mudados"] == 26 and len(j1["novos"]) == 39 and not j1["removidos"])

# ---- exame e ensaio: partes novas lidas dos JSON
try:
    ex = json.load(open(os.path.join(HERE, "EXAME_PONTOS_%s.json" % R["candidato_de_trabalho"]["sha16"]), encoding="utf-8"))
    R["exame_de_pontos"] = {"algum_falso": ex.get("algum_falso"), "ponto_aescala_all_verified": (ex.get("ponto_aescala") or {}).get("all_verified"), "ponto_aescala_checagens": (ex.get("ponto_aescala") or {}).get("mecanica"), "n_ancoras": (ex.get("ponto_aescala") or {}).get("n_ancoras"), "n_flags": (ex.get("ponto_aescala") or {}).get("n_flags"), "estatuto_dos_nomes_novos": (ex.get("ponto_aescala") or {}).get("estatuto_dos_nomes_novos"), "ratificacao_pendente": (ex.get("ponto_aescala") or {}).get("ratificacao_pendente")}
except Exception as e:  # noqa: BLE001
    R["exame_de_pontos"] = {"erro": repr(e)}

# ---- decisoes e duvidas
R["decisoes_tomadas"] = [
    "CONGELADO: VERBATIM_CONGELADO_v410.json refeito por script explicito (_r5ag_01) a partir dos arquivos das 28 falas, conservando o `fora_do_desenho` anterior: as outras 3 falas de 10/11 ficam so' em VERBATIM_CHEGARAM_DEPOIS_V410 (nao viram fala do desenho).",
    "As frases novas da R5 (FRASE_TETELESTAI, FRASE_RECONSTROI, FRASE_E36, FRASE_DISPOSITIVO, FRASE_NOMES_RATIFICADOS_D101; PT e EN) NAO carregam hash: elas vao ao handoff, ao README e ao Atlas, onde o portao do G1 recusa todo hash de 16 ou 64 hex que o handoff nao traga; o sha256 da fala 28 fica no contrato (ratificacao_d101), na D101 e na E37; o pino do runner do ACOM Mirror (sha256 e bytes, LIDOS do arquivo por script) fica no contrato e no registro.",
    "O post do X leva a clausula do Tetelestai e a errata E36, e NAO leva a citacao do dispositivo (o dispositivo e' [PILOTO][SIM], so' como citacao, com 'nada ali valida fisica').",
    "ESTATUTO_NOMES_NOVOS_AESCALA passou a 'RATIFICADOS pelo operador em 10/11/2026 (D101)'; `nomes_novos_a_ratificar` segue com os 24 nomes (compatibilidade com o exame e o ensaio); os UNICOS pendentes sao os 2 auxiliares da autoria, ditos [DECLARADO pela autoria] (RATIFICACAO_PENDENTE_AESCALA).",
    "VEREDITO_AESCALA_OK ficou como estava (o veredito nao muda com a R5; a clausula entra como c13 e nos extras).",
    "A regra da 'folha que anuncia' na c8: toda folha que traz o nome de um teorema ou auxiliar da R5 junto de ln((1-b)/b) ou (1-b)·Z tem de trazer a FRASE exata da sua lingua, a CLAUSULA do limite e a hipotese s >= 0; as folhas com 'ACOM Mirror' tem de trazer [PILOTO][SIM] e 'nada ali valida fisica' e nenhum padrao de desempenho.",
    "Contagens de bandeiras lidas do FLAGS_v410.json por script: IALD2 22 + AEscala 85 = 107 (o briefing falava em outros numeros; o numero corrige a frase).",
    "Numeros do kernel lidos dos arquivos do build (declaracoes 34279, teoremas 27363, 0 fora do trio, escada 12294, build 407 s, Audit 339 s); o cabecalho do rito_v410.sh foi regravado por _r5ag_14 (regex; substitui o _r4ag_12, que falha na regex do cabecalho da R2).",
    "O exame de pontos (exame_pontos_v410.py) exigia que o estatuto dos nomes novos NAO dissesse RATIFICADO (regra da R2/R4); com a ratificacao de 10/11 a condicao virou o espelho (_r5ag_18): exige 'RATIFICADOS pelo operador em 10/11/2026' e proibe 'DECLARADO' e 'a ratificar'.",
    "A c13 do registro recalcula com o beta de RUNTIME (alfa CODATA x raiz de e), inclusive o controle negativo (uma oitava a menos viola no adversario) e o contraexemplo de s < 0 (b = 9/10, n = 1, custos 0 e 2); a hipotese s >= 0 e' dita em toda frase da clausula.",
    "Nenhum no de topo novo no candidato: as coisas novas entram dentro de _V410_AESCALA_CONTRACT, _V410_AESCALA_TEXT, _V410_VERBATINS2, _v410_aescala_ciclo e _v410_aescala_mechanics; o comparar mantem as mesmas listas (26 mudados + 39 novos).",
    "Os harnesses rodaram com --out PROPRIO (a pasta padrao harness_saida_v410 e' compartilhada entre os dois) e ambos com --nao-exigir-refazer (o harness de textos tambem o aceita; o refazer_candidato completo nao foi rodado, por ordem do briefing: o veredito de cada um DIZ que a regeneracao nao foi comprovada por ele).",
    "Dois consertos de pos_rito que SO' os harnesses acharam (os testes rapidos nao os veem): (a) harness_fechar_sandbox_v410.py: o delta passou a abrir o runner do ACOM Mirror (sob Central de Patentes/patents, fora de work) ao importar, e o espelho da casa so' copiava de work: a copia do delta no sandbox quebrava com FileNotFoundError; o espelho agora copia tambem o que o import abriu sob patents (_r5ag_21); (b) textos_v410.py: a funcao _ss (os sha16 das falas, achados pelo NOME) ainda era a de 26 falas e a asserção `len == DL.N_FALAS_V410` (28) derrubava o fechar e o conferidor de textos: entram a 27a e a 28a (achadas pelo nome e conferidas contra os prefixos da ordem), na forma curta e na longa da secao A ordem (citacoes verbatim conferidas por _cita contra os bytes) e o tema delas no _TEMA_ESPECIAL (_r5ag_22).",
    "O candidato foi REGERADO uma vez a mais (V410_REGERAR=1), depois da 02c, antes de qualquer rodada final; os backups `.bak_*_pre_r5` (09:55) e `.bak_*_pre_r5b` (10:53) guardam os estados anteriores do candidato, do CANDIDATO_v410.json, do v410_pins.py e do FORMAL_MAP_v410.json.",
]
R["duvidas_e_ressalvas"] = [
    "O briefing dava contagens de bandeiras/ancoras diferentes das do FLAGS_v410.json (107 = 22 + 85; 62 ancoras na AEscala): segui o arquivo; se o numero do briefing era de outra base, a gerencia confere.",
    "O candidato 28b54cf5e560beeb (mencionado no meio da rodada) NAO e' o de trabalho: ficou velho depois da 02c; o de trabalho e' o sha16 acima. Os backups _pre_r5 (09:55) e _pre_r5b (10:5x) guardam os estados anteriores.",
    "Os quatro teoremas da R5 e os 2 auxiliares nao sao conferidos AQUI contra o kernel (o kernel nao e' meu para tocar; as 62 ancoras e as 85 bandeiras sao lidas do build que a gerencia fez); o que o agente conferiu foi a fiacao: o registro exige as ancoras no trio, a proveniencia e a bandeira.",
    "O ensaio a seco e o pre-teste rodaram sobre o candidato de trabalho; o rito, a purga, a custodia e o deposito NAO foram rodados (ordem do briefing).",
    "gerar_relatorio_v410.py --seco: com o refazer_do_passo4 e o p00 passados, os 20 portoes estao ok no modo seco (antes, 15 de 20 com as pecas ainda ausentes); o modo seco NAO grava nada e nao substitui o relatorio real.",
    "O harness de textos leva cerca de 35 minutos (CPU, em processo unico); rodou duas vezes (a primeira falhou na _ss, ver acima) e a segunda passou; o do fechar leva cerca de 4 minutos.",
    "O pino do runner do ACOM Mirror e' lido do arquivo do repositorio das patentes no import do delta; se o runner for alterado depois, o delta muda e a cadeia recusa.",
]

# ---- intocados
try:
    antes = json.load(open(SCRATCH, encoding="utf-8"))
except Exception as e:  # noqa: BLE001
    antes = {}
    R["intocados_erro"] = repr(e)
cmp_ = {}
for rel, v in antes.items():
    p = os.path.join(HERE, rel)
    a16 = v.get("sha16") if isinstance(v, dict) else (v[0] if isinstance(v, (list, tuple)) else v)   # (o scratchpad guarda [sha16, mtime])
    agora = S16(p) if os.path.exists(p) else None
    cmp_[rel] = {"antes": a16, "agora": agora, "igual": a16 == agora}
for rel in ("runtime_v410.py", "runtime_h0dn_v410.py", "pedra/IALD2.lean", "pedra/AEscala.lean"):
    p = os.path.join(HERE, rel)
    if os.path.exists(p) and rel not in cmp_:
        cmp_[rel] = {"antes": None, "agora": S16(p), "igual": None}
R["intocados"] = {"todos_iguais": bool(cmp_) and all(v["igual"] is True for v in cmp_.values() if v["igual"] is not None), "n": len(cmp_), "diferentes": [k for k, v in cmp_.items() if v["igual"] is False],
                  "pinos_do_briefing": {"runtime_v410.py": S16(os.path.join(HERE, "runtime_v410.py")), "runtime_h0dn_v410.py": S16(os.path.join(HERE, "runtime_h0dn_v410.py")), "pedra/IALD2.lean": S16(os.path.join(HERE, "pedra", "IALD2.lean")), "pedra/AEscala.lean": S16(os.path.join(HERE, "pedra", "AEscala.lean"))},
                  "detalhe": cmp_}

out = os.path.join(HERE, "_r5ag_RESULTADO_v410.json"); tmp = out + ".tmp"
open(tmp, "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1)); assert os.path.getsize(tmp) > 1000; os.replace(tmp, out)
print("RESULTADO gravado: %s | arquivos mudados: %d | scripts: %d | candidato %s | intocados todos iguais: %s (%d)" % (out, R["n_arquivos_mudados"], len(R["scripts_criados"]), R["candidato_de_trabalho"]["sha16"], R["intocados"]["todos_iguais"], R["intocados"]["n"]))
for k, v in P.items():
    print("  %-70s rc=%s | %s" % (k[:70], v.get("rc"), (v.get("ultima_linha") or "")[:110]))
