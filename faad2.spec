
%define major 2
%define libname %mklibname %{name}_ %{major}
%define develname %mklibname -d %{name}
%define staticname %mklibname -s -d %{name}

Summary:	Freeware Advanced Audio Decoder version 2
Name:		faad2
Version:	2.7
Release:	4
Source0:	%{name}-%{version}.tar.bz2
Patch0:		faad2-automake-1.13.patch
Patch1:		faad2-2.7-mp4ff-fpic.patch
URL:		http://www.audiocoding.com
License:	GPLv2+
Group:		Sound
BuildRequires:	sndfile-devel
#BuildRequires: libxmms-devel
BuildRequires:	libid3lib-devel
BuildRequires:	dos2unix
BuildRequires:	automake1.8
BuildRequires:	SDL-devel
Epoch:	1

%description
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder,
completely written from scratch. FAAD 2 is licensed under the GPL.

%package -n %{libname}
Summary:	Freeware Advanced Audio Decoder shared library
Group:	System/Libraries

%description -n %{libname}
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder,
completely written from scratch. FAAD 2 is licensed under the GPL.

This package contains the shared library needed by programs linked to
libfaad.

%package -n %{develname}
Summary:	Freeware Advanced Audio Decoder development files
Group:		Development/C++
Requires:	%{libname} = %{epoch}:%{version}
Provides:	lib%{name}-devel  = %{epoch}:%{version}-%{release}
Obsoletes:	%mklibname -d %{name}_ 0

%description -n %{develname}
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder,
completely written from scratch. FAAD 2 is licensed under the GPL.

This package contains the C++ headers needed to build programs with
libfaad.

%package -n %{staticname}
Summary:	Freeware Advanced Audio Decoder static libraries
Group:		Development/C++
Requires:	%{develname} = %{epoch}:%{version}
Provides:	lib%{name}-static-devel  = %{epoch}:%{version}-%{release}
Obsoletes:	%mklibname -s -d %{name}_ 0

%description -n %staticname
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
aclocal -I .
autoheader
libtoolize --automake --copy
automake -a -c
autoconf

%build
%configure2_5x
%make

%install
%makeinstall_std
#manual installation of libmp4ff
cd common/mp4ff
install -m 644 libmp4ff.a %{buildroot}%{_libdir}
install -m 644 mp4ff.h mp4ff_int_types.h %{buildroot}%{_includedir}
cd ../..
 
#remove unneeded files
# rm -f %{buildroot}%{_libdir}/xmms/Input/*a
#clean libtool files

#gw rename it to a more standard name
mkdir -p %{buildroot}%{_mandir}/man1
mv %{buildroot}%{_mandir}/manm/faad.man %{buildroot}%{_mandir}/man1/faad.1

%files
%doc README NEWS TODO AUTHORS ChangeLog
%{_bindir}/faad
%{_mandir}/man1/faad.1*

%files -n %libname
%{_libdir}/libfaad.so.%{major}*

%files -n %develname
%{_libdir}/libfaad.so
%{_includedir}/*

%files -n %staticname
%{_libdir}/libfaad.a
%{_libdir}/libmp4ff.a
