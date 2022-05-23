import xml.sax as sax


class XmlReader(sax.ContentHandler):
    def __init__(self) -> None:
        super().__init__()
        self.current = None
        self.table_data = []
        self.animal_data = []
        self.parser = sax.make_parser()

    def startElement(self, name, attrs):
        self.current = name
        if name == "animal":
            pass

    def characters(self, content) -> None:
        if self.current == "type":
            self.type = content
        elif self.current == "id":
            self.id = content
        elif self.current == "row_index":
            self.row_index = content
        elif self.current == "column_index":
            self.column_index = content
        elif self.current == "sex":
            self.sex = content

    def endElement(self, name) -> None:
        if self.current == "type":
            self.animal_data.append(self.type)
        elif self.current == "id":
            self.animal_data.append(int(self.id))
        elif self.current == "row_index":
            self.animal_data.append(int(self.row_index))
        elif self.current == "column_index":
            self.animal_data.append(int(self.column_index))
        elif self.current == "sex":
            self.animal_data.append(self.sex)
        if len(self.animal_data) == 5:
            self.table_data.append(tuple(self.animal_data))
            self.animal_data = []

        self.current = ""
