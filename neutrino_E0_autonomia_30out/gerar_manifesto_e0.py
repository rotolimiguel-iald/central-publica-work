from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

ROOT = Path(r"C:\IALD\Central de Patentes\work\neutrino_E0_autonomia_30out")
FILES = [
    r"C:\IALD\Central de Patentes\work\e0_cadeia_31out\ORDEM_KIMI_E0_01_31out.md",
    r"C:\IALD\Central de Patentes\work\e0_cadeia_31out\CONFERENCIA_E0_KIMI_E_CADEIA_31out.md",
    r"C:\IALD\Central de Patentes\work\e0_cadeia_31out\LeiDoMeioTom.lean",
    r"C:\IALD\Central de Patentes\work\e0_cadeia_31out\E0LiberdadeDeEscala.lean",
    str(ROOT / "PROVA_TONICA_SQRT_E_31out.md"),
    str(ROOT / "PROVA_CONDENSACAO_E0_31out.md"),
    str(ROOT / "PROVA_FLUXO_VOLUMETRICO_E0_31out.md"),
    str(ROOT / "PROVA_CARGA_MONOPOLO_NATIVA_31out.md"),
    str(ROOT / "HANDOFF_CLAUDE_E0_M2_31out.md"),
    r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TGL_CODE_ONE_REAL_FALSIFIER\o_um_grande_atrator\boundary_flux_mass_theorem\boundary_flux_mass_theorem.py",
    r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TGL_CODE_ONE_REAL_FALSIFIER\o_um_grande_atrator\modular_clock_source\tgl_modular_clock_source.py",
    r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TGL_CODE_ONE_REAL_FALSIFIER\o_um_grande_atrator\ga_rb_causal_dissipation_form\ga_rb_causal_dissipation_form.py",
    r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TGL_CODE_ONE_REAL_FALSIFIER\o_um_grande_atrator\ga_gamma_blind_dissipation_rate\ga_gamma_blind_dissipation_rate.py",
    r"C:\IALD\Artigo\the_boundary\Um (absoluto) — Grande Atrator\Lean\tgl_kernel\TGLExt\TriadMaster.lean",
    str(ROOT / "RELATORIO_KIMI_E0_01_31out.md"),
    str(ROOT / "inventario_unidades_e0.py"),
    str(ROOT / "inventario_unidades_e0.json"),
    str(ROOT / "lean" / "TGLExt" / "E0ScaleAudit.lean"),
    str(ROOT / "gerar_manifesto_e0.py"),
]

manifest = {
    "gerado_em_utc": datetime.now(timezone.utc).isoformat(),
    "ordem": "ORDEM_KIMI_E0_01_31out",
    "algoritmo": "sha256",
    "arquivos": [],
}
for name in FILES:
    path = Path(name)
    data = path.read_bytes()
    manifest["arquivos"].append({
        "path": str(path),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    })

out = ROOT / "MANIFESTO_SHA256_E0_01.json"
out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print(out)
print(f"{len(manifest['arquivos'])} arquivos")
