#
# Conditional build:
%bcond_without	alsa	# build without ALSA support in SDLAudio
%bcond_without	static_libs	# don't build static libraries

Summary:	MPEG4IP - system for encoding, streaming and playing MPEG-4 audio/video
Summary(pl.UTF-8):	MPEG4IP - system kodowania, streamingu i odtwarzania dźwięku i obrazu MPEG-4
Name:		mpeg4ip
Version:	1.6.1
Release:	16
Epoch:		1
License:	MPL v1.1 (original code) and other licenses (included libraries)
Group:		Applications
# official tarball corrupted
# Source0:	http://dl.sourceforge.net/mpeg4ip/%{name}-%{version}.tar.gz
Source0:	ftp://ftp.freebsd.org/pub/FreeBSD/ports/local-distfiles/ahze/%{name}-%{version}.tar.gz
# Source0-md5:	59e9d9cb7aad0a9605fb6015e7f0b197
Patch0:		%{name}-link.patch
Patch1:		%{name}-ac.patch
Patch2:		%{name}-gcc4.patch
Patch3:		%{name}-configure.patch
Patch4:		%{name}-audio_l16.cpp-typo.patch
Patch5:		%{name}-ffmpeg.patch
Patch6:		gcc44.patch
URL:		http://www.mpeg4ip.net/
BuildRequires:	SDL-devel
BuildRequires:	a52dec-libs-devel
%{?with_alsa:BuildRequires:	alsa-lib-devel >= 0.9.0}
BuildRequires:	autoconf
BuildRequires:	automake >= 1.4
BuildRequires:	faac-devel >= 1.20.1
BuildRequires:	ffmpeg-devel >= 0.4.9-3.20061204
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	lame-libs-devel >= 3.92
BuildRequires:	libid3tag-devel
BuildRequires:	libmad-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.4d
BuildRequires:	libvorbis-devel >= 1:1.0
BuildRequires:	libx264-devel
#BuildRequires:	mpeg2dec-devel
%ifarch %{ix86} %{x8664}
BuildRequires:	nasm >= 0.98.19
%endif
BuildRequires:	pkgconfig
BuildRequires:	srtp-devel >= 1.4.2
BuildRequires:	xvid-devel >= 1:1.0.0
BuildConflicts:	faad2 < 2.0-3
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing -Wno-error -D__STDC_CONSTANT_MACROS

%description
The MPEG4IP project provides a standards-based system for encoding,
streaming, and playing MPEG-4 encoded audio and video. To achieve this
the developers integrated a number of existing open source packages,
and also created some original code to fill in the gaps.

%description -l pl.UTF-8
Projekt MPEG4IP udostępnia oparty na standardach system do kodowania,
streamingu i odtwarzania dźwięku i obrazu kodowanego MPEG-4. Aby to
osiągnąć, programiści zintegrowali wiele istniejących wolnodostępnych
pakietów oraz stworzyli trochę własnego kodu, aby wypełnić luki.

%package libs
Summary:	Base shared MPEG4IP libraries
Summary(pl.UTF-8):	Podstawowe biblioteki współdzielone MPEG4IP
Group:		Libraries

%description libs
Base shared MPEG4IP libraries.

%description libs -l pl.UTF-8
Podstawowe biblioteki współdzielone MPEG4IP.

%package devel
Summary:	Header files for base MPEG4IP libraries
Summary(pl.UTF-8):	Pliki nagłówkowe podstawowych bibliotek MPEG4IP
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for base MPEG4IP libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe podstawowych bibliotek MPEG4IP.

%package static
Summary:	Static versions of base MPEG4IP libraries
Summary(pl.UTF-8):	Statyczne wersje podstawowych bibliotek MPEG4IP
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static versions of base MPEG4IP libraries.

%description static -l pl.UTF-8
Statyczne wersje podstawowych bibliotek MPEG4IP.

%package utils
Summary:	Utilities for MPEG4IP
Group:		Applications
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description utils
This package contains various utilities :
- mp4info - display information about tracks in mp4 file
- mp4dump - dumps contents from mp4 files
- mp4trackdump - dumps track information
- mp4tags - sets iTunes tag information
- mp4art - extract iTunes cover art
- mp4videoinfo - dump information about video tracks in mp4 files

%package server
Summary:	mp4 server
Group:		Daemons
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description server
This package contains the mp4 server.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
cd lib/SDLAudio
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
cd ../..
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
install -d config
touch bootstrapped
%configure \
	%{!?with_alsa:--disable-alsa} \
	%{!?with_static_libs:--disable-static} \
	--enable-ffmpeg=%{_includedir} \
	--enable-ipv6

%{__make} \
	CCAS="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT

# workaround for:
# libtool: install: warning: relinking `libmp4av.la'
#   ...  /usr/bin/ld: cannot find -lmp4v2
%{__make} -C lib/mp4v2 install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -p server/util/mp4encode/mp4encode $RPM_BUILD_ROOT%{_bindir}

