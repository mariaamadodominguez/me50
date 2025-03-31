from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# (1) information about the structure of the problem itself
ProblemInfo = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)))

# Puzzle 0
# A says "I am both a knight and a knave."

# (2) information about what the characters actually said.
ASays = And(AKnight, AKnave)

knowledge0 = And(
    ProblemInfo,
    Implication(AKnight, ASays),
    Implication(AKnave, Not(ASays))    
)

# print(f"    {knowledge0}")

# Puzzle 1
# A says "We are both knaves."
# B says nothing.

# (2) information about what the characters actually said.
ASays = And(AKnave, BKnave)

knowledge1 = And(
    ProblemInfo,
    Implication(AKnight, ASays),
    Implication(AKnave, Not(ASays))
)

# print(f"    {knowledge1}")

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."

# (2) information about what the characters actually said.
ASays = Or(And(AKnight, BKnight), And(AKnave, BKnave))
BSays = Or(And(AKnight, BKnave), And(AKnave, BKnight))    

knowledge2 = And(
    ProblemInfo,
    Implication(AKnight, ASays),
    Implication(AKnave, Not(ASays)),
    Implication(BKnight, BSays),
    Implication(BKnave, Not(BSays)))    

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

# (2) information about what the characters actually said.
ASays = And(Or(AKnight, AKnave))
BSaysA = And(AKnave)
BSaysC = And(CKnave)
CSays = And(AKnight)
knowledge3 = And(ProblemInfo,
                 Implication(AKnight, ASays),
                 Implication(AKnave, Not(ASays)),
                 Implication(BKnight, Implication(AKnight, BSaysA)),
                 Implication(BKnight, Implication(AKnave, Not(BSaysA))),
                 Implication(BKnave, Implication(AKnight, Not(BSaysA))),
                 Implication(BKnave, Implication(AKnave, BSaysA)),
                 Implication(BKnight, BSaysC),
                 Implication(BKnave, Not(BSaysC)),
                 Implication(CKnight, CSays),
                 Implication(CKnave, Not(CSays)))
 

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
