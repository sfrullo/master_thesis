.PHONY: all build_summary build_thesis build clean run

ext = aux fdb_latexmk fls log out synctex.gz toc bbl blg lof lot

build_cmd_thesis = "pdflatex main.tex && bibtex main.aux && pdflatex main.tex && pdflatex main.tex"
build_cmd_summary = "pdflatex summary.tex && bibtex summary.aux && pdflatex summary.tex && pdflatex summary.tex"

all: build clean run

build_thesis:
	sudo docker run --rm -v $$(pwd):/root/tesi -w /root/tesi aergus/latex bash -c ${build_cmd_thesis}

build_summary:
	sudo docker run --rm -v $$(pwd):/root/tesi -w /root/tesi aergus/latex bash -c ${build_cmd_summary}

build: build_summary build_thesis

run:
	xreader main.pdf summary.pdf &

clean:
	for f in ${ext}; do find . -name "*.$${f}" -delete; done

