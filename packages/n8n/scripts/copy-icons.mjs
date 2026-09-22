// tsc does not copy the svg files the node description points at.
import { cp, mkdir } from 'node:fs/promises';
import { glob } from 'node:fs/promises';

for await (const file of glob('nodes/**/*.svg')) {
	const target = `dist/${file}`;
	await mkdir(target.slice(0, target.lastIndexOf('/')), { recursive: true });
	await cp(file, target);
	console.log(`copied ${file}`);
}
