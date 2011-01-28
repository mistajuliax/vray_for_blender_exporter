'''

 V-Ray/Blender

 http://vray.cgdo.ru

 Author: Andrey M. Izrantsev (aka bdancer)
 E-Mail: izrantsev@gmail.com

 This plugin is protected by the GNU General Public License v.2

 This program is free software: you can redioutibute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is dioutibuted in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.

 All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Group

'''


''' Python modules '''
import os

''' Blender modules '''
import bpy
from bpy.props import *

''' vb modules '''
from vb25.utils import *


class VRayLamp(bpy.types.IDPropertyGroup):
    pass

bpy.types.Lamp.vray= PointerProperty(
	name= "V-Ray Lamp Settings",
	type=  VRayLamp,
	description= "V-Ray lamp settings"
)


VRayLamp.enabled= BoolProperty(
	name= "Enabled",
	description= "Turns the light on and off",
	default= True
)

VRayLamp.units= EnumProperty(
	name= "Intensity units",
	description= "Units for the intensity.",
	items= (
		('DEFAULT',"Default",""),
		('LUMENS',"Lumens",""),
		('LUMM',"Lm/m/m/sr",""),
		('WATTSM',"Watts",""),
		('WATM',"W/m/m/sr","")
	),
	default= 'DEFAULT'
)

VRayLamp.use_include_exclude= BoolProperty(
	name= "Use Include / Exclude",
	description= "Use Include / Exclude.",
	default= False
)

VRayLamp.include_exclude= EnumProperty(
	name= "Type",
	description= "Include or exclude object from lightning.",
	items= (
		('EXCLUDE',"Exclude",""),
		('INCLUDE',"Include",""),
	),
	default= 'EXCLUDE'
)

VRayLamp.include_objects= StringProperty(
	name= "Include objects",
	description= "Include objects: name{;name;etc}."
)

VRayLamp.include_groups= StringProperty(
	name= "Include groups",
	description= "Include groups: name{;name;etc}."
)

VRayLamp.fallsize= FloatProperty(
	name= "Beam radius",
	description= "Beam radius, 0.0 if the light has no beam radius.",
	min= 0.0,
	max= 10000.0,
	soft_min= 0.0,
	soft_max= 100.0,
	precision= 3,
	default= 1.0
)

VRayLamp.direct_type= EnumProperty(
	name= "Direct type",
	description= "Direct light type.",
	items= (
		('DIRECT', "Direct", ""),
		('SUN',    "Sun",    ""),
	),
	default= 'DIRECT'
)

VRayLamp.spot_type= EnumProperty(
	name= "Spot type",
	description= "Spot light subtype.",
	items= (
		('SPOT', "Spot", ""),
		('IES',  "IES",  ""),
	),
	default= 'SPOT'
)

VRayLamp.shadows= BoolProperty(
	name= "Shadows",
	description= "Produce shadows.",
	default= True
)

VRayLamp.affectDiffuse= BoolProperty(
	name= "Affect diffuse",
	description= "Produces diffuse lighting.",
	default= True
)

VRayLamp.affectSpecular= BoolProperty(
	name= "Affect specular",
	description= "Produces specular hilights.",
	default= True
)

VRayLamp.affectReflections= BoolProperty(
	name= "Affect reflections",
	description= "Appear in reflections.",
	default= False
)

VRayLamp.shadowColor= FloatVectorProperty(
	name= "Shadow color",
	description= "The shadow color. Anything but black is not physically accurate.",
	subtype= 'COLOR',
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	default= (0.0,0.0,0.0)
)

VRayLamp.shadowBias= FloatProperty(
	name= "Shadow bias",
	description= "Shadow offset from the surface. Helps to prevent polygonal shadow artifacts on low-poly surfaces.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 0.0
)

VRayLamp.shadowSubdivs= IntProperty(
	name= "Shadow subdivs",
	description= "This value controls the number of samples V-Ray takes to compute area shadows. Lower values mean more noisy results, but will render faster. Higher values produce smoother results but take more time.",
	min= 0,
	max= 256,
	default= 8
)

