import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const [prompt, size, outFile] = process.argv.slice(2);

async function main() {
	try {
		const zai = await ZAI.create();
		const response = await zai.images.generations.create({ prompt, size });
		const base64 = response?.data?.[0]?.base64;
		if (!base64) {
			console.error('No image data returned by the API');
			return;
		}
		fs.writeFileSync(outFile, Buffer.from(base64, 'base64'));
		console.log(`Image saved to ${outFile}`);
	} catch (err) {
		console.error('Image generation failed:', err?.message || err);
	}
}

main();
