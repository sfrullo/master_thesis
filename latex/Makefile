ext = aux fdb_latexmk fls log out synctex.gz toc bbl blg lof lot

all: build clean run

build:
	sudo docker run --rm -v $$(pwd):/root/tesi -w /root/tesi aergus/latex pdflatex main.tex
	sudo docker run --rm -v $$(pwd):/root/tesi -w /root/tesi aergus/latex bibtex main.aux
	sudo docker run --rm -v $$(pwd):/root/tesi -w /root/tesi aergus/latex pdflatex main.tex
	sudo docker run --rm -v $$(pwd):/root/tesi -w /root/tesi aergus/latex pdflatex main.tex

run:
	xreader main.pdf &

clean:
	for f in ${ext}; do find . -name "*.$${f}" -delete; done

