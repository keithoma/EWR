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

class _LaTeXBuilder:
    """
        Helper class for constructing LaTeX tables for visualizing list modification,
        as usually done by sorting algorithms.
    """

    # color coding constants
    SWAP_FG = 'red'
    CORRECT_BG = 'LightGreen'
    ACTIVE_BG = 'Amber'
    PIVOT_BG = 'LightCyan'
    CLEAR = ''

    def __init__(self, _list):
        """ Constructs the LaTeX builder with the list (_list) to be worked on. """
        self.text_ = ""
        self.list_ = _list
        self.fg_colors_ = ['' for item in _list]
        self.bg_colors_ = ['' for item in _list]
        self.delimiter_ = False

        self._append("\\section{Auto Generated}\n")
        self._append("\\begin{tabular}{")
        for i in range(0, len(self.list_)):
            self._append("| c ")
        self._append("|| l |}\n")

    @staticmethod
    def format_list(_list):
        """ Static helper method for generating a text representation of lists. """
        s = "\(("
        for i in range(0, len(_list)):
            if i != 0:
                s += ", "
            s += "{}".format(_list[i])
        s += "\))"
        return s

    def set_foreground(self, _index, _color):
        """
            Sets the foreground color of the list value at given index.
        """
        self.fg_colors_[_index] = _color

    def set_background(self, _index, _color):
        """
            Sets the background color of the list value at the given index.
        """
        self.bg_colors_[_index] = _color

    def swap_background(self, old, new):
        """
            Swaps the background colors of each list item to _new that matches _old.
        """
        for i in range(0, len(self.list_)):
            if self.bg_colors_[i] == old:
                self.bg_colors_[i] = new

    def log_action(self, _msg):
        """
            Logs a list action by adding a new line to the generated LaTeX table
            showing the list and the given message _msg at its right hand side.
        """
        self._append("    ")
        if not self.delimiter_:
            self._append("\\hline ")
        else:
            self.delimiter_ = False

        for i in range(0, len(self.list_)):
            if i != 0:
                self._append(" & ")
            if self.bg_colors_[i] != '':
                self._append("\\cellcolor{{{}}}".format(self.bg_colors_[i]))
            if self.fg_colors_[i] != '':
                self._append("\\color{{{}}}".format(self.fg_colors_[i]))
            self._append("{}".format(self.list_[i]))
        self._append(" & {}".format(_msg))
        self._append("\\\\\n")

    def log_line(self, _msg):
        """
            Logs given message _msg to the generated LaTeX table as a new
            full row at the end.
        """
        self._append("\\hhline{{{}}}\n".format('=' * (len(self.list_) + 1)))
        self._append("\\multicolumn{{{}}}{{ | c | }}{{{}}}\\\\".format(len(self.list_) + 1, _msg))
        self._append("\\hhline{{{}}}\n".format('=' * (len(self.list_) + 1)))
        self.delimiter_ = True

    def finish(self):
        """
            Finalizes the generated LaTeX table by appending the table trailer to it.
        """
        if not self.delimiter_:
            self._append("    \\hline\n")
        self._append("\\end{tabular}\n")

    def save(self, _filename):
        """
            Saves the generated LaTeX output to given filename, _filename.
        """
        with open(_filename, 'wt') as f:
            f.write(self.text_)

    def _append(self, _text):
        """
            Internal helper function for conviniently appending text to the internal buffer.
        """
        self.text_ += _text

class _StatsBuilder:
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
    def heapify(a, n, i, stats, logger):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        #logger.log_line("Heapify with i = {}, n = {}".format(i, n))
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

            logger.set_foreground(largest, _LaTeXBuilder.SWAP_FG)
            logger.set_foreground(i, _LaTeXBuilder.SWAP_FG)
            logger.log_action("swap {} with {}".format(a[largest], a[i]))
            logger.set_foreground(largest, _LaTeXBuilder.CLEAR)
            logger.set_foreground(i, _LaTeXBuilder.CLEAR)

            HeapSort.heapify(a, n, largest, stats, logger)

        stats.leave()

    @staticmethod
    def sort(a):
        stats = _StatsBuilder()
        n = len(a)

        # short-circuit trivial inputs
        if n < 2:
            return stats

        logger = _LaTeXBuilder(a)
        logger.log_action("initial state")

        # build heap by rearranging array
        i = n // 2 - 1
        logger.log_line("build heap between {} and {}".format(0, i))
        while i >= 0:
            stats.iterate()
            HeapSort.heapify(a, n, i, stats, logger)
            i = i - 1

        # one-by-one, extract an element from the heap
        logger.log_line("extract elements from heap")
        i = n - 1
        while i >= 0:
            stats.iterate()

            # move current root to the end
            stats.swap()
            a[0], a[i] = a[i], a[0]

            logger.set_foreground(0, _LaTeXBuilder.SWAP_FG)
            logger.set_foreground(i, _LaTeXBuilder.SWAP_FG)
            logger.log_action("swap {} with {}".format(a[0], a[i]))
            logger.set_foreground(0, _LaTeXBuilder.CLEAR)
            logger.set_foreground(i, _LaTeXBuilder.CLEAR)
            logger.set_background(i, _LaTeXBuilder.CORRECT_BG)

            # call max heapify on the reduced heap
            logger.log_line("rebuild heap between {} and {}".format(0, i))
            HeapSort.heapify(a, i, 0, stats, logger)

            i = i - 1

        logger.finish()
        logger.save('heapsort.tex')

        return stats

