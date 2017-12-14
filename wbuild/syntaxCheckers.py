"""A list of synthax checkers
"""


def no_tabs(header):
    """Check that the header contains no tabs

    Args:
      header: Header string

    Returns:
      everything ok: empty string
      error: error message
    """
    if "\t" in header:
        return "Tabs found in the header. Please remove them"
    else:
        return ""


# list all the synthax checkers here
CHECKERS = [("no_tabs", no_tabs)]


def checkHeaderSynthax(header):
    """Check the header synthax

    Args:
      file_path: file to be checked
    """

    errors = ""
    for name, checker in CHECKERS:
        error = checker(header)
        if error:
            errors += "{0}: {1}".format(name, error)

    if errors:
        raise ValueError("Errors parsing the header file: \n{0}\n{1}".format(header, errors))
