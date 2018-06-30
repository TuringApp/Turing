DESTDIR =

LANG_SRC = $(shell ls *.ts)
LANG_TARGET = $(patsubst %.ts, %.qm, $(LANG_SRC))

all: $(LANG_TARGET)

%.qm: %.ts
	lrelease $<

clean:
	rm -f *~ *.qm

install:

.PHONY: all clean install
