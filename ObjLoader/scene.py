import numpy
from ObjLoader.node import Sphere, Cube, SnowFigure

class Scene(object):

    #放置节点的深度，放置的节点距离摄像机15个单位
    PLACE_DEPTH = 15.0

    def __init__(self):
        #场景下的节点队列
        self.node_list = list()
        self.selected_node = None

    def add_node(self, node):
        """ 在场景中加入一个新节点 """
        self.node_list.append(node)

    def render(self):
        """ 遍历场景下所有节点并渲染 """
        for node in self.node_list:
            node.render()

    def place(self, shape, start, direction, inv_modelview):
        new_node = None
        if shape == 'sphere':
            new_node = Sphere()
        elif shape == 'cube':
            new_node = Cube()
        elif shape == 'figure':
            new_node = SnowFigure()

        self.add_node(new_node)

        # 得到在摄像机坐标系中的坐标
        translation = (start + direction * self.PLACE_DEPTH)

        # 转换到世界坐标系
        pre_tran = numpy.array([translation[0], translation[1], translation[2], 1])
        translation = inv_modelview.dot(pre_tran)

        new_node.translate(translation[0], translation[1], translation[2])

    def move_selected(self, start, direction, inv_modelview):

        if self.selected_node is None: return

        # 找到选中节点的坐标与深度（距离）
        node = self.selected_node
        depth = node.depth
        oldloc = node.selected_loc

        # 新坐标的深度保持不变
        newloc = (start + direction * depth)

        # 得到世界坐标系中的移动坐标差
        translation = newloc - oldloc
        pre_tran = numpy.array([translation[0], translation[1], translation[2], 0])
        translation = inv_modelview.dot(pre_tran)

        # 节点做平移变换
        node.translate(translation[0], translation[1], translation[2])
        node.selected_loc = newloc

