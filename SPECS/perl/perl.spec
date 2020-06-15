%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\((VMS|Win32|BSD::|DB\\)$)
# unicore::Name - it's needed by perl, maybe problem of rpm
# FCGI is external dependency after install of perl-CGI, remove it during RC releases
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((VMS|BSD::|Win32|Tk|Mac::|Your::Module::Here|unicore::Name|FCGI)
# Filter dependencies on private modules. Generator:
# for F in $(find lib -type f); do perl -e '$/ = undef; $_ = <>; if (/^package #\R([\w:]*);/m) { print qq{|^perl\\\\($1\\\\)} }' "$F"; done
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Locale::Codes::Country_Retired\\)|^perl\\(Locale::Codes::LangFam_Retired\\)|^perl\\(Locale::Codes::Script_Retired\\)|^perl\\(Locale::Codes::LangExt_Codes\\)|^perl\\(Locale::Codes::LangFam_Codes\\)|^perl\\(Locale::Codes::Script_Codes\\)|^perl\\(Locale::Codes::Language_Codes\\)|^perl\\(Locale::Codes::LangExt_Retired\\)|^perl\\(Locale::Codes::Currency_Codes\\)|^perl\\(Locale::Codes::LangVar_Retired\\)|^perl\\(Locale::Codes::Language_Retired\\)|^perl\\(Locale::Codes::Country_Codes\\)|^perl\\(Locale::Codes::LangVar_Codes\\)|^perl\\(Locale::Codes::Currency_Retired\\)

Summary:        Practical Extraction and Report Language
Name:           perl
Version:        5.24.1
Release:        9%{?dist}
License:        GPLv1+
URL:            http://www.perl.org/
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.cpan.org/src/5.0/%{name}-%{version}.tar.bz2
%define sha1    perl=d43ac3d39686462f86eed35b3c298ace74f1ffa0
Patch0:         CVE-2017-12883.patch
#https://perl5.git.perl.org/perl.git/patch/96c83ed78aeea1a0496dd2b2d935869a822dc8a5
Patch1:         CVE-2017-12837.patch
Patch2:         perl-CVE-2018-6797.patch
Patch3:         perl-CVE-2018-6798-1.patch
Patch4:         perl-CVE-2018-6798-2.patch
Patch5:         perl-CVE-2018-6913.patch
Patch6:         perl-CVE-2018-12015.patch
Patch7:         perl-CVE-2018-18311.patch
Patch8:         perl-CVE-2018-18313.patch
Patch9:         perl-CVE-2018-18314.patch
Patch10:        perl-CVE-2018-18312.patch
Patch11:        perl-CVE-2020-10543.patch
Provides:       perl >= 0:5.003000
Provides:       perl(getopts.pl)
Provides:       /bin/perl
BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  gdbm-devel
Requires:       zlib 
Requires:       gdbm
Requires:       glibc
Requires:       libgcc
%description
The Perl package contains the Practical Extraction and
Report Language.
%prep
%setup -q
sed -i 's/-fstack-protector/&-all/' Configure
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1

%build
export BUILD_ZLIB=False
export BUILD_BZIP2=0
CFLAGS="%{_optflags}"

sh Configure -des \
    -Dprefix=%{_prefix} \
    -Dvendorprefix=%{_prefix} \
    -Dman1dir=%{_mandir}/man1 \
    -Dman3dir=%{_mandir}/man3 \
    -Dpager=%{_bindir}"/less -isR" \
    -Duseshrplib \
    -Dusethreads \
        -DPERL_RANDOM_DEVICE="/dev/erandom"

make VERBOSE=1 %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
unset BUILD_ZLIB BUILD_BZIP2
%check
sed -i '/02zlib.t/d' MANIFEST
sed -i '/cz-03zlib-v1.t/d' MANIFEST
sed -i '/cz-06gzsetp.t/d' MANIFEST
sed -i '/porting\/podcheck.t/d' MANIFEST
make test TEST_SKIP_VERSION_CHECK=1
%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_bindir}/*
%dir %{_libdir}/perl5
%dir %{_libdir}/perl5/%{version}
%{_libdir}/perl5/%{version}/*
%{_mandir}/*/*
%changelog
*   Mon Jun 15 2020 Dweep Advani <dadvani@vmware.com> 5.24.1-9
-   Patched for fixing CVE-2020-10543
*   Fri Mar 01 2019 Dweep Advani <dadvani@vmware.com> 5.24.1-8
-   Fixed CVE-2018-18312 and CVE-2018-18314
*   Fri Feb 22 2019 Dweep Advani <dadvani@vmware.com> 5.24.1-7
-   Fixed CVE-2018-18311 and CVE-2018-18313
*   Mon Aug 13 2018 Dweep Advani <dadvani@vmware.com> 5.24.1-6
-   Fix CVE-2018-12015
*   Mon May 21 2018 Xiaolin <xiaolinl@vmware.com> 5.24.1-5
-   Fix CVE-2018-6797, CVE-2018-6798, CVE-2018-6913
*   Tue Oct 03 2017 Dheeraj Shetty <dheerajs@vmware.com> 5.24.1-4
-   CVE-2017-12837 and CVE-2017-12883 patch from
-   https://perl5.git.perl.org/perl.git/commitdiff/2be4edede4ae226e2eebd4eff28cedd2041f300f#patch1
*   Wed Jul 05 2017 Xiaolin Li <xiaolinl@vmware.com> 5.24.1-3
-   Rebuild perl after adding gdbm-devel package.
*   Thu Jun 15 2017 Chang Lee <changlee@vmware.com> 5.24.1-2
-   Updated %check
*   Mon Apr 3 2017 Robert Qi <qij@vmware.com> 5.24.1-1
-   Update to 5.24.1.
*   Thu Oct 20 2016 Xiaolin Li <xiaolinl@vmware.com> 5.22.1-5
-   CVE-2016-1238 patch from http://perl5.git.perl.org/perl.git/commit/cee96d52c39b1e7b36e1c62d38bcd8d86e9a41ab.
*   Mon Oct 10 2016 ChangLee <changlee@vmware.com> 5.22.1-4
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.22.1-3
-   GA - Bump release of all rpms
*   Tue Jan 26 2016 Anish Swaminathan <anishs@vmware.com> 5.22.1-2
-   Enable threads
*   Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com> 5.22.1-1
-   Update version
*   Thu Jun 4 2015 Touseef Liaqat <tliaqat@vmware.com> 5.18.2-2
-   Provide /bin/perl.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 5.18.2-1
-   Initial build. First version
