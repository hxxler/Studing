class TreeNode:
    def __init__(self, letter):
        self.letter = letter  
        self.ids = []         
        self.children = {}   

    def add_id(self, identifier):
        if identifier not in self.ids:
            self.ids.append(identifier)
            self.ids.sort() 

    def find_id(self, identifier):
        return identifier in self.ids

class HashTree:
    def __init__(self):
        self.root = {}

    def add_identifier(self, identifier):
        identifier = identifier[:32]
        
        first_letter = identifier[0]
        if first_letter not in self.root:
            self.root[first_letter] = TreeNode(first_letter)
        
        node = self.root[first_letter]
        node.add_id(identifier)

    def find_identifier(self, identifier):
        identifier = identifier[:32]

        first_letter = identifier[0]
        if first_letter in self.root:
            node = self.root[first_letter]
            return node.find_id(identifier)
        return False

    def display_tree(self):
        for letter, node in self.root.items():
            print(f"Letter '{letter}': {node.ids}")

def read_identifiers_from_file(file_path):
    identifiers = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                identifier = line.strip() 
                if identifier:  
                    identifiers.append(identifier)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    return identifiers

def main():
    tree = HashTree()
    
    file_path = 'identifiers.txt'
    identifiers = read_identifiers_from_file(file_path)

    for id_ in identifiers:
        tree.add_identifier(id_)

    tree.display_tree()

    search_id = 'A123'
    if tree.find_identifier(search_id):
        print(f"Identifier '{search_id}' found.")
    else:
        print(f"Identifier '{search_id}' not found.")

if __name__ == "__main__":
    main()