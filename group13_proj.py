import pygame
import random
import math
import time


class Board:
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 600
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Don't Let The Ball Drop")

    def draw(self):
        self.screen.fill((0, 0, 0))

class StickMan:
    def __init__(self, x, y, screen_width):
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.speed = 8
        self.direction = 1  # 1 for right, -1 for left
        
        # Body parts size
        self.head_radius = 10
        self.body_length = 17
        self.hand_length = 15
        self.leg_length = 20
        
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
        self.x = max(self.head_radius, min(self.screen_width - self.head_radius, self.x))
    
    def draw(self, surface):
        # Head
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y - self.body_length - self.head_radius), self.head_radius)
        
        # Body
        body_top = (self.x, self.y - self.body_length)
        body_bottom = (self.x, self.y)
        pygame.draw.line(surface, (255, 255, 255), body_top, body_bottom, 4)
        
        # Calculation of hand position's animation
        if self.walking:
            # Hands opposite to legs swing
            left_hand_angle = math.pi/4 + math.sin(self.walk_pattern) * 0.4
            right_hand_angle = math.pi/4 - math.sin(self.walk_pattern) * 0.4
        else:
            left_hand_angle = math.pi/4
            right_hand_angle = math.pi/4
        
        # Adjust hands based on direction
        if self.direction == 1:  # Facing right
            left_hand_end = (
                self.x - math.cos(left_hand_angle) * self.hand_length,
                self.y - self.body_length + math.sin(left_hand_angle) * self.hand_length
            )
            right_hand_end = (
                self.x + math.cos(right_hand_angle) * self.hand_length,
                self.y - self.body_length + math.sin(right_hand_angle) * self.hand_length
            )
        else:  # Facing left
            left_hand_end = (
                self.x - math.cos(left_hand_angle) * self.hand_length,
                self.y - self.body_length + math.sin(left_hand_angle) * self.hand_length
            )
            right_hand_end = (
                self.x + math.cos(right_hand_angle) * self.hand_length,
                self.y - self.body_length + math.sin(right_hand_angle) * self.hand_length
            )
        
        # Hands drawing
        pygame.draw.line(surface, (255, 255, 255), body_top, left_hand_end, 3)
        pygame.draw.line(surface, (255, 255, 255), body_top, right_hand_end, 3)
        
        # Calculation of leg position's animation
        if self.walking:
            left_leg_angle = math.pi/3 + math.sin(self.walk_pattern) * 0.3
            right_leg_angle = math.pi/3 - math.sin(self.walk_pattern) * 0.3
        else:
            left_leg_angle = math.pi/3
            right_leg_angle = math.pi/3
        
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
        pygame.draw.line(surface, (255, 255, 255), body_bottom, left_leg_end, 3)
        pygame.draw.line(surface, (255, 255, 255), body_bottom, right_leg_end, 3)

# === BALL FUNCTIONS ===
def create_ball(screen_width):
    angle_degrees = random.uniform(0,180)
    angle_radians = math.radians(angle_degrees)
    base_speed = 3
    ball = {
        'x': random.randint(20, screen_width - 20), 
        'y': 20,                                     
        'size': 8,                                  
        'color': '#FF6B6B',                          
        'speed_x': base_speed * math.cos(angle_radians),
        'speed_y': base_speed * math.sin(angle_radians),                                 
        'active': True, 
        'base_speed': base_speed,
        'speed_increase': 0,  
        'bounce_count': 0                             
    }
    return ball

def move_ball(ball, screen_width, screen_height, stick_man=None):
    total_speed = ball['base_speed'] + ball['speed_increase']
    
    current_magnitude = math.sqrt(ball['speed_x']**2 + ball['speed_y']**2)
    if current_magnitude > 0:
        direction_x = ball['speed_x'] / current_magnitude
        direction_y = ball['speed_y'] / current_magnitude
        
        ball['speed_x'] = direction_x * total_speed
        ball['speed_y'] = direction_y * total_speed

    ball['x'] += ball['speed_x']
    ball['y'] += ball['speed_y']
    
    if stick_man and check_collision(ball, stick_man):
        ball['speed_y'] = -abs(ball['speed_y'])  
        ball['bounce_count'] += 1

    if ball['x'] <= 0 or ball['x'] >= screen_width:
        ball['speed_x'] = -ball['speed_x']
        ball['bounce_count'] += 1

    if ball['y'] <= 0:
        ball['speed_y'] = -ball['speed_y']
        ball['bounce_count'] += 1

    if ball['bounce_count'] >= 5: 
        ball['speed_increase'] += 0.1  
        ball['bounce_count'] = 0

    if ball['y'] > screen_height:
        ball['active'] = False 
        
def check_collision(ball, stick_man):
    stickman_rect = pygame.Rect(
        stick_man.x - 25, 
        stick_man.y - 40, 
        50,               
        60                 
    )
    
    closest_x = max(stickman_rect.left, min(ball['x'], stickman_rect.right))
    closest_y = max(stickman_rect.top, min(ball['y'], stickman_rect.bottom))
    
    distance_x = ball['x'] - closest_x
    distance_y = ball['y'] - closest_y

    return (distance_x ** 2 + distance_y ** 2) <= (ball['size'] ** 2)

def draw_ball(ball, screen):
    if ball['active']:
        color = pygame.Color(ball['color'])
        pygame.draw.circle(screen, color, 
                          (int(ball['x']), int(ball['y'])), 
                          ball['size'])
    
