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

Patch0001: 0001-add-usr-share-project-dist.conf-to-the-default-confi.patch

BuildArch:  noarch

%description
The Oslo project intends to produce a python library containing
infrastructure code shared by OpenStack projects. The APIs provided
by the project should be high quality, stable, consistent and generally
useful.

The oslo-config library is a command line and configuration file
parsing library from the Oslo project.

%package -n python%{pyver}-%{pypi_name}
Summary:    OpenStack common configuration library
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}
%if %{pyver} == 3
Obsoletes: python2-%{pypi_name} < %{version}-%{release}
%endif

Requires:   python%{pyver}-oslo-i18n >= 3.15.3
Requires:   python%{pyver}-rfc3986 >= 1.2.0
Requires:   python%{pyver}-pbr
Requires:   python%{pyver}-requests >= 2.18.0
Requires:   python%{pyver}-stevedore >= 1.20.0
Requires:   python%{pyver}-debtcollector >= 1.2.0
Requires:   python%{pyver}-netaddr >= 0.7.18
%if %{pyver} == 2
Requires:   python-enum34
Requires:   PyYAML >= 3.10
%else
Requires:   python%{pyver}-PyYAML >= 3.10
%endif

BuildRequires: python%{pyver}-devel
BuildRequires: python%{pyver}-setuptools
BuildRequires: python%{pyver}-oslo-i18n
BuildRequires: python%{pyver}-rfc3986
BuildRequires: python%{pyver}-pbr
BuildRequires: git
# Required for tests
BuildRequires: python%{pyver}-testscenarios
BuildRequires: python%{pyver}-stestr
BuildRequires: python%{pyver}-testtools
BuildRequires: python%{pyver}-oslotest
BuildRequires: python%{pyver}-requests-mock
BuildRequires: python%{pyver}-netaddr
BuildRequires: python%{pyver}-stevedore
%if %{pyver} == 2
BuildRequires: python-enum34
BuildRequires: PyYAML
%else
BuildRequires: python%{pyver}-PyYAML
%endif

%if 0%{?repo_bootstrap} == 0
BuildRequires: python%{pyver}-oslo-log
%endif

%description -n python%{pyver}-%{pypi_name}
The Oslo project intends to produce a python library containing
infrastructure code shared by OpenStack projects. The APIs provided
by the project should be high quality, stable, consistent and generally
useful.

The oslo-config library is a command line and configuration file
parsing library from the Oslo project.

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:    Documentation for OpenStack common configuration library

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-fixtures
BuildRequires: python%{pyver}-openstackdocstheme
BuildRequires: python%{pyver}-oslotest >= 1.10.0
BuildRequires: python%{pyver}-stevedore
BuildRequires: python%{pyver}-sphinxcontrib-apidoc

%description -n python-%{pypi_name}-doc
Documentation for the oslo-config library.
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
%{pyver_build}

%if 0%{?with_doc}
export PYTHONPATH=.
sphinx-build-%{pyver} -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}
pushd %{buildroot}/%{_bindir}
for i in generator validator
do
ln -s oslo-config-$i oslo-config-$i-%{pyver}
done
popd

%check
%if 0%{?repo_bootstrap} == 0
PYTHON=%{pyver_bin} stestr-%{pyver} run
%endif

%files -n python%{pyver}-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/oslo-config-generator
%{_bindir}/oslo-config-generator-%{pyver}
%{_bindir}/oslo-config-validator
%{_bindir}/oslo-config-validator-%{pyver}
%{pyver_sitelib}/oslo_config
%{pyver_sitelib}/*.egg-info

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
