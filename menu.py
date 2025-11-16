import pygame

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