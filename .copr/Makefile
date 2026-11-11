# LH4051-DE RPM packaging helpers
# Requires: rpm-build, rpmdevtools (spectool), make, curl
# For COPR submission: copr-cli and COPR_PROJECT=owner/project

SHELL := /bin/bash
SPEC := ../lh4051-de.spec
RPM_TOPDIR ?= $(HOME)/rpmbuild
SRPM_DIR := $(RPM_TOPDIR)/SRPMS
COPR_PROJECT ?=

.PHONY: all help version sources srpm copr clean

all: srpm

help:
	@printf '%s\n' \
	  'make version   - print the latest stable upstream release' \
	  'make sources   - download the spec source archive' \
	  'make srpm      - build a source RPM for the latest stable release' \
	  'make copr      - build the SRPM and submit it to COPR' \
	  'make clean     - remove this build tree'

version:
	@curl -fsSL https://api.github.com/repos/kuznix-code/LH4051-DE/releases/latest | \
	  sed -nE 's/.*"tag_name":[[:space:]]*"v?([^"]+)".*/\1/p' | head -n1

sources:
	@command -v spectool >/dev/null || { echo "ERROR: install rpmdevtools (spectool)" >&2; exit 1; }
	mkdir -p "$(RPM_TOPDIR)/SOURCES" "$(RPM_TOPDIR)/SPECS"
	spectool -g -R --define "_topdir $(RPM_TOPDIR)" "$(SPEC)"

srpm: sources
	rpmbuild -bs --define "_topdir $(RPM_TOPDIR)" "$(SPEC)"
	@echo "SRPM output: $(SRPM_DIR)"

copr: srpm
	@test -n "$(COPR_PROJECT)" || { echo "ERROR: set COPR_PROJECT=owner/project" >&2; exit 1; }
	@command -v copr-cli >/dev/null || { echo "ERROR: install copr-cli" >&2; exit 1; }
	@srpm="$$(find "$(SRPM_DIR)" -maxdepth 1 -type f -name 'LH4051-DE-*.src.rpm' -printf '%T@ %p\n' | sort -nr | head -n1 | cut -d' ' -f2-)"; \
	  test -n "$$srpm" || { echo "ERROR: no LH4051-DE source RPM found" >&2; exit 1; }; \
	  echo "Submitting $$srpm to COPR project $(COPR_PROJECT)"; \
	  copr-cli build "$(COPR_PROJECT)" "$$srpm"

clean:
	rm -rf "$(RPM_TOPDIR)"
