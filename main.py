import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from web3 import Web3
from eth_account import Account
import threading
import csv
import os
import webbrowser
from datetime import datetime

# == Alchemy Sepolia ==
ALCHEMY_URL = "https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY"
web3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))

wallet = None
recipient_addresses = []
current_transactions = []
log_file = "log.csv"

# == Print Safe ==
def safe_print_tx(address, tx_hash):
    try:
        print(f"📨 TX ke {address}: {tx_hash}")
    except UnicodeEncodeError:
        print(f"TX ke {address}: {tx_hash}")

# == Wallet ==
def import_wallet():
    global wallet
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not filepath:
        return
    try:
        Account.enable_unaudited_hdwallet_features()
        with open(filepath, "r") as file:
            seed_phrase = file.read().strip()
        wallet = Account.from_mnemonic(seed_phrase)
        messagebox.showinfo("Berhasil", f"Wallet diimport: {wallet.address}")
        update_balance_label()
    except Exception as e:
        messagebox.showerror("Error", f"Gagal import wallet: {e}")

def import_wallet_thread():
    threading.Thread(target=import_wallet).start()

# == Addresses ==
def import_addresses():
    global recipient_addresses
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not filepath:
        return
    try:
        addresses = []
        with open(filepath, "r") as file:
            for line in file:
                addr = line.strip()
                if addr and Web3.is_address(addr):
                    addresses.append(web3.to_checksum_address(addr))
                else:
                    print(f"Alamat tidak valid dilewati: {addr}")
        recipient_addresses = addresses
        update_address_listbox()
        messagebox.showinfo("Berhasil", f"Memuat {len(addresses)} alamat.")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal import addresses: {e}")

def import_addresses_thread():
    threading.Thread(target=import_addresses).start()

def clear_addresses():
    global recipient_addresses
    recipient_addresses = []
    update_address_listbox()
    messagebox.showinfo("Dibersihkan", "Daftar alamat telah dikosongkan.")

# == Balance ==
def update_balance_label():
    try:
        if wallet is None:
            balance_label.config(text="Saldo Sepolia: ...")
            return
        balance_wei = web3.eth.get_balance(wallet.address)
        balance_eth = Web3.from_wei(balance_wei, 'ether')
        balance_label.config(text=f"Saldo Sepolia: {balance_eth:.6f} ETH")
    except Exception as e:
        balance_label.config(text=f"Saldo tidak tersedia: {e}")

def update_balance_label_thread():
    threading.Thread(target=update_balance_label).start()

def update_address_listbox():
    address_listbox.delete(0, tk.END)
    for addr in recipient_addresses:
        address_listbox.insert(tk.END, addr)

# == Logging ==
def log_transaction(tx_data):
    file_exists = os.path.isfile(log_file)
    with open(log_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["No", "Address", "Amount", "Status", "Explorer URL"])
        writer.writerow([
            tx_data["no"],
            tx_data["address"],
            tx_data["amount"],
            tx_data["status"],
            tx_data["explorer_url"],
        ])

# == Send ETH ==
def send_eth():
    global current_transactions
    if wallet is None:
        messagebox.showerror("Error", "Import wallet terlebih dahulu.")
        return
    if not recipient_addresses:
        messagebox.showerror("Error", "Import address.txt terlebih dahulu.")
        return

    try:
        amount_per_address_eth = float(amount_entry.get())
        amount_per_address_wei = Web3.to_wei(amount_per_address_eth, 'ether')

        selected_fee = gas_fee_choice.get()
        block_data = web3.eth.fee_history(5, 'latest', [10, 50, 90])
        base_fee = block_data['baseFeePerGas'][-1]
        priority_fee = {
            "Rendah": int(block_data['reward'][-1][0]),
            "Pasar": int(block_data['reward'][-1][1]),
            "Agresif": int(block_data['reward'][-1][2])
        }.get(selected_fee, int(block_data['reward'][-1][1]))

        max_fee_per_gas = int(base_fee + priority_fee)
        gas_limit = int(gas_limit_entry.get())
        balance = web3.eth.get_balance(wallet.address)
        total_gas_cost = max_fee_per_gas * gas_limit * len(recipient_addresses)
        total_send_amount = amount_per_address_wei * len(recipient_addresses)

        if balance < (total_send_amount + total_gas_cost):
            messagebox.showerror("Error", "Saldo tidak cukup.")
            return

        nonce = web3.eth.get_transaction_count(wallet.address)
        current_transactions = []

        for i, address in enumerate(recipient_addresses):
            tx_nonce = nonce + i
            tx = {
                'nonce': tx_nonce,
                'to': web3.to_checksum_address(address),
                'value': amount_per_address_wei,
                'gas': gas_limit,
                'maxFeePerGas': max_fee_per_gas,
                'maxPriorityFeePerGas': priority_fee,
                'chainId': 11155111
            }
            try:
                signed_tx = wallet.sign_transaction(tx)
                tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction if hasattr(signed_tx, 'raw_transaction') else signed_tx.rawTransaction)
                tx_hash_hex = web3.to_hex(tx_hash)
                status = "⏳ Pending"
                explorer_url = f"https://sepolia.etherscan.io/tx/{tx_hash_hex}"
                tx_data = {
                    "no": i + 1,
                    "address": address,
                    "amount": amount_per_address_eth,
                    "status": status,
                    "explorer_url": explorer_url,
                }
                current_transactions.append({"tx_hash": tx_hash_hex, **tx_data})
                log_transaction(tx_data)
                safe_print_tx(address, tx_hash_hex)
            except Exception as e:
                print(f"Gagal TX ke {address}: {e}")

        messagebox.showinfo("Sukses", f"Kirim {amount_per_address_eth} ETH ke {len(recipient_addresses)} alamat selesai.")
        update_balance_label()
        update_transaction_status()

    except Exception as e:
        messagebox.showerror("Error", f"Gagal kirim: {e}")

