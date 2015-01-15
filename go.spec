#
# spec file for package go
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
# Copyright (c) 2011, Sascha Peilicke <saschpe@gmx.de>
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

%global debug_package %{nil}
Name:           go
Version:        1.1.2
Release:        105.1
Summary:        A compiled, garbage-collected, concurrent programming language
License:        BSD-3-Clause
Group:          Development/Languages/Other
Url:            http://golang.org
Source0:        http://go.googlecode.com/files/go%{version}.src.tar.gz
Source1:        rpmlintrc
Source2:        go.sh
Source3:        macros.go
Source4:        godoc.service
Source6:        go-wiki-gadget.xml
Source5:        README-openSUSE
# PATCH-FIX-OPENSUSE adjust documentation paths for API/doc server
Patch1:         godoc-path-locations.patch
# PATCH-FIX-OPENSUSE add -s flag to 'go install' (don't rebuild/install std libs)
Patch3:         go-build-dont-reinstall-stdlibs.patch
# PATCH-FIX-OPENSUSE re-enable build binary only packages (we are binary distro)
# see http://code.google.com/p/go/issues/detail?id=2775 & also issue 3268
Patch4:         allow-binary-only-packages.patch
#PATCH-FIX-OPENSUSE use -x verbose build output for qemu-arm builders
Patch5:         verbose-build.patch
# PATCH-FIX-OPENSUSE BNC#776058
Patch6:         go-install-dont-reinstall-stdlibs.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  rpm
%if 0%{?suse_version} >= 1210
BuildRequires:  mercurial
BuildRequires:  systemd
%endif
%if 0%{?suse_version} >= 1100
BuildRequires:  fdupes
Recommends:     go-doc
#BNC#818502 debug edit tool of rpm fails on i586 builds
%if 0%{?suse_version} > 1230
BuildRequires:  rpm >= 4.11.1
%endif
%endif
Provides:       go-devel = %{name}%{version}
Provides:       go-devel-static = %{name}%{version}
Obsoletes:      go-devel < %{name}%{version}
ExclusiveArch:  %ix86 x86_64 %arm
# For godoc service
%if 0%{?suse_version} >= 1210
%systemd_requires
%endif

%description
Go is an expressive, concurrent, garbage collected systems programming language
that is type safe and memory safe. It has pointers but no pointer arithmetic.
Go has fast builds, clean syntax, garbage collection, methods for any type, and
run-time reflection. It feels like a dynamic language but has the speed and
safety of a static language.

%package doc
Summary:        Go documentation
Group:          Documentation/Other
Requires:       %{name} = %{version}

%description doc
Go examples and documentation.

%package vim
Summary:        Go syntax files for Vim
Group:          Productivity/Text/Editors
Requires:       %{name} = %{version}

%description vim
Vim syntax highlighting scheme for the Go programming language.

%package emacs
Summary:        Go language syntax files for Emacs
Group:          Productivity/Text/Editors
Requires:       %{name} = %{version}

%description emacs
Emacs syntax highlighting scheme for the Go programming language.

%prep
%setup -q -n %{name}
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
cp %{SOURCE4} .
cp %{SOURCE5} .

# setup go_arch (BSD-like scheme)
%ifarch %ix86
sed -i 's|GOARCH|386|' %{SOURCE3}
%define go_arch 386
%endif
%ifarch x86_64
sed -i 's|GOARCH|amd64|' %{SOURCE3}
%define go_arch amd64
%endif
%ifarch %arm
sed -i 's|GOARCH|arm|' %{SOURCE3}
%define go_arch arm
%endif

%build
export GOROOT="`pwd`"
export GOROOT_FINAL=%{_libdir}/go
export GOBIN="$GOROOT/bin"
mkdir -p "$GOBIN"
cd src
HOST_EXTRA_CFLAGS="%{optflags} -Wno-error" ./make.bash

%ifarch x86_64
# Install race detection version of std libraries (amd64 only)
cd ../
bin/go install -race std
%endif
%ifarch %ix86
strip $GOBIN/go $GOBIN/godoc # bnc#818502
%endif

%install
export GOROOT="%{buildroot}%{_libdir}/%{name}"
# bash completion seems broken
#install -Dm644 misc/bash/go %%{buildroot}%%{_sysconfdir}/bash_completion.d/go.sh
install -Dm644 %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d/go.sh
install -Dm644 misc/emacs/go-mode-load.el %{buildroot}%{_datadir}/emacs/site-lisp/go-mode-load.el
install -Dm644 misc/emacs/go-mode.el %{buildroot}%{_datadir}/emacs/site-lisp/go-mode.el
install -Dm644 misc/vim/autoload/go/complete.vim %{buildroot}%{_datadir}/vim/site/autoload/go/complete.vim
install -d %{buildroot}%{_datadir}/vim/site/ftplugin/go
install -Dm644 misc/vim/ftplugin/go/{fmt,import}.vim %{buildroot}%{_datadir}/vim/site/ftplugin/go/
install -Dm644 misc/vim/indent/go.vim %{buildroot}%{_datadir}/vim/site/indent/go.vim
install -Dm644 misc/vim/plugin/godoc.vim %{buildroot}%{_datadir}/vim/site/plugin/godoc.vim
install -Dm644 misc/vim/syntax/godoc.vim %{buildroot}%{_datadir}/vim/site/syntax/godoc.vim
install -Dm644 misc/vim/syntax/go.vim %{buildroot}%{_datadir}/vim/site/syntax/go.vim
install -Dm644 misc/vim/ftdetect/gofiletype.vim %{buildroot}%{_datadir}/vim/site/ftdetect/gofiletype.vim

