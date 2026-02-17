import unittest
import heapq
from typing import List

def determineMaxDataFlow_unordered(bandwidth: List[int], streamCount: int) -> int:
    n = len(bandwidth)
    if streamCount <= 0 or n == 0:
        return 0

    K = min(n, max(1, int(streamCount ** 0.5) * 4))
    top = sorted(bandwidth, reverse=True)[:K]

    heap = []
    for i in range(K):
        j = i
        heap.append((-(top[i] + top[j]), i, j))
    heapq.heapify(heap)

    total = 0
    while heap and streamCount > 0:
        neg_s, i, j = heapq.heappop(heap)
        total += -neg_s
        streamCount -= 1
        if j + 1 < K:
            nj = j + 1
            heapq.heappush(heap, (-(top[i] + top[nj]), i, nj))
    return total


class TestDetermineMaxDataFlow(unittest.TestCase):
    def test_case_1(self):
        bandwidth = [5, 4, 8, 4, 7]
        streamCount = 5
        expected = 86
        result = determineMaxDataFlow_unordered(bandwidth, streamCount)
        self.assertEqual(result, expected)

    def test_case_2(self):
        bandwidth = [14, 120, 8, 14]
        streamCount = 4
        expected = 626
        result = determineMaxDataFlow_unordered(bandwidth, streamCount)
        self.assertEqual(result, expected)

    def test_empty_bandwidth(self):
        self.assertEqual(determineMaxDataFlow_unordered([], 5), 0)

    def test_zero_streams(self):
        self.assertEqual(determineMaxDataFlow_unordered([10, 20, 30], 0), 0)

    def test_single_bandwidth(self):
        self.assertEqual(determineMaxDataFlow_unordered([10], 3), 60)

    def test_equal_bandwidths(self):
        self.assertEqual(determineMaxDataFlow_unordered([5, 5, 5, 5], 5), 100)


if __name__ == "__main__":
    unittest.main()