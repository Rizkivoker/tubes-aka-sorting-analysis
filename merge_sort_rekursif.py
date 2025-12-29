import pygame
import random
import sys
import numpy as np


# CONFIG

WIDTH, HEIGHT = 1000, 500
FPS = 120

BAR_COLOR = (255, 255, 255)
ACTIVE_COLOR = (255, 0, 0)
FINAL_COLOR = (0, 255, 0)
BG_COLOR = (0, 0, 0)

MIN_VAL = 10
MAX_VAL = 90


# STATE

STATE_INPUT = -1
STATE_SORTING = 0
STATE_FINAL_SWEEP = 1
STATE_DONE = 2


# INIT

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Merge Sort Visualization")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 28)


# SOUND POOL

def generate_sounds():
    sounds = {}
    sample_rate = 44100
    duration = 0.04

    for v in range(MIN_VAL, MAX_VAL + 1):
        freq = 200 + v * 6
        t = np.linspace(0, duration, int(sample_rate * duration))
        wave = 32767 * np.sin(2 * np.pi * freq * t)
        stereo = np.column_stack((wave, wave))
        sounds[v] = pygame.sndarray.make_sound(stereo.astype(np.int16))

    return sounds

sound_pool = generate_sounds()


# DRAW

def draw_bars(data, active=None, final_index=-1):
    screen.fill(BG_COLOR)
    bar_width = WIDTH // len(data)

    for i, val in enumerate(data):
        x = i * bar_width
        h = val * 5
        y = HEIGHT - h

        if i <= final_index:
            color = FINAL_COLOR
        elif i == active:
            color = ACTIVE_COLOR
        else:
            color = BAR_COLOR

        pygame.draw.rect(screen, color, (x, y, bar_width - 1, h))

def draw_input(text):
    screen.fill(BG_COLOR)
    title = font.render("MERGE SORT VISUALIZATION", True, (0, 255, 255))
    prompt = font.render("Masukkan jumlah data (n):", True, (255, 255, 255))
    box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 40)

    pygame.draw.rect(screen, (255, 255, 255), box, 2)
    input_text = font.render(text, True, (0, 255, 0))

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
    screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(input_text, (box.x + 10, box.y + 5))


# MERGE SORT (GENERATOR)

def merge_sort(arr, l, r):
    if l >= r:
        return
    mid = (l + r) // 2
    yield from merge_sort(arr, l, mid)
    yield from merge_sort(arr, mid + 1, r)
    yield from merge(arr, l, mid, r)

def merge(arr, l, mid, r):
    left = arr[l:mid + 1]
    right = arr[mid + 1:r + 1]

    i = j = 0
    k = l

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1

        yield k
        k += 1

    while i < len(left):
        arr[k] = left[i]
        i += 1
        yield k
        k += 1

    while j < len(right):
        arr[k] = right[j]
        j += 1
        yield k
        k += 1


# MAIN

state = STATE_INPUT
input_text = ""

data = []
steps = None
active_index = None
final_index = -1

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == STATE_INPUT and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if input_text.isdigit() and int(input_text) > 1:
                    n = int(input_text)
                    data = [random.randint(MIN_VAL, MAX_VAL) for _ in range(n)]
                    steps = merge_sort(data, 0, n - 1)
                    state = STATE_SORTING
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif event.unicode.isdigit():
                input_text += event.unicode

    
    # LOGIC APPLICATION
    
    if state == STATE_SORTING:
        try:
            active_index = next(steps)
            sound_pool[data[active_index]].play()
        except StopIteration:
            active_index = None
            state = STATE_FINAL_SWEEP

    elif state == STATE_FINAL_SWEEP:
        final_index += 1

        if final_index < len(data):
            sound_pool[data[final_index]].play()

        if final_index >= len(data) - 1:
            state = STATE_DONE

    
    # DRAW GRAPH
    
    if state == STATE_INPUT:
        draw_input(input_text)
    else:
        draw_bars(data, active_index, final_index)

    pygame.display.flip()

pygame.quit()
sys.exit()
