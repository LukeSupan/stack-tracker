from core.parsing import parse_name_and_mvp

# result is winrate, given wins and games, returns 0 for no games
def winrate(wins, games):
    return (wins / games * 100) if games else 0

# extract a set of all player names from the parsed team dict from parse_game_line
# mvp is cut away here.
# result is the set of the comp to be updated
def extract_players(team):
    players = set()

    # for each slot of value, split if needed and add to the players set
    for slot in team.values():
        if slot != "none":
            for names in slot.split(","):
                name, _ = parse_name_and_mvp(names) # we arent using is_mvp here. hence _
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

# TODO, MAKE MORE GENERIC
# generate a string as a key for a role-based comp
# gets rid of MVP, sorts alphabetically per role, then joins the roles with a /. making a final string key
# IF YOU WANT YOUR FINAL RESULT OF THE PRINTING TO LOOK DIFFERENT. CHANGE IT HERE. BUT. YOU NEED TO ACCOUNT FOR THIS CHANGE IN role_comp_team_size BELOW
def get_role_comp_key(team):
    players = [] # players like above but as a list. so it matters 

    # we need to get member for tank, dps, and support, just like before. sort each slot alphabetically so it doesnt matter
    for role in ("role1", "role2", "role3"):
        slot = team[role] # check each slot
        if slot == "none":
            players.append(f"{role}: none") # this role is empty
        else:
            
            # before adding them to the key. we need to get rid of mvp, otherwise we get duplicate comps.
            clean_names = []
            for raw in slot.split(","):
                name, _ = parse_name_and_mvp(raw)
                clean_names.append(name)

            sorted_players = sorted(clean_names)
            names = ", ".join(sorted_players) # rejoin the list back into a string with a comma (with a space to look better), basically just makes sure we have no duplicate role comp
            players.append(f"{role}: {names}") # add the final string to its slot in the list (THIS IS WHERE YOU WOULD CHANGE THE FORMATTING. IF YOU DO ANOTHER FUNCTION (role_comp_team_size) NEEDS TO CHANGE A GOOD BIT.
    return " / ".join(players) # make one final string by joining with

# count the number of unique players in role-based comp key
# cant just do length like with the other because the string is formatted
# if you change the formatting above, you are going to have to change this to account for it. sorry.
def role_comp_team_size(role_comp_key):
    slots = role_comp_key.split(" / ")
    players = set()
    for slot in slots:
        _, names = slot.split(":")
        names = names.strip()
        if names != "none":
            for name in names.split(", "):
                players.add(name)
    return len(players)
