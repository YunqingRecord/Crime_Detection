import os
import xml.etree.ElementTree as ET


def remove_xml(path=r'P:\YOLO_version3\darkflow\VOCdevkit\VOC2007\Annotations2'):
    files = os.listdir(path)
    for file in files:
        filename = 'P:\YOLO_version3\darkflow\VOCdevkit\VOC2007\Annotations2\\'+file
        tree = ET.parse('P:\YOLO_version3\darkflow\VOCdevkit\VOC2007\Annotations2\\'+file)
        root = tree.getroot()
        for ele in root.iter("object"):
            if ele[0].text != "person":
                print(ele[0].text)
                root.remove(ele)
        tree.write(filename)


remove_xml()




