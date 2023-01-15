import pygame
import pygame_menu
import math  # for checking for collisions with the mouse and the circle
import random
import keyboard
import turtle
import time
import pygame.freetype
import sys

pygame.init()
surface = pygame.display.set_mode((1080, 720))
paddle_height = 150

def snake():
    global index
    w = 450
    h = 450
    food_size = 10
    delay = 100
    white = (255, 255, 255)
    index = 0
    offsets = {
        "up": (0, 20),
        "down": (0, -20),
        "left": (-20, 0),
        "right": (20, 0)
    }

    def reset():
        global snake, snake_dir, food_position, pen
        snake = [[0, 0], [0, 20], [0, 40], [0, 60], [0, 80]]
        snake_dir = "up"
        food_position = get_random_food_position()
        food.goto(food_position)
        move_snake()







    def move_snake():
        global snake_dir

        new_head = snake[-1].copy()
        new_head[0] = snake[-1][0] + offsets[snake_dir][0]
        new_head[1] = snake[-1][1] + offsets[snake_dir][1]



        def goodbye():
            turtle.bye()

        def end():
            screen.bgcolor("red")
            end_turtle = turtle.Turtle()
            end_turtle.penup()
            end_turtle.goto(0,100)
            end_turtle.color("Black")
            end_turtle.pendown()
            end_turtle.hideturtle()
            style = ("courier", 60, "bold")
            end_turtle.write("GAME OVER", font=style, align="center", move=True)
            time.sleep(2)
            goodbye()

        if new_head in snake[:-1]:
            end()
        else:
            snake.append(new_head)

            if not food_collision():
                snake.pop(0)

            if snake[-1][0] > w / 2:
                snake[-1][0] -= w
            elif snake[-1][0] < - w / 2:
                snake[-1][0] += w
            elif snake[-1][1] > h / 2:
                snake[-1][1] -= h
            elif snake[-1][1] < -h / 2:
                snake[-1][1] += h

            pen.clearstamps()

            for segment in snake:
                pen.goto(segment[0], segment[1])
                pen.stamp()

            screen.update()

            turtle.ontimer(move_snake, delay)


    def food_collision():
        global food_position, index,point_turtle
        if get_distance(snake[-1], food_position) < 20:
            food_position = get_random_food_position()
            food.goto(food_position)
            point_turtle.clear()
            point_turtle.goto(0,200)
            style = ("courier", 10)
            point_turtle.write("Points:",font= style, align="center", move=True)
            index+=1
            point_turtle.write(index)

            return True
        return False


    def get_random_food_position():
        x = random.randint(- w / 2 + food_size, w / 2 - food_size)
        y = random.randint(- h / 2 + food_size, h / 2 - food_size)
        return (x, y)


    def get_distance(pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
        return distance


    def go_up():
        global snake_dir
        if snake_dir != "down":
            snake_dir = "up"


    def go_right():
        global snake_dir
        if snake_dir != "left":
            snake_dir = "right"


    def go_down():
        global snake_dir
        if snake_dir != "up":
            snake_dir = "down"


    def go_left():
        global snake_dir, point
        if snake_dir != "right":
            snake_dir = "left"


    screen = turtle.Screen()
    screen.setup(w, h)
    screen.title("Snake")
    screen.bgcolor("green")
    screen.setup(450, 450)
    screen.tracer(0)
    global point_turtle
    point_turtle = turtle.Turtle()
    point_turtle.penup()
    point_turtle.goto(0,200)
    point_turtle.color("Black")
    point_turtle.pendown()
    point_turtle.hideturtle()
    style = ("courier", 10,)
    point_turtle.write("Points:", align="center", move=True)

    pen = turtle.Turtle("square")
    pen.shapesize(1, 1, 0)
    pen.penup()

    food = turtle.Turtle()
    food.shape("square")
    food.color("red")
    food.shapesize(food_size / 20)
    food.penup()

    screen.listen()
    screen.onkey(go_up, "Up")
    screen.onkey(go_right, "Right")
    screen.onkey(go_down, "Down")
    screen.onkey(go_left, "Left")

    reset()
    turtle.done()


def pong():
    # Window setup
    window_height = 720
    window_width = 1080
    win = pygame.display.set_mode((window_width, window_height))

    pygame.display.set_caption('Pong')

    # Colors
    red = (255, 0, 0)
    white = (255, 255, 255)
    black = (0, 0, 0)

    # Sprite Classes

    class Paddle1(pygame.sprite.Sprite):
        def __init__(self):
            global paddle_height
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface([15, paddle_height])
            self.image.fill(white)
            self.rect = self.image.get_rect()
            self.points = 0

    class Paddle2(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface([15, paddle_height])
            self.image.fill(white)
            self.rect = self.image.get_rect()
            self.points = 0

    class Ball(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface([15, 15])
            self.image.fill(white)
            self.rect = self.image.get_rect()
            self.speed = 25
            self.dx = 1
            self.dy = 1

    # Sprite Creation

    paddle1 = Paddle1()
    paddle1.rect.x = 35
    paddle1.rect.y = 350

    paddle2 = Paddle2()
    paddle2.rect.x = 1045
    paddle2.rect.y = 350

    paddle_speed = 23

    pong = Ball()
    pong.rect.x = 540
    pong.rect.y = 375

    # Group of Sprites

    all_sprites = pygame.sprite.Group()
    all_sprites.add(paddle1, paddle2, pong)

    # Screen update function

    def redraw():
        # Draws black screen
        win.fill(black)

        # Title font
        font = pygame.font.SysFont('Comic Sans MS', 30)
        text = font.render('PONG', False, white)
        textRect = text.get_rect()
        textRect.center = (window_width // 2, 25)
        win.blit(text, textRect)

        # Player 1 Score
        p1_score = font.render(str(paddle1.points), False, white)
        p1Rect = p1_score.get_rect()
        p1Rect.center = (50, 50)
        win.blit(p1_score, p1Rect)

        # Player 2 Score
        p2_score = font.render(str(paddle2.points), False, white)
        p2Rect = p2_score.get_rect()
        p2Rect.center = (1030, 50)
        win.blit(p2_score, p2Rect)

        # Updates all Sprites
        all_sprites.draw(win)

        # Draws updates
        pygame.display.update()


    run = True

    # Main Loop

    while run:
        pygame.time.delay(100)


        # Quit Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Paddle Movement
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            paddle1.rect.y += -paddle_speed
        if key[pygame.K_s]:
            paddle1.rect.y += paddle_speed
        if key[pygame.K_UP]:
            paddle2.rect.y += -paddle_speed
        if key[pygame.K_DOWN]:
            paddle2.rect.y += paddle_speed

        # Moves pong ball
        pong.rect.x += pong.speed * pong.dx
        pong.rect.y += pong.speed * pong.dy

        # Wall and Paddle Bounces
        if pong.rect.y > 710:
            pong.dy = -1

        if pong.rect.y < 1:
            pong.dy = 1

        if pong.rect.x > 1070:
            pong.rect.x, pong.rect.y = 540, 375
            pong.dx = -1
            paddle1.points += 1

        if pong.rect.x < 1:
            pong.rect.x, pong.rect.y = 540, 375
            pong.dx = 1
            paddle2.points += 1

        if paddle1.rect.colliderect(pong.rect):
            pong.dx = 1

        if paddle2.rect.colliderect(pong.rect):
            pong.dx = -1

        #paddle limits

        if paddle1.rect.y < 0 :
          paddle1.rect.y = 0
        if paddle1.rect.y > window_height - paddle_height :
          paddle1.rect.y = window_height - paddle_height
        if paddle2.rect.y < 0 :
          paddle2.rect.y = 0
        if paddle2.rect.y > window_height - paddle_height :
          paddle2.rect.y = window_height - paddle_height

        #winner
        if paddle1.points == 3:
            win.fill(white)
            font = pygame.font.SysFont('Comic Sans MS', 30)
            text_winner = font.render('Player on the left wins', True, red)
            text_winnerRect = text_winner.get_rect()
            text_winnerRect.center = (window_width // 2, 25)
            win.blit(text_winner, text_winnerRect)
            pygame.display.update()
            pygame.time.delay(5000)
            break
        if paddle2.points == 3:
            win.fill(white)
            font = pygame.font.SysFont('Comic Sans MS', 30)
            text_winner = font.render('Player on the right wins', True, red)
            text_winnerRect = text_winner.get_rect()
            text_winnerRect.center = (window_width // 2, 25)
            win.blit(text_winner, text_winnerRect)
            pygame.display.update()
            pygame.time.delay(5000)
            break

        if keyboard.is_pressed('m'):
            menu()





        # Runs redraw function above
        redraw()




def aim():
    width = 1080
    height = 720
    display = pygame.display.set_mode((width, height))  # Screen/Window


    # Colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    purple = (128, 0, 128)
    grey = (128, 128, 128)
    sky = (0, 0, 220)
    blue = (85, 206, 255)
    orange = (255, 127, 80)
    red = (200, 0, 0)
    light_red = (255, 0, 0)
    green = (0, 200, 0)
    light_green = (0, 255, 0)
    colors = [white, purple, grey, blue, sky, orange, red, green]

    # Globals
    font = pygame.font.SysFont('malgungothic', int(width/28))  # The score text font
    end_font = pygame.font.SysFont('sylfaen', int(width/20))

    clock = pygame.time.Clock()  # To set the frame rate
    max_time = 60  # timer in seconds for the game
    show_seconds = True

    score = 0
    show_score = True

    loop_count = 0


    # Main Game Loop
    # Show the first circle
    cx = random.randint(20, width - 14)
    cy = random.randint(120, height - 14)
    width_of_circle = random.randint(7, 14)
    pygame.draw.circle(display, random.choice(colors), (cx, cy), width_of_circle)

    start_ticks = pygame.time.get_ticks()  # Timer start
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if keyboard.is_pressed('m'):
            menu()

        # Timer
        seconds = round((pygame.time.get_ticks() - start_ticks) / 1000, 1)  # calculate how many seconds
        if seconds >= max_time:
            show_seconds = False  # Make sure that the timer and the score do not show up on the screen anymore
            show_score = False

            end_score = end_font.render(f'You hit {round(score / 5)} targets! Nice!', True, green)
            display.fill(black)
            display.blit(end_score, (int(width / 4), (height / 2 - 50)))  # Show the score in the middle of the screen

            loop_count += 1
            if loop_count >= 900:  # if loop goes 14 times
                time.sleep(2)
                menu()


        # Score
        score_text = font.render(f'{score}', True, blue)  # Rendering the font but not putting it onto the screen yet
        timer = font.render(f'{seconds}', True, red)
        if show_score:
            display.blit(score_text, (width-100,30))  # Now putting it onto the screen at the top right
        if show_seconds:
            pygame.draw.rect(display, black, (50, 30, int(width/32)+65, int(width/32)+20))  # Rectangle over the timer to prevent clumping of the numbers
            display.blit(timer, (50, 30))


        # Checking if circle has been clicked on
        # Mouse position
        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]

        # Square the pos'
        sqx = (x - cx)**2
        sqy = (y - cy)**2

        # get what button on the mouse was clicked
        click = pygame.mouse.get_pressed()

        # If the circle has been clicked on
        if math.sqrt(sqx + sqy) < width_of_circle and click[0] == 1:  # click[0] is 1st mouse button (left click)
            score += 5  # Add 5 to the score
            display.fill(black)  # Redraw the screen
            # Redraw the circle
            cx = random.randint(20, width - 14)
            cy = random.randint(120, height - 14)
            width_of_circle = random.randint(7, 14)
            pygame.draw.circle(display, random.choice(colors), (cx, cy), width_of_circle)


        pygame.display.update()
        clock.tick()  # setting the frame rate (default is 60)

def info():

    screen = pygame.display.set_mode((1080, 720))
    pygame.display.set_caption("Information page")
    pygame.display.flip()
    font_color1=(0,150,250)
    font_color2=(185, 217, 207)
    font_color3=(255, 145, 128)
    font_color4=(171, 145, 196)
    font_color5 = (136, 158, 206)
    font_color6 = (100, 41.2, 38)

    font_obj=pygame.font.Font("C:\Windows\Fonts\segoeprb.ttf",25)
    text_obj=font_obj.render("Welcome to The Tribary of games",True,font_color1)
    text_obj2=font_obj.render("Aim Game: When you begin the game, there will be a 60 second timer",True,font_color3)
    text_obj2a=font_obj.render("hit as many targets as you can.",True,font_color3)
    text_obj3=font_obj.render("Pong 2 player Game: When you begin the game, player on left ",True,font_color4)
    text_obj3a=font_obj.render("use WASD, player on right arrows the ball will go to the",True,font_color4)
    text_obj3b=font_obj.render("player on the right, play with your friends! First to 3 wins",True,font_color4)
    text_obj4=font_obj.render("Snake game: Simple snake game, get all the apples you can!",True,font_color2)
    text_obj4b=font_obj.render("Use arrow keys to move",True,font_color2)
    text_obj5=font_obj.render("by Juliana Silva Costa",True,font_color5)
    text_obj6=font_obj.render("To go back to menu press m (For the game snake, just close the window)",True,font_color6)

    while True:
       screen.fill((0,0,0))
       screen.blit(text_obj,(22,0))
       screen.blit(text_obj2,(22,70))
       screen.blit(text_obj2a,(22,100))
       screen.blit(text_obj3,(22,200))
       screen.blit(text_obj3a,(22,230))
       screen.blit(text_obj3b,(22,260))
       screen.blit(text_obj4,(22,360))
       screen.blit(text_obj4b,(22,390))
       screen.blit(text_obj5,(22,490))
       screen.blit(text_obj6,(22,590))
       for eve in pygame.event.get():
          if eve.type==pygame.QUIT:
             pygame.quit()
             sys.exit()
          if keyboard.is_pressed('m'):
            menu()

       pygame.display.update()




def menu():
    menu = pygame_menu.Menu('The mini game Tribary', 1080, 720, theme=pygame_menu.themes.THEME_SOLARIZED)
    pygame_menu.widgets.TextInput("test")
    menu.add.button('Aim game', aim)
    menu.add.button('Pong 2 player', pong)
    menu.add.button('Snake game', snake)
    menu.add.button('Game information (IMPORTANT)', info)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(surface)

menu()
