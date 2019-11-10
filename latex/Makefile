ext = aux fdb_latexmk fls log out synctex.gz toc bbl blg lof lot

build_cmd = "pdflatex main.tex && bibtex main.aux && pdflatex main.tex && pdflatex main.tex"

all: build clean run

build:
	sudo docker run --rm -v $$(pwd):/root/tesi -w /root/tesi aergus/latex bash -c ${build_cmd}

run:
	xreader main.pdf &

clean:
	for f in ${ext}; do find . -name "*.$${f}" -delete; done

