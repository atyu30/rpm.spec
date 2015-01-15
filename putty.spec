Name:		putty
Version:	0.63
Release:	3%{?dist}
Summary:	SSH, Telnet and Rlogin client
License:	MIT
Group:		Applications/Internet
URL:		http://www.chiark.greenend.org.uk/~sgtatham/putty/
Source0:	http://the.earth.li/~sgtatham/putty/latest/%{name}-%{version}.tar.gz
Source2:	%{name}.desktop
# By default create new files as non-executables
BuildRequires:	gtk2-devel krb5-devel halibut desktop-file-utils
BuildRequires:	ImageMagick

%description
Putty is a SSH, Telnet & Rlogin client - this time for Linux.

%prep

%setup -q

%build
./mkfiles.pl
make -C doc
pushd unix
%{__sed} -i -e "s/-O2 -Wall -Werror/$RPM_OPT_FLAGS/g" \
	-e "s,/usr/local,%{_prefix},g" \
	Makefile.gtk
ln -s Makefile.gtk Makefile
popd
make %{?_smp_mflags} VER=-DSNAPSHOT=%{version} -C unix
make -C icons putty-32.png

%install
rm -rf $RPM_BUILD_ROOT
install -d  html
install -pm 0644 doc/*.html html
make install DESTDIR=$RPM_BUILD_ROOT prefix=%{_prefix} mandir=%{_mandir} INSTALL="install -p" -C unix

desktop-file-install \
  --vendor "" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %{SOURCE2}

install -m644 -D -p icons/putty-32.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/putty.png

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc LICENCE html
%{_bindir}/*
%{_mandir}/man1/*.1*
%{_datadir}/applications/*
%{_datadir}/pixmaps/%{name}.png


%changelog
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.63-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.63-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 12 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 0.63-1
- New version
  Resolves: rhbz#995610
- Dropped perms, CVE-2013-4852, CVE-2013-4206, CVE-2013-4207,
  CVE-2013-4208 patches (all in upstream)

* Thu Aug  8 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 0.62-7
- Fixed a heap-corrupting buffer underrun bug in the modmul function
  Resolves: CVE-2013-4206
- Fixed a buffer overflow vulnerability in the calculation of modular
  inverses when verifying a DSA signature
  Resolves: CVE-2013-4207
- Fixed problem when private keys are left in memory after being
  used by PuTTY tools
  Resolves: CVE-2013-4208

* Mon Aug  5 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 0.62-6
- Fixed integer overflow
  Resolves: CVE-2013-4852
- Fixed bogus dates in changelog (best estimated)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.62-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.62-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Sep 26 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 0.62-3
- Added missing ImageMagick BuildRequires

* Wed Sep 19 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 0.62-2
- Generated icon from sources

* Tue Aug  7 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 0.62-1
- New version

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-9.20100910svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.60-8.20100910svn
- Rebuild for new libpng

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-7.20100910svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep 10 2010 Mark Chappell <tremble@fedoraproject.org> - 0.60-6.20100910svn
- Bump version in line with packaging specs

* Fri Sep 10 2010 Mark Chappell <tremble@fedoraproject.org> - 0.60-6.8991svn
- Update to latest GTK2 version from SVN (r8991)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 13 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 0.60-3
- Bump-n-build for GCC 4.3

* Tue Aug 21 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 0.60-2
- Rebuild for BuildID

* Mon Apr 30 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 0.60-1
- New upstream version (mostly bugfixes)
- Previous release pre-emptively fixed CVE-2006-7162/BZ#231726
- Added patch to make "private" files (keys/logs) non-executable

* Thu Jan 25 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 0.59-1
- New upstream version
- Macro-ized Source filenames
- Cleanup of spaces/tabs to eliminate rpmlint warnings

* Sun Aug 27 2006 Michael J. Knox <michael[AT]knox.net.nz> - 0.58-3
- Rebuild for FC6

* Wed May 03 2006 Michael J. Knox <michael[AT]knox.net.nz> - 0.58-2
- rebuild

* Tue Apr 19 2005 Adrian Reber <adrian@lisas.de> - 0.58-1
- Updated to 0.58

* Tue Mar 01 2005 Adrian Reber <adrian@lisas.de> - 0.57-2
- fix build with gcc4

* Mon Feb 21 2005 Adrian Reber <adrian@lisas.de> - 0.57-1
- Updated to 0.57

* Tue Oct 26 2004 Adrian Reber <adrian@lisas.de> - 0.56-0.fdr.1
- Updated to 0.56 (bug #2209)

* Fri Aug  6 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.55-0.fdr.2
- Fix URL and source location.

* Thu Aug 05 2004 Andreas Pfaffeneder <fedora@zuhause-local.de> 0:0.55.fdr.1
- Update to 0.55 due to security problem (CORE-2004-0705).

* Tue Nov 18 2003 Andreas Pfaffeneder <fedora@zuhause-local.de> 0:0.0-0.fdr.2.20030821
- Add desktop-file-utils to build requires

* Sun Aug 24 2003 Adrian Reber <adrian@lisas.de> 0:0.0-0.fdr.1.20030821
- now honouring $RPM_OPT_FLAGS
- moved make to the build section; binaries are now stripped
- inserted _smp_mflags
- using makeinstall
- created a icon for the menu entry
- optimized the category of the .desktop file from Internet to Network
- more fedorafication

* Thu Aug 21 2003 Andreas Pfaffeneder <fedora@zuhause-local.de> 0:0.0-0.fdr.0.20030821
- Quick and dirty spec for cvs of putty
