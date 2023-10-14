from Types import Style


class StyleBinder:

    type = None
    style = None

    def __init__(self, type: Style, style: str, active: bool = True) -> None:
        self.type = type
        self.active = active
        self.style = style

    prev_style = None

    def bind(self, item: dict) -> dict:
        self.prev_style = item[self.type.value[0]]

        if not self.active:
            return item
        
        item[self.type.value[0]] = self.style
        return item

    def disable(self) -> None:
        self.active = False
    
    def enable(self) -> None:
        self.active = True
    
    def unbind(self, item: dict) -> dict:
        if not self.active:
            return item
        
        item[self.type.value[0]] = self.prev_style
        return item
    
    def get_type(self) -> Style:
        return self.type

"""
This only works with numbers
"""
class InterlacedStyleBinder:

    style1 = None,
    style2 = None,
    type = None,
    initial_content = None,
    toggle = False
    binder = None
    active = True
    
    def __init__(self, type: Style, style1: StyleBinder, style2: StyleBinder, initial_content, active: bool = True) -> None:
        self.style1 = style1
        self.style2 = style2
        self.type = type
        self.initial_content = initial_content
        self.active = active
    
    def set_initial_content(self, content) -> None:
        self.initial_content = content

    def disable(self) -> None:
        self.active = False
    
    def enable(self) -> None:
        self.active = True

    prev_style = None

    def prep(self, item: dict):
        self.prev_style = item[self.type.value[0]]
        self.toggle = False


    def iter_bind(self, item: dict, current_content:str) -> dict:
        
        # Isto significa que não é um numero, e por isso podemos 
        # saltar

        if current_content == self.initial_content or not current_content.isdigit():
            self.toggle = not self.toggle

        binder = StyleBinder(self.type, self.style1, self.active) if self.toggle else StyleBinder(self.type, self.style2, self.active)
        binder.bind(item)
        
        return item
    
    def unbind(self, item: dict) -> dict:
        item[self.type.value[0]] = self.prev_style
        self.prev_style = None
        return item

    
