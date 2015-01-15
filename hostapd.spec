%global _hardened_build 1

Name:           hostapd
Version:        2.2
Release:        1%{?dist}
Summary:        IEEE 802.11 AP, IEEE 802.1X/WPA/WPA2/EAP/RADIUS Authenticator
License:        BSD
URL:            http://w1.fi/hostapd

Source0:        http://w1.fi/releases/%{name}-%{version}.tar.gz
Source1:        %{name}.service
Source2:        %{name}.conf
Source3:        %{name}.sysconfig
Source4:        %{name}.init
Patch0:         %{name}-RPM_OPT_FLAGS.patch
Patch1:         %{name}-EAP-TLS-server-Fix-TLS-Message-Length-validation.patch

BuildRequires:  libnl3-devel
BuildRequires:  openssl-devel

%if 0%{?fedora} || 0%{?rhel} >= 7
BuildRequires:      systemd
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
%endif

%if 0%{?rhel} == 6
Requires(post):     /sbin/chkconfig
Requires(preun):    /sbin/chkconfig
Requires(preun):    /sbin/service
Requires(postun):   /sbin/service
%endif

%description
%{name} is a user space daemon for access point and authentication servers. It
implements IEEE 802.11 access point management, IEEE 802.1X/WPA/WPA2/EAP
Authenticators and RADIUS authentication server.

%{name} is designed to be a "daemon" program that runs in the back-ground and
acts as the backend component controlling authentication. %{name} supports
separate frontend programs and an example text-based frontend, hostapd_cli, is
included with %{name}.

%package logwatch
Summary:        Logwatch scripts for hostapd
Requires:       %{name} = %{version}-%{release} logwatch perl

%description logwatch
Logwatch scripts for hostapd.

%prep
%setup -q

# Hack Makefile to allow use of RPM_OPT_FLAGS
%patch0 -p1 -b .rpmopt

# git://w1.fi/srv/git/hostap.git
# 	commit 586c446e0ff42ae00315b014924ec669023bd8de
%patch1 -p1 -b .message_length

# Prepare default config file
cat %{SOURCE2} | sed -e 's/HOSTAPD_VERSION/'%{version}'/' > %{name}.conf

%build
cd hostapd
cat defconfig | sed \
    -e '/^#CONFIG_DRIVER_NL80211=y/s/^#//' \
    -e '/^#CONFIG_RADIUS_SERVER=y/s/^#//' \
    -e '/^#CONFIG_DRIVER_WIRED=y/s/^#//' \
    -e '/^#CONFIG_DRIVER_NONE=y/s/^#//' \
    -e '/^#CONFIG_IEEE80211N=y/s/^#//' \
    -e '/^#CONFIG_FULL_DYNAMIC_VLAN=y/s/^#//' \
    -e '/^#CONFIG_LIBNL32=y/s/^#//' \
    > .config
echo "CFLAGS += -I%{_includedir}/libnl3" >> .config
echo "LIBS += -L%{_libdir}" >> .config
make %{?_smp_mflags} EXTRA_CFLAGS="$RPM_OPT_FLAGS"

%install
%if 0%{?fedora} || 0%{?rhel} >= 7

# Systemd unit files
install -p -m 644 -D %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%else

# Initscripts
install -p -m 755 -D %{SOURCE4} %{buildroot}%{_initrddir}/%{name}

%endif

# logwatch files
install -d %{buildroot}/%{_sysconfdir}/logwatch/conf/services
install -pm 0644 %{name}/logwatch/%{name}.conf  \
        %{buildroot}/%{_sysconfdir}/logwatch/conf/services/%{name}.conf
install -d %{buildroot}/%{_sysconfdir}/logwatch/scripts/services
install -pm 0755 %{name}/logwatch/%{name} \
        %{buildroot}/%{_sysconfdir}/logwatch/scripts/services/%{name}

# config files
install -d %{buildroot}/%{_sysconfdir}/%{name}
install -pm 0600 %{name}.conf %{buildroot}/%{_sysconfdir}/%{name}/%{name}.conf

install -d %{buildroot}/%{_sysconfdir}/sysconfig
install -pm 0644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

# binaries
install -d %{buildroot}/%{_sbindir}
install -pm 0755 %{name}/%{name} %{buildroot}%{_sbindir}/%{name}
install -pm 0755 %{name}/%{name}_cli %{buildroot}%{_sbindir}/%{name}_cli

# man pages
install -d %{buildroot}%{_mandir}/man{1,8}
install -pm 0644 %{name}/%{name}_cli.1 %{buildroot}%{_mandir}/man1
install -pm 0644 %{name}/%{name}.8 %{buildroot}%{_mandir}/man8

# prepare docs
cp %{name}/README ./README.%{name}
cp %{name}/README-WPS ./README-WPS.%{name}
cp %{name}/logwatch/README ./README.logwatch

%if 0%{?fedora} || 0%{?rhel} >= 7

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%endif

%if 0%{?rhel} == 6

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 -eq 0 ]; then
    /sbin/service %{name} stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi

%endif

