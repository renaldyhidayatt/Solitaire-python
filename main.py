import pygame
from Deck import Deck
from ui import Button
import history_manager

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 200, 0)
blue = (50, 50, 190)
red = (100, 50, 50)
grey = (100, 100, 100)  # RGB code

display_dimensions = (1100, 800)

pygame.init()
game_display = pygame.display.set_mode(display_dimensions)

clock = pygame.time.Clock()
FPS = 10  # framerate


def quit_game():
    pygame.quit()
    quit()


def game_loop():

    undo_button = Button(
        display_dimensions,
        "Undo",
        (10, 10),
        (30, 30),
        grey,
        centered=False,
        text_size=11,
        action="undo",
    )
    pause_button = Button(
        display_dimensions,
        "Pause",
        (display_dimensions[0] - 50, 10),
        (40, 30),
        grey,
        centered=False,
        text_size=10,
        action="pause",
    )

    buttons = [undo_button, pause_button]
    deck = Deck()
    deck.load_cards()
    deck.shuffle_cards()
    deck.load_piles(display_dimensions)
    hm = history_manager.HistoryManager(deck)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()

                elif event.key == pygame.K_w:
                    pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    piles_to_update, valid_move = deck.handle_click(mouse_pos)
                    deck.update(piles_to_update, display_dimensions[1])
                    if valid_move:
                        hm.valid_move_made(deck)

                    for button in buttons:
                        if button.check_if_clicked(mouse_pos):
                            if button.action == "undo":
                                deck = hm.undo(deck)

                if event.button == 3:
                    deck.handle_right_click(mouse_pos)

        game_display.fill(blue)

        for button in buttons:
            button.display(game_display, pygame.mouse.get_pos())
        deck.display(game_display)
        pygame.display.update()
        clock.tick(FPS)


game_loop()
