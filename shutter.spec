Name:		shutter
Version:	0.91
Release:	2%{?dist}
Summary:	GTK+ 2.0 screenshot application written in perl
Group:		Applications/Multimedia
License:	GPLv3+
URL:		http://shutter-project.org
Source0:	http://shutter-project.org/wp-content/uploads/releases/tars/%{name}-%{version}.tar.gz
#BuildArch:	noarch
BuildRequires:	desktop-file-utils
Requires:	gnome-web-photo
Requires:	perl(Gtk2::ImageView)
Requires:	perl(X11::Protocol::Ext::XFIXES)
Requires:	nautilus-sendto
Requires:	hicolor-icon-theme
Requires:	perl(Gtk2::Unique)

Requires:   perl(Image::ExifTool)
Requires:   perl(Goo::Canvas)
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?filter_setup:
%filter_provides_in %{_datadir}/%{name}/resources/system/upload_plugins
%filter_setup
}

%description
Shutter is a GTK+ 2.0 screenshot application written in perl.
Shutter covers all features of common command line tools like
scrot or import and adds reasonable new features combined
with a comfortable GUI using the GTK+ 2.0 framework


%prep
%setup -q -n %{name}-%{version}
rm -vr share/doc/
# Remove the bundled perl(X11::Protocol::Ext::XFIXES)
rm -vr share/%{name}/resources/modules/X11

%build

%install
# executable and data
install -d -m 0755 -p $RPM_BUILD_ROOT%{_bindir}
install -d -m 0755 -p $RPM_BUILD_ROOT%{_datadir}
install -d -m 0755 -p $RPM_BUILD_ROOT%{perl_vendorlib}
cp -pfr bin/* $RPM_BUILD_ROOT%{_bindir}/
cp -pfr share/* $RPM_BUILD_ROOT%{_datadir}/
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/resources/modules/* \
   $RPM_BUILD_ROOT%{perl_vendorlib}
rmdir $RPM_BUILD_ROOT%{_datadir}/%{name}/resources/modules/

desktop-file-install --delete-original \
  --dir ${RPM_BUILD_ROOT}%{_datadir}/applications \
  ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop

%find_lang %{name}
%find_lang %{name}-plugins
cat %{name}-plugins.lang >> %{name}.lang
%find_lang %{name}-upload-plugins
cat %{name}-upload-plugins.lang >> %{name}.lang

%post
update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%doc CHANGES README COPYING
%{_bindir}/%{name}
%{perl_vendorlib}/Shutter/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}
%{_mandir}/man1/%{name}*
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/*/apps/*.*
%{_datadir}/icons/HighContrast/
%{_datadir}/icons/ubuntu-mono-*/*/apps/%{name}-panel.*

%changelog
* Thu Sep 26 2013 Robin Lee <cheeselee@fedoraproject.org> - 0.90.1-1
- Update to 0.90.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.90-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.90-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 19 2012 Robin Lee <cheeselee@fedoraproject.org> - 0.90-1
- Update to 0.90

* Mon Aug 20 2012 Robin Lee <cheeselee@fedoraproject.org> - 0.89.1-2
- Remove the bundled perl(X11::Protocol::Ext::XFIXES)

* Thu Aug 16 2012 Robin Lee <cheeselee@fedoraproject.org> - 0.89.1-1
- Update to 0.89.1
- Remove the patch for desktop entry file
- Filtered fake provides
- Add Perl MODULE_COMPAT requires
- Requires perl(X11::Protocol::Ext::XFIXES)
- Don't remove the executable bit of the upload plugins

* Fri Aug 10 2012 Robin Lee <cheeselee@fedoraproject.org> - 0.89-1
- Update to 0.89 (#722700, #753423, #659378, #759686, #754880)
- License changed to GPLv3+
- Patch updated
- Perl modules moved to %%{perl_vendorlib}
- Scriptlet updated
- Other cleanup

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.87.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.87.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Sep 11 2011 Liang Suilong <liangsuilong@gmail.com> - 0.87.3-1
- Upgrade to shutter-0.87.3

* Sat Jun 4 2011 Liang Suilong <liangsuilong@gmail.com> - 0.87.2-1
- Upgrade to shutter-0.87.2
- Add BR: perl(Gtk2::Unique)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.86.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Sep 13 2010 Liang Suilong <liangsuilong@gmail.com> - 0.86.4-1
- Upgrade to shutter-0.86.2
- Add icons for new version

* Thu May 06 2010 Liang Suilong <liangsuilong@gmail.com> - 0.86.2-1
- Upgrade to shutter-0.86.2
- Add BR: hicolor-icon-theme

* Mon Apr 19 2010 Liang Suilong <liangsuilong@gmail.com> - 0.86.1-1
- Upgrade to shutter-0.86.1

* Tue Mar 2 2010 Liang Suilong <liangsuilong@gmail.com> - 0.85.1-2
- Remove BR:gtklp
- fix the bug of directory ownership

* Mon Dec 7 2009 Liang Suilong <liangsuilong@gmail.com> - 0.85.1-1
- Upgrade to shutter-0.85.1

* Sat Nov 21 2009 Liang Suilong <liangsuilong@gmail.com> - 0.85-1
- Upgrade to shutter-0.85

* Mon Aug 3 2009 Liang Suilong <liangsuilong@gmail.com> - 0.80.1-1
- Updrade to shutter-0.80.1

* Mon Aug 3 2009 Liang Suilong <liangsuilong@gmail.com> - 0.80-5
- Update %%install script

* Wed Jul 29 2009 Liang Suilong <liangsuilong@gmail.com> - 0.80-4
- Update %%install script

* Mon Jul 20 2009 Liang Suilong <liangsuilong@gmail.com> - 0.80-3
- Add perl(X11::Protocol) as require

* Thu Jun 25 2009 Liang Suilong <liangsuilong@gmail.com> - 0.80-2
- Upstream to shutter-0.80 Final GA

* Thu Jun 25 2009 Liang Suilong <liangsuilong@gmail.com> - 0.80-1.ppa6
- Upstream to shutter-0.80~ppa6
- Update the SPEC file

* Thu Jun 25 2009 Liang Suilong <liangsuilong@gmail.com> - 0.70.2-3.ppa4
- Remove share/shutter/resources/pofiles/
- Remove share/shutter/resources/modules/File
- Remove share/shutter/resources/pofiles/Proc

* Wed Apr 15 2009 Liang Suilong <liangsuilong@gmail.com> - 0.70.2-2.ppa4
- Add a desktop-file-utils as BuildRequires

* Wed Apr 15 2009 Liang Suilong <liangsuilong@gmail.com> - 0.70.2-2.ppa3
- Add a desktop-file-utils as BuildRequires

* Sun Jan 18 2009 Liang Suilong <liangsuilong@gmail.com> - 0.70.2-1
- Upstream to 0.70.2

* Sun Jan 18 2009 Liang Suilong <liangsuilong@gmail.com> - 0.70.1-1
- Upstream to 0.70.1

* Sun Jan 18 2009 Liang Suilong <liangsuilong@gmail.com> - 0.70-1
- Upstream to 0.70

* Sun Jan 18 2009 Liang Suilong <liangsuilong@gmail.com> - 0.64-2
- Add several Requires so that advanced functions can run.
- Fix the authoritie of install path.

* Fri Jan 02 2009 bbbush <bbbush.yuan@gmail.com> - 0.64-1
- update to 0.64, clean up spec

* Mon Dec 29 2008 Liang Suilong <liangsuilong@gmail.com> - 0.63-3
- Initial package for Fedora
