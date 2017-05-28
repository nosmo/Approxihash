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

TODO
-------
```TODO.org``` is tracking upcoming features and/or bugs.
