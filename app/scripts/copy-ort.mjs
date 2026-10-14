// Copies the ONNX runtime WebAssembly backend (needed by the on-device speech engine) from
// node_modules into static/ort/ so the PWA serves it from its own origin. Runs before dev and
// build. The files are not committed: they are large and come from the installed package.
import { createRequire } from 'node:module';
import { mkdirSync, copyFileSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';

const require = createRequire(import.meta.url);
// Resolve the copy of onnxruntime-web that transformers.js itself uses (its package "exports"
// hides package.json, so resolve the entry file and walk up to the package folder).
const entry = require.resolve('onnxruntime-web', { paths: [dirname(require.resolve('@huggingface/transformers'))] });
const pkgDir = entry.slice(0, entry.lastIndexOf('onnxruntime-web') + 'onnxruntime-web'.length);
const dist = join(pkgDir, 'dist');
const out = join(process.cwd(), 'static', 'ort');
mkdirSync(out, { recursive: true });
// The WASM backend's three loader variants (the runtime picks one per browser: plain,
// asyncify, or JSPI). The WebGPU variant (jsep, 28 MB) is left out until WebGPU phones are a
// target; the engine asks for device 'wasm'. A phone downloads only the variant it uses.
const files = [
	'ort-wasm-simd-threaded.wasm', 'ort-wasm-simd-threaded.mjs',
	'ort-wasm-simd-threaded.asyncify.wasm', 'ort-wasm-simd-threaded.asyncify.mjs',
	'ort-wasm-simd-threaded.jspi.wasm', 'ort-wasm-simd-threaded.jspi.mjs'
];
let copied = 0;
for (const f of files) {
	const src = join(dist, f);
	if (existsSync(src)) {
		copyFileSync(src, join(out, f));
		copied++;
	}
}
console.log(`copy-ort: ${copied} runtime files -> static/ort/`);
