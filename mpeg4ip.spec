#
# Conditional build:
#
Summary:	a
Name:		mpeg4ip
Version:	0.9.7
Release:	0.2
License:	GPL
Group:		Applications
Source0:	http://unc.dl.sourceforge.net/sourceforge/mpeg4ip/%{name}-%{version}.tar.gz
#Patch0:		%{name}-externSDL.patch
URL:		http://www.xmms.org/
BuildRequires:  gtk+2-devel
BuildRequires:  lame-libs-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
empty

%prep
%setup -q
#using system SDL
#%patch0 -p1 
#rm -Rf lib/SDL

%build
rm -f missing
%{__aclocal}
%{__autoconf}
%{__automake}
cd lib/SDL
%{__aclocal}
%{__autoconf}
%configure
cd ../../
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	m4datadir=%{_aclocaldir}



%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig


%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
#%attr(755,root,root) %{_bindir}/{avi2raw,avidump,faac,gmp4player,ipvt_prog}
#%attr(755,root,root) %{_bindir}/{lboxcrop,mp4creator,mp4dump,mp4encode}
#%attr(755,root,root) %{_bindir}/{mp4extract,mp4info,mp4live,mp4player}
#%attr(755,root,root) %{_bindir}/{mp4trackdump,mp4venc,rgb2yuv,sdl-config} 
#%attr(755,root,root) %{_bindir}/{xvidenc,yuvdump}
%{_mandir}/man3/*
%{_mandir}/man1/*
%attr(755,root,root) %{_bindir}/*
%{_libdir}/*
