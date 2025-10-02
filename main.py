import pygame
from menu import main_menu, show_highscores
from game import TetrisGame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE


def game_loop(screen, clock):
    # Основной игровой цикл
    game = TetrisGame()
    running = True
    paused = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.save_stats()
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

                # Выход в меню по нажатию M во время паузы
                if paused and event.key == pygame.K_m:
                    game.save_stats()
                    return "menu"

                if not paused and not game.game_over:
                    if event.key == pygame.K_UP:
                        old_rotation = game.current_piece.rotation
                        new_rotation = (game.current_piece.rotation + 1) % 4
                        if game.valid_move(game.current_piece, game.current_piece.x, game.current_piece.y,
                                           new_rotation):
                            game.current_piece.rotation = new_rotation
                            game.current_piece.shape = game.shapes[game.current_piece.shape_idx][new_rotation]
                        else:
                            game.current_piece.rotation = old_rotation
                            game.current_piece.shape = game.shapes[game.current_piece.shape_idx][old_rotation]
                    elif event.key == pygame.K_SPACE:
                        # Используем мгновенное падение вместо постепенного
                        game.hard_drop()

        if not paused:
            game.handle_input()
            game.update()

        game.draw(screen)

        if paused:
            pause_text = game.big_font.render("ПАУЗА", True, WHITE)
            screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2))
            menu_hint = game.small_font.render("Нажмите M для выхода в меню", True, WHITE)
            screen.blit(menu_hint, (SCREEN_WIDTH // 2 - menu_hint.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()
        clock.tick(60)

        if game.game_over:
            pygame.time.delay(2000)
            running = False

    return "menu"


def main():

    # Главная функция приложения
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ELLATRIS")
    clock = pygame.time.Clock()
    # Установка иконки окна
    try:
        icon = pygame.image.load('icon.png')
        pygame.display.set_icon(icon)
    except:
        print("Не удалось загрузить иконку. Используется стандартная иконка Pygame.")

    current_screen = "menu"

    while current_screen != "quit":
        if current_screen == "menu":
            current_screen = main_menu(screen, clock)
        elif current_screen == "new_game":
            current_screen = game_loop(screen, clock)
        elif current_screen == "highscores":
            current_screen = show_highscores(screen, clock)

    pygame.quit()


if __name__ == "__main__":
    main()