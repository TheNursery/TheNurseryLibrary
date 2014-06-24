var config = {
	game_width: 800,
	game_height: 500,
	colours: {
		bg: 'rgba(0,0,0,1)',
		p1: '#ffffff',
		p2: '#ffffff',
		ball: '#ffff00'
	},
	playerStartWidth: 76,
	playerHeight: 10,
	ballSize: 10,
	vxMax: 10,
	vyMax: 10,
	eRoot: 1, // Square root of Elasticity: == 1 for perfectly elastic collisions, < 1 for damped collisions, > 1 for madness
	edgeTol: 2, // Tolerance for collision detection on the edge of player bars 2 = full ball diameter tolerance,
};

var gameState = {
	player1: {
		height: config.playerHeight,
		width: config.playerStartWidth,
		y: (config.game_height - config.playerStartWidth)/2,
		x: 0
	},
	player2: {
		height: config.playerHeight,
		width: config.playerStartWidth,
		x: config.game_width - config.playerHeight,
		y: (config.game_height - config.playerStartWidth)/2,
	},
	ball: {
		r: config.ballSize / 2,
		x: config.game_width / 2,
		y: config.game_height / 2,
		vx: (2 * Math.random() - 1) * config.vxMax,
		vy: (2 * Math.random() - 1) * config.vyMax
	},
	scores: {
		radiant: 0,
		dire: 0
	}
};

function graphics_tick(ctx) {
	// Clear the canvas
	ctx.fillStyle = config.colours.bg;
	ctx.fillRect(0, 0, config.game_width, config.game_height);

	// Draw player 1
	ctx.fillStyle = config.colours.p1;
	ctx.fillRect( gameState.player1.x, gameState.player1.y, gameState.player1.height, gameState.player1.width );

	// Draw player 2
	ctx.fillStlye = config.colours.p2;
	ctx.fillRect( gameState.player2.x, gameState.player2.y, gameState.player2.height, gameState.player2.width);

	// Draw the ball
	ctx.fillStyle = config.colours.ball;
	ctx.beginPath();
	ctx.arc( gameState.ball.x, gameState.ball.y, gameState.ball.r, 0, 2 * Math.PI );
	ctx.fill();
};


function physics_tick() {
	gameState.ball.x += gameState.ball.vx;
	gameState.ball.y += gameState.ball.vy;
};

function collision_detection() {
	// First we check to see whether the ball has touched the edge of the arena
	if (gameState.ball.y - gameState.ball.r < 0) {
		// Top - reflect
		console.log("Collision t");
		gameState.ball.y = gameState.ball.r;
		gameState.ball.vy *= -config.eRoot;
	} else if (gameState.ball.y + gameState.ball.r > config.game_height) {
		// Bottom - reflect
		console.log("Collision b");
		gameState.ball.y = config.game_height - gameState.ball.r;
		gameState.ball.vy *= - config.eRoot;
	}

	// Next check to see if we've collided with a paddle
	if (gameState.ball.x - gameState.player1.x <= gameState.player1.height + gameState.ball.r
		&& gameState.ball.y - gameState.player1.y <= gameState.player1.height + gameState.ball.r)
	{
		console.log("Collision p1");
		// Ball has touched player1's paddle
		gameState.ball.x = gameState.ball.r + gameState.player1.height;
		gameState.ball.vx *= -config.eRoot;
		return;
	} else if(Math.abs(gameState.ball.x - gameState.player2.x) <= gameState.player2.height + gameState.ball.r
		&& Math.abs(gameState.ball.y - gameState.player2.y) <= gameState.player2.height + gameState.ball.r)
	{
		console.log("Collision p2");
		gameState.ball.x = gameState.player2.height - gameState.ball.r;
		gameState.ball.vx *= -config.eRoot;
		return;
	}

	// Finally check to see if we've collided with the left or right walls
	if (gameState.ball.x - gameState.ball.r < 0) {
		// Ball has hit radiant wall
		console.log("Collision l");
		gameState.scores.dire += 1;
		new_round();		
	}
	if (gameState.ball.x + gameState.ball.r > config.game_width) {
		console.log("Collision r");
		gameState.scores.radiant += 1;
		new_round();
	}
}

function new_round() {
	document.getElementById('radiant_score').innerHTML = gameState.scores.radiant;
	document.getElementById('dire_score').innerHTML = gameState.scores.dire;
	gameState.ball.x = config.game_width / 2;
	gameState.ball.y = config.game_height / 2;
	gameState.ball.vx = (2 * Math.random() - 1) * config.vxMax;
	gameState.ball.vy = (2 * Math.random() - 1) * config.vyMax
}

function canvas_init() {
	var canvas = document.getElementById('game_canvas');
	var ctx = canvas.getContext('2d');
	canvas.width = config.game_width;
	canvas.height = config.game_height;
	ctx.fillStyle = config.colours.bg;
	ctx.fillRect(0, 0, canvas.width, canvas.height);
	
};
var ctx = document.getElementById('game_canvas').getContext('2d');

function main() {
	canvas_init();
	graphics_tick(ctx);
	loop();
};

function loop() {
	physics_tick();
	collision_detection();
	graphics_tick(ctx);
	window.setTimeout(loop, 16);
}

main();
