Summary: Statically linked binary providing simplified versions of system commands
Name: busybox
Version: 1.19.4
Release: 15%{?dist}
Epoch: 1
License: GPLv2
Group: System Environment/Shells
URL: http://www.busybox.net

Source: http://www.busybox.net/downloads/%{name}-%{version}.tar.bz2
Source1: busybox-static.config
Source2: busybox-petitboot.config
Patch1: busybox-1.15.1-uname.patch
Patch2: busybox-1.19.4-ext2_fs_h.patch
Patch3: busybox-1.19-rlimit_fsize.patch

BuildRequires: libselinux-devel >= 1.27.7-2
BuildRequires: libsepol-devel
BuildRequires: libselinux-static
BuildRequires: libsepol-static
BuildRequires: glibc-static
# This package used to include a bundled copy of uClibc, but we now
# use the system copy.
%ifnarch ppc %{power64} s390 s390x aarch64
BuildRequires: uClibc-static
%endif

%package petitboot
Group: System Environment/Shells
Summary: Version of busybox configured for use with petitboot

%description
Busybox is a single binary which includes versions of a large number
of system commands, including a shell.  This package can be very
useful for recovering from certain types of system failures,
particularly those involving broken shared libraries.

%description petitboot
Busybox is a single binary which includes versions of a large number
of system commands, including a shell.  The version contained in this
package is a minimal configuration intended for use with the Petitboot
bootloader used on PlayStation 3. The busybox package provides a binary
better suited to normal use.

%prep
%setup -q
%patch1 -b .uname -p1
%patch2 -b .ext2_fs_h -p1
%ifarch ppc %{power64} s390 s390x aarch64
%patch3 -b .rlimit_fsize -p1
%endif

%build
# create static busybox - the executable is kept as busybox-static
# We use uclibc instead of system glibc, uclibc is several times
# smaller, this is important for static build.
# uclibc can't be built on ppc64,s390,ia64, we set $arch to "" in this case
arch=`uname -m | sed -e 's/i.86/i386/' -e 's/armv7l/arm/' -e 's/armv5tel/arm/' -e 's/aarch64//' -e 's/ppc64le//' -e 's/ppc64//' -e 's/powerpc64//' -e 's/ppc//' -e 's/ia64//' -e 's/s390.*//'`

cp %{SOURCE1} .config
# set all new options to defaults
yes "" | make oldconfig
# gcc needs to be convinced to use neither system headers, nor libs,
# nor startfiles (i.e. crtXXX.o files)
if test "$arch"; then \
    mv .config .config1 && \
    grep -v ^CONFIG_SELINUX .config1 >.config && \
    yes "" | make oldconfig && \
    cat .config && \
    make V=1 \
        EXTRA_CFLAGS="-g -isystem %{_includedir}/uClibc" \
        CFLAGS_busybox="-static -nostartfiles -L%{_libdir}/uClibc %{_libdir}/uClibc/crt1.o %{_libdir}/uClibc/crti.o %{_libdir}/uClibc/crtn.o"; \
else \
    mv .config .config1 && \
    grep -v \
        -e ^CONFIG_FEATURE_HAVE_RPC \
        -e ^CONFIG_FEATURE_MOUNT_NFS \
        -e ^CONFIG_FEATURE_INETD_RPC \
        .config1 >.config && \
    echo "# CONFIG_FEATURE_HAVE_RPC is not set" >>.config && \
    echo "# CONFIG_FEATURE_MOUNT_NFS is not set" >>.config && \
    echo "# CONFIG_FEATURE_INETD_RPC is not set" >>.config && \
    yes "" | make oldconfig && \
    cat .config && \
    make V=1 CC="gcc $RPM_OPT_FLAGS"; \
fi
cp busybox_unstripped busybox.static
cp docs/busybox.1 docs/busybox.static.1

# create busybox optimized for petitboot
make clean
# copy new configuration file
cp %{SOURCE2} .config
# set all new options to defaults
yes "" | make oldconfig
# -g is needed for generation of debuginfo.
# (Don't want to use full-blown $RPM_OPT_FLAGS for this,
# it makes binary much bigger: -O2 instead of -Os, many other options)
if test "$arch"; then \
    make V=1 \
        EXTRA_CFLAGS="-g -isystem %{_includedir}/uClibc" \
        CFLAGS_busybox="-static -nostartfiles -L%{_libdir}/uClibc %{_libdir}/uClibc/crt1.o %{_libdir}/uClibc/crti.o %{_libdir}/uClibc/crtn.o"; \
else \
    make V=1 CC="%__cc $RPM_OPT_FLAGS"; \
fi
cp busybox_unstripped busybox.petitboot
cp docs/busybox.1 docs/busybox.petitboot.1

%install
mkdir -p $RPM_BUILD_ROOT/sbin
install -m 755 busybox.static $RPM_BUILD_ROOT/sbin/busybox
install -m 755 busybox.petitboot $RPM_BUILD_ROOT/sbin/busybox.petitboot
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
install -m 644 docs/busybox.static.1 $RPM_BUILD_ROOT/%{_mandir}/man1/busybox.1
install -m 644 docs/busybox.petitboot.1 $RPM_BUILD_ROOT/%{_mandir}/man1/busybox.petitboot.1


%files
%doc LICENSE README
/sbin/busybox
%{_mandir}/man1/busybox.1.gz

%files petitboot
%doc LICENSE README
/sbin/busybox.petitboot
%{_mandir}/man1/busybox.petitboot.1.gz

%changelog
* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.19.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

