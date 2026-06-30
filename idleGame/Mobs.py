import pygame
import random

WHITE = (220,220,230)
GREEN = (60,180,100)
BLUE = (50,130,220)
ORANGE = (210,100,40)

MOB_NAMES = ["Slime", "Goblin", "Orc", "Troll", "Dark Knight", "Shadow Beast",
             "Demon Lord", "Ancient Dragon"]

MOB_COLORS = [
    ((80,200,80),   (50,140,50)),   #Slime
    ((110,160,70),  (70,110,40)),   # Goblin
    ((95,115,55),   (60,75,35)),    #Orc
    ((100,100,130), (60,60,90)),    #Troll
    ((60,60,100),   (30,30,60)),    #Dark Knight
    ((80,40,100),   (50,20,70)),    #Shadow Beast
    ((180,40,40),   (120,20,20)),   #Demon Lord
    ((180,120,20),  (120,80,10)),   #Ancient Dragon
]

def _lighten(col, amt = 40):
    return tuple(min(255, c + amt) for c in col)

def _darken(col, amt = 40):
    return tuple(max(0, c - amt) for c in col)

def draw_mob_sprite(surface, mob_idx, cx, mob_y, mob_w, mob_h, hp_pct):
    sx = cx + mob_w - 110
    sy = mob_y + 8

    body_col, detail_col = MOB_COLORS[mob_idx % len(MOB_COLORS)]

    if hp_pct < 0.3:
        body_col = (min(255, body_col[0] + 60), max(0, body_col[1] - 40),
            max(0, body_col[2] - 40))
    
    if mob_idx == 0:
        pygame.draw.polygon(surface, body_col, [
            (sx + 10, sy + 45), (sx + 15, sy + 25), (sx + 30, sy + 15),
            (sx + 50, sy + 12), (sx + 70, sy + 18), (sx + 82, sy  + 35),
            (sx + 80, sy + 55), (sx + 65, sy + 68), (sx + 45, sy + 72),
            (sx + 25, sy + 66), (sx + 12, sy + 55),
        ])
        pygame.draw.ellipse(surface, detail_col, (sx + 18, sy + 45, 56, 26))
        hl = _lighten(body_col, 70)
        pygame.draw.ellipse(surface, hl, (sx + 25, sy + 20, 22 ,14))
        
        pygame.draw.circle(surface, WHITE, (sx + 35, sy + 38), 7)
        pygame.draw.circle(surface, WHITE, (sx + 58, sy + 38), 7)
        pygame.draw.circle(surface, (20, 20 ,20), (sx + 37, sy + 40), 3)
        pygame.draw.circle(surface, (20, 20, 20), (sx + 60, sy + 40), 3)
        pygame.draw.lines(surface, (20, 20, 20), False,
                        [(sx + 38, sy + 48), (sx + 46, sy + 54), (sx + 54, sy + 48)], 2)
        
    elif mob_idx == 1:

        pygame.draw.rect(surface, detail_col, (sx + 26, sy + 64, 10, 16), border_radius = 3)
        pygame.draw.rect(surface, detail_col, (sx + 46, sy + 64, 10, 16), border_radius = 3)
        pygame.draw.rect(surface, detail_col, (sx + 26, sy + 38, 32, 28), border_radius = 6)
        pygame.draw.rect(surface, body_col, (sx + 28, sy + 34, 28, 14), border_radius = 4)
        pygame.draw.rect(surface, body_col, (sx + 12, sy + 38, 16, 9), border_radius = 4)
        pygame.draw.rect(surface, body_col, (sx + 54, sy + 38, 16, 9), border_radius = 4)
        pygame.draw.rect(surface, (180, 180, 190), (sx + 66, sy + 28, 4, 16), border_radius = 1)
        pygame.draw.rect(surface, detail_col, (sx + 66, sy + 44, 8, 5), border_radius = 2)

        pygame.draw.ellipse(surface, body_col, (sx + 22, sy + 10, 38, 22))
        pygame.draw.polygon(surface, body_col, [(sx + 33, sy + 38), (sx + 41, sy + 44), (sx + 49, sy + 38 )])
        
        pygame.draw.polygon(surface, detail_col, [(sx + 18, sy + 18), (sx + 4, sy + 10), (sx + 20, sy + 28)])
        pygame.draw.polygon(surface, detail_col, [(sx + 64, sy + 18), (sx + 78, sy + 10), (sx + 62, sy + 28)])
        pygame.draw.polygon(surface, _darken(body_col, 20), [(sx + 38, sy + 24), (sx + 41, sy + 30), (sx + 44, sy + 24)])

        pygame.draw.ellipse(surface, (255,60,40), (sx + 29, sy + 18, 8, 5))
        pygame.draw.ellipse(surface, (255,60,40), (sx + 45, sy + 18, 8, 5))

        pygame.draw.polygon(surface, (30,20,10), [(sx + 32, sy + 30), (sx + 50, sy + 30), (sx + 46, sy + 35), (sx + 36, sy + 35)])
        for tx in(sx + 35, sx + 40, sx + 45):
            pygame.draw.polygon(surface, WHITE, [(tx, sy + 30), (tx + 3, sy + 30), (tx + 1, sy + 33)], 2)
            
    elif mob_idx == 2:
            pygame.draw.rect(surface, detail_col, (sx +22, sy + 66, 14, 14), border_radius = 3)
            pygame.draw.rect(surface, detail_col, (sx + 54, sy + 66, 14, 14), border_radius = 3)
            pygame.draw.rect(surface, body_col, (sx + 18, sy + 32, 54, 36), border_radius = 8)
            pygame.draw.rect(surface, (60, 40, 20), (sx + 18, sy + 58, 54, 6))

            pygame.draw.ellipse(surface, detail_col, (sx + 4, sy + 28, 22, 20))
            pygame.draw.ellipse(surface, detail_col, (sx + 64, sy + 28, 22, 20))
            pygame.draw.ellipse(surface, body_col, (sx + 22, sy + 8, 46, 30))
            pygame.draw.rect(surface, _darken(body_col, 30), (sx + 30, sy + 18, 30, 5), border_radius = 2)

            pygame.draw.circle(surface, (255, 120, 0), (sx + 34, sy + 24), 4)
            pygame.draw.circle(surface,  (255, 120, 0), (sx + 56, sy + 24), 4)

            pygame.draw.polygon(surface, WHITE, [(sx + 32, sy + 34), (sx + 36, sy + 34), (sx + 30, sy + 46)])
            pygame.draw.polygon(surface, WHITE, [(sx + 58, sy + 34), (sx + 54, sy + 34), (sx + 60, sy + 46)])

            
            pygame.draw.line(surface, (180, 30, 30), (sx + 30, sy + 28), (sx + 40, sy + 34), 3)
            pygame.draw.rect(surface, (90, 60,30), (sx + 76, sy + 10, 5, 50), border_radius = 2)
            pygame.draw.polygon(surface, (150, 150, 160), [(sx + 74, sy + 8), (sx + 92, sy + 4), (sx + 92, sy + 22), (sx + 74, sy + 20)])

    elif mob_idx == 3:
         pygame.draw.ellipse(surface, detail_col, (sx + 14, sy + 72, 24, 12))
         pygame.draw.ellipse(surface, detail_col, (sx + 52, sy + 72, 24, 12))
         pygame.draw.ellipse(surface, body_col, (sx + 12, sy + 34, 66, 42))

         pygame.draw.rect(surface, body_col, (sx + 2, sy + 38, 14, 38), border_radius = 7)
         pygame.draw.rect(surface, body_col, (sx + 74, sy + 38, 14, 38), border_radius = 7)
         pygame.draw.circle(surface, body_col, (sx + 9, sy + 76), 9)
         pygame.draw.circle(surface, body_col, (sx + 81, sy + 76), 9)

         pygame.draw.rect(surface, (110, 80, 40), (sx + 86, sy + 50, 8, 30), border_radius = 3)
         pygame.draw.ellipse(surface, (110, 80, 40), (sx + 78, sy + 40, 26, 18))

         pygame.draw.ellipse(surface, body_col, (sx + 24, sy + 10, 38, 30))
         pygame.draw.polygon(surface, body_col, [(sx + 26, sy + 30), (sx + 56, sy + 30), (sx + 50, sy + 42), (sx + 32, sy + 42)])
         
         pygame.draw.rect(surface, _darken(body_col, 30), (sx + 28, sy + 20, 26, 5), border_radius = 2)
         pygame.draw.circle(surface, (255, 220, 80), (sx + 33, sy + 26), 3)
         pygame.draw.circle(surface, (255, 220, 80), (sx + 49, sy + 26), 3)
         pygame.draw.polygon(surface, WHITE, [(sx + 38, sy + 36), (sx + 42, sy + 36), (sx + 40, sy + 42)])
        
         for wx, wy in [(sx + 20, sy + 45), (sx + 60, sy + 50), (sx + 35, sy + 60)]:
            pygame.draw.circle(surface, detail_col, (wx, wy), 4)

    elif mob_idx == 4:
        pygame.draw.polygon(surface, detail_col, [(sx + 30, sy + 28), (sx + 10, sy + 85), (sx +45, sy + 70)])
        pygame.draw.rect(surface, detail_col, (sx + 28, sy + 66, 14, 18), border_radius = 3)
        pygame.draw.rect(surface, detail_col, (sx + 48, sy + 66, 14, 18), border_radius = 3)
        pygame.draw.rect(surface, (30, 30, 30), (sx + 26, sy + 80, 18, 8), border_radius = 3)
        pygame.draw.rect(surface, (30, 30, 30), (sx + 46, sy + 80, 18, 8), border_radius = 3)
        pygame.draw.rect(surface, body_col, (sx + 22, sy + 30, 42, 38), border_radius = 4)

        pygame.draw.polygon(surface, (160, 20, 20), [(sx + 43, sy + 38), (sx + 49, sy + 48), (sx + 43, sy + 56), (sx + 37, sy + 48)])
        pygame.draw.polygon(surface, detail_col, [(sx + 6, sy + 28), (sx + 24, sy + 24), (sx + 24, sy + 44), (sx + 6, sy + 42)])
        pygame.draw.polygon(surface, detail_col, [(sx + 80, sy + 28), (sx + 62, sy + 24), (sx + 62, sy + 44), (sx + 80, sy + 42)])
        
        pygame.draw.rect(surface, body_col, (sx + 20, sy + 8, 46, 28), border_radius = 6)
        pygame.draw.polygon(surface, (160, 20, 20), [(sx + 38, sy + 8), (sx + 43, sy - 10), (sx + 48, sy + 8)])

        pygame.draw.rect(surface, (225, 50, 50), (sx + 26, sy + 18, 34, 6), border_radius = 2)
        pygame.draw.rect(surface, (190, 190, 205), (sx + 86, sy + 6, 5, 58), border_radius = 2)
        pygame.draw.rect(surface, detail_col, (sx + 78, sy + 30, 21, 6), border_radius = 2)
        pygame.draw.rect(surface, (90, 60, 30), (sx + 86, sy + 62, 5, 10))

    elif mob_idx == 5:
        for ox, oy, r in [(-6, 30, 30), (-14, 40, 7), (4, 52, 6)]:
            pygame.draw.circle(surface, body_col, (sx + 40 + ox, sy + oy),r)

        pygame.draw.ellipse(surface,  body_col, (sx + 18, sy + 38, 56, 30))

        for lx in (sx + 24, sx + 38, sx + 54, sx + 66):
            pygame.draw.polygon(surface, body_col, [(lx, sy + 58), (lx + 6, sy + 58), (lx + 3, sy +74)])
        
        pygame.draw.polygon(surface, detail_col, [(sx + 58, sy + 28), (sx + 86, sy + 34), (sx + 80, sy + 46), (sx + 56, sy + 44)])
        pygame.draw.polygon(surface, detail_col, [(sx + 58, sy + 22), (sx + 52, sy + 8), (sx + 66, sy + 24)])
        pygame.draw.polygon(surface, detail_col, [(sx + 70, sy + 20), (sx + 74, sy + 4), (sx + 80, sy + 22)])

        pygame.draw.circle(surface, (180, 0, 255), (sx + 68, sy + 34), 5)
        pygame.draw.circle(surface, (180, 0, 255), (sx + 78, sy + 36), 4)
        pygame.draw.circle(surface, WHITE, (sx + 68, sy + 34), 2)
        pygame.draw.circle(surface, WHITE, (sx + 78, sy + 36), 2)

        pygame.draw.polygon(surface, WHITE, [(sx + 74, sy + 42), (sx + 78, sy + 42), (sx + 76, sy + 47)])
        pygame.draw.polygon(surface, WHITE, [(sx + 80, sy + 42), (sx + 84, sy + 42), (sx + 82, sy + 47)])
        
    elif mob_idx == 6:
        pygame.draw.lines(surface, body_col, False, [(sx + 45, sy + 62), (sx + 22, sy + 76), (sx + 12, sy + 68)], 5)
        pygame.draw.polygon(surface, body_col, [(sx + 8, sy + 62), (sx + 18, sy + 66), (sx + 10, sy + 74)])

        pygame.draw.polygon(surface, detail_col, [(sx + 40, sy + 30), (sx + 8, sy + 8), (sx + 14, sy + 22), (sx + 2, sy + 24),
                                                  (sx + 12, sy + 34), (sx + 0, sy + 38), (sx + 22, sy + 48), (sx + 40, sy + 38)])
        pygame.draw.polygon(surface, detail_col, [(sx + 44, sy + 30), (sx + 76, sy + 8), (sx + 70, sy + 22), (sx + 82, sy + 24),
                                                  (sx + 72, sy + 34), (sx + 84, sy + 38), (sx + 62, sy + 48), (sx + 44, sy + 38)])

        pygame.draw.rect(surface, body_col, (sx + 30, sy + 66, 10, 14), border_radius = 3)
        pygame.draw.rect(surface, body_col, (sx + 46, sy + 66, 10, 14), border_radius = 3)
        pygame.draw.polygon(surface, (20, 20, 20), [(sx + 30, sy + 80), (sx +35, sy + 80), (sx + 32, sy + 86)])
        pygame.draw.polygon(surface, (20, 20, 20), [(sx + 46, sy + 80), (sx + 51, sy + 80), (sx + 48, sy + 86)])

        pygame.draw.rect(surface, body_col, (sx + 24, sy + 30, 38, 38), border_radius = 6)
        pygame.draw.polygon(surface, (255, 180, 0), [(sx + 43, sy + 38), (sx + 49, sy + 46), (sx + 43, sy + 54), (sx + 37, sy + 46)])

        pygame.draw.ellipse(surface, body_col, (sx + 20, sy + 6, 46, 32))
        pygame.draw.polygon(surface, (200, 60, 0), [(sx + 26, sy + 10), (sx + 14, sy - 10), (sx + 33, sy + 6)])
        pygame.draw.polygon(surface, (200, 60, 0), [(sx + 60, sy + 10), (sx + 72, sy - 10), (sx + 53, sy + 6)])
        pygame.draw.polygon(surface, detail_col, [(sx + 38, sy + 32), (sx + 48, sy + 32), (sx + 53, sy + 6)])

        pygame.draw.circle(surface, (255, 200, 0), (sx + 34, sy + 18), 6)
        pygame.draw.circle(surface, (255, 200, 0), (sx + 52, sy + 18), 6)
        pygame.draw.circle(surface, (200, 0, 0), (sx + 35, sy + 19), 3)
        pygame.draw.circle(surface, (200, 0, 0), (sx + 53, sy + 19), 3)

    else:
        pygame.draw.lines(surface, body_col, False, [(sx + 22, sy + 50), (sx + 8, sy + 58), (sx + 2, sy + 48)], 6)
        pygame.draw.polygon(surface, body_col, [(sx - 2, sy + 42), (sx + 8, sy + 46), (sx + 2, sy + 56)])
        pygame.draw.polygon(surface,detail_col, [(sx + 30, sy + 30), (sx + 0, sy + 4), (sx + 8, sy + 20), (sx - 6, sy + 22), (sx + 6, sy + 34), (sx +24, sy + 40)])
        pygame.draw.polygon(surface, detail_col, [(sx + 50, sy + 30), (sx + 80, sy + 4), (sx + 72, sy + 20), (sx + 86, sy + 22),(sx + 74, sy + 34), (sx + 56, sy + 40)])
        
        pygame.draw.rect(surface, body_col, (sx + 24, sy+ 58, 12, 16), border_radius = 3)
        pygame.draw.rect(surface, body_col, (sx + 48, sy + 58, 12, 16), border_radius = 3)
        for clx in (sx + 24, sx + 30, sx + 48, sx + 54):
            pygame.draw.polygon(surface, WHITE, [(clx, sy + 74), (clx + 4, sy + 74), (clx + 2, sy + 80)])
        pygame.draw.ellipse(surface, body_col, (sx + 14, sy + 34, 56, 32))
        for i in range(3):
            pygame.draw.circle(surface, detail_col, (sx + 28 + i * 14, sy + 46), 4)

        pygame.draw.polygon(surface, body_col, [(sx + 44, sy + 38), (sx + 62, sy + 30), (sx + 76, sy + 12), (sx + 58, sy + 10), (sx +46, sy +24)])
        for spx, spy in [(sx + 50, sy + 30), (sx + 58, sy + 22), (sx + 66, sy + 16)]:
            pygame.draw.polygon(surface, detail_col, [(spx - 3, spy), (spx, spy - 8), (spx + 3, spy)])
        
        pygame.draw.ellipse(surface, body_col, (sx + 62, sy + 0, 32, 22))
        pygame.draw.polygon(surface, body_col, [(sx + 88, sy + 8), (sx + 99, sy + 12), (sx + 90, sy + 18)])
        pygame.draw.polygon(surface, (200, 160, 20), [(sx + 68, sy + 2), (sx + 62, sy - 10), (sx + 74, sy + 0)])
        pygame.draw.circle(surface, (255, 220, 0), (sx + 80, sy + 8), 4)
        pygame.draw.circle(surface, (20, 20, 20), (sx + 81, sy + 9), 2)
        pygame.draw.polygon(surface, (255, 140, 0), [(sx + 99, sy + 12), (sx + 108, sy + 8), (sx + 105, sy + 14), (sx + 109, sy + 16), (sx + 99, sy + 16)])

