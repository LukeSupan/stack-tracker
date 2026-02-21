from collections import defaultdict
from core.aggregation import update_comp_stats, update_player_stats, update_role_comp_stats, update_matchup_stats
from core.models import make_player, make_comp, make_role_comp, make_matchup
from core.parsing import parse_game_line_roles
from core.printing import print_non_role_comps, print_player_stats, print_role_comps, print_matchups
from core.config import GAME_CONFIGS

def run(games):

    role_labels = GAME_CONFIGS["hero_shooter_versus"]
    player_stats = defaultdict(lambda: make_player(role_labels))
    comp_stats = defaultdict(make_comp)
    role_comp_stats = defaultdict(make_role_comp)
    matchup_stats = defaultdict(make_matchup)

    # aggregate stats for hero shooters
    for line in games:

        teams = line.split("|")

        # SPLIT THE TEAMS AND CALL EACH FUNCTION TWICE, EASY WAY TO START, ADD MATCHUPS ONCE THAT WORKS?
        # return should be, losing team, winning team, then we can easily pass the result 
        team1, result1 = parse_game_line_roles(teams[0], role_labels)
        team2, result2 = parse_game_line_roles(teams[1], role_labels)

        # run first team
        update_player_stats(player_stats, team1, result1) # each player
        update_comp_stats(comp_stats, team1, result1) # each comp, regardless of role
        update_role_comp_stats(role_comp_stats, team1, result1, role_labels) # specific roles makes comps unique

        # run second team
        update_player_stats(player_stats, team2, result2) # each player
        update_comp_stats(comp_stats, team2, result2) # each comp, regardless of role
        update_role_comp_stats(role_comp_stats, team2, result2, role_labels) # specific roles makes comps unique

        # update matchups, we have team1, team2, and the results, so, cool! (result 1 is used for calculation)
        update_matchup_stats(matchup_stats, team1, team2, result1)

    # printing final results
    print_player_stats(player_stats, role_labels)
    print_non_role_comps(comp_stats, 1) # TODO REPLACE WITH DECLARED NUMBER FOR EASY CHANGE, would be cool to let user do it with the input file, might be complicated so ill make it optional, 1 and 3 are default
    print_role_comps(role_comp_stats, role_labels, 3) # TODO REPLACE WITH DECLARED NUMBER FOR EASY CHANGE, would be cool to let user do it with the input file, might be complicated so ill make it optional, 1 and 3 are default
    print_matchups(matchup_stats, 1)
