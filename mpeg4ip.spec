Summary:	MPEG4IP - system for encoding, streaming and playing MPEG-4 audio/video
Summary(pl):	MPEG4IP - sytem kodowania, streamingu i odtwarzania d¼wiêku i obrazu MPEG-4
Name:		mpeg4ip
Version:	1.0
Release:	4
Epoch:		1
License:	MPL v1.1 (original code) and other licenses (included libraries)
Group:		Applications
Source0:	http://dl.sourceforge.net/mpeg4ip/%{name}-%{version}.tar.gz
# Source0-md5:	6ac635a1dd02d874054d6092f350157c
Patch0:		%{name}-system-SDL.patch
# don't use non-standard SDL_HasAudioDelayMsec() and SDL_AudioDelayMsec()
# an alternative is to patch system SDL adding those functions ???
Patch1:		%{name}-nosdlaudiodelay.patch
Patch2:		%{name}-xvid1.patch
Patch3:		%{name}-link.patch
Patch4:		%{name}-fmt.patch
Patch5:		%{name}-libsdp.patch
Patch6:		%{name}-types.patch
Patch7:		%{name}-pic.patch
#Patch8:		%{name}-system-rtp.patch
URL:		http://www.mpeg4ip.net/
BuildRequires:	SDL-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	faac-devel >= 1.20
BuildRequires:	gtk+2-devel >= 2.0.0
BuildRequires:	lame-libs-devel >= 3.92
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.4d
BuildRequires:	libvorbis-devel >= 1:1.0
BuildRequires:	pkgconfig
# uses included ucl-common 1.2.8 with some modifications :/
#BuildRequires:	ucl-common-devel >= 1.2.8
BuildRequires:	xvid-devel >= 1:1.0.0
BuildConflicts:	faad2 < 2.0-3
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The MPEG4IP project provides a standards-based system for encoding,
streaming, and playing MPEG-4 encoded audio and video. To achieve
this the developers integrated a number of existing open source
packages, and also created some original code to fill in the gaps.

%description -l pl
Projekt MPEG4IP udostêpnia oparty na standardach system do kodowania,
streamingu i odtwarzania d¼wiêku i obrazu kodowanego MPEG-4. Aby to
osi±gn±æ, programi¶ci zintegrowali wiele istniej±cych wolnodostêpnych
pakietów oraz stworzyli trochê w³asnego kodu, aby wype³niæ luki.

%package libs
Summary:	Base shared MPEG4IP libraries
Summary(pl):	Podstawowe biblioteki wspó³dzielone MPEG4IP
Group:		Libraries

%description libs
Base shared MPEG4IP libraries.

%description libs -l pl
Podstawowe biblioteki wspó³dzielone MPEG4IP.

%package devel
Summary:	Header files for base MPEG4IP libraries
Summary(pl):	Pliki nag³ówkowe podstawowych bibliotek MPEG4IP
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for base MPEG4IP libraries.

%description devel -l pl
Pliki nag³ówkowe podstawowych bibliotek MPEG4IP.

%package static
Summary:	Static versions of base MPEG4IP libraries
Summary(pl):	Statyczne wersje podstawowych bibliotek MPEG4IP
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static versions of base MPEG4IP libraries.

%description static -l pl
Statyczne wersje podstawowych bibliotek MPEG4IP.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
# won't work yet...
#%patch8 -p1

%build
cd lib/rtp
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
cd ../..
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure

%{__make} \
	CCAS="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/mp4player_plugin/*.{a,la}
# bogus manual
rm -rf $RPM_BUILD_ROOT%{_mandir}/manm

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README* TODO doc/{*.pdf,*.txt}
%doc doc/encoding/*.htm doc/ietf/draft*.txt doc/mcast/{mcast.txt,*_example}
%attr(755,root,root) %{_bindir}/avi2raw
%attr(755,root,root) %{_bindir}/avidump
%attr(755,root,root) %{_bindir}/gmp4player
%attr(755,root,root) %{_bindir}/lboxcrop
%attr(755,root,root) %{_bindir}/mp4*
%attr(755,root,root) %{_bindir}/rgb2yuv
%attr(755,root,root) %{_bindir}/xvidenc
%attr(755,root,root) %{_bindir}/yuvdump
%dir %{_libdir}/mp4player_plugin
%attr(755,root,root) %{_libdir}/mp4player_plugin/*.so*
%{_mandir}/man1/gmp4player.1*
%{_mandir}/man1/mp4*.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libconfig_file.so.*.*.*
%attr(755,root,root) %{_libdir}/libmp4.so.*.*.*
%attr(755,root,root) %{_libdir}/libmp4av.so.*.*.*
%attr(755,root,root) %{_libdir}/libmp4util.so.*.*.*
%attr(755,root,root) %{_libdir}/libmp4v2.so.*.*.*
%attr(755,root,root) %{_libdir}/libmsg_queue.so.*.*.*
%attr(755,root,root) %{_libdir}/libmpeg4ip_sdp.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mpeg4ip-config
%attr(755,root,root) %{_libdir}/libconfig_file.so
%attr(755,root,root) %{_libdir}/libmp4.so
%attr(755,root,root) %{_libdir}/libmp4av.so
%attr(755,root,root) %{_libdir}/libmp4util.so
%attr(755,root,root) %{_libdir}/libmp4v2.so
%attr(755,root,root) %{_libdir}/libmsg_queue.so
%attr(755,root,root) %{_libdir}/libmpeg4ip_sdp.so
%{_libdir}/libconfig_file.la
%{_libdir}/libmp4.la
%{_libdir}/libmp4av.la
%{_libdir}/libmp4util.la
%{_libdir}/libmp4v2.la
%{_libdir}/libmsg_queue.la
%{_libdir}/libmpeg4ip_sdp.la
# static-only lib - private mpeg4ip use only?
#%{_libdir}/libhttp.*a
%{_includedir}/codec_plugin.h
%{_includedir}/mp4*.h
%{_includedir}/mpeg4*.h
%{_includedir}/rtp_plugin.h
%{_includedir}/sdp*.h
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/libconfig_file.a
%{_libdir}/libmp4.a
%{_libdir}/libmp4av.a
%{_libdir}/libmp4util.a
%{_libdir}/libmp4v2.a
%{_libdir}/libmsg_queue.a
%{_libdir}/libmpeg4ip_sdp.a
