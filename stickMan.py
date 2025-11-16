import pygame
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# Stick man appearence
class StickMan:
    def __init__(self, x, y, screen_width):
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.speed = 5
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
        pygame.draw.circle(surface, WHITE, (self.x, self.y - self.body_length - self.head_radius), self.head_radius)
        
        # Body
        body_top = (self.x, self.y - self.body_length)
        body_bottom = (self.x, self.y)
        pygame.draw.line(surface, WHITE, body_top, body_bottom, 4)
        
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
        
        # Hands drawuing
        pygame.draw.line(surface, WHITE, body_top, left_hand_end, 3)
        pygame.draw.line(surface, WHITE, body_top, right_hand_end, 3)
        
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
        pygame.draw.line(surface, WHITE, body_bottom, left_leg_end, 3)
        pygame.draw.line(surface, WHITE, body_bottom, right_leg_end, 3)
        


