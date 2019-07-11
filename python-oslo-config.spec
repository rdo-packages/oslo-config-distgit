%global sname oslo.config
%global pypi_name oslo-config
%global with_doc 1

%if 0%{?fedora} || 0%{?rhel} >= 8
%global with_python3 1
%endif

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

Patch0001: 0001-add-usr-share-project-dist.conf-to-the-default-confi.patch

BuildArch:  noarch

%description
The Oslo project intends to produce a python library containing
infrastructure code shared by OpenStack projects. The APIs provided
by the project should be high quality, stable, consistent and generally
useful.

The oslo-config library is a command line and configuration file
parsing library from the Oslo project.

%package -n python2-%{pypi_name}
Summary:    OpenStack common configuration library
%{?python_provide:%python_provide python2-%{pypi_name}}

Requires:   python2-oslo-i18n >= 3.15.3
Requires:   python2-rfc3986 >= 1.2.0
Requires:   python2-pbr
Requires:   python2-requests >= 2.18.0
Requires:   python2-six >= 1.10.0
Requires:   python2-stevedore >= 1.20.0
Requires:   python2-debtcollector >= 1.2.0
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:   python2-enum34
Requires:   python2-netaddr >= 0.7.18
Requires:   python2-pyyaml >= 3.10
%else
Requires:   python-enum34
Requires:   python-netaddr >= 0.7.18
Requires:   PyYAML >= 3.10
%endif

BuildRequires: python2-devel
BuildRequires: python2-setuptools
BuildRequires: python2-oslo-i18n
BuildRequires: python2-rfc3986
BuildRequires: python2-pbr
BuildRequires: git
# Required for tests
BuildRequires: python2-testscenarios
BuildRequires: python2-testrepository
BuildRequires: python2-testtools
BuildRequires: python2-oslotest
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires: python2-enum34
BuildRequires: python2-requests-mock
BuildRequires: python2-netaddr
BuildRequires: python2-pyyaml
BuildRequires: python2-stevedore
%else
BuildRequires: python-enum34
BuildRequires: python-requests-mock
BuildRequires: python-netaddr
BuildRequires: PyYAML
BuildRequires: python-stevedore
%endif

%if 0%{?repo_bootstrap} == 0
BuildRequires: python2-oslo-log
%endif

%description -n python2-%{pypi_name}
The Oslo project intends to produce a python library containing
infrastructure code shared by OpenStack projects. The APIs provided
by the project should be high quality, stable, consistent and generally
useful.

The oslo-config library is a command line and configuration file
parsing library from the Oslo project.

%if 0%{?with_doc}
%package -n python2-%{pypi_name}-doc
Summary:    Documentation for OpenStack common configuration library
%{?python_provide:%python_provide python2-%{pypi_name}-doc}
BuildRequires: python2-sphinx
BuildRequires: python2-fixtures
BuildRequires: python2-openstackdocstheme
BuildRequires: python2-oslotest >= 1.10.0
BuildRequires: python2-stevedore
BuildRequires: python2-sphinxcontrib-apidoc
%if 0%{?with_python3}
BuildRequires: python3-sphinx
BuildRequires: python3-sphinxcontrib-apidoc
%endif
%description -n python2-%{pypi_name}-doc
Documentation for the oslo-config library.
%endif

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:    OpenStack common configuration library
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:   python3-netaddr >= 0.7.18
Requires:   python3-oslo-i18n >= 3.15.3
Requires:   python3-rfc3986 >= 1.2.0
Requires:   python3-pbr
Requires:   python3-requests >= 2.18.0
Requires:   python3-six >= 1.10.0
Requires:   python3-stevedore >= 1.20.0
Requires:   python3-debtcollector >= 1.2.0
Requires:   python3-PyYAML >= 3.10

BuildRequires: python3-devel
BuildRequires: python3-oslo-i18n
BuildRequires: python3-rfc3986
BuildRequires: python3-pbr
BuildRequires: python3-setuptools
BuildRequires: git
# Required for tests
BuildRequires: python3-fixtures
BuildRequires: python3-netaddr
BuildRequires: python3-oslotest >= 1.10.0
BuildRequires: python3-six >= 1.10.0
BuildRequires: python3-stevedore
BuildRequires: python3-PyYAML
BuildRequires: python3-testscenarios
BuildRequires: python3-testrepository
BuildRequires: python3-testtools
BuildRequires: python3-oslotest
BuildRequires: python3-requests-mock

%if 0%{?repo_bootstrap} == 0
BuildRequires: python3-oslo-log
%endif

%description -n python3-%{pypi_name}
The Oslo project intends to produce a python library containing
infrastructure code shared by OpenStack projects. The APIs provided
by the project should be high quality, stable, consistent and generally
useful.

The oslo-config library is a command line and configuration file
parsing library from the Oslo project.
%endif

%prep
%autosetup -n %{sname}-%{upstream_version} -S git
# Remove shebang from non executable file, it's used by the oslo-config-validator binary.
sed -i '/\/usr\/bin\/env/d' oslo_config/validator.py
# let RPM handle deps
rm -rf {test-,}requirements.txt

# Remove tests requiring sphinx if sphinx is not available
%if 0%{?with_doc} == 0
rm oslo_config/tests/test_sphinxext.py
rm oslo_config/tests/test_sphinxconfiggen.py
%endif

%build
%if 0%{?with_python3}
%py3_build
%endif
%py2_build

%if 0%{?with_doc}
export PYTHONPATH=.
sphinx-build -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%if 0%{?with_python3}
%py3_install
pushd %{buildroot}/%{_bindir}
for i in generator validator
do
mv oslo-config-$i oslo-config-$i-%{python3_version}
ln -s oslo-config-$i-%{python3_version} oslo-config-$i-3
done
# Let's keep backwards compatibility for some time
ln -s oslo-config-generator-%{python3_version} python3-oslo-config-generator

popd
%endif
%py2_install
pushd %{buildroot}/%{_bindir}
for i in generator validator
do
mv oslo-config-$i oslo-config-$i-%{python2_version}
ln -s oslo-config-$i-%{python2_version} oslo-config-$i-2
ln -s oslo-config-$i-%{python2_version} oslo-config-$i
done
popd

%check
%if 0%{?repo_bootstrap} == 0
PYTHON=python2 %{__python2} setup.py test
%if 0%{?with_python3}
rm -rf .testrepository
PYTHON=python3 %{__python3} setup.py test
%endif
%endif

%files -n python2-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/oslo-config-generator
%{_bindir}/oslo-config-generator-2*
%{_bindir}/oslo-config-validator
%{_bindir}/oslo-config-validator-2*
%{python2_sitelib}/oslo_config
%{python2_sitelib}/*.egg-info

%if 0%{?with_doc}
%files -n python2-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/oslo-config-generator-3*
%{_bindir}/python3-oslo-config-generator
%{_bindir}/oslo-config-validator-3*
%{python3_sitelib}/oslo_config
%{python3_sitelib}/*.egg-info
%endif

%changelog
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/oslo.config/commit/?id=dea9af2fe91e3abe6ca88ea8739cff023191abb9
