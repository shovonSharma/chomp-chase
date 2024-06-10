from maze_generator import *

start_time = 0  # Variable to keep track of the start time

#total_time
time = 30


def astar(start, goal, grid_cells):
    open_set = {start}
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = min(open_set, key=lambda cell: f_score[cell])

        if current == goal:
            path = reconstruct_path(came_from, goal)
            return path

        open_set.remove(current)

        for neighbor in current.get_neighbors(grid_cells):
            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)

                if neighbor not in open_set:
                    open_set.add(neighbor)

    return None

def heuristic(cell, goal):
    return abs(cell.x - goal.x) + abs(cell.y - goal.y)

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]


#class for AI player

class SecondPlayer:
    def __init__(self):
        self.img = pygame.image.load('img/murgi.png').convert_alpha()  # Load image for the second player
        self.img = pygame.transform.scale(self.img, (TILE - 10, TILE - 10))
        self.rect = self.img.get_rect()
        self.set_pos()

    def set_pos(self):
        # Set position to the top right corner
        self.rect.topright = (WIDTH, 0)
        self.rect.move_ip(-5, 5)  # Adjusting position slightly to fit within the border

    def draw(self):
        game_surface.blit(self.img, self.rect)


    #A* algorithm
    def move_towards_food(self, food, grid_cells):
        start_cell = grid_cells[self.rect.y // TILE * cols + self.rect.x // TILE]
        goal_cell = grid_cells[food.rect.y // TILE * cols + food.rect.x // TILE]

        path = astar(start_cell, goal_cell, grid_cells)
        if path and len(path) > 1:
            next_cell = path[1]
            target_x, target_y = next_cell.x * TILE, next_cell.y * TILE
            dx = target_x - self.rect.x
            dy = target_y - self.rect.y
            if abs(dx) > abs(dy):
                dx = dx / abs(dx)
                dy = 0
            else:
                dx = 0
                dy = dy / abs(dy)
            self.rect.move_ip(dx * player_speed, dy * player_speed)
        else:
            # Game over scenario when no path is found
            print("Game Over")
            pygame.quit()
            exit()



class Food:
    def __init__(self):
        self.img = pygame.image.load('img/food.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (TILE - 10, TILE - 10))
        self.rect = self.img.get_rect()
        self.set_pos()

    def set_pos(self):
        #self.rect.topleft = randrange(cols) * TILE + 5, randrange(rows) * TILE + 5
        # Set position to the bottom right corner
        self.rect.bottomright = (WIDTH, HEIGHT)
        self.rect.move_ip(-5, -5)  # Adjusting position slightly to fit within the border

    def draw(self):
        game_surface.blit(self.img, self.rect)


def is_collide(x, y):
    tmp_rect = player_rect.move(x, y)
    if tmp_rect.collidelist(walls_collide_list) == -1:
        return False
    return True


def eat_food():
    for food in food_list:
        if player_rect.collidepoint(food.rect.center):
            food.set_pos()
            return True
    return False


# def is_game_over():
#     global time, score, record, FPS
#     if time < 0:
#         pygame.time.wait(700)
#         player_rect.center = TILE // 2, TILE // 2
#         [food.set_pos() for food in food_list]
#         set_record(record, score)
#         record = get_record()
#         time, score, FPS = 60, 0, 

def is_game_over():
    global time, score, record, FPS
    if time < 0:
        pygame.time.wait(700)
        player_rect.center = TILE // 2, TILE // 2
        [food.set_pos() for food in food_list]
        set_record(record, score)
        record = get_record()
        time, score, FPS = 60, 0, 60
    else:
        # Check if either player reached the food
        for food in food_list:
            # Check if first player reached the food
            if player_rect.collidepoint(food.rect.center):
                # Game over scenario - First player wins
                surface.blit(text_font.render('Game Over, You Win!', True, pygame.Color('red'), True), (WIDTH + 30, 350))
                pygame.display.flip()
                pygame.time.wait(2000)  # Wait for 2 seconds before quitting
                pygame.quit()
                exit()
            # Check if second player reached the food
            elif second_player.rect.colliderect(food.rect):
                surface.blit(text_font.render('Game Over, AI Wins!', True, pygame.Color('red'), True), (WIDTH + 30, 350))
                pygame.display.flip()
                pygame.time.wait(2000)  # Wait for 2 seconds before quitting
                pygame.quit()
                exit()
                



def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')
            return 0


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))


FPS = 60
pygame.init()
game_surface = pygame.Surface(RES)
surface = pygame.display.set_mode((WIDTH + 300, HEIGHT))
clock = pygame.time.Clock()

# images
#bg_game = pygame.image.load('img/bg_1.jpg').convert()
bg = pygame.image.load('img/bg_main.jpg').convert()

#grass_green = (63,169,90) 
grass_green = (126, 219, 156)
# get maze
maze = generate_maze()


# player settings
player_speed = 5
player_img = pygame.image.load('img/morog.png').convert_alpha()
player_img = pygame.transform.scale(player_img, (TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))
player_rect = player_img.get_rect()
player_rect.center = TILE // 2, TILE // 2
directions = {pygame.K_LEFT: (-player_speed, 0), pygame.K_RIGHT: (player_speed, 0), pygame.K_UP: (0, -player_speed), pygame.K_DOWN: (0, player_speed)}
keys = {pygame.K_LEFT: pygame.K_LEFT, pygame.K_RIGHT: pygame.K_RIGHT, pygame.K_UP: pygame.K_UP, pygame.K_DOWN: pygame.K_DOWN}
direction = (0, 0)


# food settings
food_list = [Food() for i in range(3)]

# collision list
walls_collide_list = sum([cell.get_rects() for cell in maze], [])

# timer, score, record
pygame.time.set_timer(pygame.USEREVENT, 1000)

score = 0
record = get_record()

# fonts
font = pygame.font.SysFont('Impact', 50)
text_font = pygame.font.SysFont('Impact', 80)

# Second player settings
second_player = SecondPlayer()


while True:
    surface.blit(bg, (WIDTH, 0))
    surface.blit(game_surface, (0, 0))
    # game_surface.blit(bg_game, (0, 0))
    # Fill the game_surface with grassy-green color
    game_surface.fill(grass_green)

    # draw second player
    second_player.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.USEREVENT:
            time -= 1

     # Update start time and move second player after 40 seconds
    if start_time == 0:
        start_time = pygame.time.get_ticks() / 1000  # Get time in seconds
    
    # Check if time have passed
    current_time = pygame.time.get_ticks() / 1000
    if current_time - start_time >= 20:
        # Move the second player towards food
        for food in food_list:
            second_player.move_towards_food(food, maze)

    # controls and movement
    pressed_key = pygame.key.get_pressed()
    for key, key_value in keys.items():
        if pressed_key[key_value] and not is_collide(*directions[key]):
            direction = directions[key]
            break
    if not is_collide(*direction):
        player_rect.move_ip(direction)

    # draw maze
    [cell.draw(game_surface) for cell in maze]

    # gameplay
    if eat_food():
        FPS += 10
        score += 1
    is_game_over()

    # draw player
    game_surface.blit(player_img, player_rect)

    # draw food
    [food.draw() for food in food_list]

    # draw stats
    surface.blit(text_font.render('rooster/hen?', True, pygame.Color('gold'), None), (WIDTH + 0, 10))

    surface.blit(text_font.render('TIME', True, pygame.Color('cyan'), None), (WIDTH + 70, 100))
    surface.blit(font.render(f'{time}', True, pygame.Color('cyan'), None), (WIDTH + 70, 200))
    surface.blit(text_font.render('Result:', True, pygame.Color('forestgreen'), None), (WIDTH + 50, 350))
    surface.blit(font.render(f'{score}', True, pygame.Color('forestgreen'), None), (WIDTH + 70, 430))
    surface.blit(text_font.render('record:', True, pygame.Color('magenta'), None), (WIDTH + 30, 620))
    surface.blit(font.render(f'{record}', True, pygame.Color('magenta'), None), (WIDTH + 70, 700))

    #display "Player Win" or "AI Win"
    #result_text = "Player Win" if score > 0 else "AI Win"
    #surface.blit(font.render(result_text, True, pygame.Color('forestgreen'), None), (WIDTH + 70, 430))
#
    #surface.blit(text_font.render('record:', True, pygame.Color('magenta'), None), (WIDTH + 30, 620))
    #surface.blit(font.render(f'{record}', True, pygame.Color('magenta'), None), (WIDTH + 70, 700))


    pygame.display.flip()
    clock.tick(FPS)
