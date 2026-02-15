# the README explains how to use this in depth. look there first
# it is very entertaining (and useful) to tweak a lot of this stuff to see different results.
# if you have some python experience i would recommend doing it.
# if you need help, ask me, if you have something you think should be added let me know.

from games.hero_shooter import run as run_hero_shooter

# THIS IS WHERE YOU CHANGE THE FILE NAME!
with open("games.txt") as f: # (change the name of "games.txt" here to your specific text document)
    games = [line.strip() for line in f if line.strip()]

# run correct tracker based on game type
run_hero_shooter(games)
