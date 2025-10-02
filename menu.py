import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, GRAY, BLUE, GREEN, RED, VERSION, COPYRIGHT
from stats import load_stats

# Инициализация шрифтов
pygame.init()
font = pygame.font.SysFont('Arial', 24)
big_font = pygame.font.SysFont('Arial', 36)
small_font = pygame.font.SysFont('Arial', 18)


def draw_button(screen, rect, color, text):

    # Отрисовка кнопки с текстом
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

    # Горячая клавиша (если указана)
    # if hotkey:
    #    hotkey_text = small_font.render(f"({hotkey})", True, WHITE)
    #    hotkey_rect = hotkey_text.get_rect(midtop=(rect.centerx, rect.bottom + 5))
    #    screen.blit(hotkey_text, hotkey_rect)

    return rect


def main_menu(screen, clock):

    # Главное меню игры
    stats = load_stats()

    while True:
        screen.fill(BLACK)
        title = big_font.render("ELLATRIS", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        # Общая статистика в меню
        if stats["games_played"] > 0:
            total_text = font.render(f"Всего фигур: {stats['total_pieces']}", True, WHITE)
            games_text = font.render(f"Игр сыграно: {stats['games_played']}", True, WHITE)
            max_score_text = font.render(f"Рекорд: {stats['max_score']}", True, WHITE)

            screen.blit(total_text, (SCREEN_WIDTH // 2 - total_text.get_width() // 2, 100))
            screen.blit(games_text, (SCREEN_WIDTH // 2 - games_text.get_width() // 2, 130))
            screen.blit(max_score_text, (SCREEN_WIDTH // 2 - max_score_text.get_width() // 2, 160))

        # Кнопки
        new_game_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 220, 200, 50)
        highscores_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 290, 200, 50)
        exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 360, 200, 50)

        draw_button(screen, new_game_button, BLUE, "Новая игра (N)")
        draw_button(screen, highscores_button, GREEN, "Рекорды (R)")
        draw_button(screen, exit_button, RED, "Выход (E)")

        # Информация о версии и авторские права
        version_text = font.render(f"Версия {VERSION}", True, GRAY)
        copyright_text = font.render(COPYRIGHT, True, GRAY)
        screen.blit(version_text, (SCREEN_WIDTH - version_text.get_width() - 10,
                                   SCREEN_HEIGHT - version_text.get_height() - 30))
        screen.blit(copyright_text, (SCREEN_WIDTH - copyright_text.get_width() - 10,
                                     SCREEN_HEIGHT - copyright_text.get_height() - 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if new_game_button.collidepoint(mouse_pos):
                    return "new_game"
                elif highscores_button.collidepoint(mouse_pos):
                    return "highscores"
                elif exit_button.collidepoint(mouse_pos):
                    return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    return "new_game"
                elif event.key == pygame.K_r:
                    return "highscores"
                elif event.key == pygame.K_e:
                    return "quit"

        clock.tick(60)


def show_highscores(screen, clock):

    # Экран статистики и рекордов
    stats = load_stats()

    running = True
    while running:
        screen.fill(BLACK)
        title = big_font.render("СТАТИСТИКА", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        # Отображение статистики
        y_offset = 100
        stats_text = font.render(f"Всего игр: {stats['games_played']}", True, WHITE)
        screen.blit(stats_text, (SCREEN_WIDTH // 2 - stats_text.get_width() // 2, y_offset))
        y_offset += 40

        stats_text = font.render(f"Рекорд: {stats['max_score']}", True, WHITE)
        screen.blit(stats_text, (SCREEN_WIDTH // 2 - stats_text.get_width() // 2, y_offset))
        y_offset += 40

        stats_text = font.render(f"Всего фигур: {stats['total_pieces']}", True, WHITE)
        screen.blit(stats_text, (SCREEN_WIDTH // 2 - stats_text.get_width() // 2, y_offset))
        y_offset += 40

        # Статистика по фигурам
        if stats['total_pieces'] > 0:
            stats_text = font.render("Распределение фигур:", True, WHITE)
            screen.blit(stats_text, (SCREEN_WIDTH // 2 - stats_text.get_width() // 2, y_offset))
            y_offset += 40

            for name, count in stats['pieces'].items():
                percentage = count / stats['total_pieces'] * 100
                stat_text = small_font.render(f"{name}: {count} ({percentage:.1f}%)", True, WHITE)
                screen.blit(stat_text, (SCREEN_WIDTH // 2 - stat_text.get_width() // 2, y_offset))
                y_offset += 20

        back_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)
        draw_button(screen, back_button, BLUE, "Назад")

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        clock.tick(60)

    return "menu"