import pygame
import random
import time
from tetramino import Tetromino
from constants import GRID_WIDTH, GRID_HEIGHT, SHAPE_NAMES, SHAPES, SHAPE_COLORS, SGRAY, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GRID_SIZE
from stats import save_stats, load_stats
from animations import LineClearAnimation


class TetrisGame:
    def __init__(self):
        # Инициализация всех атрибутов в конструкторе
        self.key_delay = 200
        self.key_interval = 50
        self.last_key_time = {"left": 0, "right": 0, "down": 0}
        self.stats_file = "ellatris_stats.json"
        self.stats = load_stats()
        self.font = pygame.font.SysFont('Arial', 24)
        self.big_font = pygame.font.SysFont('Arial', 36)
        self.small_font = pygame.font.SysFont('Arial', 18)

        # Инициализация игровых атрибутов
        self.board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.game_over = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_speed = 1.0
        self.last_fall_time = time.time()
        self.pieces_count = 0
        self.pieces_stats = {name: 0 for name in SHAPE_NAMES}
        self.animation = None
        self.is_animating = False
        self.shapes = SHAPES
        self.shape_colors = SHAPE_COLORS

        # Создание первых фигур
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()

    def reset_game(self):
        # Сброс всех игровых атрибутов к начальным значениям
        self.board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.game_over = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_speed = 1.0
        self.last_fall_time = time.time()
        self.pieces_count = 0
        self.pieces_stats = {name: 0 for name in SHAPE_NAMES}
        self.animation = None
        self.is_animating = False
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()

    def new_piece(self):
        shape_idx = random.randint(0, len(SHAPES) - 1)
        shape = SHAPES[shape_idx][0]

        self.pieces_count += 1
        self.pieces_stats[SHAPE_NAMES[shape_idx]] += 1
        self.stats["total_pieces"] += 1
        self.stats["pieces"][SHAPE_NAMES[shape_idx]] += 1

        return Tetromino(GRID_WIDTH // 2 - len(shape[0]) // 2, 0, shape_idx)

    def valid_move(self, piece, x, y, rotation=None):
        shape_to_check = SHAPES[piece.shape_idx][rotation] if rotation is not None else piece.shape

        for y_index, row in enumerate(shape_to_check):
            for x_index, cell in enumerate(row):
                if cell:
                    if (x + x_index < 0 or x + x_index >= GRID_WIDTH or
                            y + y_index >= GRID_HEIGHT or
                            (y + y_index >= 0 and self.board[y + y_index][x + x_index])):
                        return False
        return True

    def add_to_board(self, piece):
        for y_index, row in enumerate(piece.shape):
            for x_index, cell in enumerate(row):
                if cell and y_index + piece.y >= 0:
                    self.board[y_index + piece.y][x_index + piece.x] = piece.color

    def clear_lines(self):
        lines_to_clear = []
        for y_index in range(GRID_HEIGHT):
            if all(self.board[y_index]):
                lines_to_clear.append(y_index)

        if not lines_to_clear:
            return 0, []

        # Начисление очков
        if len(lines_to_clear) == 1:
            return 10, lines_to_clear
        elif len(lines_to_clear) == 2:
            return 15, lines_to_clear
        elif len(lines_to_clear) == 3:
            return 20, lines_to_clear
        elif len(lines_to_clear) == 4:
            return 50, lines_to_clear
        return 0, lines_to_clear

    def hard_drop(self):
        # Мгновенное падение фигуры
        while self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y + 1):
            self.current_piece.y += 1

        # Немедленно добавляем фигуру на доску и обрабатываем линии
        self.add_to_board(self.current_piece)
        lines_score, lines_cleared = self.clear_lines()

        if lines_cleared:
            # Есть линии для очистки - запускаем анимацию
            self.animation = LineClearAnimation(lines_cleared, self.board)
            self.score += lines_score
            self.lines_cleared += lines_score // 10
            self.level = self.score // 1000 + 1
            self.fall_speed = max(0.1, 1.0 - (self.level - 1) * 0.1)
        else:
            # Нет линий для очистки - продолжаем обычную игру
            self.current_piece = self.next_piece
            self.next_piece = self.new_piece()

            if not self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y):
                self.game_over = True
                self.stats["games_played"] += 1
                self.stats["total_score"] += self.score
                if self.score > self.stats["max_score"]:
                    self.stats["max_score"] = self.score
                save_stats(self.stats)

        # Сбрасываем таймер падения
        self.last_fall_time = time.time()

    def update(self):
        if self.game_over:
            return

        # Если есть активная анимация, обновляем только ее
        if self.animation:
            self.is_animating = True
            self.animation.update()
            if self.animation.completed:
                # После завершения анимации удаляем линии
                for line in self.animation.lines:
                    del self.board[line]
                    self.board.insert(0, [0 for _ in range(GRID_WIDTH)])
                self.animation = None
                self.is_animating = False

                # После анимации переходим к следующей фигуре
                self.current_piece = self.next_piece
                self.next_piece = self.new_piece()

                if not self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y):
                    self.game_over = True
                    self.stats["games_played"] += 1
                    self.stats["total_score"] += self.score
                    if self.score > self.stats["max_score"]:
                        self.stats["max_score"] = self.score
                    save_stats(self.stats)
            return

        # Обычное игровое обновление
        current_time = time.time()
        if current_time - self.last_fall_time > self.fall_speed:
            if self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y + 1):
                self.current_piece.y += 1
            else:
                self.add_to_board(self.current_piece)
                lines_score, lines_cleared = self.clear_lines()

                if lines_cleared:
                    # Есть линии для очистки - запускаем анимацию
                    self.animation = LineClearAnimation(lines_cleared, self.board)
                    self.score += lines_score
                    self.lines_cleared += lines_score // 10
                    self.level = self.score // 1000 + 1
                    self.fall_speed = max(0.1, 1.0 - (self.level - 1) * 0.1)
                else:
                    # Нет линий для очистки - продолжаем обычную игру
                    self.current_piece = self.next_piece
                    self.next_piece = self.new_piece()

                    if not self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y):
                        self.game_over = True
                        self.stats["games_played"] += 1
                        self.stats["total_score"] += self.score
                        if self.score > self.stats["max_score"]:
                            self.stats["max_score"] = self.score
                        save_stats(self.stats)

            self.last_fall_time = current_time

    def handle_input(self):
        # Блокируем управление во время анимации
        if self.is_animating:
            return

        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        # Обработка движения влево
        if keys[pygame.K_LEFT]:
            if current_time - self.last_key_time["left"] > (
            self.key_delay if self.last_key_time["left"] == 0 else self.key_interval):
                if self.valid_move(self.current_piece, self.current_piece.x - 1, self.current_piece.y):
                    self.current_piece.x -= 1
                self.last_key_time["left"] = current_time
        else:
            self.last_key_time["left"] = 0

        # Обработка движения вправо
        if keys[pygame.K_RIGHT]:
            if current_time - self.last_key_time["right"] > (
            self.key_delay if self.last_key_time["right"] == 0 else self.key_interval):
                if self.valid_move(self.current_piece, self.current_piece.x + 1, self.current_piece.y):
                    self.current_piece.x += 1
                self.last_key_time["right"] = current_time
        else:
            self.last_key_time["right"] = 0

        # Обработка движения вниз
        if keys[pygame.K_DOWN]:
            if current_time - self.last_key_time["down"] > (
            self.key_delay if self.last_key_time["down"] == 0 else self.key_interval):
                if self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y + 1):
                    self.current_piece.y += 1
                self.last_key_time["down"] = current_time
        else:
            self.last_key_time["down"] = 0

    def draw(self, screen):
        screen.fill(BLACK)

        # Рисование игрового поля
        pygame.draw.rect(screen, WHITE, (GRID_SIZE, GRID_SIZE, GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE), 2)

        # Рисование сетки
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                pygame.draw.rect(screen, SGRAY,
                                 (GRID_SIZE + x * GRID_SIZE, GRID_SIZE + y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

        # Рисование фигур на доске
        for y_index, row in enumerate(self.board):
            for x_index, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell,
                                     (GRID_SIZE + x_index * GRID_SIZE, GRID_SIZE + y_index * GRID_SIZE,
                                      GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(screen, WHITE,
                                     (GRID_SIZE + x_index * GRID_SIZE, GRID_SIZE + y_index * GRID_SIZE,
                                      GRID_SIZE, GRID_SIZE), 1)

        # Рисование текущей фигуры (только если нет анимации)
        if not self.game_over and not self.animation:
            for y_index, row in enumerate(self.current_piece.shape):
                for x_index, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(screen, self.current_piece.color,
                                         (GRID_SIZE + (self.current_piece.x + x_index) * GRID_SIZE,
                                          GRID_SIZE + (self.current_piece.y + y_index) * GRID_SIZE,
                                          GRID_SIZE, GRID_SIZE))
                        pygame.draw.rect(screen, WHITE,
                                         (GRID_SIZE + (self.current_piece.x + x_index) * GRID_SIZE,
                                          GRID_SIZE + (self.current_piece.y + y_index) * GRID_SIZE,
                                          GRID_SIZE, GRID_SIZE), 1)

        # Боковая панель
        sidebar_x = GRID_SIZE + GRID_WIDTH * GRID_SIZE + 20

        # Следующая фигура
        next_text = self.font.render("Следующая:", True, WHITE)
        screen.blit(next_text, (sidebar_x, GRID_SIZE))

        next_shape = self.next_piece.shape
        for y_index, row in enumerate(next_shape):
            for x_index, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.next_piece.color,
                                     (sidebar_x + x_index * GRID_SIZE,
                                      GRID_SIZE + 40 + y_index * GRID_SIZE,
                                      GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(screen, WHITE,
                                     (sidebar_x + x_index * GRID_SIZE,
                                      GRID_SIZE + 40 + y_index * GRID_SIZE,
                                      GRID_SIZE, GRID_SIZE), 1)

        # Очки и уровень
        score_text = self.font.render(f"Очки: {self.score}", True, WHITE)
        level_text = self.font.render(f"Уровень: {self.level}", True, WHITE)
        screen.blit(score_text, (sidebar_x, GRID_SIZE + 150))
        screen.blit(level_text, (sidebar_x, GRID_SIZE + 180))

        # Статистика текущей игры
        stats_title = self.font.render("Статистика игры:", True, WHITE)
        screen.blit(stats_title, (sidebar_x, GRID_SIZE + 220))

        pieces_text = self.font.render(f"Фигур: {self.pieces_count}", True, WHITE)
        screen.blit(pieces_text, (sidebar_x, GRID_SIZE + 250))

        # Процентное соотношение фигур
        y_offset = 280
        for name, count in self.pieces_stats.items():
            if self.pieces_count > 0:
                percentage = count / self.pieces_count * 100
                stat_text = self.small_font.render(f"{name}: {count} ({percentage:.1f}%)", True, WHITE)
                screen.blit(stat_text, (sidebar_x, GRID_SIZE + y_offset))
                y_offset += 20

        # Общая статистика
        if self.stats["total_pieces"] > 0:
            stats_title = self.font.render("Общая статистика:", True, WHITE)
            screen.blit(stats_title, (sidebar_x, GRID_SIZE + y_offset + 10))
            y_offset += 40

            total_text = self.small_font.render(f"Всего фигур: {self.stats['total_pieces']}", True, WHITE)
            screen.blit(total_text, (sidebar_x, GRID_SIZE + y_offset))
            y_offset += 20

            games_text = self.small_font.render(f"Игр сыграно: {self.stats['games_played']}", True, WHITE)
            screen.blit(games_text, (sidebar_x, GRID_SIZE + y_offset))
            y_offset += 20

            max_score_text = self.small_font.render(f"Рекорд: {self.stats['max_score']}", True, WHITE)
            screen.blit(max_score_text, (sidebar_x, GRID_SIZE + y_offset))

        # Если есть активная анимация, рисуем ее
        if self.animation:
            self.animation.draw(screen)

        # Сообщение о Game Over
        if self.game_over:
            game_over_text = self.big_font.render("ИГРА ЗАКОНЧЕНА", True, (255, 0, 0))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))

            # Подсказка о выходе в меню
            menu_hint = self.small_font.render("Нажмите M для выхода в меню", True, WHITE)
            screen.blit(menu_hint, (SCREEN_WIDTH // 2 - menu_hint.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    def save_stats(self):
        save_stats(self.stats)