%files
%doc COPYING README README.hostapd README-WPS.hostapd
%doc %{name}/%{name}.conf %{name}/wired.conf
%doc %{name}/%{name}.accept %{name}/%{name}.deny
%doc %{name}/%{name}.eap_user %{name}/%{name}.radius_clients
%doc %{name}/%{name}.vlan %{name}/%{name}.wpa_psk
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sbindir}/%{name}
%{_sbindir}/%{name}_cli
%dir %{_sysconfdir}/%{name}
%{_mandir}/man1/*
%{_mandir}/man8/*
%if 0%{?fedora} || 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif

%files logwatch
%doc %{name}/logwatch/README
%config(noreplace) %{_sysconfdir}/logwatch/conf/services/%{name}.conf
%{_sysconfdir}/logwatch/scripts/services/%{name}

%changelog
* Sat Feb 22 2014 Simone Caronni <negativo17@gmail.com> - 2.1-2
- Re-enable drivers (#1068849).

* Fri Feb 14 2014 John W. Linville <linville@redhat.com> - 2.1-1
- Update to version 2.1 from upstream
- Remove obsolete patch for libnl build documentation

* Mon Feb 03 2014 Simone Caronni <negativo17@gmail.com> - 2.0-6
- Add libnl build documentation and switch libnl-devel to libnl3-devel build
  dependency (#1041471).

* Fri Nov 22 2013 John W. Linville <linville@redhat.com> - 2.0-5
- Enable CONFIG_FULL_DYNAMIC_VLAN build option

* Wed Aug 07 2013 Simone Caronni <negativo17@gmail.com> - 2.0-4
- Add EPEL 6 support.
- Remove obsolete EPEL 5 tags.
- Little spec file formatting.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.0-2
- Perl 5.18 rebuild

* Thu May 30 2013 John W. Linville <linville@redhat.com> - 2.0-1
- Update to version 2.0 from upstream
- Convert to use of systemd-rpm macros
- Build with PIE flags

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct  8 2012 John W. Linville <linville@redhat.com> - 1.0-3
- EAP-TLS: Add extra validation for TLS Message Length

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun  8 2012 John W. Linville <linville@redhat.com> - 1.0-1
- Update to version 1.0 from upstream

* Fri Jun  8 2012 John W. Linville <linville@redhat.com> - 0.7.3-9
- Remove hostapd-specific runtime state directory

* Wed Jun  6 2012 John W. Linville <linville@redhat.com> - 0.7.3-8
- Fixup typo in pid file path in hostapd.service

* Wed May 30 2012 John W. Linville <linville@redhat.com> - 0.7.3-7
- Add BuildRequires for systemd-units

* Fri May 25 2012 John W. Linville <linville@redhat.com> - 0.7.3-6
- Fixup typo in configuration file path in hostapd.service
- Tighten-up default permissions for hostapd.conf

* Tue Feb 28 2012 Jon Ciesla <limburgher@gmail.com> - 0.7.3-5
- Migrate to systemd, BZ 770310.

* Wed Jan 18 2012 John W. Linville <linville@redhat.com> - 0.7.3-4
- Add reference to sample hostapd.conf in the default installed version
- Include README-WPS from the hostapd distribution as part of the docs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 John W. Linville <linville@redhat.com> - 0.7.3-1
- Update to version 0.7.3

* Wed Nov 24 2010 John W. Linville <linville@redhat.com> - 0.6.10-3
- Use ghost directive for /var/run/hostapd
- Remove some rpmlint warnings

* Thu May 27 2010 John W. Linville <linville@redhat.com> - 0.6.10-2
- Move DTIM period configuration into Beacon set operation

* Mon May 10 2010 John W. Linville <linville@redhat.com> - 0.6.10-1
- Update to version 0.6.10

* Tue Jan 19 2010 John W. Linville <linville@redhat.com> - 0.6.9-8
- Do not compress man pages manually in spec file
- Correct date of previous changelog entry

* Thu Jan 14 2010 John W. Linville <linville@redhat.com> - 0.6.9-7
- Enable 802.11n support

* Thu Dec 17 2009 John W. Linville <linville@redhat.com> - 0.6.9-6
- Enable RADIUS server
- Enable "wired" and "none" drivers
- Use BSD license option

* Wed Dec 16 2009 John W. Linville <linville@redhat.com> - 0.6.9-5
- Use openssl instead of gnutls (broken)

* Wed Dec 16 2009 John W. Linville <linville@redhat.com> - 0.6.9-4
- Remove wired.conf from doc (not in chosen configuration)
- Use $RPM_OPT_FLAGS
- Add dist tag

* Wed Dec 16 2009 John W. Linville <linville@redhat.com> - 0.6.9-3
- Use gnutls instead of openssl
- Turn-off internal EAP server (broken w/ gnutls)
- Remove doc files not applicable to chosen configuration
- Un-mangle README filename for logwatch sub-package

* Wed Dec 16 2009 John W. Linville <linville@redhat.com> - 0.6.9-2
- Initial build
- Start release at 2 to avoid conflicts w/ previous attempts by others
