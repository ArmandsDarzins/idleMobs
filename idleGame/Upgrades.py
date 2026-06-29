

BLUE = (50, 130, 220)


UPGRADES = {
    "attack":[
        {"id":"atk1","name":"Sharpened Blade","desc":"+2 dmg / level","max":5,
         "base_cost":15,"mult":2.2,"requieres":None,"req_lvl":0,"effect":"damage","value":2},
        {"id":"atk2","name":"Heavy Strikes", "desc":"+5 dmg / level","max":4,"base_cost":120,
             "mult":2.8,"requieres":"atk1","req_lvl":3,"effect":"damage","value":5},
        {"id":"atk3","name":"Berserker Rage", "desc":"+15 dmg / level","max":3,"base_cost":1200,
         "mult":3.5,"requieres":"atk2","req_lvl":2,"effect":"damage","value":15},
    ],
    "speed": [
        {"id":"spd1","name":"Quick Hands", "desc":"-20% attack interval / level", "max":5,
         "base_cost":25,"mult":2.4,"requieres":None,"req_lvl":0,"effect":"speed", "value":0.80},
        {"id":"spd2","name":"Combat Rhythm", "desc":"-30% attack interval / level","max":3,
          "base_cost":300,"mult":3.0,"requieres":"spd1","req_lvl":3,"effect":"speed","value":0.70},
        {"id":"spd3","name":"Blur of Motion", "desc":"-40% attack interval / level","max":2,
         "base_cost":2500,"mult":4.0,"requieres":"spd2","req_lvl":2,"effect":"speed","value":0.60},
    ],
    "gold":[
        {"id":"gld1","name":"Looter Instinct","desc":"+25% gold / level","max":5,
         "base_cost":40,"mult":2.5,"requieres":None,"req_lvl":0,"effect":"gold","value":0.25},
        {"id":"gld2","name":"Treasure Sense","desc":"+60% gold / level","max":3,
         "base_cost":400,"mult":3.2,"requieres":"gld1","req_lvl":2,"effect":"gold","value":0.60},
        {"id":"gld3","name":"Legendary Hoard","desc":"+150% gold / level","max":2,
         "base_cost":3500,"mult":4.5,"requieres":"gld2","req_lvl":2,"effect":"gold","value":1.50},
    ],
    "crit":[
        {"id":"crt1","name":"Lucky Strike","desc":"+5% crit chance / level","max":4,
         "base_cost":80,"mult":2.6,"requieres":None,"req_lvl":0,"effect":"crit_chance","value":5},
        {"id":"crt2","name":"Vital Points","desc":"+3x crit mult / level","max":3,
         "base_cost":500,"mult":3.3,"requieres":"crt1","req_lvl":2,"effect":"crit_mult","value":3},
        {"id":"crt3","name":"Execution Strike","desc":"+10% crit chance / level","max":2,
         "base_cost":4000,"mult":5.0,"requieres":"crt2","req_lvl":2,"effect":"crit_chance","value":10},
    ],
}

ALL_UPGRADES = [u for upgs in UPGRADES.values() for u in upgs]


def upg_cost(upg, lvl):
    return int(upg["base_cost"] * (upg["mult"] ** lvl))

def buy_upgrade(upg_id, state, logs):
    upg = next((u for u in ALL_UPGRADES if u["id"] == upg_id), None)
    if not upg:
        return False
    lvl = state["levels"][upg_id]
    if lvl >= upg["max"]:
        return False
    if upg["requieres"] and state ["levels"][upg["requieres"]] < upg["req_lvl"]:
        return False
    cost = upg_cost(upg, lvl)
    if state["gold"] < cost:
        return False
    state["gold"] -= cost
    state["levels"][upg_id] = lvl + 1
    effect = upg["effect"]
    val = upg["value"]

    if effect == "damage":
        state["damage"] += val
    elif effect == "speed":
        state["auto_interval"] = max(100, int(state["auto_interval"] * val))
    elif effect == "gold":
        state["gold_mult"] += val
    elif effect == "crit_chance":
        state["crit_chance"] += val
    elif effect == "crit_mult":
        state["crit_mult"] += val
    
    logs.append(("Upgraded {}! ".format(upg["name"]), BLUE))
    return True