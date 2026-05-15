import os   # todo: switch file handling stuff to pathlib
import config
import subprocess

def get_files_info(working_directory:str, directory:str=".") -> str:
    """Lists all files/directories in a provided directory (name, size, is_dir).
    Args:
        :param working_dir: parent directory, boundary for workspace
        :param directory: the target directory, relative to working directory
    Returns: 
    """
    # get full paths of working and target directories
    work_dir_full_path = os.path.abspath(working_directory)
    target_dir_full_path = os.path.normpath(os.path.join(work_dir_full_path,directory))

    if not os.path.isdir(target_dir_full_path):
        return f"Error: '{directory}' is not a directory"

    if not is_valid_dir(work_dir_full_path,target_dir_full_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    files_in_dir = [os.path.join(target_dir_full_path, f) for f in os.listdir(target_dir_full_path)]

    summary = construct_summary(directory, files_in_dir)

    return summary


def is_valid_dir(working_dir: str, target_dir: str) -> bool:
    """ checks if the target is inside the working dir
    """
    is_valid = True
    common_path = os.path.commonpath([working_dir, target_dir])

    if working_dir != common_path:
        is_valid = False

    return is_valid


def get_file_info(filename:str) -> str:
    file_size = os.path.getsize(filename)
    is_dir = os.path.isdir(filename)

    return f" - {filename}: file_size={file_size} bytes, is_dir={is_dir}"


def construct_summary(directory: str, filenames: list[str]) -> str:
    """
    """
    header = [f"Result for '{directory}' directory:"]
    files_info = [get_file_info(f) for f in filenames]

    message = '\n'.join(header + files_info)
    return message


def get_file_content(working_directory: str, file_path: str) -> str:
    """
    """
    # get full paths of working dir and target file
    work_dir_full_path = os.path.abspath(working_directory)
    file_path_full_path = os.path.join(work_dir_full_path, file_path)

    if not is_valid_dir(work_dir_full_path, file_path_full_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(file_path_full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    

    with open(file_path_full_path, "r") as f:
        content = f.read(config.MAX_CHARS)
        if f.read(1):
            content += f'File {file_path} truncated: True'

        return content
    

def write_file(working_directory: str, file_path: str, content: str) -> str:
    """
    """
    # get full paths of working dir and target file
    work_dir_full_path = os.path.abspath(working_directory)
    file_path_full_path = os.path.join(work_dir_full_path, file_path)

    if os.path.isdir(file_path_full_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    if not is_valid_dir(work_dir_full_path, file_path_full_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    target_dir = os.path.dirname(file_path_full_path)
    os.makedirs(target_dir, exist_ok=True)
    
    try:
        with open(file_path_full_path, "w") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: Could not write to {file_path}: {e}"


def run_python_file(working_directory, file_path, args=None):
    """
    """
    try:
        # get full paths of working dir and target file
        work_dir_full_path = os.path.abspath(working_directory)
        file_path_full_path = os.path.normpath(os.path.join(work_dir_full_path, file_path))  # might need to add this elsewhere

        if not is_valid_dir(work_dir_full_path, file_path_full_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(file_path_full_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path_full_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python3", file_path_full_path]
        if args is not None:
            command.extend(args)

        completed_process = subprocess.run(args=command,cwd=work_dir_full_path,capture_output=True,timeout=30,text=True)

        outputs = []
        if completed_process.returncode != 0:
            outputs.append(f"Process exited with code {completed_process.returncode}")
        if completed_process.stderr is None and completed_process.stdout is None:
            outputs.append("No output produced")
        if completed_process.stdout is not None:
            outputs.append(f"STDOUT: {completed_process.stdout}")
        if completed_process.stderr is not None:
            outputs.append(f"STDERR: {completed_process.stderr}")

        output_string = '\n'.join(outputs)
        
        return output_string
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
