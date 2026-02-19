from collections import defaultdict
from core.aggregation import update_comp_stats, update_player_stats, update_role_comp_stats
from core.models import make_player, make_comp, make_role_comp
from core.parsing import parse_game_line_roles
from core.printing import print_non_role_comps, print_player_stats, print_role_comps
from core.config import GAME_CONFIGS

def run(games):

    role_labels = GAME_CONFIGS["lanes_detailed"]
    player_stats = defaultdict(lambda: make_player(role_labels))
    comp_stats = defaultdict(make_comp)
    role_comp_stats = defaultdict(make_role_comp)

    # aggregate stats for 3 lanes
    for line in games:
        team, result = parse_game_line_roles(line, role_labels)

        update_player_stats(player_stats, team, result) # each player
        update_comp_stats(comp_stats, team, result) # each comp, regardless of role
        update_role_comp_stats(role_comp_stats, team, result, role_labels) # specific roles makes comps unique

    # printing final results
    print_player_stats(player_stats, role_labels)
    print_non_role_comps(comp_stats, 1) # TODO REPLACE WITH DECLARED NUMBER FOR EASY CHANGE, would be cool to let user do it with the input file, might be complicated so ill make it optional, 1 and 3 are default
    print_role_comps(role_comp_stats, role_labels, 2) # TODO REPLACE WITH DECLARED NUMBER FOR EASY CHANGE, would be cool to let user do it with the input file, might be complicated so ill make it optional, 1 and 3 are default
