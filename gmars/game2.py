from PIL import Image
import pygame
import subprocess
import os
import sys
from music_manager import music_manager
from music_settings import open_music_settings

def set_player(im):
    global player_img
    player_img = pygame.image.load(im)
    player_img = pygame.transform.scale(player_img, (70, 70))

pygame.init()

WIDTH, HEIGHT = 1000, 600

bg = pygame.image.load("images1.jpg")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

player_img = pygame.image.load("pixil-frame-3(5).png")
player_img = pygame.transform.scale(player_img, (70, 70))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Марс")

clock = pygame.time.Clock()

player = pygame.Rect(400, 300, 70, 70)
speed = 5

pause = False

if not os.path.exists("resume.txt"):
    open("resume.txt", "w").close()

running = True

while running:
    clock.tick(60)

    if not pygame.mixer.music.get_busy() and music_manager.is_playing:
        music_manager.next_track()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause = True
                open_music_settings()
                pause = False

            elif event.key == pygame.K_p:
                pause = True
                open_music_settings()
                pause = False

            elif event.key == pygame.K_m:
                music_manager.toggle_play_pause()

            elif event.key == pygame.K_COMMA:
                music_manager.prev_track()

            elif event.key == pygame.K_PERIOD:
                music_manager.next_track()

            elif event.key == pygame.K_EQUALS:
                music_manager.set_volume(min(1.0, music_manager.volume + 0.1))

            elif event.key == pygame.K_MINUS:
                music_manager.set_volume(max(0.0, music_manager.volume - 0.1))

    keys = pygame.key.get_pressed()

    if pause == False:

        if keys[pygame.K_LEFT]:
            player.x -= speed
            set_player("pixil-frame-2(5).png")

        elif keys[pygame.K_RIGHT]:
            player.x += speed
            set_player("pixil-frame-0 (5).png")

        if keys[pygame.K_UP]:
            player.y -= speed
            set_player("pixil-frame-3(5).png")

        elif keys[pygame.K_DOWN]:
            player.y += speed
            set_player("pixil-frame-1(5).png")

        if player.x < 0:
            player.x = 0
        elif player.x > WIDTH - 70:
            player.x = WIDTH - 70

        if player.y < 0:
            player.y = 0
        elif player.y > HEIGHT - 70:
            player.y = HEIGHT - 70

    screen.blit(bg, (0, 0))
    screen.blit(player_img, player)

    font = pygame.font.SysFont(None, 36)

    task_text = "Завдання: просто ходити"
    task_surface = font.render(task_text, True, (0, 0, 0))
    task_rect = task_surface.get_rect(midtop=(WIDTH // 2, 20))
    pygame.draw.rect(screen, (245, 222, 179), task_rect.inflate(20, 10))
    screen.blit(task_surface, task_rect)

    screen.blit(font.render(
        "Music: ON" if music_manager.is_playing else "Music: OFF",
        True, (255,255,255)), (10,90))

    screen.blit(font.render(
        f"Volume: {int(music_manager.volume * 100)}%",
        True, (255,255,255)), (10,130))

    pygame.display.update()

pygame.quit()
music_manager.cleanup()