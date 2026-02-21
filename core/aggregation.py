# update stats from parsed input

# function imports
from core.parsing import parse_name_and_tags
from core.utils import extract_players, get_role_comp_key

# update the games values for each player on current team
# does not return, updates player_stats directly
# TODO add per role mvp stats, would be really cool, but probably bloated. but... so cool...
def update_player_stats(player_stats, team, result): 
    for role, names in team.items():
        if names.lower() == "none":
            continue

        # in this slot, split to get each player for this role
        for raw in names.split(","):
            name, is_mvp, is_key = parse_name_and_tags(raw) # remove tags from name but remember if they were there

            player_stats[name]["games"] += 1

            # mvp or key tag updates (from parse_name_and_tags)
            if is_mvp:
                player_stats[name]["mvps"] += 1
            elif is_key:
                player_stats[name]["keys"] += 1

            if result == "win":
                player_stats[name]["roles"][role]["wins"] += 1
                player_stats[name]["wins"] += 1
                player_stats[name]["mvpwins"] += is_mvp # add 1 if true, 0 if false to mvpwins
                player_stats[name]["keywins"] += is_key # add 1 if true, 0 if false to keywins
            else:
                player_stats[name]["roles"][role]["losses"] += 1
                player_stats[name]["losses"] += 1
                player_stats[name]["mvplosses"] += is_mvp # add 1 if true, 0 if false to mvplosses
                player_stats[name]["keylosses"] += is_key # add 1 if true, 0 if false to keylosses

    return

# update the game values for each player on current team (without roles)
# does not return, updates player_stats directly
def update_player_stats_generic(player_stats, team, result):
    # no need for splitting, team is a list that was pre split
    for raw in team:
        name, is_mvp, is_key = parse_name_and_tags(raw) # remove tags from name but remember if they were there

        player_stats[name]["games"] += 1

        if is_mvp:
            player_stats[name]["mvps"] += 1
        elif is_key:
            player_stats[name]["keys"] += 1

        if result == "win":
            player_stats[name]["wins"] += 1
            player_stats[name]["mvpwins"] += is_mvp # add 1 if true, 0 if false to mvpwins
            player_stats[name]["keywins"] += is_key # add 1 if true, 0 if false to keywins
        else:
            player_stats[name]["losses"] += 1
            player_stats[name]["mvplosses"] += is_mvp # add 1 if true, 0 if false to mvplosses
            player_stats[name]["keylosses"] += is_key # add 1 if true, 0 if false to keylosses



# update the current team comp, not caring about roles
# does not return anything, updates comp_stats directly
def update_comp_stats(comp_stats, team, result):
    comp_key = tuple(sorted(extract_players(team))) # sorts a tuple of players to use as key
    comp_stats[comp_key]["games"] += 1

    if result == "win":
        comp_stats[comp_key]["wins"] += 1
    else:
        comp_stats[comp_key]["losses"] += 1

    return

# update the current team comp, its unique based on roes
# does not return anything, updates role_comp_stats directly
def update_role_comp_stats(role_comp_stats, team, result, role_labels):
    role_comp_key = get_role_comp_key(team, role_labels) # get key to update
    role_comp_stats[role_comp_key]["games"] += 1

    if result == "win":
        role_comp_stats[role_comp_key]["wins"] += 1
    else:
        role_comp_stats[role_comp_key]["losses"] += 1

    return


# update the matchup_stats
def update_matchup_stats(matchup_stats, teams_list, results_list):
    # team data will be a list of tuples: (comp_key, result)
    team_data = []

    # combine list of teams with their respective results
    # make list of 2-tuple in team_data
    for team, result in zip(teams_list, results_list):
        # make sure extract_players returns a list of names
        comp_key = tuple(sorted(extract_players(team)))
        team_data.append((comp_key, result))

    # sort by comp_key for canonical matchup_key
    team_data.sort(key=lambda x: x[0])

    # matchup key is a tuple of all comp keys
    matchup_key = tuple(comp_key for comp_key, _ in team_data)

    # add games
    matchup_stats[matchup_key]["games"] += 1

    # add wins and losses
    for comp_key, result in team_data:
        if result.lower() == "win":
            matchup_stats[matchup_key]["wins"][comp_key] += 1
        else:
            matchup_stats[matchup_key]["losses"][comp_key] += 1