def mob_for_wave(w):
        idx = min((w - 1) // 5, len(MOB_NAMES) - 1)
        hp = int(10*(1.33 ** (w - 1)))
        base_gold = int(w * 1.8 + 1)
        return MOB_NAMES[idx], hp, base_gold
    
def spawn_mob(state):
        _, hp, _ = mob_for_wave(state["wave"])
        state["mob_hp"] = hp
        state["mob_max_hp"] = hp

def hit_mob(state, logs):
        if state["mob_hp"] <= 0:
            return False
        dmg = state["damage"]
        is_crit = False
        if state["crit_chance"] > 0 and random.random() * 100 < state ["crit_chance"]:
            dmg = int(dmg * state["crit_mult"])
            is_crit = True
        state["mob_hp"] = max(0, state["mob_hp"] - dmg)
        if is_crit:
            logs.append(("CRIT! {} damage!".format(dmg), ORANGE))
        if state["mob_hp"] <= 0:
            kill_mob(state, logs)
            return True
        return False
    
def kill_mob(state, logs):
        _, _, base_gold = mob_for_wave(state["wave"])
        earned = int(base_gold * state["gold_mult"])
        mob_name, _, _ = mob_for_wave(state["wave"])
        state["gold"] += earned
        state["kills"] += 1
        state["kills_in_wave"] += 1
        logs.append(("Killed {}!".format(mob_name), GREEN))
        if state["kills_in_wave"] >= 10:
            state["kills_in_wave"] = 0
            state["wave"] += 1
            next_name, _, _ = mob_for_wave(state["wave"])
            logs.append(("Wave {}! {} appears!".format(state["wave"], next_name), BLUE))
        spawn_mob(state)
    