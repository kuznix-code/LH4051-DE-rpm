Name:           LH4051-DE
Version:        0.1.1
Release:        2%{?dist}
Summary:        Longhorn 4051-inspired desktop environment
License:        GPL-3.0-or-later
URL:            https://github.com/kuznix-code/LH4051-DE
Source0:        https://github.com/kuznix-code/LH4051-DE/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  gtk4-devel >= 4.10
BuildRequires:  glib2-devel
BuildRequires:  gtk4-layer-shell-devel
Requires:       LH4051-DE-data = %{version}-%{release}
Requires:       LH4051-DE-session = %{version}-%{release}
Requires:       LH4051-DE-session-wayland = %{version}-%{release}
Recommends:     labwc
Suggests:       appstream

%global debug_package %{nil}

%description
LH4051-DE is a desktop shell inspired by Windows Longhorn build 4051, written
in C on top of GTK 4. It provides the desktop, panel, sidebar, start menu, file
manager, settings and app store, plus session wrappers for X11 and Wayland.

%package -n LH4051-DE-data
Summary:        Longhorn 4051-inspired desktop environment - data files
BuildArch:      noarch

%description -n LH4051-DE-data
Architecture-independent data files for LH4051-DE.

%package -n LH4051-DE-session
Summary:        Longhorn 4051-inspired desktop environment - X11 session
BuildArch:      noarch
Requires:       LH4051-DE = %{version}-%{release}
Requires:       openbox

%description -n LH4051-DE-session
Adds the LH4051-DE X11 session entry to the login manager.

%package -n LH4051-DE-session-wayland
Summary:        Longhorn 4051-inspired desktop environment - Wayland session
BuildArch:      noarch
Requires:       LH4051-DE = %{version}-%{release}
Requires:       labwc

%description -n LH4051-DE-session-wayland
Adds the LH4051-DE Wayland session entry to the login manager.

%package -n LH4051-DE-updater
Summary:        LH4051-DE updater
BuildArch:      noarch
Requires:       LH4051-DE = %{version}-%{release}

%description -n LH4051-DE-updater
Optional command-line updater for LH4051-DE.

%package -n LH4051-DE-bootstrap
Summary:        LH4051-DE dependency bootstrap tool
BuildArch:      noarch

%description -n LH4051-DE-bootstrap
Optional helper for building GTK 4 and its dependencies from source.

%prep
%autosetup -n LH4051-DE-%{version}

%build
%make_build PREFIX=%{_prefix} PKG_VERSION=%{version} CFLAGS="%{optflags}" LDFLAGS="%{build_ldflags}" all sessions

%check
./build/linux-gcc/lh4051-de --version

%install
%make_install PREFIX=%{_prefix} PKG_VERSION=%{version} CFLAGS="%{optflags}" LDFLAGS="%{build_ldflags}"
make DESTDIR=%{buildroot} PREFIX=%{_prefix} install-updater install-bootstrap

%files
%license LICENSE
%doc README.md
%{_bindir}/lh4051-de
%{_bindir}/lh4051-de-session
%{_datadir}/lh4051-de/

%files -n LH4051-DE-data
%license LICENSE
%{_datadir}/applications/lh4051-de.desktop

%files -n LH4051-DE-session
%license LICENSE
%{_datadir}/xsessions/lh4051-de.desktop

%files -n LH4051-DE-session-wayland
%license LICENSE
%{_datadir}/wayland-sessions/lh4051-de.desktop

%files -n LH4051-DE-updater
%license LICENSE
%{_bindir}/lh4051-de-updater

%files -n LH4051-DE-bootstrap
%license LICENSE
%{_bindir}/lh4051-de-bootstrap

%changelog
* Wed Nov 11 2026 kuznix-code <noreply@github.com> - 0.1.1-2
- Add Openbox as a required dependency for the X11 session.
- Prepare the RPM package for COPR rebuild.
