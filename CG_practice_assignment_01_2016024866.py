#!/usr/bin/env python3
# -*- coding: utf-8 -*
# sample_python aims to allow seamless integration with lua.
# see examples below

import os
import sys
import pdb  # use pdb.set_trace() for debugging
import code # or use code.interact(local=dict(globals(), **locals()))  for debugging.
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
class Color:
    def __init__(self, R, G, B):
        self.color = np.array([R, G, B]).astype(np.float)

    def gammaCorrect(self, gamma):
        inverseGamma = 1.0 / gamma;
        self.color = np.power(self.color, inverseGamma)

    def toUINT8(self):
        return (np.clip(self.color, 0, 1) * 255).astype(np.uint8)


class Shader:
    def __init__(self, type):
        self.type = type


class ShaderPhong(Shader):
    def __init__(self, diffuse, specular, exponent):
        self.diffuse = diffuse
        self.specular = specular
        self.exponent = exponent


class ShaderLambertian(Shader):
    def __init__(self, diffuse):
        self.diffuse = diffuse


class Sphere:
    def __init__(self, center, radius, shader):
        self.center = center
        self.radius = radius
        self.shader = shader


class Box:
    def __init__(self, minPt, maxPt, shader, normals):
        self.minPt = minPt
        self.maxPt = maxPt
        self.shader = shader
        self.normal = normals


class View:
    def __init__(self, viewPoint, viewDir, viewUp, viewProjNormal, viewWidth, viewHeight, projDistance, intensity):
        self.viewPoint = viewPoint
        self.viewDir = viewDir
        self.viewUp = viewUp
        self.viewProjNormal = viewProjNormal
        self.viewWidth = viewWidth
        self.viewHeight = viewHeight
        self.projDistance = projDistance
        self.intensity = intensity


class Light:
    def __init__(self, position, intensity):
        self.position = position
        self.intensity = intensity

def ray_trace(list,ray,viewpoint):
    min_d=sys.maxsize
    idx=-1 # find nearest obj
    cnt=0 #check hit objects
    for i in list:
        if i.__class__.__name__ == "Sphere":
            sphere_to_ray=viewpoint -i.center
            a=np.dot(ray,ray)
            b=np.dot(ray,sphere_to_ray)
            c=np.dot(sphere_to_ray,sphere_to_ray)-i.radius*i.radius
            disc=b*b-a*c
            # pdb.set_trace()
            #check later does if case really needed?
            if disc  >=0:
                if -b - np.sqrt(disc) >= 0:
                    distance= (-b - np.sqrt(disc))/a
                    if min_d>= distance:
                        min_d= distance
                        idx=cnt
            # pdb.set_trace()
        elif i.__class__.__name__ == 'Box':
            opt= 1
            # case x
            txmin = (i.minPt[0]-viewpoint[0])/ray[0]
            txmax = (i.maxPt[0]-viewpoint[0])/ray[0]
            # case y
            tymin = (i.minPt[1]-viewpoint[1])/ray[1]
            tymax = (i.maxPt[1]-viewpoint[1])/ray[1]
            #case z
            tzmin = (i.minPt[2]-viewpoint[2])/ray[2]
            tzmax = (i.maxPt[2]-viewpoint[2])/ray[2]

            if txmin > txmax:
                txmin, txmax = txmax, txmin

            if tymin > tymax:
                tymin, tymax = tymax, tymin

            if tzmin > tzmax:
                tzmin, tzmax = tzmax, tzmin

            if txmin > tymax or tymin > txmax:
                opt= 0

            tmin=txmin
            tmax=txmax
            if tymin > tmin:
                tmin = tymin

            if tymax < tmax:
                tmax = tymax

            if tmin > tzmax or tzmin > tmax:
                opt = 0

            if tzmin >= tmin:
                tmin = tzmin
            if tzmax < tmax:
                tmax = tzmax
            # min_t=min(txmin,tymin,tzmin)
            # max_t=max(txmax,tymax,tzmax)
            # pdb.set_trace()
            if opt == 1:
                if min_d >= tmin:
                    min_d = tmin
                    idx = cnt

        cnt=cnt+1
    # pdb.set_trace()
    #return mid_distanace and nearest obj index
    return [min_d,idx]

