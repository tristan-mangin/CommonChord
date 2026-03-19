// take a byte buffer or a file path and return a hex string hash. It knows nothing about files 
// on disk beyond reading bytes. Everything else that needs a hash calls this. Keeping it isolated 
// means you can swap SHA-256 for something else (xxHash, BLAKE3) by changing exactly one file.

// hashFile(path) -> string
// hashBytes(buffer, size) -> string