import glob
import os
import re

def proto_compile(output_path):
    import grpc_tools.protoc

    cli_args = [
        "grpc_tools.protoc",
        "--proto_path=hivemind/proto",
        f"--python_out={output_path}",
    ] + glob.glob("hivemind/proto/*.proto")

    code = grpc_tools.protoc.main(cli_args)
    if code:  # hint: if you get this error in jupyter, run in console for richer error message
        raise ValueError(f"{' '.join(cli_args)} finished with exit code {code}")
    # Make pb2 imports in generated scripts relative
    for script in glob.iglob(f"{output_path}/*.py"):
        with open(script, "r+") as file:
            code = file.read()
            file.seek(0)
            file.write(re.sub(r"\n(import .+_pb2.*)", "from . \\1", code))
            file.truncate()


if __name__ == "__main__":
    
    current_file_path = os.path.abspath(__file__)
    dir_name = os.path.dirname(os.path.dirname(current_file_path))
    print(f"Compiling all the .proto files in directory {os.path.join(dir_name, 'proto')}")
    proto_compile(os.path.join(dir_name, "proto"))
