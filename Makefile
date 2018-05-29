DESTDIR =

all:
	make -C src $@ DESTDIR=$(DESTDIR)

clean:
	rm -f *~
	make -C src $@ DESTDIR=$(DESTDIR)

install:
	make -C src $@ DESTDIR=$(DESTDIR)

.PHONY: all clean install