def send_eth_thread():
    threading.Thread(target=send_eth).start()

# == Status Transaksi ==
def update_transaction_status():
    status_tree.delete(*status_tree.get_children())
    for tx in current_transactions:
        try:
            receipt = web3.eth.get_transaction_receipt(tx["tx_hash"])
            status = "✅ Berhasil" if receipt.status == 1 else "❌ Gagal"
        except:
            status = "⏳ Pending"
        explorer_url = tx["explorer_url"]
        status_tree.insert("", tk.END, values=(tx["no"], tx["address"], tx["amount"], status, explorer_url))
    root.after(5000, update_transaction_status)

def on_tree_double_click(event):
    item = status_tree.selection()
    if item:
        url = status_tree.item(item, "values")[4]
        if url:
            webbrowser.open(url)

def buka_explorer_tx_terakhir():
    if not current_transactions:
        messagebox.showinfo("Info", "Belum ada transaksi.")
        return
    last_tx = current_transactions[-1]
    webbrowser.open(last_tx["explorer_url"])

def on_exit():
    if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar?"):
        root.destroy()

# == GUI ==
root = tk.Tk()
root.title("Sepolia ETH Sender - Alchemy")
root.geometry("1048x631")
root.protocol("WM_DELETE_WINDOW", on_exit)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", rowheight=30, font=("Arial", 10))
style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

frame = ttk.Frame(root, padding=20)
frame.pack(fill=tk.BOTH, expand=True)

wallet_frame = ttk.LabelFrame(frame, text="Wallet")
wallet_frame.pack(fill=tk.X, pady=5)
wbtn = ttk.Frame(wallet_frame)
wbtn.pack(fill=tk.X)
ttk.Button(wbtn, text="📂 Import Wallet", command=import_wallet_thread, width=20).pack(side=tk.LEFT, padx=5)
ttk.Button(wbtn, text="⟳ Refresh Saldo", command=update_balance_label_thread, width=20).pack(side=tk.LEFT, padx=5)
balance_label = ttk.Label(wbtn, text="Saldo Sepolia: ...")
balance_label.pack(side=tk.LEFT, padx=20)

address_frame = ttk.LabelFrame(frame, text="Daftar Alamat")
address_frame.pack(fill=tk.X, pady=5)
a_btn = ttk.Frame(address_frame)
a_btn.pack(fill=tk.X)
ttk.Button(a_btn, text="📂 Import Addresses", command=import_addresses_thread, width=20).pack(side=tk.LEFT, padx=5)
ttk.Button(a_btn, text="🪟 Hapus Address", command=clear_addresses, width=20).pack(side=tk.LEFT, padx=5)

address_listbox = tk.Listbox(frame, height=5)
address_listbox.pack(fill=tk.X, padx=5, pady=5)

trans_frame = ttk.LabelFrame(frame, text="Transaksi")
trans_frame.pack(fill=tk.X, pady=5)

input_frame = ttk.Frame(trans_frame)
input_frame.pack(fill=tk.X)
ttk.Label(input_frame, text="Nominal ETH/alamat:").pack(side=tk.LEFT, padx=5)
amount_entry = ttk.Entry(input_frame, width=10)
amount_entry.insert(0, "0.001")
amount_entry.pack(side=tk.LEFT, padx=5)

ttk.Label(input_frame, text="Gas Limit:").pack(side=tk.LEFT, padx=5)
gas_limit_entry = ttk.Entry(input_frame, width=7)
gas_limit_entry.insert(0, "21000")
gas_limit_entry.pack(side=tk.LEFT, padx=5)

ttk.Label(input_frame, text="Gas Fee:").pack(side=tk.LEFT, padx=5)
gas_fee_choice = ttk.Combobox(input_frame, values=["Rendah", "Pasar", "Agresif"], width=10, state="readonly")
gas_fee_choice.set("Pasar")
gas_fee_choice.pack(side=tk.LEFT, padx=5)

btn_frame = ttk.Frame(trans_frame)
btn_frame.pack(fill=tk.X, pady=5)
ttk.Button(btn_frame, text="❌ Keluar", command=on_exit, width=25).pack(side=tk.RIGHT, padx=5)
ttk.Button(btn_frame, text="🔎 TX Explorer Terakhir", command=buka_explorer_tx_terakhir, width=25).pack(side=tk.RIGHT, padx=5)
ttk.Button(btn_frame, text="⬫ Kirim ETH", command=send_eth_thread, width=25).pack(side=tk.RIGHT, padx=5)

status_frame = ttk.LabelFrame(frame, text="📄 Status Transaksi (Double-Click URL):")
status_frame.pack(fill=tk.BOTH, expand=True, pady=5)

status_tree = ttk.Treeview(status_frame, columns=("No", "Address", "Amount", "Status", "Explorer URL"), show="headings")
for col in ("No", "Address", "Amount", "Status", "Explorer URL"):
    status_tree.heading(col, text=col)
    status_tree.column(col, width=120, anchor="center")
status_tree.pack(fill=tk.BOTH, expand=True)
status_tree.bind("<Double-1>", on_tree_double_click)

root.mainloop()