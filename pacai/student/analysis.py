"""
Analysis question.
Change these default values to obtain the specified policies through value iteration.
If any question is not possible, return just the constant NOT_POSSIBLE:
```
return NOT_POSSIBLE
```
"""

NOT_POSSIBLE = None

def question2():
    """
    [Enter a description of what you did here.]
    Set the noise to 0 so that the agent has no risk in failing to cross the bridge.
    """

    answerDiscount = 0.9
    answerNoise = 0.0

    return answerDiscount, answerNoise

def question3a():
    """
    [Enter a description of what you did here.]
    Set noise to 0 for agent to have no risk of entering the cliff.
    Set living reward to -5 to discourage agent of continuing past the earlier goal.
    """

    answerDiscount = 0.9
    answerNoise = 0.0
    answerLivingReward = -5.0

    return answerDiscount, answerNoise, answerLivingReward

def question3b():
    """
    [Enter a description of what you did here.]
    Set discount to 0.5 for agent to not think too far ahead.
    Set noise to 0.4 to deincentivize agent from taking the bottom path.
    Set living reward to -1.0 to try to find a quick exit, but not low enough to brave the cliffs.
    """

    answerDiscount = 0.5
    answerNoise = 0.4
    answerLivingReward = -1.0

    return answerDiscount, answerNoise, answerLivingReward

def question3c():
    """
    [Enter a description of what you did here.]
    Set noise to 0 for agent to disregard the cliffs.
    Set living reward to 0 for agent to know that the best option is far terminal state.
    """

    answerDiscount = 0.9
    answerNoise = 0.0
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3d():
    """
    [Enter a description of what you did here.]
    Kept discount at 0.9 to keep agent thinking about the future.
    Set noise to 0.4 to deincentivize agent from taking the bottom path.
    Set living reward to 0 for agent to focus on finding best terminal state.
    """

    answerDiscount = 0.9
    answerNoise = 0.4
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3e():
    """
    [Enter a description of what you did here.]
    Kept discount at 0.9 to keep agent thinking about the future.
    Set noise to 0.0 so agent is taking no risk.
    Set living reward to 10.0 so smart agent knows staying alive is more rewarding than ending.
    """

    answerDiscount = 0.9
    answerNoise = 0.0
    answerLivingReward = 10.0

    return answerDiscount, answerNoise, answerLivingReward

def question6():
    """
    [Enter a description of what you did here.]
    The more episodes, the more the agent will be sure that the 1.0 is the best
    answer because it doesn't know that there is a 100.0 on the board, and landing
    on -100.0s discourages the agent from trying anything else. A learning rate will
    make this learned helplessness progress faster, and more episodes will solidify it.
    """

    return NOT_POSSIBLE

if __name__ == '__main__':
    questions = [
        question2,
        question3a,
        question3b,
        question3c,
        question3d,
        question3e,
        question6,
    ]

    print('Answers to analysis questions:')
    for question in questions:
        response = question()
        print('    Question %-10s:\t%s' % (question.__name__, str(response)))
