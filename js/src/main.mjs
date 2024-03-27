import { buildTruthTable, LOGIC_0, LOGIC_1, LOGIC_X } from './truthTable.mjs';
import { generateCircuit, calculateCircuitOutput } from './logicCircuit.mjs';
import { and, or, not } from './logicGates.mjs';

/**
 * A smarter version on this would first check depth, then determine starting width from that
 * Additionally, it would be able to take more inputs.
 * For now, defaulting to 2 inputs works. But should split angle(s) to determine next point
 * e.g. 1 input -> theta0 = 0
 * 		2 inputs -> theta1 = 45, theta2 = -45
 * 		3 inputs -> theta1 = 0, theta1 = 45, theta2 = -45
 * 		4 inputs -> theta1 = 22.5, theta2 = 45, theta3 = -22.5, theta4 = -45
 * 		.... and so on ...?
 */
const circuitToDiagram = async (circuitNode, nodeRadius=30, nodes=[], links=[], xy=[400, 0], level=0) => {

	if (circuitNode.constructor === String) {
		nodes.push({ 'tag': circuitNode, 'xy': xy });
		return;
	}

	//centre == middle level of tree. Should be pre-calculate before converting
	const middleLevel = 2;

	const shiftX = (4 * nodeRadius);
	const shiftY = (4 * nodeRadius) / (2 ** (level - middleLevel)); 

	let tag;

	if (circuitNode.gate === and) {
		tag = 'AND'

	} else if (circuitNode.gate === or) {
		tag = 'OR'

	} else if (circuitNode.gate === not) {
		tag = 'NOT'

	} 

	nodes.push({ 'tag': tag, 'xy': xy });

	const parentIdx = nodes.length - 1;

	for (let i=0; i < circuitNode.input.length; i++) {

		const child = circuitNode.input[i];
		let xyChild;

		if (i%2 == 0) {
			xyChild = [xy[0] - shiftX, xy[1] + shiftY]; 

		} else {
			xyChild = [xy[0] - shiftX, xy[1] - shiftY]; 

		}

		links.push( { 'from': nodes.length, 'to': parentIdx} );
		await circuitToDiagram(child, nodeRadius, nodes, links, xyChild, level + 1);

	};
};

const test = async () => {

	const _0 = LOGIC_0;
	const _1 = LOGIC_1;
	const _X = LOGIC_X;

	const truthTable = buildTruthTable(
		[['A', 'B', 'C'], ['F']],
		[
			[[_0, _0, _0], [_0]],
			[[_0, _0, _1], [_0]],
			[[_0, _1, _0], [_0]],
			[[_0, _1, _1], [_1]],
			[[_1, _0, _0], [_0]],
			[[_1, _0, _1], [_1]],
			[[_1, _1, _0], [_1]],
			[[_1, _1, _1], [_1]],
		]
	);

	console.log(truthTable);

	const inputVars = Object.keys(truthTable.input[0]);
	const gates = [and, or, not];
	const maxDepth = 3;
	const rampThreshold = 0;

	let circuit = await generateCircuit(gates, inputVars, maxDepth, rampThreshold);

	const circuitOutput = await calculateCircuitOutput(circuit, truthTable.input);

	console.log(circuitOutput);

	const nodeRadius = 20;
	const nodes = [];
	const links = [];
	await circuitToDiagram(circuit, nodeRadius, nodes, links);

	console.log(nodes);
	console.log(links);

	return {
		'nodeRadius': nodeRadius,
		'nodes': nodes,
		'links': links,
	};

};

export { test };
