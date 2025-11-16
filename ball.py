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

def move_ball(ball, screen_width, screen_height):
    total_speed = ball['base_speed'] + ball['speed_increase']
    
    current_magnitude = math.sqrt(ball['speed_x']**2 + ball['speed_y']**2)
    if current_magnitude > 0:
        direction_x = ball['speed_x'] / current_magnitude
        direction_y = ball['speed_y'] / current_magnitude
        
        ball['speed_x'] = direction_x * total_speed
        ball['speed_y'] = direction_y * total_speed

    ball['x'] += ball['speed_x']
    ball['y'] += ball['speed_y']

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
        
def update_ball(ball, screen_width, screen_height, screen):
    move_ball(ball, screen_width, screen_height)
    
    if not ball['active']:
        return None 
    
    draw_ball(ball, screen)
    
    return ball