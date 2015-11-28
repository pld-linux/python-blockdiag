%define 	module	blockdiag
Summary:	Blockdiag generate block-diagram image file from spec-text file
Name:		python-%{module}
Version:	1.1.6
Release:	2
License:	Apache v2.0
Group:		Development/Languages
URL:		http://blockdiag.com/en/blockdiag/index.html
Source0:	http://pypi.python.org/packages/source/b/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	6057b077618df3b9f4c5a73910ddd736
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
Requires:	python-PIL
%if "%{py_ver}" < "2.7"
Requires:	python-ordereddict
%endif
Requires:	python-funcparserlib >= 0.3.4
Requires:	python-modules >= 2.4
Requires:	python-webcolors >= 1.3.1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
blockdiag generate block-diagram image file from spec-text file.

Features:
- Generate block-diagram from dot like text (basic feature).
- Multilingualization for node-label (utf-8 only).

%prep
%setup -q -n %{module}-%{version}
%{__sed} -i -e 's/^from ez_setup/#from ez_setup/' setup.py
%{__sed} -i -e 's/^use_setuptools()/#use_setuptools()/' setup.py

%build
%py_build

%install
rm -rf $RPM_BUILD_ROOT
%py_install \
	--root $RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}/tests
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}_sphinxhelper.*

install -d $RPM_BUILD_ROOT%{_mandir}/man1
cp -p %{module}.1 $RPM_BUILD_ROOT%{_mandir}/man1

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{module}
%{_mandir}/man1/%{module}.1*
%{py_sitescriptdir}/%{module}
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-%{version}-*.egg-info
%endif
