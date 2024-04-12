# wordle
Small set of scripts to "solve" [wordle](https://www.nytimes.com/games/wordle/index.html), so you dont have to play it if you don't want to
- originally made this with my dad during christmas break '21 when wordle first went viral
- revisited it when Gurur and I started playing together

See also
- [3Blue1Brown](https://youtu.be/v68zYyaEmEA?si=Cp5qJyPri68OGBQ-) video
- the official [WordleBot](https://www.nytimes.com/interactive/2022/upshot/wordle-bot.html)

Though we beat both to publishing, despite no citations 😵‍💫

## Basic idea
The potential scores of a guess `g` induces a partitioning over the set of possible solutions `E`
- given the score, `E` can be updated to all words in `E` that could yield that score

The "best" (greedy) `g` is the one whose score induces a maximum entropy partitioning over `E`
- I think this might be a shortest-path DP type problem, but the greedy case seems to work quite well
- IIRC the [3Blue1Brown](https://youtu.be/v68zYyaEmEA?si=Cp5qJyPri68OGBQ-) video or a follow up explores this

## Setup
If you want to play, the first guess is the most computationally intensive and should be cached before hand.
- The scripts might assume that you use my first guess, `slate`

In either case, run ```python ./cache.py FIRST_GUESS```

Then you can run ```python ./play.py [SOLUTION]```
- you can play "in real time" if you dont have the solution
- if you have the solution, this just makes it so the score is computed automatically
