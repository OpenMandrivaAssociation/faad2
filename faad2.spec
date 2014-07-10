%define	major	2
%define	libname	%mklibname faad %{major}
%define boguslibname %mklibname %{name}_ %{major}
%define	devname	%mklibname -d faad
%define bogusdevname %mklibname -d %{name}
%define	static	%mklibname -s -d faad
%define bogusstatic %mklibname -s -d %{name}

Summary:	Freeware Advanced Audio Decoder version 2
Name:		faad2
Version:	2.7
Release:	9
Source0:	%{name}-%{version}.tar.bz2
Patch0:		faad2-automake-1.13.patch
Patch1:		faad2-2.7-mp4ff-fpic.patch
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

%package -n	%{devname}
Summary:	Freeware Advanced Audio Decoder development files
Group:		Development/C++
Requires:	%{libname} = %{EVRD}
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

#package xmms
#Group: Sound
#Summary: AAC input plugin for xmms
#Requires: xmms

#description xmms
#This is an AAC input plugin for xmms. AAC files are recognized by an
#.aac extension.

%prep
%setup -q
dos2unix configure.in frontend/main.c common/mp4ff/mp4ffint.h common/mp4ff/Makefile.am
%apply_patches
chmod 644 AUTHORS README TODO NEWS ChangeLog
autoupdate
autoreconf -fiv

%build
%global optflags %{optflags} -Ofast
%configure2_5x	--enable-static \
		--with-drm
%make

%install
%makeinstall_std
install -m644 common/mp4ff/libmp4ff.a %{buildroot}%{_libdir}
install -m644 common/mp4ff/{mp4ff.h,mp4ff_int_types.h} %{buildroot}%{_includedir}
 
#gw rename it to a more standard name
mkdir -p %{buildroot}%{_mandir}/man1
mv %{buildroot}%{_mandir}/manm/faad.man %{buildroot}%{_mandir}/man1/faad.1

%files
%doc README NEWS TODO AUTHORS ChangeLog
%{_bindir}/faad
%{_mandir}/man1/faad.1*

%files -n %{libname}
%{_libdir}/libfaad.so.%{major}*

%files -n %{devname}
%{_libdir}/libfaad.so
%{_includedir}/*

%files -n %{static}
%{_libdir}/libfaad.a
%{_libdir}/libmp4ff.a
