import pygame
import sys
import random
from collections import deque

from pygame.math import Vector2


class SNAKE:
    def __init__(self):
        self.body = [Vector2(10, 15), Vector2(9, 15), Vector2(8, 15)]  # Tạo rắn
        self.direction = Vector2(1, 0)  # Tạo hướng di chuyển ban đầu
        self.new_block = False  # Tạo biến khi rắn ăn mồi thì thêm 1 phần thân

        # THêm hình ảnh cho đầu rắn khi di chuyển các hướng khác nhau
        self.head = None
        self.head_up = pygame.image.load('Graphics/headup.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/headdown.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/headright.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/headleft.png').convert_alpha()

    # Hàm vẽ rắn
    def draw_snake(self):
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            if index == 0:
                screen.blit(self.update_head_graphics(), block_rect)
            else:
                screen.blit(body, block_rect)

    # Hàm kiểm tra hướng đi để chọn hình đầu rắn phù hợp
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            return self.head_left
        elif head_relation == Vector2(-1, 0):
            return self.head_right
        elif head_relation == Vector2(0, 1):
            return self.head_up
        elif head_relation == Vector2(0, -1):
            return self.head_down

    # Hàm di chuyển rắn
    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            print(self.body)

    # Hàm để biết thêm thân rắn
    def add_block(self):
        self.new_block = True

    # Hàm chọn hướng di chuyển đê đến thức ăn khi có vị trí hướng đi
    def move_towards_fruit(self, path):
        if path:
            next_cell = Vector2(path[0])
            if next_cell == self.body[0]:
                path.pop(0)
            else:
                direction = next_cell - self.body[0]
                self.direction = direction


class FRUIT:
    def __init__(self):
        self.pos = None
        self.y = None
        self.x = None
        self.randomize()
        self.sound = pygame.mixer.Sound("Audio/eat_sound.mp3")

    def draw_fruit(self):
        x_pos = int(self.pos.x * cell_size)
        y_pos = int(self.pos.y * cell_size)
        fruit_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

    def play_eat_sound(self):
        self.sound.play()


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    # Hàm để tạo các hoạt ảnh động của game
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    # Hàm vẽ elements của game (rắn, thức ăn)
    def draw_elements(self):
        while Vector2(self.fruit.pos) in self.snake.body:
            self.fruit.randomize()
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.play_eat_sound()
            self.fruit.randomize()
            self.snake.add_block()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            return False
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                return False

    def bfs(self):
        # Get the position of the snake's head and the fruit
        global current
        start = (int(self.snake.body[0].x), int(self.snake.body[0].y))
        end = (int(self.fruit.pos.x), int(self.fruit.pos.y))

        print("start", start)
        print("end", end)
        queue = deque()
        queue.append(start)
        visited = set()
        parent = {}
        found = False

        while queue:
            current = queue.popleft()
            if current == end:
                found = True
                break

            for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_pos = (current[0] + direction[0], current[1] + direction[1])

                if (
                        0 <= next_pos[0] < cell_number
                        and 0 <= next_pos[1] < cell_number
                        and next_pos not in visited
                        and Vector2(next_pos) not in self.snake.body
                ):
                    queue.append(next_pos)
                    visited.add(next_pos)
                    parent[next_pos] = current

        if found:
            path = []
            print("current", current)
            while current != start:
                path.append(current)
                current = parent[current]
            path.reverse()
            print(path)
            self.snake.move_towards_fruit(path)
            self.update()

    def dfs(self):
        # Get the position of the snake's head and the fruit
        global current
        start = (int(self.snake.body[0].x), int(self.snake.body[0].y))
        end = (int(self.fruit.pos.x), int(self.fruit.pos.y))

        print("start", start)
        print("end", end)
        stack = []
        stack.append(start)
        visited = set()
        parent = {}
        found = False

        while stack:
            current = stack.pop()
            if current == end:
                found = True
                break

            for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_pos = (current[0] + direction[0], current[1] + direction[1])

                if (
                        0 <= next_pos[0] < cell_number
                        and 0 <= next_pos[1] < cell_number
                        and next_pos not in visited
                        and Vector2(next_pos) not in self.snake.body
                ):
                    stack.append(next_pos)
                    visited.add(next_pos)
                    parent[next_pos] = current

        if found:
            path = []
            while current != start:
                path.append(current)
                current = parent[current]
            path.reverse()
            print(path)
            self.snake.move_towards_fruit(path)
            self.update()


