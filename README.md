bunch of tools for maths. I code the things i find interesting.
the code is not the best, or the fastest, as they're typically written jankily - just to get them done.
most are hooked up to matplotlib as the real goal is just the pretty pictures.
most are hooked up to other tools modules, and because of this most of the other modules change whenever a new one is added, so they get changed all the time

Note that vectors_tool, the largest file, for linear algebra, is often outdated and not tested thouroughly as i regularly change it on my machine without changing it here.
the same goes for most files, they are modified regularly depending on what it's used for but not often updated, or checked.

Most files are also incomplete, or almost completely non-functionoal (e.g. mappings tool), as they are just the skeleton of a file which will become much larger when (if)
there's time to add to them

the names of the files are hopefully self-explanatory, as well as the docstrings, but here's a list of what they do:

imaginary_numbers_and_logs and imaginary_tools are for complex number representation, and can do a bit of maths (e.g. multiplying or inverting).

list_tools was some terrible code i wrote when first getting to grips with python, that just does a lot of stuff with lists, it'll probably get deleted soon as it's absolutely terrible

matrix_tools grew out of list_tools, and is the subset relating to matrices, also terrible.

vector_tool was initially used for gram-schmidt orthogonalisation as i was doing that at the time, but then used vectors to deal with matrices, and yadda yadda.

mappings_tool is a backbone of a project i'm going to eventually do for abstract algebra.

phase_portrait and phase_portrait_with_trace plot the phase portrait of a 2x2 matrix, there's something bugging in the values though and i can't see it so it 
produces graphs, just the wrong ones.

plot_functions is just a little thing where you put in a 1d or 2d function and it plots it

plot_matrices rasters over vectors (x, y)^T and plots (x, y)^T M (x, y) for a matrix M using plot_functions. quite pretty really. requires another class in the vectors_tool i never update that hasn't been updated since it was added.

polynomial_tools is semi-functional, very incomplete, but allows you to represent polynomials, as well as equate them at values and find roots and derivatives, obviously needs an extra few lines of functionality...

stats_tools is another backbone project, but the "statistics" module already exists so unless i get round to it this'll only get used for normal and t distribution integrators.

wraps_toools was when i was learning decorators and figured i could make wraps to use to hook up all the other modules made in the future to matplotlib really easily.
