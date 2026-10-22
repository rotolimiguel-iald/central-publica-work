from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import uuid

WORK = Path("C:/IALD/Central de Patentes/Chatgpt").resolve()
OUT = Path(__file__).resolve().parent
ORIGIN = WORK / "COMPLEXO_RELATIVO_QUADRATICO_087_20260910_070916_3378612"
if not OUT.is_relative_to(WORK):
    raise RuntimeError("Unauthorized output folder")

def read_pin(path):
    path = Path(path).resolve()
    data = path.read_bytes()
    st = path.stat()
    return {"path": path.as_posix(), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(), "mtime_ns": st.st_mtime_ns}, data

def publish(path, data):
    path = Path(path).resolve()
    if not path.is_relative_to(OUT) or path.exists():
        raise RuntimeError("Only new output files inside review directory")
    temp = path.with_name(path.name + ".pending_" + uuid.uuid4().hex)
    with temp.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    if temp.read_bytes() != data:
        raise RuntimeError("Temporary bytes differ")
    if path.exists():
        raise FileExistsError(str(path))
    os.rename(temp, path)
    if path.read_bytes() != data:
        raise RuntimeError("Final bytes differ")
    return read_pin(path)[0]

def publish_json(path, obj):
    return publish(path, (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))

manifest_path = ORIGIN / "MANIFESTO_RELATIVO_CE_087.json"
manifest_pin, manifest_data = read_pin(manifest_path)
origin = json.loads(manifest_data)
extra_paths = [
    WORK / "REVISAO_REDUCAO_QUADRATICA_081_20260910_050052_914909/PARECER_H3_E5_E_REPRESENTANTES_QUADRATICOS_081.md",
    WORK / "REVISAO_CE_QUADRATICO_082_20260910_053047_6990258/PARECER_IDENTIFICACAO_CE_082.md",
]
origin_pin_records = origin["sources_before"] + [origin["note"], origin["capture"], origin["helper"]]
paths = list(dict.fromkeys(
    [manifest_path.as_posix()] + [item["path"] for item in origin_pin_records] +
    [p.as_posix() for p in extra_paths] + [Path(__file__).resolve().as_posix()]
))
before, raw = {}, {}
for path in paths:
    entry, data = read_pin(path)
    before[entry["path"]] = entry
    raw[entry["path"]] = data
checks = []
def check(name, passed, detail=None):
    checks.append({"name": name, "passed": bool(passed), "detail": detail})
for item in origin_pin_records:
    measured = before[Path(item["path"]).resolve().as_posix()]
    check("origin_pin_current:" + Path(item["path"]).name,
          measured["bytes"] == item["bytes"] and measured["sha256"] == item["sha256"],
          {"recorded": item, "current": measured})
for historical_before, historical_after in zip(origin["sources_before"], origin["sources_after"]):
    check("manifest_before_after_equal:" + Path(historical_before["path"]).name,
          historical_before == historical_after)
check("same_number_historical_inputs", len(origin["sources_before"]) == len(origin["sources_after"]))
check("manifest_documentary_checks_consistent",
      origin["checks_total"] == len(origin["checks"]) and
      origin["checks_passed"] == sum(item["passed"] for item in origin["checks"]) and
      not origin["failed_checks"])
check("origin_no_mathematical_runs",
      origin["new_mathematical_executions"] == 0 and origin["new_cas_runs"] == 0 and origin["new_lean_runs"] == 0)
source_path = Path(origin["note"]["path"]).resolve().as_posix()
source_text = raw[source_path].decode("utf-8-sig")
source_links = list(dict.fromkeys(re.findall(r"\]\(<(C:/[^>]+)>\)", source_text)))
for link in source_links:
    check("source_link_exists:" + Path(link).name, Path(link).is_file(), link)
if not all(item["passed"] for item in checks):
    publish_json(OUT / "FALHA_DOCUMENTAL_PRE_REVISAO_087.json", {"checks": checks, "before": before})
    raise RuntimeError("Documentary precondition failed")

