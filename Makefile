SHELL := /bin/bash
DISTNAME := kiehinen-0.3.2
DISTFILES := `hg status -cma -n`

distribution: distdir
	$(shell for f in $(DISTFILES); do cp $$f $(DISTNAME)/$$f; done)
	tar cjvf $(DISTNAME).tar.bz2 $(DISTNAME)/
	rm -rf $(DISTNAME)

distdir:
	mkdir -p $(DISTNAME)/icons

clean:
	rm $(DISTNAME).tar.bz2 *.pyc
