// Render TeX to HTML with KaTeX. stdin: JSON [[tex, displayMode], ...]; stdout: JSON [html, ...]
const katex = require('katex');
let input = '';
process.stdin.on('data', d => { input += d; });
process.stdin.on('end', () => {
  const out = JSON.parse(input).map(([tex, display]) => {
    try {
      return katex.renderToString(tex, { displayMode: display, throwOnError: true, strict: 'ignore', output: 'html' });
    } catch (e) {
      process.stderr.write(`KaTeX error in: ${tex}\n  ${e.message}\n`);
      return katex.renderToString(tex, { displayMode: display, throwOnError: false, strict: 'ignore', output: 'html' });
    }
  });
  process.stdout.write(JSON.stringify(out));
});
