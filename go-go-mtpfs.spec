#
# spec file for package go-go-mtpfs
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           go-go-mtpfs
Version:        0.0.0+git20131015.bb3f0c2
Release:        1.4
Summary:        Mount MTP devices over FUSE
Group:          Productivity/Multimedia/Sound/Players
License:        BSD-3-Clause
Url:            https://github.com/hanwen/go-mtpfs
Source:         go-mtpfs-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  go-devel
BuildRequires:  go-go-fuse
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(libmtp)
BuildRequires:  pkgconfig(libusb-1.0)
%if 0%{?suse_version} >= 1100
Recommends:     %{name}-doc
%endif
Provides:       go-mtpfs = 0.0+git6b55d1f9
Obsoletes:      go-mtpfs < 0.0+git6b55d1f9
%{go_requires}
%{go_provides}

%description
Go-mtpfs is a simple FUSE filesystem for mounting Android devices as a
MTP device.

It will expose all storage areas of a device in the mount, and only
reads file metadata as needed, making it mount quickly. It uses
Android extensions to read/write partial data, so manipulating large
files requires no extra space in /tmp.

It has been tested on various flagship devices (Galaxy Nexus, Xoom,
Nexus 7).  As of Jan. 2013, it uses a pure Go implementation of MTP,
which is based on libusb.

%package doc
Summary:        API documenation
Group:          Documentation/Other
Requires:       %{name} = %{version}

%description doc
API, examples and documentation.

%prep
%setup -q -n go-mtpfs-%{version}

%build
%goprep github.com/hanwen/go-mtpfs
%gobuild 

%install
%goinstall
%godoc

%files
%defattr(-,root,root,-)
%doc README LICENSE
%{_bindir}/go-mtpfs
%{go_contribdir}/*

%files doc
%defattr(-,root,root,-)
%{go_contribsrcdir}/*

%changelog
* Mon Nov 11 2013 speilicke@suse.com
- Update to 0.0.0+git20131015.bb3f0c2:
  + No changelog
* Mon Jul  1 2013 graham@andtech.eu
- patch fuse API call for newer go-fuse package
- fs: fix DefaultFile/Node snafu.
- Update for fuse.NewServer API.
- Update for fuse/nodefs API change.
- Update for FsNode API changes.
- Update for fuse.File API changes.
- Update for go-fuse SetDebug API change.
- Ignore transfer size for reads, since it may be truncated for > 4G reads.
- fs: per-storage StatFs data.
* Mon May  6 2013 vdziewiecki@suse.com
- go-mtpfs should be executable so that one can use it.
* Mon Mar 18 2013 graham@andtech.eu
- Update to latest git (3383d4fc 03.03.13)
* Sat Sep 22 2012 toddrme2178@gmail.com
- Initial spec file
