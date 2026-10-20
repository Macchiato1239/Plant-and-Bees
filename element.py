
class Element:
    def __init__(self):
        self.__elements=[]

    @property
    def elements(self):
        return self.elements

    def add_element(self, e):
        self.__elements.append(e)
elements=Element()