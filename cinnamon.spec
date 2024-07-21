# TODO:
# - fulfill dependencies
# -- python3 pampy or pam module - `import pam` or `import PAM`
# -- mintlocale (what for?)
#
# Conditional build:
%bcond_without	apidocs	# API documentation

%define	translations_version	6.2.2
%define	cinnamon_desktop_ver	2.4.0
%define	cinnamon_menus_ver	4.8.0
%define	cjs_ver			4.8.0
%define	gi_ver			1.34.2
%define	glib_ver		1:2.52.0
%define	muffin_ver		5.2.0
Summary:	Window management and application launching for Cinnamon
Summary(pl.UTF-8):	Zarządzanie oknami i uruchamianie aplikacji dla środowiska Cinnamon
Name:		cinnamon
Version:	6.2.7
Release:	0.1
License:	GPL v2+ and LGPL v2+
Group:		X11/Applications
#Source0Download: https://github.com/linuxmint/Cinnamon/tags
Source0:	https://github.com/linuxmint/Cinnamon/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f1096b77c0639e929690cc2f1e9505af
#Source1Download: https://github.com/linuxmint/cinnamon-translations/tags
Source1:	https://github.com/linuxmint/cinnamon-translations/archive/%{translations_version}/cinnamon-translations-%{translations_version}.tar.gz
# Source1-md5:	ca66b0eadc9416ef66384b3b278554ad
Source2:	polkit-%{name}-authentication-agent-1.desktop
Source3:	%{name}-common.gschema.override
Source4:	%{name}-apps.gschema.override
Patch0:		background.patch
Patch1:		autostart.patch
Patch2:		%{name}-gtkdoc.patch
Patch3:		set_wheel.patch
Patch4:		fix_path.patch
Patch5:		revert_25aef37.patch
Patch6:		%{name}-menu.patch
Patch7:		default_panal_launcher.patch
URL:		https://github.com/linuxmint/Cinnamon
BuildRequires:	NetworkManager-devel
BuildRequires:	OpenGL-devel
BuildRequires:	at-spi2-atk-devel >= 2.0
BuildRequires:	cinnamon-desktop-devel >= %{cinnamon_desktop_ver}
BuildRequires:	cinnamon-menus-devel >= %{cinnamon_menus_ver}
BuildRequires:	cjs-devel >= %{cjs_ver}
BuildRequires:	dbus-devel
BuildRequires:	desktop-file-utils
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= %{glib_ver}
BuildRequires:	gobject-introspection-devel >= %{gi_ver}
BuildRequires:	gtk+3-devel >= 3.12.0
# for screencast recorder functionality
BuildRequires:	gstreamer-devel >= 1.0
BuildRequires:	gtk-doc >= 1.15
BuildRequires:	intltool >= 0.40
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	meson >= 0.56.0
BuildRequires:	muffin-devel >= %{muffin_ver}
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig >= 1:0.22
BuildRequires:	polkit-devel >= 0.100
BuildRequires:	python3 >= 1:3.2
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	xapps-devel >= 2.6.0
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXfixes-devel
Requires:	glib2 >= %{glib_ver}
Requires:	muffin >= %{muffin_ver}
# wrapper script uses to restart old GNOME session if run --replace
# from the command line
Requires:	gobject-introspection >= %{gi_ver}
# needed for loading SVG's via gdk-pixbuf
Requires:	librsvg >= 2.0
Requires:	polkit >= 0.100
# required by polkit-cinnamon-authentication-agent-1.desktop
Requires:	polkit-gnome
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
Requires:	cinnamon-nemo
Requires:	mintlocale
Requires:	python3-dbus
Requires:	python3-pexpect
Requires:	python3-pillow
Requires:	python3-pygobject3
# or python3-pam; needed for settings (cinnamon-settings/modules/cs_user.py)
Requires:	python3-PyPAM
# RequiredComponents in the session files
Requires:	cinnamon-screensaver

# needed for theme overrides
Requires:	gnome-backgrounds

# required for keyboard applet
Requires:	gucharmap

# nm-applet, nm-connection-editor required for network applet
Requires:	NetworkManager-applet

# required for looking glass
Requires:	python3-pyinotify

# metacity is needed as fallback for cinnamon
Suggests:	metacity
# mate-panel > gnome-panel > tint2
Suggests:	gnome-panel
Suggests:	mate-panel
Suggests:	tint2

