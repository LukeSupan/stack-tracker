
from collections import defaultdict

from core.parsing import parse_name_and_tags
from core.utils import extract_players, get_role_comp_key



# add stats for each player from the current game
def update_player_stats(player_stats, team, result): 
    for role, names in team.items():
        if names == "none":
            continue

        # if multiple names, split with , and run for each
        for raw in names.split(","):
            name, is_mvp, is_key = parse_name_and_tags(raw) # remove mvp from name if present, save mvp status

            player_stats[name]["games"] += 1 # yeah man they played a game

            if is_mvp:
                player_stats[name]["mvps"] += 1
            elif is_key:
                player_stats[name]["keys"] += 1

            # im considering adding mvp tracking for each role. might be cluttered. but also i really enjoy how specific the data is. future thing anyway. if youd like to add it go ahead
            if result == "win":
                player_stats[name][f"{role}wins"] += 1 # add 1 to role winrate
                player_stats[name]["wins"] += 1
                player_stats[name]["mvpwins"] += is_mvp # add 1 if true, 0 if false to mvpwins
                player_stats[name]["keywins"] += is_key # add 1 if true, 0 if false to keywins
            else:
                player_stats[name][f"{role}losses"] += 1 # add 1 to role winrate
                player_stats[name]["losses"] += 1
                player_stats[name]["mvplosses"] += is_mvp # add 1 if true, 0 if false to mvpwins
                player_stats[name]["keylosses"] += is_key # add 1 if true, 0 if false to keylosses

    return


def update_comp_stats(comp_stats, team, result):
    # for this game, adjust the comp stats
    comp_key = tuple(sorted(extract_players(team))) # sort the set, make it a sorted tuple so that we can use it as a key with no duplicates
    comp_stats[comp_key]["games"] += 1

    if result == "win":
        comp_stats[comp_key]["wins"] += 1
    else:
        comp_stats[comp_key]["losses"] += 1

    return


def update_role_comp_stats(role_comp_stats, team, result, role_labels):
    # for this game, adjust the role comp stats
    role_comp_key = get_role_comp_key(team) # more complicated. view the function, but it gets the key
    role_comp_stats[role_comp_key]["games"] += 1

    if result == "win":
        role_comp_stats[role_comp_key]["wins"] += 1
    else:
        role_comp_stats[role_comp_key]["losses"] += 1

    return
