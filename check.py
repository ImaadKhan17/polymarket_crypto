import sqlite3
con = sqlite3.connect('data/database.db')

four_wallets = ['0x06e29649d128bd7af23e4d47b97d0026ac67b7d4', '0x3d1423f37ea3e2cb6fd75b185f723776659369d4', '0x555604b46ab2eba4145e39b93c8ccd9acc95d016', '0x7beb7e7181085bced3209fece0476c3ce2f0c930', '0x9b02387b9dad6f11f933a3698a16a2bbc95889df', '0xab84466637dfe3d7a75d6509a78b562d0964bc67', '0xacdfb12f805200f10786bf778169528d5509e322', '0xbc88174d698d1f47e36cc726c16eebaa25bd7e52', '0xcdf50112673487f236d3091b9f79bf0eb113e323', '0xd252241299fcf504dba59c92f3f7647998476139', '0xdc2f2f6fe9fc842ddc83a2f41785ed2ea453ad24', '0xe4ec08966c0bce9f0f35facf040bd3757d5434d2', '0xe5624812e65538dbe41142b28b98da7b1790eee0', '0xffa872fa93d0f8eea76c9ec21301bfd847b0182e']

for wallet in four_wallets:
    result = con.execute("SELECT COUNT(*) FROM trades WHERE wallet = ?", (wallet,)).fetchone()
    print(f"{wallet[:10]}... trades: {result[0]}")