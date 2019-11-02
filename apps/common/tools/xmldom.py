import xml.etree.cElementTree as ET


def read_xml_file(file_path):
    return ET.ElementTree(file_path)