class QuickSort:
    def __init__(self, _list):
        self.list_ = _list
        self.stats_ = _StatsBuilder()
        self.logger_ = _LaTeXBuilder(_list)

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
            _StatsBuilder class is called which adds 1 to the 'compares_' attribute (this is the reason why
            this function is not redundant).

            Arguments:
                _a (int): the left side integer to be compared with '<'
                _b (int): the right side integer to be compared with '<'
            
            Returns:
                (bool): True if 'a' is strictly smaller than 'b' and False otherwise
            """
            self.stats_.compare()
            # self.logger_.log_action("is {} less than {}?".format(_a, _b))
            return _a < _b

        def inc_i_and_swap_at(_i, _j):
            """
            Another auxilary function which increments the argument 'i' and swaps p[i] and p[j]. As with
            the function above, she calls the 'swap()' function from _StatsBuilder class which adds 1 to the
            'swaps_' attribute. Finally, the incremented 'i' is returned.

            Arguments:
                _i (int): the first index to be swapped in p
                _j (int): the second index to be swapped in p

            Returns:
                (int): the incremented i; so ++i is returned
            """
            _i = _i + 1
            self.stats_.swap()

            _partition[_i], _partition[_j] = _partition[_j], _partition[_i]

            self.logger_.set_foreground(_i, _LaTeXBuilder.SWAP_FG)
            self.logger_.set_foreground(_j, _LaTeXBuilder.SWAP_FG)
            self.logger_.log_action("swap {} with {}".format(_partition[_i], _partition[_j]))
            self.logger_.set_foreground(_i, _LaTeXBuilder.CLEAR)
            self.logger_.set_foreground(_j, _LaTeXBuilder.CLEAR)

            return _i

        def choose_pivot():
            """
                Chooses a pivot element within the given partition.
            """
            pivot_index = _high
            pivot = _partition[pivot_index]

            oldBgColors = self.logger_.bg_colors_.copy()

            self.logger_.swap_background(_LaTeXBuilder.PIVOT_BG, _LaTeXBuilder.CLEAR)
            self.logger_.set_background(_high, _LaTeXBuilder.PIVOT_BG)

            for j in range(_low, pivot_index):
                self.logger_.set_background(j, _LaTeXBuilder.ACTIVE_BG)

            self.logger_.log_action("choose the pivot {}".format(pivot))

            for j in range(_low, pivot_index):
                self.logger_.set_background(j, oldBgColors[j])

            return pivot

        # end of nested functions

        i = _low - 1
        pivot = choose_pivot()

        for j in range(_low, _high):
            self.stats_.iterate()
            if is_less(_partition[j], pivot):
                i = inc_i_and_swap_at(i, j)

        i = inc_i_and_swap_at(i, _high)
        self.logger_.set_background(i, _LaTeXBuilder.CORRECT_BG)
        return i

    def sort_range(self, _partition, _low, _high):
        """
        This static method sorts the given list 'p' recursivly.

        Arguments:
            p (list): the list to be sorted
            low (int): the starting index of the list to be sorted
            high (int): the last index of the list to be sorted
            stats (_StatsBuilder):

        Returns:
            None
        """
        self.stats_.enter()

        if _low < _high:
            pivot_index = self.partition(_partition, _low, _high)

            if pivot_index > 0:
                a = _LaTeXBuilder.format_list(_partition[_low:pivot_index])
                b = _LaTeXBuilder.format_list(_partition[pivot_index + 1: _high + 1])
                self.logger_.log_line("Partition the sequence into {} and {}".format(a, b))

                self.sort_range(_partition, _low, pivot_index - 1)

            self.sort_range(_partition, pivot_index + 1, _high)

        self.stats_.leave()

    @staticmethod
    def sort(_list):
        """
        The heart of the quicksort algorithm. 

        Arguments:
            _list (list): the list to be sorted, each element must implement the comparison operator for <
            (__lt__)

        Returns:
            (_StatsBuilder):
        """
        quicksort = QuickSort(_list)
        quicksort.run()

    def run(self):
        list_length = len(self.list_)

        # if the list_length is exactly 0 or 1, there is no need to sort
        if list_length != 0 and list_length != 1:
            self.sort_range(self.list_, 0, list_length - 1)

        self.logger_.log_action("final state")
        self.logger_.finish()
        self.logger_.save('quicksort.tex')

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
    #words = [7, 1, 5, 4, 9, 2, 8, 3, 0, 6]
    #words = [0, 1, 2, 3, 4]
    #words = [4, 3, 2, 1, 0]
    #words = [4, 10, 3, 5, 1] #geeksforgeeks
    words = [6, 5, 3, 1, 8, 7, 2, 4] #wikipedia
    print("input list: {}".format(reduce((lambda a, w: "{} {}".format(a, w)), words)))

    test_algo("quicksort", QuickSort.sort, words[:])
    test_algo("heapsort", HeapSort.sort, words[:])

if __name__ == "__main__":
    _private_test()
