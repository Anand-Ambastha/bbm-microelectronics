# Build all three LaTeX documents:   make      |   remove build files:   make clean
DOCS = PBL_Review CBS_Experiment Case_Study

all: $(DOCS:%=%.pdf)

%.pdf: %.tex common.sty student_info.tex
	latexmk -pdf -interaction=nonstopmode -halt-on-error $<

clean:
	latexmk -c $(DOCS:%=%.tex)
	rm -f *.synctex.gz

distclean:
	latexmk -C $(DOCS:%=%.tex)

.PHONY: all clean distclean
