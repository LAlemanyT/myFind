# myFind

  myfind is a simplified version of the Unix find command I coded for a university
assignment.

  It will find and print a list of all the files that fit a description as given.
Additionally, it can run extra Unix commands in addition to myfind.

The syntax to run the command is:

  myfind.py [--regex=<pattern> | --name=<filename>] <directory> <optional command>

    directory: path (absolute or relative) to the start point of the search.

    regex/name: either a regex pattern or filename to search for (can use none and can't use
      both together).

    optional command: refers to a Unix command (in the command section, {} will take the
      name/path of the file being observed) (also supports extra flags being added to this
      command).

  In the command, the regex/name attribute can be successfully given before or after the
directory is specified. If no regex or name is given, my find will print all files in all
subdirectories starting at the specified directory path.

  The script features error handling which specify whether the error was caused by an invalid
command passed in or by an inexistent optional extra command.

  This assignment was very good practice for system calls and multi-process programming.

  My find was coded in and is optimized for an Ubuntu operating system.

#Testing

  Testing was performed via input/output text files.

#Issues

    - Due to an unclear definition of what should cause a "NONZERO EXIT ERROR",
      this error message can be a little inconsistent sometimes.
