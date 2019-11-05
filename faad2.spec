%define	major	2
%define	libname	%mklibname faad %{major}
%define boguslibname %mklibname %{name}_ %{major}
%define drmlibname %mklibname faad_drm %{major}
%define	devname	%mklibname -d faad
%define bogusdevname %mklibname -d %{name}
%define	static	%mklibname -s -d faad
%define drmstatic %mklibname -s -d faad_drm
%define bogusstatic %mklibname -s -d %{name}

%define		underver 2_9_1

Summary:	Freeware Advanced Audio Decoder version 2
Name:		faad2
Version:	2.9.1
Release:	1
Source0:	https://github.com/knik0/faad2/archive/%{underver}/%{name}-%{underver}.tar.gz
#Patch1:		faad2-2.7-mp4ff-fpic.patch
URL:		http://www.audiocoding.com
License:	GPLv2+
Group:		Sound
BuildRequires:	pkgconfig(sndfile)
#BuildRequires: libxmms-devel
BuildRequires:	id3lib-devel
BuildRequires:	dos2unix
BuildRequires:	pkgconfig(sdl)
Epoch:		1

%description
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder,
completely written from scratch. FAAD 2 is licensed under the GPL.

%package -n	%{libname}
Summary:	Freeware Advanced Audio Decoder shared library
Group:		System/Libraries
Obsoletes:	%{boguslibname} < %{EVRD}

%description -n	%{libname}
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder,
completely written from scratch. FAAD 2 is licensed under the GPL.

This package contains the shared library needed by programs linked to
libfaad.

%package -n	%{drmlibname}
Summary:	DRM support for the Freeware Advanced Audio Decoder shared library
Group:		System/Libraries

%description -n	%{drmlibname}
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder,
completely written from scratch. FAAD 2 is licensed under the GPL.

This package contains the shared library needed by programs linked to
libfaad.

This module adds DRM support.

%package -n	%{devname}
Summary:	Freeware Advanced Audio Decoder development files
Group:		Development/C++
Requires:	%{libname} = %{EVRD}
Requires:	%{drmlibname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Obsoletes:	%mklibname -d %{name}_ 0
Obsoletes:	%{bogusdevname} < %{EVRD}

%description -n %{devname}
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder,
completely written from scratch. FAAD 2 is licensed under the GPL.

This package contains the C++ headers needed to build programs with
libfaad.

%package -n	%{static}
Summary:	Freeware Advanced Audio Decoder static libraries
Group:		Development/C++
Requires:	%{devname} = %{EVRD}
Provides:	%{name}-static-devel  = %{EVRD}
Obsoletes:	%mklibname -s -d %{name}_ 0
Obsoletes:	%{bogusstatic} < %{EVRD}

%description -n %{static}
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder,
completely written from scratch. FAAD 2 is licensed under the GPL.

This package contains the static libraries needed to build programs
with libfaad.

%package -n	%{drmstatic}
Summary:	DRM support for Freeware Advanced Audio Decoder static libraries
Group:		Development/C++
Requires:	%{static} = %{EVRD}

%description -n %{drmstatic}
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder,
completely written from scratch. FAAD 2 is licensed under the GPL.

This package contains the static libraries needed to build programs
with libfaad.

This module adds DRM support.

#package xmms
#Group: Sound
#Summary: AAC input plugin for xmms
#Requires: xmms

#description xmms
#This is an AAC input plugin for xmms. AAC files are recognized by an
#.aac extension.

%prep
%setup -q -n %{name}-%{underver}
%autopatch -p1
%build
autoreconf -vfi
%global optflags %{optflags} -Ofast
%configure	--enable-static \
		--with-drm

%install
%make_install
rm -rf %{buildroot}
# Hack to work around a problem with DESTDIR in libtool 1.4.x
LIBRARY_PATH="%{buildroot}/usr/lib:${LIBRARY_PATH}" make install DESTDIR=%{buildroot}
# install libmp4ff
install -m644 common/mp4ff/libmp4ff.a %{buildroot}%{_libdir}
install -m644 common/mp4ff/mp4ff.h %{buildroot}%{_includedir}
 
%files
%doc README NEWS TODO AUTHORS ChangeLog
%{_bindir}/faad
%{_mandir}/man1/faad.1*

%files -n %{libname}
%{_libdir}/libfaad.so.%{major}*

%files -n %{drmlibname}
%{_libdir}/libfaad_drm.so.%{major}*

%files -n %{devname}
%{_libdir}/libfaad.so
%{_libdir}/libfaad_drm.so
%{_includedir}/*

%files -n %{static}
%{_libdir}/libfaad.a
%{_libdir}/libmp4ff.a

%files -n %{drmstatic}
%{_libdir}/libfaad_drm.a
