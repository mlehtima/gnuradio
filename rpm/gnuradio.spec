# To prepare for the future changes in RPM macro support
%if ! %{defined python3_sitearch}
%define python3_sitearch /%{_libdir}/python3.8/site-packages
%endif

%bcond_without docs

Name:		gnuradio
Version:	3.9.8.0
Release:	0
Summary:	Software defined radio framework
License:	GPLv3
URL:		https://gnuradio.org
Source0:	%{name}-%{version}.tar.xz
Source99:	%{name}-rpmlintrc
BuildRequires:	boost-devel
BuildRequires:	cmake
#BuildRequires:	cppunit-devel
#BuildRequires:	cppzmq-devel
%if %{with docs}
BuildRequires:	doxygen
# TeX is required for formula rendering
#BuildRequires:	texlive-dvips
#BuildRequires:	texlive-latex
#BuildRequires:	tex(newunicodechar.sty)
%endif
BuildRequires:	fdupes
BuildRequires:	fftw3-devel
BuildRequires:	gcc-c++
BuildRequires:	gmp-devel
BuildRequires:	gsl-devel
BuildRequires:	log4cpp-devel
#BuildRequires:	libgsm-devel
#BuildRequires:	libmpir-devel
#BuildRequires:	memory-constraints
BuildRequires:	orc-devel
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(alsa)
BuildRequires:	python-rpm-macros
BuildRequires:	pybind11-devel
BuildRequires:	python3-devel
BuildRequires:	python3-lxml
BuildRequires:	python3-numpy
BuildRequires:	python3-six
# grc
#BuildRequires:	typelib(Gtk) = 3.0
#BuildRequires:	typelib(PangoCairo) = 1.0
#BuildRequires:	typelib(cairo) = 1.0
#BuildRequires:	python3-cairo
#BuildRequires:	python3-gobject
#BuildRequires:	python3-gobject-cairo
#BuildRequires:	python3-pyaml >= 3.11
# gr-utils
#BuildRequires:	python3-click
#BuildRequires:	python3-click-plugins
# gr-video-sdl
#BuildRequires:	libSDL-devel

#BuildRequires:	python3-qt5-devel
BuildRequires:	qwt6-devel
#BuildRequires:	swig >= 3.0.8
#BuildRequires:	uhd-devel
#BuildRequires:	update-desktop-files
#BuildRequires:	pkgconfig(codec2)
#BuildRequires:	pkgconfig(libusb-1.0)
#BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(volk) >= 2.0

# gr_modtool dependencies
#Requires:	python3-click
#Requires:	python3-click-plugins
#Requires:	python3-mako
#Requires:	python3-numpy
#Requires:	python3-qt5

%description
GNU Radio is a collection of software that when combined with minimal
hardware, allows the construction of radios where the actual waveforms
transmitted and received are defined by software. What this means is
that it turns the digital modulation schemes used in today's high
performance wireless devices into software problems.

%package -n libgnuradio
Summary:	Libraries for GNU Radio

%description -n libgnuradio
GNU Radio is a collection of software that when combined with minimal
hardware, allows the construction of radios where the actual waveforms
transmitted and received are defined by software. What this means is
that it turns the digital modulation schemes used in today's high
performance wireless devices into software problems.

This package contains the libraries for GNU Radio.

%package -n python3-%{name}
Summary:	GNU Radio Python 3 module

%description -n python3-%{name}
GNU Radio Python 3 module

%package devel
Summary:	Deveopment files for GNU Radio
Requires:	%{name} = %{version}

%description devel
GNU Radio is a collection of software that when combined with minimal
hardware, allows the construction of radios where the actual waveforms
transmitted and received are defined by software. What this means is
that it turns the digital modulation schemes used in today's high
performance wireless devices into software problems.

This package contains libraries and header files for developing
applications that use GNU Radio.

%package doc
Summary:	GNU Radio documentation
Requires:	%{name} = %{version}
BuildArch:	noarch

%description doc
GNU Radio is a collection of software that when combined with minimal
hardware, allows the construction of radios where the actual waveforms
transmitted and received are defined by software. What this means is
that it turns the digital modulation schemes used in today's high
performance wireless devices into software problems.

