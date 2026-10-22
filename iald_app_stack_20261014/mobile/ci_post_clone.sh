#!/bin/sh
set -eu
cd "${CI_PRIMARY_REPOSITORY_PATH:-$(cd "$(dirname "$0")/../../.." && pwd)}"

# Use the official pinned Node distribution. Homebrew's shared OpenSSL lock
# failed before npm ci on Xcode Cloud builds 30 and 31.
IALD_NODE_VERSION=24.21.0
case "$(uname -s)/$(uname -m)" in
  Darwin/arm64) IALD_NODE_ARCH=arm64; IALD_NODE_SHA=bed7eea5325e1108f32ce5228ddd6a5f0f08a499ee42aa7442aea583702f6057 ;;
  Darwin/x86_64) IALD_NODE_ARCH=x64; IALD_NODE_SHA=1462cb3b3046b815cf8ea436d3da450ec1a9f11dac7e5a46b0ada5305d7e8097 ;;
  *) echo "Unsupported Xcode Cloud platform" >&2; exit 1 ;;
esac
IALD_NODE_BUNDLE="node-v${IALD_NODE_VERSION}-darwin-${IALD_NODE_ARCH}"
IALD_NODE_DIR=$(mktemp -d "${TMPDIR:-/tmp}/iald-node.XXXXXX")
curl --fail --show-error --location --retry 3 --proto '=https' --tlsv1.2   "https://nodejs.org/dist/v${IALD_NODE_VERSION}/${IALD_NODE_BUNDLE}.tar.gz"   --output "${IALD_NODE_DIR}/${IALD_NODE_BUNDLE}.tar.gz"
printf '%s  %s\n' "$IALD_NODE_SHA" "${IALD_NODE_DIR}/${IALD_NODE_BUNDLE}.tar.gz" | shasum -a 256 -c -
tar -xzf "${IALD_NODE_DIR}/${IALD_NODE_BUNDLE}.tar.gz" -C "$IALD_NODE_DIR"
export PATH="${IALD_NODE_DIR}/${IALD_NODE_BUNDLE}/bin:$PATH"
test "$(node --version)" = "v${IALD_NODE_VERSION}"
node --version
npm ci --no-audit --no-fund
npm run sync:ios

# Xcode Cloud requires the committed Swift dependency lock when archiving.
test -s ios/App/App.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/Package.resolved
