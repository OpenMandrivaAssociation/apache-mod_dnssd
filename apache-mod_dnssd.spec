#Module-Specific definitions
%define mod_name mod_dnssd
%define mod_conf A47_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Mod_dnssd adds DNS-SD Zeroconf support to Apache 2.0 using Avahi
Name:		apache-%{mod_name}
Version:	0.6
Release:	%mkrel 7
Group:		System/Servers
License:	Apache License
URL:		http://0pointer.de/lennart/projects/mod_dnssd/
Source0:	http://0pointer.de/lennart/projects/mod_dnssd/mod_dnssd-%{version}.tar.gz
Source1:	%{mod_conf}
Patch0:		mod_dnssd-0.4-no_silly_checks_because_we_know_the_apache_version_is_ok.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
Requires:	apache-mod_dav >= 2.2.0
Requires:	apache-mod_userdir >= 2.2.0
BuildRequires:	autoconf2.5
BuildRequires:	automake1.8
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
BuildRequires:	libavahi-common-devel >= 0.6.4
BuildRequires:	libavahi-client-devel >= 0.6.4
BuildRequires:	lynx
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_dnssd is an Apache module which adds Zeroconf support via DNS-SD using
Avahi.

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p0

cp %{SOURCE1} %{mod_conf}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
rm -f configure
libtoolize --force --copy; aclocal-1.8 ; autoheader; automake-1.8 --add-missing --copy --foreign; autoconf

#%{_sbindir}/apxs -c src/mod_dnssd.c -Wl,-lavahi-common -Wl,-lavahi-client  

%configure2_5x --localstatedir=/var/lib

%make


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 src/.libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}%{_var}/www/html/addon-modules/%{name}-%{version}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE README doc/README.html doc/style.css
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 0.6-7mdv2012.0
+ Revision: 772621
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.6-6
+ Revision: 678307
- mass rebuild

* Thu Dec 02 2010 Paulo Andrade <pcpa@mandriva.com.br> 0.6-5mdv2011.0
+ Revision: 605079
- Rebuild with apr with workaround to issue with gcc type based alias analysis

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.6-4mdv2011.0
+ Revision: 587965
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 0.6-3mdv2010.1
+ Revision: 516093
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.6-2mdv2010.0
+ Revision: 406577
- rebuild

* Tue Feb 03 2009 Götz Waschk <waschk@mandriva.org> 0.6-1mdv2009.1
+ Revision: 336862
- update to new version 0.6

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 0.5-4mdv2009.0
+ Revision: 234936
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.5-3mdv2009.0
+ Revision: 215572
- fix rebuild
- hard code %%{_localstatedir}/lib to ease backports

* Thu Dec 20 2007 Olivier Blin <blino@mandriva.org> 0.5-2mdv2008.1
+ Revision: 135821
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 0.5-2mdv2008.0
+ Revision: 82563
- rebuild

* Wed Apr 18 2007 Oden Eriksson <oeriksson@mandriva.com> 0.5-1mdv2008.0
+ Revision: 14419
- 0.5


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.4-3mdv2007.1
+ Revision: 140669
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 0.4-2mdv2007.0
+ Revision: 79410
- Import apache-mod_dnssd

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 0.4-2mdv2007.0
- rebuild

* Sun Apr 02 2006 Oden Eriksson <oeriksson@mandriva.com> 0.4-1mdk
- 0.4 (Minor feature enhancements)

* Mon Jan 23 2006 Olivier Blin <oblin@mandriva.com> 0.3-1mdk
- 0.3
- drop Patch0 (merged upstream)

* Sun Jan 22 2006 Oden Eriksson <oeriksson@mandriva.com> 0.2-1mdk
- 0.2 (Minor bugfixes)
- added P0 to make it compile

* Thu Jan 19 2006 Oden Eriksson <oeriksson@mandriva.com> 0.1-1mdk
- initial Mandriva package

