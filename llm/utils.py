import argparse  # For parsing command-line arguments

# Function to parse command-line arguments
def parse_arguments():
    """
    Parse command-line arguments.
    :return: Parsed arguments
    """
    parser = argparse.ArgumentParser(description='Command-line interface for querying and managing models.')  # Set up argument parser
    parser.add_argument("--hide-source", "-S", action='store_true',  # Option to hide source documents
                        help='Whether to hide source documents in the query results.')
    parser.add_argument("--mute-stream", "-M", action='store_true',  # Option to mute streaming output
                        help='Whether to mute streaming of model outputs.')
    return parser.parse_args()  # Return parsed arguments