rm -f $RPM_BUILD_ROOT%{_libdir}/mp4player_plugin/*.{a,la}
# bogus manual
rm -rf $RPM_BUILD_ROOT%{_mandir}/manm

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog encoding60.dsw FEATURES.html index.html README* NEWS TODO
%doc doc/{*.pdf,*.txt,*.html,*.jpg} doc/ietf/rfc*.txt doc/mcast/{mcast.txt,*_example}
%attr(755,root,root) %{_bindir}/gmp4player
%attr(755,root,root) %{_bindir}/mp4encode
%attr(755,root,root) %{_bindir}/mp4player
%attr(755,root,root) %{_bindir}/sdl_pcm_play
%attr(755,root,root) %{_bindir}/yuvdump
%dir %{_libdir}/mp4player_plugin
%attr(755,root,root) %{_libdir}/mp4player_plugin/*.so*
%{_mandir}/man1/gmp4player.1*
%{_mandir}/man1/mp4encode.1*

# used by gui only
%attr(755,root,root) %{_libdir}/libmpeg4ipSDL*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmpeg4ipSDL*.so.0

%files libs
%defattr(644,root,root,755)
# libmp4v2.so.0 used by faac, easytag, libtunepimp, amarok-1.4 ...
%attr(755,root,root) %{_libdir}/libmp4*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmp4*.so.0

# libsdp.so.0 used by libopensync-plugin-irmc (maybe bogus)
%attr(755,root,root) %{_libdir}/libsdp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsdp.so.0

# these libs not used by anything else externally, but mpeg4ip progs
%attr(755,root,root) %{_libdir}/libmpeg4ip_*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmpeg4ip_*.so.0
%attr(755,root,root) %{_libdir}/libhttp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhttp.so.0
%attr(755,root,root) %{_libdir}/libismacryp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libismacryp.so.0
%attr(755,root,root) %{_libdir}/libsrtpif.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsrtpif.so.0
# links with SDL
%attr(755,root,root) %{_libdir}/libmsg_queue.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmsg_queue.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mpeg4ip-config
%attr(755,root,root) %{_libdir}/libhttp.so
%attr(755,root,root) %{_libdir}/libismacryp.so
%attr(755,root,root) %{_libdir}/libmp4*.so
%attr(755,root,root) %{_libdir}/libmpeg4ip*.so
%attr(755,root,root) %{_libdir}/libmsg_queue.so
%attr(755,root,root) %{_libdir}/libsdp.so
%attr(755,root,root) %{_libdir}/libsrtpif.so
%{_libdir}/libhttp.la
%{_libdir}/libismacryp.la
%{_libdir}/libmp4*.la
%{_libdir}/libmpeg4ip*.la
%{_libdir}/libmsg_queue.la
%{_libdir}/libsdp.la
%{_libdir}/libsrtpif.la
%{_includedir}/codec_plugin.h
%{_includedir}/h264_sdp.h
%{_includedir}/mp4.h
%{_includedir}/mp4av*.h
%{_includedir}/mpeg4_*.h
%{_includedir}/mpeg4ip*.h
%{_includedir}/rtp_plugin.h
%{_includedir}/sdp*.h
%{_includedir}/text_plugin.h
%{_mandir}/man3/MP4*.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libhttp.a
%{_libdir}/libismacryp.a
%{_libdir}/libmp4*.a
%{_libdir}/libmpeg4ip*.a
%{_libdir}/libmsg_queue.a
%{_libdir}/libsdp.a
%{_libdir}/libsrtpif.a
%endif

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/h264_parse
%attr(755,root,root) %{_bindir}/mp4art
%attr(755,root,root) %{_bindir}/mp4dump
%attr(755,root,root) %{_bindir}/mp4extract
%attr(755,root,root) %{_bindir}/mp4info
%attr(755,root,root) %{_bindir}/mp4tags
%attr(755,root,root) %{_bindir}/mp4trackdump
%attr(755,root,root) %{_bindir}/mp4videoinfo
%attr(755,root,root) %{_bindir}/mpeg2t_dump
%attr(755,root,root) %{_bindir}/mpeg2video_parse
%attr(755,root,root) %{_bindir}/mpeg4vol
%attr(755,root,root) %{_bindir}/mpeg_ps_extract
%attr(755,root,root) %{_bindir}/mpeg_ps_info

%files server
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/avi2raw
%attr(755,root,root) %{_bindir}/avidump
%attr(755,root,root) %{_bindir}/lboxcrop
%attr(755,root,root) %{_bindir}/mp4creator
%attr(755,root,root) %{_bindir}/mp4live
%attr(755,root,root) %{_bindir}/rgb2yuv
%{_mandir}/man1/mp4creator.1*
%{_mandir}/man1/mp4live.1*
