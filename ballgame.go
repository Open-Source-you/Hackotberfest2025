package main

import (
	"fmt"
	"image"
	"image/color"
	"math"
	"math/rand"
	"time"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
)

const (
	screenW = 960
	screenH = 540

	fieldMargin = 40

	goalWidth  = 10         // tebal garis gawang
	goalMouthH = 220        // tinggi mulut gawang (bukaan)
	ballRadius = 10.0
	maxBallSpd = 9.5

	paddleW   = 22.0
	paddleH   = 110.0
	p1Speed   = 6.0
	p2SpeedAI = 5.2
	p2Speed   = 6.0 // saat 2-player

	friction = 0.90
)

type Vec struct {
	X, Y float64
}

type Ball struct {
	Pos   Vec
	Vel   Vec
	Img   *ebiten.Image
	Radius float64
}

type Paddle struct {
	Pos         Vec
	Width       float64
	Height      float64
	Color       color.Color
	IsAI        bool
	UpKey       ebiten.Key
	DownKey     ebiten.Key
	LeftKey     ebiten.Key
	RightKey    ebiten.Key
	MaxSpeed    float64
}

type Game struct {
	ball          Ball
	p1            Paddle
	p2            Paddle
	scoreL        int
	scoreR        int
	goalTop       float64
	goalBottom    float64
	toggleCooldown int // mencegah toggle Tab bertubi-tubi
}

// ------- util gambar sederhana -------

