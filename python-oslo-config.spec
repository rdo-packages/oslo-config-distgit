%global sname oslo.config
%global milestone a5

%if 0%{?fedora}
%global with_python3 1
%endif

Name:       python-oslo-config
Epoch:      2
Version:    1.9.3
Release:    1%{?dist}
Summary:    OpenStack common configuration library

Group:      Development/Languages
License:    ASL 2.0
URL:        https://launchpad.net/oslo
Source0:    https://pypi.python.org/packages/source/o/%{sname}/%{sname}-%{version}.tar.gz

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
BuildRequires: python-d2to1

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

%description doc
Documentation for the oslo-config library.

%if 0%{?with_python3}
%package -n python3-oslo-config
Summary:    OpenStack common configuration library

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr
BuildRequires: python3-d2to1

%description -n python3-oslo-config
The Oslo project intends to produce a python library containing
infrastructure code shared by OpenStack projects. The APIs provided
by the project should be high quality, stable, consistent and generally
useful.

The oslo-config library is a command line and configuration file
parsing library from the Oslo project.
%endif

%prep
%setup -q -n %{sname}-%{version}

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
%{python2_sitelib}/oslo
%{python2_sitelib}/*.egg-info
%{python2_sitelib}/*-nspkg.pth

%files doc
%doc LICENSE doc/build/html

%if 0%{?with_python3}
%files -n python3-oslo-config
%doc README.rst LICENSE
%{_bindir}/python3-oslo-config-generator
%{python3_sitelib}/oslo_config
%{python3_sitelib}/oslo
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/*-nspkg.pth
%endif

%changelog
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
