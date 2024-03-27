import { and, or, not } from './logicGates.mjs'
import { selectRandomFromList } from './utils.mjs';


/**
 * CircuitNode : data structure for logic circuit gates
 **
 * -> gate: the type of gate at this node
 * -> input: the incoming connections (children nodes or input variables)
 **/
class CircuitNode {
  constructor (gate) {
    this.gate = gate;
    this.input = [];
  }
};

/**
 * generateCircuit : randomly generate a new logic circuit
 **
 * -> gates: the set of gate types to use
 * -> maxDepth : maximum depth of the tree which is generated
 * -> rampThreshold : Threshold for randomly choosing generation method
 *    (To definitely generate a full circuit, set rampThreshold==0)
 **/
const generateCircuit = async (gates, variables, maxDepth, rampThreshold=0.5) => {
  
  const outputNode = new CircuitNode(await selectRandomFromList(gates));

  const isFullCircuit = (Math.random() >= rampThreshold);

  await addChildren(outputNode, gates, variables, maxDepth, isFullCircuit);

  return outputNode;

};

/**
 * 
 **/
const addChildren = async (parent, gates, variables, maxDepth, isFullCircuit) => {

  for (let i = 0; i < parent.gate.length; i++) {

    if (maxDepth <= 1) {
      parent.input.push(await selectRandomFromList(variables));

    } else if (!isFullCircuit && (Math.random() < 0.5)) {
      parent.input.push(await selectRandomFromList(variables));

    } else {
      const child = new CircuitNode(await selectRandomFromList(gates));
      await addChildren(child, gates, variables, maxDepth-1, isFullCircuit);
      parent.input.push(child);

    };
  };
};

/**
 * calculateCircuitOutput : returns circuit output for given row of truth table
 **
 * -> outputNode: the node upon which we are operating
 * -> inputRow: a truth table row
 **/
const calculateCircuitOutput = async (outputNode, truthTableInput) => {

  const outputVals = [];

    for (let i = 0; i < truthTableInput.length; i++){
      outputVals.push(await calculateRowOutput(outputNode, truthTableInput[i]));

    };

    return outputVals;

};

const calculateRowOutput = async (outputNode, truthTableInputRow) => {

  const inputVals = [];

  for (let i=0; i < outputNode.gate.length; i++) {

    if (outputNode.input[i].constructor === CircuitNode) {
      inputVals.push(await calculateRowOutput(outputNode.input[i], truthTableInputRow));

    } else {
      inputVals.push(truthTableInputRow[outputNode.input[i]]);

    };

  };

  return outputNode.gate(...inputVals);

};


export { generateCircuit, calculateCircuitOutput };
