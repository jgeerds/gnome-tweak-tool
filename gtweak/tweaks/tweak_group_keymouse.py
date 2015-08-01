# This file is part of gnome-tweak-tool.
#
# Copyright (c) 2011 John Stowers
#
# gnome-tweak-tool is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gnome-tweak-tool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gnome-tweak-tool.  If not, see <http://www.gnu.org/licenses/>.

import os.path

from gi.repository import GLib

import gtweak
from gtweak.utils import XSettingsOverrides, walk_directories, make_combo_list_with_default, get_resource_dirs
from gtweak.widgets import ListBoxTweakGroup, GSettingsComboTweak, GSettingsSwitchTweak, GetterSetterSwitchTweak, Title, GSettingsComboEnumTweak

class PrimaryPasteTweak(GetterSetterSwitchTweak):
    def __init__(self, **options):
        self._xsettings = XSettingsOverrides()
        GetterSetterSwitchTweak.__init__(self, _("Middle-click Paste"), **options)

    def get_active(self):
        return self._xsettings.get_enable_primary_paste()

    def set_active(self, v):
        self._xsettings.set_enable_primary_paste(v)

class KeyThemeSwitcher(GSettingsComboTweak):
    def __init__(self, **options):
        GSettingsComboTweak.__init__(self,
			# Translators: This setting refers to a set of pre-defined key bindings
			_("Key theme"),
            "org.gnome.desktop.interface",
            "gtk-key-theme",
            make_combo_list_with_default(
                self._get_valid_key_themes(),
                "Default",
                default_text=_("<i>Default</i>")),
            **options)

    def _get_valid_key_themes(self):
        valid = walk_directories(get_resource_dirs("themes"), lambda d:
                    os.path.isfile(os.path.join(d, "gtk-3.0", "gtk-keys.css")) and \
                    os.path.isfile(os.path.join(d, "gtk-2.0-key", "gtkrc")))
        return valid

TWEAK_GROUPS = [
    ListBoxTweakGroup(_("Keyboard and Mouse"),
        GSettingsSwitchTweak(_("Show All Input Sources"),
                              "org.gnome.desktop.input-sources",
                              "show-all-sources",
                              logout_required=True,),
        KeyThemeSwitcher(),
        GSettingsComboTweak(_("Switch between overview and desktop"),
                              "org.gnome.mutter",
                              "overlay-key",
                              [("Super_L", _("Left super")), ("Super_R", _("Right super"))]),
              
        Title(_("Mouse"), ""),
        GSettingsSwitchTweak(_("Show location of pointer"),
                             "org.gnome.settings-daemon.peripherals.mouse", 
                             "locate-pointer", 
                              schema_filename="org.gnome.settings-daemon.peripherals.gschema.xml"),
        PrimaryPasteTweak(),

        Title(_("Touchpad"), ""),
        GSettingsComboEnumTweak(_("Click method"),
                                "org.gnome.desktop.peripherals.touchpad",
                                "click-method",
                                schema_filename="org.gnome.desktop.peripherals.gschema.xml"),
        ),
]
