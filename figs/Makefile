.PHONY: all

pdfs := $(patsubst %.eps,%.pdf,$(wildcard *.eps))

all: $(pdfs)

%.pdf: %.eps
	epstopdf "$<"

clean:
	rm -f *.pdf
