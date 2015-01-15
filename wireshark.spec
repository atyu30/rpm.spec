%global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

%global with_adns 0
%global with_lua 1
%global with_gtk2 1

%global with_portaudio 1
%global with_GeoIP 1


Summary:	Network traffic analyzer
Name:		wireshark
Version:	1.12.2
Release:	1%{?dist}
License:	GPL+
Group:		Applications/Internet
Source0:	http://wireshark.org/download/src/%{name}-%{version}.tar.bz2
Source1:	90-wireshark-usbmon.rules
# Fedora-specific
Patch1:		wireshark-0001-enable-Lua-support.patch
# Fedora-specific
Patch2:		wireshark-0002-Customize-permission-denied-error.patch
# Will be proposed upstream
Patch3:		wireshark-0003-fix-string-overrun-in-plugins-profinet.patch
# Will be proposed upstream
Patch4:		wireshark-0004-adds-autoconf-macro-file.patch
# Fedora-specific
Patch5:		wireshark-0005-Restore-Fedora-specific-groups.patch
# Will be proposed upstream
Patch6:		wireshark-0006-Add-pkgconfig-entry.patch
# Will be proposed upstream
Patch7:		wireshark-0007-Install-autoconf-related-file.patch
# Fedora-specific
Patch8:		wireshark-0008-move-default-temporary-directory-to-var-tmp.patch
# Fedora-specific
Patch9:		wireshark-0009-Fix-paths-in-a-wireshark.desktop-file.patch
# Update, when pushed upstream: https://code.wireshark.org/review/#/c/3770/
Patch10:		wireshark-0010-fields-print-format.patch

Url:		http://www.wireshark.org/
BuildRequires:	libpcap-devel >= 0.9
BuildRequires:	libsmi-devel
BuildRequires:	zlib-devel, bzip2-devel
BuildRequires:	openssl-devel
BuildRequires:	glib2-devel
BuildRequires:	elfutils-devel, krb5-devel
BuildRequires:	pcre-devel, libselinux
BuildRequires:	gnutls-devel
BuildRequires:	desktop-file-utils
BuildRequires:	xdg-utils
BuildRequires:	flex, bison
BuildRequires:	libcap-devel
%if 0%{?fedora} > 18
BuildRequires:	perl-podlators
%endif
BuildRequires:	libgcrypt-devel
%if %{with_GeoIP}
BuildRequires:	GeoIP-devel
%endif
%if %{with_adns}
BuildRequires:	adns-devel
%else
BuildRequires:	c-ares-devel
%endif
%if %{with_portaudio}
BuildRequires:	portaudio-devel
%endif
%if %{with_lua}
BuildRequires:	lua-devel
%endif
%if %{with_gtk2}
BuildRequires:	gtk2-devel
%else
BuildRequires:	gtk3-devel
%endif

# Temporary hack - wireshark-1.8.0 is not compilable with upstream
# Makefile.in / configure, they need to be regenerated
BuildRequires: libtool, automake, autoconf

Requires(pre):	shadow-utils
%if %{with_adns}
Requires:	adns
%endif

%package	gnome
Summary:	Gnome desktop integration for wireshark
Group:		Applications/Internet
Requires:	%{name} = %{version}-%{release}
Requires:	xdg-utils
Requires:	hicolor-icon-theme
%if %{with_gtk2}
Requires:	gtk2
%else
Requires:	gtk3
%endif
%if %{with_portaudio}
Requires:	portaudio
%endif
%if %{with_GeoIP}
Requires:	GeoIP
%endif

%package devel
Summary:	Development headers and libraries for wireshark
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release} glibc-devel glib2-devel


%description
Wireshark is a network traffic analyzer for Unix-ish operating systems.

This package lays base for libpcap, a packet capture and filtering
library, contains command-line utilities, contains plugins and
documentation for wireshark. A graphical user interface is packaged
separately to GTK+ package.

%description gnome
Contains wireshark for Gnome 2 and desktop integration file

%description devel
The wireshark-devel package contains the header files, developer
documentation, and libraries required for development of wireshark scripts
and plugins.


%prep
%setup -q

%if %{with_lua}
%patch1 -p1 -b .enable_lua
%endif

%patch2 -p1 -b .perm_denied_customization
%patch3 -p1 -b .profinet_crash
%patch4 -p1 -b .add_autoconf
%patch5 -p1 -b .restore_group

