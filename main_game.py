import pygame
from menu_exemplars import layout, layout2, btn, btn2l
from settings import get_resolution
from random import randint, choice
import copy

all_sprites, picked_Tower, is_picked, cell_size_a = pygame.sprite.Group(), -1, False, (0, 0)


class Board:
    """
    :type Классическое клеточное игровое поле для TDшки.
    """

    def __init__(self, width, height, hp=50):
        """
        :param width: Ширина поля в клетках
        :param height: Высота поля в клетках
        """
        global cell_size_a
        self.board = [[1] * width for _ in range(height)]
        self.width, self.height = width, height
        self.hp = hp
        self.to_draw = []
        self.enemies_spawn = (0, 0)
        self.enemies = [[1] * width for _ in range(height)]
        for i in range(self.height):
            temp = []
            for j in range(self.width):
                temp.append(Sprite('Sprites/grass.png', (j, i), self))
            self.to_draw.append(copy.deepcopy(temp))
        self.left, self.top, self.cell_size = None, None, None
        self.size = width * height
        self.const_space = (width + height) // 20 / 10
        cell_size_a = self.set_view(width, height)
        self.generate_way()

    def generate_way(self, road_forks=1):
        """
        :param road_forks: Кол-во развилок. Оставьте 1. Не трогайте.
        :return: Занимается генерацией карты - self.board, ничего конкретного не возвращает.
        """
        path_length, temp = self.width * self.height // 4.5, []
        for i in range(self.height):
            for j in range(self.width):
                temp.append(Sprite('Sprites/grass.png', (j, i), self))
            self.to_draw.append(copy.deepcopy(temp))
            temp.clear()

        def new_way():
            # Сначала расставляет рейтинг клеток для создания развилки.
            # Потом создаёт её на основе полученного рейтинга.
            Rate_book = {}
            point_coord = (0, 0)
            for column in range(3, len(self.board) - 3):
                for row in range(3, len(self.board[column]) - 2):
                    if self.board[column][row] == 5 or \
                            self.board[column - 1][row] == 5 or \
                            self.board[column + 1][row] == 5 or \
                            self.board[column][row + 1] == 5 or \
                            self.board[column][row - 1] == 5 or \
                            self.board[column - 1][row - 1] == 5 or \
                            self.board[column - 1][row + 1] == 5 or \
                            self.board[column + 1][row + 1] == 5 or \
                            self.board[column + 1][row - 1] == 5:
                        continue
                    else:
                        if self.board[column][row + 2] == 5 or \
                                self.board[column][row - 2] == 5 or \
                                self.board[column - 1][row - 2] == 5 or \
                                self.board[column - 1][row + 2] == 5 or \
                                self.board[column + 1][row - 2] == 5 or \
                                self.board[column + 1][row - 2] == 5 or \
                                self.board[column + 2][row + 1] == 5 or \
                                self.board[column + 2][row - 1] == 5 or \
                                self.board[column + 2][row + 2] == 5 or \
                                self.board[column + 2][row - 2] == 5 or \
                                self.board[column + 2][row] == 5 or \
                                self.board[column - 2][row] == 5 or \
                                self.board[column - 2][row + 1] == 5 or \
                                self.board[column - 2][row - 1] == 5 or \
                                self.board[column - 2][row + 2] == 5 or \
                                self.board[column - 2][row - 2] == 5:
                            continue
                        else:
                            near = False
                        cell_in_line_counter = 0
                        try:
                            for ii in self.board[row]:
                                if ii == 5:
                                    cell_in_line_counter += 1
                            for ii in range(len(self.board)):
                                if self.board[ii][column] == 5:
                                    cell_in_line_counter += 1
                        except Exception:
                            continue
                        median = ((len(self.board)) // 2, len(self.board[0]) // 2)
                        gip = (abs(median[0] - row) ** 2 + abs(median[1] - column) ** 2) ** 0.5
                        if gip == 0:
                            if near is False:
                                Rate_book[(row, column)] = ((cell_in_line_counter / self.size), near)
                        else:
                            Rate_book[(row, column)] = ((cell_in_line_counter / self.size) * gip, near)

            if len(Rate_book.keys()) / (self.width * self.height) > self.const_space or len(Rate_book.keys()) == 0:
                print('No, there is too much free space, LoL. I`ll try again.')
                self.const_space += 0.02
                self.generate_way()
            else:
                temp_max_value = sorted(Rate_book.values(), reverse=True)[0]
                for key, value in Rate_book.items():
                    if value == temp_max_value:
                        point_coord = key
                        break
                # self.board[point_coord[1]][point_coord[0]] = 22
                minimum_distances = []
                for row in range(0, len(self.board)):
                    for column in range(3, self.width // 2 + 2):
                        near_cell_way_counter = 0
                        if self.board[row][column] == 5:
                            to_right = False
                            if self.board[row - 1][column] == 5 and self.board[row + 1][column] != 5:
                                near_cell_way_counter += 1
                            elif self.board[row + 1][column] == 5 and self.board[row - 1][column] != 5:
                                near_cell_way_counter += 1
                            if self.board[row][column + 1] == 5 and self.board[row][column - 1] != 5:
                                near_cell_way_counter += 1
                                to_right = True
                            elif self.board[row][column - 1] == 5 and self.board[row][column + 1] != 5:
                                near_cell_way_counter += 1
                                to_right = True
                            if near_cell_way_counter >= 2:
                                # self.board[row][column] = 22
                                go_up, go_down, go_left, go_right = False, False, False, False
                                if to_right and self.board[row + 1][column] == 5:
                                    if row < point_coord[1]:
                                        continue
                                    else:
                                        go_up = True
                                elif to_right and self.board[row - 1][column] == 5:
                                    if row > point_coord[1]:
                                        continue
                                    else:
                                        go_down = True
                                elif self.board[row][column - 1] == 5:
                                    go_right = True
                                else:
                                    go_right = True
                                gip = (abs(point_coord[0] - column) ** 2 + abs(point_coord[1] - row) ** 2) ** 0.5
                                if go_right:
                                    minimum_distances.append([gip, [row, column], 'go_right'])
                                elif go_down:
                                    minimum_distances.append([gip, [row, column], 'go_down'])
                                elif go_up:
                                    minimum_distances.append([gip, [row, column], 'go_up'])
                if minimum_distances:
                    final_start_fork = []
                    minimum_distances = sorted(minimum_distances, key=lambda x: x[0], reverse=True)
                    print(minimum_distances)
                    for minimum_distance in minimum_distances:
                        passed_fork = True
                        temp_distance = copy.deepcopy(minimum_distance)
                        point_coord = (point_coord[1], point_coord[0])
                        if minimum_distance[2] == 'go_right':
                            while point_coord[1] > minimum_distance[1][1]:
                                minimum_distance[1][1] += 1
                                if minimum_distance[1] != point_coord:
                                    if self.board[minimum_distance[1][0]][minimum_distance[1][1]] == 5:
                                        passed_fork = False
                                        print(f'{temp_distance[1]} failed at {minimum_distance[1]}')
                                        break
                            if minimum_distance != point_coord:
                                while point_coord[0] > minimum_distance[1][0]:
                                    minimum_distance[1][0] += 1
                                    if minimum_distance[1] != point_coord:
                                        if self.board[minimum_distance[1][0]][minimum_distance[1][1]] == 5:
                                            print(f'{temp_distance[1]} failed at {minimum_distance[1]}')
                                            passed_fork = False
                                            break
                                while point_coord[0] < minimum_distance[1][0]:
                                    minimum_distance[1][0] -= 1
                                    if minimum_distance[1] != point_coord:
                                        if self.board[minimum_distance[1][0]][minimum_distance[1][1]] == 5:
                                            passed_fork = False
                                            print(f'{temp_distance[1]} failed at {minimum_distance[1]}')
                                            break
                        elif minimum_distance[2] == 'go_down':
                            while point_coord[0] > minimum_distance[1][0]:
                                minimum_distance[1][0] += 1
                                if minimum_distance[1] != point_coord:
                                    if self.board[minimum_distance[1][0]][minimum_distance[1][1]] == 5:
                                        passed_fork = False
                                        print(f'{temp_distance[1]} failed at {minimum_distance[1]}')
                                        break
                            if minimum_distance != point_coord:
                                while point_coord[1] > minimum_distance[1][1]:
                                    minimum_distance[1][1] += 1
                                    if minimum_distance[1] != point_coord:
                                        if self.board[minimum_distance[1][0]][minimum_distance[1][1]] == 5:
                                            passed_fork = False
                                            print(f'{temp_distance[1]} failed at {minimum_distance[1]}')
                                            break
                        elif minimum_distance[2] == 'go_up':
                            while point_coord[0] < minimum_distance[1][0]:
                                minimum_distance[1][0] -= 1
                                if minimum_distance[1] != point_coord:
                                    if self.board[minimum_distance[1][0]][minimum_distance[1][1]] == 5:
                                        passed_fork = False
                                        print(f'{temp_distance[1]} failed at {minimum_distance[1]}')
                                        break
                            if minimum_distance != point_coord:
                                while point_coord[1] > minimum_distance[1][1]:
                                    minimum_distance[1][1] += 1
                                    if minimum_distance[1] != point_coord:
                                        if self.board[minimum_distance[1][0]][minimum_distance[1][1]] == 5:
                                            passed_fork = False
                                            print(f'{temp_distance[1]} failed at {minimum_distance[1]}')
                                            break
                        if passed_fork:
                            final_start_fork = temp_distance
                            print(final_start_fork)
                            break
                        else:
                            print('Fork should not pass')
                    if final_start_fork:
                        #  self.board[final_start_fork[1][0]][final_start_fork[1][1]] = 22
                        minimum_distance = final_start_fork
                        if point_coord[1] >= finish_pos[1] - 2:
                            self.generate_way()
                        else:
                            if minimum_distance[2] == 'go_right':
                                while point_coord[1] > minimum_distance[1][1]:
                                    minimum_distance[1][1] += 1
                                    self.board[minimum_distance[1][0]][minimum_distance[1][1]] = 5
                                    self.to_draw[minimum_distance[1][0]][minimum_distance[1][1]] = \
                                        Sprite(img="Sprites/dirt_clear.png",
                                               pos=(minimum_distance[1][0], minimum_distance[1][1]), board=self)
                                if minimum_distance != point_coord:
                                    while point_coord[0] > minimum_distance[1][0]:
                                        minimum_distance[1][0] += 1
                                        self.board[minimum_distance[1][0]][minimum_distance[1][1]] = 5
                                        self.to_draw[minimum_distance[1][0]][minimum_distance[1][1]] = \
                                            Sprite(img="Sprites/dirt_clear.png",
                                                   pos=(minimum_distance[1][0], minimum_distance[1][1]), board=self)
                                    while point_coord[0] < minimum_distance[1][0]:
                                        minimum_distance[1][0] -= 1
                                        self.board[minimum_distance[1][0]][minimum_distance[1][1]] = 5
                                        self.to_draw[minimum_distance[1][0]][minimum_distance[1][1]] = \
                                            Sprite(img="Sprites/dirt_clear.png",
                                                   pos=(minimum_distance[1][0], minimum_distance[1][1]), board=self)
                            elif minimum_distance[2] == 'go_down':
                                while point_coord[0] > minimum_distance[1][0]:
                                    minimum_distance[1][0] += 1
                                    self.board[minimum_distance[1][0]][minimum_distance[1][1]] = 5
                                    self.to_draw[minimum_distance[1][0]][minimum_distance[1][1]] = \
                                        Sprite(img="Sprites/dirt_clear.png",
                                               pos=(minimum_distance[1][0], minimum_distance[1][1]), board=self)
                                if minimum_distance != point_coord:
                                    while point_coord[1] > minimum_distance[1][1]:
                                        minimum_distance[1][1] += 1
                                        self.board[minimum_distance[1][0]][minimum_distance[1][1]] = 5
                                        self.to_draw[minimum_distance[1][0]][minimum_distance[1][1]] = \
                                            Sprite(img="Sprites/dirt_clear.png",
                                                   pos=(minimum_distance[1][0], minimum_distance[1][1]), board=self)
                            elif minimum_distance[2] == 'go_up':
                                while point_coord[0] < minimum_distance[1][0]:
                                    minimum_distance[1][0] -= 1
                                    self.board[minimum_distance[1][0]][minimum_distance[1][1]] = 5
                                    self.to_draw[minimum_distance[1][0]][minimum_distance[1][1]] = \
                                        Sprite(img="Sprites/dirt_clear.png",
                                               pos=(minimum_distance[1][0], minimum_distance[1][1]), board=self)
                                while point_coord[1] < minimum_distance[1][1]:
                                    minimum_distance[1][1] += 1
                                    try:
                                        self.board[minimum_distance[1][0]][minimum_distance[1][1]] = 5
                                        self.to_draw[current_pos[0]][current_pos[1]] = \
                                            Sprite(img="Sprites/dirt_clear.png",
                                                   pos=(current_pos[0], current_pos[1]), board=self)
                                    except IndexError:
                                        print('[!] Ignored error - IndexError. LoL =D')
                                        break
                            temp, cell_found = minimum_distance[1][1] + 1, False
                            while temp < self.width - 1:
                                self.board[minimum_distance[1][0]][temp] = 5
                                self.to_draw[minimum_distance[1][0]][temp] = \
                                    Sprite(img="Sprites/dirt_clear.png",
                                           pos=(minimum_distance[1][0], temp), board=self)
                                temp += 1
                                if self.board[minimum_distance[1][0] - 1][temp - 1] == 5 or \
                                        self.board[minimum_distance[1][0] + 1][temp - 1] == 5:
                                    cell_found = True
                                    break
                            if minimum_distance[1][1] == finish_pos[1]:
                                while minimum_distance[1][0] < finish_pos[0]:
                                    minimum_distance[1][0] += 1
                                    if self.board[minimum_distance[1][0]][minimum_distance[1][1]] == 5:
                                        break
                                    else:
                                        self.board[minimum_distance[1][0]][minimum_distance[1][1]] = 5
                                        self.to_draw[minimum_distance[1][0]][minimum_distance[1][1]] = \
                                            Sprite(img="Sprites/dirt_clear.png",
                                                   pos=(minimum_distance[1][0], minimum_distance[1][1]), board=self)
                                while minimum_distance[1][0] > finish_pos[0]:
                                    minimum_distance[1][0] -= 1
                                    if self.board[minimum_distance[1][0]][minimum_distance[1][1]] == 5:
                                        break
                                    else:
                                        self.board[minimum_distance[1][0]][minimum_distance[1][1]] = 5
                                        self.to_draw[minimum_distance[1][0]][minimum_distance[1][1]] = \
                                            Sprite(img="Sprites/dirt_clear.png",
                                                   pos=(minimum_distance[1][0], minimum_distance[1][1]), board=self)
                            try:
                                if not cell_found:
                                    if minimum_distance[1][0] > finish_pos[0]:
                                        print('>')
                                        while minimum_distance[1][0] != finish_pos[0]:
                                            minimum_distance[1][0] -= 1
                                            self.board[minimum_distance[1][0]][minimum_distance[1][1]] = 5
                                    else:
                                        print('<')
                                        while minimum_distance[1][0] != finish_pos[0]:
                                            minimum_distance[1][0] += 1
                                            self.board[minimum_distance[1][0]][minimum_distance[1][1]] = 5
                            except IndexError:
                                self.generate_way()
                                return
                            if minimum_distance[1] == finish_pos:
                                self.board[minimum_distance[1][0]][minimum_distance[1][1]] = 8
                    else:
                        print('Re-generate')
                        self.generate_way()
                else:
                    print('Re-generate')
                    self.generate_way()

        while True:
            fork, swap_direction, cells, direction_x, direction_y, space = 0, 0, 0, 1, 0, 0
            self.board = [[1] * self.width for _ in range(self.height)]
            self.to_draw = [[1] * self.width for _ in range(self.height)]
            y = randint(3, self.height - 2)
            self.board[y][1] = 9
            current_pos = (y, 1)
            self.enemies_spawn = (y, 1)
            self.to_draw[y][1] = Sprite('Sprites/spawn.png', current_pos, self)
            y = randint(2, self.height - 1)
            self.board[y][self.width - 2] = 8
            finish_pos = y, self.width - 2
            self.finish_pos = finish_pos
            while current_pos != finish_pos:
                if space == 0:
                    if swap_direction > 1:
                        if direction_x == 0:
                            temp_random = randint(1, 7)
                            if temp_random in range(1, 4):
                                direction_y = 0
                                direction_x = 1
                                space = 2
                        else:
                            temp_random = randint(1, 2)
                            direction_x = 0
                            if temp_random == 1:
                                direction_y = 1
                            else:
                                direction_y = -1
                        swap_direction = 0
                    else:
                        swap_direction += 1
                else:
                    space -= 1
                    swap_direction += 1

                if current_pos[0] + direction_y < 1:
                    direction_y = 0
                    direction_x = 1
                elif current_pos[0] + direction_y >= self.height - 1:
                    direction_y = 0
                    direction_x = 1

                if current_pos[1] + direction_x >= self.width:
                    direction_x = 0
                    if current_pos[0] > finish_pos[0]:
                        direction_y = -1
                    elif current_pos[0] < finish_pos[0]:
                        direction_y = 1
                    else:
                        cells += 1

                if current_pos[0] == 1:
                    if self.board[current_pos[0] + 1][current_pos[1] - 1] == 5:
                        direction_y = 0
                        direction_x = 1
                elif current_pos[0] == self.height - 2:
                    if self.board[current_pos[0] - 1][current_pos[1] - 1] == 5:
                        direction_y = 0
                        direction_x = 1
                if current_pos != finish_pos:
                    if current_pos[1] + 1 == finish_pos[1]:
                        direction_y = 0
                        direction_x = 1
                    elif current_pos[1] == finish_pos[1]:
                        direction_x = 0
                        if current_pos[0] > finish_pos[0]:
                            direction_y = -1
                        elif current_pos[0] < finish_pos[0]:
                            direction_y = 1
                    current_pos = (current_pos[0] + direction_y, current_pos[1] + direction_x)
                    cells += 1
                    self.board[current_pos[0]][current_pos[1]] = 5
                    self.to_draw[current_pos[0]][current_pos[1]] = \
                        Sprite(img="Sprites/dirt_clear.png",
                               pos=(current_pos[0], current_pos[1]), board=self)
                else:
                    break
            if path_length <= cells * 1.2:
                self.board[finish_pos[0]][finish_pos[1]] = 8
                self.to_draw[finish_pos[0]][finish_pos[1]] = \
                    Sprite(img="Sprites/base.png",
                           pos=(finish_pos[0], finish_pos[1]), board=self)
                for j in range(road_forks):
                    print('Trying to create fork')
                    new_way()
                    print('[+] Successfully')
                    for jj in range(len(self.board)):
                        for ii in range(len(self.board[jj])):
                            if self.board[jj][ii] == 1:
                                self.to_draw[jj][ii] = Sprite('Sprites/grass.png', (jj, ii), self)
                break
        # for i in self.board:
        # print(i)

    def set_view(self, w2, h2):
        w, h = get_resolution()
        self.left, self.top = w // 12, h // 12
        self.cell_size = ((w - w // 12) // w2, (h - h // 12) // h2)
        return self.cell_size

    def get_cell(self, mouse_pos):
        mouse_pos = mouse_pos[0] - self.left, mouse_pos[1] - self.top
        for i in range(self.height):
            for j in range(self.width):
                if self.cell_size[0] * j < mouse_pos[0] < self.cell_size[0] * (j + 1):
                    if self.cell_size[1] * i < mouse_pos[1] < self.cell_size[1] * (i + 1):
                        return j, i
        return None

    def render(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.to_draw[i][j].__class__ == Sprite:
                    if self.to_draw[i][j].img_draw is False:
                        self.to_draw[i][j].sprite_draw(self)

    def on_click(self, cell):
        global is_picked, need_to_draw
        need_to_draw = True
        if is_picked and self.board[cell[1]][cell[0]] == 1 and \
                0 < cell[1] < self.height and 2 < cell[0] < self.width - 1:
            self.to_draw[cell[1]][cell[0]] = Base_Tower(cell[::-1], self)
            self.board[cell[1]][cell[0]] = picked_Tower
            is_picked = False

    def get_click(self, event_pos):
        global need_to_render
        tmp = self.get_cell(event_pos)
        need_to_render = True
        if tmp:
            self.on_click(tmp)


class Base_Enemy:
    def __init__(self, pos, start_pos, board: Board, hp=10, speed=5, defense=0.1, dmg=1, img='Sprites/enemy.png'):
        global all_sprites
        pos = [pos[0], pos[1]]
        self.hp, self.speed, self.defense, self.pos, self.dmg = hp, speed, defense, pos, dmg
        self.prev_pos = pos
        self.direction = 0
        self.image = pygame.image.load(img)
        self.sprite = pygame.sprite.Sprite(all_sprites)
        self.sprite.image = self.image
        self.used_fork = False
        self.sprite.image = pygame.transform.scale(self.sprite.image,
                                                   (board.cell_size[0] // 3, board.cell_size[1] // 3))
        self.sprite.image.set_colorkey(-1)
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.x, self.sprite.rect.y = board.left + start_pos[1] * board.cell_size[0] + \
                                                 board.cell_size[0] // 2 - board.cell_size[0] // 6, \
                                                 board.top + start_pos[0] * board.cell_size[1] + \
                                                 board.cell_size[1] // 2 - board.cell_size[1] // 6

    def do_you_know_the_way(self, board: Board, direction):
        y = self.pos[0]
        if direction == -1:
            while y > 0:
                if board.board[y][self.pos[1] + 1] == 5:
                    return True
                y -= 1
        elif direction == 1:
            while y < board.height:
                if board.board[y][self.pos[1] + 1] == 5:
                    return True
                y += 1
        return False

    def chose_direction(self, board: Board):
        if board.board[self.pos[0]][self.pos[1] + 1] == 8:
            self.direction = 0
        elif self.pos[1] == board.finish_pos[0]:
            if self.pos[0] < board.finish_pos[1]:
                self.direction = 1
            else:
                self.direction = 0
        elif board.board[self.pos[0]][self.pos[1] + 1] == 5:
            if board.board[self.pos[0]][self.pos[1] - 1] == 5:
                if board.board[self.pos[0] + 1][self.pos[1]] == 5 and self.used_fork is False:
                    self.direction = choice([0, 1])
                    self.used_fork = True
                elif board.board[self.pos[0] - 1][self.pos[1]] == 5 and self.used_fork is False:
                    self.direction = choice([-1, 0])
                    self.used_fork = True
                else:
                    self.direction = 0
            elif board.board[self.pos[0] + 1][self.pos[1]] == 5 and self.direction == 1 and self.used_fork is False:
                self.direction = choice([0, 1])
                self.used_fork = True
            elif board.board[self.pos[0] - 1][self.pos[1]] == 5 and self.direction == -1 and self.used_fork is False:
                self.direction = choice([0, 1])
                self.used_fork = True
            else:
                self.direction = 0
        elif board.board[self.pos[0] + 1][self.pos[1]] == 5:
            if board.board[self.pos[0] - 1][self.pos[1]] == 5 and self.direction == 0 and not self.used_fork:
                self.direction = choice([-1, 1])
                self.used_fork = True
            elif board.board[self.pos[0] - 1][self.pos[1]] == 5 and self.direction == 0:
                if self.do_you_know_the_way(board, 1):
                    self.direction = 1
                else:
                    self.direction = -1
            elif self.direction == -1:
                pass
            else:
                self.direction = 1
        elif board.board[self.pos[0] - 1][self.pos[1]] == 5:
            if board.board[self.pos[0] + 1][self.pos[1]] == 5 and self.direction == 0 and not self.used_fork:
                self.direction = choice([-1, 1])
                self.used_fork = True
            elif self.direction == 0:
                self.direction = -1

    def move(self, board: Board):
        if self.hp > 0:
            x = (self.sprite.rect.x - board.left - board.cell_size[0] / 3 +
                 board.cell_size[0] // 6) // board.cell_size[0]
            y = (self.sprite.rect.y - board.top - board.cell_size[1] / 3 +
                 board.cell_size[1] // 6) // board.cell_size[1]
            if x != self.pos[1]:
                self.prev_pos = self.pos
                self.pos[1] = round(x)
                self.chose_direction(board)
            if y > self.pos[0]:
                self.prev_pos = self.pos
                self.pos[0] = round(y)
                self.chose_direction(board)
            else:
                if (self.sprite.rect.y - board.top - board.cell_size[1] / 3 +
                    board.cell_size[1] // 6 + board.cell_size[1] // 2) \
                        // board.cell_size[1] < self.pos[0]:
                    self.prev_pos = self.pos
                    self.pos[0] = round(y)
                    self.chose_direction(board)
            if (y, x) == board.finish_pos:
                board.hp -= self.dmg
                print(board.hp)
                self.hp = 0
            if self.direction == 0:
                self.sprite.rect = self.sprite.rect.move(self.speed, 0)
            else:
                self.sprite.rect = self.sprite.rect.move(0, self.speed * self.direction)
        else:
            self.sprite.kill()
            for i in board.enemies:
                if i == self:
                    i.remove(object=self)


class Base_Tower:
    def __init__(self, board_position, board, dmg=10, reload=1, shot_distance=2, projectile_speed=0.5, level=1,
                 img='Sprites/tb_1.png'):
        """
        :param dmg: Базовый урон башни
        :param reload: Время перезарядки
        :param shot_distance: Дальность поражения
        :param projectile_speed: Скорость полёта снаряда.
        """
        self.SPD = projectile_speed
        self.ATK = dmg
        self.RLD = reload
        self.S_DIS = shot_distance
        self.board_pos = board_position
        self.LVL = level
        self.img = img
        self.tower_draw(board)

    def tower_draw(self, board: Board):
        global screen, all_sprites
        sprite = pygame.sprite.Sprite()
        img = pygame.image.load(self.img)
        sprite.image = pygame.transform.scale(img, board.cell_size)
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = board.cell_size[0] * self.board_pos[1] + board.left
        sprite.rect.y = board.cell_size[1] * self.board_pos[0] + board.top
        all_sprites.add(sprite)


class Sprite:
    def __init__(self, img, pos, board):
        self.img, self.board_pos = img, pos
        self.img_draw = False

    def sprite_draw(self, game_map):
        self.img_draw = True
        sprite = pygame.sprite.Sprite()
        img = pygame.image.load(self.img)
        sprite.image = pygame.transform.scale(img, cell_size_a)
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = game_map.cell_size[0] * self.board_pos[1] + game_map.left
        sprite.rect.y = game_map.cell_size[1] * self.board_pos[0] + game_map.top
        all_sprites.add(sprite)


def start():
    global screen, need_to_render, all_sprites
    need_to_render = False
    temporary_xy = list(map(int, input("Кол-во клеток, x; y\n").split()))
    game_map = Board(temporary_xy[0], temporary_xy[1])
    pygame.init()
    screen = pygame.display.set_mode(get_resolution())
    running = True
    board_update(game_map, screen)
    start_pos = game_map.enemies_spawn
    while running:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                btn.get_clicked(event.pos)
                btn2l.get_clicked(event.pos)
                t = Base_Enemy(start_pos, start_pos, game_map)
                if game_map.enemies[start_pos[0]][start_pos[1]] == 1:
                    game_map.enemies[start_pos[0]][start_pos[1]] = [t]
                else:
                    game_map.enemies[start_pos[0]][start_pos[1]].append(t)
                game_map.get_click(event.pos)
        for i in game_map.enemies:
            for j in i:
                if j.__class__ == list:
                    for ii in j:
                        if ii.__class__ == Base_Enemy:
                            ii.move(game_map)
        board_update(game_map, screen)
        layout.show(screen)
        layout2.show(screen)

    pygame.quit()


def board_update(game_map: Board, screen_to_render):
    game_map.render()
    all_sprites.draw(screen_to_render)
