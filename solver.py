import time
import argparse
from collections import deque


class Sanalouhos:
    """
    Solve a word puzzle game called "Sanalouhos".
    """

    def __init__(
        self,
        letters: list,
        vocabulary: set,
        ncol: int,
        nrow: int,
    ):
        self.vocabulary = vocabulary
        self.letters = letters
        self.ncol = ncol
        self.nrow = nrow
        self.grid = self.create_grid(letters, ncol, nrow)
        self.space = set((i, j) for i in range(nrow) for j in range(ncol))

    @staticmethod
    def create_grid(letters: list, ncol: int, nrow: int):
        assert len(letters) == ncol * nrow, "Invalid number of letters."
        grid = []
        for i in range(nrow):
            grid.append(letters[i * ncol : (i + 1) * ncol])
        return grid

    def _in_grid(self, x: int, y: int) -> bool:
        return 0 <= x < self.nrow and 0 <= y < self.ncol

    def _next(self, x: int, y: int):
        dir = [
            (x + 1, y + 1),
            (x + 1, y - 1),
            (x - 1, y + 1),
            (x - 1, y - 1),
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]
        values = [((i, j), (self.grid[i][j])) for (i, j) in dir if self._in_grid(i, j)]
        return values

    def _find_words(self, min_len=3):
        ans = {}

        def dfs(x: int, y: int, curr: str, wordsleft: set, path: list):
            if (x, y) in visited:
                return

            visited.append((x, y))

            remaining = {i for i in wordsleft if i.startswith(curr)}

            # No matching words left -> go back one letter
            if not remaining:
                visited.pop()
                return

            # Save current word and add new letter
            if curr in remaining and len(curr) >= min_len:
                ans[curr] = path

            neighbours = self._next(x, y)
            for coords, letter in neighbours:
                dfs(*coords, curr + letter, remaining, path + [coords])
            visited.pop()

        visited = deque()
        for x in range(self.nrow):
            for y in range(self.ncol):
                path = [(x, y)]
                dfs(x, y, self.grid[x][y], self.vocabulary, path)

        return ans

    # Knuth's Algorithm X implemented by Ali Assaf.
    # Source: https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html
    def algorithm_x(self, X, Y, solution=[]):
        if not X:
            yield list(solution)
        else:
            c = min(X, key=lambda c: len(X[c]))
            for r in list(X[c]):
                solution.append(r)
                cols = self._select(X, Y, r)
                for s in self.algorithm_x(X, Y, solution):
                    yield s
                self._deselect(X, Y, r, cols)
                solution.pop()

    def _select(self, X, Y, r):
        cols = []
        for j in Y[r]:
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].remove(i)
            cols.append(X.pop(j))
        return cols

    def _deselect(self, X, Y, r, cols):
        for j in reversed(Y[r]):
            X[j] = cols.pop()
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].add(i)

    def _format_X(self, X, Y):
        X = {j: set() for j in X}
        for i in Y:
            for j in Y[i]:
                X[j].add(i)
        return X

    def solve(self):
        X = self.space
        Y = self._find_words()
        X = self._format_X(X, Y)
        return self.algorithm_x(X, Y)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--letters", type=str, required=True)
    parser.add_argument("--ncol", type=int, required=False, default=5)
    parser.add_argument("--nrow", type=int, required=False, default=6)

    args = parser.parse_args()
    letters = list(args.letters)
    ncol = args.ncol
    nrow = args.nrow

    with open("kotus2024.txt", "r") as f:
        vocabulary = set(f.read().splitlines())

    start_time = time.perf_counter()
    sanalouhos = Sanalouhos(letters, vocabulary, ncol, nrow)
    for i in sanalouhos.solve():
        print(*i)

    print(f"Elapsed time: {time.perf_counter() - start_time:.2f} seconds.")
