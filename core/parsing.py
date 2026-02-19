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
def parse_game_line_roles(line, role_labels):
    parts = line.strip().split("/")

    expected = len(role_labels) + 1

    # make an error for bad input to make it easy to find.
    if len(parts) != expected:
        raise ValueError(
            f"Bad input: {line}\n"
            f"Expected {expected} sections but got {len(parts)}"
        )
    
    *role_parts, result = parts

    # maybe add a catch here at some point TODO

    # gather however many roles there are and zip the role labels to the role parts on this line
    # result is like: left: bob | mid: alice | right: aiden
    team = dict(zip(role_labels, role_parts))

    return team, result # return 2-tuple with the dictionary and result

# parse each player out of the line, individual players are also parsed out
# result is a list of the members, and then a result win or loss
# at this point the players still have their tags
def parse_game_line_generic(line):
    players_part, result = line.strip().split("/")

    team = []
    for player in players_part.split(","):
        team.append(player)

    return team, result
