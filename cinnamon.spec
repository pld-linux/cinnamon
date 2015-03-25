%define clutter_version 1.12.2
%define cjs_version 2.3.1
%define cinnamon_desktop_version 2.3.0
%define gobject_introspection_version 1.34.2
%define muffin_version 2.3.0
%define json_glib_version 0.13.2
Summary:	Window management and application launching for GNOME
Name:		cinnamon
Version:	2.4.6
Release:	0.1
License:	GPL v2+ and LGPL v2+
Group:		X11/Applications
Source0:	https://github.com/linuxmint/Cinnamon/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	3ef4250eb889c4f8e99e85601a6d750d
Source1:	polkit-%{name}-authentication-agent-1.desktop
Source2:	%{name}-fedora.gschema.override
Source3:	%{name}-fedora-20.gschema.override
Patch0:		background.patch
Patch1:		autostart.patch
Patch2:		%{name}-settings-apps.patch
Patch3:		set_wheel.patch
Patch4:		network-user-connections.patch
Patch5:		revert_25aef37.patch
Patch6:		%{name}-gtk-3.14.patch
Patch7:		default_panal_launcher.patch
Patch8:		remove_session_bits.patch
Patch9:		show_brightness_fix.patch
URL:		http://cinnamon.linuxmint.com/
BuildRequires:	GConf2-devel
BuildRequires:	NetworkManager-devel
BuildRequires:	cinnamon-desktop-devel >= %{cinnamon_desktop_version}
BuildRequires:	cinnamon-menus-devel
BuildRequires:	cjs-devel >= %{cjs_version}
BuildRequires:	clutter-devel >= %{clutter_version}
BuildRequires:	dbus-glib-devel
BuildRequires:	desktop-file-utils
BuildRequires:	gnome-menus-devel
BuildRequires:	gobject-introspection >= %{gobject_introspection_version}
BuildRequires:	json-glib-devel >= %{json_glib_version}
BuildRequires:	polkit-devel
BuildRequires:	udev-glib-devel
BuildRequires:	upower-devel
# for screencast recorder functionality
BuildRequires:	gstreamer-devel
BuildRequires:	intltool
BuildRequires:	libcanberra-devel
BuildRequires:	libcroco-devel
BuildRequires:	libgnome-keyring-devel
BuildRequires:	libsoup-devel
# used in unused BigThemeImage
BuildRequires:	librsvg-devel
BuildRequires:	muffin-devel >= %{muffin_version}
BuildRequires:	pulseaudio-devel
# Bootstrap requirements
BuildRequires:	gnome-common
BuildRequires:	gtk-doc
# mediia keys
BuildRequires:	colord-devel
BuildRequires:	lcms2-devel
BuildRequires:	libnotify-devel
BuildRequires:	libwacom-devel
BuildRequires:	xorg-driver-input-wacom-devel
BuildRequires:	xorg-lib-libXtst-devel
Requires:	gnome-menus >= 3.0.0-2
Requires:	muffin >= %{muffin_version}
# wrapper script uses to restart old GNOME session if run --replace
# from the command line
Requires:	gobject-introspection >= %{gobject_introspection_version}
# needed for loading SVG's via gdk-pixbuf
Requires:	librsvg2
# needed as it is now split from Clutter
Requires:	json-glib >= %{json_glib_version}
Requires:	polkit >= 0.100
Requires:	upower
# needed for session files
Requires:	cinnamon-session
# needed for schemas
Requires:	at-spi2-atk
# needed for on-screen keyboard
Requires:	caribou
# needed for the user menu
Requires:	accountsservice-libs
# needed for settings
Requires:	PyPAM
Requires:	cinnamon-control-center
Requires:	cinnamon-translations
Requires:	mintlocale
Requires:	opencv-python
Requires:	python-dbus
Requires:	python-gnome-gconf
Requires:	python-lxml
Requires:	python-pexpect
Requires:	python-pillow
Requires:	python-pygobject
# RequiredComponents in the session files
Requires:	cinnamon-screensaver
Requires:	nemo

# metacity is needed for fallback
Requires:	metacity
Requires:	tint2

# needed for theme overrides
Requires:	gnome-themes
Requires:	nimbus-icon-theme
Requires:	zukitwo-gtk2-theme
Requires:	zukitwo-gtk3-theme

# required for keyboard applet
Requires:	gucharmap

# required for network applet
Requires:	network-manager-applet
Requires:	nm-connection-editor

# required for looking glass
Requires:	python-inotify

Provides:	desktop-notification-daemon
Obsoletes:	cinnamon <= 1.8.0-1
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

%prep
%setup -q -n Cinnamon-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

