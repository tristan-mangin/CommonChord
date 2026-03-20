// anything that doesn't belong to a specific domain but is used in multiple files. Reading
// a whole file into a vector<byte>, writing bytes atomically via temp file + rename,
// formatting a timestamp as a string.

// readFileBinary(path) -> vector<byte>
// writeFileAtomic(path, data)
// formatTimestamp(time_t) -> string
// hexToBytes(hex) -> vector<byte>

#include "utils.h"
#include <fstream>

/**
 * Reads the entire contents of a file into a vector of bytes.
 * @param filePath The path to the file to read.
 * @return A vector containing the bytes read from the file.
 * @throws std::runtime_error if the file cannot be opened.
 */
std::vector<unsigned char> readFileBinary(const std::filesystem::path &filePath)
{
    // Open the file in binary mode
    std::ifstream file(filePath, std::ios::binary);
    if (!file)
    {
        throw std::runtime_error("Could not open file: " + filePath.string());
    }

    // Read the file contents into a vector of bytes
    std::vector<unsigned char> data((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
    return data;
}

/**
 * Writes data to a file atomically by first writing to a temporary file and then renaming it.
 * @param filePath The path to the file to write.
 * @param data The byte data to write to the file.
 * @throws std::runtime_error if the file cannot be written.
 */
void writeFileAtomic(const std::filesystem::path &filePath, const std::vector<unsigned char> &data)
{
    // Create a temporary file path in the same directory as the target file
    std::filesystem::path tempFilePath = filePath;
    tempFilePath += ".tmp";

    // Write data to the temporary file
    std::ofstream tempFile(tempFilePath, std::ios::binary);
    if (!tempFile)
    {
        throw std::runtime_error("Could not open temporary file for writing: " + tempFilePath.string());
    }
    tempFile.write(reinterpret_cast<const char *>(data.data()), data.size());
    tempFile.close();

    // Atomically rename the temporary file to the target file
    std::filesystem::rename(tempFilePath, filePath);
}

/**
 * Formats a timestamp as a human-readable string.
 * @param timestamp The time to format, represented as a time_t value.
 * @return A string representing the formatted timestamp.
 */
std::string formatTimestamp(std::time_t timestamp)
{
    std::tm *tm = std::localtime(&timestamp);
    char buffer[20];
    std::strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", tm);
    return std::string(buffer);
}

/**
 * Converts a hex string to a vector of bytes.
 * @param hex The hex string to convert.
 * @return A vector containing the bytes represented by the hex string.
 * @throws std::runtime_error if the hex string is invalid.
 */
std::vector<unsigned char> hexToBytes(const std::string &hex)
{
    if (hex.length() % 2 != 0)
    {
        throw std::runtime_error("Invalid hex string: length must be even");
    }
    std::vector<unsigned char> bytes;
    bytes.reserve(hex.length() / 2);
    for (size_t i = 0; i < hex.length(); i += 2)
    {
        unsigned char byte = std::stoul(hex.substr(i, 2), nullptr, 16);
        bytes.push_back(byte);
    }
    return bytes;
}