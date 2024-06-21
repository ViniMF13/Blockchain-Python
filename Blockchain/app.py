import tkinter as tk
from tkinter import simpledialog, messagebox
from .wallet import Wallet
from .blockchain import Blockchain
from .transaction import Transaction
from .node import Node

class BlockchainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blockchain")
        self.root.geometry("600x400")

        self.blockchain = Blockchain()
        self.blockchain.load_from_file('blockchain.json')

        self.node = Node(self.blockchain)
        self.wallet = None
        
        self.main_menu()

        # Bind the on_closing method to the window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def main_menu(self):
        self.clear_window()
        
        tk.Button(self.root, text="Create New Wallet", command=self.create_wallet).pack(pady=10)
        tk.Button(self.root, text="Recover Wallet", command= self.recover_wallet).pack(pady=10)

    def create_wallet(self):
        self.wallet = Wallet(self.blockchain)
        #messagebox.showinfo("Wallet Created", f"Your new wallet address: {self.wallet.get_address()}")
        print(f'your seed-phras: {self.wallet.seed_phrase}\n')
        print(f'your addres: {self.wallet.get_address()}\n')
        self.blockchain.receive_airdrop(self.wallet.get_address())
        messagebox.showinfo("Airdrop Received", "you received 1000 POO. Mine the last block to update balance")

        self.wallet_menu()

    def recover_wallet(self):
        seed_phrase = simpledialog.askstring("Seed Phrase", "Enter your seed phrase:")
        if seed_phrase:
            self.wallet = Wallet(self.blockchain, seed_phrase=seed_phrase)
            #messagebox.showinfo("Wallet Recovered", f"address: {self.wallet.get_address()}")
            print(self.wallet.seed_phrase)
            print(self.wallet.get_address())
            self.wallet_menu()
    
    def blockScan(self):
        # Create a new window for block scan
        block_window = tk.Toplevel(self.root)
        block_window.title("Block Scan")

        # Create a Text widget with a Scrollbar in the new window
        text_frame = tk.Frame(block_window)
        text_frame.pack(fill=tk.BOTH, expand=True)

        text_area = tk.Text(text_frame, wrap=tk.WORD)
        scrollbar = tk.Scrollbar(text_frame, command=text_area.yview)
        text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Fetch the blocks from the blockchain
        blocks = self.blockchain.chain  # Assuming `chain` is a list of blocks in your Blockchain class

        # Format and display the blocks
        for block in blocks:
            block_text = f"Block #{block.index}\n"
            block_text += f"Timestamp: {block.timestamp}\n"
            block_text += f"Previous Hash: {block.previous_hash}\n"
            block_text += f"Hash: {block.hash}\n"
            block_text += f"Transactions: {len(block.transactions)}\n"
            for tx in block.transactions:
                block_text += f"  Sender: {tx.sender}\n"
                block_text += f"  Receiver: {tx.receiver}\n"
                block_text += f"  Amount: {tx.amount}\n"
                block_text += "-" * 40 + "\n"
            block_text += "=" * 50 + "\n\n"
            text_area.insert(tk.END, block_text)

        # Run the new window's main loop
        block_window.mainloop()

    def wallet_menu(self):
        self.clear_window()
        
        tk.Label(self.root, text=f"Address: {self.wallet.get_address()}", font=("Arial", 12, "bold")).pack(pady=5)
        
        tk.Label(self.root, text=f"Balance: {self.blockchain.get_balance_of_address(self.wallet.get_address())}").pack(pady=15)
        
        tk.Button(self.root, text="Send Transaction", command=self.send_transaction).pack(pady=10)
        tk.Button(self.root, text="Mine Block", command=self.mine_block).pack(pady=10)
        tk.Button(self.root, text="Show Seed", command=self.show_seed).pack(pady=10)
        tk.Button(self.root, text="BlockScam", command=self.blockScan).pack(pady=10)
        tk.Button(self.root, text="LogOut", command=self.main_menu).pack(pady=10)

    def copy(self, message):
        self.root.clipboard_clear()
        self.root.clipboard_append(message)
        messagebox.showinfo("Copied", "message copied to clipboard!")

    def send_transaction(self):
        transaction_window = tk.Toplevel(self.root)
        transaction_window.title("Send Transaction")
        
        tk.Label(transaction_window, text="Receiver's Address:").pack(pady=5)
        receiver_entry = tk.Entry(transaction_window)
        receiver_entry.pack(pady=5)

        tk.Label(transaction_window, text="Amount:").pack(pady=5)
        amount_entry = tk.Entry(transaction_window)
        amount_entry.pack(pady=5)
        
        def sign_transaction():
            receiver = receiver_entry.get()
            try:
                amount = float(amount_entry.get())
                if self.blockchain.get_balance_of_address(self.wallet.get_address()) >= amount:
                    print("public key", self.wallet.public_key)
                    transaction = Transaction(self.wallet.public_key, self.wallet.get_address(), receiver, amount)
                    self.wallet.sign_transaction(transaction)
                    self.blockchain.pending_transactions.append(transaction)
                    messagebox.showinfo("Transaction Sent", f"{amount} POO sent to {receiver}")
                    transaction_window.destroy()
                else:
                    messagebox.showwarning("Transaction Failed", "Insufficient balance for this transaction.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid amount.")
        
        tk.Button(transaction_window, text="Sign Transaction", command=sign_transaction).pack(pady=5)
        tk.Button(transaction_window, text="Cancel", command=transaction_window.destroy).pack(pady=5)

    def mine_block(self):
        if self.blockchain.pending_transactions == []:
            messagebox.showinfo("no pending transactions to mine")
            raise("no pending transactions to mine")
        self.node.mine_pending_transactions(self.wallet.get_address())
        messagebox.showinfo("Block Mined", "A new block has been mined and added to the blockchain!")
        messagebox.showinfo("Rewards received", "You received a reward of 50 POO")
        self.wallet_menu()
    
    def show_seed(self):
        seed_window = tk.Toplevel(self.root)
        seed_window.title("Seed-phrase")
        
        tk.Label(seed_window, text="SEED-PHRASE:").pack(pady=5)
        tk.Label(seed_window, text={self.wallet.seed_phrase}).pack(pady=5)
        tk.Label(seed_window, text="THIS IS THE ONLY WAY TO RECOVERY YOUR WALLET!!! KEEP IT SAFE").pack(pady=5)
        tk.Button(seed_window, text="copy seed-phrase", command=lambda: self.copy(self.wallet.seed_phrase)).pack(pady=5)
        
   
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy() 

    def on_closing(self):
        # Save the blockchain data to a file
        self.blockchain.update_file('blockchain.json')
        self.root.destroy()        

if __name__ == "__main__":
    root = tk.Tk()
    app = BlockchainApp(root)
    root.mainloop()

