# COPR custom source method for LH4051-DE.
# COPR invokes: make -f .copr/Makefile srpm outdir=... spec=...
# Local use: make -f .copr/Makefile all

SHELL := /bin/bash

outdir ?= $(CURDIR)/srpms
spec ?= $(CURDIR)/../lh4051-de.spec
topdir := $(abspath $(outdir))/rpmbuild
sourcedir := $(topdir)/SOURCES

.PHONY: all srpm

all: srpm

srpm:
	@test -f "$(spec)" || { echo "ERROR: spec file not found: $(spec)" >&2; exit 1; }
	@command -v rpmspec >/dev/null || { echo "ERROR: rpmspec is required (provided by rpm-build)" >&2; exit 1; }
	@command -v rpmbuild >/dev/null || { echo "ERROR: rpmbuild is required (provided by rpm-build)" >&2; exit 1; }
	@mkdir -p "$(outdir)" "$(sourcedir)" "$(topdir)/BUILD" "$(topdir)/BUILDROOT" "$(topdir)/RPMS" "$(topdir)/SPECS"
	@version="$$(rpmspec -q --srpm --qf '%{VERSION}\n' "$(spec)" | head -n1)"; \
	  test -n "$$version" || { echo "ERROR: could not determine spec version" >&2; exit 1; }; \
	  archive="v$$version.tar.gz"; \
	  url="https://github.com/kuznix-code/LH4051-DE/archive/refs/tags/$$archive"; \
	  echo "Downloading LH4051-DE $$version source archive"; \
	  curl --fail --location --silent --show-error "$$url" -o "$(sourcedir)/$$archive"; \
	  echo "Building SRPM into $(outdir)"; \
	  rpmbuild -bs --define "_topdir $(topdir)" --define "_sourcedir $(sourcedir)" --define "_srcrpmdir $(abspath $(outdir))" "$(spec)"