def shade(m,ray,view,list,idx,light):
    if idx == -1:
        #check intersect point exists
        return np.zeros(3)
    else:
        result_color=np.zeros(3)
        y=0
        z=0
        n= np.zeros(3)
        v= -m * ray

        if list[idx].__class__.__name__ == "Sphere":
            n= normalize(view.viewPoint + m*ray - list[idx].center)

        elif list[idx].__class__.__name__ == 'Box':
            point_i = view.viewPoint + m*ray
            diff = sys.maxsize
            i = -1
            cnt = 0
            for normal in list[idx].normal:
                if abs(np.sum(normal[0:3] * point_i)-normal[3]) < diff:
                    diff = abs(np.sum(normal[0:3] * point_i)-normal[3])
                    i = cnt
                cnt = cnt + 1
            n = normalize(list[idx].normal[i][0:3])

        for i in light:
            l_i = normalize(v + i.position - view.viewPoint)
            max_v=max(0,np.dot(n,l_i))
            check = ray_trace(list, -l_i, i.position)
            if check[1] == idx:
                if list[idx].shader.__class__.__name__ == 'ShaderPhong':
                    v_unit = normalize(v)
                    h = normalize(v_unit + l_i)
                    max_p=pow(max(0,np.dot(n,h)),list[idx].shader.exponent[0])
                    result_color = result_color +((i.intensity)*(list[idx].shader.diffuse*max_v+ list[idx].shader.specular* max_p))
                elif list[idx].shader.__class__.__name__ == "ShaderLambertian":
                    result_color=result_color+(list[idx].shader.diffuse*i.intensity*max_v)
        result_color=Color(result_color[0],result_color[1],result_color[2])
        result_color.gammaCorrect(2.2)
        return result_color.toUINT8()

def normalize(v):
    new_v=v / np.sqrt(np.sum(v*v))
    return new_v

def Normal(x, y, z):
    dir = np.cross((y-x), (z-x))
    d = np.sum(dir*z)
    return np.array([dir[0], dir[1], dir[2], d])

def main():


    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    # set default values
    viewDir=np.array([0,0,-1]).astype(np.float)
    viewUp=np.array([0,1,0]).astype(np.float)
    viewProjNormal=-1*viewDir  # you can safely assume this. (no examples will use shifted perspective camera)
    viewWidth=1.0
    viewHeight=1.0
    projDistance=1.0
    intensity=np.array([1,1,1]).astype(np.float)  # how bright the light is.
    # print(np.cross(viewDir, viewUp))
    obj_list = []
    light_list = []
    imgSize=np.array(root.findtext('image').split()).astype(np.int)
#parsing camera
    for c in root.findall('camera'):
        viewPoint = np.array(c.findtext('viewPoint').split()).astype(np.float)
        viewDir = np.array(c.findtext('viewDir').split()).astype(np.float)
        if (c.findtext('projNormal')):
            viewProjNormal = np.array(c.findtext('projNormal').split()).astype(np.float)
        viewUp = np.array(c.findtext('viewUp').split()).astype(np.float)
        if (c.findtext('projDistance')):
            projDistance = np.array(c.findtext('projDistance').split()).astype(np.float)
        viewWidth = np.array(c.findtext('viewWidth').split()).astype(np.float)
        viewHeight = np.array(c.findtext('viewHeight').split()).astype(np.float)
