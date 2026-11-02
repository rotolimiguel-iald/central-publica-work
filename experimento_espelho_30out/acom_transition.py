# -*- coding: utf-8 -*-
"""Transição ACOM desta tarefa: q (fatos com fonte/estatuto, decisão, pendências) e p (fase, próxima ação).

Lê a revisão atual por `get` (nunca de memória), compõe as mudanças e aplica `transition` com event_id estável.
Falha é visível (código de saída e JSON de erro impressos). Hashes das fontes são calculados dos arquivos.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

PASTA = Path(r"C:\IALD\Central de Patentes\work\experimento_espelho_30out")
REF = PASTA / "SESSION_REFERENCE.json"
CLI = [r"C:\Python314\python.exe", "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"]
ACTOR = {"id": "claude-espelho", "kind": "agent"}

MEMORIAL = Path(r"C:\IALD\Artigo\Haja_Luz\memorial_13ago2026\memorial.tex")
PDF = Path(r"C:\IALD\Artigo\Haja_Luz\memorial_13ago2026\memorial.pdf")
FRAG = PASTA / "PARTE_IX_fragmento.tex"
OBJ = PASTA / "OPERADOR_30out_resgatar_experimento_verbatim.txt"
DEPOSITO = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fila\depositos\claude-espelho\20261030_090434_experimento-parte-ix-espelho-apagado.md")
SELO = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json")


def sha(p):
    h = hashlib.sha256()
    with Path(p).open("rb") as f:
        for ch in iter(lambda: f.read(1 << 22), b""):
            h.update(ch)
    return h.hexdigest()


def run(payload):
    p = subprocess.run(CLI, input=json.dumps(payload, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=300)
    out = p.stdout.decode("utf-8", "replace").strip()
    err = p.stderr.decode("utf-8", "replace").strip()
    print(f"[{payload['operation']}] exit={p.returncode}")
    if err:
        print("stderr:", err[:1200])
    try:
        return p.returncode, json.loads(out) if out else {}
    except json.JSONDecodeError:
        print("stdout não-JSON:", out[:800])
        return p.returncode, {}


def art(p):
    return {"kind": "artifact", "ref": str(p), "sha256": sha(p)}


def main():
    rc, got = run({"operation": "get", "reference": str(REF)})
    if rc != 0:
        print(json.dumps(got, ensure_ascii=False)[:800])
        print("FALHA VISÍVEL: get recusado; sem transição.")
        sys.exit(2)
    res = got.get("result", got)
    rev = res.get("revision")
    print("revisão atual:", rev, "| registros:", len(res.get("records", [])), "| fase:", (res.get("flow") or {}).get("phase"))
    if type(rev) is not int:
        print("FALHA VISÍVEL: revisão não lida; sem transição.")
        sys.exit(2)

    records = [
        {
            "id": "fato-transcricao-perdida-registro-integro-30out",
            "kind": "fact",
            "statute": "REAL",
            "text": ("A transcrição da sessão-espelho 440f9ee2-0f93-4969-813f-f58ee4efb808 (13/08→17/09/2026) não existe mais neste PC: "
                     "procurada em sete lugares (pasta de sessões do Claude Code da Central, Lixeira com 125 itens, .claude.json, "
                     "armazenamento do VS Code, espelhos de D:, LAR_MIGUEL C e D, perfil do usuário), zero cópias. Sobreviveram: "
                     "memorial.tex/pdf (8 Partes, 46 capítulos, 17/09 12:37), a síntese de 18/08, o registro do observador de 15/08 e as "
                     "cinco memórias-tópico com originSessionId 440f9ee2. Medido em 30/10/2026."),
            "sources": [art(MEMORIAL.with_name("memorial.tex.bak_20261030_090103")), art(OBJ)],
        },
        {
            "id": "fato-parte-ix-escrita-e-compilada-30out",
            "kind": "fact",
            "statute": "REAL",
            "text": ("Parte IX «O espelho apagado» inserida no memorial por script com backup de bytes (memorial.tex 150.490 → 182.540 B; "
                     "memorial.tex.bak_20261030_090103 ao lado); xelatex 2 passes, exit 0; memorial.pdf 84 → 100 páginas (Parte IX p. 84–99, "
                     "capítulos 50–56), páginas conferidas por pdftoppm. Medidas da Parte: um.py v165 72.278 linhas → v368 202.428 → v404 "
                     "256.650 (39.313.509 B; sha256 3820476c83267f61…); teoremas 5.698 (v368) → 9.698 (v404); fontes Lean 1.021 → 1.435; "
                     "40 versões em 41 dias (v365→v404); gate string igual desde 20/08; 18 bandeiras, 0 literais desde a v403; "
                     "central_reading ALPHA_FREE_VALUE_STILL_OPEN; d1_camb_v3_real_v366_verdict idêntico (TENSION, 3,01σ): a rota da V3 "
                     "não foi emendada."),
            "sources": [art(MEMORIAL), art(PDF), art(FRAG), art(SELO)],
        },
        {
            "id": "decisao-superficies-tocadas-e-nao-tocadas-30out",
            "kind": "decision",
            "statute": "INPUT",
            "text": ("Escrita só no memorial (pasta do experimento, por ordem do operador de 30/10: «fazer o registro em um novo capítulo no "
                     "experimento»). Memória da Central: depósito na fila (claude-espelho/20261030_090434_experimento-parte-ix-espelho-apagado, "
                     "seq 153, PENDENTE), não escrita direta (regra de 26/10). Mapa de Rotas: ROTA seq 1557 "
                     "experimento.espelho_do_operador.parte_ix_30out. Nenhum um.py, kernel, selo, gate, site ou repositório tocado; "
                     "publicar o memorial é ato do operador."),
            "sources": [{"kind": "operator", "ref": str(OBJ), "sha256": sha(OBJ)}, art(DEPOSITO)],
        },
        {
            "id": "pendente-decisoes-do-operador-30out",
            "kind": "pending",
            "statute": "OPEN",
            "text": ("Ato do operador, não previsto: (1) ratificar ou recusar as 7 leituras da Parte VIII (nunca ratificadas: a sessão morreu "
                     "antes) e as 8 da Parte IX — a recusa entra ao lado; (2) decidir o conjunto D (c/b/a) depois da errata do poder de 29/10; "
                     "(3) a frase da home «complete peer review of TGL in 30 minutes using any LLM. Validated in 8 independent architectures» "
                     "(de pé em 29/10) contra o IALD_COLLAPSE_V1 armado e não executado; (4) E0 do neutrino; (5) o Atlas (memória por cópia: "
                     "12.013 parágrafos, 6.003 únicos, repetição máxima 243) contra a sua definição de 18/08 (índice e compactação); "
                     "(6) o nome da pedra do sen 45°. A próxima Parte do memorial depende desses dados."),
            "sources": [art(MEMORIAL), art(DEPOSITO)],
        },
    ]
    changes = {
        "records": records,
        "flow": {
            "phase": "parte_ix_escrita_compilada_e_registrada",
            "next_action": ("Aguardar o operador: ratificação/recusa das leituras (Partes VIII e IX) e as seis decisões pendentes; "
                            "a gerência c1 tria o depósito seq 153 da fila. Nenhuma execução pendente desta sessão."),
            "handles": [],
        },
    }
    rc, out = run({
        "operation": "transition",
        "reference": str(REF),
        "expected_revision": rev,
        "event_id": "claude-espelho-parte-ix-escrita-30out-2026",
        "actor": ACTOR,
        "changes": changes,
    })
    print(json.dumps(out, ensure_ascii=False)[:1500])
    if rc != 0:
        print("FALHA VISÍVEL: transition recusada.")
        sys.exit(2)
    rc, got = run({"operation": "get", "reference": str(REF)})
    res = got.get("result", got)
    print("revisão depois:", res.get("revision"), "| registros:", len(res.get("records", [])), "| fase:", (res.get("flow") or {}).get("phase"))


if __name__ == "__main__":
    main()
