from core.parsing import parse_name_and_tags

# result is winrate, given wins and games, returns 0 for no games
def winrate(wins, games):
    return (wins / games * 100) if games else 0

# extract a set of all player names from the parsed team dict from parse_game_line
# mvp is cut away here.
# result is the set of the comp to be updated
def extract_players(team):
    players = set()

    # for games with roles
    if isinstance(team, dict):
        for slot in team.values():
            if slot != "none":
                for names in slot.split(","):
                    name, _, _ = parse_name_and_tags(names) # we arent using is_mvp here. hence _
                    players.add(name)
    # for games without roles.
    else:
        for name in team:
            name, _, _ = parse_name_and_tags(name)
            players.add(name)


    return players

# sort the comps of a certain size by winrate (games if equal)
# works for both role-based and non role-based
# returns a tuple (winrate, games) for sorting the comps when given a comps stats from dict
def sized_comps_sort_key(comp_stats):
    _, stats = comp_stats
    return (
        winrate(stats["wins"], stats["games"]),
        stats["games"]
    )

# generate a string as a key for a role-based comp
# gets rid of MVP, sorts alphabetically per role, then joins the roles with a /. making a final string key
def get_role_comp_key(team):
    players = []  # players like above but as a list. so order matters

    # we need to get members for role1, role2, and role3, just like before.
    # sort each slot alphabetically so it doesn’t matter
    for role in ("role1", "role2", "role3"):
        slot = team[role]  # check each slot

        if slot == "none":
            players.append("")  # this role is empty nothing else to do here

        else:
            # before adding them to the key we need to get rid of mvp,
            # otherwise we get duplicate comps, its also ugly.
            clean_names = []

            for raw in slot.split(","):
                name, _, _ = parse_name_and_tags(raw)
                clean_names.append(name)

            sorted_players = sorted(clean_names)

            # add the final string to its slot in the list
            players.append(", ".join(sorted_players))

    # make one final string by joining with /
    return "/".join(players)
# result is like aiden,luke/jr/bea or aiden//jr or aiden// or //aiden or /aiden/


# count the number of unique players in current role-based comp key
# cant just do length like with the other because the string is formatted
# if you change the formatting above, you are going to have to change this to account for it. sorry.
def role_comp_team_size(role_comp_key):
    slots = role_comp_key.split("/")
    players = set()
    for slot in slots:
        names = slot.strip()
        if names != "none":
            for name in names.split(", "):
                players.add(name)
    return len(players)
