import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    probability = 1
    zero_gene = people.keys() - (one_gene | two_genes) # Set of people with no genes

    for person in zero_gene:
        # Getting no genes means that we need to find the probability that each parent will not contribute gene

        if people[person]["mother"] is None:
            probability *= PROBS["gene"][0]
        elif people[person]["mother"] is not None:
            mother = people[person]["mother"]
            father = people[person]["father"]

            if mother in zero_gene and father in zero_gene:
                # p that person doesn't get gene from mother is 0.99
                # p that person doesn't get gene from father is 0.99 too
                probability *= (1 - PROBS["mutation"]) ** 2
            if mother in zero_gene and father in one_gene:
                # p that person doesn't get gene from mother is 0.99
                # p that person doesn't get gene from father is 0.50
                probability *= (1 - PROBS["mutation"]) * 0.5
            if mother in zero_gene and father in two_genes:
                # p that person doesn't get gene from mother is 0.99
                # p that person doesn't get gene from father is 0.01
                probability *= (1 - PROBS["mutation"]) * PROBS["mutation"]

            if mother in one_gene and father in zero_gene:
                # p that person doesn't get gene from mother is 0.5
                # p that person doesn't get gene from father is 0.99
                probability *= 0.5 * (1 - PROBS["mutation"])
            if mother in one_gene and father in one_gene:
                # p that person doesn't get gene from mother is 0.5
                # p that person doesn't get gene from father is 0.5 too
                probability *= 0.5 ** 2
            if mother in one_gene and father in two_genes:
                # p that person doesn't get gene from mother is 0.5
                # p that person doesn't get gene from father is 0.01
                probability *= 0.5 * PROBS["mutation"]

            if mother in two_genes and father in zero_gene:
                # p that person doesn't get gene from mother is 0.01
                # p that person doesnt' get gene from father is 0.99
                probability *= PROBS["mutation"] * (1 - PROBS["mutation"])
            if mother in two_genes and father in one_gene:
                # p that person doesn't get gene from mother is 0.01
                # p that person doesn't get gene from father is 0.5
                probability *= PROBS["mutation"] * 0.5
            if mother in two_genes and father in two_genes:
                # p that person doesn't get gene from mother is 0.01
                # p that person doesn't get gene from father is 0.01
                probability *= PROBS["mutation"] ** 2

        # Multiply by the probability that the person has trait with zero genes
        probability *= PROBS["trait"][0][person in have_trait]

    for person in one_gene:
        # Getting one gene means that person should inherit gene only from one of his parents
        # which means that we need to multiply the probability that it is father who gives the gene or mother, while
        # the second parent doesn't plus the opposite situation
        # (mother gives gene * father doesn't give gene) + (mother doesn't give gene * father gives gene)

        if people[person]["mother"] is None:
            probability *= PROBS["gene"][1]
        elif people[person]["mother"] is not None:
            mother = people[person]["mother"]
            father = people[person]["father"]

            # One of parents has zero genes
            if mother in zero_gene and father in zero_gene:
                # p that person gets gene from mother or father is 0.01
                # p that person doesn't get gene from mother or father is 0.99
                probability *= PROBS["mutation"] * (1 - PROBS["mutation"]) + PROBS["mutation"] * (1 - PROBS["mutation"])
            if mother in zero_gene and father in one_gene:
                # p that person gets gene from mother is 0.01
                # p that person doesn't get gene from father 0.5
                # p that person gets gene from father 0.5
                # p that person doesn't get gene from mother is 0.99
                probability *= PROBS["mutation"] * 0.5 + (1 - PROBS["mutation"]) * 0.5
            if mother in zero_gene and father in two_genes:
                # p that person gets gene from mother is 0.01
                # p that person doesn't get gene from father is 0.01
                # p that person gets gene from father is 0.99
                # p that person doesn't get gene from mother is 0.99
                probability *= PROBS["mutation"] ** 2 + (1 - PROBS["mutation"]) ** 2

            # One of parents has one gene
            if mother in one_gene and father in zero_gene:
                # p that person gets gene from mother is 0.5
                # p that person doesn't get gene from father is 0.99
                # p that person gets gene from father is 0.01
                # p that person doesn't get gene from mother is 0.5
                probability *= (1 - PROBS["mutation"]) * 0.5 + PROBS["mutation"] * 0.5
            if mother in one_gene and father in one_gene:
                # p that person gets gene from mother/father is 0.5
                # p that person doesn't get gene from father/mother is 0.5
                probability *= 0.5 ** 2 + 0.5 ** 2
            if mother in one_gene and father in two_genes:
                # p that person gets gene from mother is 0.5
                # p that person doesn't get gene from father is 0.01
                # p that person gets gene from father is 0.99
                # p that person doesn't get gene from mother is 0.5
                probability *= 0.5 * PROBS["mutation"] + (1 - PROBS["mutation"]) * 0.5

            # One of parents has two genes
            if mother in two_genes and father in zero_gene:
                # p that person gets gene from mother is 0.99
                # p that person doesn't get gene from father is 0.99
                # p that person gets gene from father is 0.01
                # p that person doesn't get gene from mother is 0.01
                probability *= (1 - PROBS["mutation"]) ** 2 + PROBS["mutation"] ** 2
            if mother in two_genes and father in one_gene:
                # p that person gets gene from mother is 0.99
                # p that person doesn't get gene from father is 0.5
                # p that person gets gene from father is 0.5
                # p that person doesn't get gene from mother is 0.01
                probability *= (1 - PROBS["mutation"]) * 0.5 + PROBS["mutation"] * 0.5
            if mother in two_genes and father in two_genes:
                # p that person gets gene from mother is 0.99
                # p that person doesn't get gene from father is 0.01
                # p that person gets gene from father is 0.99
                # p that person doesn't get gene from mother is 0.01
                probability *= (1 - PROBS["mutation"]) * PROBS["mutation"] + (1 - PROBS["mutation"]) * PROBS["mutation"]

        # Multiply by the probability that the person has trait with one gene
        probability *= PROBS["trait"][1][person in have_trait]

    for person in two_genes:
        # Getting two genes means person should inherit genes from both of the parents
        # which is why we need to find the probability each parent can contribute gene

        if people[person]["mother"] is None:
            probability *= PROBS["gene"][2]
        elif people[person]["mother"] is not None:
            mother = people[person]["mother"]
            father = people[person]["father"]

            if mother in zero_gene and father in zero_gene:
                # p that person gets gene from mother is 0.01
                # p that person gets gene from father is 0.01
                probability *= PROBS["mutation"] * PROBS["mutation"]
            if mother in zero_gene and father in one_gene:
                # p that person gets gene from mother is 0.01
                # p that person gets gene from father is 0.5
                probability *= PROBS["mutation"] * 0.5
            if mother in zero_gene and father in two_genes:
                # p that person gets gene from mother is 0.01
                # p that person gets gene from father is 0.99
                probability *= PROBS["mutation"] * (1 - PROBS["mutation"])

            if mother in one_gene and father in zero_gene:
                # p that person gets gene from mother is 0.5
                # p that person gets gene from father is 0.01
                probability *= 0.5 * PROBS["mutation"]
            if mother in one_gene and father in one_gene:
                # p that person gets gene from mother is 0.5
                # p that person gets gene from father is 0.5
                probability *= 0.5 * 0.5
            if mother in one_gene and father in two_genes:
                # p that person gets gene from mother is 0.5
                # p that person gets gene from father is 0.99
                probability *= 0.5 * (1 - PROBS["mutation"])
            if mother in two_genes and father in zero_gene:
                # p that person gets gene from mother is 0.99
                # p that person gets gene from father is 0.01
                probability *= (1 - PROBS["mutation"]) * PROBS["mutation"]
            if mother in two_genes and father in one_gene:
                # p that person gets gene from mother is 0.99
                # p that person gets gene from father is 0.5
                probability *= (1 - PROBS["mutation"]) * 0.5
            if mother in two_genes and father in two_genes:
                # p that person gets gene from mother is 0.99
                # p that person gets gene from father is 0.99
                probability *= (1 - PROBS["mutation"]) ** 2

        # Multiply by the probability that the person has trait with two genes
        probability *= PROBS["trait"][2][person in have_trait]

    return probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:

        # if person has one gene, add the joint probability p to them and so on
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p

        # if person has or hasn't trait, add the joint probability
        probabilities[person]["trait"][person in have_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:

        # sum all values from the gene set
        genes = sum(probabilities[person]["gene"].values())

        # there are only three options, 0, 1, or 2 genes
        for i in range(0, 3):
            probabilities[person]["gene"][i] /= genes

        traits = sum(probabilities[person]["trait"].values())

        # there are only two options, 0 or 1 (False of True)
        for i in range(0, 2):
            probabilities[person]["trait"][i] /= traits


if __name__ == "__main__":
    main()
