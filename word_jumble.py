"""
Word jumble game by Aaron Lee

Generate a group of random letters.  Player has to make words from them.
Points are scrabble like with multiplier for length of words
Uses a standard scrabble dictionary in dictonary.txt file
"""
 
import pygame
import random
import word_lists
 
# --- Global constants ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 150, 0)
RED = (255, 0, 0)
BLUE = (30,30,255)
PURPLE = (200,0,255)
 
SCREEN_WIDTH = 800
w = SCREEN_WIDTH//100
SCREEN_HEIGHT = 600
h = SCREEN_HEIGHT//100
DICT = word_lists.master_list

EDGE_GAP = 10 * w
BANNER_GAP = 30 * h
GUTTER = 2 * w
score = 0
 
# --- Classes ---

class RestartButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("restart.png")
        self.rect = self.image.get_rect()
        self.rect.bottomright = (SCREEN_WIDTH, SCREEN_HEIGHT)

class Ball():
    def __init__(self):
        self.diameter = random.randrange(100, 500)
        rb = random.randrange(210, 255)
        self.color = (rb, 255, rb)
        self.x = random.randrange(- SCREEN_WIDTH, SCREEN_WIDTH)
        self.xspeed = random.random()
        self.y = random.randrange(- self.diameter,  SCREEN_HEIGHT + self.diameter)
    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, [self.x, self.y, self.diameter, self.diameter])
        
    def move(self):
        self.x += self.xspeed
        if self.x > SCREEN_WIDTH + self.diameter:
            self.x = -self.diameter
            self.y = random.randrange(- self.diameter,  SCREEN_HEIGHT + self.diameter)
            self.xspeed = random.randrange(1,10)

