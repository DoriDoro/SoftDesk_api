class SerializerClassMixin:
    serializer_create_class = None
    serializer_detail_class = None
    serializer_list_class = None

    def get_serializer_class(self):
        if self.action == "create":
            return self.serializer_create_class
        elif self.action == "retrieve":
            return self.serializer_detail_class
        elif self.action == "list":
            return self.serializer_list_class
        return super().get_serializer_class()
