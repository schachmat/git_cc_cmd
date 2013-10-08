# git_cc_cmd

gets authors of a diff from git blame to send a cc about the diff

# usage

	git config --global sendmail.cccmd [PATH TO git_cc_cmd]

# known bugs / problems

* No support for spaces and other weird characters in filenames of patched files
  yet
* Deletion / Moving of files not handled correctly