note = r"""# Parecer independente: geração curva, cohomologia relativa e CE quadrático — 087

10/09/2026. Revisor /root/prepare_integration_83. [DERIVED — revisão matemática escrita]. [REAL — custódia documental medida]. Nenhuma execução matemática, CAS, Lean ou um.py.

**Parecer favorável; não identifiquei erro material no contrato fixado.** Li integralmente a [nota de /root/finish_gibbs_realization](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_RELATIVO_QUADRATICO_087_20260910_070916_3378612/GERACAO_CURVA_RELATIVO_E_CE_QUADRATICO.md>) e o [manifesto](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_RELATIVO_QUADRATICO_087_20260910_070916_3378612/MANIFESTO_RELATIVO_CE_087.json>). Conferi a geração curva dos escalares e das uma-formas, a paridade que elimina as duas-formas, a diagonal2 de □ e os restos, o quociente relativo e a passagem finita ao CE inteiro invariante pela isotropia.

A fonte mede {BYTES} bytes; SHA-256 lido nesta revisão: {HASH}. Os pins atuais e as comparações com o manifesto histórico estão no recibo. O resultado é novo087; não é retroativamente atribuído à entrega086.

## 1. O quociente e o domínio foram mantidos

O fundo é uma espaço-forma Lorentziana ORIENTADA de dimensão quatro, K>0 real fixado, κ real não nulo, sigma constante já projetado. Rher é uma álgebra real unital não nula de coeficientes inertes. Não é exigida integridade ou ausência de nilpotentes. Não há tensores espectadores, funções coordenadas ativas, operadores variando com novos campos ou infinitos jatos num único elemento.

Mcal=kerγ/E está no quociente U/E das MESMAS EOM Einstein lineares e todos os seus prolongamentos. N₂=Rher⊗Sym²Mcal é uma potência simétrica algébrica, não um conjunto de valores em algumas soluções TT. As variáveis de Weyl são bosônicas. A orientação permite o pseudoescalar com estrela; impor também reflexões como simetrias que excluam epsilon mudaria essa categoria.

A [estriteza086](<C:/IALD/Central de Patentes/Chatgpt/SIMBOLO_DIVERGENCIA_TODAS_ORDENS_086_20260910/ESTRITEZA_E_DETECTOR_PRINCIPAL_DE_DIVERGENCIA.md>) foi consumida com seu [parecer independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_SIMBOLO_DIVERGENCIA_086_20260910_064135_2856684/PARECER_ESTRITEZA_E_DIVERGENCIA_086.md>). Ela dá a injeção graduada com a derivada principal. A presente prova não necessita transformar essa injeção numa isomorfia de TODA a torre curva.

A filtração relevante é pela SOMA das ordens dos dois fatores em h. K tem grau zero porque está fixado. Confundir essa soma com a maior ordem de um fator alteraria a diagonal e invalidaria a redução; a fonte usa a soma correta.

## 2. Por que I_r e J_r realmente realizam os símbolos necessários

T_r=∇̄_(a₁…a_r)W[1] é um tensor natural linear, de simetrização normalizada e ordem r+2. O gauge linear comuta com a conexão de fundo e W(g₀)=0 implica γW[1]=0. Assim T_r e suas contrações quadráticas definem elementos efetivos do quociente.

No plano, os dois tipos são W_r^+=(r+4,r), W_r^-=(r,r+4), em pesos INTEIROS 2j. Singlete em um produto do mesmo sinal exige r=s. Um produto cruzado exigiria simultaneamente r+4=s e r=s+4, o que é impossível. A multiplicidade em cada canal permitido é um e a troca tem sinal (−1)^(2r+4)=+1, compatível com Sym².

I_r=½⟨T_r,T_r⟩ e J_r=½⟨T_r,*T_r⟩ possuem símbolos que distinguem os dois canais por uma matriz invertível: *²=−1 e os autovalores são ±i. A forma real Lorentziana troca as quiralidades, deixando duas direções REAIS, não quatro. A simetrização normalizada é identidade no símbolo plano e não introduz r!.

A não nulidade não é inferida apenas da representação. As duas ondas métricas planas da086 realizam cada quiralidade separadamente e detectam o singlete em todas as ordens. Se a expressão curva fosse de ordem efetiva menor, sua imagem principal no quociente plano, calculada pela estriteza, seria zero. Isso contradiz a avaliação plana. Portanto ord_eff(I_r)=ord_eff(J_r)=2r+4, com símbolos independentes.

Esse argumento demonstra exatamente os levantamentos CURVOS necessários. Para gerar um escalar arbitrário, seu maior símbolo pertence ao espaço de duas cópias; subtrair a combinação correspondente de I_r,J_r reduz estritamente a ordem. A indução termina. Uma relação finita teria um maior r e contrariaria a independência dos símbolos. Segue a soma direta B⁰=⊕_(r≥0)(Rher I_r⊕Rher J_r).

A normalização de I é a da nota086 de uma derivada, e seu [parecer específico](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CORRENTES_UMA_DERIVADA_086_20260910_065540_575112/PARECER_CLASSIFICACAO_E_NORMALIZACAO_086.md>) fixa I082=2I₀. J mantém a normalização anterior. Esse fator está declarado na fonte087 e não ficou escondido num nome comum.

## 3. Graus um e dois: os dois controles distintos

Para um vetor, o alvo é (1,1). Em um produto do mesmo sinal, a sobreposição exige |r−s|=1 e tem multiplicidade um; os canais cruzados não fornecem o vetor. No grau2r+5, dI_r,dJ_r realizam os dois símbolos: a divergência plana desses gradientes é não nula no teste de duas ondas, logo os próprios gradientes são não nulos.

A mesma redução do maior grau demonstra que TODA uma-forma efetiva é um gradiente de combinação finita dos I_r,J_r. Seu núcleo é zero pelos símbolos; B⁰ não contém a constante da álgebra total, pois está na parte quadrática. Assim d_B:B⁰→B¹ é isomorfismo de módulos.

O argumento para B² é de paridade, e não uma aplicação da conclusão sobre vetores. Para Λ²V*=(2,0)⊕(0,2), o singlete do segundo ou primeiro fator sl₂ exige r=s nos produtos do mesmo sinal. No alvo(2,0), o sinal de troca é

    (−1)^(r+3) (−1)^r = −1.

No alvo(0,2), quando r≥1, ele é

    (−1)^(r+4) (−1)^(r−1) = −1.

O caso r=0 em que não há alvo é corretamente separado. O tipo pertence a Λ²W_r, não a Sym²W_r. Usar derivados distintos antes da simetrização não recupera uma cópia adicional: no graduado, o singlete que força r=s está no mesmo fator irreducível, e a troca na potência simétrica é obrigatória.

Nos canais cruzados, igualar o peso que deve formar singlete deixa diferença OITO no outro, maior que o alvo de peso dois. Nenhum canal serve. Portanto o espaço plano de duas-formas é zero em todas as ordens; a injeção graduada impede um elemento curvo não nulo. B²=0 está demonstrado sem presumir sobrejetividade curva.

## 4. Diagonal2 de □: todos os slots e os termos inferiores

A definição q_V=ι_Vν fixa sem ambiguidade o sinal d_Bq_V=(div₀V)ν em assinatura Lorentziana. A identificação de B³ com os vetores e B⁴=B⁰ν é natural pela métrica e orientação. Não se usa um sinal Hodge implícito para substituir essa equação.

A contração é bilinear e a métrica e a estrela são paralelas. Logo

    □(½⟨T,T⟩)=⟨∇̄T,∇̄T⟩+⟨T,□T⟩,

e a fórmula dual tem o mesmo fator porque a bilinear com estrela é simétrica. Todos os índices de T e dos seus derivados são covariantes no comutador.

Na espaço-forma, ∇̄R₀=0. Expandir [□,∇̄] produz R₀·∇̄T; os termos (∇̄R₀)·T desaparecem por essa hipótese, não por ignorar conexão. Iterar sobre r derivados, usando □W=6KW no quociente linear e seus prolongamentos, mostra que □T_r tem ordem no máximo r+2 em h. A segunda parcela de Leibniz tem ordem≤2r+4.

Já ∇̄T_r−T_(r+1) é uma soma de comutadores: cada troca retira duas derivadas e introduz curvatura. Para r≥1, contém no máximo r−1 derivados de W, isto é, ordem r+1 em h; para r=0 é zero. Seu produto com T_(r+1), de ordem r+3, tem ordem≤2r+4. O termo principal é portanto exatamente

    ⟨T_(r+1),T_(r+1)⟩ = 2I_(r+1),

ou 2J_(r+1) na versão dual. A simetrização normalizada não altera o coeficiente DOIS.

Assim □I_r=2I_(r+1)+L_r e □J_r=2J_(r+1)+L'_r, com restos de ordem≤2r+4. Pela geração de B⁰, os restos são combinações de índices≤r. A prova não exige que o resto seja simplesmente um múltiplo de K I_r ou K J_r. Em r=0, os controles □I₀=2I₁+12KI₀ e □J₀=2J₁+12KJ₀ concordam com a convenção previamente revisada.

Esse cálculo é no quociente Einstein LINEAR efetivo. Não utiliza a equação não linear de onda de Weyl nem aplica □ plana a um tensor curvo.

## 5. O quociente relativo tem posto dois e não precisa de inversa de □

Uma expressão F finita tem maior índice. A diagonal2 permite retirar a parcela de índice r+1 subtraindo □ da combinação correspondente de I_r,J_r dividida por dois. Os novos restos têm índices menores. A indução termina em

    F=λI₀+μJ₀+□G,     G finito.

Se λI₀+μJ₀=□G e G≠0, o maior índice r de G produz uma parcela superior não nula de ordem2r+6. Não pode coincidir com a ordem≤4 do lado esquerdo. Se G=0, os símbolos de I₀,J₀ dão λ=μ=0. A redução e a unicidade usam divisão por dois, não uma inversa hiperbólica ou de K.

Portanto B⁰/□B⁰ é livre nas duas classes. No complexo relativo:

    B⁰ --d≅--> B¹ --> 0=B² --> B³ --div injectiva--> B⁴,

H⁰=H¹=H²=H³=0 e H⁴=Rher[I₀ν]⊕Rher[J₀ν]. O símbolo de d em B¹ é zero porque B²=0; isso não é uma hipótese independente de fechamento de todas as uma-formas.

A existência de uma transgressão ordinária por conexão GL não contradiz esse resultado: a transgressão não pertence ao módulo de formas invariantes por gauge de Weyl/EOM usado aqui. Não se amplia a classe de primitivas para calcular o quociente relativo.

## 6. Da isotropia ao CE completo: páginas e graus conferidos

No CE completo h-invariante, p conta ghosts de translação e q ghosts de isotropia. O diferencial decompõe-se em graus (0,1), (1,0), (2,−1). O último é a inserção de curvatura no ghost de isotropia. A filtração por p tem cinco níveis.

Em cada corte finito de ordem de jatos, h age num módulo finito semissimples. Seu cálculo vertical é

    E₁^(p,q)=Bᵖ⊗H^q(h,R).

A operação de tomar h-invariantes é exata nesses cortes; a ação induzida sobre a cohomologia vertical é trivial pela homotopia de Cartan. A passagem ao limite DIRETO algébrico conserva os ciclos e primitivas de suporte finito em jatos. Nenhuma finitude local sob toda a álgebra g de Killing foi usada.

[KNOWN — importação conferida diretamente] O apêndiceB de BBH1995, equações B.1–B.3, expressa ciclos como invariantes de coeficientes multiplicados pelos cociclos primitivos, mais fronteiras, e caracteriza a independência. Na isotropia so(1,3), a complexificação sl₂⊕sl₂ dá duas classes reais de grau três e sua álgebra exterior tem dimensões1,2,1 nos graus0,3,6. Esse é o uso da fonte; não sua hipótese sobre classes características no grau máximo nem um teorema sobre N₂ sob g. [BBH1995](https://arxiv.org/pdf/hep-th/9505173v2).

O diferencial seguinte é d_B no coeficiente horizontal. A parte d_V não deriva os representantes puros constantes em ghosts de isotropia; o termo de curvatura tem incremento p=2 e aparece depois. Assim

    E₂^(p,q)=Hᵖ(B)⊗H^q(h,R).

Pela cohomologia relativa calculada, apenas p=4 resta, com q=0,3,6. Um diferencial posterior de grau(r,1−r), r≥2, sai para p>4 ou chega de uma coluna já zero. Logo E₂=E∞. Cada grau total sobrevivente tem somente uma peça filtrada, o que elimina problemas de extensão entre colunas. A finitude em p basta; não se aplicou ML.

Obtêm-se os postos reais/herdados dois, quatro e dois em graus4,7,10, e zero nos demais. Os representantes I₀ν,J₀ν multiplicados pelos dois cociclos verticais e pelo seu produto são ciclos do CE inteiro: d_V acrescentaria uma quinta translação; d_R do fator vertical acrescentaria duas à ν. Ambos são zero. O fechamento explícito confirma os representantes; a independência e a exaustão vêm das páginas, não de uma simples enumeração.

## 7. Coeficientes, finitude e autoria de antecedentes

A extensão por Rher parte de mapas REAIS já fixados. Toda inclusão de espaço vetorial real e os mapas de símbolo injetivos permanecem injetivos após tensorizar. Dois é unidade em Rher. Um nilpotente não desaparece pela avaliação em uma solução, porque nenhuma avaliação numérica de Rher entra na prova.

A geração e a redução de □ terminam pelo maior índice. As homotopias da isotropia são finitas em cada corte; ainda que a derivada horizontal aumente a ordem, ela é aplicada apenas finitamente muitas vezes no cálculo de uma cochain de ghost finito. Não se produz uma primitiva com infinitos jatos dentro de um coeficiente. A afirmação não passa a uma soma completada ∑a_r I_r sem contrato novo.

Tenho autoria antecedente na redução081, na identificação082 e na prova de uma derivada086. Seus resultados são consumidos com os pareceres independentes da [redução081](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_REDUCAO_QUADRATICA_081_20260910_050052_914909/PARECER_H3_E5_E_REPRESENTANTES_QUADRATICOS_081.md>), da [identificação082](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CE_QUADRATICO_082_20260910_053047_6990258/PARECER_IDENTIFICACAO_CE_082.md>) e da classificação086 já vinculada. Não apresento esta revisão como aprovação independente nova das minhas próprias fontes. A geração CURVA de todos os singletes, a exclusão B², a redução triangular e a composição087 são do autor examinado e foram aqui conferidas independentemente.

## 8. Alcance final do parecer

[DERIVED] No contrato de N₂ declarado, a cohomologia relativa é de posto dois no grau quatro e zero nos demais. O CE completo h-invariante tem postos2/4/2 em graus4/7/10, sem erro material identificado na demonstração.

Esses graus pertencem à diagonal m=E−ghost=2 após o primeiro diferencial por VALÊNCIA. Correspondem às valências6/9/12. O parecer não transforma essas classes em H(s) do BRST completo: diferenciais posteriores podem relacioná-las com outras diagonais. Tampouco calcula uma anomalia física, QME, estado interagente, comparação de fundos, UV ou reconstrução geral. O sigma físico φ=id e a classe causal com suas regularidades/inserções permanecem distintos.

A fonte087 refina086 sem reeditar suas afirmações históricas. A fase/ramo e o H3 interno do programa não são os grupos cohomológicos desta nota.

[REAL — documental] Os arquivos relacionados foram medidos antes/depois e comparados aos pins do manifesto de origem. O helper histórico e sua captura foram apenas lidos/medidos, não executados. Os controles do recibo são documentais, não novas identidades matemáticas executadas. Somente este parecer, recibo e helper novos foram escritos; nenhum original, Atlas, memória, selo, gate ou fonte congelada foi alterado.
"""
note = note.replace("{BYTES}", str(before[source_path]["bytes"])).replace("{HASH}", before[source_path]["sha256"])
review_links = list(dict.fromkeys(re.findall(r"\]\(<(C:/[^>]+)>\)", note)))
for link in review_links:
    check("review_link_exists:" + Path(link).name, Path(link).is_file(), link)
