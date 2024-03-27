const selectRandomFromList = async (items) => {
  return items[Math.floor(Math.random()*items.length)];
};


export { selectRandomFromList };
