from flask import Flask, request
from board import TicTacToeBoard

app = Flask(__name__)


@app.route("/", methods=["GET"])
def server():
    board_string = request.args.get("board", None)
    if board_string is None:
        return "Value Error! No value was passed", 400
    board = TicTacToeBoard()
    try:
        board.from_string(board_string)
    except ValueError as error:
        return str(error), 400

    if board.check_win(board.OPPONENT):
        return "Opponent  has won cannot make any more move", 400
    if board.check_win(board.SERVER):
        return "Server has won cannot make any more move", 400
    result = board.make_move()
    if result is None:
        return board.to_string()
    else:
        return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
