from tkinter import *
import random

GAME_WIDTH = 600
GAME_HEIGHT = 600
SPEED = 200
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#0000FF"
FOOD_COLOR = "#FFFF00"
BACKGROUND_COLOR = "#000000"

class Snake:

    def __init__(self, canvas):
        self.canvas = canvas

        self.reset()

    def reset(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for _ in range(self.body_size):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:

    def __init__(self, canvas):
        self.canvas = canvas
        self.item_id = self.canvas.create_oval(0, 0, SPACE_SIZE, SPACE_SIZE, fill=FOOD_COLOR, tag="food")

        self.reset()

    def reset(self):
        x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        self.canvas.moveto(self.item_id, x, y)


def next_turn(snake, food):
    global score

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE

    elif direction == "down":
        y += SPACE_SIZE

    elif direction == "left":
        x -= SPACE_SIZE

    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, )

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        score += 1

        label.config(text="Score: {}".format(score))

        food.reset()

    else:
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction

    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction

    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction

    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):
    x, y, = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True

    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    global again

    canvas.delete('all')
    canvas.create_text(canvas.winfo_width() / 2,
                       canvas.winfo_height() / 2,
                       font=('consolas', 70),
                       text="GAME OVER",
                       fill="red",
                       tag="gameover")

    again = Button(canvas,
                      width=12,
                      height=2,
                      text="Play again?",
                      font=('consolas', 15),
                      bg="black",
                      fg="red",
                      activebackground="black",
                      activeforeground="red",
                      command=new_game)
    again.place(relx=0.5, rely=0.65, anchor='center')


def new_game():
    global score
    global direction
    global snake
    global food

    if again:
        again.destroy()

    score = 0
    direction = 'down'

    canvas.delete('all')
    label.config(text=f"Score:{score}")

    snake = Snake(canvas)
    food = Food(canvas)


    next_turn(snake, food)

window = Tk()
window.title("Snake game")
window.resizable(False, False)

label = Label(window,
                 text="Score:0",
                 font=('consolas', 40))
label.pack()

canvas = Canvas(window,
                   bg=BACKGROUND_COLOR,
                   height=GAME_HEIGHT,
                   width=GAME_WIDTH)
canvas.pack()

window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<a>', lambda event: change_direction('left'))
window.bind('<d>', lambda event: change_direction('right'))
window.bind('<w>', lambda event: change_direction('up'))
window.bind('<s>', lambda event: change_direction('down'))

again = None

new_game()

window.mainloop()