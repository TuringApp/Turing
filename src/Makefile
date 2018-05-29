DESTDIR =

all:
	pylupdate5 project-linux.pro
	make -C lang $@ DESTDIR=$(DESTDIR)
	make -C forms $@ DESTDIR=$(DESTDIR)

clean:
	rm -f *~
	make -C lang $@ DESTDIR=$(DESTDIR)
	make -C forms $@ DESTDIR=$(DESTDIR)

install:
	make -C lang $@ DESTDIR=$(DESTDIR)
	make -C forms $@ DESTDIR=$(DESTDIR)

.PHONY: all clean install
