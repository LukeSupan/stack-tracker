# prints the final aggregated data
# just in the terminal for now. may change

# import functions
from core.utils import winrate, comp_sort_key, role_comp_team_size, matchup_sort_key

# colors and styles for printing, autoreset resets styles (thats required)
from colorama import init, Fore, Style
init(autoreset=True)

# constants for formatting
LINE = "─" * 55 # forms a line for sections
TOTAL_WIDTH = 35 # total line width
ROLE_WIDTH = 10 # width of role labels


# || FORMATTING FUNCTIONS
# large sections, 3 max
def section(title):
    print(f"\n{Style.BRIGHT}{Fore.MAGENTA}{title}")
    print(f"{Fore.MAGENTA}{LINE}")

# underlining subsections (comp sizes)
def subsection(title):
    print(f"\n{Fore.CYAN}{title}")
    print("·" * len(title))

# format the winrecord
def format_record(w, l):
    return f"{w}W / {l}L"


# || PRINTING FUNCTIONS
# print individual players stats formatted in terminal
# doesn't return anything, just prints.
def print_player_stats(player_stats, role_labels):

    section("PLAYER STATS")

    # print all of the stats of this player
    for player, stats in sorted(player_stats.items()):
        print(f"\n{Style.BRIGHT}{player.center(22)}")
        print("─" * 22)

        # role_stats, if there are no roles (just players) skip.
        if len(role_labels) != 1:
            for role in role_labels:
                role_stats = stats["roles"][role]
                print(f"  {role:<{ROLE_WIDTH}} {format_record(role_stats['wins'], role_stats['losses'])}")


        print(f"\n  {'Overall':<{ROLE_WIDTH}} {format_record(stats['wins'], stats['losses'])}")
        print(f"  {'Winrate':<{ROLE_WIDTH}} {winrate(stats['wins'], stats['games']):.1f}%")

        # mvp usually only occurs for wins (in deadlock), in marvel rivals its both
        # keys are only in deadlock
        if stats["mvps"] > 0:
            print(f"\n  {'MVPs':<{ROLE_WIDTH}} {stats['mvps']}")
            print(f"  {'MVP Rate':<{ROLE_WIDTH}} {winrate(stats['mvps'], stats['games']):.1f}%")
            if stats["mvplosses"] != 0: # useless stat for deadlock, so we hide it
                    print(f"  {'MVP W/L':<{ROLE_WIDTH}} {format_record(stats['mvpwins'], stats['mvplosses'])}")

        if stats["keys"] > 0:
            print(f"\n  {'Keys':<{ROLE_WIDTH}} {stats['keys']}")
            print(f"  {'Key Rate':<{ROLE_WIDTH}} {winrate(stats['keys'], stats['games']):.1f}%")
            print(f"  {'Key W/L':<{ROLE_WIDTH}} {format_record(stats['keywins'], stats['keylosses'])}")

        if (stats["keys"] > 0) and (stats["mvps"] > 0):
            print(f"\n  {'MVP+Keys':<{ROLE_WIDTH}} {stats['keys'] + stats['mvps']}")
            print(f"  {'MVP/Key rate':<{ROLE_WIDTH}} {winrate(stats['keys'] + stats['mvps'], stats['games']):.1f}%")

    return

