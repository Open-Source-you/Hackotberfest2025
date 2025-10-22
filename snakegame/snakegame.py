import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 100, 255)
PURPLE = (200, 0, 200)
CYAN = (0, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 SNAKE MASTER GAME 🐍")
clock = pygame.time.Clock()
font_small = pygame.font.Font(None, 24)
font_large = pygame.font.Font(None, 48)

class SnakeGame:
    def __init__(self):
        self.reset_game()
        self.high_score = 0
        self.level = 1
        self.speed = 8
        self.game_over = False
    
    def reset_game(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.food = self.spawn_food()
        self.special_food = None
        self.special_food_timer = 0
        self.score = 0
        self.game_over = False
        self.food_eaten_count = 0
    
    def spawn_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake:
                return food
    
    def spawn_special_food(self):
        if self.special_food is None and random.random() < 0.02:
            while True:
                special = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                if special not in self.snake and special != self.food:
                    self.special_food = special
                    self.special_food_timer = 200
                    break
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction[1] == 0:
                    self.next_direction = (0, -1)
                elif event.key == pygame.K_DOWN and self.direction[1] == 0:
                    self.next_direction = (0, 1)
                elif event.key == pygame.K_LEFT and self.direction[0] == 0:
                    self.next_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and self.direction[0] == 0:
                    self.next_direction = (1, 0)
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True
    
    def update(self):
        if self.game_over:
            return
        
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or 
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or 
            new_head in self.snake):
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
            return
        
        self.snake.insert(0, new_head)
        
        if new_head == self.food:
            self.score += 10
            self.food_eaten_count += 1
            self.food = self.spawn_food()
            if self.food_eaten_count % 5 == 0:
                self.speed = min(15, self.speed + 1)
                self.level += 1
        else:
            self.snake.pop()
        
        if self.special_food:
            if new_head == self.special_food:
                self.score += 50
                self.special_food = None
            else:
                self.special_food_timer -= 1
                if self.special_food_timer <= 0:
                    self.special_food = None
        
        self.spawn_special_food()
    
    def draw(self):
        screen.fill(BLACK)
        
        for i, (x, y) in enumerate(self.snake):
            color = GREEN if i == 0 else CYAN
            pygame.draw.rect(screen, color, (x * GRID_SIZE + 1, y * GRID_SIZE + 1, 
                                             GRID_SIZE - 2, GRID_SIZE - 2))
        
        if self.food:
            pygame.draw.rect(screen, RED, (self.food[0] * GRID_SIZE + 1, 
                                          self.food[1] * GRID_SIZE + 1, 
                                          GRID_SIZE - 2, GRID_SIZE - 2))
        
        if self.special_food:
            color = YELLOW if self.special_food_timer % 20 < 10 else PURPLE
            pygame.draw.rect(screen, color, (self.special_food[0] * GRID_SIZE + 1, 
                                            self.special_food[1] * GRID_SIZE + 1, 
                                            GRID_SIZE - 2, GRID_SIZE - 2))
        
        score_text = font_small.render(f"Score: {self.score} | Level: {self.level} | High: {self.high_score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        speed_text = font_small.render(f"Speed: {self.speed} | Length: {len(self.snake)}", True, CYAN)
        screen.blit(speed_text, (10, 35))
        
        if self.game_over:
            game_over_text = font_large.render("GAME OVER!", True, RED)
            restart_text = font_small.render("Press SPACE to restart or ESC to quit", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - 180, HEIGHT // 2 - 50))
            screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 50))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            clock.tick(self.speed)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()