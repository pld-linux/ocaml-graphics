#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%if %{without ocaml_opt}
%define		_enable_debug_packages	0
%endif

%define		module	graphics
Summary:	Portable drawing primitives for OCaml
Name:		ocaml-%{module}
Version:	5.1.1
Release:	1
License:	LGPLv2 with exceptions
Source0:	https://github.com/ocaml/graphics/releases/download/%{version}/%{module}-%{version}.tbz
# Source0-md5:	bc127b5da919b61f4c928a6657c88886
URL:		https://github.com/ocaml/graphics
BuildRequires:	ocaml >= 4.09.0
BuildRequires:	ocaml-dune-devel >= 2.1
BuildRequires:	xorg-lib-libX11-devel
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The graphics library provides a set of portable drawing primitives.
Drawing takes place in a separate window that is created when
Graphics.open_graph is called.

%package        devel
Summary:	Development files for %{name}
Requires:	%{name} = %{version}-%{release}
Requires:	xorg-lib-libX11-devel

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n %{module}-%{version}

%build
dune build %{?_smp_mflags} --display=verbose

%install
rm -rf $RPM_BUILD_ROOT

dune install --destdir=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.md README.md
%dir %{_libdir}/ocaml/%{module}
%{_libdir}/ocaml/%{module}/META
%{_libdir}/ocaml/%{module}/*.cma
%{_libdir}/ocaml/%{module}/*.cmi
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/%{module}/*.cmxs
%endif
%{_libdir}/ocaml/stublibs/dllgraphics_stubs.so

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/%{module}/dune-package
%{_libdir}/ocaml/%{module}/opam
%if %{with ocaml_opt}
%{_libdir}/ocaml/%{module}/*.a
%{_libdir}/ocaml/%{module}/*.cmx
%{_libdir}/ocaml/%{module}/*.cmxa
%endif
%{_libdir}/ocaml/%{module}/*.cmt
%{_libdir}/ocaml/%{module}/*.cmti
%{_libdir}/ocaml/%{module}/*.mli
