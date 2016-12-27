Name: clipit
Version: 1.4.2
Release: alt20

Summary: Lightweight GTK+ Clipboard Manager

License: GPLv3
Group: Graphical desktop/Other
Url: https://github.com/CristianHenzel/ClipIt

Packager: Sample Maintainer <samplemaintainer@altlinux.org>
BuildPreReq: libgtk+2-devel intltool
Source: %name-%version.tar

%description
ClipIt is a lightweight GTK+ clipboard manager


%prep
%setup

%build
mv configure.in configure.ac

# AM_PATH_GTK_2_0 is unrecognized, remove it
sed -E -i.bak "s/^AM_PATH_GTK_2_0.*\$//g" configure.ac
rm configure.ac.bak -fv

# m4/Makefile.am/in disappears after autoreconf or autogen.sh, we remove it
sed -E -i.bak "s/m4\\/Makefile//g" configure.ac
rm configure.ac.bak -fv


# next is commented out
cat <<EOF > /dev/null
find /usr -name glibconfig.h -exec bash -c "dirname {} > glibconfig.h.dirname" \;
for i in `cat glibconfig.h.dirname` ; do
  i_excapedforsed_and_1st_bash=`echo $i | sed -e "s/\\//\\\\\\\\\\\\\\\\\\//g"`
  find -name Makefile.am -exec bash -c "if grep AM_CFLAGS {} ; then sed -E -i.bak \"s/^(\\\\s*AM_CFLAGS.*)\\\$/\\\\1 -I${i_excapedforsed_and_1st_bash}/g\" {} ; rm {}.bak -fv ; else echo -en \"\\\\nAM_CFLAGS = -I/usr/include/glib/2.0\\\\n\" >> {}  ; fi" \;
done
find -name Makefile.am -exec bash -c "if grep AM_CFLAGS {} ; then sed -E -i.bak \"s/^(\\\\s*AM_CFLAGS.*)\\\$/\\\\1 -I\\\\/usr\\\\/include\\\\/glib-2.0/g\" {} ; rm {}.bak -fv ; else echo -en \"\\\\nAM_CFLAGS = -I/usr/include/glib-2.0\\\\n\" >> {}  ; fi" \;
find -name Makefile.am -exec bash -c "if grep AM_CFLAGS {} ; then sed -E -i.bak \"s/^(\\\\s*AM_CFLAGS.*)\\\$/\\\\1 -I\\\\/usr\\\\/include\\\\/gtk-2.0/g\" {} ; rm {}.bak -fv ; else echo -en \"\\\\nAM_CFLAGS = -I/usr/include/gtk-2.0\\\\n\" >> {}  ; fi" \;
find -name Makefile.am -exec bash -c "if grep AM_CFLAGS {} ; then sed -E -i.bak \"s/^(\\\\s*AM_CFLAGS.*)\\\$/\\\\1 -I\\\\/usr\\\\/include\\\\/pango-1.0/g\" {} ; rm {}.bak -fv ; else echo -en \"\\\\nAM_CFLAGS = -I/usr/include/pango-1.0\\\\n\" >> {}  ; fi" \;
find -name Makefile.am -exec bash -c "if grep AM_CFLAGS {} ; then sed -E -i.bak \"s/^(\\\\s*AM_CFLAGS.*)\\\$/\\\\1 -I\\\\/usr\\\\/include\\\\/cairo/g\" {} ; rm {}.bak -fv ; else echo -en \"\\\\nAM_CFLAGS = -I/usr/include/cairo\\\\n\" >> {}  ; fi" \;
find -name Makefile.am -exec bash -c "if grep AM_CFLAGS {} ; then sed -E -i.bak \"s/^(\\\\s*AM_CFLAGS.*)\\\$/\\\\1 -I\\\\/usr\\\\/include\\\\/gdk-pixbuf-2.0/g\" {} ; rm {}.bak -fv ; else echo -en \"\\\\nAM_CFLAGS = -I/usr/include/gdk-pixbuf-2.0\\\\n\" >> {}  ; fi" \;
find -name Makefile.am -exec bash -c "if grep AM_CFLAGS {} ; then sed -E -i.bak \"s/^(\\\\s*AM_CFLAGS.*)\\\$/\\\\1 -I\\\\/usr\\\\/include\\\\/atk-1.0/g\" {} ; rm {}.bak -fv ; else echo -en \"\\\\nAM_CFLAGS = -I/usr/include/atk-1.0\\\\n\" >> {}  ; fi" \;
EOF



# gdk_display - undefined variable. Replace with a func, guess
sed -E -i.bak "s/gdk_display/gdk_display_get_default()/g" src/keybinder.c
rm src/keybinder.c.bak -fv


# add #include <gtk/gtk.h>
cp src/keybinder.c src/keybinder.c.orig
echo -en "#include <gtk/gtk.h>\\n" > src/keybinder.c
cat src/keybinder.c.orig >> src/keybinder.c
rm src/keybinder.c.orig -fv



# replace
sed -E -i.bak "s/GtkObject/GObject/g" src/preferences.c
rm src/preferences.c.bak -fv

# deprecated; noncompiled with gtk+3, when used gtk+-3; replace with 0
sed -E -i.bak "s/GTK_DIALOG_NO_SEPARATOR/0/g" src/preferences.c
rm src/preferences.c.bak -fv

# take cflags and put into Makefile.am files. Into AM_CFLAGS. Create new (echo) AM_CFLAGS, or add (sed) if exists
new_cflags="`pkg-config --cflags gtk+-2.0`"
escaped_cflags=`echo $new_cflags | sed -e "s/\\//\\\\\\\\\\\\\\\\\\//g"`
find -name Makefile.am -exec bash -c "if grep AM_CFLAGS {} ; then sed -E -i.bak \"s/^(\\\\s*AM_CFLAGS.*)\\\$/\\\\1 ${escaped_cflags}/g\" {} ; rm {}.bak -fv ; else echo -en \"\\\\nAM_CFLAGS = ${new_cflags}\\\\n\" >> {}  ; fi" \;


# same with -l flags
new_flags="`pkg-config --libs gtk+-2.0`"
escaped_flags=`echo $new_flags | sed -e "s/\\//\\\\\\\\\\\\\\\\\\//g"`
find -name Makefile.am -exec bash -c "if grep LDADD  {} ; then sed -E -i.bak \"s/^(\\\\s*LDADD.*)\\\$/\\\\1 ${escaped_flags}/g\" {} ; rm {}.bak -fv ; else echo -en \"\\\\nLDADD = ${new_flags}\\\\n\" >> {}  ; fi" \;


./autogen.sh
%configure
%make_build

%install
%makeinstall_std




%find_lang %name


%files -f %name.lang
%doc AUTHORS ChangeLog NEWS COPYING INSTALL README
%_desktopdir/%name.desktop
%_bindir/*
/usr/share/man/man1/*
/usr/share/icons/hicolor/scalable/apps/*
/etc/xdg/autostart/*

%changelog
* Sat Dec 03 2016 Sample Maintainer <samplemaintainer@altlinux.org> 1.4.2-alt20
- initial build

