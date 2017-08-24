%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global client python-senlinclient
%global sclient senlinclient
%global executable senlin
%global with_doc 1
%if 0%{?fedora} >= 24
%global with_python3 1
%endif
%global common_desc \
This is a client library for Senlin built on the Senlin \
clustering API. It provides a Python API and \
a command-line tool (senlin).

Name:       %{client}
Version:    1.4.0
Release:    1%{?dist}
Summary:    OpenStack Senlin client
License:    ASL 2.0
URL:        http://launchpad.net/%{client}/

Source0:    http://tarballs.openstack.org/%{client}/%{client}-%{upstream_version}.tar.gz

BuildArch:  noarch


%package -n python2-%{sclient}
Summary:    OpenStack Senlin client
%{?python_provide:%python_provide python2-%{sclient}}

BuildRequires:  git
BuildRequires:  openstack-macros
BuildRequires:  python2-devel
BuildRequires:  python-babel
BuildRequires:  python-heatclient
BuildRequires:  python-keystoneauth1
BuildRequires:  python-mock
BuildRequires:  python-openstacksdk
BuildRequires:  python-osc-lib
BuildRequires:  python-oslo-i18n
BuildRequires:  python-oslo-log
BuildRequires:  python-oslo-serialization
BuildRequires:  python-oslo-utils
BuildRequires:  python-pbr
BuildRequires:  python-prettytable
BuildRequires:  python-requests
BuildRequires:  python-six

Requires:       python-babel >= 2.3.4
Requires:       python-heatclient >= 1.6.1
Requires:       python-keystoneauth1 >= 3.1.0
Requires:       python-openstacksdk >= 0.9.17
Requires:       python-osc-lib >= 1.7.0
Requires:       python-oslo-i18n >= 2.1.0
Requires:       python-oslo-serialization >= 1.10.0
Requires:       python-oslo-utils >= 3.20.0
Requires:       python-pbr >= 2.0.0
Requires:       python-prettytable >= 0.7.1
Requires:       python-requests
Requires:       python-six >= 1.9.0
Requires:       PyYAML >= 3.10

%description -n python2-%{sclient}
%{common_desc}


%package -n python2-%{sclient}-tests-unit
Summary:    OpenStack senlin client unit tests
BuildRequires:  python-os-testr
BuildRequires:  python-osc-lib-tests

Requires:       python2-%{sclient} = %{version}-%{release}

Requires:       python-fixtures
Requires:       python-requests-mock
Requires:       python-mock
Requires:       python-oslotest
Requires:       python-pep8
Requires:       python-testrepository
Requires:       python-testscenarios
Requires:       python-testtools


%description -n python2-%{sclient}-tests-unit
%{common_desc}

This package contains the senlin client unit test files.


%if 0%{?with_doc}
%package -n python-%{sclient}-doc
Summary:    OpenStack senlin client documentation

BuildRequires:  python-openstackdocstheme
BuildRequires:  python-sphinx

%description -n python-%{sclient}-doc
%{common_desc}

This package contains the documentation.
%endif


%if 0%{?with_python3}
%package -n python3-%{sclient}
Summary:    OpenStack senlin client
%{?python_provide:%python_provide python3-%{sclient}}

BuildRequires:  python3-devel
BuildRequires:  python3-babel
BuildRequires:  python3-heatclient
BuildRequires:  python3-keystoneauth1
BuildRequires:  python3-mock
BuildRequires:  python3-openstacksdk
BuildRequires:  python3-osc-lib
BuildRequires:  python3-oslo-i18n
BuildRequires:  python3-oslo-log
BuildRequires:  python3-oslo-serialization
BuildRequires:  python3-oslo-utils
BuildRequires:  python3-pbr
BuildRequires:  python3-prettytable
BuildRequires:  python3-requests
BuildRequires:  python3-six

Requires:       python3-babel >= 2.3.4
Requires:       python3-heatclient >= 1.6.1
Requires:       python3-keystoneauth1 >= 3.1.0
Requires:       python3-openstacksdk >= 0.9.17
Requires:       python3-osc-lib >= 1.7.0
Requires:       python3-oslo-i18n >= 2.1.0
Requires:       python3-oslo-serialization >= 1.10.0
Requires:       python3-oslo-utils >= 3.20.0
Requires:       python3-pbr >= 2.0.0
Requires:       python3-prettytable >= 0.7.1
Requires:       python3-requests
Requires:       python3-six >= 1.9.0
Requires:       python3-PyYAML >= 3.10

%description -n python3-%{sclient}
OpenStack senlin client


%package -n python3-%{sclient}-tests-unit
Summary:        OpenStack senlin client unit tests
Requires:       python3-%{sclient} = %{version}-%{release}

Requires:       python3-fixtures
Requires:       python3-mox3
Requires:       python3-oslo-log
Requires:       python3-oslo-serialization
Requires:       python3-pbr
Requires:       python3-setuptools
Requires:       python3-subunit
Requires:       python3-testrepository
Requires:       python3-testtools
Requires:       python3-mock


%description -n python3-%{sclient}-tests-unit
OpenStack senlin client unit tests

This package contains the senlin client unit test files.

%endif # with_python3

%description
%{common_desc}

%prep
%autosetup -n %{client}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%if 0%{?with_doc}
%{__python2} setup.py build_sphinx -b html
rm -rf doc/build/html/.{doctrees,buildinfo}

%endif

%{__python2} setup.py build_sphinx --builder man

%install

%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/%{executable} %{buildroot}%{_bindir}/%{executable}-%{python3_version}
ln -s ./%{executable}-%{python3_version} %{buildroot}%{_bindir}/%{executable}-3
%endif

%py2_install
install -p -D -m 644 doc/build/man/%{executable}.1 %{buildroot}%{_mandir}/man1/%{executable}.1
mv %{buildroot}%{_bindir}/%{executable} %{buildroot}%{_bindir}/%{executable}-%{python2_version}
ln -s ./%{executable}-%{python2_version} %{buildroot}%{_bindir}/%{executable}-2
ln -s ./%{executable}-2 %{buildroot}%{_bindir}/%{executable}

%check
#%{__python2} setup.py testr
#FIXME: temporarily blacklist broken unit test
# https://review.rdoproject.org/r/#/c/8381/
ostestr -p --black-regex test_do_add_profiler_args

%files -n python2-%{sclient}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{sclient}
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/%{sclient}/tests
%{_mandir}/man1/*
%{_bindir}/%{executable}
%{_bindir}/%{executable}-2
%{_bindir}/%{executable}-%{python2_version}

%files -n python2-%{sclient}-tests-unit
%{python2_sitelib}/%{sclient}/tests

%if 0%{?with_doc}
%files -n python-%{sclient}-doc
%license LICENSE
%doc doc/build/html
%endif

%if 0%{?with_python3}
%files -n python3-%{sclient}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sclient}
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/%{sclient}/tests
%{_bindir}/%{executable}-%{python3_version}
%{_bindir}/%{executable}-3

%files -n python3-%{sclient}-tests-unit
%{python3_sitelib}/%{sclient}/tests
%endif # with_python3

%changelog
* Thu Aug 24 2017 Alfredo Moralejo <amoralej@redhat.com> 1.4.0-1
- Update to 1.4.0