func makeCircleImage(d int, c color.Color) *ebiten.Image {
	img := image.NewRGBA(image.Rect(0, 0, d, d))
	r := float64(d-1) / 2.0
	cx := r
	cy := r
	cr, cg, cb, ca := color.RGBAModel.Convert(c).(color.RGBA).RGBA()
	// convert from 16-bit to 8-bit
	r8 := uint8(cr >> 8)
	g8 := uint8(cg >> 8)
	b8 := uint8(cb >> 8)
	a8 := uint8(ca >> 8)

	for y := 0; y < d; y++ {
		for x := 0; x < d; x++ {
			dx := float64(x) - cx
			dy := float64(y) - cy
			if dx*dx+dy*dy <= r*r {
				img.SetRGBA(x, y, color.RGBA{r8, g8, b8, a8})
package main

import (
	"fmt"
	"image"
	"image/color"
	"math"
	"math/rand"
	"time"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
)

const (
	screenW = 960
	screenH = 540

	fieldMargin = 40

	goalWidth  = 10         // tebal garis gawang
	goalMouthH = 220        // tinggi mulut gawang (bukaan)
	ballRadius = 10.0
	maxBallSpd = 9.5

	paddleW   = 22.0
	paddleH   = 110.0
	p1Speed   = 6.0
	p2SpeedAI = 5.2
	p2Speed   = 6.0 // saat 2-player

	friction = 0.90
)

type Vec struct {
	X, Y float64
}

type Ball struct {
	Pos   Vec
	Vel   Vec
	Img   *ebiten.Image
	Radius float64
}

type Paddle struct {
	Pos         Vec
	Width       float64
	Height      float64
	Color       color.Color
	IsAI        bool
	UpKey       ebiten.Key
	DownKey     ebiten.Key
	LeftKey     ebiten.Key
	RightKey    ebiten.Key
	MaxSpeed    float64
}

type Game struct {
	ball          Ball
	p1            Paddle
	p2            Paddle
	scoreL        int
	scoreR        int
	goalTop       float64
	goalBottom    float64
	toggleCooldown int // mencegah toggle Tab bertubi-tubi
}

// ------- util gambar sederhana -------

func makeCircleImage(d int, c color.Color) *ebiten.Image {
	img := image.NewRGBA(image.Rect(0, 0, d, d))
	r := float64(d-1) / 2.0
	cx := r
	cy := r
	cr, cg, cb, ca := color.RGBAModel.Convert(c).(color.RGBA).RGBA()
	// convert from 16-bit to 8-bit
	r8 := uint8(cr >> 8)
	g8 := uint8(cg >> 8)
	b8 := uint8(cb >> 8)
	a8 := uint8(ca >> 8)

	for y := 0; y < d; y++ {
		for x := 0; x < d; x++ {
			dx := float64(x) - cx
			dy := float64(y) - cy
			if dx*dx+dy*dy <= r*r {
				img.SetRGBA(x, y, color.RGBA{r8, g8, b8, a8})
			}
		}
	}
	return ebiten.NewImageFromImage(img)
}

func clamp(v, lo, hi float64) float64 {
	if v < lo {
		return lo
	}
	if v > hi {
		return hi
	}
	return v
}

func sign(x float64) float64 {
	if x < 0 {
		return -1
	}
	return 1
}

// ------- Game methods -------

func NewGame() *Game {
	rand.Seed(time.Now().UnixNano())

	goalTop := (float64(screenH)-goalMouthH)/2.0
	goalBottom := goalTop + goalMouthH

	b := Ball{
		Pos:    Vec{X: screenW / 2, Y: screenH / 2},
		Vel:    Vec{X: 0, Y: 0},
		Img:    makeCircleImage(int(2*ballRadius), color.White),
		Radius: ballRadius,
	}

	p1 := Paddle{
		Pos:      Vec{X: fieldMargin + 30, Y: screenH/2 - paddleH/2},
		Width:    paddleW,
		Height:   paddleH,
		Color:    color.RGBA{230, 57, 70, 255},
		IsAI:     false,
		UpKey:    ebiten.KeyW, DownKey: ebiten.KeyS, LeftKey: ebiten.KeyA, RightKey: ebiten.KeyD,
		MaxSpeed: p1Speed,
	}

	p2 := Paddle{
		Pos:      Vec{X: float64(screenW) - fieldMargin - 30 - paddleW, Y: screenH/2 - paddleH/2},
		Width:    paddleW,
		Height:   paddleH,
		Color:    color.RGBA{69, 123, 157, 255},
		IsAI:     true, // default lawan AI
		UpKey:    ebiten.KeyArrowUp, DownKey: ebiten.KeyArrowDown, LeftKey: ebiten.KeyArrowLeft, RightKey: ebiten.KeyArrowRight,
		MaxSpeed: p2SpeedAI,
	}

	g := &Game{
		ball:        b,
		p1:          p1,
		p2:          p2,
		goalTop:     goalTop,
		goalBottom:  goalBottom,
	}
	g.kickoff(0)
	return g
}

func (g *Game) kickoff(dir int) {
	// dir: -1 ke kiri, +1 ke kanan, 0 random
	g.ball.Pos = Vec{X: screenW / 2, Y: screenH / 2}
	angle := (rand.Float64()*0.6 - 0.3) // -0.3..0.3 rad sekitar horizontal
	speed := 6.5 + rand.Float64()*1.5   // 6.5..8.0
	direction := float64([]int{-1, 1}[rand.Intn(2)])
	if dir != 0 {
		direction = float64(dir)
	}
	g.ball.Vel.X = math.Cos(angle) * speed * direction
	g.ball.Vel.Y = math.Sin(angle) * speed
}

func (g *Game) Update() error {
	// Toggle AI dengan Tab (debounce sederhana)
	if g.toggleCooldown > 0 {
		g.toggleCooldown--
	}
	if ebiten.IsKeyPressed(ebiten.KeyTab) && g.toggleCooldown == 0 {
		g.p2.IsAI = !g.p2.IsAI
		if g.p2.IsAI {
			g.p2.MaxSpeed = p2SpeedAI
		} else {
			g.p2.MaxSpeed = p2Speed
		}
		g.toggleCooldown = 15 // ~0.25 detik pada 60FPS
	}

	// Reset kickoff
	if ebiten.IsKeyPressed(ebiten.KeySpace) {
		g.kickoff(0)
	}

	g.updatePaddle(&g.p1)
	g.updatePaddle(&g.p2)

	g.updateBall()

	return nil
}

func (g *Game) updatePaddle(p *Paddle) {
	if p.IsAI {
		// AI sederhana mengejar posisi Y bola
		targetY := g.ball.Pos.Y - p.Height/2
		if math.Abs(targetY-p.Pos.Y) > 4 {
			if targetY > p.Pos.Y {
				p.Pos.Y += p.MaxSpeed
			} else {
				p.Pos.Y -= p.MaxSpeed
			}
		}
		// batasi X AI agar tidak lewat garis kanan
	} else {
		// Player kontrol
		if ebiten.IsKeyPressed(p.UpKey) {
			p.Pos.Y -= p.MaxSpeed
		}
		if ebiten.IsKeyPressed(p.DownKey) {
			p.Pos.Y += p.MaxSpeed
		}
		if ebiten.IsKeyPressed(p.LeftKey) {
			p.Pos.X -= p.MaxSpeed
		}
		if ebiten.IsKeyPressed(p.RightKey) {
			p.Pos.X += p.MaxSpeed
		}
	}

	// batas lapangan
	minX := float64(fieldMargin)
	maxX := float64(screenW) - float64(fieldMargin) - p.Width
	p.Pos.X = clamp(p.Pos.X, minX, maxX)
	p.Pos.Y = clamp(p.Pos.Y, float64(fieldMargin), float64(screenH)-float64(fieldMargin)-p.Height)
}

func (g *Game) updateBall() {
	// gerak
	g.ball.Pos.X += g.ball.Vel.X
	g.ball.Pos.Y += g.ball.Vel.Y

	// gesekan kecil agar tidak terlalu liar
	g.ball.Vel.X *= friction
	g.ball.Vel.Y *= friction

	// batas atas/bawah (papan memantul)
	top := float64(fieldMargin)
	bottom := float64(screenH - fieldMargin)
	if g.ball.Pos.Y-g.ball.Radius < top {
		g.ball.Pos.Y = top + g.ball.Radius
		g.ball.Vel.Y = math.Abs(g.ball.Vel.Y)
	}
	if g.ball.Pos.Y+g.ball.Radius > bottom {
		g.ball.Pos.Y = bottom - g.ball.Radius
		g.ball.Vel.Y = -math.Abs(g.ball.Vel.Y)
	}

	// cek gol kiri/kanan
	if g.ball.Pos.X-g.ball.Radius < float64(fieldMargin) {
		// di area kiri: gol jika Y berada dalam mulut gawang
		if g.ball.Pos.Y >= g.goalTop && g.ball.Pos.Y <= g.goalBottom {
			// GOL untuk kanan
			g.scoreR++
			g.kickoff(1) // servis ke kanan
			return
		}
		// kalau tidak, mantul dinding kiri
		g.ball.Pos.X = float64(fieldMargin) + g.ball.Radius
		g.ball.Vel.X = math.Abs(g.ball.Vel.X)
	}

	if g.ball.Pos.X+g.ball.Radius > float64(screenW-fieldMargin) {
		// di area kanan
		if g.ball.Pos.Y >= g.goalTop && g.ball.Pos.Y <= g.goalBottom {
			// GOL untuk kiri
			g.scoreL++
			g.kickoff(-1) // servis ke kiri
			return
		}
		// mantul dinding kanan
		g.ball.Pos.X = float64(screenW-fieldMargin) - g.ball.Radius
		g.ball.Vel.X = -math.Abs(g.ball.Vel.X)
	}

	// tabrakan dengan paddle
	g.handlePaddleCollision(&g.p1)
	g.handlePaddleCollision(&g.p2)

	// jaga agar kecepatan tidak kebablasan
	spd := math.Hypot(g.ball.Vel.X, g.ball.Vel.Y)
	if spd > maxBallSpd {
		scale := maxBallSpd / spd
		g.ball.Vel.X *= scale
		g.ball.Vel.Y *= scale
	}
}

func (g *Game) handlePaddleCollision(p *Paddle) {
	// cek collision lingkaran (bola) vs AABB (paddle)
	cx, cy, r := g.ball.Pos.X, g.ball.Pos.Y, g.ball.Radius
	rx, ry := p.Pos.X, p.Pos.Y
	rw, rh := p.Width, p.Height

	closestX := clamp(cx, rx, rx+rw)
	closestY := clamp(cy, ry, ry+rh)
	dx := cx - closestX
	dy := cy - closestY

	if dx*dx+dy*dy <= r*r {
		// tentukan arah pantul berdasarkan posisi relatif
		// dorong bola keluar sedikit agar tidak "nempel"
		if math.Abs(dx) > math.Abs(dy) {
			// tabrak sisi kiri/kanan
			if cx < rx {
				g.ball.Pos.X = rx - r - 0.1
				g.ball.Vel.X = -math.Abs(g.ball.Vel.X)
			} else {
				g.ball.Pos.X = rx + rw + r + 0.1
				g.ball.Vel.X = math.Abs(g.ball.Vel.X)
			}
		} else {
			// tabrak sisi atas/bawah
			if cy < ry {
				g.ball.Pos.Y = ry - r - 0.1
				g.ball.Vel.Y = -math.Abs(g.ball.Vel.Y)
			} else {
				g.ball.Pos.Y = ry + rh + r + 0.1
				g.ball.Vel.Y = math.Abs(g.ball.Vel.Y)
			}
		}
		// beri efek putaran berdasar titik kontak vertikal
		impact := ((cy - (ry + rh/2)) / (rh / 2))
		g.ball.Vel.Y += impact * 2.2
		// sedikit percepat setiap kena paddle
		g.ball.Vel.X *= 1.05
		g.ball.Vel.Y *= 1.03
	}
}

func (g *Game) Draw(screen *ebiten.Image) {
	// latar lapangan
	screen.Fill(color.RGBA{34, 139, 34, 255}) // hijau rumput

	// area dalam lapangan
	playLeft := float64(fieldMargin)
	playTop := float64(fieldMargin)
	playRight := float64(screenW - fieldMargin)
	playBottom := float64(screenH - fieldMargin)

	white := color.RGBA{240, 240, 240, 255}

	// garis tepi
	ebitenutil.DrawRect(screen, playLeft, playTop, playRight-playLeft, 3, white)    // top
	ebitenutil.DrawRect(screen, playLeft, playBottom-3, playRight-playLeft, 3, white) // bottom
	ebitenutil.DrawRect(screen, playLeft, playTop, 3, playBottom-playTop, white)      // left
	ebitenutil.DrawRect(screen, playRight-3, playTop, 3, playBottom-playTop, white)   // right

	// garis tengah
	ebitenutil.DrawRect(screen, (playLeft+playRight)/2-2, playTop, 4, playBottom-playTop, white)

	// mulut gawang (garis vertikal tipis + kotak gawang)
	// Kiri
	ebitenutil.DrawRect(screen, playLeft-1, g.goalTop, goalWidth, float64(goalMouthH), white)
	// Kanan
	ebitenutil.DrawRect(screen, playRight-goalWidth, g.goalTop, goalWidth, float64(goalMouthH), white)

	// bola
	op := &ebiten.DrawImageOptions{}
	op.GeoM.Translate(g.ball.Pos.X-g.ball.Radius, g.ball.Pos.Y-g.ball.Radius)
	screen.DrawImage(g.ball.Img, op)

	// paddles
	drawPaddle := func(p *Paddle) {
		ebitenutil.DrawRect(screen, p.Pos.X, p.Pos.Y, p.Width, p.Height, p.Color)
	}
	drawPaddle(&g.p1)
	drawPaddle(&g.p2)

	// skor & UI
	ebitenutil.DebugPrintAt(screen, fmt.Sprintf("Skor: %d - %d", g.scoreL, g.scoreR), screenW/2-40, 10)
	mode := "AI"
	if !g.p2.IsAI {
		mode = "2P"
	}
	ebitenutil.DebugPrintAt(screen, fmt.Sprintf("[Tab] Lawan: %s  |  [Space] Kickoff", mode), 10, screenH-24)
}

func (g *Game) Layout(outsideWidth, outsideHeight int) (int, int) {
	return screenW, screenH
}

func main() {
	ebiten.SetWindowTitle("Game Bola (Go + Ebiten)")
	ebiten.SetWindowResizingMode(ebiten.WindowResizingModeEnabled)
	ebiten.SetWindowSize(screenW/2, screenH/2)

	game := NewGame()
	if err := ebiten.RunGame(game); err != nil {
		panic(err)
	}
}￼Enter			}
		}
	}
	return ebiten.NewImageFromImage(img)
}

