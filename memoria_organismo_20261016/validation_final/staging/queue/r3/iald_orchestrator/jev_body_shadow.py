"""Observational queue signal: never changes the chosen executor or authority."""
import json
import re
from pathlib import Path
from .profiles import BASE
from .safe_files import save_json, utc_now
from . import nos_packet, jev_decisions, operational_memory as opmem

POLICY=BASE/"jev_body_policy.json"
QUESTIONS=BASE/"jev_questions_v1.json"

def status():
    if not POLICY.is_file(): return {"phase":"DISABLED","effects":"NONE"}
    p=json.loads(POLICY.read_bytes())
    return {"phase":p.get("phase"),"queue_shadow_enabled":p.get("queue_shadow_enabled",False),
            "max_packet_chars":p.get("max_packet_chars"),"daily_call_limit":p.get("daily_call_limit"),
            "calibration":p.get("calibration_report"),"proposed_minimum":p.get("shadow_minimum_proposed"),
            "manager_accepted":p.get("shadow_minimum_manager_accepted",False),"effects":"NONE",
            "active_promotion":"NOT_IMPLEMENTED_REQUIRES_MANAGER_REVIEW"}

def observe(task_id,prompt,constraints,selected,*,result=None, operational_projection=None):
    """Called only for a concrete already-admitted scientific board unit."""
    phase="after" if result is not None else "before"
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,100}",task_id):
        raise ValueError("Invalid task identity")
    path=BASE/"state/jev_body_shadow"/(task_id+"_"+phase+".json")
    identity=jev_decisions.digest({"task_id":task_id,"phase":phase,"prompt":prompt,"constraints":constraints,"result":result,"operational_projection":operational_projection})
    if path.is_file():
        prior=json.loads(path.read_bytes())
        if prior.get("logical_identity")!=identity:
            return {"status":"existing_identity_mismatch","effects":"NONE"}
        return prior
    try:
        if not constraints or not nos_packet.board_unit(constraints.get("branch_id","")):
            return {"status":"not_called_without_board_unit","effects":"NONE"}
        policy=json.loads(POLICY.read_bytes())
        if policy.get("phase")!="SHADOW" or not policy.get("queue_shadow_enabled"):
            return {"status":"not_called_phase_"+str(policy.get("phase")),"effects":"NONE"}
        if policy.get("shadow_minimum_manager_accepted") is not True:
            return {"status":"awaiting_manager_acceptance","effects":"NONE"}
        report_path=Path(policy["calibration_report"])
        report_bytes=report_path.read_bytes()
        if jev_decisions.hashlib.sha256(report_bytes).hexdigest()!=policy["calibration_report_sha256"]:
            raise ValueError("Calibration report changed")
        measured=json.loads(report_bytes)
        if not measured.get("complete") or measured.get("observed_cases",0)<40:
            raise ValueError("Forty measured calibration cases required")
        doc=json.loads(QUESTIONS.read_bytes())
        axes=("D5","D6","D8") if result is not None else ("D1","D2","D3","D4","D7")
        qs={k:doc["questions"][k] for k in axes}
        operational=opmem.typed_projection(operational_projection)
        nos_packet.safe_text(json.dumps(operational,ensure_ascii=False))
        evidence={"task_id":task_id,"stage":phase,"request":prompt,"selected_by_existing_policy":selected,
                  "required_provider":constraints["required_provider"],"scope":"consultative only"}
        if result is not None:
            evidence["executor_text"]=result.get("text","")
            evidence["verification"]=result.get("verification")
        task=json.dumps(evidence,ensure_ascii=False)
        budget=policy["max_packet_chars"]-len(task)-len(json.dumps(qs,ensure_ascii=False))-len(json.dumps(operational,ensure_ascii=False))-2048
        if budget<5000:
            raise ValueError("Shadow case does not fit measured budget; no truncation")
        packet=nos_packet.build(constraints["branch_id"],min(72000,budget),allowed_sources=constraints.get("allowed_sources"))
        packet["receipt"]["mode"]="shadow"
        save_json(path,{"task_id":task_id,"stage":phase,"logical_identity":identity,"at":utc_now(),
                        "status":"dispatching","packet_sha256":packet["receipt"]["packet_sha256"],"effects":"NONE"})
        response,receipt=jev_decisions.ask(task,qs,packet,operational_projection=operational_projection)
        outcome={"status":"observed","decision_id":receipt["id"],"answers":response["answers"],
                 "mode":"SHADOW","effects":"NONE","authority_granted":False}
    except Exception as exc:
        outcome={"status":"not_observed","reason_type":type(exc).__name__,"effects":"NONE","authority_granted":False}
    save_json(path,{"task_id":task_id,"stage":phase,"logical_identity":identity,"at":utc_now(),**outcome})
    return outcome
