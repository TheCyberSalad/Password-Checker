# Password Strength Checker 
## English

### Description
This Python script evaluates the strength of a password based on its length, character variety, and estimated entropy. It also checks if the password has been exposed in known data breaches using the Have I Been Pwned API and estimates cracking times for both classical and quantum computing scenarios.

### Requirements
- Python 3.6+
- Required libraries: `requests`, `getpass`, `math`, `re`, `hashlib`
- Internet connection for breach checking

### Installation
1. Install Python 3.6 or higher.
2. Install the required library:
   ```bash
   pip install requests
   ```
3. Save the script as `password_checker.py`.

### Usage
1. Run the script:
   ```bash
   python password_checker.py
   ```
2. Choose language (enter `it` for Italian or `en` for English).
3. Enter a password when prompted (input is hidden for security).
4. Review the output, which includes:
   - Password strength (Weak, Medium, Strong)
   - Estimated entropy in bits
   - Estimated classical cracking time
   - Estimated quantum cracking time (using Grover's algorithm)
   - Breach check result

### Example Output
```
Choose language (it/en): en
Enter the password: 
Strength: Strong
Estimated entropy: 95.21 bits
Classical cracking time (estimate): 301.23 years
Quantum cracking time (estimate with Grover): 2.15 days
Password not found in known breaches.
```

---

## Italiano

### Descrizione
Questo script Python valuta la robustezza di una password in base alla sua lunghezza, varietà di caratteri ed entropia stimata. Controlla anche se la password è stata esposta in violazioni/data breach noti utilizzando l'API di Have I Been Pwned e stima i tempi di cracking sia per scenari di calcolo classici che quantistici.

### Requisiti
- Python 3.6+
- Librerie richieste: `requests`, `getpass`, `math`, `re`, `hashlib`
- Connessione Internet per il controllo delle violazioni

### Installazione
1. Installa Python 3.6 o superiore.
2. Installa la libreria richiesta:
   ```bash
   pip install requests
   ```
3. Salva lo script come `password_checker.py`.

### Utilizzo
1. Esegui lo script:
   ```bash
   python password_checker.py
   ```
2. Scegli la lingua (inserisci `it` per Italiano o `en` per Inglese).
3. Inserisci una password quando richiesto (l'input è nascosto per sicurezza).
4. Esamina l'output, che include:
   - Forza della password (Debole, Media, Forte)
   - Entropia stimata in bit
   - Tempo di cracking classico stimato
   - Tempo di cracking quantistico stimato (usando l'algoritmo di Grover)
   - Risultato del controllo delle violazioni

### Esempio di Output
```
Scegli la lingua (it/en): it
Inserisci la password: 
Forza: Forte
Entropia stimata: 95.21 bit
Tempo cracking classico (stima): 301.23 anni
Tempo cracking quantistico (stima con Grover): 2.15 giorni
Password non trovata in breach noti.
```
