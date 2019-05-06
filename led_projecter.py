import bpy
import bmesh
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
from mathutils import Vector, Quaternion, Euler, Matrix
import math
from pprint import pprint
import json

def intersect_to_empty(location, normal, size, name, draw_type='SINGLE_ARROW'):
    o = bpy.data.objects.new(name, None)
    bpy.context.scene.objects.link(o)

    quat = normal.to_track_quat('Z', 'Y')
    o.rotation_mode = 'QUATERNION'
    if draw_type == "CIRCLE":
        eul = Euler((math.radians(90.0), 0.0, 0.0), 'XYZ')
        o.rotation_quaternion = (0, 0, 0, 1)
        o.rotation_quaternion.rotate(eul)
        o.rotation_quaternion.rotate(quat)
        #o.show_x_ray = True
        # o.empty_draw_type = "IMAGE"
        o.empty_draw_type = "CIRCLE"
        # img = bpy.data.images.load("//../1024px-Location_dot_red.svg.png")
        # o.data = img
        # o.empty_image_offset[0] = -0.5
        # o.empty_image_offset[1] = -0.5
        # o.color[3] = .2
    else:
        o.empty_draw_type = draw_type
        o.rotation_quaternion = quat

    o.layers[1] = True
    for i in range(20):
        o.layers[i] = (i == 1)

    #o.hide_select = True
    o.location = location

    o.empty_draw_size = size


def point_to_uv(obj, triangle_index, point, map_name, texture_size):
    uv_map = obj.data.uv_layers[map_name]

    vertices_indices = obj.data.polygons[triangle_index].vertices

    uv_map_indices = obj.data.polygons[triangle_index].loop_indices

    p1, p2, p3 = [obj.data.vertices[vertices_indices[i]].co for i in range(3)]

    uv1, uv2, uv3 = [uv_map.data[uv_map_indices[i]].uv for i in range(3)]
    uv_point = barycentric_transform(point, p1, p2, p3, uv1.to_3d(), uv2.to_3d(), uv3.to_3d())

    return uv_point.to_2d() * texture_size


def ray_cast(bvh, point, normal):
    intersection_point, intersection_normal, intersection_index, distance = bvh.ray_cast(point, normal, 100)

    if distance is None:
        raise RuntimeError
    else:
        return intersection_point, intersection_normal, intersection_index, distance


def euler_to_vec(rotation):
    v = Vector((0.0, 0.0, 1.0))
    v.rotate(rotation)
    return v


def obj_to_bvh(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bvh = BVHTree.FromBMesh(bm)
    return bvh


def first_part(empty, inner_obj, outer_obj, draw=True):
    inner_BVH = obj_to_bvh(inner_obj)
    outer_BVH = obj_to_bvh(outer_obj)

    face_id = inner_obj.closest_point_on_mesh(empty.location)[-1]

    polygon = inner_obj.data.polygons[face_id]
    
    o_location, o_normal, o_index, o_distance = ray_cast(outer_BVH, empty.location, polygon.normal)
    
    o_distance = min([o_distance,5])

    if draw:
        intersect_to_empty(empty.location, polygon.normal, o_distance, "%s_gen_ray" % empty.name)
        intersect_to_empty(o_location, o_normal, o_distance, "%s_gen_proj" % empty.name, 'CIRCLE')

    return o_index, o_location, o_distance

def second_part(outer_obj, o_index, o_location, map_name, texture_size=1):

    texture_point = point_to_uv(outer_obj, o_index, o_location, map_name, texture_size)

    return texture_point


def delete_all_gen():
    deletable = [obj for obj in bpy.data.objects if "gen" in obj.name]
    [bpy.data.objects.remove(obj, True) for obj in deletable]


delete_all_gen()

#raise RuntumeException

inner = bpy.data.objects['inner']
outer = bpy.data.objects['outer']

empties = [obj for obj in bpy.data.objects if obj.data is None]

dat = {}

maps = outer.data.uv_layers.keys()

for empty in empties:
    
    dat[empty.name] = {"maps":{}}
    dat[empty.name]["position_actual"] = list(empty.location)    
    
    try:
        o_index, position, spread = first_part(empty, inner, outer)        
        dat[empty.name]["position"] = list(position)
        dat[empty.name]["spread"] = spread
        
        for map_name in maps:
            uv_point = second_part(outer, o_index, position, map_name)
            dat[empty.name]["maps"][map_name] = [u%1 for u in uv_point]
    except:
        print("cannot calculate values for %s" % empty.name)


with open('C:\\Users\\Sam\\Desktop\\highbeam_test\\led_placement.json', 'w') as outfile:
    json.dump(dat, outfile)        
pprint(dat)