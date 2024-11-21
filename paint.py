import pygame
import math
import figures

screen = pygame.display.set_mode((800,600))
another_layer = pygame.Surface((800, 600))

figures = figures.Figures()

is_draw = False
end_pos = (0, 0)
color = (255, 255, 255) # Start color
tool = 'pen'
radius = 4 # pen radius
screen.fill((0, 0, 0)) # Black background


def roundline(screen, color, start, end, r = 1):
    dx = end[0]-start[0]
    dy = end[1]-start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int( start[0]+float(i)/distance*dx)
        y = int( start[1]+float(i)/distance*dy)
        pygame.draw.circle(screen, color, (x, y), r)



while True:
    pressed = pygame.key.get_pressed() 

    if pressed[pygame.K_r]:
        color = (255, 0, 0)     # Red
        
    elif pressed[pygame.K_b]:
        color = (0, 0, 255)     # Blue
        
    elif pressed[pygame.K_g]:
        color = (0, 255, 0)     # Green
        
    elif pressed[pygame.K_y]:
        color = (255, 255, 0)   # Yellow

    elif pressed[pygame.K_w]: 
        color = (255, 255, 255) # White

    #tools of draw

    if pressed[pygame.K_1]:
         tool = 'pen'
    if pressed[pygame.K_2]:
         tool = 'circle' 
    if pressed[pygame.K_3]:
         tool = 'rect'  
    if pressed[pygame.K_4]:
         tool = 'triangle'
    if pressed[pygame.K_5]:
         tool = 'equilateral triangle'
    if pressed[pygame.K_6]:
         tool = 'rhombus'
    if pressed[pygame.K_7]:
         tool = 'erasor'

    
    for event in pygame.event.get():
 
        if tool == 'rect': 
            figures.draw_rectangle(event, screen, another_layer, color)

        if tool == 'circle': 
            figures.draw_circle(event, screen, another_layer, color)

        if tool == 'triangle': 
            figures.draw_triangle(event, screen, another_layer, color)

        if tool == 'equilateral triangle': 
            figures.draw_equilateral_triangle(event, screen, another_layer, color)

        if tool == 'rhombus': 
            figures.draw_rhombus(event, screen, another_layer, color)

        if tool == 'erasor':
            figures.erasor(event, screen, another_layer)
        



        if event.type == pygame.QUIT: # close the paint
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN and tool == 'pen':
            pygame.draw.circle(screen, color, event.pos, radius)
            is_draw = True

        elif event.type == pygame.MOUSEBUTTONUP:
            is_draw = False

        elif event.type == pygame.MOUSEMOTION:
            if is_draw :
                pygame.draw.circle(another_layer, color, event.pos, radius)
                screen.blit(another_layer, (0, 0))
                if tool == 'pen':
                    roundline(another_layer, color, event.pos, end_pos, radius)

            end_pos = event.pos
    pygame.display.update()