VRayLamp.shadowRadius= FloatProperty(
	name= "Shadow radius",
	description= "Shadow radius.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 0
)

VRayLamp.decay= FloatProperty(
	name= "Decay",
	description= "Light decay.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 2
)

VRayLamp.cutoffThreshold= FloatProperty(
	name= "Cut-off threshold",
	description= "Light cut-off threshold (speed optimization). If the light intensity for a point is below this threshold, the light will not be computed..",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 0.1,
	precision= 3,
	default= 0.001
)

VRayLamp.intensity= FloatProperty(
	name= "Intensity",
	description= "Light intensity.",
	min= 0.0,
	max= 10000000.0,
	soft_min= 0.0,
	soft_max= 100.0,
	precision= 2,
	default= 30
)

VRayLamp.subdivs= IntProperty(
	name= "Subdivs",
	description= "This controls the number of samples for the area shadow. More subdivs produce area shadows with better quality but render slower.",
	min= 0,
	max= 256,
	default= 8
)

VRayLamp.storeWithIrradianceMap= BoolProperty(
	name= "Store with irradiance map",
	description= "When this option is on and GI calculation is set to Irradiance map V-Ray will calculate the effects of the VRayLightRect and store them in the irradiance map.",
	default= False
)

VRayLamp.invisible= BoolProperty(
	name= "Invisible",
	description= "This setting controls whether the shape of the light source is visible in the render result.",
	default= False
)

VRayLamp.noDecay= BoolProperty(
	name= "No decay",
	description= "When this option is on the intensity will not decay with distance.",
	default= False
)

VRayLamp.doubleSided= BoolProperty(
	name= "Double-sided",
	description= "This option controls whether light is beamed from both sides of the plane.",
	default= False
)

VRayLamp.lightPortal= EnumProperty(
	name= "Light portal mode",
	description= "Specifies if the light is a portal light.",
	items= (
		('NORMAL',"Normal light",""),
		('PORTAL',"Portal",""),
		('SPORTAL',"Simple portal","")
	),
	default= 'NORMAL'
)

VRayLamp.radius= FloatProperty(
	name= "Radius",
	description= "Sphere light radius.",
	min= 0.0,
	max= 10000.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 0.0
)

VRayLamp.sphere_segments= IntProperty(
	name= "Sphere segments",
	description= "Controls the quality of the light object when it is visible either directly or in reflections.",
	min= 0,
	max= 100,
	default= 20
)

VRayLamp.bumped_below_surface_check= BoolProperty(
	name= "Bumped below surface check",
	description= "If the bumped normal should be used to check if the light dir is below the surface.",
	default= False
)

VRayLamp.nsamples= IntProperty(
	name= "Motion blur samples",
	description= "Motion blur samples.",
	min= 0,
	max= 10,
	default= 0
)

