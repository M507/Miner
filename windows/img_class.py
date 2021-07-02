

class Img_Object:

    def __init__(self, img_name, point1, point2, text = None):
        self.img_name = img_name
        self.point1 = point1
        self.point2 = point2
        self.text = text
        self.priority_number = 0

    def change_text(self, text):
        text = text.lower()
        self.text = text

    def get_img_name(self):
        return self.img_name

    def get_point1(self):
        return self.point1

    def get_point2(self):
        return self.point2

    def get_text(self):
        return self.text

    def get_priority_number(self):
        return self.priority_number

    def set_priority_number(self, number):
        self.priority_number = number

    def __eq__(self, other):
        if not isinstance(other, Img_Object):
            return NotImplemented
        return self.img_name == other.img_name