# Somebody forgot to add this file into tarball (fixed in wireshark-1.12.1)
echo "prefix=@CMAKE_INSTALL_PREFIX@
exec_prefix=\${prefix}
libdir=\${prefix}/@CMAKE_INSTALL_LIBDIR@
sharedlibdir=\${libdir}
includedir=\${prefix}/include/wireshark
plugindir=@PLUGIN_INSTALL_DIR@

Name: wireshark
Description: wireshark network packet dissection library
Version: @PROJECT_VERSION@

Requires:
Libs: -L\${libdir} -L\${sharedlibdir} -lwireshark
Cflags: -I\${includedir}" > wireshark.pc.in

%patch6 -p1 -b .add_pkgconfig
%patch7 -p1 -b .install_autoconf
%patch8 -p1 -b .tmp_dir
%patch9 -p1 -b .fix_paths
%patch10 -p1 -b .fields-print-format

%build
%ifarch s390 s390x sparcv9 sparc64
export PIECFLAGS="-fPIE"
%else
export PIECFLAGS="-fpie"
%endif
# FC5+ automatic -fstack-protector-all switch
export RPM_OPT_FLAGS=${RPM_OPT_FLAGS//-fstack-protector-strong/-fstack-protector-all}
export CFLAGS="$RPM_OPT_FLAGS $CPPFLAGS $PIECFLAGS -D_LARGEFILE64_SOURCE"
export CXXFLAGS="$RPM_OPT_FLAGS $CPPFLAGS $PIECFLAGS -D_LARGEFILE64_SOURCE"
export LDFLAGS="$LDFLAGS -pie"

autoreconf -ivf

%configure \
   --bindir=%{_sbindir} \
   --enable-ipv6 \
   --with-libsmi \
   --with-gnu-ld \
   --with-pic \
%if %{with_gtk2}
   --with-gtk2 \
   --with-gtk3=no \
%else
   --with-gtk3=yes \
%endif
%if %{with_adns}
   --with-adns \
%else
   --with-adns=no \
%endif
%if %{with_lua}
   --with-lua \
%else
   --with-lua=no \
%endif
%if %{with_portaudio}
   --with-portaudio \
%else
  --with-portaudio=no \
%endif
%if %{with_GeoIP}
   --with-geoip \
%else
   --with-geoip=no \
%endif
   --with-ssl \
   --disable-warnings-as-errors \
   --with-plugins=%{_libdir}/%{name}/plugins/%{version} \
   --enable-airpcap

#remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
# The evil plugins hack
perl -pi -e 's|-L../../epan|-L../../epan/.libs|' plugins/*/*.la

make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} install_desktop_files

# Install python stuff.
mkdir -p %{buildroot}%{python_sitearch}
install -m 644 tools/wireshark_be.py tools/wireshark_gen.py  %{buildroot}%{python_sitearch}

desktop-file-validate %{buildroot}%{_datadir}/applications/wireshark.desktop

#install devel files (inspired by debian/wireshark-dev.header-files)
install -d -m 0755  %{buildroot}%{_includedir}/wireshark
IDIR="%{buildroot}%{_includedir}/wireshark"
mkdir -p "${IDIR}/epan"
mkdir -p "${IDIR}/epan/crypt"
mkdir -p "${IDIR}/epan/ftypes"
mkdir -p "${IDIR}/epan/dfilter"
mkdir -p "${IDIR}/epan/dissectors"
mkdir -p "${IDIR}/epan/wmem"
mkdir -p "${IDIR}/wiretap"
mkdir -p "${IDIR}/wsutil"
mkdir -p %{buildroot}/%{_sysconfdir}/udev/rules.d
install -m 644 color.h config.h register.h	"${IDIR}/"
install -m 644 cfile.h file.h			"${IDIR}/"
install -m 644 epan/*.h				"${IDIR}/epan/"
install -m 644 epan/crypt/*.h			"${IDIR}/epan/crypt"
install -m 644 epan/ftypes/*.h			"${IDIR}/epan/ftypes"
install -m 644 epan/dfilter/*.h			"${IDIR}/epan/dfilter"
install -m 644 epan/dissectors/*.h		"${IDIR}/epan/dissectors"
install -m 644 epan/wmem/*.h			"${IDIR}/epan/wmem"
install -m 644 wiretap/*.h			"${IDIR}/wiretap"
install -m 644 wsutil/*.h			"${IDIR}/wsutil"
install -m 644 ws_symbol_export.h               "${IDIR}/"
install -m 644 %{SOURCE1}                       %{buildroot}/%{_sysconfdir}/udev/rules.d/

# Remove .la files
rm -f %{buildroot}%{_libdir}/%{name}/plugins/%{version}/*.la

# Remove .la files in libdir
rm -f %{buildroot}%{_libdir}/*.la

%pre
getent group wireshark >/dev/null || groupadd -r wireshark
getent group usbmon >/dev/null || groupadd -r usbmon

%post
/sbin/ldconfig
/usr/bin/udevadm trigger --subsystem-match=usbmon

%postun -p /sbin/ldconfig

%post gnome
update-desktop-database &> /dev/null ||:
touch --no-create %{_datadir}/icons/gnome &>/dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
touch --no-create %{_datadir}/mime/packages &> /dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%postun gnome
update-desktop-database &> /dev/null ||:
if [ $1 -eq 0 ] ; then
	touch --no-create %{_datadir}/icons/gnome &>/dev/null
	gtk-update-icon-cache %{_datadir}/icons/gnome &>/dev/null || :

	touch --no-create %{_datadir}/icons/hicolor &>/dev/null
	gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

        touch --no-create %{_datadir}/mime/packages &> /dev/null || :
        update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/gnome &>/dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%files
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README*
%{_sbindir}/editcap
%{_sbindir}/tshark
%{_sbindir}/mergecap
%{_sbindir}/text2pcap
%{_sbindir}/dftest
%{_sbindir}/capinfos
%{_sbindir}/captype
%{_sbindir}/randpkt
%{_sbindir}/reordercap
%attr(0750, root, wireshark) %caps(cap_net_raw,cap_net_admin=ep) %{_sbindir}/dumpcap
%{_sbindir}/rawshark
%{_sysconfdir}/udev/rules.d/90-wireshark-usbmon.rules
%{python_sitearch}/*.py*
%{_libdir}/lib*.so.*
%{_libdir}/wireshark
%{_mandir}/man1/editcap.*
%{_mandir}/man1/tshark.*
%{_mandir}/man1/mergecap.*
%{_mandir}/man1/text2pcap.*
%{_mandir}/man1/capinfos.*
%{_mandir}/man1/dumpcap.*
%{_mandir}/man4/wireshark-filter.*
%{_mandir}/man1/rawshark.*
%{_mandir}/man1/dftest.*
%{_mandir}/man1/randpkt.*
%{_mandir}/man1/reordercap.*
%{_datadir}/wireshark
%if %{with_lua}
%exclude %{_datadir}/wireshark/init.lua
%endif


%files gnome
%{_datadir}/applications/wireshark.desktop
%{_datadir}/icons/hicolor/16x16/apps/wireshark.png
%{_datadir}/icons/hicolor/24x24/apps/wireshark.png
%{_datadir}/icons/hicolor/32x32/apps/wireshark.png
%{_datadir}/icons/hicolor/48x48/apps/wireshark.png
%{_datadir}/icons/hicolor/64x64/apps/wireshark.png
%{_datadir}/icons/hicolor/128x128/apps/wireshark.png
%{_datadir}/icons/hicolor/256x256/apps/wireshark.png
%{_datadir}/icons/hicolor/16x16/mimetypes/application-wireshark-doc.png
%{_datadir}/icons/hicolor/24x24/mimetypes/application-wireshark-doc.png
%{_datadir}/icons/hicolor/32x32/mimetypes/application-wireshark-doc.png
%{_datadir}/icons/hicolor/48x48/mimetypes/application-wireshark-doc.png
%{_datadir}/icons/hicolor/64x64/mimetypes/application-wireshark-doc.png
%{_datadir}/icons/hicolor/128x128/mimetypes/application-wireshark-doc.png
%{_datadir}/icons/hicolor/256x256/mimetypes/application-wireshark-doc.png
%{_datadir}/icons/hicolor/scalable/apps/wireshark.svg
%{_datadir}/mime/packages/wireshark.xml
%{_sbindir}/wireshark
%{_mandir}/man1/wireshark.*

%files devel
%doc doc/README.*
%if %{with_lua}
%config(noreplace) %{_datadir}/wireshark/init.lua
%endif
%{_includedir}/wireshark
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_datadir}/aclocal/*

%changelog
* Fri Dec  5 2014 atyu30 <ipostfix@gmail.com> - 1.12.2-2
- Build for RHEL7.0

* Mon Nov 17 2014 Peter Hatina <phatina@redhat.com> - 1.12.2-1
- Ver. 1.12.2

* Mon Sep 22 2014 Peter Hatina <phatina@redhat.com> - 1.12.1-1
- Ver. 1.12.1

