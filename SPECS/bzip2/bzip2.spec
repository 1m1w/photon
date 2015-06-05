Summary:	Contains programs for compressing and decompressing files
Name:		bzip2
Version:	1.0.6
Release:	2%{?dist}
License:	BSD
URL:		http://www.bzip.org/
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution: Photon
Source0:		http://www.bzip.org/%{version}/%{name}-%{version}.tar.gz
Patch0:		http://www.linuxfromscratch.org/patches/lfs/7.2/bzip2-1.0.6-install_docs-1.patch
%description
The Bzip2 package contains programs for compressing and
decompressing files.  Compressing text files with bzip2 yields a much better
compression percentage than with the traditional gzip.
%package	devel
Summary:	Header and development files for bzip2
%description	devel
It contains the libraries and header files to create applications 
%prep
%setup -q
%patch0 -p1
sed -i 's@\(ln -s -f \)$(PREFIX)/bin/@\1@' Makefile
sed -i "s@(PREFIX)/man@(PREFIX)/share/man@g" Makefile
%build
make VERBOSE=1 %{?_smp_mflags} -f Makefile-libbz2_so
make clean
make VERBOSE=1 %{?_smp_mflags}
%install
make PREFIX=%{buildroot}/usr install
install -vdm 0755 %{buildroot}/%{_lib}
install -vdm 0755 %{buildroot}/bin
cp -av libbz2.so* %{buildroot}/%{_lib}
install -vdm 755 %{buildroot}%{_libdir}
ln -sv ../../%{_lib}/libbz2.so.1.0 %{buildroot}%{_libdir}/libbz2.so
rm -v %{buildroot}%{_bindir}/{bunzip2,bzcat}
ln -sv bzip2 %{buildroot}/usr/bin/bunzip2
ln -sv bzip2 %{buildroot}/usr/bin/bzcat
find %{buildroot} -name '*.a'  -delete
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_bindir}/bzcat
%{_bindir}/bunzip2
%{_bindir}/bzless
%{_bindir}/bzgrep
%{_bindir}/bzip2
%{_bindir}/bzdiff
%{_bindir}/bzfgrep
%{_bindir}/bzcmp
%{_bindir}/bzip2recover
%{_bindir}/bzegrep
%{_bindir}/bzmore
%{_docdir}/bzip2-1.0.6/manual.pdf
%{_docdir}/bzip2-1.0.6/bzip2.txt
%{_docdir}/bzip2-1.0.6/manual.ps
%{_docdir}/bzip2-1.0.6/manual.html
%{_mandir}/man1/bzmore.1.gz
%{_mandir}/man1/bzfgrep.1.gz
%{_mandir}/man1/bzegrep.1.gz
%{_mandir}/man1/bzgrep.1.gz
%{_mandir}/man1/bzdiff.1.gz
%{_mandir}/man1/bzcmp.1.gz
%{_mandir}/man1/bzless.1.gz
%{_mandir}/man1/bzip2.1.gz
%{_lib}/libbz2.so.1.0.6
%{_lib}/libbz2.so.1.0
%{_libdir}/libbz2.so
%files devel
%{_includedir}/bzlib.h
%changelog
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 1.0.6-2
-   Update according to UsrMove.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.0.6-1
-	Initial build.	First version
