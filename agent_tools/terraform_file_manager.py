import os
import pathlib
from pydantic import BaseModel
from langchain_core.tools import tool


PARENT_DIR_PATH = str(pathlib.Path(os.getcwd()))


class TerraformToolInput(BaseModel):
    filename: str
    content: str
    mode: str

class TerraformFileManager:
    def __init__(self, workspace="infra-tf"):
        self.workspace = str(pathlib.Path(PARENT_DIR_PATH).joinpath(workspace))
        os.makedirs(self.workspace, exist_ok=True)

    def write_to_disk(self, filename: str, content: str, mode="w") -> str:
        file_path = os.path.join(self.workspace, filename)
        print(f"File path: {file_path}")
        with open(file_path, mode) as f:
            f.write("\n"+content+"\n")
        return f"{filename} written."

    def read_file(self, filename: str):
        file_path = os.path.join(self.workspace, filename)
        with open(file_path, "r") as fp:
            file_content = fp.read()
        return f"{filename}: {file_content}"
   

    
@tool(args_schema=TerraformToolInput)
def generate_tf_file_tool(filename: str, content: str, mode: str):
    """Write terraform generate content to file. File Mode: 'w' for overwrite, 'a' for append."""
    tf_file_writer_obj = TerraformFileManager()
    return tf_file_writer_obj.write_to_disk(filename=filename, content=content, mode=mode)

@tool(args_schema=TerraformToolInput)
def read_tf_file_tool(filename: str, content=None, mode="r"):
    """Read the content of the file for verifying current infra or new applied configuration"""
    tf_file_writer_obj = TerraformFileManager()
    return tf_file_writer_obj.read_file(filename=filename)

@tool
def list_tf_workspace_files_tool():
    """Lists the current terraform files in the workspace"""
    tf_file_manager = TerraformFileManager()
    return os.listdir(tf_file_manager.workspace)

