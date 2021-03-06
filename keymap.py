#
# V-Ray For Blender
#
# http://chaosgroup.com
#
# Author: Andrei Izrantcev
# E-Mail: andrei.izrantcev@chaosgroup.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.
#

import bpy

addon_keymaps = []


def register():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')
        kmi = km.keymap_items.new("vray.show_node_image", 'LEFTMOUSE', 'DOUBLE_CLICK')

        kmi = km.keymap_items.new('wm.call_menu_pie', 'Q', 'PRESS')
        kmi.properties.name = "VRAY_MT_ShowNtreePie"

        kmi = km.keymap_items.new("vray.ntree_node_mute", 'M', 'PRESS')

        kmi = km.keymap_items.new('wm.call_menu_pie', 'Q', 'PRESS', shift=True)
        kmi.properties.name = "VRAY_MT_AddNtreePie"

        addon_keymaps.append(km)

        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu', 'F3', 'PRESS')
        kmi.properties.name = "VRAY_MT_CameraActive"

        addon_keymaps.append(km)


def unregister():
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)

    addon_keymaps.clear()