# locations for third party libraries, see README-openSUSE for info about locations.
install -d  %{buildroot}%{_libdir}/go/contrib/pkg/linux_%{go_arch}
install -d  %{buildroot}%{_datadir}/go/contrib/src/pkg
install -d  %{buildroot}%{_datadir}/go/contrib/src/cmd
install -Dm644 README-openSUSE %{buildroot}%{_libdir}/go/contrib/
ln -s %{_libdir}/go/contrib/README-openSUSE %{buildroot}%{_datadir}/go/contrib/README-openSUSE

# godoc service
mkdir -p %{buildroot}%{_unitdir}
install -Dm644 godoc.service %{buildroot}%{_unitdir}/godoc.service

# source files for go install, godoc, etc
install -d %{buildroot}%{_datadir}/go
for ext in *.{go,c,h,s,S,py}; do
  find src -name ${ext} -exec install -Dm644 \{\} %{buildroot}%{_datadir}/go/\{\} \;
done
mkdir -p $GOROOT/src
ln -s /usr/share/go/src/pkg $GOROOT/src/pkg
ln -s /usr/share/go/src/cmd $GOROOT/src/cmd

# copy document templates, packages, obj libs and command utilities
mkdir -p %{buildroot}%{_bindir}
mkdir -p $GOROOT/lib
cp -ar lib/godoc $GOROOT/lib
mv pkg $GOROOT
mv bin/* %{buildroot}%{_bindir}
rm -f %{buildroot}%{_bindir}/{hgpatch,quietgcc}

# documentation and examples
# fix documetation permissions (rpmlint warning)
find doc/ misc/ -type f -exec chmod 0644 '{}' \;
# remove unwanted arch-dependant binaries (rpmlint warning)
rm -rf misc/cgo/test/{_*,*.o,*.out,*.6,*.8}
rm -f misc/dashboard/builder/{gobuilder,*6,*.8}
rm -f misc/goplay/{goplay,*.6,*.8}
rm -rf misc/windows
rm -rf misc/cgo/test/{_*,*.o,*.out,*.6,*.8}
# remove kate syntax file, it is shipped with libktexteditor already
rm -f misc/kate/go.xml

# install RPM macros ($GOARCH prepared in %%prep section)
install -Dm644 %{SOURCE3} %{buildroot}%{_sysconfdir}/rpm/macros.go

# break hard links
rm %{buildroot}%{_libdir}/go/pkg/linux_%{go_arch}/{cgocall,runtime}.h
ln -s %{_datadir}/go/src/pkg/runtime/{cgocall,runtime}.h %{buildroot}%{_libdir}/go/pkg/linux_%{go_arch}/

# Disable brp-strip-static-archive breaks build
%define __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib/rpm/[^/]*/?brp-strip-static-archive %{__strip}!!g')

%if 0%{?suse_version} >= 1100
%fdupes %{buildroot}%{_prefix}
%endif

%pre
%if 0%{?suse_version} >= 1210
%service_add_pre godoc.service
%endif

%post
%if 0%{?suse_version} >= 1210
%service_add_post godoc.service
%endif

%preun
%if 0%{?suse_version} >= 1210
%service_del_preun godoc.service
%endif

%postun
%if 0%{?suse_version} >= 1210
%service_del_postun godoc.service
%endif

%files
%defattr(-,root,root,-)
%doc AUTHORS CONTRIBUTORS LICENSE PATENTS README README-openSUSE
%ifarch %ix86
%{_libdir}/go/pkg/tool/linux_%{go_arch}/8*
%endif
%ifarch x86_64
%{_libdir}/go/pkg/tool/linux_%{go_arch}/6*
%endif
%ifarch %arm
%{_libdir}/go/pkg/tool/linux_%{go_arch}/5*
%endif
%{_datadir}/go/
%{_bindir}/go*
%{_libdir}/go/
# bash completion seems broken
#%%config %{_sysconfdir}/bash_completion.d/go.sh
%config %{_sysconfdir}/profile.d/go.sh
%config %{_sysconfdir}/rpm/macros.go
%if 0%{?suse_version} >= 1210 || 0%{?fedora} >= 16
%{_unitdir}/godoc.service
%endif

%files doc
%defattr(-,root,root,-)
%doc doc

