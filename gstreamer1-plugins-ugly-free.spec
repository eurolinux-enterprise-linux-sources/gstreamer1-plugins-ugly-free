%global         majorminor 1.0

#global gitrel     140
#global gitcommit  4ca3a22b6b33ad8be4383063e76f79c4d346535d
#global shortcommit %(c=%{gitcommit}; echo ${c:0:5})

%if 0%{?fedora}
%global enable_a52 1
%endif

Name:           gstreamer1-plugins-ugly-free
Version:        1.10.4
Release:        3%{?dist}
Summary:        GStreamer streaming media framework "ugly" plugins

License:        LGPLv2+ and LGPLv2
URL:            http://gstreamer.freedesktop.org/
%if 0%{?gitrel}
# git clone git://anongit.freedesktop.org/gstreamer/gst-plugins-ugly
# cd gst-plugins-ugly; git reset --hard %{gitcommit}; ./autogen.sh; make; make distcheck
# modified with gst-p-ugly-cleanup.sh from SOURCE1
%else
# The source is:
# http://gstreamer.freedesktop.org/src/gst-plugins-ugly/gst-plugins-ugly-%{version}.tar.xz
# modified with gst-p-ugly-cleanup.sh from SOURCE1
%endif
Source0:        gst-plugins-ugly-free-%{version}.tar.xz
Source1:        gst-p-ugly-cleanup.sh

BuildRequires:  gstreamer1-devel >= %{version}
BuildRequires:  gstreamer1-plugins-base-devel >= %{version}

BuildRequires:  check
BuildRequires:  gettext-devel
BuildRequires:  gtk-doc

%if 0%{?enable_a52}
BuildRequires:  liba52-devel
%endif
BuildRequires:  libcdio-devel
BuildRequires:  libdvdread-devel
BuildRequires:  mpg123-devel

Obsoletes:      gstreamer1-plugin-mpg123 < %{version}-%{release}
Provides:       gstreamer1-plugin-mpg123 = %{version}-%{release}


%description
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains plug-ins whose license is not fully compatible with LGPL.

%package devel
Summary:        Development files for the GStreamer media framework "ugly" plug-ins
Requires:       %{name} = %{version}-%{release}
Requires:       gstreamer1-plugins-base-devel


%description devel
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains the development files for the plug-ins whose license
is not fully compatible with LGPL.


%prep
%setup -q -n gst-plugins-ugly-%{version}


%build
# libsidplay was removed as obsolete, not forbidden
%configure --disable-silent-rules --disable-fatal-warnings \
    --with-package-name="GStreamer-plugins-ugly package" \
    --with-package-origin="http://www.redhat.com" \
    --enable-debug --disable-static --enable-gtk-doc --enable-experimental \
    --disable-amrnb --disable-amrwb --disable-lame \
    %{!?enable_a52:--disable-a52dec} \
    --disable-mpeg2dec --disable-sidplay --disable-twolame --disable-x264
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Register as an AppStream component to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/gstreamer-ugly-free.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2013 Richard Hughes <richard@hughsie.com> -->
<component type="codec">
  <id>gstreamer-ugly-free</id>
  <metadata_license>CC0-1.0</metadata_license>
  <name>GStreamer Multimedia Codecs - Extra</name>
  <summary>Multimedia playback for CD, DVD, and MP3</summary>
  <description>
    <p>
      This addon includes several additional codecs that have good quality and
      correct functionality, but whose license is not fully compatible with LGPL.
    </p>
    <p>
      These codecs can be used to encode and decode media files where the
      format is not patent encumbered.
    </p>
    <p>
      A codec decodes audio and video for for playback or editing and is also
      used for transmission or storage.
      Different codecs are used in video-conferencing, streaming media and
      video editing applications.
    </p>
  </description>
  <keywords>
    <keyword>CD</keyword>
    <keyword>DVD</keyword>
    <keyword>MP3</keyword>
  </keywords>
  <url type="homepage">http://gstreamer.freedesktop.org/</url>
  <url type="bugtracker">https://bugzilla.gnome.org/enter_bug.cgi?product=GStreamer</url>
  <url type="help">http://gstreamer.freedesktop.org/documentation/</url>
  <url type="donation">http://www.gnome.org/friends/</url>
  <update_contact><!-- upstream-contact_at_email.com --></update_contact>
</component>
EOF

%find_lang gst-plugins-ugly-%{majorminor}
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%files -f gst-plugins-ugly-%{majorminor}.lang
%license COPYING
%doc AUTHORS README REQUIREMENTS

%{_datadir}/appdata/*.appdata.xml

# Plugins without external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstxingmux.so

# Plugins with external dependencies
%if 0%{?enable_a52}
%{_libdir}/gstreamer-%{majorminor}/libgsta52dec.so
%endif
%{_libdir}/gstreamer-%{majorminor}/libgstcdio.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvdread.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpg123.so

%files devel
%doc %{_datadir}/gtk-doc/html/gst-plugins-ugly-plugins-%{majorminor}


%changelog
* Tue Oct 17 2017 Wim Taymans <wtaymans@redhat.com> - 1.10.4-3
- Fix for RHEL
- Disable a52dec
Resolves: #1481754

* Thu May 11 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 1.10.4-2
- Initial Fedora spec file
