// This file is part of the "quicksort" project, http://github.com/christianparpart/quicksort>
//   (c) 2019 Christian Parpart <christian@parpart.family>
//
// Licensed under the MIT License (the "License"); you may not use this
// file except in compliance with the License. You may obtain a copy of
// the License at: http://opensource.org/licenses/MIT

#include "heapsort.h"
#include "quicksort.h"

#include <cassert>
#include <cstdlib>
#include <ctime>
#include <functional>
#include <iomanip>
#include <iostream>
#include <iterator>
#include <random>
#include <sstream>
#include <string>
#include <string_view>
#include <type_traits>
#include <vector>
#include <utility>

using namespace std;

using Vector = vector<long>;
using Sort = function<void(Vector&)>;

void fail(string_view const& msg)
{
    clog << msg << '\n';
    abort();
}

void assertEquals(Vector const& a, Vector const& b)
{
    if (a.size() != b.size())
        fail("Array sizes don't match.");

    for (size_t i = 0; i < a.size(); ++i)
        if (a[i] != b[i])
            fail("Arrays don't match");
}

static auto const quicksort = make_pair("quicksort", sorting::quicksort::sort<Vector>);
static auto const heapsort = make_pair("heapsort", sorting::heapsort::sort<Vector>);

void test_sort(pair<string_view, Sort> const& sorter)
{
    cout << "Running " << sorter.first << ":\n";

    // empty
    auto const a0 = Vector{};
    auto a0_ = a0;
    sorter.second(a0_);
    assertEquals(a0_, a0);

    // single element
    auto const a1 = Vector{7};
    auto a1_ = a1;
    sorter.second(a1_);
    assertEquals(a1_, a1);

    // three elements
    auto const a3 = Vector{1, 2, 0, 0};
    auto a3_ = a3;
    sorter.second(a3_);
    assertEquals(a3_, Vector{0, 0, 1, 2});

    // already sorted
    auto const aSorted = Vector{0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    auto aSorted_ = aSorted;
    sorter.second(aSorted_);
    assertEquals(aSorted_, aSorted);
}

int main(int argc, char const** argv)
{
    string_view const action = argc == 2 ? argv[1] : "all";
    cerr << "action: " << action << '\n';

    if (action == "all")
    {
        test_sort(quicksort);
        test_sort(heapsort);
    }
    else if (action == "quicksort")
        test_sort(quicksort);
    else if (action == "heapsort")
		test_sort(heapsort);
    else
    {
        cerr << "Invalid action: '" << action << "'\n";
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