func clamp(v, lo, hi float64) float64 {
	if v < lo {
		return lo
	}
	if v > hi {
		return hi
	}
	return v
}

func sign(x float64) float64 {
	if x < 0 {
		return -1
	}
	return 1
}

// ------- Game methods -------

func NewGame() *Game {
	rand.Seed(time.Now().UnixNano())

	goalTop := (float64(screenH)-goalMouthH)/2.0
	goalBottom := goalTop + goalMouthH

	b := Ball{
		Pos:    Vec{X: screenW / 2, Y: screenH / 2},
		Vel:    Vec{X: 0, Y: 0},
		Img:    makeCircleImage(int(2*ballRadius), color.White),
		Radius: ballRadius,
	}

	p1 := Paddle{
		Pos:      Vec{X: fieldMargin + 30, Y: screenH/2 - paddleH/2},
		Width:    paddleW,
		Height:   paddleH,
		Color:    color.RGBA{230, 57, 70, 255},
		IsAI:     false,
		UpKey:    ebiten.KeyW, DownKey: ebiten.KeyS, LeftKey: ebiten.KeyA, RightKey: ebiten.KeyD,
		MaxSpeed: p1Speed,
	}

	p2 := Paddle{
		Pos:      Vec{X: float64(screenW) - fieldMargin - 30 - paddleW, Y: screenH/2 - paddleH/2},
		Width:    paddleW,
		Height:   paddleH,
		Color:    color.RGBA{69, 123, 157, 255},
		IsAI:     true, // default lawan AI
		UpKey:    ebiten.KeyArrowUp, DownKey: ebiten.KeyArrowDown, LeftKey: ebiten.KeyArrowLeft, RightKey: ebiten.KeyArrowRight,
		MaxSpeed: p2SpeedAI,
	}

	g := &Game{
		ball:        b,
		p1:          p1,
		p2:          p2,
		goalTop:     goalTop,
		goalBottom:  goalBottom,
	}
	g.kickoff(0)
	return g
}

