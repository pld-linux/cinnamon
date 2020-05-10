%define	cinnamon_desktop_ver	2.4.0
%define	cjs_ver			3.2.0
%define	gi_ver			1.34.2
%define	muffin_version		4.0.3
Summary:	Window management and application launching for GNOME
Summary(pl.UTF-8):	Zarządzanie oknami i uruchamianie aplikacji dla GNOME
Name:		cinnamon
Version:	4.4.8
Release:	0.1
License:	GPL v2+ and LGPL v2+
Group:		X11/Applications
Source0:	https://github.com/linuxmint/Cinnamon/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4f7901e5f32b4641a4e1388b79821a0d
Source1:	polkit-%{name}-authentication-agent-1.desktop
Source2:	%{name}-fedora.gschema.override
Patch0:		background.patch
Patch1:		autostart.patch
Patch3:		set_wheel.patch
Patch5:		revert_25aef37.patch
Patch7:		default_panal_launcher.patch
URL:		https://github.com/linuxmint/Cinnamon
BuildRequires:	NetworkManager-devel
BuildRequires:	OpenGL-devel
BuildRequires:	at-spi2-atk-devel >= 2.0
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	cinnamon-desktop-devel >= %{cinnamon_desktop_ver}
BuildRequires:	cinnamon-menus-devel
BuildRequires:	cjs-devel >= %{cjs_ver}
BuildRequires:	dbus-glib-devel
BuildRequires:	desktop-file-utils
BuildRequires:	glib2-devel >= 1:2.35.0
BuildRequires:	gobject-introspection-devel >= %{gi_ver}
BuildRequires:	gtk+3-devel >= 3.12.0
# for screencast recorder functionality
BuildRequires:	gstreamer-devel >= 1.0
BuildRequires:	gtk-doc >= 1.15
BuildRequires:	intltool >= 0.40
BuildRequires:	libcroco-devel >= 0.6.2
BuildRequires:	libsoup-devel >= 2.4
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	muffin-devel >= %{muffin_ver}
BuildRequires:	pkgconfig >= 1:0.22
BuildRequires:	polkit-devel >= 0.100
BuildRequires:	startup-notification-devel >= 0.11
BuildRequires:	xorg-lib-libX11-devel
Requires:	muffin >= %{muffin_ver}
# wrapper script uses to restart old GNOME session if run --replace
# from the command line
Requires:	gobject-introspection >= %{gi_ver}
# needed for loading SVG's via gdk-pixbuf
Requires:	librsvg >= 2.0
Requires:	polkit >= 0.100
# through UPowerGlib typelib
Requires:	upower
# needed for session files
Requires:	cinnamon-session
# needed for schemas
Requires:	at-spi2-atk
# through Caribou typelib; needed for on-screen keyboard
Requires:	caribou
# needed for the user menu
Requires:	accountsservice-libs
Requires:	cinnamon-control-center
Requires:	cinnamon-translations
Requires:	mintlocale
Requires:	python-dbus
Requires:	python-pexpect
Requires:	python-pillow
Requires:	python-pygobject3
# needed for settings (cinnamon-settings/modules/cs_user.py)
Requires:	python3-PyPAM
# RequiredComponents in the session files
Requires:	cinnamon-screensaver
Requires:	nemo

# metacity is needed for fallback
Requires:	metacity
Requires:	tint2

# needed for theme overrides
Requires:	gnome-themes

# required for keyboard applet
Requires:	gucharmap

# required for network applet
Requires:	NetworkManager-applet
Requires:	nm-connection-editor

# required for looking glass
Requires:	python-inotify

Provides:	desktop-notification-daemon
Obsoletes:	cinnamon-2d
Obsoletes:	cinnamon-menu-editor
Obsoletes:	cinnamon-settings

%description
Cinnamon is a Linux desktop which provides advanced innovative
features and a traditional user experience.

The desktop layout is similar to Gnome 2. The underlying technology is
forked from Gnome Shell. The emphasis is put on making users feel at
home and providing them with an easy to use and comfortable desktop
experience.

%description -l pl.UTF-8
Cinnamon to środowisko graficzne dla Linuksa zapewniające
zaawansowane, innowacyjne możliwości i tradycyjną obsługę.

Układ jest podobny do Gnome 2. Implementacja wywodzi się z powłoki
Gnome Shell. Nacisk położony jest na to, aby użytkownicy czuli się jak
w domu, oraz żeby zapewnić im łatwe w użyciu i wygodne środowisko.

