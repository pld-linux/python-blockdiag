%define 	module	blockdiag
Summary:	Blockdiag generate block-diagram image file from spec-text file
Name:		python-%module
Version:	0.9.4
Release:	1
License:	Apache v2.0
Group:		Development/Languages
URL:		http://blockdiag.com/en/blockdiag/index.html
Source0:	http://pypi.python.org/packages/source/b/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	f60754f3b314d9d4c678b8f764b8a355
#BuildRequires:	python < 3.0
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
Requires:	python-PIL
Requires:	python-setuptools
Requires:	python-webcolors >= 1.3.1
Requires:	python-devel-tools
Requires:	python-funcparserlib
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
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--skip-build \
	--root $RPM_BUILD_ROOT

%py_postclean

%{__rm} $RPM_BUILD_ROOT/%{py_sitescriptdir}/%{module}_sphinxhelper.*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/blockdiag
%{py_sitescriptdir}/%{module}
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-%{version}-*.egg-info
%endif
