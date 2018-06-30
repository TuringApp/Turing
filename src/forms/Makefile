DESTDIR =
UI_SOURCES = $(shell ls *.ui)
UI_TARGETS = $(patsubst %.ui, %.py, $(UI_SOURCES))

all: $(UI_TARGETS)

clean:
	rm -f *~ ui_*.py

install:

%.py: %.ui
	pyuic5 $< -o $@

.PHONY: all clean install
