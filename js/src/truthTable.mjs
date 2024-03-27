const LOGIC_0 = '0';
const LOGIC_1 = '1';
const LOGIC_X = 'X';

const buildTruthTable = (header, rows) => {

	const idxIn = 0;
	const idxOut = 1;

	const inputVars = header[idxIn];
	const outputVars = header[idxOut];

	const truthTable = { 'input': [], 'output': [] };

	for (let i=0; i < rows.length; i++) {

		const inputRow = {};
		const outputRow = {};

		for (let j in inputVars) {
			inputRow[inputVars[j]] = rows[i][idxIn][j];
		}

		for (let k in outputVars) {
			outputRow[outputVars[k]] = rows[i][idxOut][k];
		}

		truthTable.input.push(inputRow);
		truthTable.output.push(outputRow);

	}

	return truthTable;
};


export { LOGIC_0, LOGIC_1, LOGIC_X, buildTruthTable };
