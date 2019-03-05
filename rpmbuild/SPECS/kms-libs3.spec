Summary: C Library and Tools for Amazon S3 Access
Name: kms-libs3
Version: 6.6.0
Release: 1
License: LGPL
Group: Networking/Utilities
URL: http://sourceforge.net/projects/reallibs3
Source0: libs3-kms6.6.0.tar.gz
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root
# Want to include curl dependencies, but older Fedora Core uses curl-devel,
# and newer Fedora Core uses libcurl-devel ... have to figure out how to
# handle this problem, but for now, just don't check for any curl libraries
Buildrequires: curl-devel
Buildrequires: libxml2-devel
Buildrequires: openssl-devel
Buildrequires: make
Requires: libcurl
Requires: libxml2
Requires: openssl

#%define debug_package %{nil}

%description
This package includes the libs3 shared object library, needed to run
applications compiled against libs3, and additionally contains the s3
utility for accessing Amazon S3.

%package devel
Summary: Headers and documentation for libs3
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This library provides an API for using Amazon's S3 service (see
http://s3.amazonaws.com).  Its design goals are:

 - To provide a simple and straightforward API for accessing all of S3's
   functionality
 - To not require the developer using libs3 to need to know anything about:
     - HTTP
     - XML
     - SSL
   In other words, this API is meant to stand on its own, without requiring
   any implicit knowledge of how S3 services are accessed using HTTP
   protocols.
 - To be usable from multithreaded code
 - To be usable by code which wants to process multiple S3 requests
   simultaneously from a single thread
 - To be usable in the simple, straightforward way using sequentialized
   blocking requests


%prep
%setup -q -n libs3

%build
#BUILD=$RPM_BUILD_ROOT/build make exported

%install
BUILD=$RPM_BUILD_ROOT/build DESTDIR=$RPM_BUILD_ROOT/usr make install
rm -rf $RPM_BUILD_ROOT/usr/lib/libs3.a
mv $RPM_BUILD_ROOT/usr/lib $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
cp s3.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig
rm -rf $RPM_BUILD_ROOT/build


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/s3
%{_libdir}/libs3.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libs3.so
%{_includedir}/libs3.h
%{_libdir}/pkgconfig/s3.pc
#/usr/lib/libs3.a

%changelog
* Sat Aug 09 2008  <bryan@ischo,com> Bryan Ischo
- Split into regular and devel packages.

* Tue Aug 05 2008  <bryan@ischo,com> Bryan Ischo
- Initial build.
