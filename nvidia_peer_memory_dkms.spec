Name:		nvidia_peer_memory
Version:	1.3
Release:	1%{?dist}
Summary:	nvidia_peer_memory

Group:		System Environment/Libraries
License:	GPL
URL:		http://www.mellanox.com
Source0:	%{name}-%{version}.tar.gz

BuildRequires:	gcc kernel-headers
Requires:	dkms gcc bash

%description

nvidia peer memory kernel module.

%prep
%setup -n %{name}-%{version} -q

%install
mkdir -p %{buildroot}/usr/src/%{name}-%{version}/
cp -r * %{buildroot}/usr/src/%{name}-%{version}
mkdir -p %{buildroot}/etc/infiniband
cp nv_peer_mem.conf %{buildroot}/etc/infiniband/
mkdir -p %{buildroot}/etc/init.d
cp nv_peer_mem %{buildroot}/etc/init.d/

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root)
%attr(0755,root,root) /usr/src/%{name}-%{version}/
/etc/infiniband/nv_peer_mem.conf
%attr(0755,root,root) /etc/init.d/nv_peer_mem

%post
if ! dkms status -m %{name} | egrep %{name}/%{version},; then
   /usr/sbin/dkms add -m %{name} -v %{version}
fi
/usr/sbin/dkms build -m %{name} -v %{version}
/usr/sbin/dkms install -m %{name} -v %{version}
exit 0

%preun
/usr/bin/systemctl stop nv_peer_mem
/usr/sbin/dkms remove -m %{name} -v %{version} --all
exit 0
