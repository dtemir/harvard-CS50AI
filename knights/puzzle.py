from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
knowledge0 = And(
    # A is either a knight or a knave
    Or(AKnave, AKnight),
    Not(And(AKnave, AKnight)),

    # A says "I am both a knight and a knave."
    Biconditional(AKnight, And(AKnight, AKnave))
)


# Puzzle 1
knowledge1 = And(
    # A and B are either knights or knaves
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
    Not(And(AKnave, AKnight)),
    Not(And(BKnave, BKnight)),

    # A says "We are both knaves." (Must be Knave)
    # B says nothing. (Must be Knight)
    Biconditional(AKnight, And(AKnave, BKnave)),
)

# Puzzle 2
knowledge2 = And(
    # A and B are either knights or knaves
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
    Not(And(AKnave, AKnight)),
    Not(And(BKnave, BKnight)),

    # A says "We are the same kind."
    # B says "We are of different kinds."
    Biconditional(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))),
    Biconditional(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave))),
)

# Puzzle 3
knowledge3 = And(
    # A, B, C are either knights or knaves
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
    Or(CKnave, CKnight),
    Not(And(AKnave, AKnight)),
    Not(And(BKnave, BKnight)),
    Not(And(CKnave, CKnight)),

    # A says either "I am a knight." or "I am a knave.", but you don't know which.
    # B says "A said 'I am a knave'."
    # B says "C is a knave."
    # C says "A is a knight."
    Biconditional(Or(AKnight, AKnave), Or(AKnight, AKnave)),
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),
    Biconditional(BKnight, CKnave),
    Biconditional(CKnight, AKnight)
)


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
