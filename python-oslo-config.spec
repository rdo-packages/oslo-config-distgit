%global sname oslo.config
%global pypi_name oslo-config
%global milestone a5

%if 0%{?fedora}
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
URL:        https://launchpad.net/oslo
Source0:    http://tarballs.openstack.org/oslo.config/oslo.config-master.tar.gz

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
# python_provide does not exist in CBS Cloud buildroot
Provides:   python-%{pypi_name} = %{epoch}:%{upstream_version}
Obsoletes:  python-%{pypi_name} < %{epoch}:%{upstream_version}

Requires:   python-argparse
Requires:   python-netaddr >= 0.7.12
Requires:   python-oslo-i18n >= 2.1.0
Requires:   python-rfc3986 >= 0.2.0
Requires:   python-pbr
Requires:   python-setuptools
Requires:   python-six >= 1.9.0
Requires:   python-stevedore >= 1.10.0
Requires:   python-debtcollector >= 1.2.0

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-oslo-i18n
BuildRequires: python-rfc3986
BuildRequires: python-pbr
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
# python_provide does not exist in CBS Cloud buildroot
Provides:   python-%{pypi_name}-doc = %{epoch}:%{upstream_version}
Obsoletes:  python-%{pypi_name}-doc < %{epoch}:%{upstream_version}

BuildRequires: python-fixtures
BuildRequires: python-netaddr
BuildRequires: python-oslo-sphinx >= 2.3.0
BuildRequires: python-oslotest >= 1.10.0
BuildRequires: python-sphinx
BuildRequires: python-stevedore

%description -n python2-%{pypi_name}-doc
Documentation for the oslo-config library.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:    OpenStack common configuration library
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:   python3-netaddr >= 0.7.12
Requires:   python3-oslo-i18n >= 2.1.0
Requires:   python3-rfc3986 >= 0.2.0
Requires:   python3-pbr
Requires:   python3-setuptools
Requires:   python3-six >= 1.9.0
Requires:   python3-stevedore >= 1.10.0
Requires:   python3-debtcollector >= 1.2.0

BuildRequires: python3-devel
BuildRequires: python3-oslo-i18n
BuildRequires: python3-rfc3986
BuildRequires: python3-pbr
BuildRequires: python3-setuptools
BuildRequires: git
# Required for tests
BuildRequires: python3-fixtures
BuildRequires: python3-netaddr
BuildRequires: python3-oslo-sphinx >= 2.3.0
BuildRequires: python3-oslotest >= 1.10.0
BuildRequires: python3-six >= 1.9.0
BuildRequires: python3-stevedore

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

export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html -d build/doctrees  source build/html
popd

%check
%{__python2} setup.py test
%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py test
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
# REMOVEME: error caused by commit 
