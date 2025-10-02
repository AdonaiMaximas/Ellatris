import pygame
import random
from constants import GRID_SIZE, GRID_WIDTH


class LineClearAnimation:
    def __init__(self, lines, board):
        self.lines = lines
        self.board = board
        self.progress = 0
        self.max_progress = 25  # Уменьшил количество кадров анимации (было 30)
        self.completed = False
        self.animation_type = random.choice(["center", "left", "right", "random"])

        # Сохраняем оригинальные цвета линий для анимации
        self.original_colors = {}
        for line in lines:
            self.original_colors[line] = self.board[line][:]

    def update(self):
        self.progress += 2  # Увеличиваем прогресс быстрее (было += 1)
        if self.progress >= self.max_progress:
            self.completed = True

    def draw(self, screen):
        if self.completed:
            return

        # Разные типы анимации
        if self.animation_type == "center":
            self._draw_center_animation(screen)
        elif self.animation_type == "left":
            self._draw_left_animation(screen)
        elif self.animation_type == "right":
            self._draw_right_animation(screen)
        else:
            self._draw_random_animation(screen)

    def _draw_center_animation(self, screen):
        progress_factor = self.progress / self.max_progress
        center = GRID_WIDTH // 2
        clear_width = int(GRID_WIDTH * progress_factor)

        start_x = max(0, center - clear_width // 2)
        end_x = min(GRID_WIDTH, center + clear_width // 2)

        for line in self.lines:
            for x in range(GRID_WIDTH):
                if x < start_x or x >= end_x:
                    # Рисуем обычную клетку
                    if self.original_colors[line][x]:
                        pygame.draw.rect(screen, self.original_colors[line][x],
                                         (GRID_SIZE + x * GRID_SIZE,
                                          GRID_SIZE + line * GRID_SIZE,
                                          GRID_SIZE, GRID_SIZE))
                else:
                    # Рисуем анимацию очистки
                    alpha = int(255 * (1 - progress_factor))  # Преобразуем в int
                    color = self.original_colors[line][x]
                    if color:
                        s = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
                        s.fill((color[0], color[1], color[2], alpha))
                        screen.blit(s, (GRID_SIZE + x * GRID_SIZE,
                                        GRID_SIZE + line * GRID_SIZE))

    def _draw_left_animation(self, screen):
        progress_factor = self.progress / self.max_progress
        clear_width = int(GRID_WIDTH * progress_factor)

        for line in self.lines:
            for x in range(GRID_WIDTH):
                if x >= clear_width:
                    # Рисуем обычную клетку
                    if self.original_colors[line][x]:
                        pygame.draw.rect(screen, self.original_colors[line][x],
                                         (GRID_SIZE + x * GRID_SIZE,
                                          GRID_SIZE + line * GRID_SIZE,
                                          GRID_SIZE, GRID_SIZE))
                else:
                    # Рисуем анимацию очистки
                    alpha = int(255 * (1 - progress_factor))  # Преобразуем в int
                    color = self.original_colors[line][x]
                    if color:
                        s = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
                        s.fill((color[0], color[1], color[2], alpha))
                        screen.blit(s, (GRID_SIZE + x * GRID_SIZE,
                                        GRID_SIZE + line * GRID_SIZE))

    def _draw_right_animation(self, screen):
        progress_factor = self.progress / self.max_progress
        clear_width = int(GRID_WIDTH * progress_factor)
        start_x = GRID_WIDTH - clear_width

        for line in self.lines:
            for x in range(GRID_WIDTH):
                if x < start_x:
                    # Рисуем обычную клетку
                    if self.original_colors[line][x]:
                        pygame.draw.rect(screen, self.original_colors[line][x],
                                         (GRID_SIZE + x * GRID_SIZE,
                                          GRID_SIZE + line * GRID_SIZE,
                                          GRID_SIZE, GRID_SIZE))
                else:
                    # Рисуем анимацию очистки
                    alpha = int(255 * (1 - progress_factor))  # Преобразуем в int
                    color = self.original_colors[line][x]
                    if color:
                        s = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
                        s.fill((color[0], color[1], color[2], alpha))
                        screen.blit(s, (GRID_SIZE + x * GRID_SIZE,
                                        GRID_SIZE + line * GRID_SIZE))

    def _draw_random_animation(self, screen):
        progress_factor = self.progress / self.max_progress

        for line in self.lines:
            for x in range(GRID_WIDTH):
                # Случайный порог для каждой клетки
                cell_threshold = (x + line) % GRID_WIDTH / GRID_WIDTH

                if progress_factor < cell_threshold:
                    # Рисуем обычную клетку
                    if self.original_colors[line][x]:
                        pygame.draw.rect(screen, self.original_colors[line][x],
                                         (GRID_SIZE + x * GRID_SIZE,
                                          GRID_SIZE + line * GRID_SIZE,
                                          GRID_SIZE, GRID_SIZE))
                else:
                    # Рисуем анимацию очистки
                    alpha = int(255 * (1 - min(1, progress_factor / max(0.1, cell_threshold))))  # Преобразуем в int
                    color = self.original_colors[line][x]
                    if color:
                        s = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
                        s.fill((color[0], color[1], color[2], alpha))
                        screen.blit(s, (GRID_SIZE + x * GRID_SIZE,
                                        GRID_SIZE + line * GRID_SIZE))