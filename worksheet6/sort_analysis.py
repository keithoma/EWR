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

class LaTexBuilder:
    def __init__(self, _list):
        self.text_ = ""
        self.list_ = _list
        self.fg_colors_ = ['' for item in _list]
        self.bg_colors_ = ['' for item in _list]

    def set_foreground(self, index, color):
        self.fg_colors_[index] = color

    def set_background(self, index, color):
        self.bg_colors_[index] = color

    def swap_background(self, old, new):
        for i in range(0, len(self.list_)):
            if self.bg_colors_[i] == old:
                self.bg_colors_[i] = new

    def begin(self):
        self._append("\\section{Auto Generated}\n")
        self._append("\\begin{tabular}{")
        for i in range(0, len(self.list_)):
            self._append("| c ")
        self._append("|| l |}\n")
        self._append("    \\hline\n")

    def log(self, _msg):
        self._append("    ")
        for i in range(0, len(self.list_)):
            if i != 0:
                self._append(" & ")
            if self.bg_colors_[i] != '':
                self._append("\\cellcolor{{{}}}".format(self.bg_colors_[i]))
            if self.fg_colors_[i] != '':
                self._append("\\color{{{}}}".format(self.fg_colors_[i]))
            self._append("{}".format(self.list_[i]))
        self._append(" & {}".format(_msg))
        self._append("\\\\ \\hline \n")

    def end(self):
        self._append("\\end{tabular}\n")

    def _append(self, _text):
        self.text_ += _text

    def __str__(self):
        return self.text_;

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
    def __init__(self, _list):
        self.list_ = _list
        self.stats_ = StatsBuilder()
        self.logger_ = LaTexBuilder(_list)

    def log(self, _depth, _message):
        #print("{length:>2}: {text:>{length}}".format(length=_depth * 2, text=_message))
        return True

    def partition(self, _partition, _low, _high):
        """
        Arguments:
            _partition (list):
            _low (int): the index for the lower end
            _high (int): the index for the upper end

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
            self.stats_.compare()
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
            self.stats_.swap()

            self.logger_.set_foreground(_i, 'red')
            self.logger_.set_foreground(_j, 'red')
            self.logger_.log("swap {} with {}".format(_partition[_i], _partition[_j]))
            self.logger_.set_foreground(_i, '')
            self.logger_.set_foreground(_j, '')

            _partition[_i], _partition[_j] = _partition[_j], _partition[_i]
            return _i

        def choose_pivot():
            """
                Chooses a pivot element within the given partition.
            """
            pivot = _partition[_high]

            self.logger_.swap_background('LightCyan', '')
            self.logger_.set_background(_high, 'LightCyan')
            self.logger_.log("choose the pivot")

            return pivot

        # end of nested functions

        i = _low - 1
        pivot = choose_pivot()

        for j in range(_low, _high):
            self.stats_.iterate()
            if is_less(_partition[j], pivot):
                i = inc_i_and_swap_at(i, j)

        i = inc_i_and_swap_at(i, _high)
        self.logger_.set_background(i, 'LightGreen')
        return i

    def sort_range(self, _partition, _low, _high):
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
        self.stats_.enter()

        if _low < _high:
            old = self.logger_.bg_colors_.copy()
            self.logger_.swap_background('Amber', '')
            for i in range(_low, _high + 1):
                self.logger_.set_background(i, 'Amber')

            pivot_index = self.partition(_partition, _low, _high)
            if pivot_index > 0:
                self.sort_range(_partition, _low, pivot_index - 1)
            self.sort_range(_partition, pivot_index + 1, _high)

            # restore Amber
            # for i in range(0, len(old)):
            #     if old[i] == 'Amber':
            #         self.logger_.set_background(i, old[i])
        self.stats_.leave()

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
        quicksort = QuickSort(_list)
        quicksort.run()

    def run(self):
        self.logger_.begin()

        list_length = len(self.list_)

        # if the list_length is exactly 0 or 1, there is no need to sort
        if list_length != 0 and list_length != 1:
            self.sort_range(self.list_, 0, list_length - 1)

        self.logger_.log("final state")
        self.logger_.end()

        with open('quicksort.tex', 'wt') as f:
            f.write(self.logger_.__str__())

        return self.stats_

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
        print("  sorted: {}".format(reduce((lambda a, w: "{} {}".format(a, w)), words)))

    #words = read_words_from_file('test.txt')
    #words = ["F", "A", "C", "B"]
    words = [7, 1, 5, 4, 9, 2, 8, 3, 0, 6]
    print("input list: {}".format(reduce((lambda a, w: "{} {}".format(a, w)), words)))

    test_algo("quicksort", QuickSort.sort, words[:])
    test_algo("heapsort", HeapSort.sort, words[:])

if __name__ == "__main__":
    _private_test()
