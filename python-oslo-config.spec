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

BuildRequires: python3-devel
BuildRequires: pyproject-rpm-macros
BuildRequires: git-core

%description
The Oslo project intends to produce a python library containing
infrastructure code shared by OpenStack projects. The APIs provided
by the project should be high quality, stable, consistent and generally
useful.

The oslo-config library is a command line and configuration file
parsing library from the Oslo project.

%package -n python3-%{pypi_name}
Summary:    OpenStack common configuration library

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

# remove constraint files from tox.ini which is not handled by automatic BRs
sed -i '/^ *-c.*TOX_CONSTRAINTS_FILE/d' tox.ini
# remove some unneeded build requirements
sed -i '/^doc8.*/d' doc/requirements.txt
sed -i -e '/^mypy.*/d' -e '/^coverage.*/d' -e '/^bandit.*/d' -e '/^hacking.*/d' -e '/^pre-commit.*/d' test-requirements.txt

# There is cyclic dep between oslo.log and oslo.config to run unit tests.
%if 0%{?repo_bootstrap} != 0
sed -i -e '/^oslo.log.*/d' test-requirements.txt
%endif

# Remove shebang from non executable file, it's used by the oslo-config-validator binary.
sed -i '/\/usr\/bin\/env/d' oslo_config/validator.py
# Remove tests requiring sphinx if sphinx is not available
%if 0%{?with_doc} == 0
rm oslo_config/tests/test_sphinxext.py
rm oslo_config/tests/test_sphinxconfiggen.py
%endif

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
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

pushd %{buildroot}/%{_bindir}
for i in generator validator
do
ln -s oslo-config-$i oslo-config-$i-3
done
popd

%check
%if 0%{?repo_bootstrap} == 0
%tox -e %{default_toxenv}
%endif

%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/oslo-config-generator
%{_bindir}/oslo-config-generator-3
%{_bindir}/oslo-config-validator
%{_bindir}/oslo-config-validator-3
%{python3_sitelib}/oslo_config
%{python3_sitelib}/*.dist-info

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
