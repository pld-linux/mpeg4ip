Summary:	MPEG4IP - system for encoding, streaming and playing MPEG-4 audio/video
Summary(pl):	MPEG4IP - sytem kodowania, streamingu i odtwarzania d¼wiêku i obrazu MPEG-4
Name:		mpeg4ip
Version:	0.9.8
Release:	0.1
License:	MPL v1.1 (original code) and other licenses (included libraries)
Group:		Applications
Source0:	http://dl.sourceforge.net/sourceforge/mpeg4ip/%{name}-%{version}.tar.gz
# Source0-md5:	076ee64f2d5cec82bc391485f2b6a251
Patch0:		%{name}-system-SDL.patch
# don't use non-standard SDL_HasAudioDelayMsec() and SDL_AudioDelayMsec()
# an alternative is to patch system SDL adding those functions ???
Patch1:		%{name}-nosdlaudiodelay.patch
Patch2:		%{name}-system-xvid.patch
Patch3:		%{name}-system-rtp.patch
# use --tag=NASM for nasm assembler sources
Patch4:		%{name}-lt-tag.patch
# libtool bug: static convenience C++ libraries require --tag=CXX as workaround
Patch5:		%{name}-lt-tag-cxx.patch
URL:		http://www.xmms.org/
BuildRequires:	SDL-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:  gtk+2-devel
BuildRequires:  lame-libs-devel
BuildRequires:	libtool
# uses included ucl-common 1.2.8 with some modifications :/
#BuildRequires:	ucl-common-devel >= 1.2.8
# uses included xvid 20020412 with some modifications :/
#BuildRequires:	xvid-devel >= 1:0.9.1-2
Requires:	%{name}-libs = %{version}
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
Requires:	%{name}-libs = %{version}

%description devel
Header files for base MPEG4IP libraries.

%description devel -l pl
Pliki nag³ówkowe podstawowych bibliotek MPEG4IP.

%package static
Summary:	Static versions of base MPEG4IP libraries
Summary(pl):	Statyczne wersje podstawowych bibliotek MPEG4IP
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static versions of base MPEG4IP libraries.

%description static -l pl
Statyczne wersje podstawowych bibliotek MPEG4IP.

%prep
%setup -q
%patch0 -p1 
%patch1 -p1
# won't work yet...
#%patch2 -p1
#%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure

%{__make} \
	CCAS="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	m4datadir=%{_aclocaldir}

rm -f $RPM_BUILD_ROOT%{_libdir}/mp4player_plugin/*.{a,la}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README* TODO doc/{*.pdf,*.txt}
%doc doc/encoding/*.htm doc/ietf/draft*.txt doc/mcast/{mcast.txt,*_example}
#%attr(755,root,root) %{_bindir}/{avi2raw,avidump,faac,gmp4player,ipvt_prog}
#%attr(755,root,root) %{_bindir}/{lboxcrop,mp4creator,mp4dump,mp4encode}
#%attr(755,root,root) %{_bindir}/{mp4extract,mp4info,mp4live,mp4player}
#%attr(755,root,root) %{_bindir}/{mp4trackdump,mp4venc,rgb2yuv,sdl-config} 
#%attr(755,root,root) %{_bindir}/{xvidenc,yuvdump}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/mp4player_plugin
%{_mandir}/man1/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libh26lenc.so.*.*
%attr(755,root,root) %{_libdir}/libmp4av.so.*.*
%attr(755,root,root) %{_libdir}/libmp4util.so.*.*
%attr(755,root,root) %{_libdir}/libmp4v2.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libh26lenc.so
%attr(755,root,root) %{_libdir}/libmp4av.so
%attr(755,root,root) %{_libdir}/libmp4util.so
%attr(755,root,root) %{_libdir}/libmp4v2.so
%{_libdir}/libh26lenc.la
%{_libdir}/libmp4av.la
%{_libdir}/libmp4util.la
%{_libdir}/libmp4v2.la
# static-only libs - private mpeg4ip use only???
#%{_libdir}/libconfig_file.*a
#%{_libdir}/libhttp.*a
#%{_libdir}/libmp4.*a
#%{_libdir}/libmsg_queue.*a
#%{_libdir}/libsdp.*a
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/libh26lenc.a
%{_libdir}/libmp4av.a
%{_libdir}/libmp4util.a
%{_libdir}/libmp4v2.a