class DISPLAY:
    def __init__(self):
        self.button_start = pygame.Rect(490, 400, 192, 64)
        self.button_restart = pygame.Rect(900, 200, 192, 64)
        self.button_run = pygame.Rect(900, 300, 192, 64)
        self.button_pause = pygame.Rect(900, 400, 192, 64)
        self.button_exit = pygame.Rect(900, 500, 192, 64)
        self.button_bfs = pygame.Rect(850, 600, 60, 40)
        self.button_dfs = pygame.Rect(950, 600, 60, 40)
        self.button_Astar = pygame.Rect(1050, 600, 60, 40)
        self.button_GBFS = pygame.Rect(850, 650, 60, 40)
        self.button_UCS = pygame.Rect(950, 650, 60, 40)
        self.button_HCB = pygame.Rect(1050, 650, 60, 40)
        self.button_Dijkstra = pygame.Rect(950, 700, 60, 40)

        self.logo = pygame.Rect(420, 20, 360, 360)

        self.menu = pygame.Rect(800, 0, 400, 800)
        self.font = pygame.font.Font(None, 36)

        self.game_run = False
        self.snake_run = False

        self.snake_runBFS = False
        self.snake_runDFS = False
        self.snake_runAstar = False
        self.snake_runGBFS = False
        self.snake_runUCS = False
        self.snake_runHCB = False
        self.snake_runDijkstra = False

    def draw(self):
        text = self.font.render(f"Nhóm 4: Le Tan - Dang Huy Dieu - Pham Quoc Trung", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.topleft = (300, 600)  # Đặt vị trí hiển thị của văn bản
        screen.blit(text, text_rect)  # Vẽ văn bản lên screen

        screen.blit(logo, self.logo)
        screen.blit(start, self.button_start)

    def draw_menu(self, score):
        pygame.draw.rect(screen, (175, 215, 70), self.menu)
        self.draw_score(score)

        pygame.draw.rect(screen, (126, 166, 114), self.button_restart)
        text_restart = self.font.render("Restart", True, (0, 0, 0))
        text_restart_rect = text_restart.get_rect(center=self.button_restart.center)
        screen.blit(text_restart, text_restart_rect)

        pygame.draw.rect(screen, (126, 166, 114), self.button_pause)
        text_pause = self.font.render("Pause", True, (0, 0, 0))
        text_pause_rect = text_pause.get_rect(center=self.button_pause.center)
        screen.blit(text_pause, text_pause_rect)

        pygame.draw.rect(screen, (126, 166, 114), self.button_run)
        text_run = self.font.render("Run", True, (0, 0, 0))
        text_run_rect = text_run.get_rect(center=self.button_run.center)
        screen.blit(text_run, text_run_rect)

        pygame.draw.rect(screen, (126, 166, 114), self.button_exit)
        text_exit = self.font.render("EXIT", True, (0, 0, 0))
        text_exit_rect = text_exit.get_rect(center=self.button_exit.center)
        screen.blit(text_exit, text_exit_rect)

        pygame.draw.rect(screen, (126, 166, 114), self.button_bfs)
        text_bfs = self.font.render("BFS", True, (0, 0, 0))
        text_bfs_rect = text_bfs.get_rect(center=self.button_bfs.center)
        screen.blit(text_bfs, text_bfs_rect)

        pygame.draw.rect(screen, (126, 166, 114), self.button_dfs)
        text_dfs = self.font.render("DFS", True, (0, 0, 0))
        text_dfs_rect = text_dfs.get_rect(center=self.button_dfs.center)
        screen.blit(text_dfs, text_dfs_rect)

        pygame.draw.rect(screen, (126, 166, 114), self.button_Astar)
        text_Astar = self.font.render("A*", True, (0, 0, 0))
        text_Astar_rect = text_Astar.get_rect(center=self.button_Astar.center)
        screen.blit(text_Astar, text_Astar_rect)

        pygame.draw.rect(screen, (126, 166, 114), self.button_GBFS)
        text_GBFS = self.font.render("GBFS", True, (0, 0, 0))
        text_GBFS_rect = text_GBFS.get_rect(center=self.button_GBFS.center)
        screen.blit(text_GBFS, text_GBFS_rect)

        pygame.draw.rect(screen, (126, 166, 114), self.button_UCS)
        text_UCS = self.font.render("UCS", True, (0, 0, 0))
        text_UCS_rect = text_UCS.get_rect(center=self.button_UCS.center)
        screen.blit(text_UCS, text_UCS_rect)

        pygame.draw.rect(screen, (126, 166, 114), self.button_HCB)
        text_HCB = self.font.render("HCB", True, (0, 0, 0))
        text_HCB_rect = text_HCB.get_rect(center=self.button_HCB.center)
        screen.blit(text_HCB, text_HCB_rect)

    def draw_score(self, score):
        text = self.font.render(f"Score: {score}", True, (255, 0, 0))
        text_rect = text.get_rect()
        text_rect.topleft = (950, 100)  # Đặt vị trí hiển thị của văn bản
        screen.blit(text, text_rect)  # Vẽ văn bản lên self.menu


pygame.init()
# Tạo cửa sổ trò chơi
cell_size = 20  # số lượng pixel của 1 ô
cell_number = 40  # số lượng ô
screen = pygame.display.set_mode(((cell_number + 20) * cell_size, cell_number * cell_size))
pygame.display.set_caption('SnakeAI')
clock = pygame.time.Clock()
logo = pygame.image.load('Graphics/logo.png').convert_alpha()
start = pygame.image.load('Graphics/button_start.png').convert_alpha()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
body = pygame.image.load('Graphics/body.png').convert_alpha()
font = pygame.font.Font(None, 36)

main_game = MAIN()
main_display = DISPLAY()

# Điều chỉnh tốc độ của rắn
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 50)  # Số càng nhỏ càng nhanh

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not main_display.game_run:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_display.button_start.collidepoint(event.pos):
                    # Thực hiện hành động khi nút "Start" được nhấn
                    main_display.game_run = True
                    print("Nút 'Start' đã được nhấn!")
        if main_display.game_run:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_display.button_run.collidepoint(event.pos):
                    # Thực hiện hành động khi nút "Start" được nhấn
                    main_display.snake_run = True
                    print("Nút 'Run' đã được nhấn!")
            if (
                    main_display.snake_run is True
                    and main_display.snake_runBFS is False
                    and main_display.snake_runDFS is False
            ):
                if event.type == SCREEN_UPDATE:
                    main_game.update()
                    main_display.draw_score(len(main_game.snake.body) - 3)
                    print(len(main_game.snake.body) - 3)
                    if main_game.check_fail() == False:
                        main_display.snake_run = False
                        main_game.snake.__init__()
            if main_display.snake_run is True and main_display.snake_runBFS is True:
                if event.type == SCREEN_UPDATE:
                    main_game.bfs()
                    main_display.draw_score(len(main_game.snake.body) - 3)
                    print(len(main_game.snake.body) - 3)
                    if main_game.check_fail() == False:
                        main_display.snake_run = False
                        main_game.snake.__init__()
            if main_display.snake_run is True and main_display.snake_runDFS is True:
                if event.type == SCREEN_UPDATE:
                    main_game.dfs()
                    main_display.draw_score(len(main_game.snake.body) - 3)
                    print(len(main_game.snake.body) - 3)
                    if main_game.check_fail() == False:
                        main_display.snake_run = False
                        main_game.snake.__init__()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_display.button_exit.collidepoint(event.pos):
                    main_display.game_run = False
                    main_display.snake_run = False
                    main_game.snake.__init__()
                    print("Exit")
                if main_display.button_restart.collidepoint(event.pos):
                    main_display.snake_run = False
                    main_display.snake_runBFS = False
                    main_display.snake_runDFS = False
                    main_game.snake.__init__()
                    print("restart")
                if main_display.button_pause.collidepoint(event.pos):
                    main_display.snake_run = False
                    print("pause")
                if main_display.button_bfs.collidepoint(event.pos):
                    main_display.snake_runBFS = True
                    main_display.snake_run = True
                    print("bfs")
                if main_display.button_dfs.collidepoint(event.pos):
                    main_display.snake_runDFS = True
                    main_display.snake_run = True
                    print("dfs")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
    screen.fill((0, 0, 0))
    if not main_display.game_run:
        main_display.draw()
    if main_display.game_run:
        main_display.draw_menu(len(main_game.snake.body) - 3)
        main_game.draw_elements()
    pygame.display.update()
    clock.tick(144)
