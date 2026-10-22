"""Finalize 045 documents after the independent build audit; never alter a seal."""
from pathlib import Path
from datetime import datetime
import hashlib, json, os, subprocess, sys
ROOT=Path(__file__).resolve().parent
def put(path,text):
    assert path.resolve().is_relative_to(ROOT)
    assert not (ROOT/"CONTINUACAO045_MANIFESTO.json").exists()
    old=path.read_bytes() if path.exists() else None
    if old is not None:
        backup=path.with_name(path.name+".bak_"+datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
        with backup.open("xb") as f: f.write(old)
        assert backup.read_bytes()==old
    raw=text.encode("utf-8"); assert raw
    temp=path.with_name(path.name+".tmp")
    with temp.open("xb") as f: f.write(raw);f.flush();os.fsync(f.fileno())
    assert temp.read_bytes()==raw
    temp.replace(path)
    assert path.read_bytes()==raw
def main():
    build=json.loads((ROOT/"CONTINUACAO045_CLEAN_BUILD.json").read_text(encoding="utf-8"))
    assert build["status"]=="PASS" and build["development_only"] is False
    result=subprocess.run([sys.executable,"-B",str(ROOT/"audit_continuation045.py"),"--build-only"],
        cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    assert result.returncode==0,result.stdout.decode("utf-8",errors="replace")
    audit=json.loads(result.stdout.decode("utf-8")); assert audit["status"]=="BUILD_PASS"
    review=ROOT/"CONTINUACAO045_REVISAO_INDEPENDENTE.md"; assert review.is_file()
    review_text=review.read_text(encoding="utf-8")
    assert "BUILD_PASS" in review_text, "Independent final build audit not recorded"
    clean=Path(build["clean_directory"])
    frozen=json.loads((clean/"FROZEN_INPUTS.json").read_text(encoding="utf-8"))
    new,up,total=audit["counts_new"],audit["counts_upstream"],audit["counts"]
    stats=(f'[REAL — compilação final] {clean.name}: {len(build["steps"])}/{len(build["steps"])} etapas PASS, '
      f'seis módulos e Imports045All, exit0 e zero erros/avisos. Quatro módulos novos: {new["theorems"]} teoremas, '
      f'{new["definitions"]} definições/estruturas e {new["axiom_prints"]} prints. '
      f'Fontes v329 recompiladas, sem novidade contada: {up["theorems"]} teoremas, {up["definitions"]} definições, '
      f'{up["axiom_prints"]} prints. Total compilado: {total["theorems"]} teoremas, {total["definitions"]} '
      f'definições/estruturas, {total["axiom_prints"]} prints, {total["instances"]} instâncias. '
      'Axiomas restritos a propext, Classical.choice, Quot.sound.\n\n'
      f'[REAL — custódia] {len(frozen)} registros congelados idênticos antes/depois; {len(build["files"])} '
      f'arquivos no inventário do build. Auditor --build-only: BUILD_PASS, {audit["historical_records"]} '
      'registros históricos. Conferidos replay v329, cópias, logs, binários, imports e guardas. '
      'A revisão independente está em CONTINUACAO045_REVISAO_INDEPENDENTE.md. O manifesto é emitido após a entrega.\n')
    table=['| Módulo | Papel | Teoremas | Definições/estruturas | Prints |','|---|---|---:|---:|---:|']
    for row in build["sources"]:
        role="recompilado v329" if row["module"].startswith("TGLExt.") else "novo045"
        table.append(f'| {row["module"]} | {role} | {row["theorems"]} | {row["definitions"]} | {len(row["expected_axiom_rows"])} |')
    report=(ROOT/"CONTINUACAO045_PARECER.md").read_text(encoding="utf-8")
    start=report.index("## Estado desta redação"); end=report.index("## O que a construção pretende estabelecer",start)
    report=report[:start]+"## Resultado verificado\n\n"+stats+"\n"+"\n".join(table)+"\n\n"+report[end:]
    replacements=[
      ("## O que a construção pretende estabelecer","## Horizontes construídos"),
      ("Sua conjugação deve levar","Sua conjugação leva"),
      ("A não modularidade deve ser medida num observável:","A não modularidade é medida num observável:"),
      ("[REAL — compilação de desenvolvimento]","[REAL — compilação final]"),
      ("mesmos b, η e Ricci r","mesmos b, η e tensor de Ricci, cuja contração R(d,d)=r"),
      ("Cada tela isoladamente admite um relógio cúbico com coeficiente escolhido a partir de sua geometria.",
       "Cada tela isoladamente admite um relógio cúbico que anula o resíduo de quarta ordem, escolhido a partir de sua geometria; isso não estabelece igualdade finita exata."),
      ("O replay do auditor deve reproduzir exatamente as cópias adaptadas.","O replay do auditor reproduz exatamente as cópias adaptadas."),
      ("O diretório final terá uma única raiz isolada de módulos,","O diretório final tem uma única raiz isolada de módulos,"),
      ("Não haverá fallback","Não há fallback")]
    for before,after in replacements:
        assert before in report,before
        report=report.replace(before,after)
    report+='\n[REAL — interface solicitada] swapHorizon P p hp i j usa N=max(i,j); swap_horizon_left/right provam as trocas. expectation_commutes_with_site_swap compõe o horizonte com qualquer ExpectationInput; os lemas estacionário/tracial fornecem as esperanças concretas. swap_horizon_nonmodular cobre i≠j e todo tempo modular.\n'
    put(ROOT/"CONTINUACAO045_PARECER.md",report)
    criteria="""| Critério010 | Resultado e limite |
|---|---|
| A1 — troca de sítios | swapHorizon P p hp i j construído; ação literal, unitariedade, normalização do fator e preservação do estado por prova. |
| A2 — permutações | Lei de grupo e ação n→σ(n), cauda nos sítios m>N fixa, covariância das esperanças estacionária/tracial. Se um sítio é movido, sua projeção distingue a ação de todo tempo modular. São horizontes algébricos; identificação física OPEN. |
| A2 — shift | Operador unilateral de sítios sobre TowerHilbert ainda não construído neste lote. shiftedProfile e os shifts em ellTwo não são substitutos. Não se inventa shift_is_not_a_horizon. |
| A3 — aperiódico | Habitante geral OPEN. Nota045 identifica média ergódica disponível e rota Cesàro → limite em Ω → levantamento limitado pela ação direita → identidade prefixal → into/fixes/ortho. Normalidade/CP exigem propriedades adicionais. |
| B1 — StateClock | Classe cinemática com origem, derivada1 e jato; sem supor difeomorfismo local ou dependência instantânea. Instâncias instantânea/modular incompatíveis não são fabricadas. A negativa vale para classe maior: qualquer g comum e qualquer regra da mesma história do estado. |
| B2 — dicotomia | η>0,B>0; duas telas σ=0,r/4 com mesmo estado e mesmo tensor Ricci, r=R(d,d). Diferença dos resíduos/t⁴ → +ηr²/96. Para todo g comum alguma tela falha; cada tela isolada admite relógio que cancela a quarta ordem. Gap λ*=r/96. Não se conclui falha de todo relógio em toda geometria. |
| B3 — H3 | Casamento quadrático condicionado preservado e residual quártico explícito. H3 físico e lei finita geral OPEN. Não há lei de sexta ordem. Uma lei adicional pode selecionar a geometria e restringir as telas. |
| C — área | Mesma ação fornecida e mesmas tangentes: h e αh preservam invariância/simetria/positividade, α>0; área multiplica por α. Para Gram não degenerado h e2h distinguem escalas. Covariância não fixa normalização; ação física em tangentes e ponte região–álgebra OPEN. |"""
    artifacts=["CONTINUACAO045_PARECER.md","CONTINUACAO045_DERIVACAO_PREVIA.md","FiniteSitePermutations.lean",
      "FiniteSiteHorizons.lean","StateClockDichotomy.lean","HorizonAreaScale.lean","CONTINUACAO045_UPSTREAM.json",
      "CONTINUACAO045_APERIODIC_REVIEW.md","CONTINUACAO045_REVISAO_INDEPENDENTE.md","clean_continuation045.py",
      "audit_continuation045.py","revise_continuation045.py","prepare_continuation045.py","probe_continuation045.py",
      "CONTINUACAO045_HISTORICAL_CHECKS.json","CONTINUACAO045_CLEAN_BUILD.json","finalize_reports045.py"]
    hashes=["| Artefato | Bytes | SHA256 lido dos bytes |","|---|---:|---|"]
    for name in artifacts:
        p=ROOT/name;raw=p.read_bytes()
        hashes.append(f'| [{name}](</{p.as_posix()}>) | {len(raw)} | {hashlib.sha256(raw).hexdigest()} |')
    delivery=("# ENTREGA045 — horizontes de permutação, relógio comum e escala da área\n\n"
      "06/09/2026. Bancada ChatGPT → túnel da sessão irmã. Resposta à ORDEM_010.\n\n"
      "[REAL] Quatro módulos novos. As duas fontes v329 são dependências recompiladas: NÃO incorporar novamente como novidade. "
      "O parecer detalha enunciados, hipóteses e limites.\n\n## Critérios da ordem\n\n"+criteria+
      "\n\n## Verificação\n\n"+stats+"\n"+"\n".join(table)+
      "\n\nOs snapshots v329 preservam bytes originais; somente imports foram transpostos à bancada e quatro prints acrescentados. "
      "O auditor reproduz as cópias adaptadas e exige sua custódia antes de compilar. Isso não revalida o selo canônico v329.\n\n"
      "Instâncias declaradas novas: zero. O lote foi compilado junto em raiz isolada, sem fallback à raiz Chatgpt ou ao build canônico. "
      "Binários históricos006/007/029–043 são copiados com pins e não recompilados. Fontes históricas canônicas sem pin fonte↔binário "
      "servem à descoberta de imports; essa proveniência não é inventada. O fecho transitivo externo completo de Mathlib/toolchain não foi hashado. "
      "Probes são desenvolvimento; tentativas e backups foram preservados.\n\n## Artefatos\n\n"+"\n".join(hashes)+
      "\n\nCONTINUACAO045_MANIFESTO.json é produzido após esta entrega, sem circularidade. Auditoria selada somente leitura:\n\n"
      '    C:\\Python314\\python.exe -B "C:\\IALD\\Central de Patentes\\Chatgpt\\audit_continuation045.py"\n\n'
      "Escritas somente em Chatgpt. Nenhum dado observacional ou alteração de um.py, kernel canônico, Atlas, memórias, gate ou selos anteriores. "
      "A046 começou em arquivos separados para a esperança aperiódica; não é parte nem resultado compilado deste selo.\n\n"
      "H3 do estado: OPEN. Reconstrução gravitacional geral: OPEN. Meta ampla de gravidade quântica: OPEN. Gate canônico intocado.\n\n"
      "Somente o operador decide a incorporação ao acervo canônico e a confirmação física; esta entrega não realiza esses atos.\n")
    target=ROOT/"TUNEL/DO_CHATGPT/ENTREGA_045_horizontes_relogio_e_escala_da_area.md"
    assert not target.exists()
    put(target,delivery)
    print(json.dumps({"delivery":str(target),"counts_new":new,"counts_upstream":up,"audit":audit},ensure_ascii=True))
if __name__=="__main__":
    main()