func (g *Game) kickoff(dir int) {
	// dir: -1 ke kiri, +1 ke kanan, 0 random
	g.ball.Pos = Vec{X: screenW / 2, Y: screenH / 2}
	angle := (rand.Float64()*0.6 - 0.3) // -0.3..0.3 rad sekitar horizontal
	speed := 6.5 + rand.Float64()*1.5   // 6.5..8.0
	direction := float64([]int{-1, 1}[rand.Intn(2)])
	if dir != 0 {
		direction = float64(dir)
	}
	g.ball.Vel.X = math.Cos(angle) * speed * direction
	g.ball.Vel.Y = math.Sin(angle) * speed
}

func (g *Game) Update() error {
	// Toggle AI dengan Tab (debounce sederhana)
	if g.toggleCooldown > 0 {
		g.toggleCooldown--
	}
	if ebiten.IsKeyPressed(ebiten.KeyTab) && g.toggleCooldown == 0 {
		g.p2.IsAI = !g.p2.IsAI
		if g.p2.IsAI {
			g.p2.MaxSpeed = p2SpeedAI
		} else {
			g.p2.MaxSpeed = p2Speed
		}
		g.toggleCooldown = 15 // ~0.25 detik pada 60FPS
	}

	// Reset kickoff
	if ebiten.IsKeyPressed(ebiten.KeySpace) {
		g.kickoff(0)
	}

	g.updatePaddle(&g.p1)
atePaddle(&g.p2)

	g.updateBall()

	return nil
}

