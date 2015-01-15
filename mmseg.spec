Name: mmseg
Version: 3.2.14
Release: 1%{?dist}
Summary: A Word Identification System for Mandarin Chinese Text Based on Two Variants of the Maximum Matching Algorithm
Group:   System Environment/Daemons
License: Free for noncommercial use
URL:     http://www.coreseek.cn/opensource/mmseg/
Source0: http://www.coreseek.cn/uploads/csft/3.2/mmseg-3.2.14.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
A Word Identification System for Mandarin Chinese Text Based on Two Variants of the Maximum Matching Algorithm

%prep
%setup -q -n %{name}-%{version}

%build
./bootstrap
./configure --prefix=/usr/local/mmseg
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
/bin/rm -rf $RPM_BUILD_ROOT
/bin/rm -rf $RPM_BUILD_DIR/%{name}-%{version}

%files
%defattr(-,root,root)
%dir
/usr/local/mmseg

%changelog
* Fri Jun 13 2014 Atyu30 <ipostfix@gmail.com> - 3.2.14
- Ver. 3.2.14 for RHEL7

