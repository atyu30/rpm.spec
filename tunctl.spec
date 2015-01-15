Name:           tunctl
Version:        1.5
Release:        11%{?dist}
Summary:        Create and remove virtual network interfaces

Group:          Applications/System
License:        GPL+
URL:            http://tunctl.sourceforge.net/
Source0:        http://downloads.sourceforge.net/tunctl/tunctl-%{version}.tar.gz

BuildRequires:  docbook-utils

%description
tunctl is a tool to set up and maintain persistent TUN/TAP network
interfaces, enabling user applications access to the wire side of a
virtual nework interface. Such interfaces is useful for connecting VPN
software, virtualization, emulation and a number of other similar
applications to the network stack.

tunctl originates from the User Mode Linux project.


%prep
%setup -q


%build
make %{?_smp_mflags}


%install
make DESTDIR=%{buildroot} install


%files
%{_mandir}/man8/tunctl.8*
%{_sbindir}/tunctl
%doc ChangeLog


%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Oct 24 2013 Lubomir Rintel <lkundrak@v3.sk> - 1.5-10
- Bulk sad and useless attempt at consistent SPEC file formatting

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jul 18 2008 Henrik Nordstrom <henrik@henriknordstrom.net> 1.5-2
- Corrected package description formatting

* Wed Jul 16 2008 Henrik Nordstrom <henrik@henriknordstrom.net> 1.5-1
- Update to version 1.5 based on separate upstream release

* Tue Mar 25 2008 Lubomir Kundrak <lkundrak@redhat.com> 1.4-2
- Move to sbin (Marek Mahut, #434583)

* Fri Feb 22 2008 Lubomir Kundrak <lkundrak@redhat.com> 1.4-1
- Initial packaging
