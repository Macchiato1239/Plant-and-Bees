# Link to repo:
https://github.com/Macchiato1239/Plant-and-Bees

# WHat is included:
1. Settings to run the game
2. How to run the game
3. Game information
4. Structure of the game
5. Testing
6. Exception handling
7. Author notes

# 1. Settings to run the game
- Python 3.14+



# 2. How to run the game

# 3. Game information
## 3.1. Tower
1. Soldier has fairly good dps: 10 dmg per shot and 0.5s cooldown -> 20 dps, the price is 250
2. Freezer has a dps of 6.25 but it applies freeze debuff on enemy, which is pretty good, the price is 400
3. Minigunner has a dps of 75 so the price is 2000, idk if i should change the cost in the future
4. Farm is a bit tricky but VERY CRUCIAL if you have never played tds or btd, if you have killed every enemy in a wave, the game will reward you the farm's income * the amount of farm you have. Farm's income is currently 100/wave
## 3.2. Enemy
1. Enemy is simpler than how i intended to implement, but due to time constraint, i decided to not implement enemy buff
2. Enemy two main points are health and speed, some have health but low speed and vice versa. Some can have both.
3. To make it easier to visualize, blue hue enemy is usually quick while, while green is not. The darker the enemy, the more health it has.
# 4. Structure of the game
1. This project uses tkinter, which is a BUILT IN module of python, to create windows and handle visual implementation.
2. 

# 5. Testing
Steps to run the tests
1. Install dependencies
python3 -m pip install --break-system-packages pytest pytest-cov
2. Run the test suite
-> Navigate to project root -> cd Plant-and-Bees -> python3 -m pytest
3. To get a coverage report (a new one)
-> python3 -m pytest --cov=Base --cov=Manager --cov=States --cov=Head --cov-report=term-missing --cov-report=markdown:MarkDown/coverage.md

# 6. Exception handling

## 6.1 Built in exceptions

## 6.2. Custom exceptions

# 7. Author notes
- If you looked into the previous commits, the initial name of the project is plant-and-bees, this is inspired by my friend who is also doing an oop project that has actual characters and world building in them.
- But i changed the project to simply tower defense, which is rather basic, this is mainly because i faced many difficulties while trying to implement the game core functions and had to keep modifying its structures. 
- Due to the difficulties of the project that i put myself on, i decided to strip the project of its world building so that i can focus on the technical side of it. If i had more time, i would have gotten into world building and make the towers and enemies more balanced, interesting. Initially i also made more than 3 tower types and intended to implement buff for enemies, but i supposed that would be scope creep for what the purpose of this project.

===
Previously, i designed the towers in a way that every behavior is handled inside tower manager. This makes future update and modification much harder, for example: add a new tower type would require modifying codes in dictionary, module_tower and tower manager (too much and a bad design i would say). Apparently, this does not also follow the second priciple of SOLID

Even though i have thought of this before, a better design should be make tower properties the same among ALL tower types, and make only tower of the right type the right to use them. This means adding tower type requires less modification in tower manager, tower and dictionary