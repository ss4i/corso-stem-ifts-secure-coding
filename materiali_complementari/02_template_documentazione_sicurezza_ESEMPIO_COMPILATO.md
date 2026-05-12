# Documento di Sicurezza — MiniBlog v1.0

**Versione documento**: 1.0
**Data**: 2025-09-15
**Autore**: Mario Rossi
**Approvato da**: Lucia Bianchi (Security Lead)
**Prossima revisione**: 2026-09-15

> Questo è un **esempio compilato** del template `02_template_documentazione_sicurezza.md`.
> "MiniBlog" è un'app fittizia: piattaforma di blog personali con utenti, post e commenti.
> Serve come riferimento per gli studenti del corso STEM IFTS.

---

## 1. Informazioni generali

### 1.1 Identificativo

| Campo | Valore |
|-------|--------|
| Nome progetto | MiniBlog |
| Versione applicativa | 1.0.3 |
| Repository Git | https://github.com/esempio/miniblog |
| Ambiente | AWS EU-South-1 (Milano), 2 EC2 + RDS PostgreSQL |
| Stack | Python 3.12 + Flask 3.0 + PostgreSQL 15 + Redis |
| Owner | Team Backend (mario.rossi@esempio.it) |
| Stakeholder | Direzione, utenti finali (~5.000 bloggers), DPO |

### 1.2 Scopo del progetto

MiniBlog è una piattaforma di blog personali. Ogni utente registrato può:
- Creare/modificare/cancellare i propri post (HTML markdown)
- Caricare immagini (max 5MB) negli articoli
- Ricevere e moderare commenti
- Esportare i propri dati (GDPR Art. 15)

Il pubblico legge i post senza autenticazione.

### 1.3 Classificazione dei dati

| Categoria | Esempi | Volume |
|-----------|--------|--------|
| Dati personali comuni | username, email, password hash, profile bio | ~5.000 utenti |
| Contenuti utente | post, commenti, immagini | ~50.000 post, ~200.000 commenti |
| Log accessi | IP, user-agent, timestamp | retention 90 giorni |
| Nessun dato art. 9 GDPR | — | — |
| Nessun dato di pagamento | — | — |

### 1.4 Norme applicabili

- ✅ **GDPR** — tratta dati personali di residenti UE
- ❌ **NIS 2** — non rientriamo nei settori (siamo una piccola piattaforma editoriale, <50 dipendenti)
- ✅ **CRA** — dal 2027 saremo soggetti (prodotto digitale venduto UE)
- ❌ **Legge 4/2004** — non siamo PA né servizio universale
- ❌ **PCI DSS** — non trattiamo carte (pagamenti via Stripe in-iframe)

---

## 2. Threat Model

### 2.1 Data Flow Diagram

```
                ┌──────────────────┐
                │      Utente      │
                │   (Browser)      │
                └────────┬─────────┘
                         │ HTTPS
                ╔════════╪═══════════════════════╗   Trust boundary: Internet
                         │
                         ▼
                ┌──────────────────┐
                │   Nginx (WAF)    │
                │  Reverse proxy   │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐         ┌──────────────────┐
                │  Flask app       │◄────────│   Redis (cache)  │
                │  (2 istanze)     │         └──────────────────┘
                └────────┬─────────┘
                         │ TLS
                ╔════════╪═══════════════════════╗   Trust boundary: VPC
                         ▼
                ┌──────────────────┐
                │  PostgreSQL RDS  │
                │  (cifrato a KMS) │
                └────────┬─────────┘
                         │
                         ▼ snapshot crittografato
                ┌──────────────────┐
                │  S3 backup       │
                │  (Object Lock)   │
                └──────────────────┘
```

### 2.2 Minacce identificate (top 10)

