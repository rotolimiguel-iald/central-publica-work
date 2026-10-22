"""Create047 final reports only after the clean build and independent review pass."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parent

def new(path,text):
    assert path.resolve().is_relative_to(ROOT) and not path.exists()
    assert not (ROOT/"CONTINUACAO047_MANIFESTO.json").exists()
    b=text.encode("utf-8");t=path.with_name(path.name+".tmp")
    with t.open("xb") as f:f.write(b);f.flush();os.fsync(f.fileno())
    assert t.read_bytes()==b;t.rename(path);assert path.read_bytes()==b

def link(p):return f"[{p.name}](<{p.as_posix()}>)"

def main():
    marker=ROOT/"CONTINUACAO047_CLEAN_BUILD.json"
    build=json.loads(marker.read_text(encoding="utf-8"))
    assert build["status"]=="PASS" and build["development_only"] is False
    result=subprocess.run([sys.executable,"-B",str(ROOT/"audit_continuation047.py"),"--build-only"],
        cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    assert result.returncode==0,result.stdout.decode("utf-8",errors="replace")
    audit=json.loads(result.stdout.decode("utf-8"));assert audit["status"]=="BUILD_PASS"
    review=ROOT/"CONTINUACAO047_REVISAO_INDEPENDENTE.md"
    assert review.is_file() and "BUILD_PASS" in review.read_text(encoding="utf-8")
    clean=Path(build["clean_directory"])
    frozen=json.loads((clean/"FROZEN_INPUTS.json").read_text(encoding="utf-8"))
    c=audit["counts"];n=len(build["sources"])
    stats=(f'[REAL — lote final] {len(build["steps"])}/{len(build["steps"])} etapas PASS: {n} módulos e Imports047All. '
      f'{c["theorems"]} teoremas, {c["definitions"]} definições/estruturas, {c["axiom_prints"]} declarações '
      f'com axiomas impressos e {c["instances"]} instâncias novas. Axiomas restritos a propext, Classical.choice e Quot.sound; '
      'zero erros/avisos. As dependências históricas não são contadas como novidade.\n\n'
      f'[REAL — auditoria] BUILD_PASS. {len(frozen)} registros congelados idênticos antes/depois; '
      f'{len(build["files"])} arquivos no inventário do build; {audit["historical_records"]} registros históricos '
      'revalidados pelo auditor. Diretório final: '+link(clean)+'.\n')
    table=["| Módulo | Teoremas | Definições | Prints |","|---|---:|---:|---:|"]
    for row in build["sources"]:
      table.append(f'| {row["module"]} | {row["theorems"]} | {row["definitions"]} | {len(row["expected_axiom_rows"])} |')
    body="""## Resultado

[REAL — Lean] A expectativa E construída046 possui agora provas próprias de linearidade sobre M, preservação da unidade, do estado e do adjunto, bimodularidade sobre o centralizador, positividade completa e normalidade na formulação por supremos positivos dirigidos.

O domínio é M=theFactorObject P, para todo SiteProfile P da torre binária existente. A totalização E fora de M não é apresentada como linear. Os teoremas valem para qualquer ExpectationInput P, identificado por unicidade com o construído046; a existência desse habitante já foi provada, sem hipótese de período comum.

## Cadeia verificada

1. Ortogonalidade e separância dão unicidade pontual. Dela seguem soma, escala, estrela e bimódulo: E(CAD)=C E(A) D para C,D no centralizador e A em M. A restrição a M é empacotada como mapa linear contínuo.
2. Formas das médias de conjugação são integrais de formas no vetor transportado. O sinal não negativo passa ao limite forte. Isso prova positividade de E em M, usando também a preservação do adjunto.
3. Para todo tamanho finito k, a forma de um bloco é a soma dupla Σ_ij〈v_i,A_ij v_j〉. O mesmo transporte modular em todos os vetores preserva a positividade do bloco; médias e limites preservam o sinal. Não se exige positividade entrada a entrada.
4. Uma equivalência explícita de *-álgebras identifica CStarMatrix de operadores com operadores em H^k. A inversa é proj_i ∘ T ∘ single_j. Ela transporta e reflete positividade, permitindo empacotar a restrição de E no contrato CompletelyPositiveMap de Mathlib.
5. A cota GNS ||E(A)Ω||≤||AΩ|| e a linearidade dão contração da distância GNS. A órbita direita densa e a cota uniforme estendem a convergência em Ω à forte para filtros arbitrários.
6. Uma rede positiva crescente limitada em norma tem formas escalares crescentes limitadas. A estimativa ||Dv||²≤||D|| Re〈v,Dv〉 para incrementos positivos torna a rede Cauchy em cada vetor. Completude constrói um operador limite B, e a ordem prova que B é o supremo. Trata-se de qualquer pré-ordem dirigida não vazia, não só sequências.
7. As relações definidoras do bicomutante passam ao limite forte, logo B pertence a M. A continuidade047 dá E(A_i)→E(B); a monotonicidade e o limite forte dão E(B)=sup E(A_i). Os IsLUB usam a ordem de Loewner ambiente em B(H), com B∈M como conclusão. Uma cota em ordem fornece a cota em norma, provando preservação de TODOS os supremos positivos dirigidos.

Classical.choice seleciona limites cuja existência foi demonstrada. Não se extrai um algoritmo com taxa numérica uniforme de convergência.

