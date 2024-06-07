package main

import (
	"fmt"
	"math/rand"
	"time"
)

// Grid represents the game board
type Grid [][]bool

// NewGrid creates a new grid with the given dimensions
func NewGrid(rows, cols int) Grid {
	grid := make(Grid, rows)
	for i := range grid {
		grid[i] = make([]bool, cols)
	}
	return grid
}

// Randomize populates the grid with random cells
func (g Grid) Randomize(fillProbability float64) {
	for i := range g {
		for j := range g[i] {
			if rand.Float64() < fillProbability {
				g[i][j] = true
			}
		}
	}
}

// Print displays the grid
func (g Grid) Print() {
	for i := range g {
		for j := range g[i] {
			if g[i][j] {
				fmt.Print("X ")
			} else {
				fmt.Print(". ")
			}
		}
		fmt.Println()
	}
}

// NextGeneration calculates the next generation of the grid
func (g Grid) NextGeneration() Grid {
	newGrid := NewGrid(len(g), len(g[0]))
	for i := range g {
		for j := range g[i] {
			neighbors := g.countNeighbors(i, j)
			if g[i][j] {
				if neighbors == 2 || neighbors == 3 {
					newGrid[i][j] = true
				}
			} else {
				if neighbors == 3 {
					newGrid[i][j] = true
				}
			}
		}
	}
	return newGrid
}

// countNeighbors counts the number of live neighbors for a cell
func (g Grid) countNeighbors(row, col int) int {
	count := 0
	for i := row - 1; i <= row+1; i++ {
		for j := col - 1; j <= col+1; j++ {
			if i >= 0 && i < len(g) && j >= 0 && j < len(g[0]) && (i != row || j != col) && g[i][j] {
				count++
			}
		}
	}
	return count
}

func main() {
	rand.Seed(time.Now().UnixNano())

	rows := 10
	cols := 20
	grid := NewGrid(rows, cols)
	grid.Randomize(0.3)

	for {
		fmt.Print("\033[H\033[2J") // Clear the screen
		grid.Print()
		grid = grid.NextGeneration()
		time.Sleep(time.Millisecond * 100)
	}
}
