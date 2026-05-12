# Guida all'uso dell'IA — Validare il codice suggerito da AI

**Per**: corso IFTS STEM — Specialista nelle Tecniche di Evoluzione e Manutenzione del Software
**Collegamento**: **UF 6** (Applicativi informatici — Opportunità e rischi dell'IA) + UF 10 (Scrittura) + UF 12 (Testing)
**Tipologia**: linee guida operative
**Strumenti AI considerati**: GitHub Copilot, Claude Code, ChatGPT, Gemini Code Assist, Cursor, JetBrains AI

> Nel 2026 **scrivere codice senza AI è raro**. Ma usare AI **senza saperla validare** è pericoloso. Questa guida ti aiuta a sfruttare l'AI come moltiplicatore di produttività, **senza** introdurre vulnerabilità o codice "che sembra giusto ma non lo è".

---

## Indice

- [1. Perché serve validare](#cap1)
- [2. I 7 errori tipici del codice AI](#cap2)
- [3. Workflow di validazione in 4 step](#cap3)
- [4. Checklist per ogni suggerimento](#cap4)
- [5. Prompting per la sicurezza](#cap5)
- [6. Casi pratici — riconoscere e correggere](#cap6)
- [7. Uso etico e legale](#cap7)
- [8. Quando NON usare l'AI](#cap8)
- [9. Risorse e tool di supporto](#cap9)

---

<a name="cap1"></a>
## 1. Perché serve validare

### 1.1 Cosa sa fare l'AI

Le AI di codice (Copilot, Claude, GPT) sono modelli statistici addestrati su **miliardi di righe di codice pubblico** (GitHub, Stack Overflow, documentazione). Producono:

- ✅ Boilerplate e codice ripetitivo (loop, getter/setter, parser)
- ✅ Codice idiomatico in linguaggi comuni (Python, JS, Java, PHP)
- ✅ Refactor di codice esistente
- ✅ Test automatici (struttura)
- ✅ Documentazione (docstring, README)

### 1.2 Cosa NON sa fare bene

L'AI **non** sa:

- ❌ Il **contesto** del tuo progetto (regole business, architettura, dati)
- ❌ Le **vulnerabilità storiche** del tuo codebase
- ❌ Le **policy aziendali**
- ❌ Le **versioni** correnti delle librerie (a meno che tu non gliele dica)
- ❌ Distinguere codice **funzionante** da codice **sicuro**

### 1.3 Il problema concreto

L'AI è stata addestrata su **codice esistente, incluso quello vulnerabile**. Studi GitHub (2022, 2023) e Stanford (2023) hanno mostrato:

- **~40% dei suggerimenti Copilot** contengono vulnerabilità in scenari di sicurezza
- Sviluppatori che usano AI scrivono codice **leggermente meno sicuro** ma sono **più convinti** che sia sicuro (cognitive bias!)
- Gli stessi **pattern vulnerabili degli anni 2000** ancora suggeriti (SQL injection con f-string, ecc.)

> **Tradotto**: l'AI è uno **strumento potente ma non un revisore di sicurezza**. La validazione spetta a te.

### 1.4 La regola di base

> **Fidati ma verifica**. L'AI genera, tu validi. Sempre.

---

<a name="cap2"></a>
## 2. I 7 errori tipici del codice AI

Ecco i pattern di vulnerabilità che vediamo **più spesso** nel codice generato. Riconoscerli a vista è la skill #1.

### 2.1 SQL Injection con f-string

```python
# 🚩 Suggerimento AI tipico
def get_user(user_id):
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

**Perché lo suggerisce**: è il pattern più frequente nel codice antico online.
**Cosa fare**: riscrivi con `?` placeholder.

### 2.2 Hash deboli per password

```python
# 🚩 Suggerimento AI tipico
import hashlib
def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()
```

**Perché**: SHA-256 sembra "sicuro" (è hash crittografico).
**Cosa fare**: bcrypt o Argon2id.

### 2.3 Manca authorization check

```python
# 🚩 AI suggerisce
@app.route("/user/<int:uid>")
@login_required
def get_user(uid):
    return User.query.get(uid).to_dict()
```

**Perché**: l'AI vede "ho `@login_required`, ok". Non sa che `uid` può essere di un altro utente (IDOR).
**Cosa fare**: aggiungi ownership check.

### 2.4 Template senza escape

```javascript
// 🚩 Suggerimento AI per Express + EJS
res.send(`<h1>Ciao ${req.query.name}</h1>`);
```

**Perché**: stringhe template ES6 sembrano "moderne".
**Cosa fare**: template engine con escape, mai concatenazione.

### 2.5 CORS troppo permissivo

```python
# 🚩 AI suggerisce per "risolvere errori CORS"
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

**Perché**: è la "soluzione veloce" agli errori CORS che capita di sviluppatori in difficoltà.
**Cosa fare**: whitelist di origini precise.

### 2.6 Eccezioni catch-all

```python
# 🚩 Suggerimento "robusto" ma fail-open
try:
    if not is_authorized(user, resource):
        return 403
    return resource
except Exception:
    return resource   # 💥 fail OPEN
```

**Perché**: l'AI ha visto pattern `try/except: pass` ovunque.
**Cosa fare**: fail secure (vedi checklist).

### 2.7 Segreti hardcoded

```python
# 🚩 L'AI può inserire "esempi" plausibili
SECRET_KEY = "my-secret-key-change-me"
API_KEY = "sk-1234567890abcdef"
DB_PASSWORD = "admin123"
```

**Perché**: nei dataset di training abbondano esempi con secret in chiaro.
**Cosa fare**: env vars sempre.

### 2.8 BONUS — Dipendenze obsolete o inventate

```python
# 🚩 L'AI suggerisce import che non esistono
from python_super_security import sanitize
```

**Perché**: hallucination. Il modello "inventa" librerie plausibili.
**Cosa fare**: verifica su PyPI/npm. Se non esiste, **attacchi typosquatting** possono creare il package malevolo dopo (è successo!).

---

<a name="cap3"></a>
## 3. Workflow di validazione in 4 step

Per ogni suggerimento AI, segui questa procedura.

### Step 1 — **Leggi e capisci** (30 secondi)

❌ Non accettare codice che non capisci. Mai.

Domande da farti:
- Cosa fa questa riga / questo blocco?
- Perché l'AI l'ha proposto?
- Come si comporta con input "cattivo" (vuoto, troppo lungo, con caratteri speciali)?

> **Regola d'oro**: se non sapresti spiegarlo a un collega in 1 minuto, **non lo accettare**.

### Step 2 — **Scansiona per pattern vulnerabili** (1 minuto)

Mentalmente cerca:

- 🚩 f-string / `+` / `.format()` in SQL → SQL Injection
- 🚩 `os.system()`, `subprocess.shell=True`, `eval()`, `exec()` → RCE
- 🚩 `pickle.loads()` su dati non fidati → RCE
- 🚩 Concatenazione di HTML con input → XSS
- 🚩 `send_file(user_input)` → Path Traversal
- 🚩 Hash deboli per password (MD5, SHA-1, SHA-256)
- 🚩 Cookie senza Secure/HttpOnly/SameSite
- 🚩 `try: ... except: pass` su codice critico
- 🚩 Endpoint senza autenticazione / autorizzazione
- 🚩 Secret hardcoded
- 🚩 Import di librerie sconosciute (verifica esistenza!)

### Step 3 — **Verifica contesto** (1-2 minuti)

L'AI **non sa**:

- Quali utenti possono chiamare l'endpoint?
- Quali dati ci sono nel DB?
- Quali sono le regole business?
- Versione delle librerie usate?

**Tu sì**. Verifica che il codice sia coerente con:
- Architettura del progetto
- Pattern di autenticazione/autorizzazione esistenti
- Stack tecnologico (versioni librerie)
- Convenzioni di nomenclatura

### Step 4 — **Test e tool automatici** (5-15 minuti)

Anche dopo review umano:

- ✅ Esegui i **test esistenti** (regressione)
- ✅ Scrivi un **test specifico** per il nuovo codice (felice + edge case)
- ✅ Lancia **linter di sicurezza**:
  - Python: `bandit -r ./modified_file.py`
  - Multi-lang: `semgrep --config "p/security-audit"`
  - JS: `eslint` con plugin security
  - PHP: `phpcs` + `phpstan`
- ✅ Se modifica dipendenze: `pip-audit`, `npm audit`, `mvn dependency-check`
- ✅ Se aggiunge segreti: verifica con `gitleaks detect`

---

<a name="cap4"></a>
## 4. Checklist per ogni suggerimento

Da scorrere **prima di accettare** un blocco di codice generato.

```
☐ CAPITO: so spiegare cosa fa e perché
☐ INPUT: gestisce input vuoto, troppo lungo, caratteri speciali?
☐ SQL: nessuna f-string in query, sempre placeholder?
☐ HTML: escape automatico attivo, no `|safe` su input utente?
☐ AUTH: l'endpoint richiede login dove serve?
☐ AUTHZ: c'è ownership check sui dati di altri utenti?
☐ ERRORI: failure è "fail secure", non "fail open"?
☐ SEGRETI: nessun hardcoded, tutto in env var?
☐ DIPENDENZE: la libreria che importa esiste davvero?
☐ TEST: ho aggiunto test per il caso d'uso?
☐ LINTER: bandit/semgrep non lamenta nulla?
☐ COMMIT MESSAGE: spiego cosa cambia e perché (non "AI gen")
```

---

<a name="cap5"></a>
## 5. Prompting per la sicurezza

Come scrivere prompt che producono codice **più sicuro** di default.

### 5.1 Specifica il contesto di sicurezza

❌ Vago:
> "Scrivi un endpoint Flask per login"

✅ Specifico:
> "Scrivi un endpoint Flask `/login` POST che:
> - Usa bcrypt per verificare password
> - Risponde uniformemente '401 invalid credentials' per username/password sbagliati (no user enumeration)
> - Implementa rate limit 5/minuto per IP
> - Imposta cookie session con Secure, HttpOnly, SameSite=Lax
> - Logga eventi auth (success/failure) in formato JSON strutturato"

### 5.2 Cita standard

> "Scrivi gestione upload file conforme alle linee guida OWASP File Upload Cheat Sheet"

> "Implementa autenticazione JWT seguendo OWASP JWT Cheat Sheet (algoritmi whitelist, exp, aud, iss)"

### 5.3 Specifica framework e versione

❌ Vago:
> "Scrivi una query SQL per cercare utenti"

✅ Specifico:
> "Scrivi una query SQL parametrizzata in Python usando SQLAlchemy 2.0 ORM per cercare utenti per email"

### 5.4 Chiedi anche test

> "Scrivi questo endpoint + 5 test pytest che verificano:
> 1. Funziona con credenziali corrette
> 2. Risposta uniforme per password sbagliata
> 3. Risposta uniforme per email inesistente
> 4. Rate limit dopo 5 tentativi
> 5. Tentativo SQLi `' OR '1'='1' --` non riesce"

### 5.5 Pattern "AI come revisore"

Dopo aver scritto **tu** il codice, chiedi all'AI:

> "Rivedi questo codice per **vulnerabilità di sicurezza**. Indica:
> - SQL injection / XSS / IDOR / path traversal / SSRF
> - Hash deboli, segreti hardcoded, errori fail-open
> - Conformità OWASP Top 10
>
> [incolla codice]"

Ottieni una **seconda opinione**. Non è un audit pentest, ma cattura ovvietà.

### 5.6 Anti-pattern di prompting

❌ "Disabilita gli errori CORS"
→ AI: "ti metto `origins: '*'`"
→ Buco di sicurezza

✅ "Configura CORS per accettare richieste solo da `https://app.example.com` e `https://admin.example.com`"

---

<a name="cap6"></a>
## 6. Casi pratici — riconoscere e correggere

### 6.1 Caso 1 — Funzione di login

**Prompt all'AI**: "Scrivi una funzione Python per autenticare un utente"

**Output AI tipico**:
```python
import hashlib

def authenticate(username, password):
    pwd_hash = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{pwd_hash}'")
    return cursor.fetchone()
```

**Problemi che dovresti vedere**:
1. 🚩 SHA-256 senza salt per password (M6.4 del corso)
2. 🚩 SQL Injection nella query (M6.2)
3. 🚩 Nessuna risposta uniforme (user enumeration)
4. 🚩 Nessun rate limit
5. 🚩 Nessuna documentazione

**Versione corretta**:
```python
import bcrypt
import logging

log = logging.getLogger(__name__)

def authenticate(username: str, password: str) -> dict | None:
    """Autentica un utente con bcrypt.

    Returns dict utente se OK, None altrimenti.
    Risposta uniforme per non rivelare se l'utente esiste.
    """
    # Query parametrizzata
    user = cursor.execute(
        "SELECT id, username, password_hash FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    if user is None:
        log.warning(f"auth_failure user={username[:50]} reason=no_user")
        return None

    if not bcrypt.checkpw(password.encode(), user["password_hash"]):
        log.warning(f"auth_failure user={username[:50]} reason=wrong_pwd")
        return None

    log.info(f"auth_success user={user['username']}")
    return {"id": user["id"], "username": user["username"]}
```

### 6.2 Caso 2 — Endpoint API "modifica profilo"

**Prompt**: "Endpoint Flask per modificare il profilo utente"

**Output AI tipico**:
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

**Problemi**:
1. 🚩 Nessuna auth richiesta — chiunque modifica
2. 🚩 IDOR — utente A modifica profilo di B passando `user_id` diverso
3. 🚩 Mass Assignment — utente può impostare `role: admin`, `is_verified: true`
4. 🚩 Nessuna validation input

**Versione corretta**:
```python
from pydantic import BaseModel, EmailStr, Field
from flask_login import login_required, current_user

class ProfileUpdate(BaseModel):
    """Solo i campi che l'utente può modificare."""
    name: str | None = Field(default=None, max_length=100)
    email: EmailStr | None = None
    bio: str | None = Field(default=None, max_length=500)
    # NO: role, is_admin, balance, is_verified

@app.route("/api/profile/<int:user_id>", methods=["PUT"])
@login_required
def update_profile(user_id: int):
    # Authorization: solo il proprio profilo (o admin)
    if user_id != current_user.id and not current_user.is_admin:
        return jsonify({"error": "forbidden"}), 403

    try:
        payload = ProfileUpdate(**(request.json or {}))
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

    user = User.query.get_or_404(user_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    db.session.commit()

    return jsonify(user.to_public_dict())   # whitelist campi response
```

### 6.3 Caso 3 — Funzione "esegui comando"

**Prompt**: "Funzione per eseguire un comando di sistema"

**Output AI**:
```python
import os
def run_cmd(cmd):
    return os.popen(cmd).read()
```

**Problemi**:
1. 🚩 Command injection garantita
2. 🚩 Shell metacharacters interpretati
3. 🚩 Nessuna validation
4. 🚩 Tipicamente nasce per "fare qualcosa al volo" e finisce esposto su HTTP

**Soluzione**: **non farlo**. Se davvero serve eseguire comandi:
```python
import subprocess
import shlex

ALLOWED_COMMANDS = {"backup", "restore", "status"}

def run_safe(command_name: str, args: list[str]) -> str:
    if command_name not in ALLOWED_COMMANDS:
        raise ValueError("command not allowed")

    # Argomenti come lista, MAI shell=True
    result = subprocess.run(
        [f"/opt/myapp/scripts/{command_name}.sh"] + args,
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    )
    return result.stdout
```

E **ancora meglio**: evita di esporre esecuzione comandi via HTTP del tutto. Usa una API strutturata.

### 6.4 Caso 4 — Caricamento file

**Prompt**: "Upload di file in Flask"

**Output AI**:
```python
@app.route("/upload", methods=["POST"])
def upload():
    f = request.files["file"]
    f.save(f"uploads/{f.filename}")
    return "ok"
```

**Problemi**:
1. 🚩 Path traversal (`filename = "../etc/passwd"`)
2. 🚩 Nessun controllo estensione
3. 🚩 Nessun controllo MIME
4. 🚩 Nessun limite dimensione
5. 🚩 Nessun limite numero file
6. 🚩 Filename non sanitizzato (può contenere caratteri speciali, Unicode)

**Versione corretta**:
```python
import os
import secrets
from werkzeug.utils import secure_filename
import magic

UPLOAD_DIR = "/var/myapp/uploads"
ALLOWED_EXTS = {".png", ".jpg", ".jpeg", ".pdf"}
MAX_SIZE = 5 * 1024 * 1024   # 5 MB

@app.route("/upload", methods=["POST"])
@login_required
def upload():
    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400

    f = request.files["file"]

    # Validation
    safe_name = secure_filename(f.filename or "")
    if not safe_name:
        return jsonify({"error": "invalid filename"}), 400

    ext = os.path.splitext(safe_name)[1].lower()
    if ext not in ALLOWED_EXTS:
        return jsonify({"error": "extension not allowed"}), 400

    content = f.read(MAX_SIZE + 1)
    if len(content) > MAX_SIZE:
        return jsonify({"error": "too large"}), 413

    # MIME check reale (non header)
    mime = magic.from_buffer(content, mime=True)
    if mime not in {"image/png", "image/jpeg", "application/pdf"}:
        return jsonify({"error": "mime not allowed"}), 400

    # Nome random, non quello dell'utente (anti collision + anti path)
    new_name = f"{secrets.token_urlsafe(16)}{ext}"
    path = os.path.join(UPLOAD_DIR, new_name)

    with open(path, "wb") as out:
        out.write(content)

    return jsonify({"filename": new_name})
```

---

<a name="cap7"></a>
## 7. Uso etico e legale

### 7.1 Proprietà intellettuale

Il codice suggerito dall'AI **può contenere frammenti** simili a codice open source. Implicazioni:

- ✅ **OK**: usare per progetti personali / proof of concept
- ⚠️ **Attenzione**: se il codice è "ovvio" (es. binary search), no issue
- ⚠️ **Attenzione**: se è uno snippet specifico (es. implementazione algoritmo proprietario), possibili problemi
- ❌ **Problemi**: se il modello "ricorda" letteralmente codice con licenza viral (es. GPL) e tu lo usi in un prodotto closed

**In pratica**:
- Aziende serie definiscono **policy interna** sull'uso di AI (es. "vietato in codice production senza review legale")
- GitHub Copilot offre "duplicate detection" (avvisa se restituisce codice identico a esistente public)
- Tieni un **log degli usi AI** in feature significative

### 7.2 Privacy e segreti

Quando incolli codice in ChatGPT / Claude:

- 🚫 **Non incollare** mai codice contenente:
  - Password reali, API key, token
  - Dati personali di utenti reali
  - Strategie business confidenziali
  - Codice coperto da NDA
  - Chiavi private (SSH, GPG, TLS)

> Il caso **Samsung 2023**: dipendenti incollarono codice proprietario in ChatGPT per debugging. OpenAI lo usò per training. Codice **leakato indirettamente**.

### 7.3 Policy aziendale

Verifica con il tuo team / azienda:

- È permesso usare AI per codice production?
- Quali strumenti sono approvati? (alcuni sono enterprise con dati isolati, altri no)
- Servono review extra per codice generato?
- Come si traccia l'uso?

Se non c'è policy, **proponila tu**.

### 7.4 GDPR considerations

Se il tuo codice tratta dati personali, e l'AI tratta dati personali per generare codice, ci sono implicazioni:

- L'AI service è **responsabile del trattamento** dei tuoi prompt?
- Dove sono **memorizzati** i prompt? (USA? EU? Cina?)
- L'AI usa i prompt per **training** futuro?

Soluzioni enterprise:
- **GitHub Copilot Business/Enterprise**: dati non usati per training
- **ChatGPT Team/Enterprise**: dati non usati per training
- **Claude for Teams**: dati non usati per training
- **AWS Bedrock / Azure OpenAI**: dati nella tua tenant, no training

### 7.5 EU AI Act (in vigore 2024-2027)

Per sistemi AI **ad alto rischio** (es. scoring credito, recruitment automatico):
- Documentazione obbligatoria
- Trasparenza algoritmica
- Supervisione umana

Per sviluppatori che **usano** AI per scrivere codice: nessun obbligo diretto, ma se l'output finisce in un prodotto AI ad alto rischio, il tuo codice rientra nella catena.

---

<a name="cap8"></a>
## 8. Quando NON usare l'AI

Ci sono casi in cui l'AI **non va usata**, anche se sembra rapida:

### 8.1 Crittografia "fatta in casa"

❌ Non chiedere all'AI di:
- Implementare un algoritmo di cifratura
- Scrivere un PRNG (generatore numeri pseudo-casuali)
- Implementare un'autenticazione "custom"
- Hash personalizzato

**Perché**: la crittografia ha trappole sottilissime. Usa **librerie standard** (`cryptography`, `bcrypt`, `secrets`).

> Anche se sapessi farlo bene, **non farlo**: la regola è "non scrivere crittografia, usala".

### 8.2 Codice di sicurezza critico

- Logica di autenticazione/autorizzazione "ad alto rischio"
- Codice che processa input untrusted
- Codice che gira con privilegi elevati
- Codice in kernel/driver/firmware

In questi casi: **scrivi tu**, fatti aiutare per boilerplate, **revisione umana obbligatoria**.

### 8.3 Compliance / legale

- Configurazione GDPR (privacy policy, cookie banner)
- Termini di servizio
- Calcolo fiscale, contributi
- Validazione documenti (codice fiscale, P.IVA, IBAN — usa libreria, non regex)

### 8.4 Quando il prompt richiede troppo contesto

Se per spiegare il problema all'AI servono 200 righe di context, **stai usando lo strumento sbagliato**. Probabilmente:
- Il problema è troppo complesso → spezzettare
- Servono decisioni architetturali → umane, non AI

### 8.5 Quando NON sai validare

Se non hai le competenze per **giudicare** il codice generato (è il tuo primo giorno con quel linguaggio/framework), **non usare l'AI come ghost-writer**. Imparalo prima.

L'AI dovrebbe **accelerare** ciò che sai fare, non **sostituire** ciò che non sai.

---

<a name="cap9"></a>
## 9. Risorse e tool di supporto

### 9.1 Tool che usano AI per **trovare** vulnerabilità (non generare codice)

- **Snyk Code** — SAST con AI
- **GitHub Code Scanning** (CodeQL + AI suggestion)
- **DeepCode** (parte di Snyk)
- **Semgrep** (regole non AI, ma alta accuracy)

Usali in CI: scansionano automaticamente PR.

### 9.2 Linee guida ufficiali

- **NIST AI RMF 1.0** (Risk Management Framework): https://www.nist.gov/itl/ai-risk-management-framework
- **OWASP Top 10 for LLM Applications**: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- **MITRE ATLAS** (Adversarial Threat Landscape for AI Systems): https://atlas.mitre.org
- **EU AI Act** (testo ufficiale): https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- **GitHub Copilot trust center**: https://copilot.github.trust.page

### 9.3 Best practice per uso quotidiano

| Pratica | Frequenza |
|---------|-----------|
| Linter di sicurezza in CI | Sempre |
| Pre-commit hooks (bandit, gitleaks) | Sempre |
| Code review umana | Sempre |
| Pentest annuale | Per progetti production |
| Aggiornamento dipendenze | Weekly (Dependabot) |
| Training sviluppatori | Annuale |

### 9.4 Esercizi pratici

Per esercitarsi a riconoscere codice AI vulnerabile:

1. Chiedi all'AI di scrivere 10 endpoint diversi (auth, upload, query, ecc.)
2. Per ognuno, applica la checklist del cap 4
3. Quante vulnerabilità trovi?
4. Quante hai inizialmente accettato senza vedere?

Questo è il vero training.

---

## 10. Riassunto in 10 punti

1. **L'AI non sa di sicurezza**. Tu sì (con questa guida).
2. **Fidati ma verifica**. Sempre.
3. **Capisci ogni riga** prima di accettarla.
4. **Cerca pattern noti** di vulnerabilità (i 7 errori tipici).
5. **Verifica contesto** del tuo progetto.
6. **Test + linter** dopo ogni modifica.
7. **Prompting specifico** = output più sicuro.
8. **Mai segreti** nel prompt.
9. **Mai crittografia / sicurezza critica** da AI senza expertise umana.
10. **Documenta l'uso** dell'AI in progetti enterprise.

---

## Appendice — Domande da farsi a fine giornata

Se hai usato AI oggi, chiediti:

- [ ] Sapevo cosa stavo facendo per ognuno dei suggerimenti?
- [ ] Ho eseguito i test dopo ogni modifica?
- [ ] Ho lasciato segreti nei prompt?
- [ ] Ho controllato che le librerie suggerite esistano?
- [ ] Avrei accettato lo stesso codice da un collega senza review?

Se rispondi "no" a una di queste, **prendi 5 minuti** e revisiona.

---

> *L'AI è un moltiplicatore. Moltiplica anche gli errori se non la usi bene.*
>
> *Documento per il corso STEM IFTS — Anno formativo 2024/2025*
