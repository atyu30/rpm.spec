Name: coreseek
Version: 4.1b
Release: 1%{?dist}
Summary: 支持中文全文检索的Sphinx定制版本
Group:   System Environment/Daemons
License: GPLv2
URL:     http://www.coreseek.cn/
Source0: csft-4.1.tar.gz
#Patch0: sphinxexpr.cpp-csft-4.1-beta.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: mmseg
Requires: mysql-devel
Requires: libxml2-devel
Requires: expat-devel
Requires: python-devel

Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(postun): initscripts

%description
支持中文全文检索的Sphinx定制版本

%prep
%setup -q -n csft-4.1
#%patch0 -p1

%build
sh buildconf.sh
./configure --prefix=/usr/local/coreseek --without-unixodbc --with-mmseg --with-mmseg-includes=/usr/local/mmseg/include/mmseg/ --with-mmseg-libs=/usr/local/mmseg/lib/ --with-mysql --with-python
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
mv $RPM_BUILD_ROOT/usr/local/coreseek/etc/sphinx.conf.dist $RPM_BUILD_ROOT/usr/local/coreseek/etc/sphinx.conf
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
cp /etc/init.d/searchd $RPM_BUILD_ROOT%{_initrddir}/

%clean
/bin/rm -rf $RPM_BUILD_ROOT
/bin/rm -rf $RPM_BUILD_DIR/%{name}-%{version}

%files
%defattr(-,root,root)

%attr(0755, root, root) %{_initrddir}/
%config(noreplace) /usr/local/coreseek/etc/sphinx.conf
/usr/local/coreseek/etc/example.sql
/usr/local/coreseek/etc/sphinx-min.conf.dist

%dir
/usr/local/coreseek/bin
/usr/local/coreseek/share
%attr(-, sphinx, root) /usr/local/coreseek/var

%preun
if [ $1 -eq 0 ] ; then
    /sbin/service searchd stop >/dev/null 2>&1
    /sbin/chkconfig --del searchd
fi

%post
cat /etc/passwd |grep -q '^sphinx:'
if (( $? != 0 )); then
    /usr/sbin/groupadd -g 495 sphinx &>/dev/null
    /usr/sbin/useradd -g 495 -u 495 -m -c 'Sphinx Search' -d /var/lib/sphinx -s /sbin/nologin www &>/dev/null
fi
/sbin/chkconfig --add searchd

%changelog
* Sun May 4 2014 Purple Grape <purplegrape4@gmail.com> 3.2.14
- fresh build 3.2.14
