commit f10040f8df1de76b877b9dec09a4fcfd6f7b17af
Author: Oz <ozcodx@gmail.com>
Date:   Mon May 5 19:16:04 2025 -0500

    Add prompt analysis and search command processing to ChatSession
    
    - Implemented a new method to analyze user prompts and determine if a search is required.
    - Added instructions for users on how to format search commands within prompts.
    - Enhanced the get_response method to handle search commands and process them accordingly.
    - Introduced regex-based command processing for different search types (internet, memory, database).
    - Improved error handling and logging for prompt analysis and response generation.

commit 4dc5c8c98d779c7064fead4ee874a4004e6db964
Author: Oz <ozcodx@gmail.com>
Date:   Mon May 5 18:47:59 2025 -0500

    Refactor chat command and improve user experience
    
    - Simplified the chat command by removing advanced options and streamlining the interaction process.
    - Updated command prompts and help messages to enhance clarity and usability.
    - Improved logging and error messages for better debugging and user feedback.
    - Added a default chat mode when no arguments are provided.

commit 9f3748e6052ead1b877b10c63fe46b209c128a30
Author: Oz <ozcodx@gmail.com>
Date:   Wed Apr 9 16:41:07 2025 -0500

    Enhance configuration and documentation: add new personality and update README
    
    - Added a new 'sexy' personality to the configuration.
    - Updated README.md to include detailed sections on chat interface, personalities, and available commands.
    - Improved clarity in usage instructions and configuration examples.

commit 40d7325c9f51951fbb4a89ec905d71b92777425e
Author: Oz <ozcodx@gmail.com>
Date:   Wed Apr 9 00:07:51 2025 -0500

    Update project structure: add main application file and initial implementation
    
    - Introduced main application file with basic functionality.
    - Organized project files for better clarity and maintainability.

commit cf8b24e3f1845256c9f2eea6d3f6370b2de46ac5
Author: Oz <ozcodx@gmail.com>
Date:   Tue Apr 8 23:41:58 2025 -0500

    Add initial project files: .gitignore, README.md, and requirements.txt
    
    - Created .gitignore to exclude unnecessary files and directories.
    - Added README.md with project description, features, installation instructions, and usage guidelines.
    - Included requirements.txt listing necessary dependencies for the project.