%files vim
%defattr(-,root,root,-)
%dir %{_datadir}/vim
%{_datadir}/vim/*

%files emacs
%defattr(-,root,root,-)
%{_datadir}/emacs/site-lisp/go-mode*

%changelog
* Wed Aug 14 2013 speilicke@suse.com
- Fix Factory i586 build failure by stripping binaries earlier.
* Tue Aug 13 2013 speilicke@suse.com
- Rework %%go_prep again, use "shopt -s dotglob" to catch hidden files
- Change %%go_requires to "Require: go >= %%go_ver" instead of
  "Require: go-devel = %%go_ver". Go follows a stable release policy which
  means patch-level updates are (supposed to be) compatible.
* Tue Aug 13 2013 speilicke@suse.com
- Update to version 1.1.2:
  + includes fixes to the gc compiler and cgo, and the bufio, runtime, syscall,
    and time packages. See the change history for details. If you use package
    syscall's Getrlimit and Setrlimit functions under Linux on the ARM or 386
    architectures, please note change 55ac276af5a7 that fixes issue 5949.
- Fix %%go_prep again: Also move hidden files (.$BLA)
* Tue Aug 13 2013 speilicke@suse.com
- Also set ExclusiveArch in %%go_requires macro. Allows to drop
  %%go_exclusivearch again
- Fix %%go_prep macro: Find directories in %%_builddir based on Go
  package name prefix (not exact match).
* Tue Aug 13 2013 speilicke@suse.com
- Fix URL
- Add %%go_exclusivearch macro. It's better to only specify ExclusiveArch
  in the "go" package instead of all Go packages. Avoids errors once
  Go becomes available on more architectures
* Wed Jul 10 2013 graham@andtech.eu
- Fix godoc path locations patch
* Thu Jun 13 2013 graham@andtech.eu
- Update to Go 1.1.1
- cmd/gc: compute initialization order for top-level blank vars
- cmd/gc: save local var list before inlining
- cmd/gc: fix missing slice/array types in export data.
- runtime: fix heap corruption during GC
- runtime: zeroize g->fnstart to not prevent GC of the closure.
- cmd/gc: repair make(T) in export data for inlining.i
- runtime: fix GC scanning of slices
- cmd/gc: do not corrupt init() with initializers of _ in closures.
- runtime: introduce cnewarray() to simplify allocation of typed
  arrays.
* Tue May 14 2013 graham@andtech.eu
- Package changes
  - macros.go: update go version macro to cut trailing characters
    added by new style of "go version" identifier string
  - Update openSUSE specific patches to cleanly apply against Go 1.1
- Update package source and version to Go 1.1
- Full release notes for Go 1.1 can be found online here:
  http://golang.org/doc/go1.1
- There are too many bug fixes to list individually; details of all
  bugs fixed can be found on the issue tracker tagged with Go1.1
  http://code.google.com/p/go/issues/list?can=1&q=label%%3AGo1.1
- Language changes which may affect your existing programmes
  - Integer division by zero: http://golang.org/doc/go1.1#divzero
  - Surrogates in unicode literals: http://golang.org/doc/go1.1#unicode_literals
  - Method values: http://golang.org/doc/go1.1#method_values
  - Return requirements: http://golang.org/doc/go1.1#return
- The majority of improvements in this release are performance related
  with optimizations in the compiler and linker, garbage collection,
  goroutine scheduler, map/hashmap implementation and numerous speedups
  in the standard library. Please see the full release notes for details.
- One noteworthy addition to the toolchain is the addition of a race
  detector. This should help improve the memory safety and accuracy of
  your concurrent Go programmes. Race detection versions of the standard
  library are included in this package update. You can find instructions
  for building librarys and programmes with race detection in the manual:
  http://golang.org/doc/articles/race_detector.html
* Fri Mar 22 2013 hrvoje.senjan@gmail.com
- Drop the go-kate package, the syntax is already shipped with
  libktexteditor package
* Tue Nov  6 2012 saschpe@suse.de
- Remove misc documentation. It doesn't contain anything really useful
  and several files are found in other (sub-)packages (bnc#788344)
* Mon Oct  1 2012 saschpe@suse.de
- Update to version 1.0.3:
  - Improved documentation
  - List of fixed issues:
    https://groups.google.com/forum/#!topic/golang-nuts/co3SvXbGrNk
  - More details can be found on this full list of changes:
    http://code.google.com/p/go/source/list?name=release-branch.go1
- Removed:
  - opensuse-vim.patch, merged upstream
  - Fix for bnc#686557, offending pdf was removed upstream
* Wed Sep  5 2012 graham@andtech.eu
- BNC#776058
  - Add new patch to prevent the go install tool trying to reinstall
  std library packages that are dependencies of third party packages.
  - Using touch on the precompiled archives introdoces additional
  problems with the go install tool. Instead, we simply don't mark
  std library files as stale when a third party package is evaluated
  for installation. The behaviour remains unchanged for the root
  user and while it is inadvisable to manually reinstall standard
  libraries using the openSUSE packages, we do not disallow it.
- Spec changes
  - Remove redundant requires for ed/bison
  - Minor tweaks for cross distro builds based on FC/Mageia/Mandriva
- Macro changes
  - Tweak the BRP strip macro to work on RHEL based distros
- Add go-wiki xml widget
* Thu Aug 16 2012 graham@andtech.eu
- BNC#776058
- spec changes, reverse positions of compiled items and package
  source in the %%install section. touch compiled package archives
  after source is installed for go-doc, this prevents the go tool
  trying to re-compile/install std libraries.
* Tue Aug 14 2012 graham@andtech.eu
- Patch vim Godoc and Import plugins.
- Update spec file.
  - Instead of using tarball generated from a repo checkout, switch
    tarball source and use upstream official tarball.
  - Remove dependance on VERSION file, make spec more robust for
    future updates.
* Mon Jul 16 2012 graham@andtech.eu
- remove unavailable -x verbose flag from go fix macro
* Thu Jun 14 2012 agraf@suse.com
- fix some qemu-arm compilation errors by passing -x to go always
* Thu Jun 14 2012 graham@andtech.eu
- Update to bugfix release 1.0.2
- This fixes two major bugs:
  3695 runtime: computed hash value for struct map key ignores
  some fields
  3573 runtime: use of large map key causes crash
- Additionally, this fixes numerous smaller documentation and code
  fixes, details can be found on this full list of changes:
  http://code.google.com/p/go/source/list?name=release-branch.go1
* Tue Jun  5 2012 saschpe@suse.de
- Some Fedora_16 build fixes (i.e. added suse macros)
* Tue Jun  5 2012 graham@andtech.eu
- Fix build time path locations in macros.go for packages that
  depend on other Go packages.
* Tue May 29 2012 agraf@suse.com
- enable verbose build (fixes compilation for ARM? O_o)
* Tue May 29 2012 dmueller@suse.com
- fix build for ARM
* Wed May  9 2012 graham@andtech.eu
- Update to version 1.0.1
- fix escape analysis bug that could cause memory corruption
- other minor updates see:
  http://code.google.com/p/go/source/list?name=release-branch.go1
- go.spec: remove arch dependent conditionals from %%files section
  we don't have to select these anymore.
* Thu Apr  5 2012 graham@andtech.eu
- spec/go.sh/macros
  change install location of third party libs to $GOROOT/contrib
  add $GOROOT/contrib as the last location in users $GOPATH
- re-add sachape's typo and version check fixes
- Update godoc patch and add contrib src dir
* Mon Apr  2 2012 graham@andtech.eu
- Add %%godoc macro to help with packaging API docs
* Mon Apr  2 2012 saschpe@suse.de
- Fixed some typos
- Removed checks for outdated SUSE versions
* Mon Apr  2 2012 graham@andtech.eu
- update profile.d go.sh with $GOBIN for users
* Mon Apr  2 2012 graham@andtech.eu
- cmd/go - re-enable building from binary only packages
  we are a binary distro and the last minue change to go clean -i
  disabled building from third party binary packages. package management
  will be done via yast/zypper anyway and not go clean.
* Sat Mar 31 2012 graham@andtech.eu
- change provides to match go release string as per VERSION file
- fix %%pre, %%post etc godoc service statement
* Fri Mar 30 2012 graham@andtech.eu
- Export $GOBIN for the %%gobuild() macro
* Wed Mar 28 2012 graham@andtech.eu
- Go version 1
  http://golang.org/doc/go1.html
* Tue Mar 27 2012 graham@andtech.eu
- Release candidate 2
- Bug fixes and resolved issues
  http://weekly.golang.org/doc/devel/weekly.html#2012-03-22
* Tue Mar 13 2012 graham@andtech.eu
- No language changes
- Initial Go 1 beta offering
- Many bug fixes and resolved issues
  http://weekly.golang.org/doc/devel/weekly.html#2012-03-13
* Sat Mar 10 2012 graham@andtech.eu
- Add additional Go vim scripts, tweak goversion macro
* Fri Mar  9 2012 graham@andtech.eu
- update spec and macro file to provide working requires
* Wed Mar  7 2012 graham@andtech.eu
- update gotest/gofix macro
* Tue Mar  6 2012 graham@andtech.eu
- Update godoc & go build patches
- removed dwarf pretty printer patch
- add godoc systemd service file
* Mon Mar  5 2012 graham@andtech.eu
- Update to weekly.2012-03-04
- Changes to go/build required code refactoring
  see: http://weekly.golang.org/doc/devel/weekly.html#2012-03-04
* Fri Feb 24 2012 graham@andtech.eu
- Wpdate to weekly.2012-02-22
- Some BC breaks and language changes, too many details to list
  see release announcement:
  http://weekly.golang.org/doc/devel/weekly.html#2012-02-22
* Fri Feb 17 2012 graham@andtech.eu
- cmd/gc: fix comparison of struct with _ field
  fixes build of go-go-gtk and other packages that use cgo
* Fri Feb 17 2012 graham@andtech.eu
- Update to tip @ 2012.02017
- sync: say that Cond.Wait can not return spuriously
- runtime: Permit default behaviour of SIGTSTP, SIGTTIN, SIGTTOU
- cmd/gc: correctly typecheck expression lists in returns
- syscall: fix bounds check in Error
* Thu Feb 16 2012 graham@andtech.eu
- Update to weekly.2012-02-12
  http://weekly.golang.org/doc/devel/weekly.html#2012-02-12
* Wed Feb  8 2012 graham@andtech.eu
  This weekly snapshot includes a re-organization of the Go tools.
  Only the go, godoc, and gofmt tools are installed to $GOROOT/bin (or $GOBIN).
  The remainder are installed to $GOROOT/bin/tool.
  This puts the lesser-used tools (6g, cgo, govet, etc.) outside the user PATH.
  Instead these tools may be called through the go tool with 'go tool command'.
  For example, to vet hello.go you would type 'go tool vet hello.go'.
  Type 'go tool' see the list of available tools.
  With the move, some tools were given simpler names:
    6cov    -> cov
    6nm     -> nm
    goapi   -> api
    gofix   -> fix
    gopack  -> pack
    gopprof -> pprof
    govet   -> vet
    goyacc  -> yacc
  The os/signal package has been moved to	exp/signal.
  A new tool named 'dist'	has been introduced to	handle building the gc
  tool chain and to bootstrap the go tool. The old build scripts and make
  files have been removed.
  Full list of changes and fixes available:
  http://weekly.golang.org/doc/devel/weekly.html#2012-02-07
* Mon Feb  6 2012 saschpe@suse.de
- Satisfy Factory-Auto (only comment out %%path, not Patch)
* Sun Feb  5 2012 graham@andtech.eu
- Update to latest tip
- Now use cmd/dist to build toolchain, build scripts are removed
  build process is now as follows.
  build cmd/dist C based bootstrap tool
  - > compile C based compilers and Go based bootstrap tool
  - > compile Go based core commands and libraries
- Remove patch that affects, cmd/go/{build,pkg}.go , this command
  is under active development and building against binary installs
  is slated to be included before Go1 release.
* Tue Jan 31 2012 graham@andtech.eu
- Patch: quick hack to try and get packages building against third
  party libs if they are installed as binary archives without source
- Update some spec file entries for changing $GOROOT layout, mainly
  $GOROOT/bin/go-tools
- Add $GOBIN back for now
* Mon Jan 30 2012 graham@andtech.eu
- spec tweaks, use default locations for go tooling
  (compilers, linkers, cgo etc all in $GOROOT now)
- remove $GOBIN from /etc/profile.d/go.sh
* Fri Jan 27 2012 graham@andtech.eu
- Update to weekly.2012-01-27
- renamed the html package to exp/html
- Many fixes:
  - * http://weekly.golang.org/doc/devel/weekly.html#2012-01-27
* Tue Jan 24 2012 graham@andtech.eu
- Add %%goinstall() macro for new go tool
- Update godoc path locations patch
- Update go install patch (fixes building packages with "go install")
- Update to weekly.2012-01-20
- The image package's Tiled type has been renamed to Repeated.
- The encoding/xml package has been changed to make more idiomatic
  use of struct tags, among other things. If you use the xml package
  please read the change description to see if your code is affected:
  http://code.google.com/p/go/source/detail?r=70e914beb409
- exp/sql package to database/sql
- Package net's SetTimeout methods were changed to SetDeadline.
- Many functions in package os now take a os.FileMode argument instead
  of a plain uint32. An os.ModeSticky constant is also now defined.
- The meaning of the first buffer element for image.YCbCr has changed to
  match the semantics of the other image types like image.RGBA.
- The NewMD5, NewSHA1 and NewSHA256 functions in crypto/hmac have been
  deprecated. Use New instead, explicitly passing the hash function.
* Fri Dec 30 2011 graham@andtech.eu
- Patch new "go install" to allow -s option
  This prevents rebuild/reinstall of std libs and allows packages
  to be installed into a users $GOPATH
* Fri Dec 23 2011 graham@andtech.eu
- Update to weekly.2011.12.22
- changes to the images/ycbcr and testing packages
  * "gofix" required for code using images/ycbr
  * Testing package "B" (benchmark) type now has same methods as "T"
- Compiler inlining: Enabled in .spec as "export GCFLAGS=-l"
  * Needs to be explicitly enabled at compile time with the above
    flag or using the "-l" compiler flag
- Initial implementation of 'go' command utility
- Many fixes and updates
  * http://weekly.golang.org/doc/devel/weekly.html#2011-12-22
* Fri Dec 16 2011 dmueller@suse.de
- fix exclusivearch for %%%%arm
- fix filelist for %%%%arm
* Tue Dec 13 2011 saschpe@suse.de
- Use $GOBIN as install target directory for binaries (Make.cmd)
  regardless of $TARGDIR (Second part of bnc#735320)
* Tue Dec 13 2011 saschpe@suse.de
- Improve macros %%go_make, %%go_make_test and %%go_make_install:
  * Set TARGDIR and GOBIN all macros (bnc#735320)
  * Make sure %%{buildroot}%%{_bindir} exists in any case
- The above should simplify spec files for Go packages that use, .e.g.,
  'make tools' to install additional stuff (like binaries)
* Wed Dec  7 2011 dmacvicar@suse.de
- Set GOBIN correctly in Make.inc to point to _bindir instead
  of GOROOT/bin (bnc#735288)
* Mon Dec  5 2011 saschpe@suse.de
- Forgot to update VERSION file
* Mon Dec  5 2011 saschpe@suse.de
- Update to 05/12/2011 mercurial version:
  * No big changes
* Fri Dec  2 2011 saschpe@suse.de
- Update to r60.3 + weekly.2011-12-02:
  * crypto/tls: cleanup certificate load on windows
  * exp/ssh: add Std{in,out,err}Pipe methods to Session
  * dashboard: don't choke on weird builder names.
  * exp/ssh: export type signal, now Signal
  * os: add ModeType constant to mask file type bits
  * text/template: replace Add with AddParseTree.
  * go/doc: detect headings and format them in html
- For more see http://golang.org/doc/devel/weekly.html
* Tue Oct 18 2011 graham@andtech.eu
- Update to r60.3
- Fixes bug in the reflect package
  * disallow Interface method on Value obtained via unexported name
* Thu Oct  6 2011 graham@andtech.eu
- Update to r60.2
- Fixes memory leak in certain map types
* Wed Oct  5 2011 graham@andtech.eu
- Tweaks for gdb debugging
- go.spec changes:
  - move %%go_arch definition to %%prep section
  - pass correct location of go specific gdb pretty printer and
    functions to cpp as HOST_EXTRA_CFLAGS macro
  - install go gdb functions & printer
- gdb-printer.patch
  - patch linker (src/cmd/ld/dwarf.c) to emit correct location of go
    gdb functions and pretty printer
* Tue Sep 27 2011 saschpe@suse.de
- Add file 'VERSION' which is otherwise generated at runtime to fix
  building
* Fri Sep  2 2011 saschpe@suse.de
- Update to weekly.2001-09-01 version
  * archive/tar: support symlinks.
  * big: fix nat.scan bug. (thanks Evan Shaw)
  * bufio: handle a "\r\n" that straddles the buffer. add openbsd. avoid
    redundant bss declarations. fix unused parameters. fix windows/amd64
    build with newest mingw-w64.
  * bytes: clarify that NewBuffer is not for beginners.
  * cgo: explain how to free something. fix GoBytes. fixes callback for windows
    amd64. note that CString result must be freed.
  * effective_go: convert to use tmpltohtml.
  * exp/norm: reduced the size of the byte buffer used by reorderBuffer
    by half by reusing space when combining. a few minor fixes to support the
    implementation of norm. added implementation for []byte versions of methods.
  * exp/template/html: add some tests for ">" attributes. added handling for URL
    attributes. differentiate URL-valued attributes (such as href). reworked
    escapeText to recognize attr boundaries.
  * exp/template: moved from exp to the main tree.
  * exp/wingui: made compatible with windows/amd64.
  * flag: add Parsed, restore Usage.
  * gc: add openbsd. escape analysis. fix build on Plan 9. fix div bug. fix
    pc/line table. fix some spurious leaks. make static initialization more
    static. remove JCXZ; add JCXZW, JCXZL, and JCXZQ instructions. shuffle
    [#]includes. simplify escape analysis recursion.
  * go/ast cleanup: base File/PackageExports on FilterFile/FilterPackage code.
    adjustments to filter function. fix ast.MergePackageFiles to collect infos
    about imports. generalize ast.FilterFile.
  * go/build: add test support & use in gotest. separate test imports out when scanning.
  * go/parser: fix type switch scoping. fix type switch scoping.
  * gob: explain that Debug isn't useful unless it's compiled in.
  * gobuilder: increase log limit.
  * godashboard: fix utf-8 in user names.
  * godoc: first step towards reducing index size. add dummy playground.js to
    silence godoc warning at start-up. added systematic throttling to indexing
    goroutine. fix bug in zip.go. support for reading/writing (splitted) index
    files. use virtual file system when generating package synopses.
  * gofix: forgot to rename the URL type. osopen: fixed=true when changing O_CREAT.
  * goinstall: error out with paths that end with '/'. report lack of $GOPATH
    on errors. select the tag that is closest to runtime.Version.
  * http: add MaxBytesReader to limit request body size. add file protocol
    transport. adjust test threshold for larger suse buffers. delete error
    kludge. on invalid request, send 400 response. return 413 instead of 400
    when the request body is too large. support setting Transport's TLS client
    config.
  * image/tiff: add a decode benchmark. decoder optimization.
  * image: add PalettedImage interface, and make image/png recognize it.
  * io: add TeeReader.
  * json: add struct tag option to wrap literals in strings.
    calculate Offset for Indent correctly.
    fix decode bug with struct tag names with ,opts being ignored.
  * ld: handle Plan 9 ar format. remove duplicate bss definitions.
  * libmach: support reading symbols from Windows .exe for nm.
  * math: fix Pow10 loop. (thanks Volker Dobler)
  * mime: ParseMediaType returns os.Error now, not a nil map. media type
    formatter. text charset defaults.
  * misc/dashboard: remove limit for json package list.
  * misc/emacs: refine label detection.
  * net: add ParseMAC function. change the internal form of IPMask for IPv4.
    disable "tcp" test on openbsd. fix windows build. join and leave a IPv6
    group address, on a specific interface. make use of IPv4len, IPv6len.
    move internal string manipulation routines to parse.go.
  * os: disable Hostname test on OpenBSD. fix WNOHANG Waitmsg.
  * reflect: add Value.Bytes, Value.SetBytes methods.
  * rpc: add benchmark for async rpc calls.
  * runtime: add openbsd 386 defs.h. add runtime support for openbsd 386. add
    runtime prefix to showframe. ctrlhandler for windows amd64. fix stack
    cleanup on windows/amd64. fix void warnings. go interface to cdecl calbacks.
    handle string + char literals in goc2c. make arm work on Ubuntu Natty qemu.
    openbsd thread tweaks. simplify stack traces. speed up cgo calls. use cgo
    runtime functions to call windows syscalls. windows/amd64 callbacks fixed
    and syscall fixed to allow using it in callbacks.
  * strconv: put decimal on stack.
  * spec: update section on Implementation Differences.
  * syscall: SOMAXCONN should be 0x7fffffff at winsock2. add openbsd 386. handle
    RTM_NEWROUTE in ParseNetlinkRouteAttr on Linux. handle routing entry in
    ParseRoutingSockaddr on BSD variants. openbsd amd64 syscall support. use the
    vdso page on linux x86 for faster syscalls instead of int $0x80.
  * template/parse: give if, range, and with a common representation.
  * template: grammar fix for template documentation. range over channel. remove
    else and end nodes from public view.
  * test: put GOROOT/bin before all others in run.
  * time: fix Plan 9 build. fix zone during windows test.
  * type switches: test for pathological case.
  * version.bash: update VERSION on -save if already present.
  * websocket: implements new version of WebSocket protocol.
  * windows/386: clean stack after syscall.
  * xml: marshal "parent>child" tags correctly.
* Tue Aug  2 2011 saschpe@gmx.de
- Update to release r59:
  * Restricted usage of goto statement
  * Package reflect supports a new struct tag scheme that enables sharing of
    struct tags between multiple packages.
  * Package sort's IntArray type has been renamed to IntSlice, and similarly
    for Float64Slice and StringSlice
  * Package strings's Split function has itself been split into Split and
    SplitN. SplitN is the same as the old Split. The new Split is equivalent
    to SplitN with a final argument of -1.
  * Goinstall now installs packages and commands from arbitrary remote
    repositories (not just Google Code, Github, and so on). See the goinstall
    documentation for details.
  More at http://golang.org/doc/devel/release.html#r59
* Wed Jul 20 2011 saschpe@gmx.de
- Update to 2011-07-20 mercurial version:
  * ELF section header overlap fixed, GNU strip doesn't break binaries
    anymore
* Wed Jul 20 2011 saschpe@suse.de
- Update to weekly.2011-07-19 mercurial version:
  * archive/zip: add Writer, add Mtime_ns function to get modified time in
    sensible format.
  * cgi: close stdout reader pipe when finished.
  * cgo: add missing semicolon in generated struct,
  * codereview: fix for Mercurial 1.9.
  * dashboard: list "most installed this week" with rolling count.
  * debug/elf: read ELF Program headers.
  * debug/proc: remove unused package.
  * doc/talks/io2010: update with gofix and handle the errors.
  * exp/eval, exp/ogle: remove packages eval and ogle.
  * exp/regexp/syntax: add Prog.NumCap.
  * exp/template: API changes, bug fixes, and tweaks.
  * flag: make -help nicer.
  * fmt: Scan(&int) was mishandling a lone digit.
  * gc: fix closure bug, fix to build with clang, make size of struct{} and
    [0]byte 0 bytes , some enhancements to printing debug info.
  * gif: fix local color map and coordinates.
  * go/build: include processing of .c files for cgo packages, less aggressive
    failure when GOROOT not found.
  * go/printer: changed max. number of newlines from 3 to 2.
  * gob: register more slice types
  * godoc: support for file systems stored in .zip files.
  * hash/crc32: add SSE4.2 support.
  * html: update section references in comments to the latest HTML5 spec.
  * http: drain the pipe output in TestHandlerPanic to avoid logging deadlock,
    fix Content-Type of file extension, implement http.FileSystem for zip files,
    let FileServer work when path doesn't begin with a slash, support for
    periodic flushing in ReverseProxy.
  * image/draw: add benchmarks.
  * json: add omitempty struct tag option, allow using '$' and '-' as the struct
    field's tag encode \r and \n in strings as e.g. "\n", not "\u000A" escape
    < and > in any JSON string for XSS prevention.
  * ld: allow seek within write buffer< add a PT_LOAD PHDR entry for the PHDR
  * os: plan9: add Process.Signal as a way to send notes
  * os: don't permit Process.Signal after a successful Wait.
  * reflect: add Value.NumMethod, panic if Method index is out of range for a
    type.
  * runtime: faster entersyscall, exitsyscall, fix panic for make(chan [0]byte),
    fix subtle select bug, make TestSideEffectOrder work twice, several
    parallelism-related optimizations and fixes, string-related optimizations,
    track running goroutine count.
  * strconv: handle [-+]Infinity in atof.
  * sync: add fast paths to WaitGroup, improve RWMutex performance.
  * syscall: add Flock on Linux, parse and encode SCM_RIGHTS and SCM_CREDENTIALS
  More at http://golang.org/doc/devel/release.html#r58.1
* Sun Jul 10 2011 saschpe@gmx.de
- Update to 2011/07/10 mercurial version (post r58 and weekly.2011-07-07):
  * Package exec has been redesigned with a more convenient and succinct API.
  * Package os/signal's Signal and UnixSignal types have been moved
    to the os package.
  * Package image/draw is the new name for exp/draw. The GUI-related
    code from exp/draw is now located in the exp/gui package.
  More at http://golang.org/doc/devel/release.html#r58
* Fri Jun 24 2011 saschpe@gmx.de
- No need to set $PATH before building anymore
* Fri Jun 24 2011 saschpe@gmx.de
- DISABLE_NET_TESTS was dropped, this causes net tests to fail
  on openSUSE:Factory currently. Disable tests temporarily.
* Fri Jun 24 2011 saschpe@suse.de
- Update to 24/06/2011 mercurial version
  * http: buffer Request.Write (issue 1996)
  * libmach: fix disassembly of FCMOVcc and FCOMI
  * libmach: fix tracing on linux (for cov)
  * ld: don't attempt to build dynamic sections unnecessarily
  * syscall: add tty support to StartProcess
  * crypto/openpgp: add ElGamal support
  * http: add Server.ListenAndServeTLS (issue 1964)
* Thu Jun 16 2011 saschpe@suse.de
- %%go_requires can't depend on %%requires_ge, it isn't available on
  Fedora and RHEL.
* Wed Jun 15 2011 saschpe@suse.de
- Really set CFLAGS through HOST_EXTRA_CFLAGS environment variable
  for building Go itself and for Go macros (used by Go packages)
- Added go-fix-werrors.patch to fix fatal compiler warnings, not
  used yet as -Wno-error is passed currently
- Adhere to SUSE patch comment conventions
- Changed %%go_requires macro from '%%requires_eq go' to
  '%%requires_ge go'
* Wed Jun 15 2011 saschpe@suse.de
- Update to 15/06/2011 mercurial version
  * Increase max no of windows callbacks (issue 1912)
  * gc: compact stackframe
  * http: fix regression permitting io.Copy on HEAD response
  * Go memory model: minor clarification (issue 1941)
  * go spec: clarif rules for append, scope rules for :=
    (issue 1936, issue 1940)
  * gc: handle go print() and go println() (issue 1952)
  * net: export all fields in Interface (issue 1942)
- Spec file cleanup:
  * Remove *.6 and *.8 files from misc documentation
* Wed Jun  8 2011 saschpe@suse.de
- Added macro %%go_disable_brp_strip_static_archive to disable the
  strip check, it breaks on Fedora-based distros and generates
  a warning for SUSE-based ones. It can be removed if go binaries
  become really stripable
* Wed Jun  8 2011 saschpe@suse.de
- Update to 08/05/2011 mercurial version
  * ld: fix and simplify ELF symbol generation
  * cgo: support non intel gcc machine flags
  * gc: enable building under clang/2.9
  * countless bugfixes, documentation and speed improvements
- Don't build twice (thru all.bash and make.bash)
* Mon May 23 2011 saschpe@suse.de
- Generate %%go_ver macro from Go package version
- Use %%requires_eq for %%go_requires
* Sat May 21 2011 saschpe@gmx.de
- Switch %%go_make* macros from make to gomake
* Sat May 21 2011 saschpe@gmx.de
- Undo not installing *.h/*.c, remove hard links
- Update to 21/05/2011 mercurial version
- Added macro %%go_make_test
* Fri May 20 2011 saschpe@gmx.de
- Package more documentation
* Fri May 20 2011 saschpe@gmx.de
- Moved devel package back into main package until a better
  solution pops up
  * godoc and goinstall belong to base package and need only
    sources in the $GOROOT/srcpkg tree
  * No need to install *.h/*.c files
- Fixed %%{go_provides} macro to provide a specific version
- Changed GOROOT path also in gotry script
* Fri May 20 2011 saschpe@suse.de
- Removed double provides for devel-static package
- Provide a specific version for devel-static package
- Less build dependencies, own directories directly
- Added comments for rpmlint checks, removed old ones
* Fri May 20 2011 saschpe@suse.de
- Disable brp-strip-static-archive also on RHEL and CentOS
* Fri May 20 2011 saschpe@suse.de
- Fix %%go_make_install macro, wrong TARGDIR
* Fri May 20 2011 saschpe@suse.de
- Update to 20/05/2011 mercurial version
- Macro %%go_arch in macros.go now properly set to correct value
* Thu May 19 2011 saschpe@gmx.de
- Fix RPM macros, add arm support
* Thu May 19 2011 saschpe@gmx.de
- Added RPM macros file to simply Go packaging
- Provide devel-static file in main package
- Spec file cleanup
- Remove devel-file-in-non-devel-package rpmlint filter
- Use proper package versioning scheme (needs reinstall)
* Wed May 18 2011 saschpe@suse.de
- Disable brp-strip-static-archive on Fedora
* Wed May 18 2011 saschpe@suse.de
- Re-add STRIP=/bin/true to fix Fedora build
* Wed May 18 2011 saschpe@suse.de
- Let devel package provide devel-static
- Fix typo in devel package description
* Wed May 18 2011 saschpe@suse.de
- Update to 18/05/2011 upstream mercurial release
- Rebased godoc patch
- Removed doc/talks/go_talk-20091030.pdf, fixes bnc#686557
- No chrpath necessary anymore
- Use fdupes
- Drop executable-stack rpmlint filter, not needed anymore
* Fri Apr 29 2011 saschpe@gmx.de
- Update to 29/04/2011 upstream mercurial release
- Changed RPM variables to macros
* Mon Mar 21 2011 saschpe@suse.de
- Changed license from BSD to BSD3c
- Remove pkg_version macro, use %%%%{version} directly
- No Requires on %%%%{release}
* Tue Mar  8 2011 graham@andtech.eu
- Update to 07/03/2011 .1 upstream mercurual release
- Update godoc patch to reflect changes to path package
* Tue Mar  1 2011 graham@andtech.eu
- Update to 24/02/2011 upstream mercurial release
* Wed Feb 16 2011 graham@andtech.eu
- Update to 15/12/2011 upstream mercurial release
- Remove redundant workarounds from .spec
* Tue Feb  8 2011 graham@andtech.eu
- add go-devel for pkg and cmd source installation, this is
  intended to support goinstall(once patched).
- Move goinstall binary to go-devel package and install to
  %%{_sbindir}
- Change the godoc patch to generate API docs from the source
  install location of go-devel
* Tue Feb  1 2011 graham@andtech.eu
- Updated to release 20/01/2011
- run full test suite (without net dependant tests)
- remove redundant libcgo.so from .spec
* Wed Dec  8 2010 saschpe@suse.de
- Updated to 08/12/2010 mercurial version
* Thu Dec  2 2010 speilicke@novell.com
- Updated to 02/12/2010 mercurial version
* Tue Nov 16 2010 speilicke@novell.com
- Updated to 16/11/2010 mercurial version
* Tue Nov  9 2010 speilicke@novell.com
- Updated to 09/11/2010 mercurial version
* Mon Nov  8 2010 speilicke@novell.com
- Simplified spec file
* Mon Nov  8 2010 speilicke@novell.com
- Fixed tarball (no hg history and build files)
* Mon Nov  8 2010 speilicke@novell.com
- Updated to 08/11/2010 mercurial version
* Thu Oct 14 2010 speilicke@novell.com
- Updated to 13/08/2010 mercurial version
* Mon Oct 11 2010 speilicke@novell.com
- Example scripts permissions fixed
* Fri Oct  8 2010 speilicke@novell.com
- Updated to 10/08/2010 mercurial version
* Wed Jun 16 2010 graham@andtech.eu
- Initial package based on 09/06/2010 release
* Thu Apr 29 2010 konrad@tylerc.org>
- Initial Go hg release spec template
