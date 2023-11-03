class SerializerClassMixin:
    serializer_class = None
    serializer_create_class = None
    serializer_detail_class = None

    def get_serializer_class(self):
        if self.action == "create":
            return self.serializer_create_class
        elif self.action == "list":
            return self.serializer_class
        elif self.action == "retrieve":
            return self.serializer_detail_class
        return super().get_serializer_class()
