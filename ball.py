import pygame
import random
import math

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
        stick_man.y - 80, 
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