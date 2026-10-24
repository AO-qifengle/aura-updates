# Aura public updates

Public update feed and released binaries only. No application source or credentials.

- Manifest: https://ao-qifengle.github.io/aura-updates/updates/latest.json
- Release notes: https://ao-qifengle.github.io/aura-updates/updates/V0.5.5.0.html
- Installation package: GitHub Releases, V0.5.5.0-build67.
- The official homepage and its existing Demo version are maintained separately and are unchanged.

Publish new immutable release assets and notes before updating the manifest. Do not overwrite old packages. Keep the manifest schema and digest consistent with the actual binary. The CI workflow verifies anonymous native curl requests on a fresh GitHub-hosted runner; update the expected release values when publishing a new version.
