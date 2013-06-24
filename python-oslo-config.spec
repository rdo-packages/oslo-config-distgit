%global sname oslo.config
%global milestone a2

Name:       python-oslo-config
Epoch:      1
Version:    1.2.0
Release:    0.1.%{milestone}%{?dist}
Summary:    OpenStack common configuration library

Group:      Development/Languages
License:    ASL 2.0
URL:        https://launchpad.net/oslo
Source0:    http://tarballs.openstack.org/oslo-config/%{sname}-%{version}%{milestone}.tar.gz

BuildArch:  noarch
Requires:   python-setuptools
Requires:   python-argparse

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
%setup -q -n %{sname}-%{version}%{milestone}

sed -i 's/%{version}%{milestone}/%{version}/' PKG-INFO

# Remove bundled egg-info
rm -rf %{sname}.egg-info
# let RPM handle deps
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

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
%doc README.rst
%{python_sitelib}/oslo
%{python_sitelib}/*.egg-info

%files doc
%doc LICENSE doc/build/html

%changelog
* Mon Jun 24 2013 apevec@redhat.com - 1:1.2.0-0.1.a2
- Update to 1.2.0a2 milestone

* Tue Mar 12 2013 Mark McLoughlin <markmc@redhat.com> - 1:1.1.0-1
- Update to 1.1.0 final.

* Wed Mar  6 2013 Mark McLoughlin <markmc@redhat.com> - 1.1.0-0.1.b1
- Update to 1.1.0b1, bump epoch

* Tue Mar  5 2013 Mark McLoughlin <markmc@redhat.com> - 2013.1-0.1.b5
- Update to 2013.1b5
- Require python-argparse (#917937)

* Fri Feb 22 2013 Mark McLoughlin <markmc@redhat.com> - 2013.1-0.1.b4
- Update to 2013.1b4

* Sun Feb 17 2013 Mark McLoughlin <markmc@redhat.com> - 2013.1-0.1.b3
- Initial package (#912023).