class Scoreboard():
    def __init__(self):
        self.reveal_list = [] # for kill screen
        
        self.correct_list = [["4 ltrs"],["5 ltrs"],["6 ltrs"],["7 ltrs"],["8 ltrs"],["9 ltrs"],["10 letters"],["11 letters"],["12 letters"],["13 letters"],["14 letters"],["15 letters"],["16 letters"]] # store the words I get
        
        self.correct_list_score = [[["4 ltrs",""]],[["5 ltrs",""]],[["6 ltrs",""]],[["7 ltrs",""]],[["8 ltrs",""]],[["9 ltrs",""]],[["10 ltrs",""]],[["11 ltrs",""]],[["12 letters",""]],[["13 letters",""]],[["14 letters",""]],[["15 letters",""]],[["16 letters",""]]] # also store the scores for them in a list of lists
        self.x = 70*w
        self.y = BANNER_GAP
        self.font = pygame.font.SysFont('Roboto', 12, True, False)
        self.font_big = pygame.font.SysFont('Roboto', 24, True, False)
        self.font_small = pygame.font.SysFont('Roboto', 8, True, False)
        self.score_font = pygame.font.SysFont('Roboto', 30, True, False)
    def draw_score(self, screen, score, high, time):
        score_text = self.score_font.render("Score: " + str(score), True, BLACK)
        #high_text = self.score_font.render("High:  " + str(high), True, BLACK)
        pygame.draw.rect(screen, WHITE, [60*w, 5*h, 30*w, 15*h])  # Position of score box
        pygame.draw.rect(screen, BLACK, [60*w, 5*h, 30*w, 15*h], 2)
        screen.blit(score_text, [62*w, 8*h])
        #screen.blit(high_text, [52*w, 15*h])
        if time < 10:
            time_text = self.score_font.render("Time: " + str(int(time//60))+ ":" + "0" + str(int(time%60)), True, RED)
        else:
            if time%60 < 10:
                time_text = self.score_font.render("Time:  " + str(int(time//60))+ ":" + "0" + str(int(time%60)), True, BLACK)
            else:
                time_text = self.score_font.render("Time:  " + str(int(time//60))+ ":" + str(int(time%60)), True, BLACK)
        screen.blit(time_text, [62*w, 14*h])
    def draw(self, screen):
        #pygame.draw.line(screen, BLACK, [self.x, self.y + 17],[self.x + 110, self.y + 17], 3)
        '''
        for i in range(len(self.possible_list)):
            for j in range(len(self.possible_list[i])):
                if self.possible_list[i][j] in self.correct_list[i]:
                    #print(self.possible_list[i][j])
                    text = self.font.render(self.possible_list[i][j], True, BLACK)
                    screen.blit(text, [self.x + i * 150, self.y + j * 20])                    
        '''      
        for i in range(len(self.correct_list_score)):
            if len(self.correct_list_score[i]) > 1:
                for j in range(1,len(self.correct_list_score[i])):
                    #print(self.correct_list_score[i][j][1], "=", type(self.correct_list_score[i][j][1]))
                    
                    if self.correct_list_score[i][j][1] >= 50:
                        text = self.font.render(self.correct_list_score[i][j][0] + " " + str(self.correct_list_score[i][j][1]), True, PURPLE)                    
                    elif self.correct_list_score[i][j][1] >= 30:
                        text = self.font.render(self.correct_list_score[i][j][0] + " " + str(self.correct_list_score[i][j][1]), True, GREEN) 
                    else:
                        text = self.font.render(self.correct_list_score[i][j][0] + " " + str(self.correct_list_score[i][j][1]), True, BLACK)

                    #text = self.font.render(self.correct_list_score[i][j][0] + " " + str(self.correct_list_score[i][j][1]), True, BLACK)
                    x = min(i*5*w + (i**1.6)*w//1 + 50*w, 25*w + (5**1.6)*w//1 + 50*w)
                    screen.blit(text, [x, j * 3* h + 30*h])
    def make_randolist(self):
        self.reveal_list = []
        self.reveal_list_correct = []
        for i in range(len(self.possible_list)):
            for j in range(1, len(self.possible_list[i])):
                if self.possible_list[i][j] in self.correct_list[i]:
                    self.reveal_list_correct.append([self.possible_list[i][j], [random.randrange(-20, SCREEN_WIDTH), random.randrange(-20, SCREEN_HEIGHT)], GREEN])
                    
                else:
                    self.reveal_list.append([self.possible_list[i][j], [random.randrange(-20, SCREEN_WIDTH), random.randrange(-20, SCREEN_HEIGHT)],(random.randrange(255), 0, random.randrange(255))])
                
        
    def draw_reveal_list(self, screen):
        
        for i in range(len(self.reveal_list)):
            text = self.font.render(self.reveal_list[i][0], True, self.reveal_list[i][2])
            screen.blit(text, self.reveal_list[i][1])
        for i in range(len(self.reveal_list_correct)):
            text = self.font.render(self.reveal_list_correct[i][0], True, self.reveal_list_correct[i][2])
            screen.blit(text, self.reveal_list_correct[i][1])                
                        
        

class Inputbox():
    ''' Holds the input string of the user and displays it'''
    def __init__(self):
        self.text = ""
        self.points = 0
        self.point_text = ""
        self.x = 5*w
        self.y = 10*h
        self.font = pygame.font.SysFont('Courier', 40, True, False) # actual letters being typed
        self.font_points = pygame.font.SysFont('Calibri', 15, False, False) # info on point breakdown

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, [self.x, self.y, 40*w, 10*h])
        pygame.draw.rect(screen, WHITE, [self.x + 2, self.y + 2, 40*w-4, 10*h-4])
        text = self.font.render(self.text, True, BLACK)
        screen.blit(text, [self.x + 10, self.y + 7])
    def draw_wordscore(self, screen, scrabble_points):
        self.point_text = "Letter Score: "
        self.points = 0
        self.multiplier = "Multiplier: x " + str(max(len(self.text)-3, 1))
        for i in range(len(self.text)):
            self.point_text += str(scrabble_points.get(self.text[i])) + " "
            self.points += int(scrabble_points.get(self.text[i]))
            
            if i < len(self.text) - 1:
                self.point_text += "+ "
                
            else:
                self.point_text += "= "
        #print(self.points)        
        self.total = int(self.points) * max(len(self.text)-3, 1)
        self.point_text += str(self.points)
        
        
        text = self.font_points.render(self.point_text, True, BLACK)
        text2 = self.font_points.render(self.multiplier, True, BLACK)
        text3 = self.font_points.render("Word Score: " + str(self.total), True, BLACK)
        screen.blit(text, [self.x + w, self.y + 15 * h])
        screen.blit(text2, [self.x + w, self.y + 19 * h])
        pygame.draw.line(screen, BLACK, [self.x + w, self.y + 24*h], [self.x + 30*w, self.y + 24*h], 3)
        screen.blit(text3, [self.x + w, self.y + 26 * h])

 
class Letterbox(pygame.sprite.Sprite):
    """ These are the letters displayed in the Jumble (Boggle like I guess) """
 
    def __init__(self):
        """ Constructor, create the image of the block. """
        super().__init__()
        self.image = pygame.image.load("scrabble.png")
        #self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.font_bold = pygame.font.SysFont('Courier', 37, True, False)
        self.font = pygame.font.SysFont('Courier', 40, False, False)
        self.font_small = pygame.font.SysFont('Calibri', 15, False, False)
        
 
    def update(self):
        """ Automatically called when we need to move the block. """
        pass
    def draw_letter(self,screen, letter_list, scrabble_points):
        text = self.font_bold.render(letter_list[self.row * 4 + self.column], True, (20,20,20))
        screen.blit(text, [self.rect.x + w, self.rect.y + h])
        #text = self.font_bold.render(letter_list[self.row * 4 + self.column], True, (0,0,0))
        #screen.blit(text, [self.rect.x + 20, self.rect.y + 5]) 
        
        # draw point value
        value = self.font_small.render(str(scrabble_points.get(letter_list[self.row * 4 + self.column], " ")), True, BLACK)
        screen.blit(value, [self.rect.x + w*4, self.rect.y + h*5])
                                       
        
 
 
 
class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """
 
    def __init__(self):
        """ Constructor. Create all our attributes and initialize
        the game. """
       
        
        self.bg_music = pygame.mixer.Sound("bg.wav")
        self.bad_sound = pygame.mixer.Sound("bad.wav")
        self.good_sound = pygame.mixer.Sound("good.wav")
        self.good_big = pygame.mixer.Sound("big.wav")
        self.bg_music.set_volume(0.5)
        self.bg_music.play(-1)
        self.input_box = Inputbox()
        self.scoreboard = Scoreboard()
        self.frame = 0
        self.high = get_high_score()
        self.score = 0
        self.level = 1
        self.game_over = False
        self.intro = True
        self.time = 180
        
        
        # create background
        self.ball_list = []
        for i in range(50):
            ball = Ball()
            self.ball_list.append(ball)
            
        
        
        # create the list of letters to use
        
        letter_freq = [130,30,40,55,140,30,50,70,90,5,20,60,50,90,100,40,5,90,100,100,50,15,30,4,40,4]
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.weighted_letters = []
        for i in range(len(letters)):
            for j in range(letter_freq[i]):
                self.weighted_letters.append(letters[i])
        
        self.scrabble_points = {"A": 1, "C": 3, "B": 3, "E": 1, "D": 2, "G": 2, "F": 4, "I": 1, "H": 4, "K": 5, "J": 8, "M": 3,"L": 1, "O": 1, "N": 1, "Q": 10, "P": 3, "S": 1,"R": 1, "U": 1, "T":1, "W": 4, "V": 4, "Y": 4,"X": 8, "Z": 10}
        
            
 
        # Create sprite lists
        self.letter_list = []
        self.letter_list_pop = []
        self.letter_group = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        
        self.restart_button = RestartButton()
        self.all_sprites_list.add(self.restart_button)
 
        # Create the letter sprites and add them to the list
        # we will choose from the weighted letter list we made
        # for better play, we will also pull from a special list
        for i in range(4):
            for j in range(4):
                new_letter = Letterbox()
                self.letter_list.append(random.choice(self.weighted_letters)) # choose your letter to display and use
                if self.letter_list.count(self.letter_list[-1]) > 1:
                    self.letter_list[-1] = random.choice(self.weighted_letters)
                if self.letter_list[-1] == "Q":
                    if len(self.letter_list) > 1:
                        self.letter_list[-2] = "U"
                new_letter.row = i
                new_letter.column = j
                new_letter.rect.x = new_letter.row * (new_letter.rect.width + GUTTER) + EDGE_GAP
                new_letter.rect.y = new_letter.column * (new_letter.rect.width + GUTTER) + EDGE_GAP + BANNER_GAP
                self.letter_group.add(new_letter)
                self.all_sprites_list.add(new_letter)
        
                                    
        
        self.letter_list_pop = self.letter_list[:]
        # Create other sprites
        self.scoreboard.possible_list = [["4 letters"],["5 letters"],["6 letters"],["7 letters"],["8 letters"],["9 letters"],["10 letters"],["11 letters"],["12 letters"],["13 letters"],["14 letters"],["15 letters"],["16 letters"]]
        #print("Length dictionary = ", len(DICT))
        #print("Length letter_list = ", len(self.letter_list))
        
        # find all the possible words from the letter set
        for i in range(len(DICT)):
            for j in range(len(DICT[i])):
                for letter in DICT[i][j]:
                    if letter not in self.letter_list_pop:
                        self.letter_list_pop = self.letter_list[:]
                        break
                    else:
                        self.letter_list_pop[self.letter_list_pop.index(letter)] = " "
                else:
                    self.scoreboard.possible_list[len(DICT[i][j])-4].append(DICT[i][j])
                    self.letter_list_pop = self.letter_list[:]
                    
        #print("possible list", self.scoreboard.possible_list)
                 
        '''        
        self.len_list = []
        for i in range(15):
            self.len_list.append(None)
        for word in possible_list:
            if self.len_list[len(word)] != None:
                self.len_list[len(word)] += 1
            else:
                self.len_list[len(word)] = 0
        '''
 
    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.restart_button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.game_over = True
                    
                if self.game_over:
                    self.__init__()
            elif event.type == pygame.KEYDOWN:
                self.intro = False
                if event.key == pygame.K_a and "A" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("A")] = " "
                    self.input_box.text += "A"
                elif event.key == pygame.K_b and "B" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("B")] = " "
                    self.input_box.text += "B"
                elif event.key == pygame.K_c and "C" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("C")] = " "
                    self.input_box.text += "C"
                elif event.key == pygame.K_d and "D" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("D")] = " "
                    self.input_box.text += "D"
                elif event.key == pygame.K_e and "E" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("E")] = " "
                    self.input_box.text += "E"
                elif event.key == pygame.K_f and "F" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("F")] = " "
                    self.input_box.text += "F"
                elif event.key == pygame.K_g and "G" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("G")] = " "
                    self.input_box.text += "G"
                elif event.key == pygame.K_h and "H" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("H")] = " "
                    self.input_box.text += "H"
                elif event.key == pygame.K_i and "I" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("I")] = " "
                    self.input_box.text += "I"
                elif event.key == pygame.K_j and "J" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("J")] = " "
                    self.input_box.text += "J"
                elif event.key == pygame.K_k and "K" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("K")] = " "
                    self.input_box.text += "K"
                elif event.key == pygame.K_l and "L" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("L")] = " "
                    self.input_box.text += "L"
                elif event.key == pygame.K_m and "M" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("M")] = " "
                    self.input_box.text += "M"
                elif event.key == pygame.K_n and "N" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("N")] = " "
                    self.input_box.text += "N"
                elif event.key == pygame.K_o and "O" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("O")] = " "
                    self.input_box.text += "O"
                elif event.key == pygame.K_p and "P" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("P")] = " "
                    self.input_box.text += "P"
                elif event.key == pygame.K_q and "Q" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("Q")] = " "
                    self.input_box.text += "Q"
                elif event.key == pygame.K_r and "R" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("R")] = " "
                    self.input_box.text += "R"
                elif event.key == pygame.K_s and "S" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("S")] = " "
                    self.input_box.text += "S"
                elif event.key == pygame.K_t and "T" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("T")] = " "
                    self.input_box.text += "T"
                elif event.key == pygame.K_u and "U" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("U")] = " "
                    self.input_box.text += "U"
                elif event.key == pygame.K_v and "V" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("V")] = " "
                    self.input_box.text += "V"
                elif event.key == pygame.K_w and "W" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("W")] = " "
                    self.input_box.text += "W"
                elif event.key == pygame.K_x and "X" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("X")] = " "
                    self.input_box.text += "X"
                elif event.key == pygame.K_y and "Y" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("Y")] = " "
                    self.input_box.text += "Y"
                elif event.key == pygame.K_z and "Z" in self.letter_list_pop:
                    self.letter_list_pop[self.letter_list_pop.index("Z")] = " "
                    self.input_box.text += "Z"
                
                elif event.key == pygame.K_BACKSPACE:
                    #self.input_box.text = self.input_box.text[0:-1]
                    pass
                elif event.key == pygame.K_RETURN:
                    '''IS IT A WORD??'''
                    if self.input_box.text in self.scoreboard.possible_list[len(self.input_box.text) - 4] and self.input_box.text not in self.scoreboard.correct_list[len(self.input_box.text) - 4]:
                        
                        
                        word_score = 0
                        word_multiplier = len(self.input_box.text) - 3
                        for letter in self.input_box.text:
                            word_score += self.scrabble_points.get(letter)
                        increase = word_score * word_multiplier
                        if increase > 70:
                            self.good_big.play()
                            self.time += 30
                        elif increase > 40:
                            self.good_big.play()
                            self.time += 15                        
                        else:
                            self.good_sound.play()
                        self.score += word_score * word_multiplier
                        self.scoreboard.correct_list_score[len(self.input_box.text)-4].append([self.input_box.text, increase])
                        self.scoreboard.correct_list[len(self.input_box.text)-4].append(self.input_box.text)
                        #print("correct_list = ", self.scoreboard.correct_list)
                        #print(self.scoreboard.possible_list)
                        self.input_box.text = ""
                        self.letter_list_pop = self.letter_list[:]
                
                    else:
                        self.bad_sound.play()
                        
                        self.input_box.text = ""
                        self.letter_list_pop = self.letter_list[:]
                        
                
        return False
 
    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if not self.game_over:
            # Move all the sprites

            self.all_sprites_list.update()
 
            # do collision checks
         
            
 
            # Check the list of collisions.
            
            # do end game checks
            if self.time <= 0:
                self.scoreboard.make_randolist()
                self.game_over = True
                self.bg_music.stop()
                self.high = get_high_score()
                if self.score > self.high:
                    self.high = self.score
                save_high_score(self.high)
 
    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(WHITE)
        
        
        if self.game_over:
            # font = pygame.font.Font("Serif", 25)
            self.scoreboard.draw_reveal_list(screen)
            
            font = pygame.font.SysFont("Courier", 40, True, False)
            text = font.render("Game Over, click to restart", True, BLACK)

            text2 = font.render("Your score: " + str(self.score), True, BLACK)
            text3 = font.render("High score: " + str(self.high), True, BLACK)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y - 50])
            center_x = (SCREEN_WIDTH // 2) - (text2.get_width() // 2)
            screen.blit(text2, [center_x, center_y])
            center_x = (SCREEN_WIDTH // 2) - (text3.get_width() // 2)
            screen.blit(text3, [center_x, center_y + 50]) 
            
        elif self.intro:
            for ball in self.ball_list:
                ball.move()
                ball.draw(screen)
            self.all_sprites_list.draw(screen)
            self.input_box.draw(screen)
            self.input_box.draw_wordscore(screen, self.scrabble_points)
            self.scoreboard.draw(screen)
            self.scoreboard.draw_score(screen, self.score, self.high, self.time)
            font = pygame.font.SysFont("Calibri", 20, False, False)
            text = font.render("Mr. Lee Example Game!  Create any word (4 letters or more) from the tiles provided.", True, BLACK)
            text2 = font.render("Long words receive a score multiplier.  Big word scores receive a time bonus.", True, BLACK)
            text3 = font.render("Just use your keyboard. Press any key to begin.  GOOD LUCK!", True, BLACK)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 1.7) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y - 5*h])
            center_x = (SCREEN_WIDTH // 2) - (text2.get_width() // 2)
            screen.blit(text2, [center_x, center_y])
            center_x = (SCREEN_WIDTH // 2) - (text3.get_width() // 2)
            screen.blit(text3, [center_x, center_y + 5*h])

        else:
            self.time -= 1/30            
            for ball in self.ball_list:
                ball.move()
                ball.draw(screen)
            self.all_sprites_list.draw(screen)
            for letter in self.letter_group:
                letter.draw_letter(screen, self.letter_list_pop, self.scrabble_points)
            self.input_box.draw(screen)
            self.input_box.draw_wordscore(screen, self.scrabble_points)
            self.scoreboard.draw(screen)
            self.scoreboard.draw_score(screen, self.score, self.high, self.time)
 
        pygame.display.flip()
 
def get_high_score():
    # Default high score
    high_score = 0

    # Try to read the high score from a file
    try:
        high_score_file = open("high_score.txt", "r")
        high_score = int(high_score_file.read())
        high_score_file.close()
        #print("The high score is", high_score)
    except IOError:
        # Error reading file, no high score
        print("There is no high score yet.")
    except ValueError:
        # There's a file there, but we don't understand the number.
        print("I'm confused. Starting with no high score.")

    return high_score


def save_high_score(new_high_score):
    try:
        # Write the file to disk
        high_score_file = open("high_score.txt", "w")
        high_score_file.write(str(new_high_score))
        high_score_file.close()
    except IOError:
        # Hm, can't write it.
        print("Unable to save the high score.")


def main():
    """ Main program function. """
    # Initialize Pygame and set up the window
    pygame.init()
 
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Word Jumble")
    pygame.mouse.set_visible(False)
 
    # Create our objects and set the data
    done = False
    clock = pygame.time.Clock()
 
    # Create an instance of the Game class
    game = Game()
 
    # Main game loop
    while not done:
 
        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()
 
        # Update object positions, check for collisions
        game.run_logic()
 
        # Draw the current frame
        game.display_frame(screen)
 
        # Pause for the next frame
        clock.tick(30)
 
    # Close window and exit
    pygame.quit()
 
# Call the main function, start up the game
if __name__ == "__main__":
    main()