| ID | STRIDE | Asset | Descrizione | Prob | Imp | Rischio | Mitigazione |
|----|--------|-------|-------------|------|-----|---------|-------------|
| T-01 | S | Login | Brute force credenziali | Alta | Alto | **Alto** | Rate limit 5/min IP, bcrypt 12, lockout 15min |
| T-02 | E | Endpoint `/post/<id>/edit` | IDOR — utente modifica post altrui | Media | Alto | **Alto** | Ownership check (`filter_by(owner_id=current.id)`) |
| T-03 | I | DB | SQL Injection in ricerca post | Bassa | Critico | Medio | SQLAlchemy ORM ovunque, audit con bandit |
| T-04 | I | Commenti | Stored XSS in commenti | Media | Alto | **Alto** | bleach sanitization + Jinja2 escape + CSP |
| T-05 | T | Cookie sessione | Manipolazione cookie | Bassa | Alto | Medio | itsdangerous signed, HttpOnly, Secure, SameSite=Lax |
| T-06 | I | Upload immagini | Caricamento file `.php`/`.html` | Media | Alto | **Alto** | Whitelist estensioni + magic + Pillow verify |
| T-07 | I | API export GDPR | Esposizione dati altri utenti | Bassa | Critico | Medio | Authz + filter by user, audit log |
| T-08 | D | Frontend | DDoS volumetrico | Media | Medio | Medio | AWS Shield Standard + CloudFront |
| T-09 | I | Path traversal `/img/<file>` | Lettura file di sistema | Bassa | Critico | Medio | Whitelist + `os.path.realpath` + `startswith` |
| T-10 | I | Backup S3 | Bucket esposto pubblicamente | Bassa | Critico | Medio | ACL `private`, KMS, Object Lock, audit AWS Config |

### 2.3 Out of scope

- Sicurezza fisica datacenter AWS (gestita da AWS)
- Sicurezza degli endpoint utenti (browser, OS)
- Phishing diretto agli utenti (educazione fuori scope tecnico)

---

## 3. Controlli applicati

### 3.1 Autenticazione

| Controllo | Stato | Riferimento codice |
|-----------|-------|---------------------|
| bcrypt cost=12 | ✅ | `app/auth.py:42` |
| MFA TOTP (opzionale per utenti) | ✅ | `app/auth/totp.py` |
| Rate limit login 5/min | ✅ | `app/__init__.py:18` (Flask-Limiter) |
| Risposta uniforme login | ✅ | `app/auth.py:67` |
| Session ID rigenerato post-login | ✅ | Flask-Login default |
| Logout invalida sessione DB | ✅ | `app/auth.py:120` |
| Password ≥12 char + check HIBP | ✅ | `app/validators.py:55` |
| Reset password con token monouso | ✅ | scadenza 15 min, `app/auth/reset.py` |

### 3.2 Autorizzazione

- ✅ `@login_required` su tutti gli endpoint privati (audit: 47/47)
- ✅ Ownership check via `filter_by(owner_id=current.id)` ovunque
- ✅ `@require_role("admin")` per moderazione
- ✅ Status code corretti (401 vs 403) — verificato da `tests/test_authz.py`
- ✅ Pydantic per Mass Assignment prevention (`app/schemas.py`)

### 3.3 Input validation

- ✅ Pydantic per ogni POST/PUT (`app/schemas/*.py`)
- ✅ Username: regex `^[a-zA-Z0-9_]{3,20}$`
- ✅ Email: `EmailStr`
- ✅ File upload:
  - Whitelist: `.png`, `.jpg`, `.jpeg`, `.webp`
  - MIME check con `python-magic` (no header HTTP)
  - Max 5MB
  - `Image.open(...).verify()` (Pillow)
- ✅ Lunghezza max stringhe (Pydantic Field constraints)

### 3.4 Output / rendering

- ✅ Jinja2 escape default ON
- ⚠️ Un solo uso di `|safe` in `templates/about.html` (testo statico approvato)
- ✅ Commenti utente sanitizzati con `bleach` (whitelist: `p, b, i, a` + attr `href` http/https only)
- ✅ Markdown post: `markdown` library + `bleach` post-processing

### 3.5 Header HTTP di sicurezza

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-{{nonce}}';
                          style-src 'self' 'unsafe-inline';
                          img-src 'self' data: https://cdn.miniblog.it;
                          frame-ancestors 'none'
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

Configurazione: `nginx/security-headers.conf` + Flask `app/security.py`.

Voto securityheaders.com: **A** (verificato 2025-09-01).

### 3.6 Cifratura

