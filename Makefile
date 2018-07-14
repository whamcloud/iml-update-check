NAME          := iml-update-check
MODULE_SUBDIR := .

include include/common.mk
include include/git-versioning.mk
include include/rpm.mk

all: rpms

version:
	echo 'VERSION = "$(VERSION)"' > scm_version.py
	echo 'PACKAGE_VERSION = "$(PACKAGE_VERSION)"' >> scm_version.py
	echo 'BUILD = "$(BUILD_NUMBER)"' >> scm_version.py
	echo 'IS_RELEASE = $(IS_RELEASE)' >> scm_version.py

dist/$(NAME)-$(PACKAGE_VERSION).tar.gz: Makefile *.js *.py
	mkdir -p dist/
	git archive --prefix $(NAME)-$(PACKAGE_VERSION)/ -o $@ HEAD

$(NAME)-$(PACKAGE_VERSION).tar.gz: dist/$(NAME)-$(PACKAGE_VERSION).tar.gz
	cp $< $@
