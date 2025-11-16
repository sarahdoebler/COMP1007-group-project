from board import Board
from ball import update_ball, create_ball, increase_all_balls_speed
import pygame
import time
from stickMan import StickMan
from menu import show_start_screen

try:
    from menu import show_start_screen
    has_menu = True
except ImportError:
    has_menu = False
    print("Menu module not found - skipping start screen")

def show_countdown(screen, width, height):
    font = pygame.font.Font(None, 150)
    for i in range(3, 0, -1):
        screen.fill((0, 0, 0))  
        
        text = font.render(str(i), True, (255, 255, 255))
        text_rect = text.get_rect(center=(width/2, height/2))
        screen.blit(text, text_rect)
        
        pygame.display.flip()
        pygame.time.wait(1000)  
        
def show_level_complete(screen, width, height, level):
    font_big = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 36)
    
    screen.fill((0, 0, 0))
    
    text1 = font_big.render(f"Level {level} Complete!", True, (0, 255, 0))
    text1_rect = text1.get_rect(center=(width/2, height/2 - 50))
    screen.blit(text1, text1_rect)
    
    text2 = font_small.render(f"Starting Level {level + 1}...", True, (255, 255, 255))
    text2_rect = text2.get_rect(center=(width/2, height/2 + 20))
    screen.blit(text2, text2_rect)
    
    pygame.display.flip()
    pygame.time.wait(2000) 
             
def format_time(seconds):
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes}:{remaining_seconds:02d}"

def draw_hearts(screen, x, y, lives, max_lives=3):
    heart_size = 15
    spacing = 30
    
    for i in range(max_lives):
        heart_x = x + i * spacing
        if i < lives:
            color = (255, 0, 0) 
        else:
            color = (100, 100, 100)  
        
        pygame.draw.circle(screen, color, (heart_x - 5, y), heart_size // 2)
        pygame.draw.circle(screen, color, (heart_x + 5, y), heart_size // 2)
        points = [
            (heart_x - 10, y + 5),
            (heart_x + 10, y + 5),
            (heart_x, y + 15)
        ]
        pygame.draw.polygon(screen, color, points)

def get_level_parameters(level):
    level_params = {
        1: {"duration": 60, "ball_spawn_interval": 12, "max_balls": 5, "speed_increase": 0.1},
        2: {"duration": 60, "ball_spawn_interval": 10, "max_balls": 6, "speed_increase": 0.2},
        3: {"duration": 60, "ball_spawn_interval": 8, "max_balls": 7, "speed_increase": 0.3},
        4: {"duration": 60, "ball_spawn_interval": 6, "max_balls": 7, "speed_increase": 0.4},
        5: {"duration": 60, "ball_spawn_interval": 5, "max_balls": 7, "speed_increase": 0.5}
    }
    return level_params.get(level, level_params[5]) 
        
def main():
    board = Board()
    clock = pygame.time.Clock()
    if has_menu:
        if not show_start_screen(board.screen, board.WIDTH, board.HEIGHT):
            return
    show_countdown(board.screen, board.WIDTH, board.HEIGHT)
    current_level = 1
    level_params = get_level_parameters(current_level)
    level_start_time = time.time()
    stick_man = StickMan(board.WIDTH // 2, board.HEIGHT - 50, board.WIDTH)
    balls = [create_ball(board.WIDTH)]  
    lives = 3
    last_ball_time = time.time()
 
    game_over = False
    game_won = False
    
    running = True
    while running:
        current_time = time.time()
        level_elapsed_time = current_time - level_start_time
        time_remaining = max(0, level_params["duration"] - level_elapsed_time)
        if time_remaining <= 0 and not game_over and not game_won:
            if current_level < 5:
                show_level_complete(board.screen, board.WIDTH, board.HEIGHT, current_level)
                current_level += 1
                lives = 3
                level_params = get_level_parameters(current_level)
                level_start_time = time.time()
                
                balls = [create_ball(board.WIDTH)]
                last_ball_time = time.time()
            else:
                game_won = True
                print("CONGRATULATION! ALL LEVELS COMPLETED!")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            stick_man.move_left()
        elif keys[pygame.K_d]:
            stick_man.move_right()
        else:
            stick_man.stop()
        
        stick_man.update()
        
        if (current_time - last_ball_time >= level_params["ball_spawn_interval"] and 
            len(balls) < level_params["max_balls"] and not game_over and not game_won):
            balls.append(create_ball(board.WIDTH))
            last_ball_time = current_time
            balls = increase_all_balls_speed(balls, level_params["speed_increase"])
        
        board.draw()
        font = pygame.font.Font(None, 36)
        time_text = font.render(f"Time: {format_time(time_remaining)}", True, (255, 255, 255))
        level_text = font.render(f"Level: {current_level}", True, (255, 255, 255))

        board.screen.blit(time_text, (10, 10))
        board.screen.blit(level_text, (10, 50))

        draw_hearts(board.screen, board.WIDTH - 120, 30, lives)
        
        stick_man.draw(board.screen)
        
        active_balls = []
        balls_lost_this_frame = 0
        
        for ball in balls:
            updated_ball = update_ball(ball, board.WIDTH, board.HEIGHT, board.screen, stick_man)
            if updated_ball is not None:
                active_balls.append(updated_ball)
            else:
                balls_lost_this_frame += 1
        
        balls = active_balls
        
        if balls_lost_this_frame > 0:
            lives -= balls_lost_this_frame
            if lives <= 0 and not game_won:
                game_over = True
                print("Game Over!")
        
        if game_over or game_won:
            font = pygame.font.Font(None, 74)
            if game_over:
                text = font.render("GAME OVER", True, (255, 0, 0))
            else:
                text = font.render("YOU WIN!", True, (0, 255, 0))
            
            text_rect = text.get_rect(center=(board.WIDTH/2, board.HEIGHT/2))
            board.screen.blit(text, text_rect)
            pygame.display.flip() 
            pygame.time.wait(3000)  
            running = False
            
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()