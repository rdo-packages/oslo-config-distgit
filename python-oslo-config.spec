%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%global sname oslo.config
%global pypi_name oslo-config
%global with_doc 1

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:       python-oslo-config
Epoch:      2
Version:    XXX
Release:    XXX
Summary:    OpenStack common configuration library

Group:      Development/Languages
License:    ASL 2.0
URL:        https://launchpad.net/%{sname}
Source0:    https://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%description
The Oslo project intends to produce a python library containing
infrastructure code shared by OpenStack projects. The APIs provided
by the project should be high quality, stable, consistent and generally
useful.

The oslo-config library is a command line and configuration file
parsing library from the Oslo project.

%package -n python3-%{pypi_name}
Summary:    OpenStack common configuration library
%{?python_provide:%python_provide python3-%{pypi_name}}
Obsoletes: python2-%{pypi_name} < %{version}-%{release}

%if (0%{?fedora} && 0%{?fedora} < 32) || (0%{?rhel} && 0%{?rhel} < 9)
Requires:   python3-importlib-metadata >= 1.7.0
%endif
Requires:   python3-oslo-i18n >= 3.15.3
Requires:   python3-rfc3986 >= 1.2.0
Requires:   python3-pbr
Requires:   python3-requests >= 2.18.0
Requires:   python3-stevedore >= 1.20.0
Requires:   python3-debtcollector >= 1.2.0
Requires:   python3-netaddr >= 0.7.18
Requires:   python3-yaml >= 5.1

BuildRequires: python3-devel
BuildRequires: pyproject-rpm-macros
BuildRequires: git-core


%description -n python3-%{pypi_name}
The Oslo project intends to produce a python library containing
infrastructure code shared by OpenStack projects. The APIs provided
by the project should be high quality, stable, consistent and generally
useful.

The oslo-config library is a command line and configuration file
parsing library from the Oslo project.

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:    Documentation for OpenStack common configuration library

%description -n python-%{pypi_name}-doc
Documentation for the oslo-config library.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif

%autosetup -n %{sname}-%{upstream_version} -S git

# Remove shebang from non executable file, it's used by the oslo-config-validator binary.
sed -i '/\/usr\/bin\/env/d' oslo_config/validator.py

# Remove constraints file in tox deps as pyproject-rpm-macros doesn't support it
sed -i '/.*-c{env:TOX_CONSTRAINTS_FILE.*/d' tox.ini

sed -i '/^doc8.*/d' doc/requirements.txt
sed -i '/^pre-commit.*/d' test-requirements.txt
sed -i '/^bandit.*/d' test-requirements.txt
sed -i '/^hacking.*/d' test-requirements.txt

%if 0%{?repo_bootstrap} == 1
sed -i '/^oslo.log*/d' test-requirements.txt
%endif

# Remove tests requiring sphinx if sphinx is not available
%if 0%{?with_doc} == 0
rm oslo_config/tests/test_sphinxext.py
rm oslo_config/tests/test_sphinxconfiggen.py
%endif

%generate_buildrequires
%pyproject_buildrequires -R -t -e %{default_toxenv},docs

%build
%pyproject_wheel

%if 0%{?with_doc}
%tox -e docs
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install
%pyproject_save_files oslo_config

pushd %{buildroot}/%{_bindir}
for i in generator validator
do
ln -s oslo-config-$i oslo-config-$i-3
done
popd

%check
%if 0%{?repo_bootstrap} == 0
%tox -e %{default_toxenv} -- -- --black-regex test_generator_raises_error
%endif

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst
%{_bindir}/oslo-config-generator
%{_bindir}/oslo-config-generator-3
%{_bindir}/oslo-config-validator
%{_bindir}/oslo-config-validator-3


%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
