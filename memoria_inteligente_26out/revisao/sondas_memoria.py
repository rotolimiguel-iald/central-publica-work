# -*- coding: utf-8 -*-
"""sondas_memoria.py -- revisão independente de memoria.py (gerência c1, 26/10/2026). Sondas MINHAS, além dos testes do construtor, sobre a
cópia C:\\t\\mem_rev\\sonda (montada aqui de real_copia; o real NUNCA é tocado). Importa o memoria.py DA CÓPIA com MEMORIA_DIR=sonda.
 P1  caminho de destruição em _escrever_atomico: outro escritor grava entre o os.replace e a conferência -> o «restaura do backup» apaga a escrita alheia?
 P2  corte da ÚLTIMA linha do livro: verificar passa? (o limite declarado) + protótipo da correção mínima (cabeça do livro em arquivo à parte)
 P3  falsos positivos do filtro: «entre Nós» (a casa), 11 dígitos com dígitos verificadores de CPF, menções legítimas de .env / iald_stack
 P4  vigiar SEM --enforcar: o que muda no disco (foto antes/depois)
 P5  vigiar --enforcar com MEMORY.md CRLF: bytes do .bak_estranho, linhas do depósito estranho, restauração
 P6  promover para MEMORY_2.md (CRLF): fins de linha do bloco anexado
 P7  _medida vs count(b'\\n'): arquivo sem nova linha final (a régua do pós-rito usa count)
 P8  promover: backup de bytes == conteúdo anterior; temporário sumiu; pino re-escrito; livro
uso: python -X utf8 -B sondas_memoria.py"""
import importlib.util, json, os, shutil, subprocess, sys, hashlib, time, re
REV = r"C:\t\mem_rev"; RC = os.path.join(REV, "real_copia"); S = os.path.join(REV, "sonda")
H = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
sha = lambda b: hashlib.sha256(b).hexdigest()
R = {}


def nova_sonda(indice_bytes=None):
    if os.path.isdir(S):
        shutil.rmtree(S)
    os.makedirs(os.path.join(S, "fila", "depositos", "codex-coordenadora"))
    for f in os.listdir(RC):
        p = os.path.join(RC, f)
        if os.path.isfile(p) and f.endswith(".md"):
            shutil.copy2(p, os.path.join(S, f))
    shutil.copy2(os.path.join(RC, "fila", "memoria.py"), os.path.join(S, "fila", "memoria.py"))
    if indice_bytes is not None:
        with open(os.path.join(S, "MEMORY.md"), "wb") as f:
            f.write(indice_bytes)


def rodar(*args, g=False, entrada=None):
    env = dict(os.environ); env.pop("MEMORIA_GERENCIA", None); env["MEMORIA_DIR"] = S; env["PYTHONUTF8"] = "1"
    if g:
        env["MEMORIA_GERENCIA"] = "claude-c1"
    cp = subprocess.run([PY, "-X", "utf8", "-B", os.path.join(S, "fila", "memoria.py")] + list(args), input=entrada, capture_output=True, env=env, cwd=S)
    def j(t):
        t = t.decode("utf-8", "replace").strip()
        try:
            return json.JSONDecoder().raw_decode(t)[0] if t else None
        except Exception:
            return {"_raw": t[:400]}
    return cp.returncode, j(cp.stdout), j(cp.stderr)


def foto(raiz):
    out = {}
    for d, _, fs in os.walk(raiz):
        for f in fs:
            p = os.path.join(d, f); out[os.path.relpath(p, raiz)] = sha(open(p, "rb").read())
    return out


