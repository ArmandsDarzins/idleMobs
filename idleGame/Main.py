import json
import os
import pygame

from Upgrades import UPGRADES, ALL_UPGRADES, upg_cost, buy_upgrade
from Mobs import MOB_NAMES, draw_mob_sprite, mob_for_wave, spawn_mob, hit_mob

pygame.init()

WIDTH, HEIGHT = 900,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mob idle")
clock = pygame.time.Clock()

BG = (18, 18, 24)
SURFACE = (28, 28, 38)
SURFACE2 = (38, 38, 52)
WHITE = (220, 220, 230)
MUTED = (120, 120, 140)
GOLD = (186, 117, 23)
RED = (200, 60, 60)
GREEN = (60, 180, 100)
BLUE = (50, 130, 220)
ORANGE = (210, 100, 40)
LOCKED = (60, 60, 75)
TAB_ACTIVE = (50, 130, 220)

font_big = pygame.font.SysFont("segoeui", 28, bold = True)
font_med = pygame.font.SysFont("segoeui", 18)
font_small = pygame.font.SysFont("segoeui", 14)
font_tiny = pygame.font.SysFont("segoeui", 12)

SAVE_FILE = "save.json"


def default_state():
    return{
        "gold":0, "kills":0, "wave":1, "kills_in_wave":0,
        "damage":1, "auto_interval": 1000,
        "gold_mult":1.0, "crit_chance":0, "crit_mult":2,
        "mob_hp":0, "mob_max_hp":0,
        "levels": {u["id"]:0 for u in ALL_UPGRADES},
    }

def save_game(state):
    with open(SAVE_FILE, "w") as f:
        json.dump(state, f)

def load_game():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE) as f:
                data = json.load(f)
            s = default_state()
            s.update(data)
            return s
        except:
            pass

    return default_state()

def draw_rect_rounded(surface, color, rect, radius = 8):
    pygame.draw.rect(surface, color, rect, border_radius = radius)


def draw_text(surface, text, font, color, x, y, align = "left"):
    img = font.render(str(text), True, color)
    if align == "center":
        x -= img.get_width() // 2
    elif align == "right":
        x -= img.get_width()
    surface.blit(img, (x, y))
    return img.get_width(), img.get_height()

def draw_bar(surface, x, y, w, h, pct, color, bg = SURFACE2):
    draw_rect_rounded(surface, bg, (x, y, w, h), 4)
    if pct > 0:
        draw_rect_rounded(surface, color, (x, y, int(w * pct), h), 4)


PANEL_LEFT = 10
PANEL_TOP = 10
PANEL_W = 280
PANEL_H = HEIGHT - 20

COMBAT_X = PANEL_LEFT + PANEL_W + 10
COMBAT_W = WIDTH - COMBAT_X - 10
STAT_H = 80
MOB_H = 150
LOG_H = HEIGHT - PANEL_TOP - STAT_H - MOB_H - 40

TAB_NAMES = ["Attack", "Speed", "Gold", "Crit"]
TAB_KEYS = ["attack", "speed", "gold", "crit"]

