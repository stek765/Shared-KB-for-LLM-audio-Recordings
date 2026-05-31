# Glossario Cross-Materia

Termini tecnici condivisi tra le materie. Aggiornato automaticamente da `/stek_transcribe`.

---

## Ethereum / Blockchain

- **Blockchain** — registro distribuito e immutabile; ogni blocco è crittograficamente collegato al precedente | vedi [[01_lezione-2]]
- **UTXO** (Unspent Transaction Output) — output di una transazione non ancora speso; rappresenta lo stato in Bitcoin | vedi [[01_lezione-2]]
- **Wallet** — gestore di chiavi pubbliche/private; non memorizza saldi, li deriva dalla blockchain | vedi [[01_lezione-2]]
- **Chiave privata** — segreto per firmare transazioni; equivale a un OTP bancario; se persa i fondi sono irrecuperabili | vedi [[01_lezione-2]]
- **Smart Contract** — programma eseguibile sulla blockchain Ethereum; immutabile dopo il deploy | vedi [[01_lezione-2]]
- **EVM** (Ethereum Virtual Machine) — ambiente di esecuzione deterministica degli smart contract su ogni nodo | vedi [[01_lezione-2]]
- **Solidity** — linguaggio ad alto livello per scrivere smart contract; compilato in bytecode EVM | vedi [[01_lezione-2]]
- **Gas** — unità di misura delle risorse computazionali in Ethereum; prezzo dipende dalla congestione di rete | vedi [[01_lezione-2]]
- **Nonce** — numero sequenziale che garantisce l'ordine delle transazioni provenienti da uno stesso EOA | vedi [[01_lezione-2]]
- **EOA** (Externally Owned Account) — account controllato da un utente tramite chiave privata | vedi [[01_lezione-2]]
- **Proof of Work** — algoritmo di consenso basato su puzzle computazionale (mining); usato da Bitcoin | vedi [[01_lezione-2]]
- **Proof of Stake** — algoritmo di consenso basato su stake economico; usato da Ethereum dal 2022 | vedi [[01_lezione-2]]
- **Validatore** — nodo che propone/attesta blocchi in PoS; richiede 32 ETH in stake | vedi [[01_lezione-2]]
- **Slot** — intervallo di 12 secondi in cui un validatore propone un blocco (Ethereum PoS) | vedi [[01_lezione-2]]
- **Epoch** — gruppo di 32 slot (~6 min); al termine si finalizzano i blocchi | vedi [[01_lezione-2]]
- **LMD Ghost** — algoritmo di fork choice in Ethereum PoS; sceglie il branch con peso maggiore | vedi [[01_lezione-2]]
- **Casper FFG** — protocollo di finalizzazione in Ethereum PoS; richiede 2/3 dei validatori concordi | vedi [[01_lezione-2]]
- **Oracolo** — servizio che porta dati dal mondo reale sulla blockchain per gli smart contract | vedi [[01_lezione-2]]
- **Slashing** — penalità economica per un validatore che si comporta in modo scorretto in PoS | vedi [[01_lezione-2]]
- **Mempool** — area di memoria dove le transazioni attendono di essere incluse in un blocco | vedi [[01_lezione-2]]
- **Deploy** — pubblicazione di uno smart contract sulla blockchain tramite transazione verso address(0) | vedi [[01_lezione-2]]

