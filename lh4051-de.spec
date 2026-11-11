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
Release:        3%{?dist}
Summary:        GTK4 desktop shell inspired by Windows Longhorn Build 4051

License:        GPL-3.0-or-later
URL:            https://github.com/kuznix-code/LH4051-DE
Source0:        https://github.com/kuznix-code/LH4051-DE/archive/refs/heads/stable.tar.gz

Requires:       %{name}-data = %{version}-%{release}

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
BuildArch:      noarch

%description data
Desktop application entry for launching LH4051-DE in windowed mode.

%package session
Summary:        X11 login session for LH4051-DE
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       openbox

%description session
X11 display-manager session entry and launcher integration for LH4051-DE.
The session wrapper can start an available window manager.

%package session-xfwm4
Summary:        X11 login session for LH4051-DE with Xfwm4
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       xfwm4
BuildArch:      noarch

%description session-xfwm4
X11 display-manager session entry for LH4051-DE configured to launch xfwm4.

%package session-marco
Summary:        X11 login session for LH4051-DE with Marco
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       marco
BuildArch:      noarch

%description session-marco
X11 display-manager session entry for LH4051-DE configured to launch marco.

%package session-metacity
Summary:        X11 login session for LH4051-DE with Metacity
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       metacity
BuildArch:      noarch

%description session-metacity
X11 display-manager session entry for LH4051-DE configured to launch metacity.

%package session-icewm
Summary:        X11 login session for LH4051-DE with Icewm
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       icewm
BuildArch:      noarch

%description session-icewm
X11 display-manager session entry for LH4051-DE configured to launch icewm.

%package session-fluxbox
Summary:        X11 login session for LH4051-DE with Fluxbox
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       fluxbox
BuildArch:      noarch

%description session-fluxbox
X11 display-manager session entry for LH4051-DE configured to launch fluxbox.

%package session-wayland
Summary:        Wayland login session for LH4051-DE
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       labwc

%description session-wayland
Wayland display-manager session entry for LH4051-DE. The session wrapper
supports layer-shell compositors such as labwc and sway.

%package session-wayland-sway
Summary:        Wayland login session for LH4051-DE with Sway
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       sway
BuildArch:      noarch

%description session-wayland-sway
Wayland display-manager session entry configured to launch LH4051-DE with Sway.

%package sessions-x11-all
Summary:        All LH4051-DE X11 sessions
Requires:       %{name}-session = %{version}-%{release}
Requires:       %{name}-session-xfwm4 = %{version}-%{release}
Requires:       %{name}-session-marco = %{version}-%{release}
Requires:       %{name}-session-metacity = %{version}-%{release}
Requires:       %{name}-session-icewm = %{version}-%{release}
Requires:       %{name}-session-fluxbox = %{version}-%{release}
BuildArch:      noarch

%description sessions-x11-all
Meta-package installing every available LH4051-DE X11 session.

%package sessions-wayland-all
Summary:        All LH4051-DE Wayland sessions
Requires:       %{name}-session-wayland = %{version}-%{release}
Requires:       %{name}-session-wayland-sway = %{version}-%{release}
BuildArch:      noarch

%description sessions-wayland-all
Meta-package installing every available LH4051-DE Wayland session.

%package sessions-all
Summary:        All LH4051-DE sessions
Requires:       %{name}-sessions-x11-all = %{version}-%{release}
Requires:       %{name}-sessions-wayland-all = %{version}-%{release}
BuildArch:      noarch

%description sessions-all
Meta-package installing every available LH4051-DE X11 and Wayland session.

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
%autosetup -n LH4051-DE-stable

%build
%make_build LAYER_SHELL=auto

%install
%make_install PREFIX=%{_prefix}
# The upstream default install target currently installs the updater too.
# Keep it out of the default package set unless its optional subpackage is enabled.
%if %{without updater}
rm -f %{buildroot}%{_bindir}/lh4051-de-updater
%else
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

%files session-xfwm4
%{_datadir}/xsessions/lh4051-de-xfwm4.desktop

%files session-marco
%{_datadir}/xsessions/lh4051-de-marco.desktop

%files session-metacity
%{_datadir}/xsessions/lh4051-de-metacity.desktop

%files session-icewm
%{_datadir}/xsessions/lh4051-de-icewm.desktop

%files session-fluxbox
%{_datadir}/xsessions/lh4051-de-fluxbox.desktop

%files session-wayland
%{_datadir}/wayland-sessions/lh4051-de.desktop

%files session-wayland-sway
%{_datadir}/wayland-sessions/lh4051-de-sway.desktop

%files sessions-x11-all

%files sessions-wayland-all

%files sessions-all

%if %{with updater}
%files updater
%{_bindir}/lh4051-de-updater
%endif

%if %{with bootstrap}
%files bootstrap
%{_bindir}/lh4051-de-bootstrap
%endif
