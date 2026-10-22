# -*- coding: utf-8 -*-
"""finalizar_r3_4.py (R3.4, 19/10/2026) -- depois do run REAL do pre_selo da v394 (ensaio, so leitura da producao e do Nos): (1) copia o recibo e as evidencias do run (de C:/t/vb10/...) para
R3_4/recibo_pre_selo_v394/ (bytes iguais, conferidos); (2) confere o recibo pelo MESMO caminho que o B(n) pos_selo usara (verificar_recibo_pre_selo_real.py); (3) deriva o recibo do kernel
no contrato R3_4 (derivar_recibo_kernel_r3_4.py); (4) grava PINO_RECIBO_PRE_SELO_v394_R3_4.json e a copia PINOS_BN_v394.R3_4.json (a pasta v394 nao e tocada; a gerencia copia).
Tudo lido por script; so escreve arquivos NOVOS dentro de R3_4. uso: python -I -B -X utf8 finalizar_r3_4.py <pasta do run real em C:/t/vb10>"""
import sys
sys.dont_write_bytecode = True
import datetime, hashlib, json, os, shutil, subprocess
from pathlib import Path

RUN = Path(sys.argv[1])
AQUI = Path(__file__).resolve().parent.parent
CADEIA = Path("C:/IALD/Central de Patentes/work/cadeia_de_selo")
V394 = CADEIA / "v394"
PY = sys.executable


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def pinar(p):
    p = Path(p)
    return dict(path=str(p), sha256=sha(p), bytes=p.stat().st_size)


def mudancas_depois_do_inicio(raiz, quando_iso):
    """os arquivos sob `raiz` (sem seguir juncao) com mtime posterior ao instante `quando_iso` (hora local): nome relativo e mtime."""
    t0 = datetime.datetime.fromisoformat(quando_iso).timestamp()
    out, pilha = [], [Path(raiz)]
    while pilha:
        d = pilha.pop()
        with os.scandir(d) as it:
            for e in it:
                if e.is_junction() or e.is_symlink():
                    continue
                if e.is_dir(follow_symlinks=False):
                    pilha.append(Path(e.path))
                elif e.is_file(follow_symlinks=False) and e.stat().st_mtime > t0:
                    out.append([os.path.relpath(e.path, raiz), datetime.datetime.fromtimestamp(e.stat().st_mtime).isoformat(timespec="seconds")])
    out.sort()
    return dict(n=len(out), amostra=out[:40])


recs = sorted(RUN.glob("RECIBO_SINCRONIZACAO_v393_*.json"))
assert len(recs) == 1, recs
rec = recs[0]
rj = json.loads(rec.read_bytes())
assert rj["fase"] == "pre_selo" and rj["modo"] == "ensaio" and rj["producao"] is True and rj["versao_alvo"] == "v393", (rj["fase"], rj["modo"])
# (1) copia das evidencias
DST = AQUI / "recibo_pre_selo_v394"
DST.mkdir()
copiados = {}
for src in [rec] + sorted((RUN / "recibos").glob("*")) + [RUN / n for n in ("MANIFESTO_CANDIDATO_B4.json", "CONTRATO_CANONICO_B4.md") if (RUN / n).is_file()]:
    rel = src.relative_to(RUN)
    d = DST / rel
    d.parent.mkdir(parents=True, exist_ok=True)
    with open(d, "xb") as f:
        f.write(src.read_bytes())
    assert sha(d) == sha(src)
    copiados[str(rel)] = sha(d)
rec_copia = DST / rec.name
# (2) a conferencia pelo caminho do B(n)
ver = subprocess.run([PY, "-I", "-B", "-X", "utf8", str(AQUI / "_construcao" / "verificar_recibo_pre_selo_real.py"), str(rec_copia)], capture_output=True, text=True, encoding="utf-8", errors="replace")
(AQUI / "evidencias").mkdir(exist_ok=True)
vj = json.loads(ver.stdout)
(AQUI / "evidencias" / "VERIFICACAO_RECIBO_PRE_SELO_REAL.json").write_bytes(json.dumps(dict(comando="verificar_recibo_pre_selo_real.py <recibo>", rc=ver.returncode, resultado=vj), ensure_ascii=False, indent=1).encode("utf-8"))
# (3) o recibo do kernel R3_4 derivado
kder = AQUI / "KERNEL_RECIBO_v394_R3_4.json"
kd = subprocess.run([PY, "-I", "-B", "-X", "utf8", str(AQUI / "derivar_recibo_kernel_r3_4.py"), "--recibo", str(V394 / "kernel" / "KERNEL_RECIBO_v394.json"), "--saida", str(kder)],
                    capture_output=True, text=True, encoding="utf-8", errors="replace")