sed -i -e 's@gksu@pkexec@g'  files/usr/bin/cinnamon-settings-users

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
NOCONFIGURE=1 ./autogen.sh
%configure \
	--disable-silent-rules \
	--disable-static \
	--disable-rpath \
	--disable-schemas-compile \
	--enable-introspection=yes \
	--enable-compile-warnings=no

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# Remove shebang from files
sed -i -e '1{\@^#!%{_bindir}/env python@d}' $RPM_BUILD_ROOT%{_prefix}/lib/cinnamon-settings/*/*.py

# Fix perms
chmod +x $RPM_BUILD_ROOT%{_prefix}/lib/cinnamon-settings/bin/{install,remove}Schema.py

# Remove .la file
%{__rm} $RPM_BUILD_ROOT%{_libdir}/cinnamon/libcinnamon.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/cinnamon/libcinnamon-js.la

install -D %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/cinnamon-fedora.gschema.override

# install polkik autostart desktop file
install -D -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/cinnamon.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/cinnamon2d.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/cinnamon-settings*.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/cinnamon-menu-editor.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/polkit-cinnamon-authentication-agent-1.desktop

# fix hardcoded path
sed -i -e 's@/usr/lib/cinnamon-control-center@%{_libdir}/cinnamon-control-center@g' \
	$RPM_BUILD_ROOT%{_prefix}/lib/cinnamon-settings/bin/capi.py

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
%doc COPYING README NEWS AUTHORS
/etc/xdg/menus/cinnamon-applications-merged
/etc/xdg/menus/cinnamon-applications.menu
%attr(755,root,root) %{_bindir}/cinnamon
%attr(755,root,root) %{_bindir}/cinnamon-desktop-editor
%attr(755,root,root) %{_bindir}/cinnamon-extension-tool
%attr(755,root,root) %{_bindir}/cinnamon-json-makepot
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
%attr(755,root,root) %{_bindir}/cinnamon2d
%{_mandir}/man1/cinnamon-extension-tool.1*
%{_mandir}/man1/cinnamon-launcher.1*
%{_mandir}/man1/cinnamon-menu-editor.1*
%{_mandir}/man1/cinnamon-settings.1*
%{_mandir}/man1/cinnamon.1*
%{_mandir}/man1/cinnamon2d.1
%{_mandir}/man1/gnome-session-cinnamon.1
%{_mandir}/man1/gnome-session-cinnamon2d.1
%{_mandir}/man1/gnome-session.1
%{_desktopdir}/cinnamon-menu-editor.desktop
%{_desktopdir}/cinnamon-settings*.desktop
%{_desktopdir}/cinnamon.desktop
%{_desktopdir}/cinnamon2d.desktop
%{_desktopdir}/polkit-cinnamon-authentication-agent-1.desktop
%{_datadir}/dbus-1/services/org.Cinnamon.HotplugSniffer.service
%{_datadir}/dbus-1/services/org.Cinnamon.Melange.service
%{_datadir}/dbus-1/services/org.Cinnamon.Slideshow.service
%{_datadir}/desktop-directories/cinnamon-*.directory
%{_datadir}/glib-2.0/schemas/cinnamon-fedora.gschema.override
%{_datadir}/glib-2.0/schemas/org.cinnamon.gschema.xml
%{_datadir}/cinnamon-session/sessions/cinnamon.session
%{_datadir}/cinnamon-session/sessions/cinnamon2d.session
%{_iconsdir}/hicolor/*/categories/*.svg
%{_iconsdir}/hicolor/*/emblems/cs-*.svg
%{_datadir}/polkit-1/actions/org.cinnamon.settings-users.policy
%{_datadir}/xsessions/cinnamon.desktop
%{_datadir}/xsessions/cinnamon2d.desktop

%dir %{_libdir}/cinnamon
%{_libdir}/cinnamon/Cinnamon-0.1.typelib
%{_libdir}/cinnamon/CinnamonJS-0.1.typelib
%{_libdir}/cinnamon/Gvc-1.0.typelib
%{_libdir}/cinnamon/St-1.0.typelib
%{_libdir}/cinnamon/cinnamon-hotplug-sniffer
%{_libdir}/cinnamon/cinnamon-perf-helper

%attr(755,root,root) %{_libdir}/cinnamon/libcinnamon-js.so
%attr(755,root,root) %{_libdir}/cinnamon/libcinnamon.so

%dir %{_datadir}/cinnamon
%{_datadir}/cinnamon/applets
%{_datadir}/cinnamon/bumpmaps
%{_datadir}/cinnamon/desklets
%{_datadir}/cinnamon/faces
%{_datadir}/cinnamon/icons
%{_datadir}/cinnamon/js
%{_datadir}/cinnamon/search_providers
%{_datadir}/cinnamon/theme
%{_datadir}/cinnamon/thumbnails

%{_prefix}/lib/cinnamon-desktop-editor
%{_prefix}/lib/cinnamon-json-makepot
%{_prefix}/lib/cinnamon-looking-glass
%{_prefix}/lib/cinnamon-menu-editor
%{_prefix}/lib/cinnamon-screensaver-lock-dialog
%{_prefix}/lib/cinnamon-settings-users
%dir %{_prefix}/lib/cinnamon-settings
%dir %{_prefix}/lib/cinnamon-settings/bin
%{_prefix}/lib/cinnamon-settings/bin/*.ui
%attr(755,root,root) %{_prefix}/lib/cinnamon-settings/bin/*.py
%{_prefix}/lib/cinnamon-settings/*.ui
%{_prefix}/lib/cinnamon-settings/*.py
%{_prefix}/lib/cinnamon-settings/data
%{_prefix}/lib/cinnamon-settings/modules
%{_prefix}/lib/cinnamon-slideshow
