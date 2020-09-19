Approxihash
========

Approxihash is a simple tool for generation of lists of hashes based on
arbitrary key-value data. The initial usecase for this tool was for
testing weak hashing mechanisms in keys and identifiers used on
web applications.

Example Usecase
--------

Assuming knowledge of a user ID, an email and a userclass, approxihash
can be used as follows:

```approxihash.py -k userid:d00df00f email:nosmo@nosmo.me user_class:admin -H sha1 md5```

This command will return a list of hashes based on permutations of all
of the key-value data, hashed by the supplied functions. These hashes
can then be piped to other tools or pipelines, and if a hash is found
to be valid, the same command can be run again with the ```-v``` flag
to show what combination of elements and which hash function were used
to generate the hash.

Features
-------

*JSON input*: If the `-j`/`--json` parameter is passed on the
 commandline, any input to STDIN will be treated as JSON. At the
 moment the only supported data is a dictionary of key:value pairs.

*Hash functions*: Approxihash supports all default hashlib functions
 and these can be specified on the command line using
 `--hashfn`/`-H`. A special `ALL` hash function is supported that will
 generate all hashes with all hash functions.

*Minimum combinations*: The `--min-combinations`/`-m` command line
 argument specifies the minimum number of parameters used for
 hashing - meaning that for 10 arguments with a minimum combination
 factor of 3, only combinations of three or more elements from the 10
 items in the argument list will be hashed.

*Dividers*: By default the permutations of input data will not be
 joined by a separator. The `--divider`/`-D` flag can be used to
 specify a divider. Without a divider specified, hashed data for
 `["a","b","c"]` will take combinations akin to `abc`. With a divider
 specified, the combinations will be of the form `a,b,c,`.

TODO
-------
```TODO.org``` is tracking upcoming features and/or bugs.