def mod():
    os.environ["MEMORIA_DIR"] = S
    spec = importlib.util.spec_from_file_location("memoria_sonda", os.path.join(S, "fila", "memoria.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


IDX = ("# MEMORY.md\n\n> Índice de teste; ler também o [MEMORY_2.md](MEMORY_2.md).\n\n## Ler primeiro\n\n- [a](a.md) — um\n\n## Estado corrente\n\n"
       + "".join("- [item %03d](t.md) — descrição %03d\n" % (i, i) for i in range(20)) + "\n## O operador\n\n- [b](b.md) — dois\n").encode("utf-8")

# ───────── P1: o restaura-do-backup de _escrever_atomico apaga uma escrita alheia posterior ao replace?
nova_sonda(IDX); m = mod()
alvo = os.path.join(S, "sonda_p1.txt"); open(alvo, "wb").write(b"ANTIGO\n")
replace0 = m.os.replace
def replace_e_outro_escritor(src, dst):
    replace0(src, dst)
    with open(dst, "ab") as f:            # outro processo (ex.: o pos-rito) grava logo depois do nosso replace
        f.write(b"LINHA DE OUTRO ESCRITOR (so' existe aqui)\n")
m.os.replace = replace_e_outro_escritor
try:
    m._escrever_atomico(alvo, b"NOVO\n"); erro = None
except Exception as e:
    erro = "%s: %s" % (type(e).__name__, getattr(e, "mensagem", e))
finally:
    m.os.replace = replace0
fim = open(alvo, "rb").read()
R["P1_restaura_do_backup_apaga_outro_escritor"] = {"erro": erro, "conteudo_final": fim.decode(), "linha_alheia_sobreviveu": b"OUTRO ESCRITOR" in fim,
                                                   "voltou_ao_ANTIGO": fim == b"ANTIGO\n", "backups": sorted(f for f in os.listdir(S) if f.startswith("sonda_p1.txt.bak_"))}
# controle: em que casos o ramo de restauração e' alcançável? (tmp divergente / replace recusado deixam p intacto; so' o pos-check falha com p mudado)
# ───────── P2: corte da ultima linha do livro
nova_sonda(IDX)
rc, o, e = rodar("pinar", "--motivo", "pino inicial da sonda", g=True); assert rc == 0, e
rc, o1, e = rodar("depositar", "--quem", "codex-coordenadora", "--tipo", "project", "--estatuto", "DECLARADO", "--alvo", "MEMORY_2.md", "--texto", "primeiro depósito da sonda, texto neutro."); assert rc == 0, e
rc, o2, e = rodar("depositar", "--quem", "codex-coordenadora", "--tipo", "project", "--estatuto", "DECLARADO", "--alvo", "MEMORY_2.md", "--texto", "segundo depósito da sonda, texto neutro."); assert rc == 0, e
livro = os.path.join(S, "fila", "fila.jsonl"); L = open(livro, "rb").read(); linhas = L.split(b"\n")
cortado = b"\n".join(linhas[:-2]) + b"\n"   # tira a ULTIMA linha (a do 2o deposito)
with open(livro, "wb") as f:
    f.write(cortado)
rc_v, ov, ev = rodar("verificar"); rc_l, ol, el = rodar("listar")
R["P2_corte_da_ultima_linha"] = {"verificar_rc": rc_v, "verificar_ok": (ov or {}).get("ok"), "violacoes": (ov or {}).get("violacoes"),
                                 "listar_estados": (ol or {}).get("por_estado"), "nao_registrados": [x["id"] for x in (ol or {}).get("nao_registrados", [])],
                                 "n_linhas_livro_antes": len([l for l in linhas if l.strip()]), "n_depois": len([l for l in cortado.split(b"\n") if l.strip()])}
# protótipo da correção mínima: cabeça do livro num arquivo à parte, gravado por _acrescenta (aqui simulado) e conferido por verificar
cab = {"seq": len([l for l in linhas if l.strip()]), "hash": json.loads(linhas[-2].decode())["hash"]}
rows = [json.loads(l) for l in cortado.split(b"\n") if l.strip()]
R["P2_correcao_minima_cabeca_a_parte"] = {"cabeca_gravada": cab, "livro_cortado_cabeca": {"seq": rows[-1]["seq"], "hash": rows[-1]["hash"]},
                                         "detectaria": not (rows[-1]["seq"] == cab["seq"] and rows[-1]["hash"] == cab["hash"]),
                                         "proposta": "_acrescenta grava fila\\CABECA.json {seq, hash, ts} (temporario -> replace) DEPOIS do livro; _parse_livro/verificar: rows[-1].hash == CABECA.hash e len(rows) == CABECA.seq; CABECA ausente com livro nao vazio = violacao; o pino do MEMORY.md tambem pode carregar livro_cabeca"}
# ───────── P3: falsos positivos do filtro
nova_sonda(IDX); rodar("pinar", g=True)
casos = {
    "entre_Nos_a_casa_maiuscula": "A pedra foi examinada entre Nós e o espelho público; nada mais.",
    "entre_nos_minusculo_reserva": "isto fica só entre nós, não registre",
    "11_digitos_bytes_kids_17712469440": "O catálogo KiDS tem 17712469440 bytes exatos no disco.",
    "11_digitos_com_separador": "O catálogo KiDS tem 17.712.469.440 bytes exatos no disco.",
    "mencao_legitima_dotenv": "O monitor lê a configuração; o arquivo .env nunca sai do servidor (regra 8).",
    "mencao_legitima_iald_stack": "A regra 8 diz: iald_stack_v7.py nunca sai, só existência e mtime.",
    "email_do_operador_como_identidade": "autoria: [dado pessoal removido]",
    "timestamp_14_digitos": "rodada 20261026191628 concluída",
    "sha16_hex": "selo a5aacfa4e5be9b12 e 6981660b5f7cd537",
    "casa_Nos_no_caminho": r"copiado de C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py",
}
R["P3_filtro"] = {}
for k, txt in casos.items():
    rc, o, e = rodar("depositar", "--quem", "codex-coordenadora", "--tipo", "project", "--estatuto", "DECLARADO", "--alvo", "MEMORY_2.md", "--texto", txt)
    R["P3_filtro"][k] = {"rc": rc, "codigo": (e or {}).get("codigo") if rc else "OK", "padroes": sorted({a["padrao"] for a in ((e or {}).get("achados") or [])})}
# ───────── P4: vigiar SEM --enforcar: o que muda no disco
nova_sonda(IDX); rodar("pinar", g=True)
with open(os.path.join(S, "MEMORY.md"), "ab") as f:
    f.write("- [linha estranha](x.md) — acrescentada fora da promoção\n".encode("utf-8"))
antes = foto(S); rc, o, e = rodar("vigiar"); depois = foto(S)
R["P4_vigiar_sombra"] = {"rc": rc, "estado": (o or {}).get("estado"), "novos_arquivos": sorted(set(depois) - set(antes)), "arquivos_mudados": sorted(k for k in antes if k in depois and antes[k] != depois[k]),
                        "apagados": sorted(set(antes) - set(depois)), "fora_de_fila": [k for k in (set(depois) - set(antes)) | {k for k in antes if k in depois and antes[k] != depois[k]} if not k.startswith("fila")]}
rc2, o2, _ = rodar("vigiar"); R["P4_vigiar_sombra"]["segunda_vez_repetido"] = (o2 or {}).get("repetido"); R["P4_vigiar_sombra"]["segunda_vez_novos"] = sorted(set(foto(S)) - set(depois))
# ───────── P5: --enforcar com CRLF
IDX_CRLF = IDX.replace(b"\n", b"\r\n")
nova_sonda(IDX_CRLF); rodar("pinar", g=True)
estranha = IDX_CRLF + "- [estranha CRLF](x.md) — fora da promoção, com acento ção\r\n".encode("utf-8")
with open(os.path.join(S, "MEMORY.md"), "wb") as f:
    f.write(estranha)
rc, o, e = rodar("vigiar", "--enforcar")
baks = sorted(f for f in os.listdir(S) if f.startswith("MEMORY.md.bak_estranho_"))
dep_dir = os.path.join(S, "fila", "depositos", "estranho"); deps = sorted(os.listdir(dep_dir)) if os.path.isdir(dep_dir) else []
dep_b = open(os.path.join(dep_dir, deps[0]), "rb").read() if deps else b""
R["P5_enforcar_crlf"] = {"rc": rc, "estado": (o or {}).get("estado"), "restaurado_igual_ao_pino": open(os.path.join(S, "MEMORY.md"), "rb").read() == IDX_CRLF,
                         "bak_estranho_igual_a_versao_estranha": bool(baks) and open(os.path.join(S, baks[0]), "rb").read() == estranha,
                         "deposito_estranho": deps, "linha_no_deposito": b"estranha CRLF" in dep_b, "deposito_tem_CRLF": b"\r\n" in dep_b,
                         "corpo_do_deposito_fim": dep_b[-80:].decode("utf-8", "replace")}
# ───────── P6: promover para MEMORY_2.md (CRLF)
nova_sonda(IDX); rodar("pinar", g=True)
m2 = os.path.join(S, "MEMORY_2.md"); m2_antes = open(m2, "rb").read()
rc, o, e = rodar("depositar", "--quem", "codex-coordenadora", "--tipo", "project", "--estatuto", "DECLARADO", "--alvo", "MEMORY_2.md", "--texto", "texto neutro para o segundo arquivo.\nsegunda linha.")
rc, o, e = rodar("promover", o["id"], "--para", "MEMORY_2.md", g=True)
m2_depois = open(m2, "rb").read()
R["P6_promover_memory2_crlf"] = {"rc": rc, "m2_crlf_antes": m2_antes.count(b"\r\n"), "m2_lf_sozinhos_antes": m2_antes.count(b"\n") - m2_antes.count(b"\r\n"),
                                 "prefixo_preservado": m2_depois.startswith(m2_antes), "bloco_anexado_tem_LF_sem_CR": (m2_depois[len(m2_antes):].count(b"\n") - m2_depois[len(m2_antes):].count(b"\r\n")) > 0,
                                 "backup": (o or {}).get("backup_topico"), "bloco": m2_depois[len(m2_antes):][:200].decode("utf-8", "replace")}
# ───────── P7: _medida vs count('\n')
m = mod()
sem_nl = IDX.rstrip(b"\n")
R["P7_medida_sem_nova_linha_final"] = {"splitlines": m._medida(sem_nl)["linhas"], "count_n": sem_nl.count(b"\n"), "com_nl_splitlines": m._medida(IDX)["linhas"], "com_nl_count": IDX.count(b"\n")}
# ───────── P8: promover: backup de bytes, temporario, pino, livro
nova_sonda(IDX); rodar("pinar", g=True)
top = os.path.join(S, "regua-prova-vs-juizo.md"); top_antes = open(top, "rb").read(); idx_antes = open(os.path.join(S, "MEMORY.md"), "rb").read()
rc, o, e = rodar("depositar", "--quem", "codex-coordenadora", "--tipo", "project", "--estatuto", "DECLARADO", "--alvo", "regua-prova-vs-juizo.md", "--texto", "nota neutra de sonda para o tópico."); assert rc == 0, e
rc, o, e = rodar("promover", o["id"], "--para", "regua-prova-vs-juizo.md", "--linha-indice", "- [sonda](regua-prova-vs-juizo.md) — linha de sonda", g=True)
R["P8_promover"] = {"rc": rc, "erro": e, "backup_topico_igual_ao_anterior": bool(o) and open(o["backup_topico"], "rb").read() == top_antes,
                    "backup_indice_igual_ao_anterior": bool(o) and open(o["backup_indice"], "rb").read() == idx_antes,
                    "topico_preserva_prefixo": open(top, "rb").read().startswith(top_antes), "tmp_sobrou": sorted(f for f in os.listdir(S) if ".tmp_" in f),
                    "pino_bate_indice": json.load(open(os.path.join(S, "fila", "PINO_MEMORY.json"), encoding="utf-8"))["sha256"] == sha(open(os.path.join(S, "MEMORY.md"), "rb").read()),
                    "espelho_igual_indice": open(os.path.join(S, "fila", "PINO_MEMORY_conteudo.md"), "rb").read() == open(os.path.join(S, "MEMORY.md"), "rb").read(),
                    "livro_linhas": len([l for l in open(os.path.join(S, "fila", "fila.jsonl"), "rb").read().split(b"\n") if l.strip()]),
                    "backups_do_livro": len([f for f in os.listdir(os.path.join(S, "fila")) if f.startswith("fila.jsonl.bak_")])}
json.dump(R, open(os.path.join(H, "SONDAS_MEMORIA.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps(R, ensure_ascii=False, indent=1, default=str))
