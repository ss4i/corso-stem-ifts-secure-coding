# Checklist Secure Coding — Guida rapida

**Per**: corso IFTS STEM — Specialista nelle Tecniche di Evoluzione e Manutenzione del Software
**Tipologia**: materiale di consultazione **da tenere a portata di mano mentre scrivi codice**
**Linguaggi coperti**: Python, Java, JavaScript/TypeScript, PHP, CSS/HTML
**Collegamenti**: UF 9 (progettazione), UF 10 (scrittura), UF 11 (sviluppo), UF 12 (testing), UF 13 (manutenzione)

> Questa checklist non si **legge**. Si **consulta** mentre scrivi codice e prima di un commit. Stampala, mettila vicino al monitor. Usala come "lista di controllo da pilota".

---

## Come usarla

La checklist è organizzata in **8 sezioni** per **fase del lavoro**:

1. [Prima di scrivere — design](#sec1)
2. [Validazione degli input](#sec2)
3. [Output e rendering](#sec3)
4. [Accesso a database](#sec4)
5. [Autenticazione e sessione](#sec5)
6. [Autorizzazione](#sec6)
7. [Gestione segreti e configurazione](#sec7)
8. [Errori e logging](#sec8)
9. [Prima del commit / merge](#sec9)
10. [Prima del deploy in produzione](#sec10)

Per ogni controllo c'è:
- ✅ **Cosa fare** (la regola)
- 💡 **Esempio** in uno o più linguaggi del corso
- ⚠️ **Anti-pattern** da evitare

---

<a name="sec1"></a>
## 1. Prima di scrivere — design

### 1.1 Threat modeling minimo (5 minuti)

✅ **Prima di scrivere una nuova feature**, chiediti:
- Quali **dati** tocca?
- Chi può **accedere** (autenticato? anonimo? admin?)
- Cosa può andare **storto** se un attaccante manipola input/sessione?
- Dove sono i **trust boundary** (Internet → server, server → DB)?

💡 Cinque minuti di "STRIDE light" salvano ore di refactor.

### 1.2 Least privilege

✅ Dare a ogni componente il **minimo privilegio** che gli serve.
- Utente DB per la webapp: solo SELECT/INSERT/UPDATE sulle sue tabelle.
- App che gira come utente non-root.
- API key con permessi solo per ciò che serve.

⚠️ Anti-pattern: "do permessi pieni, poi vediamo".

### 1.3 Defense in Depth

✅ **Non** affidarsi a un'unica difesa. Layered.
- HTTPS **e** validazione **e** rate limit **e** WAF
- Bucarne una non compromette il sistema.

⚠️ "Tanto abbiamo HTTPS, basta": **no**.

### 1.4 Fail Secure

✅ Quando un controllo fallisce, **chiudi** (default deny).

💡 Python:
```python
try:
    if not is_authorized(user, resource):
        return 403
    return resource
except Exception:
    log.exception("auth check failed")
    return 503   # ✅ NON ritornare la risorsa
```

⚠️ Anti-pattern:
```python
try:
    if not is_authorized(user, resource): return 403
    return resource
except:
    return resource   # 💥 fail OPEN
```

### 1.5 KISS

✅ **Meno** codice = meno bug = meno vulnerabilità.
- Meno dipendenze.
- Meno feature opzionali abilitate.
- Codice leggibile in 5 minuti da un collega.

---

<a name="sec2"></a>
## 2. Validazione degli input

### 2.1 Validazione lato server (sempre)

✅ Ogni input proveniente da **fuori il tuo codice** è untrusted: form HTML, query string, header HTTP, body JSON, file upload, parametri URL, cookie.

✅ Valida **server-side**, anche se hai già validato lato client.

⚠️ "Lo controllo solo lato JavaScript": bypassabile in 5 secondi con curl.

### 2.2 Whitelist > Blacklist

✅ Definisci cosa **accetti** (whitelist), non cosa **rifiuti** (blacklist).

💡 Python:
```python
import re
USERNAME_RE = re.compile(r"^[a-zA-Z0-9_]{3,20}$")
if not USERNAME_RE.fullmatch(username):
    raise ValueError("username invalido")
```

💡 PHP:
```php
if (!preg_match('/^[a-zA-Z0-9_]{3,20}$/', $username)) {
    throw new InvalidArgumentException("username invalido");
}
```

⚠️ `str_replace("'", "", $input)`: blacklist sempre bypassabile.

### 2.3 Type validation

✅ Verifica che i dati siano del tipo atteso.

💡 Python con Pydantic:
```python
from pydantic import BaseModel, EmailStr, Field
class UserCreate(BaseModel):
    email: EmailStr
    age: int = Field(ge=18, le=120)
```

💡 Java con Bean Validation:
```java
public class UserCreate {
    @Email private String email;
    @Min(18) @Max(120) private int age;
}
```

💡 JavaScript con Zod:
```javascript
import { z } from "zod";
const UserCreate = z.object({
    email: z.string().email(),
    age: z.number().int().min(18).max(120),
});
```

### 2.4 Lunghezza massima

✅ Imposta **sempre** un limite di lunghezza prima di processare.

⚠️ Stringhe non limitate causano:
- ReDoS (regex con backtracking esponenziale)
- DoS di memoria
- Overflow in alcuni contesti

### 2.5 File upload

✅ Valida:
- **Estensione** (whitelist)
- **MIME type reale** (libmagic, NON header HTTP che è spoofabile)
- **Dimensione** (max size)
- **Contenuto** (es. Pillow per verificare immagine valida)

💡 Python:
```python
import magic
mime = magic.from_buffer(file_content, mime=True)
if mime not in {"image/png", "image/jpeg"}:
    raise ValueError("mime non ammesso")
```

⚠️ Fidarsi di `request.files["x"].content_type` (header HTTP).

---

<a name="sec3"></a>
## 3. Output e rendering

### 3.1 Escape HTML automatico

✅ Usa template engine che fanno **escape di default**.

| Linguaggio | Engine | Escape automatico? |
|------------|--------|---------------------|
| Python | Jinja2 (Flask, Django) | ✅ Sì |
| Java | Thymeleaf | ✅ Sì |
| JavaScript | React (JSX), Vue | ✅ Sì |
| PHP | Twig, Blade | ✅ Sì |
| PHP "raw" | `echo $x` | ❌ NO, fai `htmlspecialchars()` |

⚠️ Disabilitare l'escape (`{{ x \| safe }}`, `{!! $x !!}`, `v-html`, `dangerouslySetInnerHTML`) su input utente = **XSS garantita**.

### 3.2 Contesti diversi richiedono encoding diversi

✅ Encoding dipende da **dove** finisce l'output:

| Contesto | Encoding |
|----------|----------|
| HTML body | HTML escape (`&lt;` etc.) |
| Attributo HTML | HTML attribute escape |
| JavaScript string | JS escape (`<`) |
| CSS | CSS escape |
| URL | URL encoding (`%3C`) |
| JSON | JSON encoding (`<`) |

💡 PHP:
```php
echo htmlspecialchars($var, ENT_QUOTES | ENT_HTML5, 'UTF-8');
```

💡 JavaScript inline:
```html
<!-- ❌ rischioso -->
<script>var x = "{{ user_input }}";</script>

<!-- ✅ usa data attribute + JS DOM -->
<div data-user="{{ user_input }}"></div>
<script>
  var x = document.querySelector('div').dataset.user;
</script>
```

### 3.3 Content-Security-Policy

✅ Imposta header CSP restrittivo (riduce drasticamente XSS impact):

```
Content-Security-Policy: default-src 'self';
  script-src 'self' 'nonce-r4nd0m';
  frame-ancestors 'none'
```

### 3.4 JSON responses

✅ `Content-Type: application/json` sempre.
✅ Usa la libreria standard (`json.dumps`, `JSON.stringify`, `Jackson`, `json_encode`), mai concatenazione di stringhe.

⚠️ `f'{"name": "{user}"}'` in Python: se `user` contiene `"`, JSON invalido o injection.

---

<a name="sec4"></a>
## 4. Accesso a database

### 4.1 Query parametrizzate (sempre)

✅ Mai concatenare input utente in query SQL. Sempre placeholder.

💡 Python (sqlite3, psycopg2):
```python
# ✅
cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# ❌
cur.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

💡 Java (PreparedStatement):
```java
PreparedStatement ps = conn.prepareStatement(
    "SELECT * FROM users WHERE id = ?");
ps.setInt(1, userId);
ResultSet rs = ps.executeQuery();
```

💡 PHP (PDO):
```php
$stmt = $pdo->prepare("SELECT * FROM users WHERE id = ?");
$stmt->execute([$userId]);
```

💡 JavaScript (better-sqlite3):
```javascript
const stmt = db.prepare("SELECT * FROM users WHERE id = ?");
const user = stmt.get(userId);
```

### 4.2 ORM come scelta preferita

✅ ORM forza il pattern parametrizzato. Più sicuro per default.

| Linguaggio | ORM tipici |
|------------|------------|
| Python | SQLAlchemy, Django ORM |
| Java | Hibernate, JPA |
| JavaScript/TS | Prisma, TypeORM |
| PHP | Doctrine, Eloquent (Laravel) |

⚠️ Anche con ORM, evita `text()` o `raw()` con f-string:
```python
# ❌ SQLi possibile anche in SQLAlchemy
session.execute(text(f"SELECT * FROM users WHERE id = {user_id}"))
```

### 4.3 Least privilege DB user

✅ L'utente DB della webapp deve avere **solo** i privilegi necessari.
- ❌ NON deve avere `GRANT`, `DROP`, `CREATE USER`
- ❌ NON dovrebbe essere `postgres` o `root` DB

### 4.4 Stored procedure ≠ sicurezza automatica

⚠️ Le stored procedure **non** sono automaticamente safe. Se costruiscono dinamicamente SQL al loro interno con input, sono vulnerabili come una query inline.

---

<a name="sec5"></a>
## 5. Autenticazione e sessione

### 5.1 Hashing password

✅ Algoritmi accettati: **bcrypt**, **Argon2id**, **scrypt**, **PBKDF2** (≥600.000 iter).

❌ Mai: MD5, SHA-1, SHA-256 (anche con salt — troppo veloce).
❌ Mai: password in chiaro o "cifrate" con AES (reversibile = breach catastrofico).

💡 Python:
```python
import bcrypt
hash_db = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt(rounds=12))
ok = bcrypt.checkpw(input_pwd.encode(), hash_db)
```

💡 Java (Spring Security):
```java
BCryptPasswordEncoder encoder = new BCryptPasswordEncoder(12);
String hash = encoder.encode(password);
boolean ok = encoder.matches(input, hash);
```

💡 PHP:
```php
$hash = password_hash($pwd, PASSWORD_BCRYPT, ['cost' => 12]);
$ok = password_verify($input, $hash);
```

### 5.2 Password policy minima

✅ Lunghezza minima: 12 caratteri (NIST raccomanda).
✅ Verifica contro **liste di password compromesse** (HaveIBeenPwned API).
✅ Niente caratteri obbligatori "fissi" (es. 1 maiuscola): è meglio una passphrase lunga.

⚠️ Anti-pattern: forzare reset ogni 90 giorni (NIST l'ha sconsigliato dal 2017 — porta a password peggiori).

### 5.3 MFA / 2FA

✅ Offri MFA (TOTP, WebAuthn). Obbligatorio per:
- Account admin
- Operazioni critiche (cambio password, modifica email)

### 5.4 Rate limiting su login

✅ Limite per IP **e** per username (5 tentativi/minuto tipico).

✅ Lockout temporaneo dopo N falliti (15 min).

⚠️ Anche con rate limit, **risposta uniforme**: "email o password sbagliati", **mai** "utente non esiste" (user enumeration).

### 5.5 Cookie di sessione

✅ Cookie con **tutti** questi attributi:
```
Set-Cookie: session=abc;
            Secure; HttpOnly; SameSite=Lax;
            Path=/; Max-Age=3600
```

| Attributo | Cosa fa |
|-----------|---------|
| `Secure` | Solo su HTTPS |
| `HttpOnly` | JS non può leggerlo (anti-XSS) |
| `SameSite=Lax`/`Strict` | Anti-CSRF |
| `Max-Age` | Scadenza |

### 5.6 Session ID

✅ Generato con CSPRNG (≥128 bit di entropia).
✅ Rigenerato dopo login (anti session fixation).
✅ Invalidato lato server al logout (non solo cookie cancellato).

⚠️ Session ID prevedibili = takeover.

### 5.7 JWT (se li usi)

✅ `algorithms=["HS256"]` whitelist in decode (mai `none`).
✅ `exp` < 1 ora per access token.
✅ Refresh token con rotation.
✅ `aud`/`iss` validati.
✅ JWT in cookie HttpOnly (mai in localStorage).

---

<a name="sec6"></a>
## 6. Autorizzazione

### 6.1 Authentication ≠ Authorization

✅ "Sei loggato" non significa "puoi fare X".

✅ Verifica **ownership** o **role** **server-side** su ogni endpoint che ritorna dati di altri utenti.

💡 Python:
```python
@app.route("/fattura/<int:fid>")
@login_required
def fattura(fid):
    f = Fattura.query.filter_by(
        id=fid, owner_id=session["user_id"]
    ).first_or_404()
    return render_template("fattura.html", f=f)
```

⚠️ Anti-pattern: nascondere ID in UI ("security by obscurity"). Inutile.

### 6.2 Status code corretti

| Code | Quando |
|------|--------|
| 401 | **Non** autenticato |
| 403 | Autenticato ma **non autorizzato** |
| 404 | Risorsa non esiste |

⚠️ Usare 404 per "non autorizzato" maschera info ma confonde i tool/log.

### 6.3 Function-level authz

✅ Endpoint admin sotto `/admin/...` con decorator centrale.

💡 Java (Spring Security):
```java
@PreAuthorize("hasRole('ADMIN')")
@GetMapping("/admin/users")
public List<User> listAll() { ... }
```

### 6.4 Mass Assignment / BOPLA

✅ Whitelist dei campi che l'utente può modificare.

💡 Python (Pydantic):
```python
class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    # NO: role, is_admin, balance
```

⚠️ `for k,v in data.items(): setattr(user, k, v)` accetta qualunque campo, incluso `is_admin = True`.

---

<a name="sec7"></a>
## 7. Gestione segreti e configurazione

### 7.1 Segreti fuori dal codice

✅ Mai password, API key, token nel codice sorgente.

✅ Usa:
- Variabili d'ambiente (`os.environ` Python, `process.env` JS, `$_ENV` PHP, `System.getenv()` Java)
- File `.env` (locale) escluso da Git
- Secrets manager (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault)

💡 Python:
```python
import os
SECRET_KEY = os.environ["SECRET_KEY"]   # KeyError se mancante = fail-fast
```

### 7.2 `.gitignore`

✅ Sempre presente, sempre include:
```
.env
.env.local
*.pem
*.key
secrets/
credentials*.json
```

### 7.3 Verifica con tool

✅ Esegui **gitleaks** o **TruffleHog** prima di ogni push.

✅ Configura **pre-commit hook** che blocca commit con secret.

### 7.4 Se hai committato un secret per sbaglio

1. **Revoca** subito la credenziale (genera nuova).
2. Riscrivi history (BFG Repo-Cleaner).
3. Force push (warning collaboratori).
4. **Non pensare** "ho cancellato il commit, ok". Tutti i fork hanno ancora il secret.

### 7.5 Configurazione per ambiente

✅ Default sicuri.
- `DEBUG = False` in prod.
- `secure_cookies = True` in prod.
- TLS minimum 1.2 (1.3 preferito).

⚠️ Anti-pattern: stessa configurazione dev/prod. Differenzia.

---

<a name="sec8"></a>
## 8. Errori e logging

### 8.1 Errori al client = generici

✅ HTTP 500 generico: `{"error": "internal_server_error"}`.

❌ Mai stack trace al client (information disclosure).

💡 Python (Flask):
```python
@app.errorhandler(Exception)
def handle(e):
    app.logger.exception("unhandled")
    return jsonify({"error": "internal"}), 500
```

💡 PHP:
```php
ini_set('display_errors', '0');     // produzione
error_reporting(E_ALL);
ini_set('log_errors', '1');
ini_set('error_log', '/var/log/app/php_errors.log');
```

### 8.2 Logging strutturato

✅ Output JSON (Elastic Common Schema o OpenTelemetry).
✅ Stdout (no file diretti, lascia farlo a chi gestisce).

💡 Python:
```python
import logging
from pythonjsonlogger import jsonlogger
handler = logging.StreamHandler()
handler.setFormatter(jsonlogger.JsonFormatter())
log.addHandler(handler)

log.info("login.success", extra={
    "event_type": "auth.login.success",
    "user_id": user.id, "ip": ip,
})
```

### 8.3 Cosa loggare

✅ Login (OK+FAIL), logout, cambio password
✅ Accessi a risorse sensibili
✅ Errori 5xx con context
✅ Modifica ruoli/permessi
✅ Operazioni critiche (transazioni, delete)

❌ **MAI** loggare in chiaro:
- Password
- Token completi (solo prefisso)
- Numeri di carta
- CF/SSN intero
- Cookie sessione completi

### 8.4 Audit log

✅ Per operazioni critiche: log immutabile (append-only) separato.

✅ Hash chain (SHA-256) per detection tampering.

---

<a name="sec9"></a>
## 9. Prima del commit / merge

Checklist da **scorrere prima di ogni `git commit`**:

- [ ] Nessun `print()` / `console.log` / `var_dump` di debug
- [ ] Nessuna password / API key hardcoded
- [ ] Nessun `TODO: fix later` su codice di sicurezza
- [ ] `.env` non staged
- [ ] Test passano (`pytest`, `mvn test`, `npm test`)
- [ ] Linter pulito (`bandit`, `eslint`, `phpstan`)
- [ ] Code review fatta (se >1 sviluppatore)
- [ ] Documentazione aggiornata (vedi UF 7 — collegamento documento "Template documentazione")
- [ ] Messaggio commit chiaro (cosa, perché)

### 9.1 Pre-commit hooks automatici

Configura `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks: [{id: gitleaks}]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks: [{id: bandit, args: ["-ll"]}]
```

Da ora ogni commit viene controllato automaticamente.

---

<a name="sec10"></a>
## 10. Prima del deploy in produzione

- [ ] `DEBUG = False` ovunque
- [ ] Variabili d'ambiente di produzione configurate
- [ ] HTTPS configurato con certificato valido (non self-signed)
- [ ] HSTS attivo (`max-age=31536000; includeSubDomains; preload`)
- [ ] Tutti i 6 header di sicurezza attivi (HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy)
- [ ] Cookie sessione con Secure + HttpOnly + SameSite
- [ ] Database con utente least-privilege
- [ ] Backup automatici testati
- [ ] Logging centralizzato attivo
- [ ] Monitoring + alert configurati
- [ ] Disaster recovery plan documentato
- [ ] Penetration test eseguito (almeno annuale)
- [ ] SBOM generato (`pip-audit`, `npm audit`, `mvn dependency-check`)
- [ ] Patching SLA definito (CVE Critical entro 7 gg)
- [ ] Privacy policy / GDPR cookie banner aggiornati
- [ ] Notifica breach: chi chiama il Garante in 72h?

---

## Riferimenti normativi (sintesi)

| Articolo | Cosa richiede |
|----------|---------------|
| **GDPR Art. 5** | Principi (minimizzazione, integrità, riservatezza) |
| **GDPR Art. 25** | Privacy by Design and by Default |
| **GDPR Art. 32** | Misure tecniche adeguate (cifratura, pseudonimizzazione, backup, test regolari) |
| **GDPR Art. 33-34** | Notifica breach entro 72h |
| **NIS 2 Art. 21** | 10 misure di gestione del rischio (incluse MFA, cifratura, formazione) |
| **NIS 2 Art. 23** | Notifica incidenti (24h + 72h + 30gg) |
| **CRA (2027)** | Prodotti con elementi digitali — niente vulnerabilità note alla vendita |
| **Legge 4/2004** | Accessibilità prodotti digitali (collegamento UF 9) |

---

## Stampabile — versione una pagina

```
┌─────────────────────────────────────────────────────────────────┐
│ CHECKLIST SECURE CODING — VERSIONE TASCA                         │
├─────────────────────────────────────────────────────────────────┤
│ INPUT                                                            │
│   ✓ Valida server-side (whitelist)                               │
│   ✓ Type validation (Pydantic/Bean Validation/Zod)               │
│   ✓ Lunghezza max sempre                                         │
│                                                                  │
│ OUTPUT                                                           │
│   ✓ Template engine con escape automatico                        │
│   ✓ Non disabilitare l'escape su input utente                    │
│   ✓ CSP attivo                                                   │
│                                                                  │
│ DATABASE                                                         │
│   ✓ Query parametrizzate / ORM                                   │
│   ✓ Mai f-string in SQL                                          │
│   ✓ Utente DB con least privilege                                │
│                                                                  │
│ AUTH                                                             │
│   ✓ bcrypt / Argon2id (mai MD5/SHA)                              │
│   ✓ Rate limit + lockout                                         │
│   ✓ Cookie Secure+HttpOnly+SameSite                              │
│   ✓ Risposta uniforme login                                      │
│                                                                  │
│ AUTHZ                                                            │
│   ✓ Ownership check server-side                                  │
│   ✓ 401 vs 403 corretto                                          │
│   ✓ Pydantic per Mass Assignment                                 │
│                                                                  │
│ SEGRETI                                                          │
│   ✓ Env var, mai in codice                                       │
│   ✓ .gitignore include .env                                      │
│   ✓ gitleaks in pre-commit                                       │
│                                                                  │
│ ERRORI                                                           │
│   ✓ 500 generico al client                                       │
│   ✓ Stack trace solo in log interno                              │
│   ✓ Logging strutturato JSON                                     │
│                                                                  │
│ PRIMA DEL COMMIT                                                 │
│   ✓ Test passano                                                 │
│   ✓ Linter pulito                                                │
│   ✓ Nessun secret                                                │
│   ✓ .env non staged                                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Per approfondire

- **OWASP Top 10** (web app): https://owasp.org/Top10/
- **OWASP API Security Top 10**: https://owasp.org/API-Security/
- **OWASP Cheat Sheet Series**: https://cheatsheetseries.owasp.org
- **NIST SP 800-218** (Secure Software Development Framework)
- **OWASP ASVS** (Application Security Verification Standard)

---

> Questa checklist è un **documento vivo**. Aggiornala quando incontri vulnerabilità nuove o nei post-mortem dei tuoi progetti.
>
> *Per il corso STEM IFTS — Anno formativo 2024/2025*
