# -*- coding: utf-8 -*-
# @Author: Alessandro Keller
# @Date: 2024-12-04 08:18:01
# @Last Modifier: Alessandro Keller
# @Last Modified time: 2024-12-04 16:21:27
# @Description: This is a 2D game where you have to jump over two randomly generated Cactuses.

import time
import random
import os
import keyboard  # importiert alle nötigen Bibliotheken

# Die Spielfeldgröße
WIDTH = 50
HEIGHT = 10

# Die Spielerposition
player_x = 5
player_y = HEIGHT - 1

# Die Hindernisse
obstacles = []
obstacle_types = ["Kaktus klein", "Kaktus groß"]

# Der Spieler
player_char = "O"
is_jumping = False
jump_duration = 10 
jump_count = 0


running = True
game_over = False

# Geschwindigkeit der Hindernisse
obstacle_speed = 1
last_spawn_time = 0
spawn_interval = 2  

# Variable für gesprungene Hindernisse
jumped_over_count = 0
max_jumps = 15  # Wenn man 15 Objekte überspringt hat man das Spiel durchgespielt



# für Function wurde mit Hilfe von ChatGPT gearbeitet

def clear_screen():

    os.system("cls" if os.name == "nt" else "clear")

def print_centered(text):

    box_width = len(text) + 4
    space_padding = (WIDTH - box_width) // 2
    print(" " * space_padding + "=" * box_width)
    print(" " * space_padding + f"| {text} |")
    print(" " * space_padding + "=" * box_width)

def start_screen():
    clear_screen()
    print("\n" + "=" * 50)
    print_centered("Willkommen zum Spiel!")
    print("\n" + "=" * 50)
    print("\nDrücke eine beliebige Taste, um zu starten.")
    while not keyboard.read_event():  # Warte, bis eine Taste gedrückt wird
        pass

def end_screen():

    clear_screen()
    if jumped_over_count >= max_jumps:
        print("\n" + "=" * 50)
        print_centered("DU HAST GEWONNEN!")
        print("\n" + "=" * 50)
    else:
        print("\n" + "=" * 50)
        print_centered("GAME OVER!")
        print("\n" + "=" * 50)
    print(" " * 10 + "Danke fürs Spielen!")
    print(" " * 10 + "Drücke 'q', um das Spiel zu beenden")
    while True:
        if keyboard.is_pressed("q"):  # Beenden des Spiels
            break

def draw_field():
    clear_screen()
    for y in range(HEIGHT):
        row = ""
        for x in range(WIDTH):
            if x == player_x and y == player_y:
                row += player_char
            elif any(obstacle["x"] == x and obstacle["y"] == y and obstacle["type"] == "Kaktus klein" for obstacle in obstacles):
                row += f"\033[1;32m🌵\033[0m"
            elif any(obstacle["x"] == x and obstacle["y"] == y and obstacle["type"] == "Kaktus groß" for obstacle in obstacles):
                row += f"\033[1;34m🌵\033[0m"
            elif any(obstacle["x"] == x and obstacle["y"] + 1 == y and obstacle["type"] == "Kaktus groß" for obstacle in obstacles):
                row += f"\033[1;34m🌵\033[0m"
            else:
                row += f"\033[1;36m.\033[0m"
        print(row)
    print("\nDrücke die Leertaste, um zu springen.")

def update_obstacles():

    global game_over, jumped_over_count
    for obstacle in obstacles:
        obstacle["x"] -= obstacle_speed 
        
        if (
            (obstacle["x"] == player_x and obstacle["y"] == player_y) or  # Kollision mit dem kleinen Kaktus
            (obstacle["type"] == "Kaktus groß" and obstacle["x"] == player_x and (obstacle["y"] == player_y or obstacle["y"] + 1 == player_y))  # Kollision mit beiden Teilen des großen Kaktus
        ):
            game_over = True

        if obstacle["x"] < 0 and obstacle["y"] == HEIGHT - 1:  # Spieler ist erfolgreich über ein Hindernis gesprungen
            jumped_over_count += 1
            if jumped_over_count >= max_jumps:  # Die Bedingung für Spielende
                game_over = True

    obstacles[:] = [obs for obs in obstacles if obs["x"] >= 0]

def spawn_obstacle():

    global last_spawn_time
    current_time = time.time()
    if current_time - last_spawn_time >= spawn_interval:
        obstacle_type = random.choice(obstacle_types)
        y_position = HEIGHT - 1 if obstacle_type == "Kaktus klein" else HEIGHT - 2
        obstacles.append({"x": WIDTH - 1, "y": y_position, "type": obstacle_type})
        last_spawn_time = current_time 

def update_player():

    global is_jumping, player_y, jump_count
    if is_jumping:
        if jump_count < jump_duration // 2:
            player_y -= 1
            jump_count += 1
        elif jump_count < jump_duration:
            player_y += 1
            jump_count += 1
        else:
            is_jumping = False
            jump_count = 0

def main():
    global running, is_jumping, game_over
    start_screen()
    while running:
        if game_over:
            draw_field()
            end_screen()
            break

        draw_field()
        update_obstacles()
        spawn_obstacle()
        update_player()


        if keyboard.is_pressed("space") and not is_jumping:
            is_jumping = True 

        time.sleep(0.038)  # perfekte Zeit, dass es flüssig läuft 

if __name__ == "__main__":
    main()