%package apidocs
Summary:	API documentation for Cinnamon desktop
Summary(pl.UTF-8):	Dokumentacja API środowiska Cinnamon
Group:		Documentation
%if "%{_rpmversion}" >= "4.6"
BuildArch:	noarch
%endif

%description apidocs
API documentation for Cinnamon desktop.

%description apidocs -l pl.UTF-8
Dokumentacja API środowiska Cinnamon.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch5 -p1
%patch7 -p1

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
install -d m4
%{__glib_gettextize}
%{__gtkdocize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-static \
	--disable-rpath \
	--disable-schemas-compile \
	--enable-introspection \
	--enable-compile-warnings=no \
	--with-ca-certificates=/etc/certs/ca-certificates.crt \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/cinnamon/libcinnamon.la

install -D %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/cinnamon-fedora.gschema.override

# install polkit autostart desktop file
%{__sed} -e 's,@libexecdir@,%{_libexecdir},' %{SOURCE1} >$RPM_BUILD_ROOT%{_desktopdir}/polkit-cinnamon-authentication-agent-1.desktop

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/cinnamon.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/cinnamon2d.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/cinnamon-settings*.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/cinnamon-menu-editor.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/polkit-cinnamon-authentication-agent-1.desktop

# fix hardcoded path
#sed -i -e 's@/usr/lib/cinnamon-control-center@%{_libdir}/cinnamon-control-center@g' \
#	$RPM_BUILD_ROOT%{_prefix}/lib/cinnamon-settings/bin/capi.py

# create directory for lang files
install -d $RPM_BUILD_ROOT%{_datadir}/cinnamon/locale

# to fix man page brp check
touch $RPM_BUILD_ROOT%{_mandir}/man1/gnome-session.1

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
if [ $1 -eq 0 ]; then
	%update_icon_cache hicolor
	%glib_compile_schemas
fi

%posttrans
%update_icon_cache hicolor
%glib_compile_schemas

%files
%defattr(644,root,root,755)
%doc AUTHORS README.rst
%attr(755,root,root) %{_bindir}/cinnamon
%attr(755,root,root) %{_bindir}/cinnamon-desktop-editor
%attr(755,root,root) %{_bindir}/cinnamon-file-dialog
%attr(755,root,root) %{_bindir}/cinnamon-install-spice
%attr(755,root,root) %{_bindir}/cinnamon-json-makepot
%attr(755,root,root) %{_bindir}/cinnamon-killer-daemon
%attr(755,root,root) %{_bindir}/cinnamon-launcher
%attr(755,root,root) %{_bindir}/cinnamon-looking-glass
%attr(755,root,root) %{_bindir}/cinnamon-menu-editor
%attr(755,root,root) %{_bindir}/cinnamon-preview-gtk-theme
%attr(755,root,root) %{_bindir}/cinnamon-screensaver-lock-dialog
%attr(755,root,root) %{_bindir}/cinnamon-session-cinnamon
%attr(755,root,root) %{_bindir}/cinnamon-session-cinnamon2d
%attr(755,root,root) %{_bindir}/cinnamon-settings
%attr(755,root,root) %{_bindir}/cinnamon-settings-users
%attr(755,root,root) %{_bindir}/cinnamon-slideshow
%attr(755,root,root) %{_bindir}/cinnamon-subprocess-wrapper
%attr(755,root,root) %{_bindir}/cinnamon-xlet-makepot
%attr(755,root,root) %{_bindir}/cinnamon2d
%attr(755,root,root) %{_bindir}/xlet-about-dialog
%attr(755,root,root) %{_bindir}/xlet-settings
%dir %{_libdir}/cinnamon
%attr(755,root,root) %{_libdir}/cinnamon/libcinnamon.so
%{_libdir}/cinnamon/Cinnamon-0.1.typelib
%{_libdir}/cinnamon/St-1.0.typelib
%if "%{_libexecdir}" != "%{_libdir}"
%dir %{_libexecdir}/cinnamon
%endif
%attr(755,root,root) %{_libexecdir}/cinnamon/cinnamon-hotplug-sniffer
%attr(755,root,root) %{_libexecdir}/cinnamon/cinnamon-perf-helper
/etc/xdg/menus/cinnamon-applications-merged
/etc/xdg/menus/cinnamon-applications.menu
%dir %{_datadir}/cinnamon
%{_datadir}/cinnamon/applets
%{_datadir}/cinnamon/bumpmaps
%attr(755,root,root) %{_datadir}/cinnamon/cinnamon-dbus-command
%{_datadir}/cinnamon/cinnamon-desktop-editor
%{_datadir}/cinnamon/cinnamon-looking-glass
%{_datadir}/cinnamon/cinnamon-menu-editor
%{_datadir}/cinnamon/cinnamon-screensaver-lock-dialog
%{_datadir}/cinnamon/cinnamon-settings-users
%dir %{_datadir}/cinnamon/cinnamon-settings
%{_datadir}/cinnamon/cinnamon-settings/bin
%{_datadir}/cinnamon/cinnamon-settings/modules
%attr(755,root,root) %{_datadir}/cinnamon/cinnamon-settings/cinnamon-settings.py
%attr(755,root,root) %{_datadir}/cinnamon/cinnamon-settings/xlet-settings.py
%{_datadir}/cinnamon/cinnamon-settings/config.py
%{_datadir}/cinnamon/cinnamon-settings/icons
%{_datadir}/cinnamon/cinnamon-settings/*.ui
%{_datadir}/cinnamon/cinnamon-slideshow
%{_datadir}/cinnamon/desklets
%{_datadir}/cinnamon/faces
%{_datadir}/cinnamon/icons
%{_datadir}/cinnamon/js
%{_datadir}/cinnamon/search_providers
%{_datadir}/cinnamon/sounds
%{_datadir}/cinnamon/theme
%{_datadir}/cinnamon/thumbnails
%{_datadir}/cinnamon-session/sessions/cinnamon.session
%{_datadir}/cinnamon-session/sessions/cinnamon2d.session
%{_datadir}/dbus-1/services/org.Cinnamon.HotplugSniffer.service
%{_datadir}/dbus-1/services/org.Cinnamon.Melange.service
%{_datadir}/dbus-1/services/org.Cinnamon.Slideshow.service
%{_datadir}/desktop-directories/cinnamon-*.directory
%{_datadir}/glib-2.0/schemas/cinnamon-fedora.gschema.override
%{_datadir}/glib-2.0/schemas/org.cinnamon.gschema.xml
%{_datadir}/polkit-1/actions/org.cinnamon.settings-users.policy
%{_datadir}/xsessions/cinnamon.desktop
%{_datadir}/xsessions/cinnamon2d.desktop
%{_desktopdir}/cinnamon-killer-daemon.desktop
%{_desktopdir}/cinnamon-menu-editor.desktop
%{_desktopdir}/cinnamon-onscreen-keyboard.desktop
%{_desktopdir}/cinnamon-settings*.desktop
%{_desktopdir}/cinnamon.desktop
%{_desktopdir}/cinnamon2d.desktop
%{_desktopdir}/polkit-cinnamon-authentication-agent-1.desktop
%{_iconsdir}/hicolor/scalable/actions/caps-lock*-symbolic.svg
%{_iconsdir}/hicolor/scalable/actions/list-edit-symbolic.svg
%{_iconsdir}/hicolor/scalable/actions/num-lock*-symbolic.svg
%{_iconsdir}/hicolor/scalable/actions/pan-*-symbolic.svg
%{_iconsdir}/hicolor/scalable/actions/pan-*-symbolic-rtl.svg
%{_iconsdir}/hicolor/scalable/apps/cinnamon.svg
%{_iconsdir}/hicolor/scalable/apps/cinnamon-panel-launcher.svg
%{_iconsdir}/hicolor/scalable/apps/cinnamon-symbolic.svg
%{_iconsdir}/hicolor/scalable/apps/removable-drives.svg
%{_iconsdir}/hicolor/scalable/categories/cs-*.svg
%{_iconsdir}/hicolor/scalable/devices/audio-speaker-*.svg
%{_iconsdir}/hicolor/scalable/devices/audio-subwoofer.svg
%{_iconsdir}/hicolor/scalable/devices/bluetooth.svg
%{_iconsdir}/hicolor/scalable/devices/cpu-symbolic.svg
%{_iconsdir}/hicolor/scalable/emblems/cs-xlet-*.svg
%{_mandir}/man1/cinnamon-launcher.1*
%{_mandir}/man1/cinnamon-menu-editor.1*
%{_mandir}/man1/cinnamon-settings.1*
%{_mandir}/man1/cinnamon.1*
%{_mandir}/man1/cinnamon2d.1
%{_mandir}/man1/gnome-session-cinnamon.1
%{_mandir}/man1/gnome-session-cinnamon2d.1
%{_mandir}/man1/gnome-session.1

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/cinnamon
%{_gtkdocdir}/cinnamon-js
%{_gtkdocdir}/cinnamon-st
%{_gtkdocdir}/cinnamon-tutorials
