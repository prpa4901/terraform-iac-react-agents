import os
import pathlib
from pydantic import BaseModel
from langchain_core.tools import tool
import subprocess

PARENT_DIR_PATH = str(pathlib.Path(os.getcwd()))


class IACToolInput(BaseModel):
    terraform_operation_command: str

class IACOperator:
    def __init__(self, workspace="infra-tf"):
        self.workspace = str(pathlib.Path(PARENT_DIR_PATH).joinpath(workspace))

    def run_terraform_command(self, command: str):
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                check=True,
                cwd="/home/priteshlp243/projects1/terraform-iac-react-agents/infra-tf",
                text=True
            )
            result = result.stdout
            import re
            ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
            result = ansi_escape.sub('', result)
            return result
        except FileNotFoundError:
            return "Error: Terraform command not found. Please ensure Terraform is installed and available in your PATH."
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
  
@tool(return_direct=True, args_schema=IACToolInput)
def run_terraform_operation_tool(terraform_operation_command: str):

    """Executes a Terraform command and returns the output of the plan or apply."""
    iac_operator = IACOperator()
    return iac_operator.run_terraform_command(terraform_operation_command)
