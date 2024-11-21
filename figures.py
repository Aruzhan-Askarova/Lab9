import pygame
import math

class Figures:
    def __init__(self):
        self.x1 = 10
        self.y1 = 10
        self.x2 = 10
        self.y2 = 10
        self.isMouseDown = False
        self.erase_color = (0, 0, 0)

    def draw(self, event, screen, another_layer):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                self.x1, self.y1 = event.pos
                self.isMouseDown = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.isMouseDown = False
                another_layer.blit(screen, (0, 0))

    def draw_rectangle(self, event, screen, another_layer, color):
        self.draw(event, screen, another_layer)

        if event.type == pygame.MOUSEMOTION:
            if self.isMouseDown:
                self.x2, self.y2 = event.pos
                screen.blit(another_layer, (0, 0))  
                pygame.draw.rect(screen, color, pygame.Rect(*self.getRectangle()), 3)

    def getRectangle(self):
        x = min(self.x1, self.x2)
        y = min(self.y1, self.y2)
        w = abs(self.x1 - self.x2)
        h = abs(self.y1 - self.y2)
        return (x, y, w, h)


    def draw_circle(self, event, screen, another_layer, color):
        self.draw(event, screen, another_layer)

        if event.type == pygame.MOUSEMOTION:
            if self.isMouseDown:
                self.x2, self.y2 = event.pos
                screen.blit(another_layer, (0, 0))
                radius = ((self.x2 - self.x1)** 2 + (self.y2 - self.y1)** 2)** 0.5 
                pygame.draw.circle(screen, color, (self.x1, self.y1), int(radius), 3)  


    def draw_triangle(self, event, screen, another_layer, color):
        self.draw(event, screen, another_layer)

        if event.type == pygame.MOUSEMOTION:
            if self.isMouseDown:
                self.x2, self.y2 = event.pos
                screen.blit(another_layer, (0, 0))  
                radius = int(((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2) ** 0.5)  
                points = self.TriangleCoordinates(self.x1, self.y1, radius)  
                pygame.draw.polygon(screen, color, points, 3)  

    def TriangleCoordinates(self, x, y, radius):

        # Angles of triangle
        angle1 = math.radians(95)  
        angle2 = math.radians(215)  
        angle3 = math.radians(325)  
        
        # Coordinates of triangle
        x1 = x + radius * math.cos(angle1)
        y1 = y - radius * math.sin(angle1)
        x2 = x + radius * math.cos(angle2)
        y2 = y - radius * math.sin(angle2)
        x3 = x + radius * math.cos(angle3)
        y3 = y - radius * math.sin(angle3)
        
        
        return [(x1, y1), (x2, y2), (x3, y3)]



    def draw_equilateral_triangle(self, event, screen, another_layer, color):
        self.draw(event, screen, another_layer)

        if event.type == pygame.MOUSEMOTION:
            if self.isMouseDown:
                self.x2 = event.pos[0]
                self.y2 = event.pos[1]
                screen.blit(another_layer, (0, 0))  
                pygame.draw.polygon(screen, color, self.get_equilateral_triangle_points(), 3) 

    def get_equilateral_triangle_points(self):
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        hypotenuse = math.sqrt(dx ** 2 + dy ** 2)
        angle = math.atan2(dy, dx)
        x3 = self.x1 + hypotenuse * math.cos(angle + math.pi / 2)
        y3 = self.y1 + hypotenuse* math.sin(angle + math.pi / 2)
        return [(self.x1, self.y1), (self.x2, self.y2), (x3, y3)]



    def draw_rhombus(self, event, screen, another_layer, color):
        self.draw(event, screen, another_layer)

        if event.type == pygame.MOUSEMOTION:
            if self.isMouseDown:
                self.x2, self.y2 = event.pos
                screen.blit(another_layer, (0, 0))  
                pygame.draw.polygon(screen, color, self.get_rhombus_points(), 3)  

    def get_rhombus_points(self):
        cx = (self.x1 + self.x2) / 2  # center by OX
        cy = (self.y1 + self.y2) / 2  # center by OY
        dx = self.x2 - cx  # half of width of rhombus
        dy = self.y2 - cy  # half of height of rhombus
        return [(cx, cy - dy), (cx + dx, cy), (cx, cy + dy), (cx - dx, cy)]



    def erasor(self, event, screen, another_layer):
        self.draw(event, screen, another_layer)

        if event.type == pygame.MOUSEMOTION:
            if self.isMouseDown:
                pygame.draw.circle(screen, self.erase_color, event.pos, 25)  
                pygame.draw.circle(another_layer, self.erase_color, event.pos, 25)