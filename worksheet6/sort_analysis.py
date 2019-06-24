#! /usr/bin/env python3

"""
    This file is part of the "EWR" project.
      (c) 2019 Christian Parpart <christian@parpart.family>
      (c) 2019 Kei Thoma <thomakei@gmail.com>

    Licensed under the MIT License (the "License"); you may not use this
    file except in compliance with the License. You may obtain a copy of
    the License at: http://opensource.org/licenses/MIT

    It implements QuickSort and Heapsort algorithms along with some statistical data retrieval
    and requested methods by the Lecture we both attend(ed) to.
"""

import sys
import time
import argparse

class _LaTeXBuilder:
    """
        Internal helper API for constructing LaTeX tables for visualizing list modification,
        as usually done by sorting algorithms.
    """

    # color coding constants (TODO: future improvements: make them configurable)
    SWAP_FG = "red"
    CORRECT_BG = "LightGreen"
    ACTIVE_BG = "Amber"
    PIVOT_BG = "LightCyan"
    CLEAR = ""

    def __init__(self, _list):
        """ Constructs the LaTeX builder with the list (_list) to be worked on. """
        self.text_ = ""
        self.list_ = _list
        self.fg_colors_ = ["" for item in _list]
        self.bg_colors_ = ["" for item in _list]
        self.delimiter_ = False

        self._append("\\section{Auto Generated}\n")
        self._append("\\begin{tabular}{")
        self._append("| c " * len(self.list_))
        self._append("|| l |}\n")

    @staticmethod
    def format_list(_list):
        """ Static helper method for generating a text representation of lists. """
        return "\\(({}\\))".format(", ".join(map(str, _list)))

    class Context:
        """ Helper class for scoped color setting via with-statement. """
        def __init__(self, _builder, _index, _foreground, _background):
            """
                Constructs color setter.
                Parameters:
                    _builder (_LaTeXBuilder): LaTeX builder to operate on.
                    _index (int): list index to set color at.
                    _foreground (str): background color to set or None
                    _background (str): foreground color to set or None
            """
            self.builder_ = _builder
            self.index_ = _index
            self.foreground_ = _foreground
            self.background_ = _background

            if _foreground != None:
                self.old_foreground_ = _builder.fg_colors_[_index]
            else:
                self.old_foreground_ = None

            if _background != None:
                self.old_background_ = _builder.bg_colors_[_index]
            else:
                self.old_background_ = None

        def __enter__(self):
            """ Internal magic-method to be invoked upon with-statement scope entrance,
                setting colors. """
            if self.foreground_ != None:
                self.builder_.set_foreground(self.index_, self.foreground_)

            if self.background_:
                self.builder_.set_background(self.index_, self.background_)

        def __exit__(self, _type, _value, _traceback):
            """ Internal magic-method to be invoked upon with-statement scope exit,
                reverting set colors. """
            if self.old_foreground_ != None:
                self.builder_.fg_colors_[self.index_] = self.old_foreground_

            if self.old_background_ != None:
                self.builder_.bg_colors_[self.index_] = self.old_background_

    def foreground(self, _index, _color):
        """
            Constructs scoped foreground color. Use with with-statement.
            Parameters:
                _index (int): list index to set color at
                _color (str): foreground color to set
            Returns:
                (Context): The context object being used internally by the with-statement.
        """
        return _LaTeXBuilder.Context(self, _index, _color, None)

    def background(self, _index, _color):
        """
            Constructs scoped background color. Use with with-statement.
            Parameters:
                _index (int): list index to set color at
                _color (str): background color to set
            Returns:
                (Context): The context object being used internally by the with-statement.
        """
        return _LaTeXBuilder.Context(self, _index, None, _color)

    def set_foreground(self, _index, _color):
        """
            Sets the foreground color of the list value at given index.
            Parameters:
                _index (int): list index to set color at
                _color (str): foreground color to set
            Returns:
                (None): None
        """
        self.fg_colors_[_index] = _color

    def set_background(self, _index, _color):
        """
            Sets the background color of the list value at the given index.
            Parameters:
                _index (int): list index to set color at
                _color (str): background color to set
            Returns:
                (None): None
        """
        self.bg_colors_[_index] = _color

    def swap_background(self, _old, _new):
        """
            Swaps the background colors of each list item to _new that matches _old.
            Parameters:
                _old (str): old color to swap from
                _new (str): new color to swap to
            Returns:
                (None): None
        """
        for i in range(0, len(self.list_)):
            if self.bg_colors_[i] == _old:
                self.bg_colors_[i] = _new

    def log_action(self, _msg):
        """
            Logs a list action by adding a new line to the generated LaTeX table
            showing the list and the given message _msg at its right hand side.
            Parameters:
                _msg (str): the message to be printed as action along-side the list in a row
            Returns:
                (None): None
        """
        self._append("    ")
        if not self.delimiter_:
            self._append("\\hline ")
        else:
            self.delimiter_ = False

        for i in range(0, len(self.list_)):
            if i != 0:
                self._append(" & ")
            if self.bg_colors_[i] != "":
                self._append("\\cellcolor{{{}}}".format(self.bg_colors_[i]))
            if self.fg_colors_[i] != "":
                self._append("\\color{{{}}}".format(self.fg_colors_[i]))
            self._append("{}".format(self.list_[i]))
        self._append(" & {}".format(_msg))
        self._append("\\\\\n")

    def log_line(self, _msg):
        """
            Logs given message _msg to the generated LaTeX table as a new
            full row at the end.
            Parameters:
                _msg (str): the message to be printed in its dedicated single row
            Returns:
                (None): None
        """
        self._append("\\hhline{{{}}}\n".format("=" * (len(self.list_) + 1)))
        self._append("\\multicolumn{{{}}}{{ | c | }}{{{}}}\\\\".format(len(self.list_) + 1, _msg))
        self._append("\\hhline{{{}}}\n".format("=" * (len(self.list_) + 1)))
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
            Parameters:
                _filename (str): Filename to the local filesystems file to store the generated LaTeX
                                 fragment to.
        """
        with open(_filename, "wt") as f:
            f.write(self.text_)

    def _append(self, _text):
        """
            Internal helper function for conviniently appending text to the internal buffer.
            Parameters:
                _text (str): The bare text to append to the internal LaTeX buffer.
            Returns:
                (None): None
        """
        self.text_ += _text

class _StatsBuilder:
    """
        Internal helper API for constructing statistical metrics of (sorting) algorithms.
    """

    def __init__(self):
        """
            Constructs the _StatsBuilder with all values set to 0 and
            start_time_ set to current time.
        """
        self.compares_ = 0
        self.swaps_ = 0
        self.calls_ = 0
        self.iterations_ = 0
        self.recursion_depth_ = 0
        self.current_recursion_depth_ = 0
        self.start_time_ = time.time()

    def compare(self):
        """ Increments compare-count by one. """
        self.compares_ += 1

    def swap(self):
        """ Increments swap-count by one. """
        self.swaps_ += 1

    def call(self):
        """ Increments call-count by one. """
        self.calls_ += 1

    def iterate(self):
        """ Increments iteration-count by one. """
        self.iterations_ += 1

    def enter(self):
        """
            Increments current recursion depth by one and updates maximum reached recursion depth
            to current recursion depth if exceeded.
        """
        self.current_recursion_depth_ += 1
        if self.current_recursion_depth_ > self.recursion_depth_:
            self.recursion_depth_ = self.current_recursion_depth_

    def leave(self):
        """
            Decrements current recursion depth by one.
        """
        self.current_recursion_depth_ -= 1

    def elapsed(self):
        """
            Returns the duration in milliseconds this _StatsBuilder object exists since construction.
        """
        return time.time() - self.start_time_

    def __str__(self):
        """
            Returns a JSON-style string representation of the collected metrics.
        """
        fmt = "{{compares: {}, swaps: {}, calls: {}, iterations: {}, recursion: {}, elapsed: {}}}"
        return fmt.format(self.compares_, self.swaps_, self.calls_, self.iterations_,
                          self.recursion_depth_, self.elapsed())

def heapsort(_list):
    """
        Implements heapsort algorithm on given list.
        Parameters:
            _list (list): The list to be sorted (in-place).
            _n (int): Number of elements in the list to operate on.
            _i (int): Middle element.
            _stats (_StatsBuilder): Statistics builder
            _logger (_LaTeXBuilder): LaTeX builder instance.
        Returns:
            (_StatsBuilder): Execution statistics.
    """
    def heapify(_list, _n, _i, _stats, _logger):
        """ TODO: docstring """
        _stats.enter()

        # determine largest element index
        largest_element_index = _i
        LEFT_CHILD_INDEX = 2 * _i + 1
        if LEFT_CHILD_INDEX < _n:
            _stats.compare()
            if _list[LEFT_CHILD_INDEX] > _list[largest_element_index]:
                largest_element_index = LEFT_CHILD_INDEX

        RIGHT_CHILD_INDEX = 2 * _i + 2
        if RIGHT_CHILD_INDEX < _n:
            _stats.compare()
            if _list[RIGHT_CHILD_INDEX] > _list[largest_element_index]:
                largest_element_index = RIGHT_CHILD_INDEX

        # if the largest element isn't at index _i, swap!
        if largest_element_index != _i:
            _stats.swap()
            _list[_i], _list[largest_element_index] = _list[largest_element_index], _list[_i]

            with _logger.foreground(largest_element_index, _LaTeXBuilder.SWAP_FG):
                with _logger.foreground(_i, _LaTeXBuilder.SWAP_FG):
                    _logger.log_action("swap {} with {}".format(_list[largest_element_index], _list[_i]))

            heapify(_list, _n, largest_element_index, _stats, _logger)

        _stats.leave()

    stats = _StatsBuilder()
    logger = _LaTeXBuilder(_list)
    logger.log_action("initial state")

    # short-circuit trivial inputs
    if len(_list) > 1:
        # build heap by rearranging array
        i = len(_list) // 2 - 1
        logger.log_line("build heap with middle element {}".format(_list[i]))
        with logger.background(i, _LaTeXBuilder.ACTIVE_BG):
            while i >= 0:
                stats.iterate()
                heapify(_list, len(_list), i, stats, logger)
                i = i - 1

        # one-by-one, extract an element from the heap
        logger.log_line("extract elements from heap")
        i = len(_list) - 1
        while i >= 0:
            stats.iterate()

            # move current root to the end
            stats.swap()
            _list[0], _list[i] = _list[i], _list[0]

            with logger.foreground(0, _LaTeXBuilder.SWAP_FG):
                with logger.foreground(i, _LaTeXBuilder.SWAP_FG):
                    logger.log_action("swap {} with {}".format(_list[0], _list[i]))
            logger.set_background(i, _LaTeXBuilder.CORRECT_BG)

            # call max heapify on the reduced heap
            logger.log_line("rebuild heap between {} and {}".format(0, i))
            heapify(_list, i, 0, stats, logger)

            i = i - 1

    logger.finish()
    return stats, logger

class QuickSort:
    """
        Implements quicksort algorithm. This is a class instead of a function due to helper methods
        being more well and clean when not all nested, due to shared variable use.
    """

    def __init__(self, _list):
        self.list_ = _list
        self.stats_ = _StatsBuilder()
        self.logger_ = _LaTeXBuilder(_list)

    def partition(self, _partition, _low, _high):
        """
        Arguments:
            _partition (list):
            _low (int): the index for the lower end
            _high (int): the index for the upper end

        Returns:
            (int): new pivot index
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
        return quicksort.run()

    def run(self):
        """ TODO: docstring """
        list_length = len(self.list_)

        # if the list_length is exactly 0 or 1, there is no need to sort
        if list_length != 0 and list_length != 1:
            self.sort_range(self.list_, 0, list_length - 1)

        self.logger_.log_action("final state")
        self.logger_.finish()

        return self.stats_, self.logger_

