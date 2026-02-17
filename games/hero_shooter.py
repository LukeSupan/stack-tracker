from collections import defaultdict
from core.models import make_player, make_comp, make_role_comp
from core.parsing import parse_name_and_mvp, parse_game_line_roles
from core.utils import role_comp_team_size, get_role_comp_key, sized_comps_sort_key, extract_players, winrate
from core.printing import print_non_role_comps, print_player_stats, print_role_comps
from core.config import GAME_CONFIGS

# --------------------------
# AGGREGATION
# --------------------------
# total process is:
# parse_game_line -> parse_name_and_mvp for each role on that line -> adjust winrates for players -> extract and adjust both comp types -> print (TODO BASED ON GAMETYPE)

def run(games):

    role_labels = GAME_CONFIGS["hero_shooter"]
    player_stats = defaultdict(make_player)
    comp_stats = defaultdict(make_comp)
    role_comp_stats = defaultdict(make_role_comp)

    # for each game, add relevant stats
    for line in games:
        team, result = parse_game_line_roles(line)

        # add stats for each player from the current game
        for role, names in team.items():
            if names == "none":
                continue

            # if multiple names, split with , and run for each
            for raw in names.split(","):
                name, is_mvp = parse_name_and_mvp(raw) # remove mvp from name if present, save mvp status

                player_stats[name]["games"] += 1 # yeah man they played a game

                if is_mvp:
                    player_stats[name]["mvps"] += 1

                # im considering adding mvp tracking for each role. might be cluttered. but also i really enjoy how specific the data is. future thing anyway. if youd like to add it go ahead
                if result == "win":
                    player_stats[name][f"{role}wins"] += 1 # add 1 to role winrate
                    player_stats[name]["wins"] += 1
                    player_stats[name]["mvpwins"] += is_mvp # add 1 if true, 0 if false to mvpwins
                else:
                    player_stats[name][f"{role}losses"] += 1 # add 1 to role winrate
                    player_stats[name]["losses"] += 1
                    player_stats[name]["mvplosses"] += is_mvp # add 1 if true, 0 if false to mvpwins


        # for this game, adjust the comp stats
        comp_key = tuple(sorted(extract_players(team))) # sort the set, make it a sorted tuple so that we can use it as a key with no duplicates
        comp_stats[comp_key]["games"] += 1

        if result == "win":
            comp_stats[comp_key]["wins"] += 1
        else:
            comp_stats[comp_key]["losses"] += 1


        # for this game, adjust the role comp stats
        role_comp_key = get_role_comp_key(team) # more complicated. view the function, but it gets the key
        role_comp_stats[role_comp_key]["games"] += 1

        if result == "win":
            role_comp_stats[role_comp_key]["wins"] += 1
        else:
            role_comp_stats[role_comp_key]["losses"] += 1



    # --------------------------
    # PRINTING
    # --------------------------
    # print individual players stats. if deadlock print lane instead of tank type
    print_player_stats(player_stats, role_labels)

    print_non_role_comps(comp_stats, 1) # TODO REPLACE WITH DECLARED NUMBER FOR EASY CHANGE, would be cool to let user do it with the input file

    print_role_comps(role_comp_stats, 3) # TODO REPLACE WITH DECLARED NUMBER FOR EASY CHANGE, would be cool to let user do it with the input file
    