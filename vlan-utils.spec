%define rname vlan

Summary:	Utilities for controlling vlans
Name:		%{rname}-utils
Version:	1.9
Release:	8
License:	GPL
Group:		System/Kernel and hardware
URL:		http://www.candelatech.com/~greear/vlan.html 
Source0:	http://www.candelatech.com/~greear/vlan/vlan.%{version}.tar.gz
Patch0:		vlan-1.6-mdkconf.patch
Patch1:		vlan.1.9-format_not_a_string_literal_and_no_format_arguments.diff
Patch2:		vlan.1.9-nostrip.diff
BuildRequires:	kernel-headers >= 2.4.14 lynx
Provides:	vconfig
Obsoletes:	vconfig
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%make RPM_OPT_FLAGS="%{optflags}" LDFLAGS="%{ldflags}" vconfig

%install
rm -rf %{buildroot}

install -m755 vconfig -D %{buildroot}/sbin/vconfig
install -m755 vlan_test.pl -D %{buildroot}/sbin/vlan-test
install -m644 vconfig.8 -D %{buildroot}%{_mandir}/man8/vconfig.8

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGELOG contrib README vlan.html
/sbin/*
%{_mandir}/man8/vconfig.8*


%changelog
* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 1.9-5mdv2011.0
+ Revision: 670771
- mass rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 1.9-4mdv2011.0
+ Revision: 608126
- rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 1.9-3mdv2010.1
+ Revision: 519080
- rebuild

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.9-2mdv2010.0
+ Revision: 427495
- rebuild

* Tue Dec 23 2008 Oden Eriksson <oeriksson@mandriva.com> 1.9-1mdv2009.1
+ Revision: 317921
- 1.9
- new url
- fix build with -Werror=format-security (P1)
- don't strip
- use %%ldflags

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 1.8-7mdv2009.0
+ Revision: 225920
- rebuild

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 1.8-6mdv2008.1
+ Revision: 152812
- remove useless kernel require
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Sep 19 2007 Antoine Ginies <aginies@mandriva.com> 1.8-5mdv2008.0
+ Revision: 91217
- increase release an rebuild to fix lost in space 32bits package


* Sat Mar 17 2007 Oden Eriksson <oeriksson@mandriva.com> 1.8-4mdv2007.1
+ Revision: 145487
- Import vlan-utils

* Sat Mar 17 2007 Oden Eriksson <oeriksson@mandriva.com> 1.8-4mdv2007.1
- use the %%mrel macro
- bunzip patches

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.8-3mdk
- Rebuild

* Sun Jan 23 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.8-2mdk
- rebuild
- fix summary-ended-with-dot

