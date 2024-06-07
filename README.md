# Conway's Game of Life (Ebiten)

This is a simple implementation of Conway's Game of Life using the Ebiten game library.

## How to Play

1. Click the "PLAY" button to start the game.
2. The game will start with a randomized grid of cells.
3. Watch as the cells evolve according to the rules of Conway's Game of Life.

## Rules

The game follows these simple rules:

* **Survival:** A live cell with 2 or 3 live neighbors survives to the next generation.
* **Death:** A live cell with fewer than 2 live neighbors dies (underpopulation).
A live cell with more than 3 live neighbors dies (overpopulation).
* **Birth:** A dead cell with exactly 3 live neighbors becomes a live cell (reproduction).

## Controls

* **Mouse Click:** Used to interact with the game menu.

## Installation

1. Make sure you have Go installed on your system.
2. Install the Ebiten game library: `go get github.com/hajimehoshi/ebiten/v2`
3. Clone this repository: `git clone https://github.com/nomopo45/gameOflife.git`
4. Navigate to the project directory: `cd gameOflife`
5. Initialize go modules: `go mod init conway.go`
6. Install dependencies: `go mod tidy`
7. Run the game: `go run .`

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