func (g *Game) updatePaddle(p *Paddle) {
	if p.IsAI {
		// AI sederhana mengejar posisi Y bola
		targetY := g.ball.Pos.Y - p.Height/2
		if math.Abs(targetY-p.Pos.Y) > 4 {
			if targetY > p.Pos.Y {
				p.Pos.Y += p.MaxSpeed
			} else {
				p.Pos.Y -= p.MaxSpeed
			}
		}
		// batasi X AI agar tidak lewat garis kanan
	} else {
		// Player kontrol
		if ebiten.IsKeyPressed(p.UpKey) {
			p.Pos.Y -= p.MaxSpeed
		}
		if ebiten.IsKeyPressed(p.DownKey) {
			p.Pos.Y += p.MaxSpeed
		}
		if ebiten.IsKeyPressed(p.LeftKey) {
			p.Pos.X -= p.MaxSpeed
		}
		if ebiten.IsKeyPressed(p.RightKey) {
			p.Pos.X += p.MaxSpeed
		}
	}

	// batas lapangan
	minX := float64(fieldMargin)
	maxX := float64(screenW) - float64(fieldMargin) - p.Width
	p.Pos.X = clamp(p.Pos.X, minX, maxX)
	p.Pos.Y = clamp(p.Pos.Y, float64(fieldMargin), float64(screenH)-float64(fieldMargin)-p.Height)
}

