%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

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
License:    Apache-2.0
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

BuildRequires:  git-core
BuildRequires:  openstack-macros

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
%description -n python3-%{sclient}
%{common_desc}


%package -n python3-%{sclient}-tests-unit
Summary:    OpenStack senlin client unit tests
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


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini
sed -i '/sphinx-build/ s/-W//' tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
%tox -e docs
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

%check
%tox -e %{default_toxenv}

%files -n python3-%{sclient}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sclient}
%{python3_sitelib}/*.dist-info
%exclude %{python3_sitelib}/%{sclient}/tests

%files -n python3-%{sclient}-tests-unit
%{python3_sitelib}/%{sclient}/tests

%if 0%{?with_doc}
%files -n python-%{sclient}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