assert kd.returncode == 0, kd.stdout + kd.stderr
# (4) os pinos
bat = rj["bateria_resultado"]
por_teste = {t["id"]: t["resultado"] for t in bat["testes"]}
t12 = json.loads((rec_copia.parent / "recibos" / "T12_T13_T14_ATRATOR.json").read_bytes())
esboco, bateria, cadeia = AQUI / "sincronizar_bancada.py", AQUI / "BATERIA_VINCULO_v393.json", AQUI / "CADEIA_DE_SELOS_v394.json"
assert rj["script_sha256"] == sha(esboco), "o esboco mudou depois do run real"
assert rj["bateria"]["sha256"] == sha(bateria) and rj["cadeia_de_selos"]["sha256"] == sha(cadeia)
base = json.loads((AQUI / "_construcao" / "baseline_antes.json").read_bytes())
depois_p = AQUI / "_construcao" / "baseline_depois_run_real.json"
subprocess.run([PY, "-I", "-B", "-X", "utf8", str(AQUI / "_construcao" / "medir_baseline.py"), str(depois_p)], capture_output=True, check=True)
dep = json.loads(depois_p.read_bytes())
intocados = dict(producao=dict(n_arquivos_antes=base["producao"]["n_arquivos"], n_arquivos_depois=dep["producao"]["n_arquivos"], lista_igual=base["producao"]["lista_sha256"] == dep["producao"]["lista_sha256"],
                               manifesto_igual=base["producao"]["manifesto_sha256"] == dep["producao"]["manifesto_sha256"]),
                 nos=dict(topo_igual=base["nos"]["topo_sha256"] == dep["nos"]["topo_sha256"], **{c: base["nos"][c]["sha256"] == dep["nos"][c]["sha256"] and base["nos"][c]["mtime_ns"] == dep["nos"][c]["mtime_ns"]
                                                                                                   for c in ("um.py", "um_absoluto_selo.json", "um_absoluto.json", "tgl_kernel_proof_manifest.json")}),
                 cadeia_v394=dict(n_arquivos_antes=base["cadeia_v394"]["n_arquivos"], n_arquivos_depois=dep["cadeia_v394"]["n_arquivos"], lista_igual=base["cadeia_v394"]["lista_sha256"] == dep["cadeia_v394"]["lista_sha256"],
                                  mudancas_por_outra_sessao=mudancas_depois_do_inicio(V394, base["quando"]),
                                  nota="a pasta v394 e VIVA (a gerencia a edita); esta tarefa nao escreve nela (as saidas vao a C:/t/vb10 e R3_4; o esboco recusa --saida fora das raizes); os arquivos com mtime posterior ao inicio sao de outra sessao"),
                 bases_vNNN_iguais=base["bases_vNNN"] == dep["bases_vNNN"],
                 eventos=dict(linhas_antes=base["eventos"]["linhas"], linhas_depois=dep["eventos"]["linhas"], observacao="o livro e VIVO (outras sessoes anotam); este trabalho nunca o abre para escrita"))
pino = dict(contrato="PINO_RECIBO_PRE_SELO_v394_R3_4", quando=rj["inicio_utc"], path=str(rec_copia), sha256=sha(rec_copia), bytes=rec_copia.stat().st_size, versao_nos=rj["nos"]["UM_VERSION"],
            um_py_sha16_do_nos=rj["nos"]["um_py"]["sha256"][:16], bancada_pina=dict(version=rj["manifesto_anterior"]["version"], deployment_id=rj["manifesto_anterior"]["deployment_id"],
                                                                                   um_py_sha16=rj["manifesto_anterior"]["um_py_pinado"][:16], estado_do_contrato_instalado=rj["manifesto_anterior"]["estado_do_contrato_instalado"]),
            comando_exato=("python -I -B -X utf8 \"%s\" --bancada \"C:\\IALD\\Bancada_Um\" --producao --nos \"%s\" --versao v393 --fase pre_selo --modo ensaio --bateria \"%s\" --bateria-sha256 %s "
                           "--cadeia-de-selos \"%s\" --cadeia-de-selos-sha256 %s --saida \"%s\"" % (esboco, rj["nos"]["dir"], bateria, sha(bateria), cadeia, sha(cadeia), RUN)),
            esboco=pinar(esboco), bateria=dict(**pinar(bateria), versao=rj["bateria"]["versao"]), cadeia_de_selos=pinar(cadeia), veredito=rj["veredito"], codigo_de_saida=0,
            contagens=dict(n=bat["n"], passa=bat["passa"], falha=bat["falha"], nao_executado=bat["nao_executado"], veredito_bateria=bat["veredito"]), por_teste=por_teste,
            t12_t13_t14_por_corrida={k: ("PASSA" if v.get("passa") else "FALHA") for k, v in t12["runs"].items()},
            adendo_de_pino_do_t12=t12["adendo_de_pino"]["entrada_do_um_py"], salto=rj["salto"], pinos_da_versao=rj["bateria"]["pinos_da_versao"],
            utilizavel_como_recibo_pre_selo_do_B_n=bool(vj.get("aceito")), conferido_por=dict(script="_construcao/verificar_recibo_pre_selo_real.py", rc=ver.returncode,
                                                                                            resultado="aceito" if vj.get("aceito") else vj.get("recusa")),
            escrita_na_producao_e_no_nos=intocados, copias_das_evidencias=copiados,
            escopo="validade matematica e replay documental na face testada; nenhum dado observado; NOT_FALSIFIED nao e creditacao; o gate nao se move")
