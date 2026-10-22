#!/bin/sh
set -eu
cd "${CI_PRIMARY_REPOSITORY_PATH:-$(cd "$(dirname "$0")/../../.." && pwd)}"
if ! command -v node >/dev/null 2>&1; then
  brew install node@24
  export PATH="$(brew --prefix node@24)/bin:$PATH"
fi
node --version
npm ci --no-audit --no-fund
npm run sync:ios

# Xcode Cloud requires the committed Swift dependency lock when archiving.
test -s ios/App/App.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/Package.resolved
