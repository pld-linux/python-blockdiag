#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	blockdiag
Summary:	Blockdiag generate block-diagram image file from spec-text file
Summary(pl.UTF-8):	Generowanie obrazków diagramów blokowych z opisu tekstowego
Name:		python-%{module}
# keep 1.x here for python2 support
Version:	1.5.4
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/blockdiag/
Source0:	https://files.pythonhosted.org/packages/source/b/blockdiag/%{module}-%{version}.tar.gz
# Source0-md5:	2de59ac957224c4f92ea3072aa1221bf
Patch0:		%{name}-tests.patch
URL:		http://blockdiag.com/en/blockdiag/index.html
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-ReportLab
BuildRequires:	python-docutils
BuildRequires:	python-funcparserlib
BuildRequires:	python-nose
BuildRequires:	python-pillow
BuildRequires:	python-webcolors
%if "%{py_ver}" < "2.7"
BuildRequires:	python-ordereddict
BuildRequires:	python-unittest2
%endif
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-ReportLab
BuildRequires:	python3-docutils
BuildRequires:	python3-funcparserlib
BuildRequires:	python3-nose
BuildRequires:	python3-nose_exclude
BuildRequires:	python3-pillow
BuildRequires:	python3-webcolors
%endif
%endif
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
Requires:	python-modules >= 1:2.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
blockdiag generates block-diagram image file from spec-text file.

Features:
- Generate block-diagram from dot like text (basic feature).
- Multilingualization for node-label (UTF-8 only).

%description -l pl.UTF-8
blockdiag generuje pliki obrazów diagramów blokowych z tekstowych
plików opisu.

Funkcje:
- generowanie diagramów z tekstu w stylu dot (podstawowa funkcja).
- obsługa wielu języków dla etykiet węzłów (tylko UTF-8).

%package -n python3-%{module}
Summary:	Blockdiag generate block-diagram image file from spec-text file
Summary(pl.UTF-8):	Generowanie obrazków diagramów blokowych z opisu tekstowego
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-%{module}
blockdiag generates block-diagram image file from spec-text file.

Features:
- Generate block-diagram from dot like text (basic feature).
- Multilingualization for node-label (utf-8 only).

%description -n python3-%{module} -l pl.UTF-8
blockdiag generuje pliki obrazów diagramów blokowych z tekstowych
plików opisu.

Funkcje:
- generowanie diagramów z tekstu w stylu dot (podstawowa funkcja).
- obsługa wielu języków dla etykiet węzłów (tylko UTF-8).

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
# disable tests requiring network: test_command.TestBlockdiagApp.test_app_cleans_up_images, test_generate_diagram.test_generate, test_generate_diagram.ghostscript_not_found_test
PYTHONPATH=$(pwd)/src \
nosetests-%{py_ver} src/blockdiag/tests -e 'test_app_cleans_up_images|test_generate\>|ghostscript_not_found_test'
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
# disable tests requiring network: test_command.TestBlockdiagApp.test_app_cleans_up_images, test_generate_diagram.test_generate, test_generate_diagram.ghostscript_not_found_test
# test_setup_inline_svg_is_true_with_multibytes fails on utf-8 vs latin-1 inconsistency
PYTHONPATH=$(pwd)/src \
nosetests-%{py3_ver} src/blockdiag/tests -e 'test_app_cleans_up_images|test_generate\>|ghostscript_not_found_test|test_setup_inline_svg_is_true_with_multibytes'
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/blockdiag/tests

%{__mv} $RPM_BUILD_ROOT%{_bindir}/{blockdiag,blockdiag-2}
install -d $RPM_BUILD_ROOT%{_mandir}/man1
cp -p blockdiag.1 $RPM_BUILD_ROOT%{_mandir}/man1/blockdiag-2.1

%py_postclean
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/blockdiag/tests

%{__mv} $RPM_BUILD_ROOT%{_bindir}/{blockdiag,blockdiag-3}
ln -s blockdiag-3 $RPM_BUILD_ROOT%{_bindir}/blockdiag
install -d $RPM_BUILD_ROOT%{_mandir}/man1
cp -p blockdiag.1 $RPM_BUILD_ROOT%{_mandir}/man1/blockdiag-3.1
echo '.so blockdiag-3.1' >$RPM_BUILD_ROOT%{_mandir}/man1/blockdiag.1
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%attr(755,root,root) %{_bindir}/blockdiag-2
%{py_sitescriptdir}/blockdiag
%{py_sitescriptdir}/blockdiag_sphinxhelper.py[co]
%{py_sitescriptdir}/%{module}-%{version}-*.egg-info
%{_mandir}/man1/blockdiag-2.1*
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%attr(755,root,root) %{_bindir}/blockdiag
%attr(755,root,root) %{_bindir}/blockdiag-3
%{py3_sitescriptdir}/blockdiag
%{py3_sitescriptdir}/blockdiag_sphinxhelper.py
%{py3_sitescriptdir}/__pycache__/blockdiag_sphinxhelper.cpython-*.py[co]
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%{_mandir}/man1/blockdiag.1*
%{_mandir}/man1/blockdiag-3.1*
%endif