#parsing objects
    for c in root.findall('surface'):
        type_c = c.get('type')
        #parsing objsects if type==sphere
        if type_c == 'Sphere':
            center_c = np.array(c.findtext('center').split()).astype(np.float)
            radius_c = np.array(c.findtext('radius')).astype(np.float)
            ref = ''
            for child in c:
                if child.tag == 'shader':
                    ref = child.get('ref')
            for d in root.findall('shader'):
                if d.get('name') == ref:
                    diffuse_d = np.array(d.findtext('diffuseColor').split()).astype(np.float)
                    type_d = d.get('type')
                    if type_d == 'Lambertian':
                        shader = ShaderLambertian(diffuse_d)
                        obj_list.append(Sphere(center_c, radius_c, shader))
                    elif type_d == 'Phong':
                        exponent_d = np.array(d.findtext('exponent').split()).astype(np.float)
                        specular_d = np.array(d.findtext('specularColor').split()).astype(np.float)
                        shader = ShaderPhong(diffuse_d, specular_d, exponent_d)
                        # pdb.set_trace()
                        obj_list.append(Sphere(center_c, radius_c, shader))
        #parsing objects if type==Box
        elif type_c == 'Box':
            minPt_c = np.array(c.findtext('minPt').split()).astype(np.float)
            maxPt_c = np.array(c.findtext('maxPt').split()).astype(np.float)

            point_a = np.array([minPt_c[0], minPt_c[1], maxPt_c[2]])
            point_b = np.array([minPt_c[0], maxPt_c[1], minPt_c[2]])
            point_c = np.array([maxPt_c[0], minPt_c[1], minPt_c[2]])
            point_d = np.array([minPt_c[0], maxPt_c[1], maxPt_c[2]])
            point_e = np.array([maxPt_c[0], minPt_c[1], maxPt_c[2]])
            point_f = np.array([maxPt_c[0], maxPt_c[1], minPt_c[2]])
            normals = []
            normals.append(Normal(point_a, point_c, point_e))
            normals.append(Normal(point_b, point_c, point_f))
            normals.append(Normal(point_a, point_b, point_d))
            normals.append(Normal(point_a, point_e, point_d))
            normals.append(Normal(point_e, point_c, point_f))
            normals.append(Normal(point_d, point_f, point_b))

            ref = ''
            for child in c:
                if child.tag == 'shader':
                    ref = child.get('ref')
            for d in root.findall('shader'):
                if d.get('name') == ref:
                    diffuse_d = np.array(d.findtext('diffuseColor').split()).astype(np.float)
                    type_d = d.get('type')
                    if type_d == 'Lambertian':
                        shader = ShaderLambertian(diffuse_d)
                        obj_list.append(Box(minPt_c, maxPt_c, shader, normals))
                    elif type_d == 'Phong':
                        exponent_d = np.array(d.findtext('exponent').split()).astype(np.float)
                        specular_d = np.array(d.findtext('specularColor').split()).astype(np.float)
                        shader = ShaderPhong(diffuse_d, specular_d, exponent_d)
                        obj_list.append(Box(minPt_c, maxPt_c, shader, normals))
#parsing lights
    for c in root.findall('light'):
        position_c = np.array(c.findtext('position').split()).astype(np.float)
        intensity_c = np.array(c.findtext('intensity').split()).astype(np.float)
        light_list.append(Light(position_c, intensity_c))
    #code.interact(local=dict(globals(), **locals()))
    view = View(viewPoint, viewDir, viewUp, viewProjNormal, viewWidth, viewHeight, projDistance, intensity)
    # Create an empty image
    width=imgSize[0]
    height=imgSize[1]
    channels=3
    img = np.zeros((height, width, channels), dtype=np.uint8)
    img[:,:]=0
    #set pixel points
    pixel_x=view.viewWidth / width
    pixel_y=view.viewHeight / height
#coordinate x,y,z to w,u,v
    w = view.viewDir #z
    u = np.cross(w, view.viewUp) #y
    v = np.cross(w, u) #x
# normalize w u v to unit_w unit_u unit_v
    unit_w=normalize(w)
    unit_u=normalize(u)
    unit_v=normalize(v)

    #start s = e+uu+vv-dw
    #u=l+(r-l)i+0.5)/nx
    start= (unit_w* view.projDistance - unit_u* (pixel_x/2.) * (width+1) - unit_v * (pixel_y/2.) *(height+1))
    # pdb.set_trace()s
    # replace the code block below!
    for x in np.arange(width):
        for y in np.arange(height):
            #make ray
            ray=start+unit_u*x*pixel_x+unit_v*y*pixel_y
            #find hit point
            hit=ray_trace(obj_list,ray,view.viewPoint)
            # pdb.set_trace()
            #set color
            img[y][x] = shade(hit[0],ray,view,obj_list,hit[1],light_list)

    rawimg = Image.fromarray(img, 'RGB')
    #rawimg.save('out.png')
    rawimg.save(sys.argv[1]+'.png')

if __name__=="__main__":
    main()
