#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	SHA
Summary:	Implementations of the SHA suite of message digest functions
Summary(pl.UTF-8):	Implementacje zestawu funkcji skrótu SHA
Name:		ghc-%{pkgname}
Version:	1.6.4.4
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/SHA
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	f2a26839057b5e4fd53b8f6a41b88553
URL:		http://hackage.haskell.org/package/SHA
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-array
BuildRequires:	ghc-base >= 4
BuildRequires:	ghc-base < 6
BuildRequires:	ghc-binary >= 0.7
BuildRequires:	ghc-bytestring > 0.8
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-array-prof
BuildRequires:	ghc-base-prof >= 4
BuildRequires:	ghc-binary-prof >= 0.7
BuildRequires:	ghc-bytestring-prof > 0.8
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-base >= 4
Requires:	ghc-binary >= 0.7
Requires:	ghc-bytestring > 0.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This library implements the SHA suite of message digest functions,
according to NIST FIPS 180-2 (with the SHA-224 addendum), as well as
the SHA-based HMAC routines. The functions have been tested against
most of the NIST and RFC test vectors for the various functions.
While some attention has been paid to performance, these do not
presently reach the speed of well-tuned libraries, like OpenSSL.

%description -l pl.UTF-8
Ta biblioteka implementuje zestaw funkcji skrótu SHA zgodnych z NIST
FIPS 180-2 (z dodatkiem SHA-224), a także funkcje HMAC oparte na SHA.
Funkcje te zostały przetestowane względem większości wektorów
testowych NIST i RFC dla różnych funkcji. O ile zwrócono pewną uwagę
na wydajność, obecnie nie osiągnięto szybkości dobrze dostrojonych
bibliotek, takich jak OpenSSL.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4
Requires:	ghc-binary-prof >= 0.7
Requires:	ghc-bytestring-prof > 0.8

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%attr(755,root,root) %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Digest
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Digest/Pure
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Digest/Pure/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Digest/Pure/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Digest/Pure/*.p_hi
%endif
