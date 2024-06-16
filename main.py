import tkinter as tk
from Blockchain.app import BlockchainApp  # Adjust this import based on your project structure

if __name__ == "__main__":
    root = tk.Tk()  # Initialize the main Tkinter window
    app = BlockchainApp(root)  # Create an instance of BlockchainApp with the root window
    root.mainloop()  # Start the Tkinter main loop