def increase_all_balls_speed(balls, increase_amount):
    for ball in balls:
        ball['speed_increase'] += increase_amount
    return balls
        
def update_ball(ball, screen_width, screen_height, screen, stick_man=None):
    move_ball(ball, screen_width, screen_height, stick_man)
    
    if not ball['active']:
        return None 
    
    draw_ball(ball, screen)
    
    return ball

# === MENU FUNCTIONS ===
def show_start_screen(screen, width, height):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (100, 150, 255)
    
    title_font = pygame.font.Font(None, 80)
    instruction_font = pygame.font.Font(None, 25)
    start_font = pygame.font.Font(None, 50)
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: 
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
        
        screen.fill(BLACK)
        
        title = title_font.render("DON'T LET THE BALL DROP", True, BLUE)
        title_rect = title.get_rect(center=(width/2, height/4))
        screen.blit(title, title_rect)
        
        instructions = [
            "• Move character with A (left) and D (right)",
            "• Catch balls before they hit the ground", 
            "• Survive 60 seconds to win",
            "• Each new ball increases speed",
            "• Avoid letting any ball drop"
        ]
        
        y_pos = height/2 - 50
        for instruction in instructions:
            text = instruction_font.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(width/2, y_pos))
            screen.blit(text, text_rect)
            y_pos += 40
        
        start_text = start_font.render("Start the game!", True, WHITE)
        start_rect = start_text.get_rect(center=(width/2, height - 100))
        screen.blit(start_text, start_rect)
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    
    return True

# === GAME FUNCTIONS ===
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

def show_next_round_screen(screen, width, height, level):
    font_big = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 36)
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
        
        screen.fill((0, 0, 0))
        
        # Level Text
        text1 = font_big.render(f"Level {level}", True, (100, 150, 255))
        text1_rect = text1.get_rect(center=(width/2, height/2 - 50))
        screen.blit(text1, text1_rect)
        
        # Start-Anweisung
        text2 = font_small.render("Press ENTER or CLICK to start round", True, (255, 255, 255))
        text2_rect = text2.get_rect(center=(width/2, height/2 + 20))
        screen.blit(text2, text2_rect)
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    
    return True
             
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

# === MAIN GAME ===
def main():
    board = Board()
    clock = pygame.time.Clock()
    
    # Start screen
    if not show_start_screen(board.screen, board.WIDTH, board.HEIGHT):
        return
    
    show_countdown(board.screen, board.WIDTH, board.HEIGHT)
    
    # Level system
    current_level = 1
    level_params = get_level_parameters(current_level)
    level_start_time = time.time()
    
    stick_man = StickMan(board.WIDTH // 2, board.HEIGHT - 50, board.WIDTH)
    balls = [create_ball(board.WIDTH)]  
    
    # Lives system
    lives = 3
    last_ball_time = time.time()
    game_over = False
    game_won = False
    
    running = True
    while running:
        current_time = time.time()
        level_elapsed_time = current_time - level_start_time
        time_remaining = max(0, level_params["duration"] - level_elapsed_time)
        
        # Level completion check
        if time_remaining <= 0 and not game_over and not game_won:
            if current_level < 5:
                show_level_complete(board.screen, board.WIDTH, board.HEIGHT, current_level)
                current_level += 1
                
                # Reset lives for new level
                lives = 3
                level_params = get_level_parameters(current_level)
                
                if not show_next_round_screen(board.screen, board.WIDTH, board.HEIGHT, current_level):
                    return
                
                show_countdown(board.screen, board.WIDTH, board.HEIGHT)
                
                # Reset balls for new level
                balls = [create_ball(board.WIDTH)]
                last_ball_time = time.time()
                level_start_time = time.time()
            else:
                game_won = True
                print("CONGRATULATION! ALL LEVELS COMPLETED!")
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # StickMan controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            stick_man.move_left()
        elif keys[pygame.K_d]:
            stick_man.move_right()
        else:
            stick_man.stop()
        
        stick_man.update()
        
        # Ball creation
        if (current_time - last_ball_time >= level_params["ball_spawn_interval"] and 
            len(balls) < level_params["max_balls"] and not game_over and not game_won):
            balls.append(create_ball(board.WIDTH))
            last_ball_time = current_time
            balls = increase_all_balls_speed(balls, level_params["speed_increase"])
        
        # Drawing
        board.draw()
        font = pygame.font.Font(None, 36)
        time_text = font.render(f"Time: {format_time(time_remaining)}", True, (255, 255, 255))
        level_text = font.render(f"Level: {current_level}", True, (255, 255, 255))

        board.screen.blit(time_text, (10, 10))
        board.screen.blit(level_text, (10, 50))

        draw_hearts(board.screen, board.WIDTH - 120, 30, lives)
        
        stick_man.draw(board.screen)
        
        # Update balls
        active_balls = []
        balls_lost_this_frame = 0
        
        for ball in balls:
            updated_ball = update_ball(ball, board.WIDTH, board.HEIGHT, board.screen, stick_man)
            if updated_ball is not None:
                active_balls.append(updated_ball)
            else:
                balls_lost_this_frame += 1
        
        balls = active_balls
        
        # Lives system
        if balls_lost_this_frame > 0:
            lives -= balls_lost_this_frame
            if lives <= 0 and not game_won:
                game_over = True
                print("Game Over!")
        
        # Game end
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