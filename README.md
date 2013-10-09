# git_cc_cmd

gets authors of a diff from git blame to send a cc about the diff

# usage

	git config --global sendmail.cccmd [PATH TO git_cc_cmd]

# known bugs / problems

* No support for spaces and other weird characters in filenames of patched
  files. This will not be implemented since i discourage such filenames. Also
  there is a nice
„[feature](https://github.com/git/git/commit/1a9eb3b9d50367bee8fe85022684d812816fe531)“
  about spaces in filenames.
* Merge commits will not be handled, since git seems to not produce a patch-file
  for them.
* Changes to files containing only one line will not result in this files author
  to be output.