func (g *Game) updateBall() {
	// gerak
	g.ball.Pos.X += g.ball.Vel.X
	g.ball.Pos.Y += g.ball.Vel.Y

	// gesekan kecil agar tidak terlalu liar
	g.ball.Vel.X *= friction
	g.ball.Vel.Y *= friction

	// batas atas/bawah (papan memantul)
	top := float64(fieldMargin)
	bottom := float64(screenH - fieldMargin)
	if g.ball.Pos.Y-g.ball.Radius < top {
		g.ball.Pos.Y = top + g.ball.Radius
		g.ball.Vel.Y = math.Abs(g.ball.Vel.Y)
	}
	if g.ball.Pos.Y+g.ball.Radius > bottom {
		g.ball.Pos.Y = bottom - g.ball.Radius
		g.ball.Vel.Y = -math.Abs(g.ball.Vel.Y)
	}

	// cek gol kiri/kanan
	if g.ball.Pos.X-g.ball.Radius < float64(fieldMargin) {
		// di area kiri: gol jika Y berada dalam mulut gawang
		if g.ball.Pos.Y >= g.goalTop && g.ball.Pos.Y <= g.goalBottom {
			// GOL untuk kanan
			g.scoreR++
			g.kickoff(1) // servis ke kanan
			return
		}
		// kalau tidak, mantul dinding kiri
		g.ball.Pos.X = float64(fieldMargin) + g.ball.Radius
		g.ball.Vel.X = math.Abs(g.ball.Vel.X)
	}

	if g.ball.Pos.X+g.ball.Radius > float64(screenW-fieldMargin) {
		// di area kanan
		if g.ball.Pos.Y >= g.goalTop && g.ball.Pos.Y <= g.goalBottom {
			// GOL untuk kiri
			g.scoreL++
			g.kickoff(-1) // servis ke kiri
			return
		}
		// mantul dinding kanan
		g.ball.Pos.X = float64(screenW-fieldMargin) - g.ball.Radius
		g.ball.Vel.X = -math.Abs(g.ball.Vel.X)
	}

	// tabrakan dengan paddle
	g.handlePaddleCollision(&g.p1)
	g.handlePaddleCollision(&g.p2)

	// jaga agar kecepatan tidak kebablasan
	spd := math.Hypot(g.ball.Vel.X, g.ball.Vel.Y)
	if spd > maxBallSpd {
		scale := maxBallSpd / spd
		g.ball.Vel.X *= scale
		g.ball.Vel.Y *= scale
	}
}

