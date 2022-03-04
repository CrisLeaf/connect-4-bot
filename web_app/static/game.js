const player1 = "Player";
var player1Color = '#EF6156';

const player2 = "Bot";
var player2Color = '#ECEA22';

var tableRow = document.getElementsByTagName('tr');
var tableData = document.getElementsByTagName('td');
var playerTurn = document.querySelector('.player-turn');
const slots = document.querySelectorAll('.slot');
const resetBtn = document.querySelector('.reset');

var currentPlayer = 1;
let winner;
playerTurn.textContent = `${player1}'s turn!`

/*
for (i = 0; i < tableData.length; i++) {
    tableData[i].addEventListener('click', (e) => {
        console.log(`${e.target.parentElement.rowIndex},${e.target.cellIndex}`)
    });
};
*/

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
        if (tableRow[i].children[column].style.backgroundColor == 'white') {
            //console.log(column, tableRow[i].rowIndex);
            row.push(tableRow[i].children[column]);

			if (currentPlayer === 1) {
				gameArray[i][column] = 1;
			} else {
				gameArray[i][column] = -1;
			}
			//console.log(JSON.stringify(gameArray));

			/*
			fetch("/getmethod", {
				method: "POST",
				body: JSON.stringify({"game_array": JSON.stringify(gameArray)})
			}).then(function (response) {
				response.json().then((res) => console.log(res.bot_move));
			});
			*/

			var obj;


			fetch("/getmethod", {
				method: "POST",
				body: JSON.stringify({"game_array": JSON.stringify(gameArray)})
			}).then(function (response) {
				response.json()
				.then((data) => obj = data)
				.then(() => console.log(obj));
			});


			console.log(obj.bot_move);






            if (currentPlayer === 1) {
                row[0].style.backgroundColor = '#EF6156';
                if (horizontalCheck() || verticalCheck() || diagonalCheck() || diagonalCheck2()) {
                    playerTurn.textContent = "Player Wins!";
                    playerTurn.style.color = player1Color;
                    return alert("Player Wins!");
                } else if (drawCheck()) {
                    playerTurn.textContent = 'Draw!';
                    return alert('Draw!');
                } else {
                    //playerTurn.textContent = `${player2}'s turn`
                    return currentPlayer = 2;
                }
            } else {
                row[0].style.backgroundColor = '#ECEA22';
                if (horizontalCheck() || verticalCheck() || diagonalCheck() || diagonalCheck2()) {
                    playerTurn.textContent = "Bot Wins!";
                    playerTurn.style.color = player2Color;
                    return alert("Bot Wins!");
                } else if (drawCheck()) {
                    playerTurn.textContent = 'Draw!';
                    return alert('Draw!');
                } else {
                    //playerTurn.textContent = `${player1}'s turn`;
                    return currentPlayer = 1;
                }

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
	for (i = 0; i < 6; i++) {
		for (j = 0; j < 7; j++) {
			gameArray[i][j] = 0;
		}
	}
    slots.forEach(slot => {
        slot.style.backgroundColor = 'white';
    });
    playerTurn.style.color = 'black';
    return (currentPlayer === 1 ? playerTurn.textContent = `${player1}'s turn` : playerTurn.textContent = `${player2}'s turn`);
});