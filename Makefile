DESTDIR =

all:
	make -C src $@ DESTDIR=$(DESTDIR)

clean:
	rm -f *~
	make -C src $@ DESTDIR=$(DESTDIR)

install:
	make -C src $@ DESTDIR=$(DESTDIR)
	find $(DESTDIR) -name .gitignore | xargs rm -f

.PHONY: all clean install
