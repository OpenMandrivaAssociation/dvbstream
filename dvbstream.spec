# Define Mandrake Linux version we are building for
%define mdkversion %(perl -pe '/(\\d+)\\.(\\d)\\.?(\\d)?/; $_="$1$2".($3||0)' /etc/mandrake-release)


%if %mdkversion < 1000
%define kernel_rel 2.4.22-28.tmb.1mdk
%define kernel_dir /usr/src/linux-%{kernel_rel}
%define kernel_inc %kernel_dir/3rdparty/mod_dvb/include
%else
#define kernel_rel 2.6.3-7mdk
%define kernel_dir /usr/src/linux
#-{kernel_rel}
%define kernel_inc %kernel_dir/include
%endif

Summary:	Dvbstream
Name:		dvbstream
Version:	0.8.2
Release:	1
#Source0:	http://osdn.dl.sourceforge.net/dvbtools/%{name}-%{version}.tar.bz2
Source0:	http://www.orcas.net/dvbstream/dvbstream-%{version}.tar.bz2
URL:		https://www.linuxstb.org
License:	GPL
Group:		Video
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	pkgconfig(ncurses)
Prefix:		%{_prefix}

%description
 DVBstream is based on the ts-rtp package available at
 http://www.linuxtv.org.  It broadcasts a (subset of a) DVB transport
 stream over a LAN using the rtp protocol.  There were a couple of
 small bugs in the original ts-rtp application, which I have fixed
 here.

%prep
%autosetup -n %{name} -p1

%build
#UK
make INCS=-I%kernel_inc
install -m755 dvbstream dvbstream-uk
install -m755 dumprtp dvb_dumprtp-uk
install -m755 rtpfeed dvb_rtpfeed-uk
install -m755 ts_filter dvb_ts_filter-uk
make clean
#Finland
make INCS=-I%kernel_inc FINLAND=1
install -m755 dvbstream dvbstream-fin
install -m755 dumprtp dvb_dumprtp-fin
install -m755 rtpfeed dvb_rtpfeed-fin
install -m755 ts_filter dvb_ts_filter-fin
make clean

make INCS=-I%kernel_inc FINLAND2=1
install -m755 dvbstream dvbstream-fin2
install -m755 dumprtp dvb_dumprtp-fin2
install -m755 rtpfeed dvb_rtpfeed-fin2
install -m755 ts_filter dvb_ts_filter-fin2

%install
rm -rf $RPM_BUILD_ROOT
install -d -m755 %buildroot%_bindir
install -m755 dvbstream-* %buildroot%_bindir/
install -m755 dvb_dumprtp* %buildroot%_bindir/
install -m755 dvb_rtpfeed* %buildroot%_bindir/
install -m755 dvb_ts_filter* %buildroot%_bindir/

install -d -m755 %buildroot%_libdir/%name
install TELNET/* %buildroot%_libdir/%name/

echo "update-alternatives --install %_bindir/dvbstream dvbstream %_bindir/dvbstream-uk 30 \\" >> dvbstream-setup-alternatives.sh
for i in dvb_dumprtp dvb_rtpfeed dvb_ts_filter ; do
	echo "--slave  %_bindir/$i $i %_bindir/$i-uk \\" >> dvbstream-setup-alternatives.sh
done
echo >> dvbstream-setup-alternatives.sh

echo "update-alternatives --install %_bindir/dvbstream dvbstream %_bindir/dvbstream-fin 20 \\" >> dvbstream-setup-alternatives.sh
for i in dvb_dumprtp dvb_rtpfeed dvb_ts_filter ; do
	echo "--slave  %_bindir/$i $i %_bindir/$i-fin \\" >> dvbstream-setup-alternatives.sh
done
echo >> dvbstream-setup-alternatives.sh


echo "update-alternatives --install %_bindir/dvbstream dvbstream %_bindir/dvbstream-fin2 10 \\" >> dvbstream-setup-alternatives.sh
for i in dvb_dumprtp dvb_rtpfeed dvb_ts_filter ; do
	echo "--slave  %_bindir/$i $i %_bindir/$i-fin2 \\" >> dvbstream-setup-alternatives.sh
done
echo >> dvbstream-setup-alternatives.sh

%post -f dvbstream-setup-alternatives.sh

%postun
if [ $1 = 0 ]; then
	update-alternatives --remove dvbstream %_bindir/dvbstream-uk
	update-alternatives --remove dvbstream %_bindir/dvbstream-fin
	update-alternatives --remove dvbstream %_bindir/dvbstream-fin2
fi
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README COPYING CHANGES
%_bindir/*
%dir %_libdir/%name
%_libdir/%name/*



%changelog
* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 0.5-4mdv2009.0
+ Revision: 244557
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Dec 04 2007 Thierry Vignaud <tv@mandriva.org> 0.5-2mdv2008.1
+ Revision: 115126
- use %%mkrel
- import dvbstream


* Tue Jun 08 2004 Svetoslav Slavtchev <svetljo@gmx.de> 0.5-3mdk
- initial contrib

* Sun Apr 04 2004 Svetoslav Slavtchev <svetljo@gmx.de> 0.5-2mdk
- fix group
- add changelog :-)
- rename spec to dvbstream (!dvbstream2)
  update-alternatives should be working :-)

* Sun Apr 04 2004 Svetoslav Slavtchev <svetljo@gmx.de> 0.5-1mdk
- initial build for club