## Estatutos e limites

[REAL — escopo formal] Normalidade significa aqui a formulação explícita por preservação de supremos positivos dirigidos. O lote não conta uma equivalência adicional com continuidade fraca-* como se tivesse sido formalizada.

[REAL — histórico] NOTA047_PROPRIEDADES_DA_ESPERANCA.md é o estudo preliminar escrito antes dos módulos047. Seus OPEN registram pendências daquele momento. As propriedades agora demonstradas são as enumeradas neste parecer e nos enunciados compilados. As derivações individuais precedem suas fontes; o plano de integração precede o lote final, não todos os ensaios.

[OPEN] H3, seleção física da área, ação de horizontes sobre tangentes/regiões e reconstrução gravitacional geral. As obstruções045 ao relógio definido só pelo estado e a liberdade de escala de formas invariantes não foram removidas por esses teoremas. Horizonte algébrico não é automaticamente horizonte de espaço-tempo. Nenhuma confirmação física ou alteração de gate.

## Critérios da ordem010

| Critério | Resultado e limite |
|---|---|
| A.3 — expectativa para todo perfil |046 fornece o habitante;047 prova suas propriedades adicionais sem periodicidade. |
| Não circularidade | CP e normalidade são conclusões; nenhum campo novo assume a própria propriedade a provar. |
| A.1–A.2 — horizontes | Construções045 e covariância046 preservadas como antecedentes; nenhum shift unilateral inventado. |
| B — relógio/H3 | As obstruções anteriores permanecem; positividade e normalidade não selecionam a geometria. |
| C — área | Nenhuma escala/protocolo de área física é fixado por047. |
| Guardas008/010 | Lote limpo conjunto, importador, fontes congeladas, cobertura de axiomas, revisão independente e escritas somente em Chatgpt. |

## Fronteira da auditoria

Fontes novas são copiadas exatamente; o fechamento transitivo LOCAL usa cópias pinadas de dependências históricas. LEAN_PATH não usa a raiz Chatgpt nem o build canônico como fallback. CentralizerDensity usa o antecedente035 com instâncias nomeadas; o original033 com instâncias anônimas não é recompilado.

Binários históricos são rechecados, não reconstruídos. Fontes canônicas sem pin de origem servem para descobrir imports; não se inventa correspondência fonte–binário. Imports diretos externos para Mathlib/pacotes/toolchain são registrados; o fechamento transitivo EXTERNO completo não é exaustivamente hashado.

Sondas são desenvolvimento, não evidência final. Tentativas, logs e backups permanecem preservados. O manifesto é emitido após a entrega para evitar autorreferência de hashes. Nenhuma alteração no um.py, kernel canônico, Atlas, memórias, gate ou selos anteriores faz parte047.
"""
    report="# CONTINUAÇÃO047 — propriedades da expectativa para perfil geral\n\n"+stats+"\n"+"\n".join(table)+"\n\n"+body
    new(ROOT/"CONTINUACAO047_PARECER.md",report)
    artifacts=["CONTINUACAO047_PARECER.md","CONTINUACAO047_DERIVACAO_PREVIA.md",
      "NOTA047_PROPRIEDADES_DA_ESPERANCA.md",*[row["module"]+".lean" for row in build["sources"]],
      *["DERIVACAO047_"+name+".md" for name in
        ["ALGEBRA","POSITIVIDADE","REPRESENTACAO","BLOCOS","CP","CONTINUIDADE","LIMITE_MONOTONO","NORMALIDADE","INFRA"]],
      "CONTINUACAO047_REVISAO_INDEPENDENTE.md","clean_continuation047.py",
      "audit_continuation047.py","probe_continuation047.py","CONTINUACAO047_CLEAN_BUILD.json","finalize_reports047.py"]
    hashes=["| Artefato | Bytes | SHA256 lido dos bytes |","|---|---:|---|"]
    for name in artifacts:
      p=ROOT/name;b=p.read_bytes()
      hashes.append(f"| {link(p)} | {len(b)} | {hashlib.sha256(b).hexdigest()} |")
    delivery=("# ENTREGA047 — expectativa normal e completamente positiva\n\n"
      +datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
      +". Bancada ChatGPT → túnel. Continuação do alvo A.3 da ORDEM_010.\n\n"
      +stats+"\n"+"\n".join(table)+"\n\n"+body+"\n## Artefatos\n\n"+"\n".join(hashes)
      +'\n\nAuditoria selada, somente leitura:\n\n'
      +'    C:\\Python314\\python.exe -B "C:\\IALD\\Central de Patentes\\Chatgpt\\audit_continuation047.py"\n\n'
      +'CONTINUACAO047_MANIFESTO.json será emitido após esta entrega. O comando acima verifica o selo quando presente.\n\n'
      +'H3: OPEN. Reconstrução gravitacional geral: OPEN. Meta ampla de gravidade quântica: OPEN. Gate canônico intocado.\n\n'
      +'Somente o operador decide a incorporação ao acervo canônico e a confirmação física; esta entrega não realiza esses atos.\n')
    target=ROOT/"TUNEL/DO_CHATGPT/ENTREGA_047_propriedades_da_expectativa.md"
    new(target,delivery)
    print(json.dumps({"delivery":str(target),"counts":c,"audit":audit,"hash_rows":len(artifacts)}))

if __name__=="__main__":main()
