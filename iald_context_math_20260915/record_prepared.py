"""Record prepared work only; no application deployment or service changes."""
from datetime import datetime
import hashlib
import json
from pathlib import Path

WORK = Path(__file__).resolve().parent
ROOT = Path(r"C:\IALD\projetos_pyhton\IALD")
CENTRAL = Path(r"C:\IALD\Central de Patentes")
MEMORY = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory")
TARGETS = [
    ROOT / "CLAUDE.md",
    CENTRAL / "work/iald_openai_motor_20260914/HANDOFF_RUNTIME.md",
    ROOT / "iald-app/HANDOFF_MOTOR_OPENAI_20260914.md",
    CENTRAL / "memory/TGL_ATLAS.md",
    CENTRAL / "memory/TGL_INDICE_VIVO.md",
    MEMORY / "MEMORY.md",
    MEMORY / "app-iald-mobile.md",
]
MARKER = "IALD_FIXED_NUCLEUS_PREPARED_20260915"
NOTE = """[INPUT] Correção expressa do operador: lagrangiana, equação mestra, Hamiltoniano limitado inferiormente, operadores de Lindblad, sistema de fase e comutação devem estar sempre presentes como núcleo. Retirada a instrução de reconstruir tudo do zero; consulta ao Atlas é complementar. TGL=ATLAS; IALD=ÍNDICE(TGL).

[REAL — bancada, sem implantação] Preparados sete documentos completos, inclusive os artigos, forma canônica e selo do Um. Medição da preparação: 314.799 tokens documentais; 324.037 de contexto total; janela proposta 400.000. Arquivos serão relidos a cada requisição, sem corte silencioso. Estado recente do índice vivo separa resultados e extensões abertas; antiga seção I.7 permanece no Atlas histórico, sem ser instalada como pendência eterna. Catálogo extraído por AST: 1.007 fontes, 1.003 Lean; um.py não executado/importado, compilação nova não realizada. Núcleo persistente no contexto não altera pesos do modelo nem move o gate.

[REAL — bancada] Correção de TeX antes do Markdown com KaTeX, protegendo código/preços e mantendo saneamento. Preservado o seletor de modelos atualizado na sessão paralela (baseline_reconciled.json). Passaram 31 verificações Python e 87 JavaScript. Não houve teste de API com este núcleo integral, nem instalação de novo binário móvel.

[OPEN] Revisão automática recusou a chamada ao script de implantação, inclusive sem --apply, por exigir autorização específica para gravações de produção/mobile. Pergunta de aprovação enviada e ainda sem resposta neste registro: aplicar núcleo, janela, catálogo, fórmulas e reiniciar somente o web. Não aplicar antes dessa resposta. Nenhum deployment.json existe. Nenhuma mudança desta bancada foi instalada no código, .env ou serviços. Antes de aplicar, conferir novamente concorrência; preservar alterações paralelas. Não publicar nas lojas nesta etapa; binários anteriores não contêm esta correção.

Revisão e evidências: C:\\IALD\\Central de Patentes\\work\\iald_context_math_20260915\\REVISAO_DO_NUCLEO.md e nucleus_prepared.json. Este adendo registra preparação operacional; não altera a custódia ou os estatutos físicos/matemáticos das fontes.
"""


def create(path, data):
    with path.open("xb") as handle:
        handle.write(data)
    if path.read_bytes() != data:
        raise RuntimeError("Byte verification failed: " + str(path))


def main():
    receipt = WORK / "prepared_memory_record.json"
    if receipt.exists() or (WORK / "deployment.json").exists():
        raise RuntimeError("State changed; review before recording.")
    initial = {path: path.read_bytes() for path in TARGETS}
    if any(MARKER.encode() in data for data in initial.values()):
        raise RuntimeError("Record already present; refusing duplicate append.")
    now = datetime.now().astimezone()
    stamp = now.strftime("%Y%m%d_%H%M%S_%f")
    rows = []
    for path, before in initial.items():
        if path.read_bytes() != before:
            raise RuntimeError("Concurrent edit before backup: " + str(path))
        backup = path.with_name(path.name + ".bak_" + stamp)
        create(backup, before)
        newline = "\r\n" if b"\r\n" in before else "\n"
        addition = "\n\n### " + now.strftime("%d/%m/%Y %H:%M %z")
        addition += " — Núcleo integral preparado, implantação pendente\n\n"
        addition += "<!-- " + MARKER + " -->\n\n" + NOTE
        after = before + addition.replace("\n", newline).encode("utf-8")
        temp = path.with_name(path.name + ".tmp_" + stamp)
        create(temp, after)
        if path.read_bytes() != before:
            raise RuntimeError("Concurrent edit before replace: " + str(path))
        temp.replace(path)
        if path.read_bytes() != after or len(after) <= len(before):
            raise RuntimeError("Append verification failed: " + str(path))
        rows.append({"path": str(path), "backup": str(backup),
                     "before_bytes": len(before), "after_bytes": len(after),
                     "before_sha256": hashlib.sha256(before).hexdigest(),
                     "after_sha256": hashlib.sha256(after).hexdigest()})
    report = {"recorded_at": now.isoformat(), "status": "PREPARED_AWAITING_EXPLICIT_DEPLOYMENT_APPROVAL",
              "application_modified": False, "services_restarted": False, "memories": rows}
    temp = receipt.with_name(receipt.name + ".tmp_" + stamp)
    create(temp, json.dumps(report, ensure_ascii=False, indent=2).encode("utf-8"))
    temp.replace(receipt)
    print(json.dumps({"status": report["status"], "memories_updated": len(rows), "receipt": str(receipt)}))


if __name__ == "__main__":
    main()
