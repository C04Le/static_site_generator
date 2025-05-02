from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if text_type != TextType.TEXT or delimiter not in node.text:
            new_nodes.append(node)
        elif node.text.count(delimiter) % 2 != 0:
            raise Exception(f"Invalid markdown syntax - closing delimiter missing in {node}")
        else:
             #run another for loop which will be checking how many times we split > mod 2 == 1 or 0 to identify if it's normal text or delimited text   
            pass
    return new_nodes

print(split_nodes_delimiter([TextNode("This is **text** with a **bold** word", TextType.TEXT)],"**",TextType.TEXT))