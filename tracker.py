from collections import defaultdict

# MUST BE FORMATTED AS FOLLOWS:
# tank,tank2/dps1,dps2/support1,support2/win(orloss)
# you dont need to fill every slot. use none when you dont have someone you know
# examples:
# luke/mar/kayla/win
# none/mar/kayla/loss
# none/luke,mar/kayla/win
# luke,mar/aiden,ray/kayla,dalton/win
# comments are separators for multiple players in a role
# slashes are separators for different roles
# if you are playing marvel rivals or want to add a mvp for whatever reason:
# luke(mvp),aiden/mar/kayla/win
# in this case, luke is the mvp.
# i treat mvp and svp the same, just say mvp. you can see the win loss ratio for mvps
# THIS AND MORE IS ALL IN THE README.



# || FILE FOR INPUT (THIS IS WHAT YOU ARE LOOKING FOR MOST LIKELY)
# open the formatted file (look in README to generate)
with open("games.txt") as f: # CHANGE games.txt TO MATCH YOUR TEXT FILE. GAMES.TXT IS JUST MY CHOICE
    games = [line.strip() for line in f if line.strip()]



# || DATA MODELS
# make a player, contains most data
def make_player():
    return {
        "tankwins": 0, "tanklosses": 0,
        "dpswins": 0, "dpslosses": 0,
        "supportwins": 0, "supportlosses": 0,
        "wins": 0, "losses": 0, "games": 0,
        "mvps": 0,
        "mvpwins": 0,
        "mvplosses": 0
    }

# make comp. these dont consider the roles of the team at all
# purely just players, interesting to have. better in small datasets
def make_comp():
    return {
        "wins": 0, "losses": 0, "games": 0
    }

# make role comp, considers the roles of the team
# better in large datasets but super interesting
def make_role_comp():
    return {
        "wins": 0, "losses": 0, "games": 0
    }

# create dicts to save multiple players/comps
# data storing is setup. parse next
player_stats = defaultdict(make_player)
comp_stats = defaultdict(make_comp)
role_comp_stats = defaultdict(make_role_comp)



# || PARSING
# helper function to parse mvps out of names
# result is the name minus (mvp) if present and true (for removal) or false (for no need).
def parse_name(name):
    name.strip()
    if name.endswith("(mvp)"):
        return name.replace("(mvp)", ""), True
    return name, False

# parse the notable game stats out of the line, mvp is still included for now
# result is dictionary of the game, showing the tanks, dps, and support, and then a result win or loss
# at this point tank could be something like: luke,mar(mvp).
def parse_game(line):
    tank_player, dps_player, support_player, result = line.split("/")
    return { "tank": tank_player, "dps": dps_player, "support": support_player }, result # return dictionary and result



# helper function for printing
def winrate(wins, games):
    return (wins / games * 100) if games else 0



# TODO, extract_players for non role specific winrates

    

# || AGGREGATION
# for each game, add relevant stats
for line in games:
    roles, result = parse_game(line)

    # add stats for each player from the current game
    for role, names in roles.items():
        if names == "none":
            continue

        # if multiple names, split with , and run for each
        for raw in names.split(","):
            name, is_mvp = parse_name(raw) # remove mvp if present

            player_stats[name]["games"] += 1 # yeah man they played a game

            if is_mvp:
                player_stats[name]["mvps"] += 1

            # im considering adding mvp tracking for each role. might be cluttered. but also i really enjoy how specific the data is
            if result == "win":
                player_stats[name][f"{role}wins"] += 1 # add 1 to role winrate
                player_stats[name]["wins"] += 1
                player_stats[name]["mvpwins"] += is_mvp # add 1 if true, 0 if false to mvpwins
            else:
                player_stats[name][f"{role}losses"] += 1 # add 1 to role winrate
                player_stats[name]["losses"] += 1
                player_stats[name]["mvplosses"] += is_mvp # add 1 if true, 0 if false to mvpwins


# || PRINTING
# print individual players stats
for player, stats in sorted(player_stats.items()):
    print(f"\n===== {player} =====") # 5 ='s on left plus a space centers it above the following
    print(f"  Tank:    {stats['tankwins']}W / {stats['tanklosses']}L")
    print(f"  DPS:     {stats['dpswins']}W / {stats['dpslosses']}L")
    print(f"  Support: {stats['supportwins']}W / {stats['supportlosses']}L")
    print(f"  Overall: {stats['wins']}W / {stats['losses']}L")
    print(f"  Winrate: {winrate(stats['losses'],stats['wins']):.1f}%") # colon here is a format specifier. just set to 1 decimal point

    # im making it so mvp only prints if they have mvp stats. overwatch players have zero use for it.
    if stats['mvps'] > 0:
        print(f"    MVPs: {stats['mvps']}")
        print(f"    MVP Ratio: {stats['mvpwins']}W / {stats['mvplosses']}L")




# print non role comps (2 or more) to avoid some clutter, 1 is reasonable if you want to change this. i just prefer less clutter and who cares about 1 game.

# print role comps (3 or more) would be really cluttered with less
