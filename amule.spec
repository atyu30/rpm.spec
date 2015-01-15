# TODO: setup firefox for ed2k links using triggers and a file in /usr/lib/firefox-3.0.1/defaults/preferences/
%global _hardened_build 1

Name:           amule
Version:        2.3.1
Release:        3%{?dist}
Summary:        File sharing client compatible with eDonkey
License:        GPLv2+
Group:          Applications/Internet
Source0:        http://dl.sourceforge.net/%{name}/aMule-%{version}.tar.xz
Patch0:         aMule-2.3.1-gcc47.patch
URL:            http://amule.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# See http://www.amule.org/wiki/index.php/Requirements
BuildRequires:  wxGTK-devel >= 0:2.8.7, desktop-file-utils, expat-devel
BuildRequires:  gd-devel >= 2.0.0, libpng-devel
BuildRequires:  gettext-devel, flex, bison
BuildRequires:  readline-devel, cryptopp-devel, libupnp-devel
BuildRequires:  GeoIP-devel
Requires(pre):  chkconfig
Requires:       %{name}-nogui

%description
aMule is an easy to use multi-platform client for ED2K Peer-to-Peer
Network. It is a fork of xMule, whis was based on eMule for
Windows. aMule currently supports (but is not limited to) the
following platforms: Linux, *BSD and MacOS X.

%package nogui
Summary:        Components of aMule which don't require a GUI (for servers)
Group:          Applications/Internet

%description nogui
This package contains the aMule components which don't require a GUI.
It is useful for servers which don't have Xorg.


%package -n xchat-%{name}
Summary:        Plugin to display aMule's statistics in XChat
Group:          Applications/Internet
Requires:       %{name} = %{version}-%{release}
Requires:       xchat
%if 0%{?fedora} > 9 || 0%{?rhel} > 5 
BuildArch:      noarch 
%endif 

%description -n xchat-%{name}
This plugins allows you to display aMule statistics in XChat


%prep
%setup -q -n aMule-%{version}
%patch0 -p1 -b .gcc47
manfiles=`find . -name "*.1"`
for manfile in $manfiles; do
    iconv -f ISO-8859-1 -t UTF-8 < $manfile > $manfile.utf8
    touch -r $manfile $manfile.utf8
    mv -f $manfile.utf8 $manfile
done

%build
%configure \
    --disable-rpath \
    --disable-debug \
    --docdir=%{_datadir}/doc/%{name}-%{version} \
    --enable-wxcas \
    --enable-cas \
    --enable-alc \
    --enable-alcc \
    --enable-xas \
    --enable-amule-daemon \
    --enable-amulecmd \
    --enable-webserver \
    --enable-amule-daemon \
    --enable-geoip \
    --enable-ccache \
    --enable-amule-gui \
    --enable-optimize \
    --with-denoise-level=0

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT _docs

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

%find_lang %{name}

# desktop files
desktop-file-install --vendor livna \
                     --delete-original\
                     --dir $RPM_BUILD_ROOT%{_datadir}/applications\
                     --add-category Network\
                     $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

iconv -f ISO-8859-1 -t UTF-8 < src/utils/aLinkCreator/alc.desktop \
      > $RPM_BUILD_ROOT%{_datadir}/applications/alc.desktop
desktop-file-install --vendor livna \
                     --delete-original\
                     --dir $RPM_BUILD_ROOT%{_datadir}/applications\
                     $RPM_BUILD_ROOT%{_datadir}/applications/alc.desktop

desktop-file-install --vendor livna \
                     --delete-original\
                     --dir $RPM_BUILD_ROOT%{_datadir}/applications\
                     $RPM_BUILD_ROOT%{_datadir}/applications/wxcas.desktop

desktop-file-install --vendor livna \
                     --delete-original\
                     --dir $RPM_BUILD_ROOT%{_datadir}/applications\
                     --add-category Network\
                     $RPM_BUILD_ROOT%{_datadir}/applications/%{name}gui.desktop


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc ABOUT-NLS
%{_bindir}/alc
%{_bindir}/amule
%{_bindir}/cas
%{_bindir}/wxcas
%{_bindir}/amulegui
%{_datadir}/%{name}/
%{_datadir}/cas
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*
%{_mandir}/man1/alc.1.gz
%{_mandir}/*/man1/alc.1.gz
%{_mandir}/man1/amule.1.gz
%{_mandir}/*/man1/amule.1.gz
%{_mandir}/man1/cas.1.gz
%{_mandir}/*/man1/cas.1.gz
%{_mandir}/man1/wxcas.1.gz
%{_mandir}/*/man1/wxcas.1.gz
%{_mandir}/man1/amulegui.1.gz
%{_mandir}/*/man1/amulegui.1.gz
%exclude %{_datadir}/%{name}/webserver

%files nogui
%defattr(-,root,root,-)
%{_bindir}/alcc
%{_bindir}/amulecmd
%{_bindir}/amuled
%{_bindir}/amuleweb
%{_bindir}/ed2k
%{_datadir}/%{name}/webserver
%{_mandir}/man1/alcc.1.gz
%{_mandir}/*/man1/alcc.1.gz
%{_mandir}/man1/amulecmd.1.gz
%{_mandir}/*/man1/amulecmd.1.gz
%{_mandir}/man1/amuled.1.gz
%{_mandir}/*/man1/amuled.1.gz
%{_mandir}/man1/amuleweb.1.gz
%{_mandir}/*/man1/amuleweb.1.gz
%{_mandir}/man1/ed2k.1.gz
%{_mandir}/*/man1/ed2k.1.gz


%files -n xchat-%{name}
%defattr(-,root,root,-)
%{_bindir}/autostart-xas
%attr(0755, root, root) %{_libdir}/xchat/plugins/xas.pl
%{_mandir}/man1/xas.1.gz
%{_mandir}/*/man1/xas.1.gz


%changelog
* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-3
- Mass rebuilt for Fedora 19 Features

