class MaskPosition:

    def __init__(self, **kwargs):
        self.point = kwargs.get('point')
        self.x_shift = kwargs.get('x_shift')
        self.y_shift = kwargs.get('y_shift')
        self.scale = kwargs.get('scale')
