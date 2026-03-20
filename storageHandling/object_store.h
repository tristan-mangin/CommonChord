// responsible for reading and writing blobs to objects/. It takes a hash and gives back bytes, 
// or takes bytes and returns a hash. It decides the objects/ab/cdef123... directory sharding 
// scheme. It does not know what a commit is — it just stores and retrieves opaque byte sequences.

// storeFromFile(filePath) -> hash_string
// retrieveToFile(hash, filePath) -> void
// exists(hash) -> bool
// objectPath(hash) -> filesystem::path