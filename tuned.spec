Summary: A dynamic adaptive system tuning daemon
Name: tuned
Version: 0.1.0
Release: 1%{?dist}
License: GPLv2+
Group: System Environment/Daemons
# The source for this package was pulled from upstream git.  Use the
# following commands to get the corresponding tarball:
#  git clone git://fedorapeople.org/~pknirsch/tuned.git/
#  cd tuned
#  git checkout v%{version}
#  make archive
Source: tuned-%{version}.tar.bz2
URL: http://fedorapeople.org/~pknirsch/git/tuned.git/
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(postun): initscripts
BuildArch: noarch

%description
The tuned package contains a daemon that tunes system settings dynamically.

%package utils
Summary: Disk and net monitoring systemtap scripts
Requires: systemtap kernel-debuginfo
Group: Applications/System

%description utils
The tuned-utils package contains several systemtap scripts to allow detailed
manual monitoring of the system.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%post
/sbin/chkconfig --add tuned

%preun
if [ $1 = 0 ] ; then
    /sbin/service tuned stop >/dev/null 2>&1
    /sbin/chkconfig --del tuned
fi

%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service tuned condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README doc/README.txt doc/TIPS.txt
%{_initddir}/tuned
%config(noreplace) %{_sysconfdir}/tuned.conf
%{_sbindir}/tuned
%{_datadir}/tuned
%{_mandir}/man8/*

%files utils
%defattr(-,root,root,-)
%{_sbindir}/netdevstat
%{_sbindir}/diskdevstat


%changelog
* Mon Feb 23 2009 Phil Knirsch <pknirsch@redhat.com> - 0.1.0-1
- Initial version
