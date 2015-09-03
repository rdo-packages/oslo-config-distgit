%global sname oslo.config
%global pypi_name oslo-config

%if 0%{?fedora}
%global with_python3 1
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:       python-oslo-config
Epoch:      2
Version:    2.4.0
Release:    1%{?dist}
Summary:    OpenStack common configuration library

Group:      Development/Languages
License:    ASL 2.0
URL:        https://launchpad.net/oslo
Source0:    https://pypi.python.org/packages/source/o/%{sname}/%{sname}-%{version}.tar.gz

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

Requires:   python-setuptools
Requires:   python-argparse
Requires:   python-six >= 1.9.0
Requires:   python-netaddr
Requires:   python-stevedore
Requires:   python-pbr

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr
BuildRequires: python-oslotest

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

BuildRequires: python-sphinx
BuildRequires: python-fixtures
BuildRequires: python-oslo-sphinx >= 2.3.0
BuildRequires: python-netaddr
BuildRequires: python-stevedore

%description -n python2-%{pypi_name}-doc
Documentation for the oslo-config library.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:    OpenStack common configuration library
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:   python3-setuptools
Requires:   python3-six >= 1.9.0
Requires:   python3-netaddr
Requires:   python3-stevedore
Requires:   python3-pbr

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-netaddr
BuildRequires: python3-stevedore
BuildRequires: python3-pbr
# FIXME when python3-oslotest is available
# Depends on python-mox3 under review:
# https://bugzilla.redhat.com/show_bug.cgi?id=1259333
#BuildRequires: python3-oslotest

%description -n python3-%{pypi_name}
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

# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/tests

export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html -d build/doctrees  source build/html
popd

%check
%{__python2} setup.py test
%if 0%{?with_python3}
# FIXME when python3-oslotest is available
#%{__python3} setup.py test
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
* Thu Sep 03 2015 Alan Pevec <alan.pevec@redhat.com> 2:2.4.0-1
- Update to upstream 2.4.0

* Mon Aug 17 2015 Alan Pevec <alan.pevec@redhat.com> 2:2.2.0-1
- Update to upstream 2.2.0

* Thu Jul 23 2015 Alan Pevec <alan.pevec@redhat.com> 2:2.0.0-1
- Update to upstream 2.0.0

* Thu Jun 25 2015 Alan Pevec <alan.pevec@redhat.com> 2:1.12.1-1
- Update to upstream 1.12.1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 27 2015 Alan Pevec <alan.pevec@redhat.com> 2:1.9.3-1
- Update to upstream 1.9.3

* Mon Feb 23 2015 Alan Pevec <alan.pevec@redhat.com> 2:1.7.0-1
- Update to upstream 1.7.0

* Sat Sep 20 2014 Alan Pevec <apevec@redhat.com> - 2:1.4.0
- Final 1.4.0 release, Epoch bumped to make 1.4.0 win over 1.4.0.0

* Wed Sep 17 2014 Alan Pevec <apevec@redhat.com> - 1:1.4.0.0-0.4.a5
- Update to 1.4.0.0a5 milestone

* Wed Sep 17 2014 Haïkel Guémar <hguemar@fedoraproject.org> - 1:1.4.0.0-0.3.a3
- Rename python3 subpackage

* Mon Sep 15 2014 Haïkel Guémar <hguemar@fedoraproject.org> - 1:1.4.0.0-0.2.a3
- Add python3 subpackage

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Oct 11 2013 Alan Pevec <apevec@redhat.com> - 1.2.1-1
- Update to 1.2.1

* Tue Aug 20 2013 apevec@redhat.com 1.2.0-0.5.a3
- Look also for $prog-dist.conf for glance-manage

* Thu Aug 8 2013 pbrady@redhat.com - 1:1.2.0-0.4.a3
- Look for /usr/share/$project/$project-dist.conf by default

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.0-0.3.a3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 pbrady@redhat.com - 1:1.2.0-0.2.a3
- Update to 1.2.0a3 milestone

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
