import { test } from './src/main.mjs'
import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const port = 8000;

app.use(express.static(__dirname));

app.listen(port, () => {

  console.log(`Listening on port ${port}`);

});

app.get('/test', async (req, resp) => {

  const testResults = await test();

  resp.json(testResults);

});

