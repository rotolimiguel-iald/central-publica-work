"""Create046 final documents from audited evidence; do not replace existing outputs."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parent
def new(path,text):
    assert path.resolve().is_relative_to(ROOT) and not path.exists()
    assert not (ROOT/"CONTINUACAO046_MANIFESTO.json").exists()
    b=text.encode("utf-8");t=path.with_name(path.name+".tmp")
    with t.open("xb") as f:f.write(b);f.flush();os.fsync(f.fileno())
    assert t.read_bytes()==b;t.rename(path)
    assert path.read_bytes()==b
def link(p):return f"[{p.name}](</{p.as_posix()}>)"
def main():
    marker=ROOT/"CONTINUACAO046_CLEAN_BUILD.json"
    build=json.loads(marker.read_text(encoding="utf-8"))
    assert build["status"]=="PASS" and build["development_only"] is False
    result=subprocess.run([sys.executable,"-B",str(ROOT/"audit_continuation046.py"),"--build-only"],
        cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    assert result.returncode==0,result.stdout.decode("utf-8",errors="replace")
    audit=json.loads(result.stdout.decode("utf-8"));assert audit["status"]=="BUILD_PASS"
    review=ROOT/"CONTINUACAO046_REVISAO_INDEPENDENTE.md"
    assert review.is_file() and "BUILD_PASS" in review.read_text(encoding="utf-8")
    clean=Path(build["clean_directory"])
    frozen=json.loads((clean/"FROZEN_INPUTS.json").read_text(encoding="utf-8"))
    c=audit["counts"]
    stats=(f'[REAL — lote final] {len(build["steps"])}/{len(build["steps"])} etapas PASS: seis módulos e Imports046All. '
      f'{c["theorems"]} teoremas, {c["definitions"]} definições/estruturas, {c["axiom_prints"]} declarações '
      f'com axiomas impressos e {c["instances"]} instâncias novas. Somente propext, Classical.choice e Quot.sound; '
      'zero erros/avisos. Todos os seis módulos são novos046; dependências históricas não são contadas como novidade.\n\n'
      f'[REAL — auditoria] BUILD_PASS. {len(frozen)} registros congelados idênticos antes/depois; '
      f'{len(build["files"])} arquivos no inventário do build; {audit["historical_records"]} registros históricos '
      'revalidados pelo auditor. Diretório final: '+link(clean)+'.\n')
    table=["| Módulo | Teoremas | Definições | Prints |","|---|---:|---:|---:|"]
    for row in build["sources"]:
      table.append(f'| {row["module"]} | {row["theorems"]} | {row["definitions"]} | {len(row["expected_axiom_rows"])} |')
    body="""## Resultado e cadeia

[REAL — Lean] aperiodicExpectationInput(P):ExpectationInput(P) foi construído para TODO P:SiteProfile desta torre binária, sem hipótese de periodicidade ou de esperança prévia. O nome aperiódico inclui perfis periódicos como casos particulares. Para A no fator M e todo vetor v:

    C_n(A)v = (n+1)⁻¹ ∫₀ⁿ⁺¹ σ_t(A)v dt  →  E(A)v.

1. A média da fase r≠0 tem norma≤2/(|r|T); a fase zero permanece1. O limite matricial é specExpect: sobrevivem todos os blocos de pesos iguais, inclusive degenerados.
2. A média de U(t)v é uma contração em todo o Hilbert. A convergência local, a densidade do pré-Hilbert e a completude produzem um limite para cada vetor.
3. Em AΩ, esse limite coincide com a média por conjugação. As médias C_n(A) pertencem a M e têm norma≤‖A‖. Sua comutação com a ação direita local propaga o limite em Ω a uma família densa; a cota uniforme dá convergência forte em todos os vetores. O operador B resultante pertence ao bicomutante que define M, tem norma≤‖A‖ e é determinado por BΩ. B e sua convergência não foram presumidos.
4. Em cada corte N, towerExpectation N(E A) é towerPi(specExpect(towerW N)(expectationMatrix N A)). A igualdade vem da continuidade da projeção, limite local e separância.
5. Pinching e limites GNS provam into, fixes e ortho. Em M, ‖E(A)‖≤‖A‖ e E(E(A))=E(A); não se afirma aqui um lema de Lipschitz.
6. A composição com the_lift_on_the_tower dá Ad(h)∘E=E∘Ad(h) em M para todo h:TowerHorizon P. A unicidade identifica o termo com qualquer outro habitante sobre M, inclusive os periódicos e traciais. A covariância de E∘K mantém as hipóteses de que K preserva M e é covariante.

Classical.choice escolhe limites de existência demonstrada. Isso não é um algoritmo numérico com taxa uniforme de convergência.

## Critérios da ordem

