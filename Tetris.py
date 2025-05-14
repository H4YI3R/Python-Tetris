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
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
]

def create_board():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

def draw_block(screen, shape, x, y):
    for row_idx, row in enumerate(shape):
        for col_idx, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    BLUE,
                    (x + col_idx * BLOCK_SIZE, y + row_idx * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                )

def draw_board(screen, board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    BLUE,
                    (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                )

def check_collision(board, shape, x, y):
    for row_idx, row in enumerate(shape):
        for col_idx, cell in enumerate(row):
            if cell:
                board_x = (x // BLOCK_SIZE) + col_idx
                board_y = (y // BLOCK_SIZE) + row_idx
                if board_x < 0 or board_x >= COLS or board_y >= ROWS:
                    return True
                if board_y >= 0 and board[board_y][board_x]:
                    return True
    return False

def place_block(board, shape, x, y):
    for row_idx, row in enumerate(shape):
        for col_idx, cell in enumerate(row):
            if cell:
                board_x = (x // BLOCK_SIZE) + col_idx
                board_y = (y // BLOCK_SIZE) + row_idx
                if 0 <= board_x < COLS and 0 <= board_y < ROWS:
                    board[board_y][board_x] = 1
# 방향 전환 함수
def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]

# 줄 삭제 함수
def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = ROWS - len(new_board)
    for _ in range(lines_cleared):
        new_board.insert(0, [0] * COLS)
    return new_board, lines_cleared

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tetris')

    clock = pygame.time.Clock()
    board = create_board()
    running = True

    current_block = random.choice(SHAPES)
    block_x, block_y = 4 * BLOCK_SIZE, 0

    drop_timer = 0
    move_delay = 150  # ms
    last_move_time = pygame.time.get_ticks()
    last_rotate_time = pygame.time.get_ticks()

    while running:
        screen.fill(BLACK)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 한 번만 처리되는 이벤트 (회전)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if current_time - last_rotate_time > move_delay:
                        rotated_block = rotate(current_block)
                        if not check_collision(board, rotated_block, block_x, block_y):
                            current_block = rotated_block
                        last_rotate_time = current_time

        # 키가 계속 눌려 있는 상태에 대해 일정 시간 간격으로만 반응
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and current_time - last_move_time > move_delay:
            if not check_collision(board, current_block, block_x - BLOCK_SIZE, block_y):
                block_x -= BLOCK_SIZE
                last_move_time = current_time
        if keys[pygame.K_RIGHT] and current_time - last_move_time > move_delay:
            if not check_collision(board, current_block, block_x + BLOCK_SIZE, block_y):
                block_x += BLOCK_SIZE
                last_move_time = current_time
        if keys[pygame.K_DOWN] and current_time - last_move_time > move_delay:
            if not check_collision(board, current_block, block_x, block_y + BLOCK_SIZE):
                block_y += BLOCK_SIZE
                last_move_time = current_time

        # 자동 낙하
        drop_timer += clock.get_time()
        if drop_timer > 500:
            if not check_collision(board, current_block, block_x, block_y + BLOCK_SIZE):
                block_y += BLOCK_SIZE
            else:
                place_block(board, current_block, block_x, block_y)
                board, _ = clear_lines(board)
                current_block = random.choice(SHAPES)
                block_x, block_y = 4 * BLOCK_SIZE, 0
                if check_collision(board, current_block, block_x, block_y):
                    print("Game Over")
                    running = False
            drop_timer = 0

        draw_board(screen, board)
        draw_block(screen, current_block, block_x, block_y)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
