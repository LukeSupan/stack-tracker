# import functions
from core.parsing import parse_name_and_tags

# result is winrate, given wins and games, returns 0 for no games
def winrate(wins, games):
    return (wins / games * 100) if games else 0

# extract a set of all player names from the parsed team dict from parse_game_line
# tags are cut away here.
# result is the set of the comp to be updated
def extract_players(team):
    players = set()

    # for games with roles
    if isinstance(team, dict):
        for slot in team.values():
            if slot != "none":
                for names in slot.split(","):
                    name, _, _ = parse_name_and_tags(names) # we arent using tags here. hence _s
                    players.add(name)

    # for games without roles.
    else:
        for name in team:
            name, _, _ = parse_name_and_tags(name)
            players.add(name)

    return players

# sort the comps of a certain size by winrate (games if equal)
# works for both role-based and non role-based comps
# returns a tuple (winrate, games) for sorting the comps when given a comps stats from dict
def comp_sort_key(comp_stats):
    _, stats = comp_stats
    return (
        winrate(stats["wins"], stats["games"]),
        stats["games"]
    )
# sort by games played (desc), then by team1 winrate
def matchup_sort_key(matchup_stats):
    matchup, stats = matchup_stats

    # calculate winrate per team
    winrates = [
        stats["wins"][team] / stats["games"] if stats["games"] > 0 else 0
        for team in matchup
    ]

    max_winrate = max(winrates)  # or avg(winrates) if you prefer
    games_played = stats["games"]

    # sort by max_winrate first, then games played
    return (max_winrate, games_played)

# generate a string as a key for a role-based comp
# gets rid of MVP, sorts alphabetically per role, then joins the roles with a /. making a final string key
# returns a generated string as a key
def get_role_comp_key(team, role_labels):
    players = []  # players like non role comps, but as a list. so order matters

    # we need to get members for role1, role2, and role3, just like before.
    # sort each slot alphabetically so it doesn’t matter
    for role in role_labels:
        slot = team[role]  # check each slot

        if slot == "none":
            players.append("")  # this role is empty nothing else to do here
            continue


        # before adding them to the key we need to get rid of tags,
        # otherwise we get duplicate comps, its also ugly.
        clean_names = []

        for raw in slot.split(","):
            name = parse_name_and_tags(raw)[0] # get only the name
            clean_names.append(name)

        sorted_players = sorted(clean_names)

        # add the final string to its slot in the list
        players.append(", ".join(sorted_players))

    # make one final string by joining with /
    return "/".join(players)
# result is like alice,bob/robert/aiden or alice//bob or alice// or //bob or /aiden/

# count the number of unique players in current role-based comp key
# cant just do length like with non role because the string is formatted (with /s and ,s)
# returns the size of the team comp
def role_comp_team_size(role_comp_key):
    slots = role_comp_key.split("/")
    players = set()
    for slot in slots:
        names = slot.strip()
        if names != "none":
            for name in names.split(", "):
                players.add(name)
    return len(players)
