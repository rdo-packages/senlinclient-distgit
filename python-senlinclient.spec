%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        http://tarballs.openstack.org/%{client}/%{client}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%description
%{common_desc}

%package -n python3-%{sclient}
Summary:    OpenStack Senlin client
%{?python_provide:%python_provide python3-%{sclient}}

BuildRequires:  git-core
BuildRequires:  openstack-macros

BuildRequires:  python3-devel
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

Requires:       python3-heatclient >= 1.10.0
Requires:       python3-keystoneauth1 >= 3.11.0
Requires:       python3-openstacksdk >= 0.24.0
Requires:       python3-osc-lib >= 1.11.0
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-serialization >= 2.18.0
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-pbr >= 2.0.0
Requires:       python3-prettytable >= 0.7.2
Requires:       python3-requests
Requires:       python3-PyYAML >= 5.3.1

%description -n python3-%{sclient}
%{common_desc}


%package -n python3-%{sclient}-tests-unit
Summary:    OpenStack senlin client unit tests
BuildRequires:  python3-os-testr
BuildRequires:  python3-osc-lib-tests

Requires:       python3-%{sclient} = %{version}-%{release}

Requires:       python3-fixtures
Requires:       python3-mock
Requires:       python3-oslotest
Requires:       python3-stestr
Requires:       python3-testtools
Requires:       python3-requests-mock
Requires:       python3-testscenarios


%description -n python3-%{sclient}-tests-unit
%{common_desc}

This package contains the senlin client unit test files.


%if 0%{?with_doc}
%package -n python-%{sclient}-doc
Summary:    OpenStack senlin client documentation

BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-sphinx

%description -n python-%{sclient}-doc
%{common_desc}

This package contains the documentation.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{client}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%{py3_build}

%if 0%{?with_doc}
sphinx-build-3 -b html doc/source doc/build/html
rm -rf doc/build/html/.{doctrees,buildinfo}

%endif

%install
%{py3_install}

%check
export PYTHON=python3
stestr run

%files -n python3-%{sclient}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sclient}
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/%{sclient}/tests

%files -n python3-%{sclient}-tests-unit
%{python3_sitelib}/%{sclient}/tests

%if 0%{?with_doc}
%files -n python-%{sclient}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
