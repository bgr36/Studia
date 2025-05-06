package main

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

const NrOfTravelers = 15
const MinSteps = 10
const MaxSteps = 100
const MinDelay = 0.01
const MaxDelay = 0.05
const BoardWidth = 15
const BoardHeight = 15

var StartTime = time.Now()

type Position struct {
	X int
	Y int
}

func (p *Position) MoveDown() {
	p.Y = (p.Y + 1) % BoardHeight
}

func (p *Position) MoveUp() {
	p.Y = (p.Y - 1 + BoardHeight) % BoardHeight
}

func (p *Position) MoveRight() {
	p.X = (p.X + 1) % BoardWidth
}

func (p *Position) MoveLeft() {
	p.X = (p.X - 1 + BoardWidth) % BoardWidth
}

type Trace struct {
	ID        int
	Symbol    rune
	TimeStamp time.Duration
	Position  Position
}

func (t *Trace) Print() {
	fmt.Printf("%.9f %d %d %d %c\n", t.TimeStamp.Seconds(), t.ID, t.Position.X, t.Position.Y, t.Symbol)
}

type TraceArray [MaxSteps]Trace

type TracesSequence struct {
	Last       int
	TraceArray TraceArray
}

func (ts *TracesSequence) PrintTraces() {
	for i := 0; i <= ts.Last; i++ {
		ts.TraceArray[i].Print()
	}
}

type Cell struct {
	mu       sync.Mutex
	Occupied bool
}

type Grid struct {
	Cells map[Position]*Cell
}

var grid = NewGrid(BoardWidth, BoardHeight)

func NewGrid(width, height int) *Grid {
	grid := &Grid{Cells: make(map[Position]*Cell)}
	for x := 0; x < width; x++ {
		for y := 0; y < height; y++ {
			grid.Cells[Position{x, y}] = &Cell{}
			grid.Cells[Position{x, y}].Occupied = false
		}
	}
	return grid
}

type TravelerTask struct {
	ID       int
	Symbol   rune
	Position Position
	Traces   TracesSequence
	Steps    int
	Active   bool
	RNG      *rand.Rand
}

func (t *TravelerTask) Init(ID int, seed int64, symbol rune) {
	t.ID = ID
	t.Symbol = symbol
	t.RNG = rand.New(rand.NewSource(seed))

	for {
		position := Position{
			X: int(float64(BoardWidth) * t.RNG.Float64()),
			Y: int(float64(BoardHeight) * t.RNG.Float64()),
		}

		grid.Cells[position].mu.Lock()
		if _, taken := grid.Cells[position]; !taken || !grid.Cells[position].Occupied {
			grid.Cells[position].Occupied = true
			t.Position = position
			grid.Cells[position].mu.Unlock()
			break
		}
		grid.Cells[position].mu.Unlock()

	}

	t.Active = true

	t.Traces = TracesSequence{}
	t.Traces.Last = -1
	t.storeTrace(time.Now().Sub(StartTime))
	t.Steps = MinSteps + int(float64(MaxSteps-MinSteps)*t.RNG.Float64())
}

func (t *TravelerTask) Start(traceChannel chan<- TracesSequence) {

	for range t.Steps {
		if !t.Active {
			break
		}
		delay := MinDelay + (MaxDelay-MinDelay)*t.RNG.Float64()
		time.Sleep(time.Duration(delay * float64(time.Second)))
		t.Active = t.makeStep()
		t.storeTrace(time.Now().Sub(StartTime))
	}
	traceChannel <- t.Traces
}

func (t *TravelerTask) storeTrace(timestamp time.Duration) {
	t.Traces.Last++
	t.Traces.TraceArray[t.Traces.Last] = Trace{
		TimeStamp: timestamp,
		ID:        t.ID,
		Position:  t.Position,
		Symbol:    t.Symbol,
	}
}

func (t *TravelerTask) makeStep() bool {
	oldPosition := t.Position
	start := time.Now()

	direction := t.RNG.Intn(4)

	for {
		switch direction {
		case 0:
			t.Position.MoveUp()
		case 1:
			t.Position.MoveDown()
		case 2:
			t.Position.MoveLeft()
		case 3:
			t.Position.MoveRight()
		}

		if time.Since(start) > 5*time.Duration(MaxDelay*float64(time.Second)) {
			t.Position = oldPosition
			t.Symbol = t.Symbol + 32
			return false
		}

		grid.Cells[t.Position].mu.Lock()
		if _, taken := grid.Cells[t.Position]; !taken || !grid.Cells[t.Position].Occupied {
			grid.Cells[oldPosition].Occupied = false
			grid.Cells[t.Position].Occupied = true
			grid.Cells[t.Position].mu.Unlock()
			break
		}
		grid.Cells[t.Position].mu.Unlock()

		t.Position = oldPosition
	}
	return true
}

func main() {
	fmt.Printf("-1 %d %d %d\n", NrOfTravelers, BoardWidth, BoardHeight)

	traceChannel := make(chan TracesSequence, NrOfTravelers)

	travelTasks := make([]TravelerTask, NrOfTravelers)
	symbol := 'A'

	for i := range NrOfTravelers {
		travelTasks[i].Init(i, time.Now().UnixNano()+int64(i), symbol)
		symbol++
	}

	var wg sync.WaitGroup
	wg.Add(NrOfTravelers)

	for i := range NrOfTravelers {
		go func(task *TravelerTask) {
			defer wg.Done()
			task.Start(traceChannel)
		}(&travelTasks[i])
	}

	go func() {
		wg.Wait()
		close(traceChannel)
	}()

	for trace := range traceChannel {
		trace.PrintTraces()
	}
}
