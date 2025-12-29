import pygame
import random
import sys
import numpy as np
import time

# =====================
# CONFIG
# =====================
WIDTH, HEIGHT = 1200, 620
FPS = 120

BAR_COLOR = (230, 230, 230)
REC_COLOR = (255, 80, 80)
ITER_COLOR = (80, 160, 255)
FINAL_COLOR = (0, 255, 0)
BG_COLOR = (0, 0, 0)
DIVIDER_COLOR = (255, 220, 0)

MIN_VAL = 10
MAX_VAL = 90

# =====================
# STATE
# =====================
STATE_INPUT = 0
STATE_SORTING = 1
STATE_FINAL = 2
STATE_DONE = 3

# =====================
# INIT
# =====================
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Merge Sort: Rekursif vs Iteratif")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 22)

LEFT_AREA = pygame.Rect(0, 0, WIDTH // 2, HEIGHT)
RIGHT_AREA = pygame.Rect(WIDTH // 2, 0, WIDTH // 2, HEIGHT)

# =====================
# TIMER
# =====================
start_time_rec = None
start_time_iter = None
elapsed_rec = 0.0
elapsed_iter = 0.0
rec_done = False
iter_done = False

# =====================
# SOUND POOL
# =====================
def generate_sounds(base_freq):
    sounds = {}
    sample_rate = 44100
    duration = 0.025

    for v in range(MIN_VAL, MAX_VAL + 1):
        freq = base_freq + v * 6
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave = 16000 * np.sin(2 * np.pi * freq * t)
        stereo = np.column_stack((wave, wave))
        sounds[v] = pygame.sndarray.make_sound(stereo.astype(np.int16))

    return sounds

sound_rec = generate_sounds(520)
sound_iter = generate_sounds(240)
sound_final = generate_sounds(450)

# =====================
# DRAW
# =====================
def draw_bars(area, data, active, final_idx, active_color):
    n = len(data)
    bar_w = area.width / n 

    for i, v in enumerate(data):
        x = area.x + (i * bar_w)
        h = (v / MAX_VAL) * (HEIGHT - 100) 
        y = HEIGHT - h

        if i <= final_idx:
            color = FINAL_COLOR
        elif i == active:
            color = active_color
        else:
            color = BAR_COLOR

        current_w = bar_w if n > 200 else bar_w - 1
        pygame.draw.rect(screen, color, (x, y, max(1, current_w), h))

def draw_titles():
    r = font.render("MERGE SORT REKURSIF", True, REC_COLOR)
    i = font.render("MERGE SORT ITERATIF", True, ITER_COLOR)
    screen.blit(r, (LEFT_AREA.centerx - r.get_width() // 2, 10))
    screen.blit(i, (RIGHT_AREA.centerx - i.get_width() // 2, 10))
    
    # --- LOGIKA AUTO-HIDE INDIKATOR ---
    current_time = time.time()
    if is_paused:
        # Teks Pause tetap tampil selama di-pause
        pause_txt = font.render(" Process Paused | Press 'P' to Resume", True, (255, 255, 255))
        screen.blit(pause_txt, (20, 80)) 
    elif current_time - hint_timer < HINT_DURATION:
        # Teks instruksi hanya tampil selama HINT_DURATION (3 detik)
        hint_txt = font.render("P: Pause | R: Replay | ESC: Menu", True, (200, 200, 200))
        screen.blit(hint_txt, (20, 80))

def draw_timers():
    t1 = font.render(f"Time: {elapsed_rec:.3f} s", True, REC_COLOR)
    t2 = font.render(f"Time: {elapsed_iter:.3f} s", True, ITER_COLOR)
    screen.blit(t1, (LEFT_AREA.centerx - t1.get_width() // 2, 40))
    screen.blit(t2, (RIGHT_AREA.centerx - t2.get_width() // 2, 40))

def draw_divider():
    pygame.draw.line(screen, DIVIDER_COLOR, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)

def draw_input(text):
    screen.fill(BG_COLOR)
    font_header = pygame.font.SysFont("consolas", 32, bold=True)
    
    text_tugas = font.render("Kelompok 4 - IF 48-12 - S1 Informatika - Telkom University", True, (255, 215, 0))
    text_kelompok = font.render("Tugas Besar Analisis Kompleksitas Algoritma", True, (255, 215, 0))
    text_anggota = font.render("Anggota Kelompok: ARM | MIF | MRA", True, (255, 215, 0))
    screen.blit(text_kelompok, (10, 10))
    screen.blit(text_tugas, (10, 35))
    screen.blit(text_anggota, (10, 60))

    title = font_header.render("MERGE SORT VISUALIZATION APP (RECURSIVE vs ITERATIVE)", True, (0, 255, 255))
    prompt = font.render("Masukkan jumlah data (n), lalu tekan ENTER", True, (255, 255, 255))

    box = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2, 240, 40)
    pygame.draw.rect(screen, (255, 255, 255), box, 2)

    val = font.render(text, True, (0, 255, 0))

    if len(text) >= 5:
        warning_text = font.render("Maksimal input: 5 digit!", True, (255, 80, 80))
        screen.blit(warning_text, (WIDTH // 2 - warning_text.get_width() // 2, HEIGHT // 2 + 50))

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 210)) 
    screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(val, (box.x + 10, box.y + 6))

# =====================
# MERGE SORT LOGIC
# =====================
def merge_sort_rec(arr, l, r):
    if l >= r: return
    m = (l + r) // 2
    yield from merge_sort_rec(arr, l, m)
    yield from merge_sort_rec(arr, m + 1, r)
    yield from merge(arr, l, m, r)

def merge_sort_iter(arr):
    n = len(arr)
    size = 1
    while size < n:
        for l in range(0, n, size * 2):
            m = min(l + size - 1, n - 1)
            r = min(l + size * 2 - 1, n - 1)
            if m < r: yield from merge(arr, l, m, r)
        size *= 2

def merge(arr, l, m, r):
    left = arr[l:m + 1]
    right = arr[m + 1:r + 1]
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

# =====================
# MAIN LOOP
# =====================
state = STATE_INPUT
input_text = ""
base = [] 
data_rec = []
data_iter = []
steps_rec = None
steps_iter = None
active_rec = None
active_iter = None
final_idx = -1
final_tick = 0
FINAL_DELAY = 2
is_paused = False
hint_timer = 0  
HINT_DURATION = 3.0  

running = True
while running:
    clock.tick(FPS)
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Reset timer setiap kali tombol ditekan agar teks muncul sebentar
            hint_timer = time.time()

            if state == STATE_INPUT:
                if event.key == pygame.K_RETURN:
                    if input_text.isdigit() and int(input_text) > 1:
                        n = int(input_text)
                        base = [random.randint(MIN_VAL, MAX_VAL) for _ in range(n)]
                        data_rec = base.copy()
                        data_iter = base.copy()
                        steps_rec = merge_sort_rec(data_rec, 0, n - 1)
                        steps_iter = merge_sort_iter(data_iter)
                        start_time_rec = time.time()
                        start_time_iter = time.time()
                        elapsed_rec = elapsed_iter = 0
                        rec_done = iter_done = False
                        final_idx = -1
                        state = STATE_SORTING
                        is_paused = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isdigit() and len(input_text) < 5:
                    input_text += event.unicode
            
            else: 
                if event.key == pygame.K_p and state == STATE_SORTING:
                    is_paused = not is_paused
                if event.key == pygame.K_r:
                    data_rec = base.copy()
                    data_iter = base.copy()
                    steps_rec = merge_sort_rec(data_rec, 0, len(base) - 1)
                    steps_iter = merge_sort_iter(data_iter)
                    start_time_rec = time.time()
                    start_time_iter = time.time()
                    elapsed_rec = elapsed_iter = 0
                    rec_done = iter_done = False
                    final_idx = -1
                    state = STATE_SORTING
                    is_paused = False
                if event.key == pygame.K_ESCAPE:
                    state = STATE_INPUT
                    input_text = ""

    if state == STATE_SORTING:
        if not is_paused:
            try:
                active_rec = next(steps_rec)
                sound_rec[data_rec[active_rec]].play()
                elapsed_rec = time.time() - start_time_rec
            except StopIteration:
                active_rec = None
                rec_done = True
            try:
                active_iter = next(steps_iter)
                sound_iter[data_iter[active_iter]].play()
                elapsed_iter = time.time() - start_time_iter
            except StopIteration:
                active_iter = None
                iter_done = True
            if rec_done and iter_done: state = STATE_FINAL
        else:
            start_time_rec = time.time() - elapsed_rec
            start_time_iter = time.time() - elapsed_iter

    elif state == STATE_FINAL:
        final_tick += 1
        if final_tick >= FINAL_DELAY:
            final_tick = 0
            if final_idx < len(data_rec) - 1:
                final_idx += 1
                sound_final[data_rec[final_idx]].play()
            else: state = STATE_DONE

    if state == STATE_INPUT:
        draw_input(input_text)
    else:
        draw_bars(LEFT_AREA, data_rec, active_rec, final_idx, REC_COLOR)
        draw_bars(RIGHT_AREA, data_iter, active_iter, final_idx, ITER_COLOR)
        draw_divider()
        draw_titles()
        draw_timers()

    pygame.display.flip()

pygame.quit()
sys.exit()