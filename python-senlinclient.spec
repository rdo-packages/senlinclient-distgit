# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global client python-senlinclient
%global sclient senlinclient
%global executable senlin
%global with_doc 1
%global common_desc \
This is a client library for Senlin built on the Senlin \
clustering API. It provides a Python API and \
a command-line tool (senlin).

Name:       %{client}
Version:    XXX
Release:    XXX
Summary:    OpenStack Senlin client
License:    ASL 2.0
URL:        http://launchpad.net/%{client}/

Source0:    http://tarballs.openstack.org/%{client}/%{client}-%{upstream_version}.tar.gz

BuildArch:  noarch

%description
%{common_desc}

%package -n python%{pyver}-%{sclient}
Summary:    OpenStack Senlin client
%{?python_provide:%python_provide python%{pyver}-%{sclient}}

BuildRequires:  git
BuildRequires:  openstack-macros
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-babel
BuildRequires:  python%{pyver}-heatclient
BuildRequires:  python%{pyver}-keystoneauth1
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-openstacksdk
BuildRequires:  python%{pyver}-osc-lib
BuildRequires:  python%{pyver}-oslo-i18n
BuildRequires:  python%{pyver}-oslo-log
BuildRequires:  python%{pyver}-oslo-serialization
BuildRequires:  python%{pyver}-oslo-utils
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-prettytable
BuildRequires:  python%{pyver}-requests
BuildRequires:  python%{pyver}-six

Requires:       python%{pyver}-babel >= 2.3.4
Requires:       python%{pyver}-heatclient >= 1.10.0
Requires:       python%{pyver}-keystoneauth1 >= 3.4.0
Requires:       python%{pyver}-openstacksdk >= 0.11.2
Requires:       python%{pyver}-osc-lib >= 1.10.0
Requires:       python%{pyver}-oslo-i18n >= 3.15.3
Requires:       python%{pyver}-oslo-serialization >= 2.18.0
Requires:       python%{pyver}-oslo-utils >= 3.33.0
Requires:       python%{pyver}-pbr >= 2.0.0
Requires:       python%{pyver}-prettytable >= 0.7.2
Requires:       python%{pyver}-requests
Requires:       python%{pyver}-six >= 1.10.0
# Handle python2 exception
%if %{pyver} == 2
Requires:       PyYAML >= 3.10
%else
Requires:       python%{pyver}-pyyaml >= 3.10
%endif

%description -n python%{pyver}-%{sclient}
%{common_desc}


%package -n python%{pyver}-%{sclient}-tests-unit
Summary:    OpenStack senlin client unit tests
BuildRequires:  python%{pyver}-os-testr
BuildRequires:  python%{pyver}-osc-lib-tests

Requires:       python%{pyver}-%{sclient} = %{version}-%{release}

Requires:       python%{pyver}-fixtures
Requires:       python%{pyver}-mock
Requires:       python%{pyver}-oslotest
Requires:       python%{pyver}-stestr
Requires:       python%{pyver}-testtools
# Handle python2 exception
%if %{pyver} == 2
Requires:       python-requests-mock
Requires:       python-testscenarios
%else
Requires:       python%{pyver}-requests-mock
Requires:       python%{pyver}-testscenarios
%endif


%description -n python%{pyver}-%{sclient}-tests-unit
%{common_desc}

This package contains the senlin client unit test files.


%if 0%{?with_doc}
%package -n python-%{sclient}-doc
Summary:    OpenStack senlin client documentation

BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-sphinx

%description -n python-%{sclient}-doc
%{common_desc}

This package contains the documentation.
%endif

%prep
%autosetup -n %{client}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%{pyver_build}

%if 0%{?with_doc}
sphinx-build-%{pyver} -b html doc/source doc/build/html
rm -rf doc/build/html/.{doctrees,buildinfo}

%endif

%install
%{pyver_install}

%check
#%{pyver_bin} setup.py testr
#FIXME: temporarily blacklist broken unit test
# https://review.rdoproject.org/r/#/c/8381/
ostestr -p --black-regex test_do_add_profiler_args

%files -n python%{pyver}-%{sclient}
%license LICENSE
%doc README.rst
%{pyver_sitelib}/%{sclient}
%{pyver_sitelib}/*.egg-info
%exclude %{pyver_sitelib}/%{sclient}/tests

%files -n python%{pyver}-%{sclient}-tests-unit
%{pyver_sitelib}/%{sclient}/tests

%if 0%{?with_doc}
%files -n python-%{sclient}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
