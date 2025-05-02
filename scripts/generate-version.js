const fs = require('fs');
const path = require('path');

const pkg = require('../package.json');
const versionFile = path.resolve(__dirname, '../src/version.ts');

const content = `// Auto-generated from package.json
export const VERSION = '${pkg.version}';
`;

try {
  fs.writeFileSync(versionFile, content);
} catch (err) {
  console.error('[version] Failed to write version.ts:', err);
  process.exit(1);
}
