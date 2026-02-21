# make a new player, contains all individual data. bulk of information.
# you can see most of these things on tracking sites. but you can control the data here
# im considering redoing the role parts so that it isnt as static. havent decided yet.

# defaultdict will automatically intitialize new keys when they appear

# players on each team
from collections import defaultdict


def make_player(role_labels):
    return {
        # general stats
        "wins": 0, "losses": 0, "games": 0,

        # dynamic roles
        "roles": {
            role: {"wins": 0, "losses": 0}
            for role in role_labels
        },

        # tags stats
        "mvps": 0,
        "mvpwins": 0,
        "mvplosses": 0,

        "keys": 0,
        "keywins": 0,
        "keylosses": 0
    }



# comps that ignore roles
def make_comp():
    return {
        "wins": 0, "losses": 0, "games": 0
    }

# comps that are made unique by role placements
def make_role_comp():
    return {
        "wins": 0, "losses": 0, "games": 0
    }

# comps that ignore roles
def make_matchup():
        return {
        "games": 0,
        "wins": defaultdict(int),
        "losses": defaultdict(int)
    }