Provides:	desktop-notification-daemon
Obsoletes:	cinnamon-2d < 2.4
Obsoletes:	cinnamon-menu-editor < 2.4
Obsoletes:	cinnamon-settings < 2.4
Obsoletes:	cinnamon-translations < 4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
BuildArch:	noarch

%description apidocs
API documentation for Cinnamon desktop.

%description apidocs -l pl.UTF-8
Dokumentacja API środowiska Cinnamon.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
%meson build \
	--default-library=shared \
	%{?with_apidocs:-Ddocs=true}

%ninja_build -C build

%{__make} -C cinnamon-translations-%{translations_version}

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

install -Dp %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/cinnamon-common.gschema.override
install -Dp %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/cinnamon-apps.gschema.override

# install polkit autostart desktop file
%{__sed} -e 's,@libexecdir@,%{_libexecdir},' %{SOURCE2} >$RPM_BUILD_ROOT%{_desktopdir}/polkit-cinnamon-authentication-agent-1.desktop

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/cinnamon.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/cinnamon2d.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/cinnamon-settings*.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/cinnamon-menu-editor.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/polkit-cinnamon-authentication-agent-1.desktop

%py3_comp $RPM_BUILD_ROOT%{py3_sitescriptdir}/cinnamon
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitescriptdir}/cinnamon

# no headers
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/cinnamon/{Cinnamon-0.1,St-1.0}.gir

# to fix man page brp check (note: do not package)
touch $RPM_BUILD_ROOT%{_mandir}/man1/cinnamon-session.1

