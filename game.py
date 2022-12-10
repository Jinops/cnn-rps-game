import pygame.camera
import pygame.image
import pygame.time
import sys
import random
import numpy as np
from tensorflow.python.keras.models import load_model
from enum import Enum


model = load_model("./model.h5")
print(model.summary())


class Rps(Enum):
  ROCK = 0
  PAPER = 1
  SCISSORS = 2

def rps_game(my_hand, computer_hand):
  if my_hand == Rps.ROCK.value:
    if computer_hand == Rps.ROCK.value:
      return "DRAW"
    elif computer_hand == Rps.PAPER.value:
      return "LOSS"
    elif computer_hand == Rps.SCISSORS.value:
      return "WIN"

  elif my_hand == Rps.PAPER.value:
    if computer_hand == Rps.ROCK.value:
      return "WIN"
    elif computer_hand == Rps.PAPER.value:
      return "DRAW"
    elif computer_hand == Rps.SCISSORS.value:
      return "LOSS"

  elif my_hand == Rps.SCISSORS.value:
    if computer_hand == Rps.ROCK.value:
      return "LOSS"
    elif computer_hand == Rps.PAPER.value:
      return "WIN"
    elif computer_hand == Rps.SCISSORS.value:
      return "DRAW"


pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)

computer_hand_pos = (100, 100)
player_hand_pos = (500, 100)
hand_size = (300, 300)
timer_pos = (450, 160)

screen = pygame.display.set_mode( ( 960 , 640 ) ) # center: 480 * 320
pygame.display.set_caption("Rock Paper Scissor!")
screen.fill(white)

pygame.camera.init()
webcam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
webcam.start()

ticks_timer=pygame.time.get_ticks()
font = pygame.font.Font(None, 40)

pygame.draw.rect(screen, black, computer_hand_pos+ hand_size) # computer hand bg
pygame.draw.rect(screen, black, player_hand_pos + hand_size) # player hand bg

pygame.display.flip()

while True :
    for e in pygame.event.get() :
        if e.type == pygame.QUIT :
            sys.exit()

    # draw cam
    cam_img = pygame.transform.scale(webcam.get_image(), hand_size)
    screen.blit(cam_img, player_hand_pos)

    # draw timer
    sec=1-(pygame.time.get_ticks()-ticks_timer)//1000
    time_text = font.render(str(sec), True, black)
    pygame.draw.rect(screen, white, timer_pos + (30, 30)) # time text bg
    screen.blit(time_text, timer_pos)

    pygame.display.flip()

    if sec==0: 
        screen.blit(cam_img, player_hand_pos)
        pygame.display.flip()

        computer_hand = random.randrange(0,3)
        computer_img_src = None
        if computer_hand == Rps.ROCK.value:
          computer_img_src = "rock.png"
        elif computer_hand == Rps.SCISSORS.value:
          computer_img_src = "scissors.png"
        elif computer_hand == Rps.PAPER.value:
          computer_img_src = "paper.png"

        print(computer_hand, computer_img_src)

        computer_img = pygame.transform.scale(pygame.image.load(computer_img_src), hand_size)
        screen.blit(computer_img, computer_hand_pos)

        #predict = np.argmax(model.predict(computer_img_src), axis=-1)
        print(model.predict(computer_img_src))
        
        
        pygame.time.delay(1000)
        ticks_timer=pygame.time.get_ticks()
