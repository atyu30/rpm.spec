Summary:	Extract headers from rpm in a old yum repository
Name:		yum-arch
Version:	2.2.2
Release:	13%{?dist}
License:	GPLv2+
Group:		System Environment/Base
URL:		http://linux.duke.edu/yum/
Source0:	http://linux.duke.edu/projects/yum/download/2.2/yum-%{version}.tar.gz
Patch1:		yum-arch-folder.patch
Patch2:		yum-arch-python26.patch
Patch3:		yum-arch-2.2.2-python-2.2.patch
Patch4:		yum-arch-2.2.2-no-dep-warn.patch
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:	python2, gettext
Requires:	python, rpm-python, rpm >= 0:4.1.1, libxml2-python

%description
Extract headers from rpm in a old yum repository.

This package only provides the old yum-arch command from yum-%{version}.
It should be used to generate repository information for Fedora Core < 4
and Red Hat Enterprise Linux < 5, all of which are now unsupported.

%prep
%setup -q -n yum-%{version}

# This is yum-arch, no longer yum
%patch1 -p0 -b .folder

# Fix syntax to be compatible with python2 ≥ 2.6
%patch2 -p1 -b .p26

# Avoid dependency on /usr/bin/python2.2
%patch3

# Silence the deprecation warning; anybody that's tracked down this package
# knows that they're building repos for EOL distros
%patch4

%build
make

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

# Placate rpmlint
find %{buildroot}%{_datadir}/%{name} -name '*.py' |
	xargs grep -l '^#!/usr/' |
	xargs chmod -c +x

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog
%{_bindir}/yum-arch
%{_datadir}/yum-arch/
%{_mandir}/man8/yum-arch.8*

%changelog
* Mon Apr  2 2012 Paul Howarth <paul@city-fan.org> - 2.2.2-13
- Import from Fedora

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 11 2010 David Malcolm <dmalcolm@redhat.com> - 2.2.2-10
- Recompiling .py files against Python 2.7 (#623421)

* Sun Feb 14 2010 Remi Collet <Fedora@FamilleCollet.com> - 2.2.2-9
- Improve python 2.6 patch (fix FTBFS #564994)

* Sat Sep 26 2009 Remi Collet <Fedora@FamilleCollet.com> - 2.2.2-8
- Fix python 2.6 warnings (#521869)

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 16 2009 Remi Collet <Fedora@FamilleCollet.com> - 2.2.2-6
- Fix python 2.6 issue

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.2.2-4
- Rebuild for Python 2.6

* Mon Aug 11 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.2.2-3
- Fix license tag

* Sun Feb 18 2007 Remi Collet <Fedora@FamilleCollet.com> - 2.2.2-2
- From package review (#229123) 
  - Own /usr/share/yum-arch
  - Delete shellbangs in libs

* Sat Feb 17 2007 Remi Collet <Fedora@FamilleCollet.com> - 2.2.2-1
- Initial spec for Extras
