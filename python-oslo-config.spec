%global sname oslo-config
%global btag b3

Name:       python-oslo-config
Version:    2013.1
Release:    0.1.%{btag}%{?dist}
Summary:    OpenStack common configuration library

Group:      Development/Languages
License:    ASL 2.0
URL:        https://launchpad.net/oslo
Source0:    http://tarballs.openstack.org/%{sname}/%{sname}-%{version}%{btag}.tar.gz

# See https://review.openstack.org/22134
Source1:    LICENSE

BuildArch:  noarch
Requires:   python-setuptools

BuildRequires: python2-devel
BuildRequires: python-setuptools

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

%description doc
Documentation for the oslo-config library.

%prep
%setup -q -n %{sname}-%{version}%{btag}
# Remove bundled egg-info
rm -rf oslo_config.egg-info
# let RPM handle deps
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

cp %{SOURCE1} .

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/tests

export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html -d build/doctrees   source build/html
popd
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo

%check

%files
%doc README
%{python_sitelib}/oslo
%{python_sitelib}/*.egg-info
%{python_sitelib}/*-nspkg.pth

%files doc
%doc LICENSE doc/build/html

%changelog
* Sun Feb 17 2013 Mark McLoughlin <markmc@redhat.com> 2013.1-0.1.b3
- Initial package (#912023).
