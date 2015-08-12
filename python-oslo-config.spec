%global sname oslo.config
%global milestone a5

%if 0%{?fedora}
%global with_python3 1
%endif

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
Requires:   python-setuptools
Requires:   python-argparse
Requires:   python-six >= 1.9.0
Requires:   python-netaddr
Requires:   python-stevedore
Requires:   python-pbr

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr

%description
The Oslo project intends to produce a python library containing
infrastructure code shared by OpenStack projects. The APIs provided
by the project should be high quality, stable, consistent and generally
useful.

The oslo-config library is a command line and configuration file
parsing library from the Oslo project.

%package doc
Summary:    Documentation for OpenStack common configuration library
Group:      Documentation

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx >= 2.3.0
BuildRequires: python-netaddr
BuildRequires: python-stevedore

%description doc
Documentation for the oslo-config library.

%if 0%{?with_python3}
%package -n python3-oslo-config
Summary:    OpenStack common configuration library

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr

%description -n python3-oslo-config
The Oslo project intends to produce a python library containing
infrastructure code shared by OpenStack projects. The APIs provided
by the project should be high quality, stable, consistent and generally
useful.

The oslo-config library is a command line and configuration file
parsing library from the Oslo project.
%endif

%prep
%setup -q -n %{sname}-%{upstream_version}

%patch0001 -p1

# let RPM handle deps
rm -f requirements.txt

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%if 0%{?with_python3}
# we build the python3 version first not to crush the python2
# version of oslo-config-generator
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/oslo-config-generator \
   %{buildroot}%{_bindir}/python3-oslo-config-generator
# FIXME: documentation not built due to non-python3
popd
%endif

%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/tests

export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html -d build/doctrees   source build/html
popd
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo

%check

%files
%doc README.rst LICENSE
%{_bindir}/oslo-config-generator
%{python2_sitelib}/oslo_config
%{python2_sitelib}/*.egg-info

%files doc
%doc LICENSE doc/build/html

%if 0%{?with_python3}
%files -n python3-oslo-config
%doc README.rst LICENSE
%{_bindir}/python3-oslo-config-generator
%{python3_sitelib}/oslo_config
%{python3_sitelib}/*.egg-info
%endif

%changelog
