from website_creator.dimacs_reader import DimacsReader
from file_ui.file_utils import remove_file_extension

def main():

    path = "data/dimacs_example"
    DR = DimacsReader(path)
    nodes, edges = DR.read_dimacs_file("example.dimacs")
    print(nodes)
    print(edges)
    filename = "example.dimacs"
    ext = ".dimacs"
    new = remove_file_extension(filename, ext)
    print(new)



if __name__ == "__main__":
    main()
