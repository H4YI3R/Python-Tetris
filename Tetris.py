import pygame
import random

# Pygame 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 300, 600
ROWS, COLS = 20, 10
BLOCK_SIZE = WIDTH // COLS

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# 블록 모양 정의 (I, O, T, S, Z, L, J)
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1,1]],
    [[0, 1, 0], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
]

# 게임 보드 초기화
def creat_board():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

# 블록 그리기 함수
def draw_block(screen, shape, x, y):
    for row_idx, row in enumerate(shape):
        for col_idx, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    BLUE,
                    (x + col_idx * BLOCK_SIZE, y + row_idx * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                )

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tetris')

    clock = pygame.time.Clock()
    board = creat_board()
    running = True

    current_block = random.choice(SHAPES)
    block_x, block_y = 4 * BLOCK_SIZE, 0

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 블록 이동 로직
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            block_x -= BLOCK_SIZE
        if keys[pygame.K_RIGHT]:
            block_x += BLOCK_SIZE
        if keys[pygame.K_DOWN]:
            block_y += BLOCK_SIZE

        # 게임 보드와 블록 그리기
        draw_block(screen, current_block, block_x, block_y)

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
if __name__ == '__main__':
    main()