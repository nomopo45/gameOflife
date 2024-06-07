package main

import (
	"image/color"
	"log"
	"math/rand"
	"time"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
	"github.com/hajimehoshi/ebiten/v2/inpututil"
	"github.com/hajimehoshi/ebiten/v2/text"

	"golang.org/x/image/font/basicfont"
)

const (
	screenWidth  = 640
	screenHeight = 480
	cellSize     = 10
)

// Game implements ebiten.Game interface.
type Game struct {
	grid     *Grid
	gameState string
}

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
	for i := row - 1; i <= row + 1; i++ {
		for j := col - 1; j <= col + 1; j++ {
			if i >= 0 && i < len(g) && j >= 0 && j < len(g[0]) && (i != row || j != col) && g[i][j] {
				count++
			}
		}
	}
	return count
}

// Update proceeds the game state.
// Update is called every tick (1/60 [s] by default).
func (g *Game) Update() error {
	// Update game logic here.
	if g.gameState == "running" {
		newGrid := g.grid.NextGeneration()
		*g.grid = newGrid
		time.Sleep(time.Millisecond * 100)
	}

	if inpututil.IsMouseButtonJustPressed(ebiten.MouseButtonLeft) && g.gameState == "startMenu" {
		x, y := ebiten.CursorPosition()
		if x >= 270 && x <= 370 && y >= 180 && y <= 230 {
			g.gameState = "running"
		}
	}

	return nil
}

// Draw draws the game screen.
// Draw is called every frame (typically 1/60[s] for 60Hz display).
func (g *Game) Draw(screen *ebiten.Image) {
	// Draw game graphics here.
	if g.gameState == "startMenu" {
		// Draw start menu
		drawButton(screen, 270, 180, 100, 50, color.White, "PLAY")
	} else {
		for row := range *g.grid {
			for col, cell := range (*g.grid)[row] {
				if cell {
					ebitenutil.DrawRect(screen, float64(col*cellSize), float64(row*cellSize), cellSize, cellSize, color.White)
				}
			}
		}
	}
}

// Layout takes care of screen resizing
func (g *Game) Layout(outsideWidth, outsideHeight int) (int, int) {
	return screenWidth, screenHeight
}

func main() {
	rand.Seed(time.Now().UnixNano())

	rows := screenHeight / cellSize
	cols := screenWidth / cellSize
	grid := NewGrid(rows, cols)
	grid.Randomize(0.3)

	game := &Game{grid: &grid, gameState: "startMenu"}
	ebiten.SetWindowSize(screenWidth, screenHeight)
	ebiten.SetWindowTitle("Conway's Game of Life (Ebiten)")
	if err := ebiten.RunGame(game); err != nil {
		log.Fatal(err)
	}
}

func drawButton(screen *ebiten.Image, x, y, width, height int, color color.Color, label string) {
	ebitenutil.DrawRect(screen, float64(x), float64(y), float64(width), float64(height), color)
	text.Draw(screen, label, basicfont.Face7x13, x+10, y+38, color.Black)
}
