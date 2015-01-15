Summary: HTML pages thumbnailer
Name: gnome-web-photo
Version: 0.10.2
Release: 1%{?dist}
License: LGPLv2+
Group: Applications/Internet
URL: http://download.gnome.org/sources/gnome-web-photo/0.10/
Source0: http://download.gnome.org/sources/gnome-web-photo/0.10/%{name}-%{version}.tar.xz

BuildRequires: libxml2-devel
BuildRequires: gtk3-devel
BuildRequires: webkitgtk3-devel
BuildRequires: libjpeg-devel
BuildRequires: gettext intltool

%description
gnome-web-photo contains a thumbnailer that will be used by GNOME applications,
including the file manager, to generate screenshots of web pages.

%prep
%setup -q

%build
%configure --with-gtk=3.0
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc ChangeLog AUTHORS README TODO COPYING.README
%{_bindir}/gnome-web-photo
%{_bindir}/gnome-web-print
%{_bindir}/gnome-web-thumbnail
%{_datadir}/gnome-web-photo
%{_datadir}/thumbnailers/gnome-web-photo.thumbnailer

%changelog
* Mon Jul 04 2011 Bastien Nocera <bnocera@redhat.com> 0.10.2-1
- Update to 0.10.2

* Mon Apr  4 2011 Christopher Aillon <caillon@redhat.com> 0.10.1-1
- Update to 0.10.1

* Wed Mar 09 2011 Bastien Nocera <bnocera@redhat.com> 0.10-2
- Bump release, -1 was already built using the wrong target

* Wed Mar 09 2011 Bastien Nocera <bnocera@redhat.com> 0.10-1
- Update to 0.10

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jun 23 2010 Jan Horak <jhorak@redhat.com> - 0.9-10
- Rebuild against newer gecko

* Mon Apr 12 2010 Martin Stransky <stransky@redhat.com> - 0.9-9
- Updated gecko dependency

* Sun Apr 04 2010 Caolán McNamara <caolanm@redhat.com> - 0.9-8
- Rebuild against newer gecko

* Fri Mar 26 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.9-7
- fix implicit linking causing FTBFS with the new ld in F13+

* Tue Mar 23 2010 Jan Horak <jhorak@redhat.com> - 0.9-6
- Rebuild against newer gecko

* Fri Feb 26 2010 Matthias Clasen <mclasen@redhat.com> - 0.9-5
- Rebuild

* Thu Nov 26 2009 Jan Horak <jhorak@redhat.com> - 0.9-4
- Rebuild against newer gecko

* Thu Nov 05 2009 Jan Horak <jhorak@redhat.com> - 0.9-3
- Rebuild against newer gecko

* Tue Oct 27 2009 Jan Horak <jhorak@redhat.com> - 0.9-2
- Rebuild against newer gecko

* Wed Sep 23 2009 Matthias Clasen <mclasen@redhat.com> - 0.9-1
- Update to 0.9

* Fri Sep 11 2009 Jan Horak <jhorak@redhat.com> - 0.8-6
- Rebuild against newer gecko

* Thu Aug 06 2009 Jan Horak <jhorak@redhat.com> - 0.8-5
- Rebuild against newer gecko

* Tue Aug 04 2009 Jan Horak <jhorak@redhat.com> - 0.8-4
- Rebuild against newer gecko

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Jan Horak <jhorak@redhat.com> - 0.8-2
- Rebuild against newer gecko

* Tue Jun 30 2009 Matthias Clasen <mclasen@redhat.com> - 0.8-1
- Update to 0.8

* Mon Apr 27 2009 Christopher Aillon <caillon@redhat.com> - 0.7-2
- Rebuild against newer gecko

* Mon Apr 13 2009 Matthias Clasen <mclasen@redhat.com> - 0.7-1
- Update to 0.7

* Tue Mar 24 2009 Jan Horak <jhorak@redhat.com> - 0.6-2
- Fix for rebuild against newer gecko

* Tue Mar 17 2009 Matthias Clasen <mclasen@redhat.com> - 0.6-1
- Update to 0.6

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 06 2009 Christopher Aillon <caillon@redhat.com> - 0.3-13
- Rebuild against newer gecko

* Wed Nov 12 2008 Christopher Aillon <caillon@redhat.com> - 0.3-12
- Rebuild against newer gecko

* Wed Mar 12 2008 Marco Pesenti Gritti <mpg@redhat.com> - 0.3-11
- Better xulrunner-1.9 patch which also works with very long pages

* Fri Mar  7 2008 Marco Pesenti Gritti <mpg@redhat.com> - 0.3-10
- Add patch to make it work with xulrunner 1.9

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.3-9
- Autorebuild for GCC 4.3

* Tue Nov 27 2007 Christopher Aillon <caillon@redhat.com> - 0.3-8
- Rebuild against newer gecko

* Fri Nov 23 2007 - Bastien Nocera <bnocera@redhat.com> - 0.3-7
- Rebuilding against xulrunner will require a lot of porting,
  disable for now

* Fri Nov 16 2007 - Bastien Nocera <bnocera@redhat.com> - 0.3-6
- Try to rebuild with xulrunner

* Thu Oct 25 2007 - Bastien Nocera <bnocera@redhat.com> - 0.3-5
- Rebuild for new Gecko, tighten dependencies

* Mon Sep 10 2007 - Bastien Nocera <bnocera@redhat.com> - 0.3-4
- Fix license, as mentioned by Kevin Fenzi

* Thu Sep 06 2007 - Bastien Nocera <bnocera@redhat.com> - 0.3-3
- Update following Matthias Clasen's comments

* Wed Sep 05 2007 - Bastien Nocera <bnocera@redhat.com> - 0.3-2
- Update following Peter Gordon's comments

* Tue Mar 20 2007 - Bastien Nocera <bnocera@redhat.com> - 0.3-1
- First post!