| Cosa | Algoritmo | Riferimento |
|------|-----------|-------------|
| TLS | 1.3 (1.2 minimum), ECDHE-ECDSA-CHACHA20 | nginx config |
| Password | bcrypt cost=12 | `app/auth.py` |
| DB at rest | AES-256 via AWS RDS encryption (KMS) | AWS Console |
| Backup at rest | AES-256 via S3 SSE-KMS + Object Lock | AWS Console |
| Session cookie | Signed via Flask SECRET_KEY (32 bytes random) | env var |
| Token reset password | Signed JWT (HS256) con `exp` 15min | `app/auth/reset.py` |

Rotazione SECRET_KEY: annuale + on-demand.

### 3.7 Gestione segreti

- ✅ Tutti i segreti in env vars
- ✅ `.env` in `.gitignore`
- ✅ Pre-commit hook gitleaks attivo (`.pre-commit-config.yaml`)
- ✅ Produzione: AWS Secrets Manager (rotazione automatica per DB password ogni 30gg)
- ✅ Verifica con `gitleaks detect --source .` mensile — 0 finding

### 3.8 Database

- ✅ Utente `miniblog_app` con permessi solo `SELECT, INSERT, UPDATE, DELETE` su schema `public`
- ❌ Nessun `GRANT`, `DROP`, `CREATE` per l'app
- ✅ Connessione TLS-only (`sslmode=require`)
- ✅ SQLAlchemy ORM ovunque (zero query raw nel codebase, verificato)
- ✅ Backup automatici daily, retention 30gg + monthly 12 mesi
- ✅ Restore testato mensilmente (ultimo: 2025-08-15)

### 3.9 Logging e audit

| Tipo | Cosa | Retention | Storage |
|------|------|-----------|---------|
| App log | Errori, info, query lente | 30gg | CloudWatch |
| Audit log | Login OK/FAIL, modifica role, delete user, export GDPR | 7 anni | S3 Object Lock + hash chain SHA-256 |
| Access log nginx | Tutti gli HTTP | 90gg | S3 |

Formato: JSON Elastic Common Schema.

PII: email mascherate (`m***@example.com`) nei log non-audit.

### 3.10 Supply chain

- ✅ pip-audit in CI (blocca su Critical)
- ✅ Dependabot weekly (PR automatiche)
- ✅ SBOM generato ad ogni release (`scripts/generate-sbom.sh`)
- ✅ Versioni pinned in `requirements.txt`
- ✅ SLA: Critical CVE patchata entro 7 gg

Ultimo audit: 2025-09-10 — 0 vulnerabilità High/Critical.

### 3.11 Pipeline CI/CD

`.github/workflows/security.yml`:

| Check | Stato | Bloccante? |
|-------|-------|-----------|
| Bandit (SAST) | ✅ | Sì (Critical/High) |
| Semgrep | ✅ | Sì |
| pip-audit (SCA) | ✅ | Sì (Critical) |
| gitleaks | ✅ | Sì |
| pytest + coverage ≥80% | ✅ | Sì |
| Trivy container scan | ✅ | Sì (Critical/High) |
| OWASP ZAP baseline (staging) | ✅ | No (alert) |
| Branch protection main | ✅ — require PR + green CI + 1 reviewer | |
| Signed commits | ⚠️ raccomandato | |

### 3.12 Network

- ✅ App **non** esposta direttamente — dietro nginx + AWS ALB
- ✅ DB nella subnet privata (Security Group: solo dalla subnet app)
- ✅ SSH solo via bastion host (chiave + MFA)
- ✅ AWS WAF con managed rules OWASP Top 10
- ✅ AWS Shield Standard (DDoS L3/L4)

---

## 4. Vulnerabilità note e debt

| ID | Descrizione | Sev | Workaround | Scoperto | Piano |
|----|-------------|-----|-------------|----------|-------|
| DT-01 | MFA non obbligatoria per nuovi utenti | Media | No | 2025-04 | Rollout obbligatorio Q1 2026 |
| DT-02 | `pillow` ha CVE-2025-XXXX (Low) — patch in v11.5, ora siamo a 11.4 | Bassa | nessun input image-bomb finora | 2025-09-08 | Aggiornare al prossimo sprint |
| DT-03 | Test coverage 81% — target 85% | Bassa | N/A | continuo | Q4 2025 |

---

## 5. Test di sicurezza

### 5.1 Test automatici

