import os
import random
import re
import sys
from copy import deepcopy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Store probability of each link
    prob_distribution = {}
    # Pages to which given page has links
    potential_pages = corpus[page]

    # If page has no outgoing links, return a probability distribution that chooses randomly between all pages
    if len(potential_pages) == 0:
        prob = 1 / len(corpus)
        for corpus_page in corpus:
            prob_distribution[corpus_page] = prob

        return prob_distribution

    # Damping probability (the probability that surfer visits a link)
    damping_prob = damping_factor / len(potential_pages)
    # Random damping probability (the probability that surfer visits a link regardless whether given page has access
    # to it)
    damping_prob_random = (1 - damping_factor) / len(corpus)

    # Fill out probability distribution with damping probability
    for potential_page in potential_pages:
        prob_distribution[potential_page] = damping_prob

    # Fill out probability distribution with random damping probability
    for corpus_page in corpus:
        if corpus_page in potential_pages:
            prob_distribution[corpus_page] += damping_prob_random
        else:
            prob_distribution[corpus_page] = damping_prob_random

    return prob_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Dictionary to store pagerank
    pagerank = {}

    # Choosing page at random
    next_page = random.choice(list(corpus))

    # Iterating over the given number of samples
    for i in range(n - 1):
        # Each time create a next transition model with probabilities of pages
        model = transition_model(corpus, next_page, damping_factor)

        # Choose a page at random considering probabilities given by transition model
        next_page = random.choices(list(model), weights=model.values(), k=1).pop()

        # Fill out pagerank with the number of times surfer lands on particular page
        if next_page in pagerank:
            pagerank[next_page] += 1
        else:
            pagerank[next_page] = 1

    # Divide the number of times surfer landed at one page by the sample size
    for page in pagerank:
        pagerank[page] = pagerank[page] / n

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Dictionary to store pagerank
    pagerank = {}

    # Iterate over all pages and assign initial probability to pagerank
    for page in corpus:
        pagerank[page] = 1 / len(corpus)

    # Keep boolean to know when the results start converging (difference no greater than 0.001)
    converged = False
    while not converged:
        # Copy pagerank
        pagerank_copy = {k: v for k, v in pagerank.items()}
        # Keep difference to find out whether results converge and we can stop
        pagerank_diff = {}

        # Iterate over each page in corpus
        for page in corpus.keys():
            # Keep count of current pagerank
            probability = 0

            # Summation: PR(i) / NumLinks(i)
            for page_i, pages in corpus.items():
                # Check if current page has a link to our page p
                if page in pages:
                    # Use previous pagerank for summation
                    probability += pagerank_copy[page_i] / len(pages)
                # In case current page has no links to other pages
                elif len(pages) == 0:
                    # Interpret as having one link for every page
                    probability += 1 / len(corpus)

            # Calculate the rest of the formula given in task background for iterative algorithm
            pagerank[page] = (1 - damping_factor) / len(corpus) + (damping_factor * probability)

            # Store the difference between previous pagerank and current to know when to stop
            pagerank_diff[page] = abs(pagerank_copy[page] - pagerank[page])
            # print(pagerank_diff)

        # Check if we can leave the while loop by making sure if there is no gap of more than 0.001 between
        # current pagerank and previous pagerank
        converged = True
        for page in pagerank_diff:
            if pagerank_diff[page] > 0.001:
                converged = False

    # Important: normalize.
    # Pageranks must sum up to 1. In case with corpus2, they do not sum up and thus need to be normalized
    # by dividing each pagerank with their overall sum
    sum_pagerank = 0
    for k in pagerank:
        sum_pagerank += pagerank[k]

    for k in pagerank:
        pagerank[k] = pagerank[k] / sum_pagerank

    return pagerank


if __name__ == "__main__":
    main()
