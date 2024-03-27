const drawCircle = (context, centreX, centreY, circleX, circleY, radius) => {

	const angleStart = 0;
	const angleEnd = 2 * Math.PI;

	const circleCentre = [
	  	centreX + circleX, 
  		centreY + circleY
  	];
	  
  	context.beginPath()
	context.arc(...circleCentre, radius, angleStart, angleEnd);
	context.stroke()
}

const writeText = (context, centreX, centreY, startX, startY, maxWidth, text) => {

  	const textStart = [ 
	  	centreX + startX, 
  		centreY + startY 
  	];
	  
	context.strokeText(text, ...textStart, maxWidth);

}

const drawNode = (context, centreX, centreY, circleX, circleY, nodeRadius, tag) => {

	const maxWidth = nodeRadius;

	const textStart = [
		circleX - (maxWidth / 5),
		circleY + (maxWidth / 10)
	];

	drawCircle(context, centreX, centreY, circleX, circleY, nodeRadius);
	writeText(context, centreX, centreY, ...textStart, maxWidth, tag);

}

const drawLink = (context, centreX, centreY, fromX, fromY, toX, toY, nodeRadius) => {

  	const lineStart = [
	  	centreX + fromX + nodeRadius, 
  		centreY + fromY
  	];

  	const lineElbow = [
	  	centreX - ((toX - fromX)/2), 
  		centreY + fromY
  	]

   	const lineEnd = [
	  	centreX + toX - nodeRadius, 
  		centreY + toY
  	];

	context.lineWidth = 1.5;
	context.lineJoin = 'miter';
	context.beginPath();
	context.moveTo(...lineStart);
	//context.lineTo(...lineElbow);
	context.lineTo(...lineEnd);
	context.stroke();

}

const drawCircuit = (canvasId, nodeRadius, nodes, links) => {

  	const canvas = document.getElementById(canvasId);
  	const context = canvas.getContext('2d');

	const canvasCentre = [ 
		canvas.width / 2, 
	  	canvas.height / 2 
  	];	

	nodes.forEach((node) => {

		drawNode(context, ...canvasCentre, ...node.xy, nodeRadius, node.tag);

	});

	links.forEach((link) => {

		xyFrom = nodes[link.from].xy;
		xyTo = nodes[link.to].xy;

		drawLink(context, ...canvasCentre, ...xyFrom, ...xyTo, nodeRadius);
	});

}
