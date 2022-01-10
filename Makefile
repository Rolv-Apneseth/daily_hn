PREFIX ?= /usr/local

all:
	@echo Run \'make install\' to install daily-hn.

install:
	@mkdir -p $(DESTDIR)$(PREFIX)/bin
	@cp -p daily-hn.py $(DESTDIR)$(PREFIX)/bin/daily-hn
	@chmod 755 $(DESTDIR)$(PREFIX)/bin/daily-hn

uninstall:
	@rm -rf $(DESTDIR)$(PREFIX)/bin/daily-hn