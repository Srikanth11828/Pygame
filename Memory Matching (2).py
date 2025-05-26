import pygame
import random
import time
import os
pygame.init()
WIDTH, HEIGHT = 800, 600
GRID_COLS, GRID_ROWS = 4, 4  
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LETTER_COLORS = [
    (255, 99, 71),   
    (60, 179, 113),  
    (65, 105, 225),   
    (238, 130, 238), 
    (255, 215, 0),  
    (70, 130, 180),  
    (255, 140, 0),   
    (147, 112, 219)   
]

TOTAL_HORIZONTAL_SPACE = WIDTH - 40 
TOTAL_VERTICAL_SPACE = HEIGHT - 100 
CARD_WIDTH = (TOTAL_HORIZONTAL_SPACE - (GRID_COLS - 1) * 10) // GRID_COLS
CARD_HEIGHT = (TOTAL_VERTICAL_SPACE - (GRID_ROWS - 1) * 10) // GRID_ROWS
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Matching Game")
font = pygame.font.SysFont('Arial', 72) 
small_font = pygame.font.SysFont('Arial', 36)


image_dir = r"C:\Users\user\Desktop\project\sri"
cover_image_path = os.path.join(image_dir, r"C:\Users\user\Desktop\project\sri.png")
cover_image = pygame.image.load(cover_image_path).convert_alpha()
cover_image = pygame.transform.smoothscale(cover_image, (CARD_WIDTH, CARD_HEIGHT))

cards = []
revealed = []
matched = []
first_card = None
second_card = None
game_started = False
start_time = 0
moves = 0
flip_back_time = None  
flip_delay = 1000  


letter_colors_map = {}

def create_cards():
    global cards, revealed, matched, letter_colors_map
    cards = []
    revealed = []
    matched = []
    letter_colors_map = {}


    symbols = [chr(65 + i) for i in range(GRID_COLS * GRID_ROWS // 2)] * 2
    random.shuffle(symbols)


    unique_letters = list(set(symbols))
    for i, letter in enumerate(unique_letters):
        letter_colors_map[letter] = LETTER_COLORS[i % len(LETTER_COLORS)]

    grid_width = GRID_COLS * CARD_WIDTH + (GRID_COLS - 1) * 10
    grid_height = GRID_ROWS * CARD_HEIGHT + (GRID_ROWS - 1) * 10
    start_x = (WIDTH - grid_width) // 2
    start_y = 70 

    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = start_x + col * (CARD_WIDTH + 10)
            y = start_y + row * (CARD_HEIGHT + 10)

            symbol = symbols.pop()
            cards.append({
                'rect': pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT),
                'symbol': symbol
            })
            revealed.append(False)
            matched.append(False)

def draw_card(i):
    card = cards[i]
    rect = card['rect']
    

    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=8)

    if revealed[i] or matched[i]:
        
        color = letter_colors_map[card['symbol']]
        pygame.draw.rect(screen, color, rect, border_radius=8)

    
        text = font.render(card['symbol'], True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
        pygame.draw.rect(screen, BLACK, rect, 2, border_radius=8)
    else:
    
        screen.blit(cover_image, rect)

def draw_cards():
    for i in range(len(cards)):
        draw_card(i)

def draw_info():
    elapsed = int(time.time() - start_time) if game_started else 0
    timer_text = small_font.render(f"Time: {elapsed}s", True, BLACK)
    moves_text = small_font.render(f"Moves: {moves}", True, BLACK)

    screen.blit(timer_text, (20, 20))
    screen.blit(moves_text, (WIDTH - 150, 20))

    if all(matched):
        congrats_text = small_font.render("Congratulations! You won!", True, (0, 128, 0))
        screen.blit(congrats_text, (WIDTH//2 - 130, HEIGHT - 40))

def reset_game():
    global first_card, second_card, game_started, start_time, moves, flip_back_time
    first_card = None
    second_card = None
    flip_back_time = None
    game_started = False
    start_time = 0
    moves = 0
    create_cards()

def main():
    global first_card, second_card, game_started, start_time, moves, flip_back_time

    clock = pygame.time.Clock()
    reset_game()
    running = True

    while running:
        screen.fill(WHITE)

        current_time = pygame.time.get_ticks() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not all(matched):
                pos = pygame.mouse.get_pos()


                if flip_back_time is None:
                    for i, card in enumerate(cards):
                        if card['rect'].collidepoint(pos) and not revealed[i] and not matched[i]:
                            if not game_started:
                                game_started = True
                                start_time = time.time()

                            if first_card is None:
                                first_card = i
                                revealed[i] = True
                            elif second_card is None and i != first_card:
                                second_card = i
                                revealed[i] = True
                                moves += 1
                                flip_back_time = current_time + flip_delay 
                            break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()

        
        if flip_back_time and current_time >= flip_back_time:
            if cards[first_card]['symbol'] != cards[second_card]['symbol']:
                revealed[first_card] = False
                revealed[second_card] = False
            else:
                matched[first_card] = True
                matched[second_card] = True

            first_card = None
            second_card = None
            flip_back_time = None

        draw_cards()
        draw_info()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
