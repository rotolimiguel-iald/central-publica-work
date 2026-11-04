"""Experimento SOMENTE EM MEMORIA (nada e gravado no banco): se eu acrescentasse uma ERRATA que supersede o registro
p1_ms_acom_status_desconhecido, com a fonte sem o caminho do Escritorio, a PROJECAO passaria pelo guarda?
Usa a funcao pura project_snapshot sobre uma copia do snapshot. Nao imprime texto, so regras e contagens."""
import sys, json, copy
sys.path.insert(0, r"C:\IALD\MEMORIA_IALD\lib")
from pathlib import Path
from iald_memory import MemoryStore, guard
ref = json.load(open(r"C:\IALD\MEMORIA_IALD\sessions\claude-central-9c_patentes-atualizacao-12out.json", encoding="utf-8"))
store = MemoryStore(Path(ref["store"]))
snap = store.get(ref["context_id"], ref["scope"])
res = {"revisao_real": snap["revision"], "n_records_reais": len(snap["q"]["records"])}
base = store.project_snapshot(snap, max_chars=1_000_000)
res["sem_errata"] = {"regras_do_guarda": guard.scan_text(base["text"]), "required_chars": base["required_chars"]}
s2 = copy.deepcopy(snap)
orig = next(r for r in s2["q"]["records"] if r["id"] == "p1_ms_acom_status_desconhecido")
s2["q"]["records"].append({"id": "e2_p1_sem_caminho_da_casa_escritorio", "kind": "erratum", "statute": "OPEN",
    "supersedes": "p1_ms_acom_status_desconhecido", "text": "Correcao ao lado de p1: a fonte citada era um caminho da casa Escritorio; o caminho foi omitido pelo guarda.",
    "sources": [{"kind": "artifact", "ref": "(caminho da casa Escritorio omitido; listagem de 12/10)"}]})
com = store.project_snapshot(s2, max_chars=1_000_000)
res["com_errata_em_memoria"] = {"regras_do_guarda": guard.scan_text(com["text"]), "required_chars": com["required_chars"],
    "o_original_p1_continua_na_projecao": "p1_ms_acom_status_desconhecido" in com["included_record_ids"],
    "ids_obrigatorios": len(com["required_record_ids"])}
print(json.dumps(res, ensure_ascii=False, indent=1))