VRayLamp.diffuse_contribution= FloatProperty(
	name= "Diffuse contribution",
	description= "A multiplier for the effect of the light on the diffuse.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

VRayLamp.specular_contribution= FloatProperty(
	name= "Specular contribution",
	description= "A multiplier for the effect of the light on the specular.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

VRayLamp.areaSpeculars= BoolProperty(
	name= "Area speculars",
	description= "When this parameter is enabled, the specular highlights will be computed with the real light shape as defined in the .ies files.",
	default= False
)

VRayLamp.ignoreLightNormals= BoolProperty(
	name= "Ignore light normals",
	description= "When this option is off, more light is emitted in the direction of the source surface normal.",
	default= True
)

VRayLamp.tex_resolution= IntProperty(
	name= "Tex resolution",
	description= "Specifies the resolution at which the texture is sampled when the \"Tex Adaptive\" option is checked.",
	min= 0,
	max= 10,
	default= 512
)

VRayLamp.tex_adaptive= BoolProperty(
	name= "Tex adaptive",
	description= "When this option is checked V-Ray will use impotance sampling on the texture in order to produce better shadows.",
	default= True
)

VRayLamp.causticSubdivs= IntProperty(
	name= "Caustic subdivs",
	description= "Caustic subdivisions. Lower values mean more noisy results, but will render faster. Higher values produce smoother results but take more time.",
	min= 1,
	max= 100000,
	default= 1000
)

VRayLamp.causticMult= FloatProperty(
	name= "Caustics multiplier",
	description= "Caustics multiplier.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 1
)

VRayLamp.ies_file= StringProperty(
	name= "IES file",
	subtype= 'FILE_PATH',
	description= "IES file."
)

VRayLamp.soft_shadows= BoolProperty(
	name= "Soft shadows",
	description= "Use the shape of the light as described in the IES profile.",
	default= True
)

VRayLamp.turbidity= FloatProperty(
	name= "Turbidity",
	description= "This parameter determines the amount of dust in the air and affects the color of the sun and sky.",
	min= 2.0,
	max= 100.0,
	soft_min= 2.0,
	soft_max= 6.0,
	precision= 3,
	default= 3.0
)

VRayLamp.intensity_multiplier= FloatProperty(
	name= "Intensity multiplier",
	description= "This is an intensity multiplier for the Sun.",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 2,
	default= 1.0
)

VRayLamp.ozone= FloatProperty(
	name= "Ozone",
	description= "This parameter affects the color of the sun light.",
	min= 0.0,
	max= 1.0,
	soft_min= 0.0,
	soft_max= 1.0,
	precision= 3,
	default= 0.35
)

VRayLamp.water_vapour= FloatProperty(
	name= "Water vapour",
	description= "Water vapour.",
	min= 0.0,
	max= 10.0,
	soft_min= 0.0,
	soft_max= 2.0,
	precision= 3,
	default= 2
)

VRayLamp.size_multiplier= FloatProperty(
	name= "Size",
	description= "This parameter controls the visible size of the sun.",
	min= 0.0,
	max= 100.0,
	soft_min= 0.0,
	soft_max= 10.0,
	precision= 3,
	default= 1
)

VRayLamp.invisible= BoolProperty(
	name= "Invisible",
	description= "When on, this option makes the sun invisible, both to the camera and to reflections.",
	default= False
)

VRayLamp.horiz_illum= FloatProperty(
	name= "Horiz illumination",
	description= "Specifies the intensity (in lx) of the illumination on horizontal surfaces coming from the Sky.",
	min= 0.0,
	max= 100000.0,
	soft_min= 0.0,
	soft_max= 100000.0,
	precision= 0,
	default= 25000
)

VRayLamp.sky_model= EnumProperty(
	name= "Sky model",
	description= "Allows you to specify the procedural model that will be used to generate the VRaySky texture.",
	items= (
		('CIEOVER',"CIE Overcast",""),
		('CIECLEAR',"CIE Clear",""),
		('PREETH',"Preetham et al.","")
	),
	default= 'PREETH'
)



'''
	GUI
'''
narrowui= 200


def base_poll(cls, context):
	rd= context.scene.render
	return (context.lamp) and (rd.engine in cls.COMPAT_ENGINES)


class VRayDataPanel():
	bl_space_type  = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context     = 'data'


class DATA_PT_context_lamp(VRayDataPanel, bpy.types.Panel):
	bl_label = ""
	bl_options = {'HIDE_HEADER'}

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		layout= self.layout

		ob= context.object
		lamp= context.lamp
		space= context.space_data
		wide_ui= context.region.width > narrowui

		if wide_ui:
			split= layout.split(percentage=0.65)
			if ob:
				split.template_ID(ob, 'data')
				split.separator()
			elif lamp:
				split.template_ID(space, 'pin_id')
				split.separator()
		else:
			if ob:
				layout.template_ID(ob, 'data')
			elif lamp:
				layout.template_ID(space, 'pin_id')

		if wide_ui:
			layout.prop(lamp, 'type', expand=True)
		else:
			layout.prop(lamp, 'type')


class DATA_PT_vray_light(VRayDataPanel, bpy.types.Panel):
	bl_label       = "Lamp"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		wide_ui= context.region.width > narrowui
		layout= self.layout

		ob= context.object
		lamp= context.lamp
		vl= lamp.vray

		split= layout.split()
		col= split.column()
		col.prop(vl,'enabled', text="On")

		split= layout.split()
		col= split.column()
		if not ((lamp.type == 'SUN' and vl.direct_type == 'SUN') or (lamp.type == 'AREA' and vl.lightPortal != 'NORMAL')):
			col.prop(lamp,'color', text="")
		if lamp.type == 'AREA':
			col.prop(vl,'lightPortal', text="Mode")
		if not ((lamp.type == 'SUN' and vl.direct_type == 'SUN') or (lamp.type == 'AREA' and vl.lightPortal != 'NORMAL')):
			col.prop(vl,'units', text="Units")
		if not ((lamp.type == 'SUN' and vl.direct_type == 'SUN') or (lamp.type == 'AREA' and vl.lightPortal != 'NORMAL')):
			col.prop(vl,'intensity', text="Intensity")
		col.prop(vl,'subdivs')
		col.prop(vl,'causticSubdivs', text="Caustics")
		
		if wide_ui:
			col= split.column()
		col.prop(vl,'invisible')
		col.prop(vl,'affectDiffuse')
		col.prop(vl,'affectSpecular')
		col.prop(vl,'affectReflections')
		col.prop(vl,'noDecay')

		if(lamp.type == 'AREA'):
			col.prop(vl,'doubleSided')

		if((lamp.type == 'AREA') or (lamp.type == 'POINT' and vl.radius > 0)):
			col.prop(vl,'storeWithIrradianceMap')


class DATA_PT_vray_light_shape(VRayDataPanel, bpy.types.Panel):
	bl_label       = "Shape"

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		lamp= context.lamp
		return (lamp and base_poll(__class__, context))

	def draw(self, context):
		wide_ui= context.region.width > narrowui
		layout= self.layout

		ob= context.object
		lamp= context.lamp
		vl= lamp.vray

		if lamp.type == 'AREA':
			layout.prop(lamp,'shape', expand=True)
			#  use_rect_tex: bool = false
			#  tex_resolution: integer = 512
			#  tex_adaptive: float = 1

		elif lamp.type == 'SUN':
			layout.prop(vl,'direct_type', expand=True)

		elif lamp.type == 'SPOT':
			layout.prop(vl,'spot_type', expand=True)

		split= layout.split()
		col= split.column()
		if lamp.type == 'AREA':
			if lamp.shape == 'SQUARE':
				col.prop(lamp,'size')
			else:
				col.prop(lamp,'size', text="Size X")
				if wide_ui:
					col= split.column()
				col.prop(lamp,'size_y')

		elif lamp.type == 'POINT':
			col.prop(vl,'radius')
			if vl.radius > 0:
				col.prop(vl,'sphere_segments')

		elif lamp.type == 'SUN':
			if vl.direct_type == 'DIRECT':
				col.prop(vl,'fallsize')
			else:
				split= layout.split()
				col= split.column()
				col.prop(vl,'sky_model')
				
				split= layout.split()
				col= split.column()
				col.prop(vl,'turbidity')
				col.prop(vl,'ozone')
				col.prop(vl,'intensity_multiplier', text= "Intensity")
				col.prop(vl,'size_multiplier', text= "Size")
				if wide_ui:
					col= split.column()
				col.prop(vl,'invisible')
				col.prop(vl,'horiz_illum')
				col.prop(vl,'water_vapour')

				split= layout.split()
				col= split.column()
				col.operator('vray.add_sky', icon='TEXTURE')

		elif lamp.type == 'SPOT':
			if vl.spot_type == 'SPOT':
				col.prop(lamp,'distance')
				if wide_ui:
					col= split.column()
				col.prop(lamp,'spot_size', text="Size")
				col.prop(lamp,'spot_blend', text="Blend")
			else:
				col.prop(vl,'ies_file', text="File")
				col.prop(vl,'soft_shadows')

		elif(lamp.type == 'HEMI'):
			#  objectID: integer = 0
			#  use_dome_tex: bool = false
			#  tex_resolution: integer = 512
			#  dome_targetRadius: float = 100
			#  dome_emitRadius: float = 150
			#  dome_spherical: bool = false
			#  tex_adaptive: float = 1
			#  dome_rayDistance: float = 100000
			#  dome_rayDistanceMode: integer = 0

			pass

		else:
			pass


class DATA_PT_vray_light_shadows(VRayDataPanel, bpy.types.Panel):
	bl_label   = "Shadows"
	bl_options = {'DEFAULT_CLOSED'}

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw_header(self, context):
		vl= context.lamp.vray
		self.layout.prop(vl,'shadows', text="")

	def draw(self, context):
		wide_ui= context.region.width > narrowui
		layout= self.layout

		ob= context.object
		lamp= context.lamp
		vl= lamp.vray

		layout.active = vl.shadows

		split= layout.split()
		col= split.column()
		col.prop(vl,'shadowColor', text="")
		if wide_ui:
			col= split.column()
		col.prop(vl,'shadowBias', text="Bias")
		if(lamp.type in ('SPOT','POINT','SUN')):
			col.prop(vl,'shadowRadius', text="Radius")

		split= layout.split()
		col= split.column()
		if(lamp.type == 'AREA'):
			pass
		elif(lamp.type == 'POINT'):
			pass
		elif(lamp.type == 'SUN'):
			pass
		elif(lamp.type == 'SPOT'):
			pass
		elif(lamp.type == 'HEMI'):
			pass
		else:
			pass


class DATA_PT_vray_light_advanced(VRayDataPanel, bpy.types.Panel):
	bl_label   = "Advanced"
	bl_options = {'DEFAULT_CLOSED'}

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw(self, context):
		wide_ui= context.region.width > narrowui
		layout= self.layout

		ob= context.object
		lamp= context.lamp
		vl= lamp.vray

		split= layout.split()
		col= split.column()
		col.prop(vl,'diffuse_contribution', text="Diffuse cont.")
		col.prop(vl,'specular_contribution', text="Specular cont.")
		col.prop(vl,'cutoffThreshold', text="Cut-off")
		
		if wide_ui:
			col= split.column()
		col.prop(vl,'nsamples')
		col.prop(vl,'bumped_below_surface_check', text="Bumped surface check")
		col.prop(vl,'ignoreLightNormals')
		col.prop(vl,'areaSpeculars')
		
		if(lamp.type == 'AREA'):
			pass
		elif(lamp.type == 'POINT'):
			pass
		elif(lamp.type == 'SUN'):
			pass
		elif(lamp.type == 'SPOT'):
			pass
		elif(lamp.type == 'HEMI'):
			pass
		else:
			pass


class VRAY_LAMP_include_exclude(VRayDataPanel, bpy.types.Panel):
	bl_label   = "Include / Exclude"
	bl_options = {'DEFAULT_CLOSED'}

	COMPAT_ENGINES= {'VRAY_RENDER','VRAY_RENDER_PREVIEW'}

	@classmethod
	def poll(cls, context):
		return base_poll(__class__, context)

	def draw_header(self, context):
		VRayLamp= context.lamp.vray
		self.layout.prop(VRayLamp, 'use_include_exclude', text="")

	def draw(self, context):
		wide_ui= context.region.width > narrowui
		layout= self.layout

		VRayLamp= context.lamp.vray

		layout.active= VRayLamp.use_include_exclude

		split= layout.split()
		col= split.column()
		col.prop(VRayLamp, 'include_exclude', text="")
		col.prop_search(VRayLamp, 'include_objects',  context.scene, 'objects', text="Objects")
		col.prop_search(VRayLamp, 'include_groups',   bpy.data,      'groups',  text="Groups")


class VRAY_OT_add_sky(bpy.types.Operator):
	bl_idname = "vray.add_sky"
	bl_label  = "Add Sky texture"
	bl_description = "Add Sky texture to the background."

	def invoke(self, context, event):
		sce= context.scene

		try:
			tex= bpy.data.textures.new('VRaySky', type= 'VRAY')
			tex.vray.type= 'TEXSKY'

			for i,slot in enumerate(sce.world.texture_slots):
				if not slot:
					new_slot= sce.world.texture_slots.create(i)
					new_slot.texture= tex
					break
		except:
			print("V-Ray/Blender: Sky texture only availble in \"%s\"!" % color("Special build",'green'))
		
		return{'FINISHED'}