if not all(item["passed"] for item in checks):
    publish_json(OUT / "FALHA_LINKS_PARECER_087.json", {"checks": checks})
    raise RuntimeError("Review link error")
review_pin = publish(OUT / "PARECER_GERACAO_CURVA_RELATIVO_E_CE_087.md", note.encode("utf-8"))
after = {}
for path in paths:
    measured, _ = read_pin(path)
    after[measured["path"]] = measured
    old = before[measured["path"]]
    check("input_preserved:" + Path(path).name,
          old["bytes"] == measured["bytes"] and old["sha256"] == measured["sha256"] and
          old["mtime_ns"] == measured["mtime_ns"])
check("review_bytes_roundtrip",
      (OUT / Path(review_pin["path"]).name).read_bytes() == note.encode("utf-8"))
passed = all(item["passed"] for item in checks)
record = {
    "status": "PASS_DOCUMENTARY_AND_INDEPENDENT_WRITTEN_REVIEW_NO_MATERIAL_ERROR" if passed else "FAIL_DOCUMENTARY",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "reviewer": "/root/prepare_integration_83",
    "review_note": review_pin,
    "scope": "Full independent review of proposed curved scalar/form generation, quadratic relative complex, triangular wave-operator quotient, and isotropy-invariant CE ranks; not full BRST or quantum anomaly.",
    "sources_before": list(before.values()), "sources_after": list(after.values()),
    "checks": checks,
    "documentary_checks_total": len(checks),
    "documentary_checks_passed": sum(item["passed"] for item in checks),
    "failed_checks": [item for item in checks if not item["passed"]],
    "files_preserved": len(before) if passed else None,
    "primary_source_read": {"url": "https://arxiv.org/pdf/hep-th/9505173v2",
                            "scope": "AppendixB B.1-B.3 and Lorentz primitive Lie algebra cocycles only; no top-degree characteristic theorem."},
    "own_antecedent_authorship_disclosed": ["Reduction081", "CE082", "OneDerivative086"],
    "new_mathematical_executions": 0, "new_cas_executions": 0, "new_lean_compilations": 0,
    "um_executed_or_imported": False, "historical_helpers_executed": False,
    "originals_written": False, "existing_files_modified": False,
    "canonical_reopened": False,
    "external_approval_claimed": False,
}
record_pin = publish_json(OUT / "REGISTRO_REVISAO_RELATIVO_CE_087.json", record)
print(json.dumps({"status": record["status"], "review": review_pin, "receipt": record_pin,
                  "checks": [record["documentary_checks_passed"], record["documentary_checks_total"]],
                  "preserved": record["files_preserved"], "failed": record["failed_checks"]},
                 ensure_ascii=False, indent=2))
if not passed:
    raise RuntimeError("Preservation failure recorded")

