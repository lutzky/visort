visort
======

`visort` ("visual" sort) is a small command-line utility intended for a very
specific use-case.

Imagine `long_running_short_output` as a command which takes a long time to
run, and prints few lines of information at a time. Furthermore, you might want
to interrupt that program before it finishes running, if you have enough data.
In this case, you'd simply hit `Ctrl+C` when you have enough data. But what
happens if you want that data sorted?

    long_running_short_output | sort   # Won't display any output until
                                       # long_running_short_output is done :(

    long_running_short_output | visort # Will display sorted data as it comes in

I hope that you find this useful.
