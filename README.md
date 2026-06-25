# CommonChord - Music Version Control
    
Personal project testing the concept of an open-source version control platform for music production. The basic framework is similar to git, with commits, branches, etc. eventually to be implemented to support large music files.

# Stack 

| Tool         | Use                                              |
|--------------|--------------------------------------------------|
| C++          | General file management (storage, hashing, etc.) |
| Python       | File comparison, visualization, machine learning |
| Django       | Backend                                          |
| React/Native | Frontend web and mobile                          |
| PostgreSQL   | Database                                         | 

# Latest Updates

### Ableton File Parsing and Waveform Decomposition - 6/25/2026
- GET /api/repos/{id}/commits/{hash}/parse_als/ - parse ableton .als files into JSON
- GET /api/repos/{id}/commits/{hash}/waveform/ - downsampled amplitude data

### End-to-end Workflow - 5/5/2026
- POST /api/repos/ — created a repo on disk and in the DB
- POST /api/repos/{id}/add/ — staged a file
- POST /api/repos/{id}/commits/ — created a commit
- GET /api/repos/{id}/commits/ — retrieved and synced commit history
- GET /api/repos/{id}/checkout/{hash}/ — retrieved the correct file contents
- GET /api/repos/{id}/status/  — current staging status

### Binary File (Git Like) Storage Handling - 4/21/2026
- Find, create, and add hashed binary objects to repositories
- Status and add checks to add only what is wanted
- Implemented and tested in C++ 

# Features to be Implemented

- Profiles to store/access musical repositories from different access points
- Quick access to stored versions of music production files for remote collaboration
- Visual comparison between different versions of .WAV files, eventually extended to DAW project files: .als (ableton), .logicx (logic), .ptx (pro tools) 
- Machine learning to determine genre/vibe of created music
