#! /usr/bin/env python3
# This file is part of the "quicksort" project, http://github.com/christianparpart/quicksort>
#   (c) 2019 Christian Parpart <christian@parpart.family>
#   (c) 2019 Kei Thoma <thomakei@gmail.com>
#
# Licensed under the MIT License (the "License"); you may not use this
# file except in compliance with the License. You may obtain a copy of
# the License at: http://opensource.org/licenses/MIT

import time
from functools import reduce

class StatsBuilder:
    def __init__(self):
        self.compares_ = 0
        self.swaps_ = 0
        self.calls_ = 0
        self.iterations_ = 0
        self.recursion_depth_ = 0
        self.current_recursion_depth_ = 0
        self.start_time_ = time.time()

    def compare(self):
        self.compares_ = self.compares_ + 1

    def swap(self):
        self.swaps_ = self.swaps_ + 1

    def call(self):
        self.calls_ = self.calls_ + 1

    def iterate(self):
        self.iterations_ = self.iterations_ + 1

    def enter(self):
        self.current_recursion_depth_ = self.current_recursion_depth_ + 1
        if self.current_recursion_depth_ > self.recursion_depth_:
            self.recursion_depth_ = self.current_recursion_depth_

    def leave(self):
        self.current_recursion_depth_ = self.current_recursion_depth_ - 1

    def elapsed(self):
        return time.time() - self.start_time_

    def __str__(self):
        fmt = "{{compares: {}, swaps: {}, calls: {}, iterations: {}, recursion: {}, elapsed: {}}}"
        return fmt.format(self.compares_, self.swaps_, self.calls_, self.iterations_,
                          self.recursion_depth_, self.elapsed())

class HeapSort:
    @staticmethod
    def heapify(a, n, i, stats):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        stats.enter()

        if l < n:
            stats.compare()
            if a[l] > a[largest]:
                largest = l

        if r < n:
            stats.compare()
            if a[r] > a[largest]:
                largest = r

        if largest != i:
            stats.swap()
            a[i], a[largest] = a[largest], a[i]
            HeapSort.heapify(a, n, largest, stats)

        stats.leave()

    @staticmethod
    def sort(a):
        stats = StatsBuilder()
        n = len(a)

        # short-circuit trivial inputs
        if n < 2:
            return stats

        # build heap by rearranging array
        i = n // 2 - 1
        while i >= 0:
            stats.iterate()
            HeapSort.heapify(a, n, i, stats)
            i = i - 1

        # one-by-one, extract an element from the heap
        i = n - 1
        while i >= 0:
            stats.iterate()

            # move current root to the end
            stats.swap()
            a[0], a[i] = a[i], a[0]

            # call max heapify on the reduced heap
            HeapSort.heapify(a, i, 0, stats)

            i = i - 1

        return stats

class QuickSort:
    @staticmethod
    def partition(_partition, _low, _high, _stats):
        """
        Arguments:
            _partition (list):
            _low (int): the index for the lower end
            _high (int): the index for the upper end
            _stats (StatsBuilder):

        Returns:
            (int):
        """

        # nested functions
        def is_less(_a, _b):
            """
            This is an auxilary function which compares the two arguments 'a' and 'b'. If 'a' is strictly
            smaller than 'b' she returns True and False otherwise. Also, the 'compare()' function from the
            StatsBuilder class is called which adds 1 to the 'compares_' attribute (this is the reason why
            this function is not redundant).

            Arguments:
                _a (int): the left side integer to be compared with '<'
                _b (int): the right side integer to be compared with '<'
            
            Returns:
                (bool): True if 'a' is strictly smaller than 'b' and False otherwise
            """
            _stats.compare()
            return _a < _b

        def inc_i_and_swap_at(_i, _j):
            """
            Another auxilary function which increments the argument 'i' and swaps p[i] and p[j]. As with
            the function above, she calls the 'swap()' function from StatsBuilder class which adds 1 to the
            'swaps_' attribute. Finally, the incremented 'i' is returned.

            Arguments:
                _i (int): the first index to be swapped in p
                _j (int): the second index to be swapped in p

            Returns:
                (int): the incremented i; so ++i is returned
            """
            _i = _i + 1
            _stats.swap()
            _partition[_i], _partition[_j] = _partition[_j], _partition[_i]
            return _i
        # end of nested functions

        i = _low - 1
        pivot = _partition[_high]

        for j in range(_low, _high):
            _stats.iterate()
            if is_less(_partition[j], pivot):
                i = inc_i_and_swap_at(i, j)

        return inc_i_and_swap_at(i, _high)

    @staticmethod
    def sort_range(_partition, _low, _high, _stats):
        """
        This static method sorts the given list 'p' recursivly.

        Arguments:
            p (list): the list to be sorted
            low (int): the starting index of the list to be sorted
            high (int): the last index of the list to be sorted
            stats (StatsBuilder):

        Returns:
            None
        """
        _stats.enter()

        if _low < _high:
            pivot_index = QuickSort.partition(_partition, _low, _high, _stats)
            if pivot_index > 0:
                QuickSort.sort_range(_partition, _low, pivot_index - 1, _stats)
            QuickSort.sort_range(_partition, pivot_index + 1, _high, _stats)

        _stats.leave()

    @staticmethod
    def sort(_list):
        """
        The heart of the quicksort algorithm. 

        Arguments:
            _list (list): the list to be sorted, each element must implement the comparison operator for <
            (__lt__)

        Returns:
            (StatsBuilder):
        """
        stats = StatsBuilder()
        list_length = len(_list)

        # if the list_length is exactly 0 or 1, there is no need to sort
        if list_length != 0 and list_length != 1:
            QuickSort.sort_range(_list, 0, list_length - 1, stats)
        return stats






# as per home-assignment
def sort_A(a):
    stats = QuickSort.sort(a)
    return (stats.compares_ + stats.swaps_, stats.elapsed())

# as per home-assignment
def sort_B(a):
    stats = HeapSort.sort(a)
    return (stats.compares_ + stats.swaps_, stats.elapsed())

def read_words_from_file(filename):
    with open(filename, mode='r', encoding='utf-8') as f:
        return f.read().split()

def _private_test():
    def test_algo(name, sort, words):
        stats = sort(words)
        print("{}: {}".format(name, stats))
        print("  sorted: {}".format(reduce((lambda a, w: a + ' ' + w), words)))

    words = ["F", "A", "C", "B"] # read_words_from_file("test.txt")
    print("input list: {}".format(reduce((lambda a, w: a + ' ' + w), words)))

    test_algo("quicksort", QuickSort.sort, words[:])
    test_algo("heapsort", HeapSort.sort, words[:])

if __name__ == "__main__":
    _private_test()