This package contains documentation for GNU Radio.

%package	examples
Summary:	GNU Radio examples
Requires:	%{name} = %{version}

%description examples
GNU Radio is a collection of software that when combined with minimal
hardware, allows the construction of radios where the actual waveforms
transmitted and received are defined by software. What this means is
that it turns the digital modulation schemes used in today's high
performance wireless devices into software problems.

This package contains some examples of using GNU Radio.

%prep
%autosetup -n %{name}-%{version}/%{name}

# remove buildtime from documentation
sed -i 's|^HTML_TIMESTAMP         = YES|HTML_TIMESTAMP         = NO|' docs/doxygen/Doxyfile.in

# protect the template files from %%cmake macro magic / mangling
find  gr-utils/modtool/templates/gr-newmod -name CMakeLists.txt -exec mv '{}' '{}.tmpl' \;

%build
#limit_build -m 2000
mkdir -p build
cd build
%cmake \
  -DENABLE_MANPAGES=OFF \
  -DGR_PYTHON_DIR=%{python3_sitearch} \
  -DPYTHON_EXECUTABLE=%{__python3} \
  -DSYSCONFDIR=%{_sysconfdir} \
  ..

%make_build CFLAGS="%{optflags} -fno-strict-aliasing" CXXFLAGS="%{optflags} -fno-strict-aliasing"

%install
# move the template files back
find  gr-utils/modtool/templates/gr-newmod -name CMakeLists.txt.tmpl -execdir mv '{}' 'CMakeLists.txt' \;

cd build
%make_install
#make_install -C build

install -d %{buildroot}%{_docdir}/%{name}
mv %{buildroot}/%{_datadir}/doc/%{name}-*/* %{buildroot}%{_docdir}/%{name}/

# Compiled examples are installed as "data", but are arch dependent
install -dm 0755 %{buildroot}%{_libdir}/gnuradio
mv %{buildroot}%{_datadir}/gnuradio/examples %{buildroot}%{_libdir}/gnuradio/

# remove duplicate icons (just keep hicolor)
rm -rf %{buildroot}%{_datadir}/%{name}/grc/freedesktop
rm -rf %{buildroot}%{_datadir}/icons/gnome

%fdupes %{buildroot}%{_docdir}
%fdupes %{buildroot}%{_includedir}
%fdupes %{buildroot}%{_libdir}

%post -n libgnuradio -p /sbin/ldconfig
%postun -n libgnuradio -p /sbin/ldconfig

%files
%license COPYING
%{_bindir}/*
%dir %{_datadir}/gnuradio
#{_datadir}/gnuradio/grc/
#{_datadir}/gnuradio/modtool/
#{_datadir}/gnuradio/themes/
%{_datadir}/gnuradio/fec/
%{_datadir}/gnuradio/clang-format.conf
#{_datadir}/icons/hicolor/*/apps/gnuradio-grc.png
#{_datadir}/applications/gnuradio-grc.desktop
#{_datadir}/mime/packages/gnuradio-grc.xml
%dir %{_sysconfdir}/gnuradio
%dir %{_sysconfdir}/gnuradio/conf.d
%config(noreplace) %{_sysconfdir}/gnuradio/conf.d/*.conf
%dir %{_docdir}/%{name}/
%{_docdir}/%{name}/README*
%{_docdir}/%{name}/CHANGELOG*
%{_docdir}/%{name}/CONTRIBUTING*
# doc package
%exclude %{_docdir}/%{name}/html/
%exclude %{_docdir}/%{name}/xml/
%exclude %{_docdir}/%{name}/*.py
%exclude %{_docdir}/%{name}/*.grc

%files -n libgnuradio
%{_libdir}/libgnuradio*.so.*

%files  -n python3-%{name}
%{python3_sitearch}/*

%files devel
%{_includedir}/%{name}/
%{_includedir}/pmt/
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/gnuradio/

%files doc
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/html/
%{_docdir}/%{name}/xml/
#{_docdir}/%{name}/*.py
#{_docdir}/%{name}/*.grc

%files examples
%dir %{_libdir}/gnuradio
%{_libdir}/gnuradio/examples/