# this is one of the most interesting parts. you can see who is weak. and strong i suppose
# min games is the minimum games required to print a comp
# doesn't return anything, just prints the comps formatted in the terminal
def print_non_role_comps(comp_stats, min_games=1):

    # if any of these statements are false, do not print the header, it wont have anything later
    has_data = any(
        stats["games"] >= min_games
        for stats in comp_stats.values()
    )

    if not has_data:
        return

    section("\nNON-ROLE COMPS")

    # print in order of smallest to largest team size first
    team_sizes = sorted({len(comp) for comp in comp_stats})

    # print each of the teams for each of the sizes that need to be printed.
    for size in team_sizes:

        # use list comprehension to make a new list
        # gather comps of this size. you can limit the number of games needed here with stats["games"] > x
        # result is a list of tuples: (("alice", "bob"), {"wins": 1.....}), and so on
        sized_comps = [
            (comp, stats) # we are adding comps and their stats to the list, output
            for comp, stats in comp_stats.items() # this gets all comps, iteration
            if len(comp) == size and stats["games"] >= min_games # get only comps of this size, filter
        ]

        # if this size is empty, we dont print the title card and move on
        if not sized_comps:
            continue

        subsection(f"{size}-PLAYER TEAMS")

        # sort by winrate, the key is winrate first, games played as backup
        sized_comps.sort(key=comp_sort_key, reverse=True)
        
        # print the comps in order
        for comp, stats in sized_comps:
            names = ", ".join(comp) # combine names for the comp
            print(f"{names:{TOTAL_WIDTH}} {winrate(stats["wins"], stats["games"]):5.1f}% ({stats['games']} games)") # pad to reach TOTAL_WIDTH spaces, 5 spaces to have it line up nice

    return

# min games is the minimum games required to print a comp
# doesn't return anything, just prints the comps formatted in the terminal
def print_role_comps(role_comp_stats, role_labels, min_games=3):

    # if any of these statements are false, do not print the header
    has_data = any(
        stats["games"] >= min_games
        for stats in role_comp_stats.values()
    )

    if not has_data:
        return

    section("\nROLE COMPS")

    # print in order of smallest to largest team size first
    team_sizes = sorted({role_comp_team_size(role_comp) for role_comp in role_comp_stats})

    # print all games for each size
    for size in team_sizes:
        # use list comprehension to make a new list
        # gather comps of this size. you can limit the number of games needed here with stats["games"] > x
        # result is a list of tuples: (("alice", "bob"), {"wins": 1.....}), and so on
        sized_role_comps = [
            (role_comp, stats) # we are adding comps and their stats to the list, output
            for role_comp, stats in role_comp_stats.items() # this gets all comps, iteration
            if role_comp_team_size(role_comp) == size and stats["games"] >= min_games # need at least 3 games. theres not much of a pattern before that. the clutter is crazy. you can change it if youd like to play around
        ]

        # if its empty, we dont print the title card and move on
        if not sized_role_comps:
            continue

        # sort by winrate (highest first), then by number of games (highest first as tiebreaker)
        sized_role_comps.sort(key=comp_sort_key, reverse=True)

        # header is used as labels for the roles
        subsection(f"{size}-PLAYER TEAMS")
        header = " | ".join(role_labels) # use the role_labels as a header

        print(f"{Style.BRIGHT}{header:{TOTAL_WIDTH}}{Style.RESET_ALL}")

        # we have the comps for this size, print them nicely
        for role_comp, stats in sized_role_comps:

            print_list = []
            # split by /'s for roles, print title for each
            slots = role_comp.split("/")
            for slot in slots:

                # add a copy of the raw text basically.
                # if i dont do this it counts the invisible color characters. i want to keep those. they are cool...
                if slot:
                    slot_text = slot
                else:
                    slot_text = "none"
                
                print_list.append(slot_text)

            # join and print the comp
            role_comp_print = " | ".join(print_list)
            print(f"{role_comp_print:{TOTAL_WIDTH}} {winrate(stats['wins'], stats['games']):5.1f}% ({stats['games']} games)")

    return
            
def print_matchups(matchup_stats, min_games=1):

    # check if anything should print
    has_data = any(
        stats["games"] >= min_games
        for stats in matchup_stats.values()
    )

    if not has_data:
        return

    section("MATCHUPS")

    # filter usable matchups
    filtered = [
        (matchup, stats)
        for matchup, stats in matchup_stats.items()
        if stats["games"] >= min_games
    ]

    # after filtering, sort each matchup by games played
    filtered.sort(key=lambda item: item[1]["games"], reverse=True)

    # print matchups
    for teams, stats in filtered:

        # get the team names, wins, and losses for each team
        team_names = [", ".join(team) for team in teams]
        team_wins = [stats["wins"][team] for team in teams]

        # join the team names with vs
        print(" vs ".join(team_names))
        print("Record:", team_wins)
        print("Total Games:", stats["games"])
        print()