pino_p = AQUI / "PINO_RECIBO_PRE_SELO_v394_R3_4.json"
with open(pino_p, "xb") as f:
    f.write(json.dumps(pino, ensure_ascii=False, indent=1).encode("utf-8"))
orig = json.loads((V394 / "PINOS_BN_v394.json").read_bytes())
novo = dict(orig)
novo["esboco_R3_3_substituido"] = novo.pop("esboco_R3_3")
novo["esboco_R3_4"] = pinar(esboco)
novo["bateria_R2_substituida"] = novo.pop("bateria")
novo["bateria"] = dict(**pinar(bateria), versao=rj["bateria"]["versao"], fase="pre_selo da v394 (Nos v393 instalado)",
                       regra="regenerada por script em cada versao (gerar_bateria_r3_4.py --base R2/BATERIA_VINCULO.json --versao <instalada> --pinos-bn <PINOS_BN da instalada>); a do pos_selo da v394 e gerada DEPOIS do selo")
novo["pino_um_py_da_bateria"] = pinar(AQUI / "bateria_r3_4" / "PINO_UM_PY_v393.json")
novo["driver_t12_t14"] = pinar(AQUI / "bateria_r3_4" / "t12_t14_atrator_r3_4.py")
novo["cadeia_de_selos"] = pinar(cadeia)
novo["recibo_pre_selo_ensaio_R3_3_substituido"] = novo.pop("recibo_pre_selo")
novo["recibo_pre_selo"] = dict(**pinar(rec_copia), versao_nos=rj["nos"]["UM_VERSION"], veredito=rj["veredito"], utilizavel_como_recibo_pre_selo_do_B_n=bool(vj.get("aceito")),
                               pino_do_pino=pinar(pino_p), com_salto=dict(de=rj["salto"]["de"]["versao"], ate=rj["salto"]["ate"]["versao"], versoes_puladas=rj["salto"]["versoes_puladas"]))
novo["kernel_recibo_R3_2_original"] = novo["kernel_recibo"]
novo["kernel_recibo_R3_4_proposto"] = dict(**pinar(kder), derivado_de=novo["kernel_recibo"], por="derivar_recibo_kernel_r3_4.py",
                                          nota="PROPOSTA: so o contrato e modulos_de_auditoria mudam; o B(n) R3.4 aceita o R3_2 OU o R3_4, mas so o R3_4 libera as 3 pedras de auditoria (sem declaracoes); a gerencia decide qual pinar em kernel_recibo")
novo["comandos_do_pos_selo"] = "ver RESULTADO_R3_4.md, secao 7 (comandos exatos do pos_selo da v394 com salto)"
novo["nota"] = ("COPIA de PINOS_BN_v394.json feita pela R3.4 (19/10/2026) em R3_4; a pasta v394 NAO foi tocada; a gerencia copia. [REAL] tudo lido por script. Mudancas: esboco R3.4 no lugar da R3.3; "
                "bateria por versao (v393) no lugar da R2; cadeia de selos v392->v393; recibo pre_selo REAL com o salto declarado (BATERIA_PASSA); recibo do kernel R3_4 proposto. "
                "criterios/candidato/esperados/pins_do_candidato: como estavam (x19 e a decisao da gerencia).")
novo_p = AQUI / "PINOS_BN_v394.R3_4.json"
with open(novo_p, "xb") as f:
    f.write(json.dumps(novo, ensure_ascii=False, indent=1).encode("utf-8"))
print(json.dumps(dict(recibo=str(rec_copia), recibo_sha256=sha(rec_copia), utilizavel=bool(vj.get("aceito")), veredito=rj["veredito"], contagens=pino["contagens"], kernel_R3_4=sha(kder),
                      pinos_bn=sha(novo_p), pino_recibo=sha(pino_p), intocados=intocados), ensure_ascii=False, indent=1))