# as per home-assignment
def sort_A(_list):
    """ TODO: docstring """
    stats, _ = QuickSort.sort(_list)
    return (stats.compares_ + stats.swaps_, stats.elapsed())

# as per home-assignment
def sort_B(_list):
    """ TODO: docstring """
    stats, _ = heapsort(_list)
    return (stats.compares_ + stats.swaps_, stats.elapsed())

# as per home-assignment, except that the naming wasn't mentioned, so we chose one.
def read_words_from_file(_filename):
    """ TODO: docstring """
    with open(_filename, mode="r", encoding="utf-8") as f:
        return f.read().split()

def main(argv):
    """
        main function actually implementing command line interface
        Parameters:
            argv (list): reflecting sys.argv, list of strings
    """

    def test_algo(_name, _sort, _list, _latex_tracefile):
        """ tiny helper for generic testing sort algos. """
        stats, _latex = _sort(_list)
        print("{}: {}".format(_name, stats))
        print("  sorted: {}".format(", ".join(map(str, _list))))
        if _latex_tracefile:
            _latex.save(_latex_tracefile)

    def parse_args():
        """
            tiny helper function for setting up CLI parser and parsing argv."
        """
        arg_parser = argparse.ArgumentParser(prog="sort_analyzer.py",
                                             description="Sorting algorithm analysis.")
        arg_parser.add_argument("--quicksort", action="store_true", help="Uses quicksort algorithm.")
        arg_parser.add_argument("--heapsort", action="store_true", help="Uses heapsort algorithm.")
        arg_parser.add_argument("--word-file", help="Specifies file to load words from.")
        arg_parser.add_argument("--latex-trace",
                                help=("Specifies file name to write LaTeX fragment to that contains"
                                      " a log table of all instructions being done (as readable as"
                                      " possible)."))
        args = arg_parser.parse_args(argv)
        if (args.heapsort and args.quicksort) or (not args.heapsort and not args.quicksort):
            print("You must specify at exactly one algorithm, --quicksort or --heapsort.")
            sys.exit(1)
        return args

    args = parse_args()

    if args.word_file:
        print("Loading word set from file: {}".format(args.word_file))
        words = read_words_from_file(args.word_file)
        print("    words: {}".format(words))
    else:
        words = [6, 5, 3, 1, 8, 7, 2, 4]
        print("Defaulting to demo word set: {}".format(words))

    if args.heapsort:
        test_algo("heapsort", heapsort, words[:], args.latex_trace)

    if args.quicksort:
        test_algo("quicksort", QuickSort.sort, words[:], args.latex_trace)

if __name__ == "__main__":
    main(sys.argv[1:])
