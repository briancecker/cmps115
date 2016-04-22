import os

PROJECT_DIR = os.path.abspath(os.path.join(__file__, "..", ".."))
RESOURCES_DIR = os.path.abspath(os.path.join(PROJECT_DIR, "resources"))
TMP_DIR = os.path.abspath(os.path.join(PROJECT_DIR, "tmp"))

if not os.path.exists(RESOURCES_DIR):
    os.makedirs(RESOURCES_DIR)

if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)


def abs_resource_path(resource_path):
    """
    Get the absolute path to some resource file in resources.
    Args:
        resource_path: list of path pieces starting inside the resources directory.
        e.g. to get to resources/some_dir/test.txt pass ["some_dir", "test.txt"]

    Returns: An absolute path as a string

    """
    return os.path.abspath(os.path.join(RESOURCES_DIR, *resource_path))


def path_leaf(path):
    """
    Gets the leaf of a path
    Args:
        path: path as a string

    Returns: leaf (last file or directory) in a path as a string

    """
    head, tail = os.path.split(path)
    return tail or os.path.basename(head)
