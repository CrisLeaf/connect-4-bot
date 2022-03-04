const player1 = "Player";
var player1Color = '#EF6156';

const player2 = "Bot";
var player2Color = '#ECEA22';

var drawColor = '#595959';

var tableRow = document.getElementsByTagName('tr');
var tableData = document.getElementsByTagName('td');
var playerTurn = document.querySelector('.player-turn');
const slots = document.querySelectorAll('.slot');
const resetBtn = document.querySelector('.reset');
var normalBtn = document.getElementById("normal");
var hardBtn = document.getElementById("hard");


normalBtn.classList.add("clicked");

playerTurn.textContent = "";

var currentPlayer = 1;
let winner;
//playerTurn.textContent = `${player1}'s turn!`

var playTime = true;
var resetTime = true;

const gameArray = [[0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0]]

function changeColor (e) {
    let column = e.target.cellIndex;
    let row = [];

    for (i = 5; i > -1; i--) {
        if (tableRow[i].children[column].style.backgroundColor == 'white' && playTime === true) {
            row.push(tableRow[i].children[column]);
            row[0].style.backgroundColor = '#EF6156';
            playTime = false;
            resetTime = false;

            if (currentPlayer === 1) {
                gameArray[i][column] = 1
                if (horizontalCheck() || verticalCheck() || diagonalCheck() || diagonalCheck2()) {
                    playerTurn.style.color = player1Color;
                    playerTurn.textContent = "Player Wins!";
                    resetTime = true;
                    return alert("Player Wins!");
                } else if (drawCheck()) {
                    playerTurn.style.color = drawColor;
                    playerTurn.textContent = 'Draw!';
                    return alert('Draw!');
                } else {
		            fetch("/bot", {
		                method: "POST",
		                body: JSON.stringify({"game_array": JSON.stringify(gameArray)})
		            }).then(function (response) {
		                response.json()
		                .then((data) => botMove = data)
		                .then(() => playTime = true)
		                .then(() => botPlay(botMove.bot_move))
		                .then(() => resetTime = true)
		            });
		            return
                }
            }
        }
    }
}

function botPlay (column) {
	let row = [];

	for (i = 5; i > -1; i--) {
        if (tableRow[i].children[column].style.backgroundColor == 'white') {
            row.push(tableRow[i].children[column]);
            row[0].style.backgroundColor = '#ECEA22';
            gameArray[i][column] = -1

            if (horizontalCheck() || verticalCheck() || diagonalCheck() || diagonalCheck2()) {
                playerTurn.style.color = player2Color;
                playerTurn.textContent = "Bot Wins!";
                playTime = false;
                return alert("Bot Wins!");
            } else if (drawCheck()) {
                playerTurn.style.color = drawColor;
                playerTurn.textContent = 'Draw!';
                return alert('Draw!');
            } else {
                return currentPlayer = 1;
            }
        }

    }
}

Array.prototype.forEach.call(tableData, (cell) => {
	cell.addEventListener('click', changeColor);
    cell.style.backgroundColor = 'white';
});

function colorMatchCheck (one, two, three, four) {
    return (one === two && one === three && one === four && one !== 'white' && one !== undefined);
}

function horizontalCheck () {
    for (let row = 0; row < tableRow.length; row++) {
        for (let col =0; col < 4; col++) {
           if (colorMatchCheck(tableRow[row].children[col].style.backgroundColor,tableRow[row].children[col+1].style.backgroundColor,
                                tableRow[row].children[col+2].style.backgroundColor, tableRow[row].children[col+3].style.backgroundColor)) {
               return true;
           }
        }
    }
}

function verticalCheck () {
    for (let col = 0; col < 7; col++) {
        for (let row = 0; row < 3; row++) {
            if (colorMatchCheck(tableRow[row].children[col].style.backgroundColor, tableRow[row+1].children[col].style.backgroundColor,
                                tableRow[row+2].children[col].style.backgroundColor,tableRow[row+3].children[col].style.backgroundColor)) {
                return true;
            };
        }
    }
}

function diagonalCheck () {
    for (let col = 0; col < 4; col++) {
        for (let row = 0; row < 3; row++) {
            if (colorMatchCheck(tableRow[row].children[col].style.backgroundColor, tableRow[row+1].children[col+1].style.backgroundColor,
                tableRow[row+2].children[col+2].style.backgroundColor,tableRow[row+3].children[col+3].style.backgroundColor)) {
                return true;
            }
        }
    }
}

function diagonalCheck2 () {
    for (let col = 0; col < 4; col++) {
        for (let row = 5; row > 2; row--) {
            if (colorMatchCheck(tableRow[row].children[col].style.backgroundColor, tableRow[row-1].children[col+1].style.backgroundColor,
                tableRow[row-2].children[col+2].style.backgroundColor,tableRow[row-3].children[col+3].style.backgroundColor)) {
                return true;
            }
        }
    }
}

function drawCheck () {
    let fullSlot = []
    for (i=0; i < tableData.length; i++) {
        if (tableData[i].style.backgroundColor !== 'white') {
            fullSlot.push(tableData[i]);
        }
    }
    if (fullSlot.length === tableData.length) {
        return true;
    }
}

resetBtn.addEventListener('click', () => {
	if (resetTime === true) {
		playTime = true;
		for (i = 0; i < 6; i++) {
			for (j = 0; j < 7; j++) {
				gameArray[i][j] = 0;
			}
		}
	    slots.forEach(slot => {
	        slot.style.backgroundColor = 'white';
	    });
	    playerTurn.textContent = "";
	    return (currentPlayer === 1);
    } else {
        return
    }
});

function changeDifficulty (lvl) {
	if (lvl == 1) {
		fetch("/d", {
            method: "POST",
            body: JSON.stringify({"level": JSON.stringify(lvl)})
        });
        hardBtn.classList.remove("clicked");
		normalBtn.classList.add("clicked");
	} else {
		fetch("/d", {
            method: "POST",
            body: JSON.stringify({"level": JSON.stringify(lvl)})
        });
        normalBtn.classList.remove("clicked");
		hardBtn.classList.add("clicked");
	}
}