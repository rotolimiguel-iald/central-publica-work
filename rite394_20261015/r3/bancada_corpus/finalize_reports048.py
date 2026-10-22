"""Create048 reports only after final clean compilation and independent audit."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, os, subprocess, sys
ROOT=Path(__file__).resolve().parent

def new(path,text):
    assert path.resolve().is_relative_to(ROOT) and not path.exists()
    assert not (ROOT/"CONTINUACAO048_MANIFESTO.json").exists()
    raw=text.encode("utf-8")
    temp=path.with_name(path.name+".tmp")
    with temp.open("xb") as f:
        f.write(raw);f.flush();os.fsync(f.fileno())
    assert temp.read_bytes()==raw
    temp.rename(path)
    assert path.read_bytes()==raw

def link(p):return f"[{p.name}](<{p.as_posix()}>)"

def main():
    marker=ROOT/"CONTINUACAO048_CLEAN_BUILD.json"
    build=json.loads(marker.read_text(encoding="utf-8"))
    assert build["status"]=="PASS" and build["development_only"] is False
    run=subprocess.run([sys.executable,"-B",str(ROOT/"audit_continuation048.py"),"--build-only"],
        cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    assert run.returncode==0,run.stdout.decode("utf-8",errors="replace")
    audit=json.loads(run.stdout.decode("utf-8"))
    assert audit["status"]=="BUILD_PASS"
    review=ROOT/"CONTINUACAO048_REVISAO_INDEPENDENTE.md"
    assert review.is_file()
    review_text=review.read_text(encoding="utf-8")
    assert "BUILD_PASS" in review_text
    assert "Build SHA256: "+hashlib.sha256(marker.read_bytes()).hexdigest() in review_text
    assert "Diretório final: "+Path(build["clean_directory"]).as_posix() in review_text
    c=audit["counts"]
    clean=Path(build["clean_directory"])
    before=json.loads((clean/"FROZEN_INPUTS.json").read_text(encoding="utf-8"))
    after=json.loads((clean/"FROZEN_INPUTS_AFTER.json").read_text(encoding="utf-8"))
    assert before==after
    stats=(f'[REAL — lote final] {len(build["steps"])}/{len(build["steps"])} etapas PASS; '
        f'{len(build["sources"])} módulos mais Imports048All. {c["theorems"]} teoremas, '
        f'{c["definitions"]} definições/estruturas, {c["instances"]} instâncias novas e '
        f'{c["axiom_prints"]} declarações com axiomas impressos. '
        'Zero erros/avisos; axiomas no máximo propext, Classical.choice e Quot.sound.\n\n'
        f'[REAL — auditoria] BUILD_PASS; {len(before)} registros congelados iguais antes/depois; '
        f'{len(build["files"])} arquivos no inventário do build; '
        f'{audit["historical_records"]} registros históricos revalidados. '
        'Dependências históricas não são contadas como teoremas novos.\n\n'
        'Diretório final: '+link(clean)+'.\n')
    table=["| Módulo | Teoremas | Definições | Instâncias | Prints |","|---|---:|---:|---:|---:|"]
    for row in build["sources"]:
        table.append(f'| {row["module"]} | {row["theorems"]} | {row["definitions"]} | '
                     f'{len(row["instances"])} | {len(row["expected_axiom_rows"])} |')
    body="""## Resultado e hipóteses

[REAL — Lean] A obstrução de Borchers da torre-produto sobrevive ao transporte concreto de estado027. Para todo P,Q com afinidade positiva, uma família V(a) de operadores no Hilbert P, fortemente contínua em zero, V(0)=I e que preserva normas, é trivial se satisfaz
profileFlowConjugation(t,V(a))=V(exp(-2*pi*t)*a).
O argumento conjuga V de volta ao Hilbert Q pelo profileGNSUnitary, aplica product_borchers_trivial e retorna a P. Não exige um período comum, lei de grupo de V nem um gerador positivo como hipóteses adicionais. Também não afirma que toda dinâmica geométrica satisfaz essa relação: ela permanece explícita no enunciado.

[REAL — Lean] Um período do fluxo algébrico força retorno dos rótulos em qualquer localização fiel covariante. Para famílias A(r) de conjuntos de operadores da torre, o período e a covariância sob r↦exp(-rate*t)*r forçam A(exp(-rate*T))=A(1). Se esses dois rótulos forem distinguidos, há contradição. A forma com localização injetiva, T>0 e rate≠0 deduz a separação necessária.

[REAL — aplicação concreta] A referência estacionária thirdThermalReference, de peso 1/3, tem período positivo já demonstrável pelos lemas existentes. O boost044 satisfaz exatamente boostFlow(rate,t,centralNullCurve(r))=centralNullCurve(exp(-rate*t)*r). A048 liga esse fluxo geométrico à obstrução: para rate ≠ 0, uma associação N de pontos/rótulos centrais a conjuntos de operadores, injetiva ao longo do raio e globalmente covariante sob o boost e o fluxo modular periódico, não existe. O mapa N é quantificado no negativo, não produzido como rede física.

## Limites da conclusão

[OPEN] Uma álgebra correspondente a um wedge isolado invariante não distingue os rótulos utilizados; não é excluída. O argumento por período não exclui perfis aperiódicos. O enunciado compilado assume covariância global; versões locais exigem examinar domínios e composição, e versões aproximadas exigem outro controle. Covariância exata numa vizinhança uniforme de zero pode ser iterada até o período quando as ações compõem e o domínio permite. O primeiro argumento cobre o fluxo transportado de qualquer perfil-produto de afinidade positiva, mesmo sem período comum, somente sob sua relação de Borchers.

