import { LOGIC_0, LOGIC_1, LOGIC_X } from './truthTable.mjs';


const and = (a, b) => {
  if ((a===LOGIC_0) || (b===LOGIC_0)) return LOGIC_0;
  if ((a===LOGIC_1) && (b===LOGIC_1)) return LOGIC_1;
  return LOGIC_X;
}

const or = (a, b) => {
  if ((a===LOGIC_1) || (b===LOGIC_1)) return LOGIC_1;
  if ((a===LOGIC_0) && (b===LOGIC_0)) return LOGIC_0;
  return LOGIC_X;
}

const not = (a) => {
  if (a===LOGIC_0) return LOGIC_1;
  if (a===LOGIC_1) return LOGIC_0;
  return LOGIC_X;
}


export { and, or, not };
