import os
import sys
import time
import random
import pygame
import pygame.freetype
from pygame.locals import *
 
 
# Class for the orange dude
class Player(object):
    
    def __init__(self):
        self.rect = pygame.Rect(32, 32, 16, 16)
 
    def move(self, dx, dy):
        
        # Move each axis separtely. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
    
    def move_single_axis(self, dx, dy):
        
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy
 
        # If you collide with a wall, move out based on velocity
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom
        
        # If you collide with a box
        for box in boxes:
            if self.rect.colliderect(box.rect):
                game_state.exer1()
                boxes.remove(box)
                
 
# Nice class to hold a wall rect
class Wall(object):
    
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
    
    

class Box(object):
    
    def __init__(self, pos):
        boxes.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

class GameState():
    
    def __init__(self):
        self.state = "intro"
    
    def intro(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                self.state = 'main_game'
    
    
        # Just added this to make it slightly fun ;)
        '''
        if player.rect.colliderect(end_rect):
            pygame.quit()
            sys.exit()
        
        for box in boxes:
            if player.rect.colliderect(box):
                exer1()
        '''
        
        # Drawing
        screen.fill((0, 0, 0))
        screen.blit(intro_text, (0, 0))
        # gfxdraw.filled_circle(screen, 255, 200, 5, (0,128,0))
        pygame.display.flip()
    
    def main_game(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
 
        # Move the player if an arrow key is pressed
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            player.move(-2, 0)
        if key[pygame.K_RIGHT]:
            player.move(2, 0)
        if key[pygame.K_UP]:
            player.move(0, -2)
        if key[pygame.K_DOWN]:
            player.move(0, 2)
    
    
        # Just added this to make it slightly fun ;)
        
        if player.rect.colliderect(end_rect):
            pygame.quit()
            sys.exit()
        
        
        # Drawing
        screen.fill((0, 0, 0))
        for wall in walls:
            pygame.draw.rect(screen, (255, 255, 255), wall.rect)
        for box in boxes:
            pygame.draw.rect(screen, (0, 128, 0), box.rect)
        pygame.draw.rect(screen, (255, 0, 0), end_rect)
        pygame.draw.rect(screen, (255, 200, 0), player.rect)
        # gfxdraw.filled_circle(screen, 255, 200, 5, (0,128,0))
        pygame.display.flip()
    
    def exer1(self):
        font = pygame.font.Font(None, 32)
        input_box = pygame.Rect(490, 240, 240, 32)
        input_box_color = (255, 255, 255)
        input_background_color = (0, 0, 0)
        LIGHT_BLUE = (0, 128, 255)
        GRAY = (128, 128, 128)
        user_answer = ''
        # Define the variables for the user's answer and input box status
        input_box_active = False
        exer1_running = True
        while exer1_running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicks on the input box, activate it
                    if input_box.collidepoint(event.pos):
                        input_box_active = not input_box_active
                    else:
                        input_box_active = False
                    # Change the color of the input box depending on its status
                    input_box_color = LIGHT_BLUE if input_box_active else GRAY
                if event.type == pygame.KEYDOWN:
                    # If the input box is active, allow the user to enter text
                    if input_box_active:
                        if event.key == pygame.K_RETURN:
                            # When the user presses Enter, print their answer and reset the input box
                            print(user_answer)
                            if user_answer.lower() == answer:
                                game_state.right_answer()
                                countdown_time = 3
                                for i in range(countdown_time, 0, -1):
                                    time.sleep(1)
                            elif user_answer.lower() != answer:
                                game_state.wrong_answer()
                                countdown_time = 3
                                for i in range(countdown_time, 0, -1):
                                    time.sleep(1)
                            del questions[0:2]
                            exer1_running = False
                        elif event.key == pygame.K_BACKSPACE:
                            # Allow the user to delete characters with the Backspace key
                            user_answer = user_answer[:-1]
                            pygame.draw.rect(screen, input_background_color, input_box)
                            pygame.draw.rect(screen, input_box_color, input_box, 2)
                            user_answer_surface = font.render(user_answer, True, (255, 255, 255))
                            screen.blit(user_answer_surface, (input_box.x+5, input_box.y+5))
                            pygame.display.update()
                        else:
                            # Add the character to the user's answer
                            user_answer += event.unicode
            
            question_text = questions[0]
            answer = questions[1]
            
            # answer = my_list[0][1]
            # Draw the screen
            question_surface = font.render(question_text, True, (255, 0, 0))
            screen.blit(question_surface, (460, 70))
            # (screen_width//4+10, 70)
            pygame.draw.rect(screen, input_background_color, input_box)
            pygame.draw.rect(screen, input_box_color, input_box, 2)
            user_answer_surface = font.render(user_answer, True, (255, 255, 255))
            screen.blit(user_answer_surface, (input_box.x+5, input_box.y+5))
            pygame.display.flip()
            
        if not exer1_running:
            game_state.main_game()
    
    def state_manager(self):
        if self.state == "intro":
            self.intro()
        elif self.state == "main_game":
            self.main_game()
        elif self.state == "exer":
            self.exer1()
    
    def right_answer(self):
        font = pygame.font.Font(None, 32)
        answer_surface = font.render('Õige!', True, (255, 255, 255))
        screen.blit(answer_surface, (580, 150))
        pygame.display.flip()
    
    def wrong_answer(self):
        font = pygame.font.Font(None, 32)
        answ = 'Vale. Õige vastus on ' + questions[1]
        answer_surface = font.render(answ, True, (255, 255, 255))
        screen.blit(answer_surface, (500, 150))
        pygame.display.flip()
        
 
# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

#Set up the introduction window
intro_screen = pygame.display.set_mode((320, 240))
intro_text = pygame.image.load("intro.png")
# Set up the display
screen_width = 1180
screen_height = 490
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Labyrinth Game")
game_state = GameState()
LIGHT_BLUE = (0, 128, 255)
GRAY = (128, 128, 128)

clock = pygame.time.Clock()
walls = [] # List to hold the walls
boxes = [] # List to hold the boxes
player = Player() # Create the player
 
# Holds the level layout in a list of strings.
level = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W       Y     Y    W",
    "W  WW WWWWWW WWW   W",
    "W W   W         Y  W",
    "W W    YW   WWWWW  W",
    "W WWWWWWWWWYW   W  W",
    "W  W   W  Y W    Y W",
    "WW W  Y  W    W W WW",
    "WWYWW WWWWW     W  W",
    "W     W   Y   WWW  W",
    "W WW  W WWWWYWW    W",
    "W  W  WY W    Y    W",
    "W  WW WW W   WWW   W",
    "W        W E   W   W",
    "WWWWWWWWWWWWWWWWWWWW",
]



questions = ['Mitu teemakooli on Vocos?', '7', 'Mida võiks tähendada märk "#"?', 'kommentaar',
             'Mitut eriala on ligikaudu Vocos võimalik omandada?', '80', 'Mitu korrust on kopli õppehoones? (nr)',
             '4', 'Väljasta koodina: Hello world! (kasuta print())',
             'print("hello world!")', 'Mis on VOCO täisnimi??', 'tartu rakenduslik kolledž', 'Näita koodina x ja y summa väljastamine',
             'print(x + y)', 'Mis kool asub voco kõrval??', 'variku kool', 'Mis oli Voco eelmine nimi?',
             'tartu kutsehariduskeskus', 'Mida tähistab int?', 'täisarvu', 'Mitu korpust on Vocos?', '3',
             'Mida tähistab float', 'ujukomaarvu', 'Mitu aastat õpitakse tarkvaraarenduse eriala?', '4']

# Parse the level string above. W = wall, E = exit, Y = exercise
x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        elif col == "E":
            end_rect = pygame.Rect(x, y, 16, 16)
        elif col == "Y":
            box_rect = Box((x, y))
        x += 16
    y += 16
    x = 0

print(boxes)

running = True
while running:
    
    clock.tick(60)
    game_state.state_manager()
    clock.tick(360)
 
pygame.quit()