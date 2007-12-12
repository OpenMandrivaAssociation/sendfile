Summary:	Asynchronous file transfer service
Name:		sendfile
Version:	2.1a
Release:	2mdk
License:	GPL
Group:		Networking/File transfer
URL:		http://www.belwue.de/projekte/saft/sendfile.html
Source:		%{name}-%{version}.tar.bz2
Source1:	sendfile-xinetd
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	xinetd

%description
Sendfile is an asynchronous file transfer service for the Internet, like the
sendfile facility in Bitnet: Any user A can send files to another user B
without B being active in any way.

Sendfile which is an implementation of the SAFT protocol (Simple Asynchronous
File Transfer) offers you a true asynchronous file transfer service for the
Internet. Virtually any form of file can be sent, including encrypted ones.

The sendfile package contains 5 main programs:
  sendfiled  - the sendfile daemon which will be started by inetd
  sendfile   - the sendfile client for sending files
  sendmsg    - the send-message client for sending one-line text messages
  receive    - the receive client for picking up already received files
  fetchfile  - the O-SAFT client to obtain files from a remote SAFT server


%prep
%setup -q

%build
%make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf %buildroot

# install isn't good, so we do it by hand...
%__install -d %buildroot/%_sbindir
%__install src/sendfiled %buildroot/%_sbindir/
%__install -d %buildroot/%_var/spool/sendfile/LOG
%__install -d %buildroot/%_var/spool/sendfile/OUTGOING
%__install -d %buildroot/%_sysconfdir
%__install etc/sendfile.deny %buildroot/%_sysconfdir/
%__install etc/sendfile.cf %buildroot/%_sysconfdir/
%__install -D %SOURCE1 %buildroot/%_sysconfdir/xinetd.d/sendfile
%__install -d %buildroot/%_mandir/man1/
%__install doc/*.1 %buildroot/%_mandir/man1/
%__install -d %buildroot/%_mandir/man1
%__install -D etc/check_sendfile %buildroot/%_sysconfdir/profile.d/sendfile-check.sh
%__install -d %buildroot/%_bindir
%__install src/{sendfile,sendmsg,receive,fetchfile,utf7encode,wlock} %buildroot/%_bindir/
ln -s utf7encode %buildroot/%_bindir/utf7decode
%__install etc/{sfconf,sfdconf} %buildroot/%_bindir/

%clean
rm -rf %buildroot

%post
service xinetd reload

%postun
service xinetd reload

%files
%defattr(0755,root,root,0755)
%_sbindir/*
%_bindir/*
%defattr(0644,root,root,0755)
%doc doc/AUTHORS doc/COPYING doc/ChangeLog doc/doc.txt doc/doku.txt
%doc doc/features doc/LIESMICH* doc/README* doc/THANKS doc/vorteile
%dir %_var/spool/sendfile
%attr(0700,root,root) %dir %_var/spool/sendfile/LOG
%attr(1777,root,root) %dir %_var/spool/sendfile/OUTGOING
%config(noreplace) %_sysconfdir/sendfile.*
%config(noreplace) %_sysconfdir/profile.d/*
%config(noreplace) %_sysconfdir/xinetd.d/*
%_mandir/*/*

