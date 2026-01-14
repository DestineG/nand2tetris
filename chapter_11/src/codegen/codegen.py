# src/codegen/codegen.py

class CodeGenerator:
    def __init__(self, output_file):
        self.output = open(output_file, 'w')

    def write_push(self, segment, index):
        seg_map = {
            "var": "local",
            "arg": "argument",
            "field": "this",
            "static": "static"
        }
        real_seg = seg_map.get(segment, segment)
        self.output.write(f"push {real_seg} {index}\n")
    
    def write_pop(self, segment, index):
        seg_map = {
            "var": "local",
            "arg": "argument",
            "field": "this",
            "static": "static"
        }
        real_seg = seg_map.get(segment, segment)
        self.output.write(f"pop {real_seg} {index}\n")

    def write_arithmetic(self, command):
        # add | sub | neg | eq | gt | lt | and | or | not
        self.output.write(f"{command.lower()}\n")
    
    def write_label(self, label):
        self.output.write(f"label {label}\n")
    
    def write_goto(self, label):
        self.output.write(f"goto {label}\n")
    
    def write_if(self, label):
        self.output.write(f"if-goto {label}\n")
    
    def write_call(self, name, n_args):
        self.output.write(f"call {name} {n_args}\n")
    
    def write_function(self, name, n_locals):
        self.output.write(f"function {name} {n_locals}\n")
    
    def write_return(self):
        self.output.write("return\n")