%define rname vlan

Summary:	Utilities for controlling vlans
Name:		%{rname}-utils
Version:	1.9
Release:	19
License:	GPL
Group:		System/Kernel and hardware
URL:		http://www.candelatech.com/~greear/vlan.html 
Source0:	http://www.candelatech.com/~greear/vlan/vlan.%{version}.tar.gz
Patch0:		vlan-1.6-mdkconf.patch
Patch1:		vlan.1.9-format_not_a_string_literal_and_no_format_arguments.diff
Patch2:		vlan.1.9-nostrip.diff
BuildRequires:	kernel-headers lynx
Provides:	vconfig
Obsoletes:	vconfig

%description
Virtual networking refers to the ability of switches and routers to
configure logical topologies on top of the physical network
infrastructure, allowing any arbitrary collection of LAN segments
within a network to be combined into an autonomous user group,
appearing as a single LAN.

This package implement support (along with the kernel patch) :

     * Implements 802.1Q VLAN spec.
     * Can support up to 4094 VLANs per ethernet interface.
     * Scales well in critical paths: O(n), where n is the number of
       PHYSICAL ethernet interfaces, and that is only on ingress. O(1) in
       every other critical path, as far as I know.
     * Supports MULTICAST
     * Can change MAC address of VLAN.
     * Multiple naming conventions supported, and adjustable at runtime.
     * Optional header-reordering, to make the VLAN interface look JUST
       LIKE an Ethernet interface. This fixes some problems with DHCPd
       and anything else that uses a SOCK_PACKET socket. Default setting
       is off, which works for every other protocol I know about, and is
       slightly faster.

%prep

%setup -q -n %{rname}
%patch0 -p1 -b .mdkconf
%patch1 -p0 -b .format_not_a_string_literal_and_no_format_arguments
%patch2 -p0 -b .nostrip

rm -rf `find -type d -name CVS`

%build
make clean
rm -f macvlan_config vconfig *.o
%make CC=%{__cc} RPM_OPT_FLAGS="%{optflags}" LDFLAGS="%{ldflags}" vconfig

%install
install -m755 vconfig -D %{buildroot}/sbin/vconfig
install -m755 vlan_test.pl -D %{buildroot}/sbin/vlan-test
install -m644 vconfig.8 -D %{buildroot}%{_mandir}/man8/vconfig.8

%files
%doc CHANGELOG contrib README vlan.html
/sbin/*
%{_mandir}/man8/vconfig.8*
