#Module-Specific definitions
%define mod_name mod_dnssd
%define mod_conf A47_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Mod_dnssd adds DNS-SD Zeroconf support to Apache 2.0 using Avahi
Name:		apache-%{mod_name}
Version:	0.4
Release:	%mkrel 3
Group:		System/Servers
License:	Apache License
URL:		http://0pointer.de/lennart/projects/mod_dnssd/
Source0:	http://0pointer.de/lennart/projects/mod_dnssd/mod_dnssd-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
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
mod_dnssd is an Apache module which adds Zeroconf support via
DNS-SD using Avahi.

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p0

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
rm -f configure
libtoolize --force --copy; aclocal-1.8 ; autoheader; automake-1.8 --add-missing --copy --foreign; autoconf

#%{_sbindir}/apxs -c src/mod_dnssd.c -Wl,-lavahi-common -Wl,-lavahi-client  

%configure2_5x

%make


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 src/.libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

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


