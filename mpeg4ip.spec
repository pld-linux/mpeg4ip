# TODO:
# - link libmpeg4ipSDL with -lSDL
# - link both player/plugin/rtp/isma_audio/ plugins with -lSDL
# - check player/plugin/rtp/isma_video/
#   isma_enc_video_rtp_plugin.so.0.0.0: undefined reference to `parse_fmtp_for_mpeg4'
# - check player/plugin/video/mpeg3/
#   mpeg3_video_plugin.so.0.0.0: undefined reference to `MP4AV_Mpeg3FindPictHdr'
# - check player/src/codec/mp3/
#   mp3_plugin.so.0.0.0: undefined reference to `MP4AV_Mp3HeaderFromBytes'
#   mp3_plugin.so.0.0.0: undefined reference to `MP4AV_Mp3GetHdrLayer'
#   mp3_plugin.so.0.0.0: undefined reference to `MP4AV_Mp3GetHdrSamplingWindow'
#   mp3_plugin.so.0.0.0: undefined reference to `MP4AV_Mp3GetBitRate'
# - check player/src/codec/wav/
#   wav_plugin.so.0.0.0: undefined reference to `SDL_FreeWAV'
#   wav_plugin.so.0.0.0: undefined reference to `SDL_RWFromFile'
#   wav_plugin.so.0.0.0: undefined reference to `SDL_LoadWAV_RW'
Summary:	MPEG4IP - system for encoding, streaming and playing MPEG-4 audio/video
Summary(pl):	MPEG4IP - sytem kodowania, streamingu i odtwarzania d�wi�ku i obrazu MPEG-4
Name:		mpeg4ip
Version:	1.1
Release:	0.1
Epoch:		1
License:	MPL v1.1 (original code) and other licenses (included libraries)
Group:		Applications
Source0:	http://dl.sourceforge.net/mpeg4ip/%{name}-%{version}.tar.gz
# Source0-md5:	fef0224a45485653a8db87bdd5c9e745
# Source0-size:	4351378
Patch0:		%{name}-link.patch
Patch1:		%{name}-types.patch
Patch2:		%{name}-gcc34.patch
Patch3:		%{name}-gtk.patch
Patch4:		%{name}-abort.patch
URL:		http://www.mpeg4ip.net/
BuildRequires:	SDL-devel
BuildRequires:	alsa-lib-devel >= 0.9.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	faac-devel >= 1.20
BuildRequires:	gtk+2-devel >= 2.0.0
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

%description
The MPEG4IP project provides a standards-based system for encoding,
streaming, and playing MPEG-4 encoded audio and video. To achieve
this the developers integrated a number of existing open source
packages, and also created some original code to fill in the gaps.

%description -l pl
Projekt MPEG4IP udost�pnia oparty na standardach system do kodowania,
streamingu i odtwarzania d�wi�ku i obrazu kodowanego MPEG-4. Aby to
osi�gn��, programi�ci zintegrowali wiele istniej�cych wolnodost�pnych
pakiet�w oraz stworzyli troch� w�asnego kodu, aby wype�ni� luki.

%package libs
Summary:	Base shared MPEG4IP libraries
Summary(pl):	Podstawowe biblioteki wsp�dzielone MPEG4IP
Group:		Libraries

%description libs
Base shared MPEG4IP libraries.

%description libs -l pl
Podstawowe biblioteki wsp�dzielone MPEG4IP.

%package devel
Summary:	Header files for base MPEG4IP libraries
Summary(pl):	Pliki nag��wkowe podstawowych bibliotek MPEG4IP
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for base MPEG4IP libraries.

%description devel -l pl
Pliki nag��wkowe podstawowych bibliotek MPEG4IP.

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
%patch4 -p0

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
%doc AUTHORS COPYING ChangeLog encoding60.dsw FEATURES.html index.html README* NEWS TODO 
%doc doc/{*.pdf,*.txt,*.html,*.jpg} doc/ietf/rfc*.txt doc/mcast/{mcast.txt,*_example}
%attr(755,root,root) %{_bindir}/rgb2yuv
%attr(755,root,root) %{_bindir}/mp4encode
%attr(755,root,root) %{_bindir}/mp4player
%attr(755,root,root) %{_bindir}/mp4creator
%attr(755,root,root) %{_bindir}/yuvdump
%attr(755,root,root) %{_bindir}/gmp4player
%attr(755,root,root) %{_bindir}/mp4dump
%attr(755,root,root) %{_bindir}/mp4info
%attr(755,root,root) %{_bindir}/mp4live
%attr(755,root,root) %{_bindir}/mp4tags
%attr(755,root,root) %{_bindir}/mpeg4vol
%attr(755,root,root) %{_bindir}/h264_parse
%attr(755,root,root) %{_bindir}/mp4extract
%attr(755,root,root) %{_bindir}/mp4trackdump
%attr(755,root,root) %{_bindir}/avi2raw
%attr(755,root,root) %{_bindir}/avidump
%attr(755,root,root) %{_bindir}/mpeg2video_parse
%attr(755,root,root) %{_bindir}/lboxcrop
%dir %{_libdir}/mp4player_plugin
%attr(755,root,root) %{_libdir}/mp4player_plugin/*.so*
%{_datadir}/mp4venc_template.par
%{_mandir}/man1/*.1.gz

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mpeg4ip-config
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*.h
%{_mandir}/man3/*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
