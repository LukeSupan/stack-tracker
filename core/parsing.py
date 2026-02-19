# parse input format into easily usable format

# parse mvp and key tags out of name
# result is the name minus (mvp) or (key) if present and true (for removal) or false (for no need) for each.
# first boolean is mvp, second is key
def parse_name_and_tags(name):
    name = name.strip()
    if name.endswith("(mvp)"):
        return name.replace("(mvp)", ""), True, False
    elif name.endswith("(key)"):
        return name.replace("(key)", ""), False, True
    return name, False, False

# parse each role out of the line, individual players are not parsed out yet
# result is dictionary of the game, showing the roles, and then a result win or loss
# at this point role1 - role3 could still be something like: luke,mar(mvp).
def parse_game_line_roles(line):
    role1_players, role2_players, role3_players, result = line.strip().split("/")
    return { "role1": role1_players, "role2": role2_players, "role3": role3_players }, result # return 2-tuple with dictionary and result

# parse each player out of the line, individual players are also parsed out
# result is a list of the members, and then a result win or loss
# at this point the players still have their tags
def parse_game_line_generic(line):
    players_part, result = line.strip().split("/")

    team = []
    for player in players_part.split(","):
        team.append(player)

    return team, result
