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
Version:    XXX
Release:    XXX
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
BuildRequires:  python2-babel
BuildRequires:  python2-heatclient
BuildRequires:  python2-keystoneauth1
BuildRequires:  python2-mock
BuildRequires:  python2-openstacksdk
BuildRequires:  python2-osc-lib
BuildRequires:  python2-oslo-i18n
BuildRequires:  python2-oslo-log
BuildRequires:  python2-oslo-serialization
BuildRequires:  python2-oslo-utils
BuildRequires:  python2-pbr
BuildRequires:  python2-prettytable
BuildRequires:  python2-requests
BuildRequires:  python2-six

Requires:       python2-babel >= 2.3.4
Requires:       python2-heatclient >= 1.10.0
Requires:       python2-keystoneauth1 >= 3.3.0
Requires:       python2-openstacksdk >= 0.9.19
Requires:       python2-osc-lib >= 1.8.0
Requires:       python2-oslo-i18n >= 3.15.3
Requires:       python2-oslo-serialization >= 2.18.0
Requires:       python2-oslo-utils >= 3.33.0
Requires:       python2-pbr >= 2.0.0
Requires:       python2-prettytable >= 0.7.1
Requires:       python2-requests
Requires:       python2-six >= 1.10.0
%if 0%{?fedora} > 0
Requires:       python2-pyyaml >= 3.10
%else
Requires:       PyYAML >= 3.10
%endif

%description -n python2-%{sclient}
%{common_desc}


%package -n python2-%{sclient}-tests-unit
Summary:    OpenStack senlin client unit tests
BuildRequires:  python-os-testr
BuildRequires:  python-osc-lib-tests

Requires:       python2-%{sclient} = %{version}-%{release}

Requires:       python2-fixtures
Requires:       python2-mock
Requires:       python2-oslotest
Requires:       python2-stestr
Requires:       python2-testtools
%if 0%{?fedora} > 0
Requires:       python2-requests-mock
Requires:       python2-testscenarios
Requires:       python2-pep8
%else
Requires:       python-requests-mock
Requires:       python-testscenarios
Requires:       python-pep8
%endif


%description -n python2-%{sclient}-tests-unit
%{common_desc}

This package contains the senlin client unit test files.


%if 0%{?with_doc}
%package -n python-%{sclient}-doc
Summary:    OpenStack senlin client documentation

BuildRequires:  python2-openstackdocstheme
BuildRequires:  python2-sphinx

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
BuildRequires:  python3-os-testr

Requires:       python3-babel >= 2.3.4
Requires:       python3-heatclient >= 1.10.0
Requires:       python3-keystoneauth1 >= 3.3.0
Requires:       python3-openstacksdk >= 0.9.19
Requires:       python3-osc-lib >= 1.8.0
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-serialization >= 2.18.0
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-pbr >= 2.0.0
Requires:       python3-prettytable >= 0.7.1
Requires:       python3-requests
Requires:       python3-six >= 1.10.0
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
Requires:       python3-stestr
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

%install

%if 0%{?with_python3}
%py3_install
%endif
%py2_install

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

%files -n python3-%{sclient}-tests-unit
%{python3_sitelib}/%{sclient}/tests
%endif # with_python3

%changelog