- `tests/security/test_sqli.py` — 12 test
- `tests/security/test_idor.py` — 8 test
- `tests/security/test_xss.py` — 7 test
- `tests/security/test_authz.py` — 18 test
- `tests/security/test_csrf.py` — 5 test
- `tests/security/test_upload.py` — 9 test

Esecuzione: ogni PR. Tempo: ~2 min.

### 5.2 Pentest

| Quando | Eseguito da | Findings |
|--------|--------------|----------|
| 2024-12-01 | Team interno | 2 Medium, 3 Low — chiusi |
| 2025-06-15 | Acme Sec (esterno) | 1 High (XSS edge case), 3 Medium, 7 Low |

High chiuso entro 5 giorni dal report.

Report archiviati in `docs/pentest/` (accesso: security team + CTO).

### 5.3 Vulnerability disclosure

Email: `security@miniblog.it` (chiave PGP disponibile su `/security.txt`).

Policy: 90 giorni timeline standard, riconoscimento ricercatore in `SECURITY.md`.

---

## 6. Incident response

### 6.1 Contatti emergenza

| Ruolo | Nome | Tel | Email |
|-------|------|-----|-------|
| Security Lead | Lucia Bianchi | +39 333 ... | l.bianchi@miniblog.it |
| DPO | Marco Verdi | +39 366 ... | dpo@miniblog.it |
| CTO | Paolo Neri | +39 348 ... | cto@miniblog.it |
| AWS support | Premium | - | ID account 1234567890 |

### 6.2 Playbook

Vedi `docs/incident-response-playbook.md`.

Simulazione tabletop annuale: ultima 2025-04-20.

---

## 7. Compliance

### 7.1 GDPR

| Adempimento | Stato | Riferimento |
|--------------|-------|-------------|
| Registro trattamenti (Art. 30) | ✅ | `docs/registro-trattamenti.xlsx` |
| Privacy policy pubblica | ✅ | `/privacy` |
| Cookie banner conforme | ✅ | Iubenda |
| Diritto export (Art. 15) | ✅ | endpoint `/account/data-export` |
| Diritto cancellazione (Art. 17) | ✅ | endpoint `/account/delete` + procedura admin |
| DPIA | ✅ | `docs/dpia-miniblog.pdf` (rev 2025-03) |
| Procedura 72h breach | ✅ | playbook + simulazione annuale |
| Pseudonimizzazione test DB | ✅ | `scripts/anonymize.py` |

### 7.2 NIS 2

Non applicabile (non rientriamo nei settori essenziali/importanti).

### 7.3 CRA (dicembre 2027)

Piano di compliance avviato Q3 2025:
- SBOM già generato
- Vulnerability disclosure policy attiva
- Patching SLA documentato
- Supporto sicurezza minimo 5 anni dichiarato

---

## 8. Approvazione

### 8.1 Storico revisioni

| Versione | Data | Autore | Modifiche |
|----------|------|--------|-----------|
| 0.1 | 2024-09-15 | M. Rossi | Bozza iniziale |
| 1.0 | 2024-12-01 | M. Rossi | Approvato per release v1.0 |
| 1.1 | 2025-04-15 | L. Bianchi | Post pentest interno |
| 1.2 | 2025-06-30 | L. Bianchi | Post pentest esterno + DT-01 |
| 1.3 | 2025-09-15 | M. Rossi | Update CI/CD, refresh |

### 8.2 Approvazione versione 1.3

| Ruolo | Nome | Data | Approvazione |
|-------|------|------|---------------|
| Security Lead | Lucia Bianchi | 2025-09-15 | ✅ Approvato via email |
| DPO | Marco Verdi | 2025-09-16 | ✅ Approvato |
| CTO | Paolo Neri | 2025-09-17 | ✅ Approvato |

### 8.3 Prossima revisione

2026-09-15 — review annuale + post pentest 2026-06.

---

## 9. Allegati

- [Allegato A] `docs/dpia-miniblog.pdf` (DPIA)
- [Allegato B] `docs/pentest/2025-06-acme-sec.pdf`
- [Allegato C] `docs/registro-trattamenti.xlsx`
- [Allegato D] `docs/architecture-diagram.png`
- [Allegato E] `docs/disaster-recovery-plan.pdf`
- [Allegato F] `sbom-v1.0.3.json`

---

*Esempio per il corso STEM IFTS — Anno formativo 2024/2025*
