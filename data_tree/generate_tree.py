import xml.etree.ElementTree as ET
from xml.dom import minidom

tree =  ET.parse('data/icd10gm2023.xml')
root = tree.getroot()

def generate_tree(tree: ET.ElementTree):
    icd_root = ET.Element('ICD10GM')

    root = tree.getroot()

    code_to_elem = {}
    for elem in root.iter('Class'):
        code_to_elem[elem.attrib['code']] = elem

    # Define a function to get the description of an element
    def get_description(elem):
        label = elem.find(".//Label")
        if label is not None:
            return label.text
        else:
            return ""

    for chapter in root.findall(".//Class[@kind='chapter']"):
        icd_chapter = code_to_elem.get(chapter.attrib['code'], None)
        if icd_chapter is not None:
            chapter_elem = ET.Element('item', {'type': 'chapter'})
            name_elem = ET.Element('name')
            name_elem.text = chapter.attrib['code']
            description_elem = ET.Element('description')
            description_elem.text = get_description(icd_chapter)

            chapter_elem.append(name_elem)
            chapter_elem.append(description_elem)

            icd_root.append(chapter_elem)

    for block in root.findall(".//Class[@kind='block']"):
        icd_block = code_to_elem.get(block.attrib['code'], None)
        if icd_block is not None:
            block_elem = ET.Element('item', {'type': 'block'})
            name_elem = ET.Element('name')
            name_elem.text = block.attrib['code']
            description_elem = ET.Element('description')
            description_elem.text = get_description(icd_block)

            block_elem.append(name_elem)
            block_elem.append(description_elem)

            super_class_code = icd_block.find(".//SuperClass").attrib['code']

            super_class = icd_root.find(".//item[name='"+super_class_code+"']")

            super_class.append(block_elem)

    for category in root.findall(".//Class[@kind='category']"):
        icd_category = code_to_elem.get(category.attrib['code'], None)
        if icd_category is not None:
            category_elem = ET.Element('item', {'type': 'category'})
            if len(category.attrib['code']) > 3:
                category_elem = ET.Element('item', {'type': 'subcategory'})
            name_elem = ET.Element('name')
            name_elem.text = category.attrib['code']
            description_elem = ET.Element('description')
            description_elem.text = get_description(icd_category)

            category_elem.append(name_elem)
            category_elem.append(description_elem)

            super_class_code = icd_category.find(".//SuperClass").attrib['code']

            super_class = icd_root.find(".//item[name='"+super_class_code+"']")

            super_class.append(category_elem)




    return ET.ElementTree(icd_root)

icd_tree = generate_tree(tree)

pretty_tree = minidom.parseString(ET.tostring(icd_tree.getroot())).toprettyxml(indent='\t')

with open("icd_tree_2.xml", "w") as f:
    f.write(pretty_tree)