cd cinnamon-translations-%{translations_version}
for f in usr/share/locale/*/LC_MESSAGES/%{name}.mo ; do
	install -Dp "$f" "$RPM_BUILD_ROOT/$f"
done
cd ..

# not supported by glibc (as of 2.39)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{ie,frp,jv,ksw,nap,rue,qu,sco}
# almost empty version of nb(?) under withdrawn code
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/no

%find_lang %{name}

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

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README.rst debian/changelog
%attr(755,root,root) %{_bindir}/cinnamon
%attr(755,root,root) %{_bindir}/cinnamon-calendar-server
%attr(755,root,root) %{_bindir}/cinnamon-close-dialog
%attr(755,root,root) %{_bindir}/cinnamon-dbus-command
%attr(755,root,root) %{_bindir}/cinnamon-desktop-editor
%attr(755,root,root) %{_bindir}/cinnamon-display-changes-dialog
%attr(755,root,root) %{_bindir}/cinnamon-file-dialog
%attr(755,root,root) %{_bindir}/cinnamon-hover-click
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
%attr(755,root,root) %{_bindir}/cinnamon-spice-updater
%attr(755,root,root) %{_bindir}/cinnamon-subprocess-wrapper
%attr(755,root,root) %{_bindir}/cinnamon-xlet-makepot
%attr(755,root,root) %{_bindir}/cinnamon2d
%attr(755,root,root) %{_bindir}/xlet-about-dialog
%attr(755,root,root) %{_bindir}/xlet-settings
%dir %{_libdir}/cinnamon
%attr(755,root,root) %{_libdir}/cinnamon/libcinnamon.so
%attr(755,root,root) %{_libdir}/cinnamon/libst.so
%{_libdir}/cinnamon/Cinnamon-0.1.typelib
%{_libdir}/cinnamon/St-1.0.typelib
%attr(755,root,root) %{_libexecdir}/cinnamon-calendar-server.py
%attr(755,root,root) %{_libexecdir}/cinnamon-hotplug-sniffer
%attr(755,root,root) %{_libexecdir}/cinnamon-perf-helper
%{py3_sitescriptdir}/cinnamon
/etc/xdg/menus/cinnamon-applications-merged
/etc/xdg/menus/cinnamon-applications.menu
%dir %{_datadir}/cinnamon
%{_datadir}/cinnamon/applets
%{_datadir}/cinnamon/bumpmaps
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
%{_datadir}/cinnamon/cinnamon-settings/*.svg
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
%{_datadir}/cinnamon-session/sessions/cinnamon-wayland.session
%{_datadir}/cinnamon-session/sessions/cinnamon2d.session
%{_datadir}/dbus-1/services/org.Cinnamon.HotplugSniffer.service
%{_datadir}/dbus-1/services/org.Cinnamon.Melange.service
%{_datadir}/dbus-1/services/org.Cinnamon.Slideshow.service
%{_datadir}/dbus-1/services/org.cinnamon.CalendarServer.service
%{_datadir}/desktop-directories/cinnamon-*.directory
%{_datadir}/glib-2.0/schemas/cinnamon-apps.gschema.override
%{_datadir}/glib-2.0/schemas/cinnamon-common.gschema.override
%{_datadir}/glib-2.0/schemas/org.cinnamon.gestures.gschema.xml
%{_datadir}/glib-2.0/schemas/org.cinnamon.gschema.xml
%{_datadir}/polkit-1/actions/org.cinnamon.settings-users.policy
%{_datadir}/wayland-sessions/cinnamon-wayland.desktop
%{_datadir}/xdg-desktop-portal/x-cinnamon-portals.conf
%{_datadir}/xsessions/cinnamon.desktop
%{_datadir}/xsessions/cinnamon2d.desktop
%{_desktopdir}/cinnamon-killer-daemon.desktop
%{_desktopdir}/cinnamon-menu-editor.desktop
%{_desktopdir}/cinnamon-onscreen-keyboard.desktop
%{_desktopdir}/cinnamon-settings*.desktop
%{_desktopdir}/cinnamon-wayland.desktop
%{_desktopdir}/cinnamon.desktop
%{_desktopdir}/cinnamon2d.desktop
%{_desktopdir}/polkit-cinnamon-authentication-agent-1.desktop
%{_iconsdir}/hicolor/24x24/actions/cinnamon-hc-*-click.png
%{_iconsdir}/hicolor/scalable/actions/cinnamon-caps-lock-*symbolic.svg
%{_iconsdir}/hicolor/scalable/actions/cinnamon-num-lock-*symbolic.svg
%{_iconsdir}/hicolor/scalable/actions/list-edit-symbolic.svg
%{_iconsdir}/hicolor/scalable/actions/pan-*-symbolic.svg
%{_iconsdir}/hicolor/scalable/actions/pan-*-symbolic-rtl.svg
%{_iconsdir}/hicolor/scalable/apps/cinnamon.svg
%{_iconsdir}/hicolor/scalable/apps/cinnamon-panel-launcher.svg
%{_iconsdir}/hicolor/scalable/apps/cinnamon-symbolic.svg
%{_iconsdir}/hicolor/scalable/apps/cinnamon-virtual-keyboard.svg
%{_iconsdir}/hicolor/scalable/apps/cinnamon-wayland_badge-symbolic.svg
%{_iconsdir}/hicolor/scalable/apps/cinnamon2d_badge-symbolic.svg
%{_iconsdir}/hicolor/scalable/apps/cinnamon_badge-symbolic.svg
%{_iconsdir}/hicolor/scalable/apps/removable-drives.svg
%{_iconsdir}/hicolor/scalable/categories/cinnamon-all-applications-symbolic.svg
%{_iconsdir}/hicolor/scalable/categories/cs-*.svg
%{_iconsdir}/hicolor/scalable/devices/audio-speaker-*.svg
%{_iconsdir}/hicolor/scalable/devices/audio-subwoofer.svg
%{_iconsdir}/hicolor/scalable/devices/bluetooth.svg
%{_iconsdir}/hicolor/scalable/devices/cpu-symbolic.svg
%{_iconsdir}/hicolor/scalable/emblems/cs-xlet-*.svg
%{_mandir}/man1/cinnamon.1*
%{_mandir}/man1/cinnamon-launcher.1*
%{_mandir}/man1/cinnamon-looking-glass.1*
%{_mandir}/man1/cinnamon-menu-editor.1*
%{_mandir}/man1/cinnamon-screensaver-lock-dialog.1*
%{_mandir}/man1/cinnamon-settings.1*
%{_mandir}/man1/cinnamon-session-cinnamon.1*
%{_mandir}/man1/cinnamon-session-cinnamon2d.1*
%{_mandir}/man1/cinnamon2d.1*
%exclude %{_mandir}/man1/cinnamon-session.1

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/cinnamon
%{_gtkdocdir}/cinnamon-js
%{_gtkdocdir}/cinnamon-st
%{_gtkdocdir}/cinnamon-tutorials
%endif
