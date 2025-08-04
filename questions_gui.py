import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, Frame, Label, Message
import pandas as pd
import random
import os
import re

class ModernLeetCodeApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()

        # Load data
        self.df = None
        self.load_data()

        # Setup styles
        self.setup_styles()

        # Create GUI
        self.create_widgets()

    def setup_window(self):
        """Configure main window with high-DPI support"""
        self.root.title("LeetCode Random Question Generator")
        self.root.geometry("1000x750")
        self.root.configure(bg='#0d1117')

        # High-DPI support for Windows
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass

        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.root.winfo_screenheight() // 2) - (750 // 2)
        self.root.geometry(f"1000x750+{x}+{y}")

    def setup_styles(self):
        """Configure ttk styles for dark theme"""
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configure styles
        self.style.configure('Title.TLabel', 
                           background='#0d1117', 
                           foreground='#58a6ff', 
                           font=('Segoe UI', 24, 'bold'))

        self.style.configure('Control.TLabel', 
                           background='#0d1117', 
                           foreground='#f0f6fc', 
                           font=('Segoe UI', 12))

        self.style.configure('Modern.TButton',
                           background='#238636',
                           foreground='#ffffff',
                           font=('Segoe UI', 12, 'bold'),
                           padding=(20, 10))

        self.style.map('Modern.TButton',
                      background=[('active', '#2ea043'),
                                ('pressed', '#1a7f37')])

        self.style.configure('Modern.TCombobox',
                           fieldbackground='#21262d',
                           background='#21262d',
                           foreground='#f0f6fc',
                           font=('Segoe UI', 11))

    def load_data(self):
        """Load the CSV file with questions"""
        csv_file = 'leetcode_top_interview_150.csv'
        if os.path.exists(csv_file):
            try:
                self.df = pd.read_csv(csv_file)
            except Exception as e:
                messagebox.showerror("Error", f"Error loading CSV: {str(e)}")
        else:
            messagebox.showerror("File Not Found", 
                               "CSV file 'leetcode_top_interview_150.csv' not found!")

    def create_widgets(self):
        """Create all GUI widgets"""

        # Header Section
        header_frame = Frame(self.root, bg='#161b22', height=100)
        header_frame.pack(fill='x', padx=20, pady=20)
        header_frame.pack_propagate(False)

        title_label = Label(header_frame,
                           text="🎯 LeetCode Random Question Generator",
                           bg='#161b22',
                           fg='#58a6ff',
                           font=('Segoe UI', 24, 'bold'))
        title_label.pack(expand=True)

        subtitle_label = Label(header_frame,
                              text="Practice coding problems with randomized selection",
                              bg='#161b22',
                              fg='#8b949e',
                              font=('Segoe UI', 12))
        subtitle_label.pack()

        # Control Panel
        control_frame = Frame(self.root, bg='#0d1117', height=80)
        control_frame.pack(fill='x', padx=20, pady=10)
        control_frame.pack_propagate(False)

        # Left side controls
        left_controls = Frame(control_frame, bg='#0d1117')
        left_controls.pack(side='left', expand=True, fill='both')

        # Questions count
        questions_frame = Frame(left_controls, bg='#0d1117')
        questions_frame.pack(side='left', padx=10)

        Label(questions_frame, 
              text="Questions:", 
              bg='#0d1117', 
              fg='#f0f6fc',
              font=('Segoe UI', 12, 'bold')).pack(side='top')

        self.num_questions = tk.StringVar(value="2")
        spinbox = tk.Spinbox(questions_frame,
                            from_=1, to=10,
                            width=5,
                            textvariable=self.num_questions,
                            font=('Segoe UI', 12),
                            bg='#21262d',
                            fg='#f0f6fc',
                            buttonbackground='#30363d',
                            insertbackground='#f0f6fc',
                            relief='flat',
                            bd=1)
        spinbox.pack(side='top', pady=5)

        # Difficulty filter
        difficulty_frame = Frame(left_controls, bg='#0d1117')
        difficulty_frame.pack(side='left', padx=20)

        Label(difficulty_frame,
              text="Difficulty:",
              bg='#0d1117',
              fg='#f0f6fc',
              font=('Segoe UI', 12, 'bold')).pack(side='top')

        self.difficulty_filter = tk.StringVar(value="All")
        combo = ttk.Combobox(difficulty_frame,
                            textvariable=self.difficulty_filter,
                            values=["All", "Easy", "Medium", "Hard"],
                            width=12,
                            style='Modern.TCombobox',
                            font=('Segoe UI', 12))
        combo.pack(side='top', pady=5)
        combo.state(['readonly'])

        # Generate button
        generate_btn = tk.Button(control_frame,
                               text="Generate Questions",
                               command=self.generate_questions,
                               bg='#238636',
                               fg='#ffffff',
                               font=('Segoe UI', 14, 'bold'),
                               relief='flat',
                               bd=0,
                               padx=30,
                               pady=12,
                               cursor='hand2')
        generate_btn.pack(side='right', padx=20)

        # Hover effects for button
        def on_enter(e):
            generate_btn.config(bg='#2ea043')
        def on_leave(e):
            generate_btn.config(bg='#238636')

        generate_btn.bind("<Enter>", on_enter)
        generate_btn.bind("<Leave>", on_leave)

        # Results area with custom scrollbar
        results_container = Frame(self.root, bg='#0d1117')
        results_container.pack(fill='both', expand=True, padx=20, pady=10)

        # Canvas for scrollable content
        self.canvas = tk.Canvas(results_container, bg='#0d1117', highlightthickness=0)
        scrollbar = ttk.Scrollbar(results_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg='#0d1117')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mousewheel scrolling
        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.canvas.bind("<MouseWheel>", on_mousewheel)

        # Status bar
        status_frame = Frame(self.root, bg='#161b22', height=40)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)

        self.status_label = Label(status_frame,
                                 text="Ready to generate questions",
                                 bg='#161b22',
                                 fg='#8b949e',
                                 font=('Segoe UI', 11))
        self.status_label.pack(side='left', padx=20, pady=10)

        # Database info
        if self.df is not None:
            db_info = f"Database: {len(self.df)} questions loaded"
            db_label = Label(status_frame,
                           text=db_info,
                           bg='#161b22',
                           fg='#8b949e',
                           font=('Segoe UI', 11))
            db_label.pack(side='right', padx=20, pady=10)

        # Show welcome message
        self.show_welcome()

    def show_welcome(self):
        """Display welcome message"""
        welcome_frame = Frame(self.scrollable_frame, bg='#0d1117')
        welcome_frame.pack(fill='x', padx=20, pady=50)

        # Welcome card
        card = Frame(welcome_frame, bg='#161b22', relief='solid', bd=1)
        card.pack(anchor='center', padx=50, pady=20)

        Label(card,
              text="🚀 Welcome to LeetCode Practice!",
              bg='#161b22',
              fg='#58a6ff',
              font=('Segoe UI', 20, 'bold')).pack(pady=20)

        instructions = [
            "📊 Select the number of questions you want to practice",
            "🎯 Choose difficulty level (All, Easy, Medium, Hard)",
            "⚡ Click 'Generate Questions' to get random problems",
            "📚 Each question includes full problem description"
        ]

        for instruction in instructions:
            Label(card,
                  text=instruction,
                  bg='#161b22',
                  fg='#f0f6fc',
                  font=('Segoe UI', 12),
                  justify='left').pack(anchor='w', padx=30, pady=5)

        if self.df is not None:
            stats_text = f"📈 Database loaded: {len(self.df)} questions available"
            easy = len(self.df[self.df['Difficulty'] == 'Easy'])
            medium = len(self.df[self.df['Difficulty'] == 'Medium'])
            hard = len(self.df[self.df['Difficulty'] == 'Hard'])
            stats_text += f" (Easy: {easy}, Medium: {medium}, Hard: {hard})"

            Label(card,
                  text=stats_text,
                  bg='#161b22',
                  fg='#39d353',
                  font=('Segoe UI', 11)).pack(pady=15)

        Label(card,
              text="Ready when you are! 💪",
              bg='#161b22',
              fg='#8b949e',
              font=('Segoe UI', 12, 'italic')).pack(pady=(10, 20))

    def clear_results(self):
        """Clear the results area"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def create_question_card(self, question, question_num):
        """Create a beautiful question card"""

        # Main card frame
        card_frame = Frame(self.scrollable_frame, bg='#0d1117')
        card_frame.pack(fill='x', padx=20, pady=15)

        # Question card
        card = Frame(card_frame, bg='#161b22', relief='solid', bd=1)
        card.pack(fill='x', padx=10)

        # Header section
        header = Frame(card, bg='#21262d', height=60)
        header.pack(fill='x', padx=2, pady=2)
        header.pack_propagate(False)

        # Question number and ID
        Label(header,
              text=f"QUESTION {question_num}",
              bg='#21262d',
              fg='#58a6ff',
              font=('Segoe UI', 16, 'bold')).pack(pady=10)

        Label(header,
              text=f"Problem ID: {question['Id']}",
              bg='#21262d',
              fg='#8b949e',
              font=('Segoe UI', 10)).pack()

        # Title section
        title_frame = Frame(card, bg='#161b22')
        title_frame.pack(fill='x', padx=20, pady=15)

        Label(title_frame,
              text=question['Title'],
              bg='#161b22',
              fg='#f0f6fc',
              font=('Segoe UI', 18, 'bold'),
              wraplength=800,
              justify='center').pack()

        # Difficulty badge
        difficulty = question['Difficulty']
        diff_colors = {
            'Easy': '#39d353',
            'Medium': '#d29922', 
            'Hard': '#f85149'
        }

        diff_frame = Frame(card, bg='#161b22')
        diff_frame.pack(pady=10)

        diff_badge = Label(diff_frame,
                          text=f"● {difficulty.upper()}",
                          bg='#161b22',
                          fg=diff_colors.get(difficulty, '#8b949e'),
                          font=('Segoe UI', 12, 'bold'))
        diff_badge.pack()

        # Description section
        desc_frame = Frame(card, bg='#161b22')
        desc_frame.pack(fill='x', padx=20, pady=15)

        Label(desc_frame,
              text="📋 Problem Description",
              bg='#161b22',
              fg='#58a6ff',
              font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(0, 10))

        # Description text area
        desc_text = tk.Text(desc_frame,
                           wrap='word',
                           height=12,
                           bg='#0d1117',
                           fg='#f0f6fc',
                           font=('Consolas', 11),
                           relief='solid',
                           bd=1,
                           padx=15,
                           pady=15,
                           state='normal')
        desc_text.pack(fill='x')

        # Clean and format description
        description = str(question['Description'])
        description = re.sub(r'<[^>]+>', '', description)
        description = re.sub(r'\s+', ' ', description).strip()

        # Add formatted text
        desc_text.insert('1.0', description)
        desc_text.config(state='disabled')

        # Add some spacing at the bottom
        Frame(card, bg='#161b22', height=10).pack()

    def generate_questions(self):
        """Generate and display random questions"""
        if self.df is None:
            messagebox.showerror("Error", "No data loaded")
            return

        try:
            num = int(self.num_questions.get())
            difficulty = self.difficulty_filter.get()

            # Filter by difficulty
            filtered_df = self.df.copy()
            if difficulty != "All":
                filtered_df = filtered_df[filtered_df['Difficulty'] == difficulty]

            if len(filtered_df) == 0:
                messagebox.showwarning("No Questions", f"No questions found for {difficulty}")
                return

            if num > len(filtered_df):
                num = len(filtered_df)
                messagebox.showinfo("Info", f"Only {num} questions available")

            # Get random questions
            questions = filtered_df.sample(n=num)

            # Clear previous results
            self.clear_results()

            # Header
            header_frame = Frame(self.scrollable_frame, bg='#0d1117')
            header_frame.pack(fill='x', padx=20, pady=20)

            Label(header_frame,
                  text=f"🎯 Generated {num} Random Question{'s' if num != 1 else ''}",
                  bg='#0d1117',
                  fg='#39d353',
                  font=('Segoe UI', 20, 'bold')).pack()

            Label(header_frame,
                  text=f"Difficulty Filter: {difficulty}",
                  bg='#0d1117',
                  fg='#8b949e',
                  font=('Segoe UI', 12)).pack(pady=5)

            # Create question cards
            for i, (_, question) in enumerate(questions.iterrows(), 1):
                self.create_question_card(question, i)

            # Footer
            footer_frame = Frame(self.scrollable_frame, bg='#0d1117')
            footer_frame.pack(fill='x', padx=20, pady=30)

            Label(footer_frame,
                  text="🎉 Good luck with your practice!",
                  bg='#0d1117',
                  fg='#58a6ff',
                  font=('Segoe UI', 14, 'bold')).pack()

            Label(footer_frame,
                  text="Generate again for different questions",
                  bg='#0d1117',
                  fg='#8b949e',
                  font=('Segoe UI', 11)).pack(pady=5)

            # Update status
            self.status_label.config(text=f"Generated {num} questions successfully!")

            # Scroll to top
            self.canvas.yview_moveto(0)

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = ModernLeetCodeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
