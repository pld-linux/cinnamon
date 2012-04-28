%define	_internel_version  a8b1a03
%define clutter_version 1.4.0
%define gobject_introspection_version 0.10.1
%define muffin_version 1.0.2
%define eds_version 2.91.6
%define json_glib_version 0.13.2
Summary:	Window management and application launching for GNOME
Name:		cinnamon
Version:	1.4.0
Release:	0.2
License:	GPL v2+
Group:		X11/Applications
URL:		http://cinnamon.linuxmint.com/
Source0:	https://github.com/linuxmint/Cinnamon/tarball/1.4/%{name}-%{version}.tar.gz
# Source0-md5:	2afb656fb8834571c902ba74f1f5116c
Source1:	%{name}.desktop
Source2:	%{name}.session
Source3:	menu.png
# Replace mint favorites with fedora gnome-shell defaults
Patch0:		%{name}-favourite-apps-firefox.patch
Patch1:		menu.patch
Patch2:		settings.patch
Patch3:		logout_theme.patch
Patch4:		gir_bluetooth.patch
BuildRequires:	GConf2
BuildRequires:	NetworkManager-devel
BuildRequires:	ca-certificates
BuildRequires:	clutter-devel >= %{clutter_version}
BuildRequires:	dbus-glib-devel
BuildRequires:	desktop-file-utils
BuildRequires:	evolution-data-server-devel >= %{eds_version}
BuildRequires:	gjs-devel >= 0.7.14-6
BuildRequires:	glib2-devel
BuildRequires:	gnome-desktop-devel
BuildRequires:	gnome-menus-devel >= 3.1.5-2.fc16
BuildRequires:	gobject-introspection >= %{gobject_introspection_version}
BuildRequires:	json-glib-devel >= %{json_glib_version}
BuildRequires:	polkit-devel
BuildRequires:	telepathy-glib-devel
BuildRequires:	telepathy-logger-devel >= 0.2.6
BuildRequires:	udev-glib-devel
BuildRequires:	upower-devel
# for screencast recorder functionality
BuildRequires:	folks-devel
BuildRequires:	gstreamer-devel
BuildRequires:	gtk+3-devel
BuildRequires:	intltool
BuildRequires:	libcanberra-devel
BuildRequires:	libcroco-devel
# for barriers
BuildRequires:	xorg-lib-libXfixes-devel >= 5.0
# used in unused BigThemeImage
BuildRequires:	librsvg-devel
BuildRequires:	muffin-devel >= %{muffin_version}
BuildRequires:	pulseaudio-devel
%ifnarch s390 s390x
#BuildRequires:	gnome-bluetooth >= 2.91
#BuildRequires:	gnome-bluetooth-libs-devel >= 2.91
%endif
# Bootstrap requirements
BuildRequires:	gnome-common
BuildRequires:	gtk-doc
Requires:	gnome-menus >= 3.0.0-2
# wrapper script uses to restart old GNOME session if run --replace
# from the command line
Requires:	gobject-introspection >= %{gobject_introspection_version}
# needed for loading SVG's via gdk-pixbuf
Requires:	librsvg
# needed as it is now split from Clutter
Requires:	json-glib >= %{json_glib_version}
# might be still be needed.
Requires:	muffin >= %{muffin_version}
Requires:	polkit >= 0.100
Requires:	upower
# needed for session files
Requires:	gnome-session
# needed for schemas
Requires:	at-spi2-atk
Requires(pre):	GConf2
Requires(post):	GConf2
Requires(preun):	GConf2
# needed for on-screen keyboard
Requires:	caribou
# needed for settings
Requires:	python-dbus
Requires:	python-pygobject
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cinnamon is a Linux desktop which provides advanced innovative
features and a traditional user experience.

The desktop layout is similar to Gnome 2.

The underlying technology is forked from Gnome Shell.

The emphasis is put on making users feel at home and providing them
with an easy to use and comfortable desktop experience.

