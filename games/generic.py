from collections import defaultdict
from core.aggregation import update_comp_stats, update_player_stats_generic
from core.models import make_player, make_comp
from core.parsing import parse_game_line_generic
from core.printing import print_non_role_comps, print_player_stats_generic

def run(games):
    player_stats = defaultdict(make_player)
    comp_stats = defaultdict(make_comp)

    # aggregate stats for hero shooters
    for line in games:
        team, result = parse_game_line_generic(line)

        # update_player_stats_generic(player_stats, team, result) # each player
        update_player_stats_generic(player_stats, team, result)
        update_comp_stats(comp_stats, team, result) # each comp, there are no roles in generic

    # printing final results
    print_player_stats_generic(player_stats)
    print_non_role_comps(comp_stats, 1) # TODO REPLACE WITH DECLARED NUMBER FOR EASY CHANGE, would be cool to let user do it with the input file, might be complicated so ill make it optional, 1 and 3 are default
