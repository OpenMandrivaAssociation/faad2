%define	major	2
%define	libname	%mklibname faad %{major}
%define boguslibname %mklibname %{name}_ %{major}
%define drmlibname %mklibname faad_drm %{major}
%define	devname	%mklibname -d faad
%define bogusdevname %mklibname -d %{name}
%define	static	%mklibname -s -d faad
%define drmstatic %mklibname -s -d faad_drm
%define bogusstatic %mklibname -s -d %{name}

# faad is used by ffmpeg, ffmpeg is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif
%define lib32name libfaad%{major}
%define drmlib32name libfaad_drm%{major}
%define dev32name libfaad-devel

%define		underver %(echo %{version} |sed -e 's,\\.,_,g')

Summary:	Freeware Advanced Audio Decoder version 2
Name:		faad2
Version:	2.10.0
Release:	1
Source0:	https://github.com/knik0/faad2/archive/%{underver}/%{name}-%{underver}.tar.gz

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

%if %{with compat32}
%package -n	%{lib32name}
Summary:	Freeware Advanced Audio Decoder shared library (32-bit)
Group:		System/Libraries

%description -n	%{lib32name}
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder,
completely written from scratch. FAAD 2 is licensed under the GPL.

This package contains the shared library needed by programs linked to
libfaad.

%package -n	%{drmlib32name}
Summary:	DRM support for the Freeware Advanced Audio Decoder shared library (32-bit)
Group:		System/Libraries

%description -n	%{drmlib32name}
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder,
completely written from scratch. FAAD 2 is licensed under the GPL.

This package contains the shared library needed by programs linked to
libfaad.

This module adds DRM support.

%package -n	%{dev32name}
Summary:	Freeware Advanced Audio Decoder development files (32-bit)
Group:		Development/C++
Requires:	%{lib32name} = %{EVRD}
Requires:	%{drmlib32name} = %{EVRD}
Requires:	%{devname} = %{EVRD}

%description -n %{dev32name}
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder,
completely written from scratch. FAAD 2 is licensed under the GPL.

This package contains the C++ headers needed to build programs with
libfaad.
%endif

%prep
%autosetup -p1 -n %{name}-%{underver}
autoreconf -vfi

export CONFIGURE_TOP="$(pwd)"
%global optflags %{optflags} -Ofast

%if %{with compat32}
mkdir build32
cd build32
%configure32	--with-drm
cd ..
%endif

mkdir build
cd build
%configure	--enable-static \
		--with-drm

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build
 
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
%{_libdir}/pkgconfig/faad2.pc
%{_includedir}/*

%files -n %{static}
%{_libdir}/libfaad.a

%files -n %{drmstatic}
%{_libdir}/libfaad_drm.a

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libfaad.so.%{major}*

%files -n %{drmlib32name}
%{_prefix}/lib/libfaad_drm.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/libfaad.so
%{_prefix}/lib/libfaad_drm.so
%{_prefix}/lib/pkgconfig/faad2.pc
%endif
