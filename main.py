from board import Board
from ball import update_ball, create_ball, increase_all_balls_speed
import pygame
import time
#from stickMan import StickMan

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

if __name__ == "__main__":
    main()


        
   