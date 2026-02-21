# the README explains how to use this in depth. look there first
# it is very entertaining (and useful) to tweak a lot of this stuff to see different results.
# if you have some python experience i would recommend doing it.
# if you need help, ask me, if you have something you think should be added let me know.

# import game runners
from games.hero_shooter import run as run_hero_shooter # overwatch, marvel rivals, anything like that
from games.lanes import run as run_lanes
from games.generic import run as run_generic
from games.generic_versus import run as run_generic_versus
from games.moba import run as run_moba
from games.lanes_detailed import run as run_lanes_detailed
from games.hero_shooter_versus import run as run_hero_shooter_versus

# from games.deadlock import run as run_deadlock # could include other games with 3 lanes TODO
# from games.generic import run as run_generic # this is all generic games with no roles. less info but, it does the job
GAME_RUNNERS = {
    "hero_shooter": run_hero_shooter,
    "hero_shooter_versus": run_hero_shooter_versus,
    "generic": run_generic,
    "generic_versus": run_generic_versus,
    "lanes": run_lanes,
    "lanes_detailed": run_lanes_detailed,
    "moba": run_moba
}


# THIS IS WHERE YOU CHANGE THE FILE NAME! CHANGE 
with open("input/rocketleague.txt") as f:
    lines = [line.strip() for line in f if line.strip()]


game_name = lines[0].lower().strip()
games = lines[1:]


# decide which game to run
runner = GAME_RUNNERS.get(game_name)

if not runner:
    raise ValueError(f"{game_name} is not an accepted flag")

# get output
runner(games)
