# CommonChord - Music Version Control
    
Personal project testing the concept of an open-source version control platform for music production. The basic framework is similar to git, with commits, branches, etc. eventually to be implemented to support large music files.

# Stack (current plan)

| Tool         | Use                                              |
|--------------|--------------------------------------------------|
| C++          | General file management (storage, hashing, etc.) |
| Python       | File comparison, visualization, machine learning |
| Django       | Backend                                          |
| React/Native | Frontend web and mobile                          |
| PostgreSQL   | Database                                         | 

# Latest Updates
### BVCS (Bindary Version Control System) - 4/21/2026
- Custom built C++ command line tool that functions similarly to Git, but designed specifically for large binary files (specifically audio recordings and DAW project files).
- Content-addressed storage used to store every version of a file. Each is identified by the SHA-256 hash of its contents. Stops identical files from being stored more than once and each version is automatically integrity checked.
- Users initialize a repo with the bvcs init, stage a file with bvcs checkout, with all version history stored locally in a .bvcs folder.
- All file I/O is streamed directly between disk locations without loading file contents into memory, making it practical for audio files that can be hundreds of megabytes in size.
- This CLI is intended to be driven by a Django backend via subprocess calls, which will expose the version control functionality through a REST API and eventually a web frontend featuring audio waveform visualization, Daw project file snapshots, and genre/vibe classification through machine learning.

# Features to be Implemented

- Profiles to store/access musical repositories from different access points
- Quick access to stored versions of music production files for remote collaboration
- Visual comparison between different versions of .WAV files, eventually extended to DAW project files: .als (ableton), .logicx (logic), .ptx (pro tools) 
- Machine learning to determine genre/vibe of created music
