// the orchestrator. This is the only file that knows about the whole system and calls the
// others. Each user command (init, add, commit, log, checkout) is a method here. It holds
// a path to the repo root and creates the ObjectStore, Index, etc. as member objects.

// Class: Repository
//      public:
//          init(), add(filePath), commit(message), log(), checkout(hashOrBranch, outputPath)
//      private:
//          resolveRef(name) -> hash, headHash() -> string, writeHead(hash), findRepoRoot() -> path

#include "repository.h"
#include <iostream>

/**
 * Constructs a Repository rooted at the given path. Does not initialize anythin on the disk. Need to
 * call init() for that.
 * @param repoRoot The root directory of the repository.
 * @throws std::runtime_error if the repoRoot is not a valid directory.
 */
Repository::Repository(const std::filesystem::path &repoRoot) : m_root(repoRoot) {}

// Public Interface

/**
 * Creates the .bvcs directory structure on disk
 * @throws std::runtime_error if the repository is already initialized at the given path or if there 
 * is an error creating the directory structure.
 */
void Repository::init()
{
    if (isInitialized())
    {
        throw std::runtime_error("Repository already exists at: " + m_root.string());
    }

    // Create the directory structure
    std::filesystem::create_directories(bvcsDir() / "objects");
    std::filesystem::create_directories(refsDir());

    // Write an empty HEAD file to mark the repo as initialized but
    // with no commits yet
    writeFileAtomic(bvcsDir() / "HEAD", {});

    std::cout << "Initialized empty repository at " << m_root.string() << "\n";
}

/**
 * Hashes the file at filePath and writes the hash to the index
 * @param filePath The path to the file to add to the staging area.
 * @throws std::runtime_error if the file does not exist or the repo is not initialized
 */
void Repository::add(const std::filesystem::path &filePath) {}

/**
 * Creates a commit from the currently staged hash, writes it to the object store, and advances HEAD
 * @param message The commit message describing the changes in this commit.
 * @throws std::runtime_error if there is no staged hash, the repo is not initialized
 */
void Repository::commit(const std::string &message) {}

/**
 * Walks the commit chain from HEAD and prints each commit's metadata to stdout.
 */
void Repository::log() const {}

/** 
 * Retrieves the file associated with the given commit hash (or branch name) and writes it to outputPath
 * @param hashOrBranch The commit hash or branch name to check out.
 * @param outputPath The path where the checked-out file will be written.
 */
void Repository::checkout(const std::string &hashOrBranch, const std::filesystem::path &outputPath) const {}

/**
 * Returns the root path of this repository
 */
std::filesystem::path Repository::root() const
{
    return m_root;
}

/**
 * Returns true if a .bvcs directory exists at the repoRoot
 */
bool Repository::isInitialized() const
{
    return std::filesystem::exists(bvcsDir());
}

// Private Helpers

/**
 * Returns the path to .bvcs directory
 */
std::filesystem::path Repository::bvcsDir() const 
{
    return m_root / ".bvcs";
}

/**
 * Returns the path to .bvcs/refs/heads/
 */
std::filesystem::path Repository::refsDir() const {
    return bvcsDir() / "refs" / "heads";
}

/**
 * Returns the full SHA-256 hash that HEAD currently points to, or an empty string if the repo has no commits yet.
 */
std::string Repository::headHash() const {}

/**
 * Writes a commit hash to .bvcs/HEAD
 * @param hash The commit hash to write to HEAD.
 */
void Repository::writeHead(const std::string &hash) {}

/**
 * Given a branch name or a hash prefix/full hash, returns the full resolved commit hash
 * @throws std::runtime_error if the name cannot be resolved to a valid commit hash
 * @param hashOrBranch The branch name or hash prefix/full hash to resolve.
 * @return The full commit hash that the name resolves to.
 */
std::string Repository::resolveRef(const std::string &hashOrBranch) const {}

/**
 * @throws std::runtime_error if the repository is not initialized
 */
void Repository::assertInitialized() const {}

/**
 * @throws std::runtime_error if there is no staged hash in the index
 */
void Repository::assertStaged() const {}