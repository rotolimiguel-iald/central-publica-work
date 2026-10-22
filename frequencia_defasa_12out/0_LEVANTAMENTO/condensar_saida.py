# -*- coding: utf-8 -*-
# Gera as versoes CONDENSADAS (para a saida estruturada da subtarefa) de LEVANTAMENTO.md e DEFINICOES.json.
# Os arquivos integrais ficam nesta pasta; as versoes condensadas apontam para eles com sha16 lido por script.
import json, os, hashlib, re
AQUI = os.path.dirname(os.path.abspath(__file__))


def sha16(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:16]


MD = os.path.join(AQUI, "LEVANTAMENTO.md")
DJ = os.path.join(AQUI, "DEFINICOES.json")
md = open(MD, encoding="utf-8").read()
d = json.load(open(DJ, encoding="utf-8"))
s_md, s_dj = sha16(MD), sha16(DJ)

# --- MD condensado: secao 3 (tabelas) e secao 8 (lista de arquivos) viram ponteiros
i3 = md.index("## 3. Teoremas de kernel existentes")
i4 = md.index("## 4. Mapa de rotas")
i8 = md.index("## 8. Arquivos desta pasta")
n_teo = md[i3:i4].count("\n| `")
sec3 = ("## 3. Teoremas de kernel existentes que tocam o tema\n\n"
        f"[REAL] {n_teo} linhas de tabela (teoremas, definições e âncoras de runtime/core/túnel/literatura) com arquivo:linha e sha16 estão na "
        f"versão integral `LEVANTAMENTO.md` (sha16 `{s_md}`), seção 3; a lista de teoremas segue no campo `teoremas_existentes` desta saída. "
        "131 declarações foram medidas aqui por `#print axioms` (todas no trio, 0 sorryAx, EXIT 0).\n\n")
sec8 = ("## 8. Arquivos desta pasta\n\n"
        f"Pasta `C:\\IALD\\Central de Patentes\\work\\frequencia_defasa_12out\\0_LEVANTAMENTO`: `LEVANTAMENTO.md` (integral, sha16 `{s_md}`), "
        f"`DEFINICOES.json` (integral, sha16 `{s_dj}`), `CONFERENCIA_PINOS.json` (todo sha16 conferido contra os bytes), `CONFERENCIA_BETA.json`, "
        "`HASHES_TEXTOS_OPERADOR.json`, `EMBUTIDO_VS_KERNEL*.json`, `IMPRESSAO_DIGITAL_KERNEL_*.json`, `KERNEL_INDICE.json`, `lean_check\\` "
        "(sondas, saídas e recibos), `mapa\\`, `inventario\\`, `nos_vivo\\` e os scripts.\n")
cond = md[:i3] + sec3 + md[i4:i8] + sec8
cond = cond.replace("(resumo; a íntegra com linha e sha16 de cada âncora está em `DEFINICOES.json`)",
                    "(resumo; a íntegra com linha e sha16 de cada âncora está em `DEFINICOES.json` e na seção 3 do `LEVANTAMENTO.md` integral)")
# a tabela de pinos e as consultas ficam; o restante e identico ao integral
open(os.path.join(AQUI, "_saida_levantamento_md.txt"), "w", encoding="utf-8", newline="\n").write(cond)

# --- JSON condensado
objs = []
for o in d["objetos"]:
    ak, ar, ac, ao, al = [], [], [], [], []
    for a in o["ancoras"]:
        t = a.get("tipo")
        if t == "kernel":
            ak.append(a['nome'])
        elif t == "runtime_um_py":
            ar.append(f"um.py l.{a['linha']}: {a['descricao']} {a['estatuto']}")
        elif t in ("core_v391", "selo_v391"):
            ac.append(f"{'core' if t == 'core_v391' else 'selo'} {a['caminho']} = {str(a['valor'])[:120]}")
        elif t in ("arquivo", "texto_operador", "memoria", "tunel", "selo"):
            ao.append(f"{os.path.basename(a['arquivo'])} [{a['sha16']}] {a['estatuto']}")
        elif t in ("literatura", "mathlib_pinada_no_Nos"):
            al.append(f"{a.get('ref') or a.get('nome')} — {a['estatuto']}")
        elif t == "mapa_de_rotas":
            ao.append(f"mapa {a['rota']} seqs {a['seqs']}: {a['nota']}")
        elif t == "medido_aqui":
            ao.append(f"medido aqui {json.dumps(a['valores'], ensure_ascii=False)} {a['estatuto']}")
    fo = "; ".join(f"{f['texto']} l.{','.join(str(n) for n in f['linhas'])}" for f in o["fonte_operador"])
    x = {"id": o["id"], "termo": o["termo"], "fonte_operador": fo, "definicao_canonica": o["definicao_canonica"],
         "estatuto": o["estatuto"], "novo_ou_reafirmacao": o["novo_ou_reafirmacao"],
         "ancoras_no_integral": {"kernel": len(ak), "runtime_um_py": len(ar), "core_selo": len(ac), "arquivos_mapa_medidos": len(ao),
                                 "literatura_mathlib": len(al)},
         "kernel": ak}
    for k in ("lacuna", "consulta_ausencia_kernel"):
        if k in o:
            x[k] = o[k]
    objs.append(x)
cj = {"unidade": d["unidade"], "data": d["data"], "integral": {"arquivo": DJ, "sha16": s_dj},
      "textos_operador": d["textos_operador"],
      "pinos": {k: (v.get("sha16") if isinstance(v, dict) and "sha16" in v else None) for k, v in d["pinos"].items() if k not in ("kernel_impressao_digital", "kernel_impressao_digital_depois")},
      "kernel_impressao_digital": {k: d["pinos"]["kernel_impressao_digital"][k] for k in ("n_arquivos", "bytes_total", "sha256_metadados", "sha256_conteudo_lean")},
      "kernel_impressao_digital_igual_antes_depois": all(d["pinos"]["kernel_impressao_digital"][k] == d["pinos"]["kernel_impressao_digital_depois"][k]
                                                          for k in ("n_arquivos", "bytes_total", "sha256_metadados", "sha256_conteudo_lean")),
      "beta_runtime": d["beta_runtime"], "lean_sandbox": d["lean_sandbox"], "embutido_vs_kernel": d["embutido_vs_kernel"],
      "objetos": objs}
txt = json.dumps(cj, ensure_ascii=False, separators=(",", ":"))
open(os.path.join(AQUI, "_saida_definicoes_json.txt"), "w", encoding="utf-8", newline="\n").write(txt)
print("md condensado", len(cond.encode("utf-8")), "json condensado", len(txt.encode("utf-8")))
