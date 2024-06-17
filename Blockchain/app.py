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
        tk.Button(self.root, text="Recover Wallet", command=self.recover_wallet).pack(pady=10)

    def create_wallet(self):
        self.wallet = Wallet(self.blockchain)
        #messagebox.showinfo("Wallet Created", f"Your new wallet address: {self.wallet.get_address()}")
        print(f'your seed-phras: {self.wallet.seed_phrase}\n')
        print(f'your addres: {self.swallet.get_address()}\n')
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

    def wallet_menu(self):
        self.clear_window()
        
        tk.Label(self.root, text=f"Address: {self.wallet.get_address()}", font=("Arial", 12, "bold")).pack(pady=5)
        
        tk.Label(self.root, text=f"Balance: {self.blockchain.get_balance_of_address(self.wallet.get_address())}").pack(pady=15)
        
        tk.Button(self.root, text="Send Transaction", command=self.send_transaction).pack(pady=10)
        tk.Button(self.root, text="Mine Block", command=self.mine_block).pack(pady=10)
        tk.Button(self.root, text="Show Seed", command=self.show_seed).pack(pady=10)
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
        tk.Button(seed_window, text="copy seed-phrase", command=self.copy(self.wallet.seed_phrase)).pack(pady=5)
        
   
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