[OPEN] Nenhum dos negativos é impossibilidade geral de Bisognano–Wichmann ou da gravitação. Uma representação com dados modulares diferentes continua uma rota a investigar. Apenas conjugá-los unitariamente como na027 não sai da classe demonstradamente obstruída.

[OPEN] H3 e a reconstrução física geral continuam em aberto. A028 já separa o casamento de calor do casamento de área; o último é equivalente, sob suas hipóteses geométricas e de fonte, a eta Ric(d,d)=2*pi T(d,d). A hipótese em einstein_from_summable_area_matching continua visível. A048 não a deriva, não ajusta a métrica para esconder a hipótese e não seleciona a escala de área.

A proposta de classificação de formas invariantes por infinitas permutações e a comparação com princípios variacionais estão registradas, com estatutos próprios, em NOTA048_MAPA_DAS_HIPOTESES.md. Não são resultados Lean048.

## Critérios das ordens

| Critério | Resultado e alcance |
|---|---|
|007 C — identificação modular/geométrica| Novo controle do fluxo027 e controle de localização sob o boost044. A identificação física segue OPEN.|
|010 A — expectativa e horizontes| Antecedentes045–047 preservados; a048 não repete nem integra suas provas.|
|010 B — H3/relógio| Negativos finitos e casamento infinitesimal condicional anteriores permanecem.|
|010 C — regiões/área| Condição de fidelidade e covariância agora testada contra período. Nenhuma rede física ou escala de área construída.|
|Não circularidade| Injetividade, covariância e Borchers aparecem como hipóteses testadas; não como existência decretada de um objeto.|
|008/010 — custódia| Dois módulos em lote final limpo, Imports048All, cobertura de axiomas, revisão independente e escritas restritas a Chatgpt.|

## Fronteira da auditoria

Fontes048 copiadas byte a byte. O fechamento transitivo local usa dependências pinadas dos manifests006/007/029/032/033/034/035/036/037/040/041/043/044/045/046. A044 é necessária ao boost; a048 não importa teoremas novos047. Nenhum fallback em LEAN_PATH para a raiz Chatgpt ou o build canônico.

As fontes e evidências dos lotes históricos usados como overrides são rechecadas pelo auditor, não reconstruídas. Fontes canônicas sem pin histórico servem à descoberta de imports; não se fabrica a relação fonte-binário. Os imports diretos para Mathlib/pacotes/stdlib e a ferramenta Lean são registrados; a fronteira externa transitiva inteira não foi reconstruída nem exaustivamente hashada.

As derivações específicas antecedem seus respectivos módulos. O plano da integração e da infraestrutura antecede o lote final; não se apresenta como anterior a todo ensaio de desenvolvimento. Sondas por módulo têm marca explícita de desenvolvimento e não substituem o lote final. Tentativas, logs e backups são preservados.

Nenhuma alteração no um.py, kernel canônico, Atlas, índice, memórias, gate ou selos anteriores integra esta continuação. O manifesto é emitido depois da entrega para evitar um hash autorreferente. NOT_FALSIFIED não é CONFIRMED.
"""
    report="# CONTINUAÇÃO048 — controles da identificação modular com a geometria\n\n"+stats+"\n"+"\n".join(table)+"\n\n"+body
    new(ROOT/"CONTINUACAO048_PARECER.md",report)
    artifacts=["CONTINUACAO048_PARECER.md","CONTINUACAO048_DERIVACAO_PREVIA.md",
        "NOTA048_MAPA_DAS_HIPOTESES.md","DERIVACAO048_TRANSPORTE.md",
        "DERIVACAO048_LOCALIZACAO.md","DERIVACAO048_INFRA.md",
        *[s["module"]+".lean" for s in build["sources"]],
        "CONTINUACAO048_REVISAO_INDEPENDENTE.md","clean_continuation048.py",
        "audit_continuation048.py","CONTINUACAO048_CLEAN_BUILD.json","finalize_reports048.py"]
    hashes=["| Artefato | Bytes | SHA256 lido dos bytes |","|---|---:|---|"]
    for name in artifacts:
        p=ROOT/name;raw=p.read_bytes()
        hashes.append(f"| {link(p)} | {len(raw)} | {hashlib.sha256(raw).hexdigest()} |")
    delivery="# ENTREGA048 — limites concretos da identificação modular/geométrica\n\n"
    delivery+=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")+". Bancada ChatGPT → túnel.\n\n"
    delivery+=stats+"\n"+"\n".join(table)+"\n\n"+body+"\n## Artefatos\n\n"+"\n".join(hashes)
    delivery+='\\n'.replace("\\n","\n")+"\nAuditoria selada, somente leitura:\n\n"
    delivery+='    C:\\Python314\\python.exe -B "C:\\IALD\\Central de Patentes\\Chatgpt\\audit_continuation048.py"\n\n'
    delivery+="CONTINUACAO048_MANIFESTO.json será emitido após esta entrega; o comando verifica o selo quando presente.\n\n"
    delivery+="H3: OPEN. Reconstrução gravitacional geral: OPEN. Meta ampla de gravidade quântica: OPEN. Gate canônico intocado.\n\n"
    delivery+="Somente o operador decide a incorporação ao acervo canônico e a confirmação física; esta entrega não realiza esses atos.\n"
    target=ROOT/"TUNEL/DO_CHATGPT/ENTREGA_048_obstrucoes_da_identificacao_geometrica.md"
    new(target,delivery)
    print(json.dumps({"delivery":str(target),"counts":c,"audit":audit,"hash_rows":len(artifacts)}))

if __name__=="__main__":main()
