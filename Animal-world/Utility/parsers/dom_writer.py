import xml.dom.minidom as minidom


class XmlWriter:
    def __init__(self, file_name: str) -> None:
        """
        DOM parser for writing XML files
        :param file_name: name of the file
        """
        self.file_name = file_name
        self.document = minidom.Document()
        self.rows = []

    def create_animals(self, data: dict) -> None:
        """
        Creates animal element based on input data
        :param data: dictionary with ['id', 'type', 'row_index, 'column_index', 'sex'] keys
        :return: None
        """
        animal = self.document.createElement("animal")

        for key in data:
            temp_child = self.document.createElement(key)
            animal.appendChild(temp_child)
            node_text = self.document.createTextNode(data[key].strip())
            temp_child.appendChild(node_text)
        self.rows.append(animal)

    def create_xml_file(self) -> None:
        table = self.document.createElement("table")

        for animal in self.rows:
            table.appendChild(animal)

        self.document.appendChild(table)

        self.document.writexml(open(self.file_name, 'w'),
                               indent="  ",
                               addindent="  ",
                               newl='\n'
                               )
        self.document.unlink()
