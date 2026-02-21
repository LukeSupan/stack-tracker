from collections import defaultdict
from core.aggregation import update_comp_stats, update_player_stats, update_matchup_stats
from core.models import make_player, make_comp, make_matchup
from core.parsing import parse_game_line_roles
from core.printing import print_non_role_comps, print_player_stats, print_role_comps, print_matchups
from core.config import GAME_CONFIGS

def run(games):

    role_labels = GAME_CONFIGS["generic_versus"]
    player_stats = defaultdict(lambda: make_player(role_labels))
    comp_stats = defaultdict(make_comp)
    matchup_stats = defaultdict(make_matchup)

    # aggregate stats for generic versus games
    for line in games:

        teams_split = line.split("|")

        # SPLIT THE TEAMS AND CALL EACH FUNCTION TWICE, EASY WAY TO START, ADD MATCHUPS ONCE THAT WORKS?
        # return should be, losing team, winning team, then we can easily pass the result 
        
        teams_list = []
        results_list = []

        for team in teams_split:
            team_roles, result = parse_game_line_roles(team, role_labels)
            teams_list.append(team_roles)
            results_list.append(result)

        # process the teams dynamically so there can be any number of words
        for team, result in zip(teams_list, results_list):
            update_player_stats(player_stats, team, result)
            update_comp_stats(comp_stats, team, result)

        # update matchups
        update_matchup_stats(matchup_stats, teams_list, results_list)

    # printing final results
    print_player_stats(player_stats, role_labels)
    print_non_role_comps(comp_stats, 1) # TODO REPLACE WITH DECLARED NUMBER FOR EASY CHANGE, would be cool to let user do it with the input file, might be complicated so ill make it optional, 1 and 3 are default
    print_matchups(matchup_stats, 1) # TODO REPLACE WITH DECLARED NUMBER
