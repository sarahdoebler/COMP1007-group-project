from board import Board
from ball import update_ball, create_ball, increase_all_balls_speed
import pygame
import time
import sys
import math

# Stick man class
class StickMan:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.direction = 1  # 1 for right, -1 for left
        
        # Body parts size
        self.head_radius = 20
        self.body_length = 40
        self.arm_length = 30
        self.leg_length = 40
        
        # Animation
        self.walking = False
        self.walk_pattern = 0
        self.walk_speed = 0.2
    
    def move_left(self):
        self.x -= self.speed
        self.direction = -1
        self.walking = True
    
    def move_right(self):
        self.x += self.speed
        self.direction = 1
        self.walking = True
    
    def stop(self):
        self.walking = False
    
    def update(self):
        # Update animation if walking
        if self.walking:
            self.walk_pattern += self.walk_speed
        
        # Keep stick man within screen bounds
        self.x = max(self.head_radius, min(WIDTH - self.head_radius, self.x))
    
    def draw(self, surface):
        # Head
        pygame.draw.circle(surface, BLACK, (self.x, self.y - self.body_length - self.head_radius), self.head_radius)
        
        # Body
        body_top = (self.x, self.y - self.body_length)
        body_bottom = (self.x, self.y)
        pygame.draw.line(surface, BLACK, body_top, body_bottom, 4)
        
        # Calculation of hand position's animation
        if self.walking:
            # Hands opposite to legs swing
            left_hand_angle = math.pi/4 + math.sin(self.walk_pattern) * 0.4
            right_hand_angle = math.pi/4 - math.sin(self.walk_pattern) * 0.4
        else:
            left_hand_angle = math.pi/4
            right_hand_angle = math.pi/4
        
        # Adjust arms based on direction
        if self.direction == 1:  # Facing right
            left_hand_end = (
                self.x - math.cos(left_hand_angle) * self.arm_length,
                self.y - self.body_length + math.sin(left_hand_angle) * self.arm_length
            )
            right_hand_end = (
                self.x + math.cos(right_hand_angle) * self.arm_length,
                self.y - self.body_length + math.sin(right_hand_angle) * self.arm_length
            )
        else:  # Facing left
            left_hand_end = (
                self.x - math.cos(left_hand_angle) * self.arm_length,
                self.y - self.body_length + math.sin(left_hand_angle) * self.arm_length
            )
            right_hand_end = (
                self.x + math.cos(right_hand_angle) * self.arm_length,
                self.y - self.body_length + math.sin(right_hand_angle) * self.arm_length
            )
        
        # Hands drawing
        pygame.draw.line(surface, BLACK, body_top, left_hand_end, 3)
        pygame.draw.line(surface, BLACK, body_top, right_hand_end, 3)
        
        # Calculation of leg position's animation
        if self.walking:
            left_leg_angle = math.pi/6 + math.sin(self.walk_pattern) * 0.3
            right_leg_angle = math.pi/6 - math.sin(self.walk_pattern) * 0.3
        else:
            left_leg_angle = math.pi/6
            right_leg_angle = math.pi/6
        
        # Direction adjustment of legs
        if self.direction == 1:  # Facing right
            left_leg_end = (
                self.x - math.cos(left_leg_angle) * self.leg_length,
                self.y + math.sin(left_leg_angle) * self.leg_length
            )
            right_leg_end = (
                self.x + math.cos(right_leg_angle) * self.leg_length,
                self.y + math.sin(right_leg_angle) * self.leg_length
            )
        else:  # Facing left
            left_leg_end = (
                self.x - math.cos(left_leg_angle) * self.leg_length,
                self.y + math.sin(left_leg_angle) * self.leg_length
            )
            right_leg_end = (
                self.x + math.cos(right_leg_angle) * self.leg_length,
                self.y + math.sin(right_leg_angle) * self.leg_length
            )
        
        # Draw legs
        pygame.draw.line(surface, BLACK, body_bottom, left_leg_end, 3)
        pygame.draw.line(surface, BLACK, body_bottom, right_leg_end, 3)
        
# Create stick man
    stick_man = StickMan(WIDTH // 2, HEIGHT - 100)
    
    balls = [create_ball(board.WIDTH)]  
    max_balls = 5  
    ball_spawn_interval = 15  
    last_ball_time = time.time()
    game_start_time = time.time()
    game_duration = 60  
    game_over = False
    game_won = False
    
    running = True
    while running:
        current_time = time.time()
        elapsed_time = current_time - game_start_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Handle keyboard input for character movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            stick_man.move_left()
        elif keys[pygame.K_d]:
            stick_man.move_right()
        else:
            stick_man.stop()
            
        # Update stick man
        stick_man.update()

def show_countdown(screen, width, height):
    font = pygame.font.Font(None, 150)
    for i in range(3, 0, -1):
        screen.fill((0, 0, 0))  
        
        text = font.render(str(i), True, (255, 255, 255))
        text_rect = text.get_rect(center=(width/2, height/2))
        screen.blit(text, text_rect)
        
        pygame.display.flip()
        pygame.time.wait(1000)  
        
def main():
    board = Board()
    clock = pygame.time.Clock()
    show_countdown(board.screen, board.WIDTH, board.HEIGHT)
    
    balls = [create_ball(board.WIDTH)]  
    max_balls = 5  
    ball_spawn_interval = 15  
    last_ball_time = time.time()
    game_start_time = time.time()
    game_duration = 60  
    game_over = False
    game_won = False
    
    running = True
    while running:
        current_time = time.time()
        elapsed_time = current_time - game_start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if (current_time - last_ball_time >= ball_spawn_interval and 
            len(balls) < max_balls and not game_over and not game_won):
            balls.append(create_ball(board.WIDTH))
            last_ball_time = current_time
            balls = increase_all_balls_speed(balls, 0.2)
        
        board.draw()
        
        
        active_balls = []
        for ball in balls:
            updated_ball = update_ball(ball, board.WIDTH, board.HEIGHT, board.screen)
            if updated_ball is not None:
                active_balls.append(updated_ball)
            else:
                if not game_won:
                    game_over = True
                    print("Game Over!")
        
        balls = active_balls
        
        if elapsed_time >= game_duration and not game_over:
            game_won = True
            print("CONGRATULATION! YOU PASSED!")
        
        if game_over or game_won:
            font = pygame.font.Font(None, 74)
            if game_over:
                text = font.render("GAME OVER", True, (255, 0, 0))
            else:
                text = font.render("WIN!", True, (0, 255, 0))
            
            text_rect = text.get_rect(center=(board.WIDTH/2, board.HEIGHT/2))
            board.screen.blit(text, text_rect)
            pygame.display.flip() 
            pygame.time.wait(3000)  
            running = False
            
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
