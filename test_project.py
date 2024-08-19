import pytest, sys, re
from project import main, cont, discontinue, checkWin, showBoard, announce, inputValidate


def test_main_invalid_one(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "game")
    #since sys.exit() is called on invalid input
    with pytest.raises(SystemExit): 
        main()

def test_main_invalid_two(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "player")
    #since sys.exit() is called on invalid input
    with pytest.raises(SystemExit): 
        main()

#FOR THE SAKE OF YOUR SANITY I RECOMMEND NOT EVEN LOOKING AT THIS ONE
def test_input_validate(monkeypatch):
    #counter attribute for the fake_pormpter function
    #Using it in this weird index way because getting UnboundLocalError
    count = [0]

    #Scenarios to test and their expected results (which i know)
    scenarios = ["1 1", "2 3", "3 2", "f f", "4 4", "1 x", "tacos apples", "1 2 3 4 5"]
    results = [[0, 0], [1, 2], [2, 1], "f", False, False, False, False]

    #The replacement for prompter for testing purposes
    def fake_prompter(prompt, mark):
        #Use the counter variable to return the correct scenario
        result = scenarios[count[0]]
        count[0] += 1
        return result

    #Monkeypatch TO disable the original prompter function
    monkeypatch.setattr("project.prompter", fake_prompter)

    #Something to match the patterns, by Mahad
    def pattern_match(inp):
        pattern = r"^(?P<column>[1-3]|f) (?P<row>[1-3]|f)$"
        if (matches:=re.search(pattern, inp)):
            col = matches.group("column")
            row = matches.group("row")
            try:
                col, row = int(col)-1, int(row)-1
                return [col, row]
            except:
                if col == "f" and row == "f":
                    return "f"
            
        else:
            return False
    #Assertion
    for x in range(len(scenarios)):
        result = pattern_match(scenarios[x])
        if result == results[x]:
            assert inputValidate("x") == results[x]
        else:
            sys.exit("You messed up")
#FOR THE SAKE OF YOUR SANITY I RECOMMEND NOT EVEN LOOKING AT THIS ONE