from pathlib import Path
from transaction import atomic,write_evidence,digest
W=Path(__file__).resolve().parent
R=Path('C:/IALD/projetos_pyhton/IALD/iald-app')
source=R/'ios/App/ci_scripts/ci_post_clone.sh'
raw=source.read_bytes()
rows={line.split()[1]:line.split()[0] for line in (W/'mobile/SHASUMS256-node-v24.21.0.txt').read_text().splitlines()}
arm=rows['node-v24.21.0-darwin-arm64.tar.gz'];x64=rows['node-v24.21.0-darwin-x64.tar.gz']
text='''#!/bin/sh
set -eu
cd "${CI_PRIMARY_REPOSITORY_PATH:-$(cd "$(dirname "$0")/../../.." && pwd)}"

# Use the official pinned Node distribution. Homebrew's shared OpenSSL lock
# failed before npm ci on Xcode Cloud builds 30 and 31.
IALD_NODE_VERSION=24.21.0
case "$(uname -s)/$(uname -m)" in
  Darwin/arm64) IALD_NODE_ARCH=arm64; IALD_NODE_SHA=ARM_HASH ;;
  Darwin/x86_64) IALD_NODE_ARCH=x64; IALD_NODE_SHA=X64_HASH ;;
  *) echo "Unsupported Xcode Cloud platform" >&2; exit 1 ;;
esac
IALD_NODE_BUNDLE="node-v${IALD_NODE_VERSION}-darwin-${IALD_NODE_ARCH}"
IALD_NODE_DIR=$(mktemp -d "${TMPDIR:-/tmp}/iald-node.XXXXXX")
curl --fail --show-error --location --retry 3 --proto '=https' --tlsv1.2 \
  "https://nodejs.org/dist/v${IALD_NODE_VERSION}/${IALD_NODE_BUNDLE}.tar.gz" \
  --output "${IALD_NODE_DIR}/${IALD_NODE_BUNDLE}.tar.gz"
printf '%s  %s\\n' "$IALD_NODE_SHA" "${IALD_NODE_DIR}/${IALD_NODE_BUNDLE}.tar.gz" | shasum -a 256 -c -
tar -xzf "${IALD_NODE_DIR}/${IALD_NODE_BUNDLE}.tar.gz" -C "$IALD_NODE_DIR"
export PATH="${IALD_NODE_DIR}/${IALD_NODE_BUNDLE}/bin:$PATH"
test "$(node --version)" = "v${IALD_NODE_VERSION}"
node --version
npm ci --no-audit --no-fund
npm run sync:ios

# Xcode Cloud requires the committed Swift dependency lock when archiving.
test -s ios/App/App.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/Package.resolved
'''.replace('ARM_HASH',arm).replace('X64_HASH',x64)
assert 'brew install' not in text and len(arm)==len(x64)==64
candidate=W/'mobile/ci_post_clone.sh'
atomic(candidate,text.encode())
write_evidence(W/'mobile/ci_fix_plan.json',{'source':str(candidate),'destination':str(source),'baseline_sha256':digest(raw),'sha256':digest(candidate.read_bytes()),'git_destination':'rotolimiguel-iald/iald-app','branch':'codex/mobile-release','client_features_changed':False,'reason':'Homebrew OpenSSL lock prevents dependency installation on Xcode Cloud','checksums_source':str(W/'mobile/node_source.json')})
print('MOBILE_CI_FIX_STAGED')
