# bst_height_experiment.py
import random
import time
from typing import Any, Callable, List
import matplotlib.pyplot as plt # type: ignore

from bst import BinarySearchTree, BinTree, insert  # your implementation

# imp variables
TREES_PER_RUN = 10_000          
LOW_TARGET_SEC = 1.5               # lower bound for timing window
HIGH_TARGET_SEC = 2.5              # upper bound for timing window
SAMPLES = 50                       # number of N samples from 0..n_max

# helper functions

# Build a BST of size n using random floats in [0,1) with comparator a<b.
def random_tree(n: int) -> BinarySearchTree:
    cmp: Callable[[Any, Any], bool] = lambda a, b: a < b
    bst = BinarySearchTree(comes_before=cmp, tree=None)
    for _ in range(n):
        x = random.random()
        bst = insert(bst, x)
    return bst

# Height in *edges*. Empty tree has height -1; a single-node tree has height 0.
def tree_height_edges(bst: BinarySearchTree) -> int:

    def h_node(t : BinTree) -> int:
        # BinTree is Union[Node, None]; Node has .left/.right
        if t is None:
            return -1
        # match/case optional; direct recursion is simple here
        return 1 + max(h_node(t.left), h_node(t.right))
    return h_node(bst.tree)


# find the average height of a random_tree
def average_height_for_N(n: int, runs: int = TREES_PER_RUN) -> float:
    total = 0
    for _ in range(runs):
        bst = random_tree(n)
        total += tree_height_edges(bst)
    return total / runs if runs > 0 else -1.0

# Return seconds to build & measure `runs` random trees of size n.
def time_one_N(n: int, runs: int = TREES_PER_RUN) -> float:
    start = time.perf_counter()
    for _ in range(runs):
        _ = tree_height_edges(random_tree(n))
    return time.perf_counter() - start


def time_insert_into_random_tree(n: int, TREES_PER_RUN: int) -> float:
    """
    Build TREES_PER_RUN random trees of size n and insert one random value
    into each. Returns total time (in seconds).
    """
    start = time.perf_counter()
    for _ in range(TREES_PER_RUN):
        bst = random_tree(n)
        _ = insert(bst, random.random())  # measure one insert per tree
    return time.perf_counter() - start

def run_experiment():
    # 1) n_max
    
    n_max = 64
    
    # 2) sample N values (0..n_max) inclusive, 50 points
    if SAMPLES <= 1:
        Ns = [n_max]
    else:
        Ns = sorted(set(int(round(i * n_max / (SAMPLES - 1))) for i in range(SAMPLES)))

    # 3) compute average height at each N
    avg_heights: List[float] = []
    for n in Ns:
        avg_h = average_height_for_N(n, runs=TREES_PER_RUN)
        avg_heights.append(avg_h)
        print(f"N={n:6d}  avg_height={avg_h:.3f}")

    # 4) plot
    plt.figure()
    plt.title(f"Average Height of Random BSTs vs N\n(TREES_PER_RUN={TREES_PER_RUN})")
    plt.xlabel("N (number of nodes)")
    plt.ylabel("Average height (edges; empty=-1)")
    plt.plot(Ns, avg_heights, marker="o")  # do not specify colors per style guide
    plt.tight_layout()
    plt.show()

#measure and plot the avg time to insert a random value into a random bst of size n
def run_experiment_insert():
    
    # n_max
    n_max = 64

    # Evenly spaced N values from 0 to n_max
    Ns = [int(round(i * n_max / (SAMPLES - 1))) for i in range(SAMPLES)]
    avg_times : list[float]= []

    print("Measuring average insertion times...")
    for n in Ns:
        total_time = time_insert_into_random_tree(n, TREES_PER_RUN)
        avg_time = total_time / TREES_PER_RUN
        avg_times.append(avg_time)
        print(f"N={n:6d}  avg_insert_time={avg_time:.8f}s")

    # Plot results
    plt.figure()
    plt.title(f"Average Insert Time vs Tree Size/Number of Nodes N\n(TREES_PER_RUN={TREES_PER_RUN})")
    plt.xlabel("N (number of nodes/size of tree)")
    plt.ylabel("Average time per insert (seconds)")
    plt.plot(Ns, avg_times, marker="o")
    plt.tight_layout()
    plt.savefig("insert_time_vs_N2.png")  # writes a PNG next to your script
    plt.close()

if __name__ == "__main__":
    run_experiment_insert()
