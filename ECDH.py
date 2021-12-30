# Raz Mor 315029264
# Oran Algresy 313205163
from tinyec import registry
import tkinter as tk
from PIL import Image, ImageTk
import secrets
from sympy import isprime
import random


root = tk.Tk()
WIDTH = 700
HEIGHT = 650
root.geometry(str(WIDTH)+'x'+str(HEIGHT))
root.resizable(width=False, height=False)
root.title("Elliptic Curve Diffie-Hellman")
root.wm_iconbitmap('./data/icon.ico')


def choose_prime(size):
    start = int("1"+"0"*(size-1))+1
    stop = int("9"*size)
    return random.sample([potencialP for potencialP in range(
        start, stop, 2) if isprime(potencialP)], 1)[0]


def compress(pubKey):
    return hex(pubKey.x) + hex(pubKey.y % 2)[2:]


alice_private_key = tk.StringVar()
alice_private_key.set("")

alice_public_key = tk.StringVar()
alice_public_key.set("")

alice_shared_key = tk.StringVar()
alice_shared_key.set("")

bob_private_key = tk.StringVar()
bob_private_key.set("")

bob_public_key = tk.StringVar()
bob_public_key.set("")

bob_shared_key = tk.StringVar()
bob_shared_key.set("")


def key_generator():

    alice_entry = tk.Entry()
    alice_entry.place(x=128+40, y=210)

    bob_entry = tk.Entry()
    bob_entry.place(x=128+40, y=HEIGHT//2+200)

    curve = registry.get_curve('brainpoolP256r1')

    prime = choose_prime(3)

    alicePrivKey = secrets.randbelow(curve.field.n)
    alicePubKey = alicePrivKey * curve.g

    bobPrivKey = secrets.randbelow(curve.field.n)
    bobPubKey = bobPrivKey * curve.g

    def alice_rev_hide():
        if alice_private_key.get() == '*'*len(str(alicePrivKey)):
            alice_private_key.set(str(alicePrivKey))
        else:
            alice_private_key.set('*'*len(str(alicePrivKey)))

    def bob_rev_hide():
        if bob_private_key.get() == '*'*len(str(bobPrivKey)):
            bob_private_key.set(str(bobPrivKey))
        else:
            bob_private_key.set('*'*len(str(bobPrivKey)))

    def encription(src, key, sender):
        dst = ""
        if sender == "alice":
            for c in src:
                dst += chr(ord(c)+int(str(key)[:3]))
            alice_entry.delete(0, "end")
            alice_entry.insert(0, dst)
        else:
            for c in src:
                dst += chr(ord(c)+int(str(key)[:3]))
            bob_entry.delete(0, "end")
            bob_entry.insert(0, dst)

    def decription(src, key, sender):
        dst = ""
        if sender == "alice":
            for c in src:
                dst += chr(ord(c)-int(str(key)[:3]))
            alice_entry.delete(0, "end")
            alice_entry.insert(0, dst)
        else:
            for c in src:
                dst += chr(ord(c)-int(str(key)[:3]))
            bob_entry.delete(0, "end")
            bob_entry.insert(0, dst)

    def send(sender):
        if sender == "alice":
            bob_entry.delete(0, "end")
            bob_entry.insert(0, alice_entry.get())
            alice_entry.delete(0, "end")
        else:
            alice_entry.delete(0, "end")
            alice_entry.insert(0, bob_entry.get())
            bob_entry.delete(0, "end")

    alice_enc_btn = tk.Button(root, text="Encrypt", command=lambda: encription(
        alice_entry.get(), int(compress(aliceSharedKey), 16), "alice"))
    alice_enc_btn.place(x=40, y=190, w=100)
    alice_dec_btn = tk.Button(root, text="Decrypt", command=lambda: decription(
        alice_entry.get(), int(compress(aliceSharedKey), 16), "alice"))
    alice_dec_btn.place(x=40, y=220, w=100)
    alice_send_btn = tk.Button(
        root, text="Send", command=lambda: send("alice"))
    alice_send_btn.place(x=128+180, y=206)
    alice_clear_btn = tk.Button(
        root, text="Clear", command=lambda: alice_entry.delete(0, "end"))
    alice_clear_btn.place(x=128+40, y=235)

    bob_enc_btn = tk.Button(root, text="Encrypt", command=lambda: encription(
        bob_entry.get(), int(compress(bobSharedKey), 16), "bob"))
    bob_enc_btn.place(x=40, y=HEIGHT//2+180, w=100)
    bob_dec_btn = tk.Button(root, text="Decrypt", command=lambda: decription(
        bob_entry.get(), int(compress(bobSharedKey), 16), "bob"))
    bob_dec_btn.place(x=40, y=HEIGHT//2+210, w=100)
    bob_send_btn = tk.Button(
        root, text="Send", command=lambda: send("bob"))
    bob_send_btn.place(x=128+180, y=HEIGHT//2+196)
    bob_clear_btn = tk.Button(
        root, text="Clear", command=lambda: bob_entry.delete(0, "end"))
    bob_clear_btn.place(x=128+40, y=HEIGHT//2+225)

    alice_public_key.set(compress(alicePubKey))
    alice_private_key.set('*'*len(str(alicePrivKey)))
    a_rev_btn = tk.Button(root, text="Reveal/Hide", command=alice_rev_hide)
    a_rev_btn.place(x=128//2-27, y=128, width=100)

    bob_public_key.set(compress(bobPubKey))
    bob_private_key.set('*'*len(str(bobPrivKey)))
    b_rev_btn = tk.Button(root, text="Reveal/Hide", command=bob_rev_hide)
    b_rev_btn.place(x=128//2-27, y=HEIGHT//2-20+128, width=100)

    aliceSharedKey = alicePrivKey * bobPubKey
    aliceSharedKey.x %= prime
    aliceSharedKey.y %= prime
    print(aliceSharedKey)
    alice_shared_key.set(compress(aliceSharedKey))

    bobSharedKey = bobPrivKey * alicePubKey
    bobSharedKey.x %= prime
    bobSharedKey.y %= prime
    print(bobSharedKey)
    bob_shared_key.set(compress(bobSharedKey))


alice_img = Image.open("./data/Alice.png")
alice = ImageTk.PhotoImage(alice_img)
alice_label = tk.Label(image=alice)
alice_label.image = alice
alice_label.place(x=20, y=20)
alice_private_label = tk.Label(textvariable=alice_private_key)
alice_public_label = tk.Label(textvariable=alice_public_key)
alice_shared_label = tk.Label(textvariable=alice_shared_key)

tk.Label(text="private key: ").place(x=128+40, y=40)
alice_private_label.place(x=128+40, y=60)

tk.Label(text="public key: ").place(x=128+40, y=100)
alice_public_label.place(x=128+40, y=120)

tk.Label(text="Alice shared key: ").place(x=128+40, y=160)
alice_shared_label.place(x=128+40, y=180)

bob_img = Image.open("./data/Bob.png")
bob = ImageTk.PhotoImage(bob_img)
bob_label = tk.Label(image=bob)
bob_label.image = bob
bob_label.place(x=20, y=HEIGHT//2)
bob_private_label = tk.Label(textvariable=bob_private_key)
bob_public_label = tk.Label(textvariable=bob_public_key)
bob_shared_label = tk.Label(textvariable=bob_shared_key)


tk.Label(text="private key: ").place(x=128+40, y=HEIGHT//2+20)
bob_private_label.place(x=128+40, y=HEIGHT//2+40)

tk.Label(text="public key: ").place(x=128+40, y=HEIGHT//2+80)
bob_public_label.place(x=128+40, y=HEIGHT//2+100)

tk.Label(text="Bob shared key: ").place(x=128+40, y=HEIGHT//2+140)
bob_shared_label.place(x=128+40, y=HEIGHT//2+160)

key_genBtn = tk.Button(root, text="Generate Keys", command=key_generator)
key_genBtn.place(x=WIDTH//2-100, y=HEIGHT-50, width=200)

root.mainloop()
