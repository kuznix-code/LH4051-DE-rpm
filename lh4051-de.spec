# Dynamic latest-stable RPM spec for LH4051-DE.
# Optional subpackages (disabled by default): build with --with updater and/or
# --with bootstrap. These are intended mainly for Linux From Scratch and other
# systems without a package manager; updater is also useful on Windows/macOS.
%bcond_with updater
%bcond_with bootstrap
# The GitHub /releases/latest API excludes drafts and prereleases. RPM expands
# Version while creating the SRPM, so the resulting SRPM has a concrete version.
Name:           LH4051-DE
Version:        %(curl -fsSL https://api.github.com/repos/kuznix-code/LH4051-DE/releases/latest | grep '"tag_name"' | head -n1 | cut -d '"' -f4 | sed 's/^v//')
Release:        1%{?dist}
Summary:        GTK4 desktop shell inspired by Windows Longhorn Build 4051

License:        GPL-3.0-or-later
URL:            https://github.com/kuznix-code/LH4051-DE
Source0:        https://github.com/kuznix-code/LH4051-DE/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  gtk4-devel
BuildRequires:  glib2-devel
BuildRequires:  gtk4-layer-shell-devel

%description
LH4051-DE is a GTK4 desktop shell recreating the appearance and workflow of
Windows Longhorn Build 4051. It includes a taskbar, Start menu, sidebar,
Explorer, and X11/Wayland session support.

%package data
Summary:        Application menu entry for LH4051-DE
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildArch:      noarch

%description data
Desktop application entry for launching LH4051-DE in windowed mode.

%package session
Summary:        X11 login session for LH4051-DE
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description session
X11 display-manager session entry and launcher integration for LH4051-DE.
The session wrapper can start an available window manager.

%package session-wayland
Summary:        Wayland login session for LH4051-DE
Requires:       %{name}%{?_isa} = %{version}-%{release}
Recommends:     labwc

%description session-wayland
Wayland display-manager session entry for LH4051-DE. The session wrapper
supports layer-shell compositors such as labwc and sway.

%if %{with updater}
%package updater
Summary:        Optional self-updater for LH4051-DE
Requires:       %{name} = %{version}-%{release}

%description updater
Self-updater for LH4051-DE. Intended primarily for Linux From Scratch and
other systems without a package manager. On package-managed distributions,
updates should normally be installed through the system package manager.

%endif
%if %{with bootstrap}
%package bootstrap
Summary:        Optional bootstrap installer for LH4051-DE
Requires:       %{name} = %{version}-%{release}

%description bootstrap
Bootstrap installer for LH4051-DE. Intended primarily for Linux From Scratch
systems, where users manage installation and updates outside a package manager.

%endif

%prep
%autosetup -n LH4051-DE-%{version}

%build
%make_build LAYER_SHELL=auto

%install
%make_install PREFIX=%{_prefix}
%if %{with updater}
%make_install PREFIX=%{_prefix} install-updater
%endif
%if %{with bootstrap}
%make_install PREFIX=%{_prefix} install-bootstrap
%endif

%files
%license LICENSE
%{_bindir}/lh4051-de
%{_bindir}/lh4051-de-session
%{_datadir}/lh4051-de/version

%files data
%{_datadir}/applications/lh4051-de.desktop

%files session
%{_datadir}/xsessions/lh4051-de.desktop

%files session-wayland
%{_datadir}/wayland-sessions/lh4051-de.desktop

%if %{with updater}
%files updater
%{_bindir}/lh4051-de-updater
%endif

%if %{with bootstrap}
%files bootstrap
%{_bindir}/lh4051-de-bootstrap
%endif
