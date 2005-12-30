#
# Conditional build:
%bcond_without	alsa	# build without ALSA support in SDLAudio
#
Summary:	MPEG4IP - system for encoding, streaming and playing MPEG-4 audio/video
Summary(pl):	MPEG4IP - system kodowania, streamingu i odtwarzania d¼wiêku i obrazu MPEG-4
Name:		mpeg4ip
Version:	1.4.1
Release:	2
Epoch:		1
License:	MPL v1.1 (original code) and other licenses (included libraries)
Group:		Applications
Source0:	http://dl.sourceforge.net/mpeg4ip/%{name}-%{version}.tar.gz
# Source0-md5:	68968c23c7e9d23cac11f15f3bcf7ede
Patch0:		%{name}-link.patch
Patch1:		%{name}-types.patch
Patch2:		%{name}-gcc4.patch
URL:		http://www.mpeg4ip.net/
BuildRequires:	SDL-devel
%{?with_alsa:BuildRequires:	alsa-lib-devel >= 0.9.0}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	faac-devel >= 1.20
BuildRequires:	ffmpeg-devel >= 0.4.9
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	lame-libs-devel >= 3.92
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.4d
BuildRequires:	libvorbis-devel >= 1:1.0
BuildRequires:	pkgconfig
BuildRequires:	libid3tag-devel
BuildRequires:	xvid-devel >= 1:1.0.0
BuildConflicts:	faad2 < 2.0-3
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing

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

%build
cd lib/SDLAudio
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
cd ../rtp
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
install -d config
touch bootstrapped
%configure \
	%{!?with_alsa:--disable-alsa}

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
%attr(755,root,root) %{_bindir}/avi2raw
%attr(755,root,root) %{_bindir}/avidump
%attr(755,root,root) %{_bindir}/gmp4player
%attr(755,root,root) %{_bindir}/h264_parse
%attr(755,root,root) %{_bindir}/lboxcrop
%attr(755,root,root) %{_bindir}/mp4art
%attr(755,root,root) %{_bindir}/mp4creator
%attr(755,root,root) %{_bindir}/mp4dump
%attr(755,root,root) %{_bindir}/mp4extract
%attr(755,root,root) %{_bindir}/mp4info
%attr(755,root,root) %{_bindir}/mp4live
%attr(755,root,root) %{_bindir}/mp4player
%attr(755,root,root) %{_bindir}/mp4tags
%attr(755,root,root) %{_bindir}/mp4trackdump
%attr(755,root,root) %{_bindir}/mp4videoinfo
%attr(755,root,root) %{_bindir}/mpeg2video_parse
%attr(755,root,root) %{_bindir}/mpeg4vol
%attr(755,root,root) %{_bindir}/mpeg_ps_extract
%attr(755,root,root) %{_bindir}/mpeg_ps_info
%attr(755,root,root) %{_bindir}/rgb2yuv
%attr(755,root,root) %{_bindir}/sdl_pcm_play
%attr(755,root,root) %{_bindir}/yuvdump
%dir %{_libdir}/mp4player_plugin
%attr(755,root,root) %{_libdir}/mp4player_plugin/*.so*
%{_mandir}/man1/gmp4player.1*
%{_mandir}/man1/mp4creator.1*
# no program
#%{_mandir}/man1/mp4encode.1*
%{_mandir}/man1/mp4live.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mpeg4ip-config
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*.h
%{_mandir}/man3/*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
