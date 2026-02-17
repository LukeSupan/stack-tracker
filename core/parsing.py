# --------------------------
# PARSING FUNCTIONS
# --------------------------
# parse mvps out of names.
# result is the name minus (mvp) if present and true (for removal) or false (for no need).
def parse_name_and_tags(name):
    name = name.strip()
    if name.endswith("(mvp)"):
        return name.replace("(mvp)", ""), True, False
    elif name.endswith("(key)"):
        return name.replace("(key)", ""), False, True
    return name, False, False

# parse the notable game stats out of the line, mvp is still included for now
# result is dictionary of the game, showing the roles, and then a result win or loss
# at this point role1 - role3 could still be something like: luke,mar(mvp).
def parse_game_line_roles(line):
    role1_player, role2_player, role3_player, result = line.strip().split("/")
    return { "role1": role1_player, "role2": role2_player, "role3": role3_player }, result # return 2-tuple with dictionary and result



def parse_game_line_generic(line):
    players_part, result = line.strip().split("/")

    team = []
    for player in players_part.split(","):
        team.append(player)

    return team, result
