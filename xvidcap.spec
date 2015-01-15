Summary: An X-Windows screen capture tool
Name:    xvidcap
Version: 1.1.7
Release: 12%{?dist}
License: GPLv2
Group:   Applications/Multimedia
URL:     http://xvidcap.sourceforge.net
Source0: http://sourceforge.net/projects/xvidcap/%{name}-%{version}.tar.gz
Patch0:  shmstr.h.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gettext
BuildRequires: libXmu-devel
BuildRequires: scrollkeeper
BuildRequires: lame-devel, libvorbis-devel
BuildRequires: ffmpeg-devel >= 0.4.8
BuildRequires: perl(XML::Parser)
BuildRequires: libglade2-devel
BuildRequires: dbus-devel dbus-glib-devel
Requires: mplayer
Obsoletes: gvidcap < %{version}
Provides: gvidcap = %{version}

%description
xvidcap is a screen capture tool for creating videos off
an X-Window desktop for illustration or documentation purposes. 
It is intended to be a standard-based alternative for 
commercial tools, such as Lotus ScreenCam or Camtasia Studio.

%prep
%setup -q
if [ ! -e "/usr/include/X11/extensions/shmstr.h" ]; then
%patch0 -p1 -b .shmstr
fi

%build
export LDFLAGS="$LDFLAGS -lX11 -lz -lXext"
%configure
make

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
rm -fr %{buildroot}%{_prefix}/doc
rm -fr %{buildroot}%{_datadir}/doc/%{name}
ln -s %{name} %{buildroot}%{_bindir}/gvidcap
%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README INSTALL AUTHORS ChangeLog
%{_bindir}/%{name}
%{_bindir}/%{name}-dbus-client
%{_bindir}/gvidcap
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/omf/%{name}
%{_datadir}/gnome/help/%{name}
%{_datadir}/dbus-1/services/net.jarre_de_the.Xvidcap.service
%{_mandir}/man1/%{name}*.1*
%{_mandir}/*/man1/%{name}*.1*

%changelog
* Tue Sep 30 2014 atyu30 <ipostfix@gmail.com> - 1.1.7-13
- Build for RHEL7
* Thu May 27 2010 Paulo Roma <roma@lcg.ufrj.br> - 1.1.7-12
- Fixed dso.

