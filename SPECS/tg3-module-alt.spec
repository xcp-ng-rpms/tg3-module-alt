%define vendor_name Broadcom
%define vendor_label broadcom
%define driver_name tg3
%define module_dir override

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}-alt
Version: 3.139j
Release: 1%{?dist}
License: GPLv2

# New comment:
# Source extracted from Broadcom.com
# URL: https://docs.broadcom.com/docs/1232743257
Source: tg3-%{version}.tar.gz

Patch0: Makefile.patch

BuildRequires: gcc
BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n tg3-%{version}

%build
%{?cov_wrap} %{__make} KVER=%{kernel_version}

%install
%{?cov_wrap} %{__make} PREFIX=%{buildroot} KVER=%{kernel_version} BCMMODDIR=/lib/modules/%{kernel_version}/%{module_dir} DEPMOD=/bin/true install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+wx

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%changelog
* Tue Dec 12 2023 Gael Duperrey <gduperrey@vates.tech> - 3.319j.1
- Initial package: version 3.319j
- Synced from broadcom.com

