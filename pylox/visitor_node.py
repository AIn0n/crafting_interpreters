class Visitor_node:
    def accept(self, visitor):
        method_name = "visit" + type(self).__name__
        method = getattr(visitor, method_name)
        return method(self)
