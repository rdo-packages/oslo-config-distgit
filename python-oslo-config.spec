%global sname oslo.config
%global pypi_name oslo-config

%if 0%{?fedora}
%global with_python3 1
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:       python-oslo-config
Epoch:      2
Version:    5.2.1
Release:    1%{?dist}
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
Requires:   python2-rfc3986 >= 0.3.1
Requires:   python2-pbr
Requires:   python2-six >= 1.10.0
Requires:   python2-stevedore >= 1.20.0
Requires:   python2-debtcollector >= 1.2.0
%if 0%{?fedora} > 0
Requires:   python2-netaddr >= 0.7.18
Requires:   python2-pyyaml >= 3.10
%else
Requires:   python-netaddr >= 0.7.18
Requires:   PyYAML >= 3.10
%endif

BuildRequires: python2-devel
BuildRequires: python2-setuptools
BuildRequires: python2-oslo-i18n
BuildRequires: python2-rfc3986
BuildRequires: python2-pbr
BuildRequires: git

%description -n python2-%{pypi_name}
The Oslo project intends to produce a python library containing
infrastructure code shared by OpenStack projects. The APIs provided
by the project should be high quality, stable, consistent and generally
useful.

The oslo-config library is a command line and configuration file
parsing library from the Oslo project.

%package -n python2-%{pypi_name}-doc
Summary:    Documentation for OpenStack common configuration library
%{?python_provide:%python_provide python2-%{pypi_name}-doc}

BuildRequires: python2-fixtures
BuildRequires: python2-openstackdocstheme
BuildRequires: python2-oslotest >= 1.10.0
BuildRequires: python2-sphinx
BuildRequires: python2-stevedore
%if 0%{?fedora} > 0
BuildRequires: python2-netaddr
BuildRequires: python2-pyyaml
%else
BuildRequires: python-netaddr
BuildRequires: PyYAML
%endif

%description -n python2-%{pypi_name}-doc
Documentation for the oslo-config library.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:    OpenStack common configuration library
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:   python3-netaddr >= 0.7.18
Requires:   python3-oslo-i18n >= 3.15.3
Requires:   python3-rfc3986 >= 0.3.1
Requires:   python3-pbr
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
BuildRequires: python3-openstackdocstheme
BuildRequires: python3-oslotest >= 1.10.0
BuildRequires: python3-six >= 1.10.0
BuildRequires: python3-stevedore
BuildRequires: python3-PyYAML

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

# let RPM handle deps
rm -rf {test-,}requirements.txt

%build
%{__python2} setup.py build
%if 0%{?with_python3}
%{__python3} setup.py build
%endif

%install
%if 0%{?with_python3}
# we build the python3 version first not to crush the python2
# version of oslo-config-generator
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/oslo-config-generator \
   %{buildroot}%{_bindir}/python3-oslo-config-generator
%endif
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%check
# Tests disabled because of https://review.openstack.org/#/c/334858
# Re-enable them when it's fixed.
%{__python2} setup.py test || :
%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py test || :
%endif

%files -n python2-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/oslo-config-generator
%{python2_sitelib}/oslo_config
%{python2_sitelib}/*.egg-info

%files -n python2-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/python3-oslo-config-generator
%{python3_sitelib}/oslo_config
%{python3_sitelib}/*.egg-info
%endif

%changelog
* Wed Jan 23 2019 RDO <dev@lists.rdoproject.org> 2:5.2.1-1
- Update to 5.2.1

* Sat Feb 10 2018 RDO <dev@lists.rdoproject.org> 2:5.2.0-1
- Update to 5.2.0

