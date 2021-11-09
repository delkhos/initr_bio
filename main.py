import sys
from bdgates import parser as parser_bdgates
from bdgates import gates
from bdgates import relations

def main():
    if len(sys.argv) != 5:
        print("usage: main.py [gate database file] [verilog file] [tolerance] [destination file]")
        sys.exit()

    bdgate_path = sys.argv[1]
    source_path = sys.argv[2]
    tolerance   = float(sys.argv[3])
    dest_path   = sys.argv[4]

    try:
        bdgate = open(bdgate_path).read() 
    except FileNotFoundError:
        print("Gates database file not found.")
        sys.exit()
    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=} when trying to open gates database file")

    parser_bdgates.parse(bdgate)

    try:
        source = open(source_path).read() 
    except FileNotFoundError:
        print("Source file not found.")
        sys.exit()
    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=} when trying to source file")

    from verilog import parse_verilog

    try:
        with open(dest_path, "w") as dest:
            transformed_source = parse_verilog(source, tolerance, gates, relations)
            print(transformed_source, file = dest)
    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")

if __name__ == "__main__":
    main()

