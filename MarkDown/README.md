
# WHat is included:
1. Settings to run the game
2. How to run the game
3. Structure of the game
4. Testing
5. Exception handling
6. Author notes

# 1. Settings to run the game
- Python 3.14+



# 2. How to run the game

# 3. Structure of the game
1. This project uses tkinter, which is a BUILT IN module of python, to create windows and handle visual implementation.
2. 

# 4. Testing
Steps to run the tests
1. Install dependencies
python3 -m pip install --break-system-packages pytest pytest-cov
2. Run the test suite
-> Navigate to project root -> cd Plant-and-Bees -> python3 -m pytest
3. To get a coverage report (a new one)
-> python3 -m pytest --cov=Base --cov=Manager --cov=States --cov=Head --cov-report=term-missing --cov-report=markdown:MarkDown/coverage.md

# 5. Exception handling

## 5.1 Built in exceptions

## 5.2. Custom exceptions

# 6. Author notes
- If you looked into the previous commits, the initial name of the project is plant-and-bees, this is inspired by my friend who is also doing an oop project that has actual characters and world building in them.
- But i changed the project to simply tower defense, which is rather basic, this is mainly because i faced many difficulties while trying to implement the game core functions and had to keep modifying its structures. 
- Due to the difficulties of the project that i put myself on, i decided to strip the project of its world building so that i can focus on the technical side of it. If i had more time, i would have gotten into world building and make the towers and enemies more balanced, interesting. Initially i also made more than 3 tower types and intended to implement buff for enemies, but i supposed that would be scope creep for what the purpose of this project.
