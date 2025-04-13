import tkinter as tk
from tkinter import ttk, messagebox

class CipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Kriptografi")
        self.root.geometry("600x400")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Notebook untuk tab Encode/Decode
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Frame Encode
        self.encode_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.encode_frame, text='Encode')
        self.create_encode_widgets()
        
        # Frame Decode
        self.decode_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.decode_frame, text='Decode')
        self.create_decode_widgets()
    
    def create_encode_widgets(self):
        # Pilihan Cipher
        ttk.Label(self.encode_frame, text="Pilih Metode:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.encode_cipher = ttk.Combobox(self.encode_frame, values=["Caesar Cipher", "Vigenere Cipher"])
        self.encode_cipher.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.encode_cipher.current(0)
        
        # Input Plain Text
        ttk.Label(self.encode_frame, text="Plain Text:").grid(row=1, column=0, padx=5, pady=5, sticky='nw')
        self.encode_plain_text = tk.Text(self.encode_frame, height=5, width=50)
        self.encode_plain_text.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        # Input Key/Shift
        self.encode_key_label = ttk.Label(self.encode_frame, text="Shift (angka):")
        self.encode_key_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.encode_key = ttk.Entry(self.encode_frame)
        self.encode_key.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        
        # Tombol Encode
        ttk.Button(self.encode_frame, text="Encode", command=self.encode_text).grid(row=3, column=1, padx=5, pady=10, sticky='e')
        
        # Hasil Encode
        ttk.Label(self.encode_frame, text="Encoded Text:").grid(row=4, column=0, padx=5, pady=5, sticky='nw')
        self.encode_result = tk.Text(self.encode_frame, height=5, width=50, state='disabled')
        self.encode_result.grid(row=4, column=1, padx=5, pady=5, sticky='ew')
        
        # Bind combobox change
        self.encode_cipher.bind("<<ComboboxSelected>>", self.update_encode_key_label)
    
    def create_decode_widgets(self):
        # Pilihan Cipher
        ttk.Label(self.decode_frame, text="Pilih Metode:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.decode_cipher = ttk.Combobox(self.decode_frame, values=["Caesar Cipher", "Vigenere Cipher"])
        self.decode_cipher.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.decode_cipher.current(0)
        
        # Input Encoded Text
        ttk.Label(self.decode_frame, text="Encoded Text:").grid(row=1, column=0, padx=5, pady=5, sticky='nw')
        self.decode_encoded_text = tk.Text(self.decode_frame, height=5, width=50)
        self.decode_encoded_text.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        # Input Key/Shift
        self.decode_key_label = ttk.Label(self.decode_frame, text="Shift (angka):")
        self.decode_key_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.decode_key = ttk.Entry(self.decode_frame)
        self.decode_key.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        
        # Tombol Decode
        ttk.Button(self.decode_frame, text="Decode", command=self.decode_text).grid(row=3, column=1, padx=5, pady=10, sticky='e')
        
        # Hasil Decode
        ttk.Label(self.decode_frame, text="Decoded Text:").grid(row=4, column=0, padx=5, pady=5, sticky='nw')
        self.decode_result = tk.Text(self.decode_frame, height=5, width=50, state='disabled')
        self.decode_result.grid(row=4, column=1, padx=5, pady=5, sticky='ew')
        
        # Bind combobox change
        self.decode_cipher.bind("<<ComboboxSelected>>", self.update_decode_key_label)
    
    def update_encode_key_label(self, event=None):
        cipher = self.encode_cipher.get()
        if cipher == "Caesar Cipher":
            self.encode_key_label.config(text="Shift (angka):")
        else:
            self.encode_key_label.config(text="Kunci (huruf):")
    
    def update_decode_key_label(self, event=None):
        cipher = self.decode_cipher.get()
        if cipher == "Caesar Cipher":
            self.decode_key_label.config(text="Shift (angka):")
        else:
            self.decode_key_label.config(text="Kunci (huruf):")
    
    def encode_text(self):
        cipher = self.encode_cipher.get()
        plain_text = self.encode_plain_text.get("1.0", "end-1c")
        key = self.encode_key.get()
        
        if not plain_text:
            messagebox.showerror("Error", "Masukkan plain text terlebih dahulu!")
            return
        
        if not key:
            messagebox.showerror("Error", "Masukkan key/shift terlebih dahulu!")
            return
        
        try:
            if cipher == "Caesar Cipher":
                shift = int(key)
                result = self.caesar_encrypt(plain_text, shift)
            else:
                # Validasi kunci hanya huruf untuk Vigenere
                if not key.isalpha():
                    messagebox.showerror("Error", "Kunci Vigenere harus huruf saja!")
                    return
                result = self.vigenere_encrypt(plain_text, key)
            
            self.encode_result.config(state='normal')
            self.encode_result.delete("1.0", "end")
            self.encode_result.insert("1.0", result)
            self.encode_result.config(state='disabled')
        except ValueError:
            messagebox.showerror("Error", "Shift harus angka untuk Caesar Cipher!")
    
    def decode_text(self):
        cipher = self.decode_cipher.get()
        encoded_text = self.decode_encoded_text.get("1.0", "end-1c")
        key = self.decode_key.get()
        
        if not encoded_text:
            messagebox.showerror("Error", "Masukkan encoded text terlebih dahulu!")
            return
        
        if not key:
            messagebox.showerror("Error", "Masukkan key/shift terlebih dahulu!")
            return
        
        try:
            if cipher == "Caesar Cipher":
                shift = int(key)
                result = self.caesar_decrypt(encoded_text, shift)
            else:
                # Validasi kunci hanya huruf untuk Vigenere
                if not key.isalpha():
                    messagebox.showerror("Error", "Kunci Vigenere harus huruf saja!")
                    return
                result = self.vigenere_decrypt(encoded_text, key)
            
            self.decode_result.config(state='normal')
            self.decode_result.delete("1.0", "end")
            self.decode_result.insert("1.0", result)
            self.decode_result.config(state='disabled')
        except ValueError:
            messagebox.showerror("Error", "Shift harus angka untuk Caesar Cipher!")
    
    # Caesar Cipher Functions
    def caesar_encrypt(self, plain_text, shift):
        encrypted_text = ""
        for char in plain_text:
            if char.isalpha():
                shift_amount = shift % 26
                if char.islower():
                    encrypted_char = chr(((ord(char) - ord('a') + shift_amount) % 26) + ord('a'))
                else:
                    encrypted_char = chr(((ord(char) - ord('A') + shift_amount) % 26) + ord('A'))
                encrypted_text += encrypted_char
            else:
                encrypted_text += char
        return encrypted_text
    
    def caesar_decrypt(self, encrypted_text, shift):
        return self.caesar_encrypt(encrypted_text, -shift)
    
    # Vigenere Cipher Functions
    def vigenere_encrypt(self, plain_text, key):
        encrypted_text = ""
        key_length = len(key)
        key_index = 0
        
        for char in plain_text:
            if char.isalpha():
                key_char = key[key_index % key_length]
                key_shift = ord(key_char.lower()) - ord('a')
                
                if char.islower():
                    encrypted_char = chr(((ord(char) - ord('a') + key_shift) % 26) + ord('a'))
                else:
                    encrypted_char = chr(((ord(char) - ord('A') + key_shift) % 26) + ord('A'))
                
                encrypted_text += encrypted_char
                key_index += 1
            else:
                encrypted_text += char
        return encrypted_text
    
    def vigenere_decrypt(self, encrypted_text, key):
        decrypted_text = ""
        key_length = len(key)
        key_index = 0
        
        for char in encrypted_text:
            if char.isalpha():
                key_char = key[key_index % key_length]
                key_shift = ord(key_char.lower()) - ord('a')
                
                if char.islower():
                    decrypted_char = chr(((ord(char) - ord('a') - key_shift) % 26) + ord('a'))
                else:
                    decrypted_char = chr(((ord(char) - ord('A') - key_shift) % 26) + ord('A'))
                
                decrypted_text += decrypted_char
                key_index += 1
            else:
                decrypted_text += char
        return decrypted_text

if __name__ == "__main__":
    root = tk.Tk()
    app = CipherApp(root)
    root.mainloop()