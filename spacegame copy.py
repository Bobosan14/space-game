import pygame
import sys
import random


import mediapipe as mp #Hand Landmarking 
import cv2 #Capturing Live Stream
cap= cv2.VideoCapture(0)

mp_hands=mp.solutions.hands #Hand Landmark Detection
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands= mp_hands.Hands (    
    model_complexity=0,         
    min_detection_confidence=0.9, # This value can be changed to signify how sure you want the computer to be 
    min_tracking_confidence=0.9)

#my_sound = pygame.mixer.Sound('music.mp4')
#my_sound.play()

def hand_gesture_detection():
    ret, frame = cap.read() #Capture Frame from video
    
   
    frame.flags.writeable= False # To improve detection
    frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)#Converts from Blue Green Red format to Red Green Blue format
    
    result = hands.process(frame) #Sending the resulting image to the hand detection model

    frame.flags.writeable=True
    frame=cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            x_cord_9= hand_landmarks.landmark[9].x
            y_cord_9= hand_landmarks.landmark[9].y
            
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
            
        return x_cord_9, y_cord_9
    else:
        return 1,1
        
           
    #cv2.imshow('frame', frame)        
    #cv2.destroyAllWindows
    

# Initialize 
pygame.init()

WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CON_WIDTH, CON_HEIGHT = 60, 60
FPS = 60

score = 0

b_music= pygame.mixer.Sound('music.wav')
b_music.play()
b_music.set_volume(0.2)
#Draw bg
background = pygame.image.load("space-background.jpg")
background = pygame.transform.scale(background,(WIDTH*2,HEIGHT*2))
background_rect = background.get_rect()
background_rect.center = 400,300
# Load spaceship image
spaceship_image = pygame.image.load("jezza.png")  
spaceship = pygame.transform.scale(spaceship_image, (60, 75)) 

# Load the asteroid image;
asteroid_image = pygame.image.load("asteroid.png")  
asteroid_image = pygame.transform.scale(asteroid_image, (50, 30))  

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodgers Game")

# Spaceship properties
spaceship_x = 400
spaceship_y = 500
spaceship_speed = 5



# Asteroid properties
asteroids = []
asteroid_speed = 7
spawn_frequency = 8
asteroid_counter = 0


# draw asteroid
def draw_asteroids(asteroids):
    for asteroid in asteroids:
        screen.blit(asteroid_image, (asteroid.x, asteroid.y))

# render text
def render_score():
    font = pygame.font.SysFont(None, 36)
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))  

def render_FPS():
    font = pygame.font.SysFont(None, 36)
    score_text = font.render("Speed: " + str(asteroid_speed), True, WHITE)
    screen.blit(score_text, (10,30))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get pressed keys
    #keys = pygame.key.get_pressed()
            
    
    hand_x_coord, hand_y_coord = hand_gesture_detection()

    spaceship_x = hand_x_coord*WIDTH
    spaceship_y = hand_y_coord*HEIGHT
    

    # Wrap around screen
    if spaceship_x < 0:
        spaceship_x = WIDTH
    elif spaceship_x > WIDTH:
        spaceship_x = 0

    # Spawn asteroid
    if asteroid_counter % spawn_frequency == 0:
        asteroid_x = random.randint(0, WIDTH - CON_WIDTH)
        asteroid_y = -CON_HEIGHT
        asteroids.append(pygame.Rect(asteroid_x, asteroid_y, CON_WIDTH, CON_HEIGHT))
    asteroid_counter = (asteroid_counter + 1) % spawn_frequency  # Reset asteroid counter

    # Move asteroids down screen
    for asteroid in asteroids:
        asteroid.y += asteroid_speed

        # Check collision
        if asteroid.y > spaceship_y:
            score += 1
            asteroids.remove(asteroid)  # Remove the asteroid once it passes the spaceship


    # Check collision
    spaceship_rect = pygame.Rect(spaceship_x, spaceship_y, spaceship.get_width(), spaceship.get_height())
    for asteroid in asteroids:
        if spaceship_rect.colliderect(asteroid):
            running = False
    if score==20:
        asteroid_speed=12


    if score==40:
        asteroid_speed=17


    if score==60:
        asteroid_speed=21

    if score==100:
        print("Congratulations you beat the game!")
        pygame.quit()
        sys.exit()
    
    
    screen.blit(background,background_rect)

    # Draw spaceship image
    screen.blit(spaceship, (spaceship_x, spaceship_y))


    # Draw asteroids
    draw_asteroids(asteroids)

    # Render ,display score
    render_score()
    render_FPS()
    # Update display
    pygame.display.flip()
    pygame.time.Clock().tick(FPS)


# Print final score
print("Final Score:", score)

pygame.quit()
sys.exit()

