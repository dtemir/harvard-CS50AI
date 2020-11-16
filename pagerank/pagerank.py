import os
import random
import re
import sys

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
    pagerank = {}

    for corpus_page in corpus:
        pagerank[corpus_page] = 0

    next_page = random.choice(list(corpus))

    for i in range(n - 1):
        model = transition_model(corpus, next_page, damping_factor)
        probabilities = []

        for k in model.keys():
            probabilities.append(model[k])

        next_page = random.choices(list(corpus), weights=probabilities, k=1).pop()

        if next_page in pagerank:
            pagerank[next_page] += 1
        else:
            pagerank[next_page] = 1

    for page in pagerank:
        pagerank[page] = pagerank[page] / n

    # sum = 0
    # for page in pagerank:
    #     sum += pagerank[page]
    #
    # print(sum)

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}

    for corpus_page in corpus:
        pagerank[corpus_page] = 1 / len(corpus)


if __name__ == "__main__":
    main()
