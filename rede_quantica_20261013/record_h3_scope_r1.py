"""Read the existing H3 proofs and record their exact scope, without rebuilding."""
import ast
import datetime as dt
import json
from pathlib import Path
import sys
from diary_r1 import ROOT, new, pin

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
KERNEL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
RITE = ROOT/'work/rite394_20261015/r3'
sys.path.insert(0,str(OUT/'full_rite'))
from qualified_index_v394_r2 import parse_lean_axioms_v394


def main():
    target = OUT/'R9_H3_SCOPE_R1.json'
    assert not target.exists()
    audit_log = RITE/'tgl_kernel_audit_capture.txt'
    parsed = parse_lean_axioms_v394(audit_log.read_text(encoding='utf-8'))
    assert parsed['ok']
    tree = ast.parse((RITE/'um_v394_final.py').read_bytes())
    embedded = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign)
        and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='_EMBEDDED_KERNEL_FILES')
    provenance_path = OUT/'full_rite/declaration_sources_r3/DECLARATION_SOURCES.json'
    provenance = json.loads(provenance_path.read_bytes())
    records = []
    entries = [
        ('TGLExt/TheImportedSecondQuantization.lean','def lightH2','TGLExt.ImportedSQ.lightH2',
         'REAL_CONSTRUCTOR_WITH_NAMED_INPUTS',
         'H2 uses the same Fock certificate and clock N. Its kappa is 1/refRadius(N); the modular/Unruh normalization is constructed within that chosen clock.'),
        ('TGLExt/TheImportedSecondQuantization.lean','def lightH3 (','TGLExt.ImportedSQ.lightH3',
         'REAL_CONSTRUCTOR_WITH_NAMED_INPUTS',
         'For the named MaxwellCertificate, regular state domain, G>0 and clock N, the null-solution constructor supplies H3 on the same standard horizon. This is already a term, not a missing implication. It consumes charge_link and a nonzero modular-energy regular state, and does not construct these Maxwell inputs.'),
        ('TGLExt/LiganteLeiCampoCurvo.lean','def NamedAtlasH3','ChatgptAudit.F23CurvedFieldLigand.NamedAtlasH3',
         'REAL_DEFINITION_NOT_AN_INHABITANT',
         'Quantifies every point and nonzero null direction of every chart. It requires the specified microscopic area error divided by t^2 to tend to zero; a name alone supplies no such limit.'),
        ('TGLExt/LiganteLeiCampoCurvo.lean','theorem passage_h3_to_connected_smooth_atlas_einstein','ChatgptAudit.F23CurvedFieldLigand.passage_h3_to_connected_smooth_atlas_einstein',
         'REAL_CONDITIONAL_IMPLICATION',
         'NamedAtlasH3 plus conserved source and smooth compatible connected atlas imply a unique cosmological coefficient and Einstein equation with 8*pi*G. The finite passage identity is already proved; the arrow from it to H3 is an explicit input and contributes no independent physical derivation of H3. No metric, global solution or Maxwell-to-recordSource identification is constructed.'),
        ('TGLExt/HorizonEinsteinReconstruction.lean','theorem horizon_einstein_reconstruction','ChatgptAudit.horizon_einstein_reconstruction',
         'REAL_CONDITIONAL_IMPLICATION',
         'Requires a symmetric conserved differentiable tensor and a LocalHorizonPencil at every point and null vector. Those inputs yield the geometric field equation; a single chosen null direction cannot discharge the universal pencils input.'),
        ('TGLExt/StateClockDichotomy.lean','theorem state_clock_dichotomy','ChatgptAudit.Clock045.state_clock_dichotomy',
         'REAL_TYPED_OBSTRUCTION_WITH_SPECIFIED_SCOPE',
         'For the defined positive-mass amplitude family and eta>0, every state-only common clock fails fourth-order matching on at least one of two screens with different tidal anisotropy. This theorem does not assert failure for every screen, does not forbid adding geometric data, and must not be promoted to a universal impossibility of second-order Clausius.')]
    for rel,anchor,name,status,scope in entries:
        path = KERNEL/rel; raw = path.read_bytes(); body = raw.decode('utf-8')
        assert body.replace('\r\n','\n') == embedded[rel].replace('\r\n','\n')
        assert provenance[name] == rel and name in parsed['axioms']
        assert set(parsed['axioms'][name]) <= {'propext','Classical.choice','Quot.sound'}
        lines = body.splitlines()
        positions = [i+1 for i,line in enumerate(lines) if anchor in line]
        assert len(positions)==1,(name,positions)
        records.append(dict(declaration=name,source=pin(path),line=positions[0],status=status,
            axioms=parsed['axioms'][name],scope=scope,canonical_body_matches_executed_candidate=True))
    result = dict(unit='F1.FECHO_20261015',requirement='R9',claim=845,
        created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        status='SCOPE_CLASSIFIED_FROM_EXISTING_PROOFS',records=records,
        evidence=[pin(audit_log),pin(provenance_path),pin(RITE/'RITE_RECEIPT.json')],
        distinction={'already_term':'H2 and H3 constructors under the named certificates, and the all-direction Clausius-to-Einstein implication.',
            'not_supplied':'A joint Maxwell certificate on the complete net, its physical source identification on all curved charts, or an inhabitant of all-direction geometric H3 for that system.',
            'literature_status':'The physical identification with Jacobson is KNOWN in the house literature; this record does not claim a new derivation or independent literature check.',
            'completion_scope':'The classification required by R9 is exhibited; this is not completion of the independent R5/R7/R8 constructions.'},
        independent_review_pending=True,production_modified=False,gate_moved=False,script=pin(__file__))
    new(target,result)
    print(json.dumps(dict(result=pin(target),declarations=len(records)),ensure_ascii=False))


if __name__=='__main__':
    main()