%prep
%setup -q -n linuxmint-Cinnamon-%{_internel_version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

# make changes for settings move to %{_datadir}
mv files%{_prefix}/lib/cinnamon-settings files%{_datadir}
sed -i -e 's@/usr/lib@/usr/share@g' files/usr/bin/cinnamon-settings \
	files%{_datadir}/cinnamon-settings/cinnamon-settings.py

# make changes for menu-editor move to %{_datadir}
mv files%{_prefix}/lib/cinnamon-menu-editor files%{_datadir}
rm -rf files%{_prefix}/lib
sed -i -e 's@/usr/lib@/usr/share@g' files/usr/bin/cinnamon-menu-editor \
	files%{_datadir}/cinnamon-menu-editor/Alacarte/MainWindow.py

# replace menu image
rm -f data/theme/menu.png
cp %{SOURCE3} data/theme/menu.png

# remove and replace the session files as they don't work with fedora (can't be bothered to patch it)
rm -f files%{_bindir}/gnome-session-cinnamon  \
	files%{_datadir}/xsessions/cinnamon.desktop \
	files%{_datadir}/gnome-session/sessions/cinnamon.session
cp %{SOURCE1} files%{_datadir}/xsessions/
cp %{SOURCE2} files%{_datadir}/gnome-session/sessions/

# files replaced with fedora files
rm -f files%{_datadir}/desktop-directories/cinnamon-menu-applications.directory \
	files%{_datadir}/desktop-directories/cinnamon-utility.directory \
	files%{_datadir}/desktop-directories/cinnamon-utility-accessibility.directory \
	files%{_datadir}/desktop-directories/cinnamon-development.directory \
	files%{_datadir}/desktop-directories/cinnamon-education.directory \
	files%{_datadir}/desktop-directories/cinnamon-game.directory \
	files%{_datadir}/desktop-directories/cinnamon-graphics.directory \
	files%{_datadir}/desktop-directories/cinnamon-network.directory \
	files%{_datadir}/desktop-directories/cinnamon-audio-video.directory \
	files%{_datadir}/desktop-directories/cinnamon-office.directory \
	files%{_datadir}/desktop-directories/cinnamon-system-tools.directory \
	files%{_datadir}/desktop-directories/cinnamon-other.directory
# adjust font size
sed -i -e 's,font-size: 9.5pt,font-size: 10pt,g' data/theme/cinnamon.css
sed -i -e 's,font-size: 9pt,font-size: 10pt,g' data/theme/cinnamon.css
sed -i -e 's,font-size: 8.5pt,font-size: 10pt,g' data/theme/cinnamon.css
sed -i -e 's,font-size: 8pt,font-size: 10pt,g' data/theme/cinnamon.css
sed -i -e 's,font-size: 7.5pt,font-size: 10pt,g' data/theme/cinnamon.css

rm -rf debian
rm configure

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
#CFLAGS="%{rpmcflags} -Wno-error=deprecated-declarations"
%configure \
	--with-ca-certificates=/etc/certs/ca-certificates.crt \
	--disable-static \
	--enable-compile-warnings=yes \

%{__make} V=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 \
	DESTDIR=$RPM_BUILD_ROOT

# Remove .la file
%{__rm} $RPM_BUILD_ROOT%{_libdir}/cinnamon/libcinnamon.la

# Remove firefox plugin
rm -rf $RPM_BUILD_ROOT%{_libdir}/mozilla

desktop-file-install \
	--add-category="Utility" \
	--remove-category="DesktopSettings" \
	--remove-key="Encoding" \
	--add-only-show-in="GNOME" \
	--delete-original \
	--dir=$RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_desktopdir}/cinnamon-settings.desktop

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/cinnamon.desktop

#%find_lang %{name}
touch %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install cinnamon.schemas

%preun
%gconf_schema_uninstall cinnamon.schemas

%postun
%glib_compile_schemas

%posttrans
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/cinnamon
%attr(755,root,root) %{_bindir}/cinnamon-settings
%attr(755,root,root) %{_bindir}/cinnamon-extension-tool
%{_sysconfdir}/gconf/schemas/cinnamon.schemas
%{_sysconfdir}/xdg/menus/cinnamon-applications.menu
%{_sysconfdir}/xdg/menus/cinnamon-settings.menu
%{_datadir}/desktop-directories/cinnamon-*.directory
%{_datadir}/glib-2.0/schemas/*.xml
%{_desktopdir}/cinnamon.desktop
%{_desktopdir}/cinnamon-settings.desktop
%{_datadir}/xsessions/cinnamon.desktop
%{_datadir}/gnome-session/sessions/cinnamon.session

%dir %{_datadir}/cinnamon
%{_datadir}/cinnamon/applets
%{_datadir}/cinnamon/js
%{_datadir}/cinnamon/search_providers
%{_datadir}/cinnamon/shaders
%{_datadir}/cinnamon/theme
%attr(755,root,root) %{_libdir}/cinnamon/libcinnamon.so

%dir %{_datadir}/cinnamon-settings
%{_datadir}/cinnamon-settings/cinnamon-settings.py
%{_datadir}/cinnamon-settings/cinnamon-settings.ui
%{_datadir}/cinnamon-settings/data

%{_datadir}/dbus-1/services/org.Cinnamon.CalendarServer.service
%{_datadir}/dbus-1/services/org.Cinnamon.HotplugSniffer.service

%dir %{_libdir}/cinnamon
%{_libdir}/cinnamon/Cinnamon-0.1.typelib
%{_libdir}/cinnamon/Gvc-1.0.typelib
%{_libdir}/cinnamon/St-1.0.typelib
%attr(755,root,root) %{_libdir}/cinnamon-calendar-server
%attr(755,root,root) %{_libdir}/cinnamon-perf-helper
%attr(755,root,root) %{_libdir}/cinnamon-hotplug-sniffer
%{_mandir}/man1/%{name}.1*

# i wonder why excluded?
#%exclude %{_bindir}/cinnamon-menu-editor
#%exclude %{_datadir}/cinnamon-menu-editor/
%attr(755,root,root) %{_bindir}/cinnamon-menu-editor
%dir %{_datadir}/cinnamon-menu-editor
%dir %{_datadir}/cinnamon-menu-editor/Alacarte
%{_datadir}/cinnamon-menu-editor/Alacarte/MainWindow.py
%{_datadir}/cinnamon-menu-editor/Alacarte/MenuEditor.py
%{_datadir}/cinnamon-menu-editor/Alacarte/__init__.py
%{_datadir}/cinnamon-menu-editor/Alacarte/config.py
%{_datadir}/cinnamon-menu-editor/Alacarte/util.py
%{_datadir}/cinnamon-menu-editor/cinnamon-menu-editor.ui
