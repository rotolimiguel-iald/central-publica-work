"""Static preparation checks only; does not build, preview, install or publish."""
import ast
from prepare_mobile import HERE, PREVIOUS, inventory, read, require, report, sha

def main():
    baseline = read(HERE/'BASELINE.json')
    require(inventory()==baseline, 'Checkout changed since inventory')
    scripts = sorted(HERE.glob('*.py'))
    for path in scripts:
        ast.parse(path.read_text(encoding='utf8'), filename=str(path))
    build = (HERE/'build_android42.py').read_text(encoding='utf8')
    require('build41' not in build and 'android41.init.gradle' not in build and
            'versionCode=41' not in build and '4.1(41)' not in build, 'Obsolete build constants')
    init = (HERE/'android42.init.gradle').read_text(encoding='utf8')
    require('app_scroll_20261106/mobile/release' in init and 'versionCode != 42' in init,
            'Wrong output/version guard')
    require(not (HERE/'prepared').exists() and not (HERE/'release').exists(), 'Unexpected execution/staging')
    require(not (HERE/'PLAN.json').exists(), 'Parent-stage plan already exists; use later verification')
    provenance = read(HERE/'PROVENANCE.json')
    for item in provenance['sources'].values():
        from pathlib import Path
        require(sha(Path(item['path']).read_bytes())==item['sha256'], 'Prior pipeline source drift')
    outputs = {p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir())
               if p.is_file() and p.name!='PREPARATION_CHECK.json'}
    report(HERE/'PREPARATION_CHECK.json', dict(
        status='PASS_STATIC_PREPARATION_ONLY', independent_review='PENDING_PARENT_DISTINCT_REVIEW',
        python_files_parsed=len(scripts), baseline_unchanged=True,
        stage_copied=False,build_executed=False,checkout_written=False,pushed=False,
        apple_accessed=False,output_pins=outputs,
        limits=['No functional scroll test here','No Gradle execution','No release availability verification']))

if __name__=='__main__':
    main()