| ORDEM_010 | Resultado e limite |
|---|---|
| A.3 — perfil aperiódico | Pago no registro ExpectationInput para todo perfil admissível; limite e operador são construídos. |
| A.3 — ausência de circularidade | Não se usa TakesakiInput.expectation como premissa; usam-se médias, densidade, completude, cota uniforme e bicomutante. |
| A.1–A.2 — horizontes | Construções045 preservadas como antecedentes. O novo termo é covariante por qualquer horizonte do contrato; nenhum shift unilateral novo. |
| B — relógio/H3 | As obstruções045 permanecem; o novo habitante não seleciona geometria nem remove a diferença entre os relógios requeridos por telas distintas. |
| C — área | Covariância algébrica obtida; a ação física em tangentes e a normalização de área continuam abertas. |
| Guardas008/010 | Seis módulos juntos, importador, cobertura de axiomas, termos nomeados, revisão independente e custódia; escritas somente em Chatgpt. |

## Limites formais e físicos

[OPEN] ExpectationInput tem os campos E, into, fixes e ortho. A normalidade, positividade completa, linearidade e bimodularidade não são campos desse registro. Esta entrega prova adicionalmente ‖E(A)‖≤‖A‖, idempotência e limite forte em M; não declara as demais propriedades formalizadas. Fora de M, E é zero por definição; não há promessa de linearidade em todo B(H).

[OPEN] Normalidade não decorre automaticamente da frase limite de médias. Essas propriedades adicionais ainda exigem provas próprias.

[OPEN] Horizonte algébrico e resposta covariante E∘K precisam ser ligados a regiões, métrica, telas, área e dinâmica gravitacional. H3 e a reconstrução gravitacional geral continuam abertos. Covariância não seleciona sozinha a escala ou o protocolo de área.

## Fronteira da auditoria

Fontes novas são cópias exatas; dependências locais transitivas são copiadas com pins históricos. LEAN_PATH não usa a raiz Chatgpt ou o build canônico como fallback. Binários históricos são rechecados, não reconstruídos. Fontes canônicas históricas sem pin de origem servem à descoberta de imports: não se inventa correspondência fonte–binário. Imports diretos que cruzam para Mathlib/pacotes/toolchain são registrados; o fechamento transitivo externo completo não foi hashado.

Probes e tentativas são desenvolvimento; logs e backups foram preservados. O manifesto final é emitido após a entrega para evitar autorreferência de hashes. Nenhuma alteração em um.py, kernel canônico, Atlas, memórias, gate ou selos anteriores.
"""
    report="# CONTINUAÇÃO046 — esperança modular para perfil geral\n\n"+stats+"\n"+"\n".join(table)+"\n\n"+body
    new(ROOT/"CONTINUACAO046_PARECER.md",report)
    artifacts=["CONTINUACAO046_PARECER.md","CONTINUACAO046_DERIVACAO_PREVIA.md",
      *[row["module"]+".lean" for row in build["sources"]],
      "DERIVACAO046_APERIODICA.md","DERIVACAO046_LEVANTAMENTO.md","DERIVACAO046_VETORIAL.md",
      "DERIVACAO046_PREFIXO.md","DERIVACAO046_ESPERANCA.md","DERIVACAO046_LEVANTAMENTO_GERAL.md",
      "DERIVACAO046_INFRA.md","CONTINUACAO046_REVISAO_INDEPENDENTE.md","clean_continuation046.py",
      "audit_continuation046.py","probe_continuation046.py","CONTINUACAO046_CLEAN_BUILD.json","finalize_reports046.py"]
    hashes=["| Artefato | Bytes | SHA256 lido dos bytes |","|---|---:|---|"]
    for name in artifacts:
      p=ROOT/name;b=p.read_bytes()
      hashes.append(f"| {link(p)} | {len(b)} | {hashlib.sha256(b).hexdigest()} |")
    delivery=("# ENTREGA046 — média modular e esperança para perfil geral\n\n"
      +datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
      +". Bancada ChatGPT → túnel. Resposta à ORDEM_010, alvo A.3.\n\n"
      +"[REAL — Lean] aperiodicExpectationInput P construído para todo perfil admissível. "
      +"A existência da esperança e do limite forte são conclusões. A hipótese de período comum foi retirada.\n\n"
      +stats+"\n"+"\n".join(table)+"\n\n"+body+"\n## Artefatos\n\n"+"\n".join(hashes)
      +'\n\nAuditoria selada, somente leitura:\n\n'
      +'    C:\\Python314\\python.exe -B "C:\\IALD\\Central de Patentes\\Chatgpt\\audit_continuation046.py"\n\n'
      +'CONTINUACAO046_MANIFESTO.json será emitido após esta entrega. O comando acima verifica o selo quando presente.\n\n'
      +'H3: OPEN. Normalidade/CP: OPEN na formalização. Reconstrução gravitacional geral: OPEN. '
      +'Meta ampla de gravidade quântica: OPEN. Gate canônico intocado.\n\n'
      +'Somente o operador decide a incorporação ao acervo canônico e a confirmação física; esta entrega não realiza esses atos.\n')
    target=ROOT/"TUNEL/DO_CHATGPT/ENTREGA_046_media_modular_e_expectativa.md"
    new(target,delivery)
    print(json.dumps({"delivery":str(target),"counts":c,"audit":audit,"hash_rows":len(artifacts)}))
if __name__=="__main__":main()
