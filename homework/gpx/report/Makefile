all:
	platex    -kanji=utf8 report 
	pbibtex   -kanji=utf8 report 
	platex    -kanji=utf8 report
	platex    -kanji=utf8 report
	dvipdfmx  -p a4 report 
clean:
	/bin/rm -f *~ *.log *.dvi *.blg *.aux *.out *.bbl *.lot *.toc *.lof *.pdf


