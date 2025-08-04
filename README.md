# LeetCode Random Question Generator

A desktop application that generates random coding problems from LeetCode's Top 150 Interview Questions to help with interview preparation.

## Features

- Generate 1-10 random questions from 150 curated interview problems
- Filter questions by difficulty (Easy, Medium, Hard, or All)
- Dark theme interface for comfortable viewing
- Complete problem descriptions with examples and constraints
- Both GUI and command-line versions available

## Requirements

- Python 3.7 or higher
- pandas
- requests
- beautifulsoup4
- tkinter (usually included with Python)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/RishabhWDB/DSA-Question-Generator.git
   cd DSA-Question-Generator
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### GUI Version (Recommended)
```
python leetcode_gui_enhanced.py
```

### Command Line Version
```
python random_leetcode_generator.py [number_of_questions]
```

## How to Use

1. Run the application
2. Select the number of questions you want (1-10)
3. Choose difficulty filter if desired
4. Click "Generate Questions" or run the command
5. Practice solving the generated problems

## Question Database

The application includes 150 questions from LeetCode's most frequently asked interview problems:

- 40 Easy questions
- 92 Medium questions  
- 18 Hard questions

Topics covered include arrays, strings, linked lists, trees, dynamic programming, graphs, and more.

## File Structure

```
DSA-Question-Generator/
├── leetcode_gui_enhanced.py          # Main GUI application
├── leetcode_top_interview_150.csv    # Question database
├── random_leetcode_generator.py      # Command-line version
├── requirements.txt                  # Dependencies
└── README.md                         # This file
```

## Troubleshooting

**"No module named 'tkinter'"**
- Windows: Reinstall Python with "tcl/tk and IDLE" option checked
- Ubuntu/Debian: `sudo apt-get install python3-tk`
- macOS: `brew install python-tk`

**"CSV file not found"**
- Ensure `leetcode_top_interview_150.csv` is in the same directory as the Python files

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License

## Contact

GitHub: https://github.com/RishabhWDB
