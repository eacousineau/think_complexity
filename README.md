# Think Complexity

This is a fork of Dr. Downey's [original SVN repository](http://code.google.com/p/complexity/) for his book, [Think Complexity](http://www.greenteapress.com/compmod/).

In fact, this first started out with modifications to the [source available from the website](http://www.greenteapress.com/compmod/complexity.tex.zip), so that is why there is history starting from two separate points.

## Differences

The primary difference is that the `hevea.sty` file is directly added, `figs/Makefile` has been added to convert `*.eps` figures to `*.pdf` (with the additional root-level make target `pdf_figures`), and a few minor adjustments to the book has been made.

## Compilation

First, convert the figures to `*.pdf` if using `pdflatex`:

	cd figs && make

For compiling the document, for me [TeXstudio](http://texstudio.sourceforge.net/) works out of the box.
