# Tic Tac Toe API

## Introduction

The Tic Tac Toe API is a web service that allows you to play the classic game of Tic Tac Toe (also known as Noughts and Crosses) against an AI opponent. This API is built using Python and Flask, and it follows the standard rules of Tic Tac Toe.

## Requirements

Before you can run the Tic Tac Toe API, ensure you have the following requirements installed on your system:

- Python 3.x: You need Python 3.6 or newer to run the API.
- Flask: Install Flask, a micro web framework for Python, using pip:
  ```
  pip install -r requirements.txt
  ```

## Cloning the Code

To clone the Tic Tac Toe API code from the GitHub repository, follow these steps:

1. Open your terminal or command prompt.

2. Change the current working directory to where you want to store the project:

   ```
   cd /path/to/your/directory
   ```

3. Clone the repository using Git:

   ```
   git clone https://github.com/Lewanja/tic_tac_toe_api.git
   ```



4. After cloning, navigate to the project directory:

   ```
   cd tic_tac_toe_api
   ```

Now you have the Tic Tac Toe API code on your local machine and can proceed to run it.

## Usage

To use the Tic Tac Toe API, you can send HTTP GET requests to the root endpoint (`/`) with the current state of the Tic Tac Toe board as a query parameter named "board." The board is represented as a string of characters, where each character represents a cell on the board. The characters can be 'X' (for the opponent), 'O' (for the server), or a space ' ' (for an empty cell).

Example Request:
```
GET http://localhost:5000/?board=XXO OXO X
```

- 'X' represents the opponent's move.
- 'O' represents the server's move.
- ' ' (space) represents an empty cell.

## Responses

The API will respond with the updated state of the board after the server's move. If the server detects an invalid board state or if the game has already been won by either player, it will return an appropriate error message.

Example Response:
```
XOO OXO X
```

## API Endpoints

### GET /

- **Description:** Play a move in the Tic Tac Toe game.
- **Query Parameters:**
  - `board` (string, required): The current state of the Tic Tac Toe board.
- **Response:**
  - Success: The updated state of the board after the server's move.
  - Error: Error message if the move is invalid or the game has already been won.

## Error Handling

The Tic Tac Toe API provides error messages in the following scenarios:

- If the provided board string is not valid (e.g., incorrect length or contains invalid characters), it returns a "Value Error! No value was passed" error with a status code of 400 (Bad Request).

- If the game has already been won by either the opponent or the server, it returns an error message indicating the winner and that no more moves can be made.

## Running the API

To run the Tic Tac Toe API, you can use the provided Dockerfile and Docker Compose file. The API runs on port 5000 by default.

### Dockerfile

The Dockerfile sets up the API environment and installs the required dependencies. You can build the Docker image using the following command:

```
docker build -t tic_tac_toe_api .
```

### Docker Compose

The provided Docker Compose file (docker-compose.yml) allows you to easily run the API in a container. To start the API using Docker Compose, run the following command:

```
docker-compose up
```

## What Can Be Improved

While the Tic Tac Toe API functions as intended, there are several areas where it can be improved and expanded:

1. **Code/Function comments:** Enhance the Code/Function comments by providing arguments, their types and return types of methods and explanation of how the method works.

2. **Testing:** Develop comprehensive unit tests and integration tests to verify the correctness of the API's behavior. Automated testing will help catch regressions and ensure reliability.