def main():
    state = load_game()
    if state["mob_hp"] <= 0 or state["mob_max_hp"] == 0:
        spawn_mob(state)

    logs = []
    auto_on = False
    auto_timer = 0
    active_tab = 0
    scroll_y = 0
    running = True

    while running:
        dt = clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(state)
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = True
            if event.type == pygame.MOUSEWHEEL:
                scroll_y = max(0, scroll_y - event.y * 20)


        if auto_on:
            auto_timer += dt
            if auto_timer >= state["auto_interval"]:
                auto_timer = 0
                if hit_mob(state, logs):
                    save_game(state)

        if len(logs) > 30:
            logs = logs[-30:]

        screen.fill(BG)

        draw_rect_rounded(screen, SURFACE, (PANEL_LEFT, PANEL_TOP, PANEL_W, PANEL_H), 12)

        tab_w = PANEL_W // 4
        for i, tab in enumerate(TAB_NAMES):
            tx = PANEL_LEFT + i * tab_w
            col = TAB_ACTIVE if i == active_tab else SURFACE2
            draw_rect_rounded(screen, col, (tx + 2, PANEL_TOP + 8, tab_w - 4, 28), 6)
            draw_text(screen, tab, font_tiny, WHITE if i == active_tab else MUTED, tx + tab_w // 2, PANEL_TOP + 15, align = "center")
            if mouse_click and tx < mouse_pos[0] < tx + tab_w and PANEL_TOP + 8 <mouse_pos[1] < PANEL_TOP + 36:
                active_tab = i
                scroll_y = 0
        
        cat = TAB_KEYS[active_tab]
        upgs = UPGRADES[cat]
        uy = PANEL_TOP + 48 - scroll_y
        buy_buttons = []

        for i, upg in enumerate(upgs):
            lvl = state["levels"][upg["id"]]
            locked = upg["requieres"] and state["levels"][upg["requieres"]] < upg["req_lvl"]
            maxed = lvl >= upg["max"]
            cost = upg_cost(upg, lvl)
            can_afford = state["gold"] >= cost

            if i > 0 and uy > PANEL_TOP + 40:
                pygame.draw.line(screen, MUTED, (PANEL_LEFT + 20, uy - 6), (PANEL_LEFT + 20, uy), 2)
            
            node_h = 90
            node_col = LOCKED if locked else(SURFACE2 if not maxed else(30, 55, 35))
            draw_rect_rounded(screen, node_col, (PANEL_LEFT + 8, uy, PANEL_W - 16, node_h), 8)

            if uy > PANEL_TOP + 36 and uy < PANEL_TOP + PANEL_H:
                draw_text(screen, upg ["name"], font_small, MUTED if locked else WHITE, PANEL_LEFT + 16, uy + 8)
                draw_text(screen, upg["desc"], font_tiny, MUTED, PANEL_LEFT + 16, uy + 26)

                for p in range(upg["max"]):
                    pip_col = BLUE if p < lvl else SURFACE
                    pygame.draw.rect(screen, pip_col, (PANEL_LEFT + 16 + p * 18, uy + 44, 14, 5), border_radius = 3)
            
                if maxed:
                    draw_text(screen, "MAX", font_tiny, GREEN, PANEL_LEFT + PANEL_W - 50, uy + 36)
                
                elif locked:
                    req = next((u for u in ALL_UPGRADES if u ["id"] == upg["requieres"]), None)

                    draw_text(screen, "Req: {} lv{}".format(req["name"] if req else "?", upg["req_lvl"]),
                              font_tiny, MUTED, PANEL_LEFT + 16, uy + 62)
                    
                else:
                    btn_col = GREEN if can_afford else SURFACE
                    btn_rect = (PANEL_LEFT + PANEL_W - 90, uy + 56, 82, 24)
                    draw_rect_rounded(screen, btn_col, btn_rect, 6)
                    draw_text(screen, "{}g".format(cost), font_tiny, WHITE, PANEL_LEFT + PANEL_W - 49, uy + 62, align = "center")
                    buy_buttons.append((btn_rect, upg["id"]))
                    draw_text(screen, "{}/{}".format(lvl, upg["max"]), font_tiny, MUTED, PANEL_LEFT + 16, uy + 62)


            uy += node_h + 8

        if mouse_click:
            for btn_rect, upg_id in buy_buttons:
                if btn_rect[0] < mouse_pos[0] < btn_rect[0] + btn_rect[2] and \
                    btn_rect[1] < mouse_pos[1] < btn_rect[1] + btn_rect[3]:
                    if buy_upgrade(upg_id, state, logs):
                        save_game(state)


        cx = COMBAT_X

        stats = [
            ("Gold",    "{:,}".format(int(state["gold"])),  GOLD),
            ("Kills",   "{:,}".format(state["kills"]),  WHITE),
            ("Wave",    state["wave"],  BLUE),
            ("Damage",  state["damage"],    WHITE),
            ("Crit",    "{}%".format(int(state["crit_chance"])), ORANGE),
        ]
        card_w = (COMBAT_W - 8 * 4) // 5
        for i, (label, val, col) in enumerate(stats):
            sx = cx + i * (card_w + 8)
            draw_rect_rounded(screen, SURFACE, (sx, PANEL_TOP, card_w, STAT_H), 8)
            draw_text(screen, label, font_tiny, MUTED, sx + card_w // 2, PANEL_TOP + 10, align = "center")
            draw_text(screen, val, font_med, col, sx + card_w // 2, PANEL_TOP + 32, align = "center")

        mob_y = PANEL_TOP + STAT_H + 10
        draw_rect_rounded(screen, SURFACE, (cx, mob_y, COMBAT_W, MOB_H), 12)
        mob_name, _, _ = mob_for_wave(state["wave"])
        mob_idx = min((state["wave"] - 1) // 5, len(MOB_NAMES) - 1)
        draw_text(screen, mob_name, font_big, WHITE, cx + 16, mob_y + 12)
        kills_left = 10 - state["kills_in_wave"]
        draw_text(screen, "Wave {} - {} kills till next wave". format(state["wave"], kills_left),
                    
                    font_tiny, MUTED, cx + 16, mob_y + 44)
        
        pct = state["mob_hp"] / state["mob_max_hp"] if state["mob_max_hp"] > 0 else 1
        draw_bar(screen, cx + 16, mob_y + 62, COMBAT_W - 140, 12, pct, RED)
        draw_text(screen, "{:,} / {:,} HP". format(state["mob_hp"], state["mob_max_hp"]), font_tiny, MUTED, cx + 16, mob_y + 78)

        draw_mob_sprite(screen, mob_idx, cx, mob_y, COMBAT_W, MOB_H, pct)

        atk_rect = (cx + 16, mob_y + 98, 130, 36)
        atk_hover = atk_rect[0] < mouse_pos[0] < atk_rect[0] + atk_rect[2] and \
                    atk_rect[1] < mouse_pos[1] < atk_rect[1] + atk_rect[3]
        draw_rect_rounded(screen, RED if atk_hover else (140, 40, 40), atk_rect, 8)
        draw_text(screen, "Attack", font_med, WHITE, cx + 16 + 65, mob_y + 108, align = "center")

        if mouse_click and atk_hover:
            if hit_mob(state, logs):
                save_game(state)

        auto_rect = (cx + 16 + 138, mob_y + 98, 160, 36)
        auto_hover = auto_rect[0] < mouse_pos[0] < auto_rect[0] + auto_rect[2] and \
                    auto_rect[1] < mouse_pos[1] < auto_rect[1] + auto_rect[3]
        auto_col = (30, 120, 60) if auto_on else SURFACE2
        draw_rect_rounded(screen, auto_col, auto_rect, 8)
        draw_text(screen, "Auto: {}".format("ON" if auto_on else "OFF"), font_med, WHITE, auto_rect[0] + 80, mob_y + 108, align = "center")

        if mouse_click and auto_hover:
            auto_on = not auto_on
            auto_timer = 0

        log_y = mob_y + MOB_H + 10
        draw_rect_rounded(screen, SURFACE, (cx, log_y, COMBAT_W, LOG_H), 12)
        draw_text(screen, "Log", font_tiny, MUTED, cx + 12, log_y + 8)
        visible = logs[-((LOG_H - 25) // 18):]
        for i, (msg, col) in enumerate(visible):
            draw_text(screen, msg, font_tiny, col, cx + 12, log_y + 26 + i * 18)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
                    