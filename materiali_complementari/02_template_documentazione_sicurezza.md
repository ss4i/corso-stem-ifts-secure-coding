# Template di Documentazione — Controlli di Sicurezza di un Progetto

**Per**: corso IFTS STEM — Specialista nelle Tecniche di Evoluzione e Manutenzione del Software
**Collegamento**: **UF 7** (Tecniche di redazione documentazione tecnica) + UF 9 (Progettazione del software)
**Tipologia**: template **da copiare e compilare** per ogni progetto
**Audience del documento finale**: sviluppatori, security reviewer, DPO, auditor esterni

> Documentare i controlli di sicurezza **non è burocrazia**: è un requisito **legale** (GDPR Art. 32, NIS 2 Art. 21, ISO/IEC 27001, CRA dal 2027) e **operativo** (incident response, audit, compliance).
>
> Questo template fornisce la struttura standard. La compilazione per un progetto reale richiede circa **4-8 ore** di lavoro distribuite tra le fasi del progetto (NON tutto alla fine).

---

## Come usare questo template

1. **Copia** questo file all'avvio del progetto come `SECURITY.md` nella radice del repo.
2. **Compila progressivamente** durante lo sviluppo, non alla fine.
3. **Versionalo con Git** insieme al codice.
4. **Revisionalo** in ogni release maggiore (versione X.0).
5. **Condividilo** con DPO, security team, auditor.

> Le sezioni con `[da compilare]` sono i campi obbligatori. Le sezioni con `(opzionale)` si compilano se applicabili.

---

# Documento di Sicurezza — [Nome del Progetto]

**Versione documento**: 1.0
**Data**: [YYYY-MM-DD]
**Autore**: [Nome / Team]
**Approvato da**: [Nome / Ruolo]
**Prossima revisione**: [data + 12 mesi]

---

## 1. Informazioni generali sul progetto

### 1.1 Identificativo

| Campo | Valore |
|-------|--------|
| **Nome progetto** | [es. Gestionale Clienti v2] |
| **Versione applicativa** | [es. 2.3.1] |
| **Repository Git** | [URL] |
| **Ambiente di esecuzione** | [es. AWS EU-West-1, on-premise Linux] |
| **Lingue/Framework** | [es. Python 3.12 + Flask + PostgreSQL] |
| **Owner** | [team / persona responsabile] |
| **Stakeholder principali** | [committente, utenti, DPO, …] |

### 1.2 Scopo del progetto

[2-3 paragrafi: cosa fa l'applicativo, chi sono gli utenti, quali processi business supporta]

### 1.3 Classificazione dei dati trattati

| Categoria | Esempi | Volume stimato |
|-----------|--------|----------------|
| Dati personali "comuni" | nome, email, indirizzo | [es. ~10.000 record] |
| Dati personali "particolari" (Art. 9 GDPR) | salute, biometrici, opinioni | [se applicabile] |
| Dati di pagamento | carte, IBAN, transazioni | [se applicabile] |
| Dati aziendali confidenziali | strategie, ricette, IP | [se applicabile] |
| Credenziali utenti | password, token, chiavi | sempre |

### 1.4 Norme di riferimento applicabili

- [ ] **GDPR** (Reg. UE 2016/679) — Sì, tratta dati personali
- [ ] **NIS 2** (Dir. UE 2022/2555) — Sì/No (settore soggetto?)
- [ ] **Cyber Resilience Act** (Reg. UE 2024/2847, dal 12/2027) — Sì se prodotto digitale venduto in UE
- [ ] **Legge 4/2004** (accessibilità) — Sì se applicativo PA o servizio al pubblico
- [ ] **PCI DSS** — Sì se tratta carte di pagamento
- [ ] **Direttiva NIS 1** (2016/1148) — superata da NIS 2

---

## 2. Threat Model (sintesi)

### 2.1 Data Flow Diagram

```
[descrivere o allegare DFD]

Esempio testuale:
[Utente] → HTTPS → [Frontend (Flask)] → [Backend API]
                          ↓                      ↓
                    [DB Sessions]        [DB PostgreSQL]
                                                ↓
                                        [Backup S3 cifrato]

Trust boundary:
  - Internet → Frontend (cifratura + validation)
  - Backend → DB (TLS + least privilege)
  - Backend → Backup (cifratura at rest)
```

### 2.2 Minacce identificate (STRIDE)

| ID | Categoria STRIDE | Asset/Componente | Descrizione | Probabilità | Impatto | Rischio | Mitigazione |
|----|-------------------|--------------------|--------------|-------------|---------|---------|-------------|
| T-01 | Spoofing | Login | Account takeover via password rubata | Media | Alto | **Alto** | bcrypt + MFA + rate limit (cap. 5.4) |
| T-02 | Tampering | Sessione | Manipolazione cookie | Bassa | Alto | Medio | Cookie HttpOnly+Secure+SameSite (cap. 5.5) |
| T-03 | Repudiation | Audit | Utente nega operazione | Bassa | Medio | Basso | Audit log immutabile (cap. 7.2) |
| T-04 | Information Disclosure | DB | SQL Injection | Media | Critico | **Critico** | Query parametrizzate (cap. 4.1) |
| T-05 | Denial of Service | Login | Brute force | Alta | Medio | Medio | Rate limit + lockout (cap. 5.4) |
| T-06 | Elevation of Privilege | API | IDOR | Media | Alto | **Alto** | Ownership check (cap. 6.1) |
| ... | ... | ... | ... | ... | ... | ... | ... |

**Scala**:
- Probabilità: Bassa / Media / Alta
- Impatto: Basso / Medio / Alto / Critico
- Rischio = Probabilità × Impatto (matrice 3×4)

### 2.3 Out of scope

[Cosa NON è coperto da questo documento. Es.: sicurezza fisica del datacenter, gestione utenti di Active Directory, ecc.]

---

## 3. Controlli di sicurezza applicati

Per ogni voce: **cosa abbiamo fatto** (non cosa avremmo dovuto fare).

### 3.1 Autenticazione

| Controllo | Stato | Dettaglio | Riferimento codice |
|-----------|-------|-----------|---------------------|
| Hashing password | ✅ Implementato | bcrypt cost=12 | `app/auth.py:42` |
| MFA | ⚠️ Parziale | TOTP solo per admin | `app/auth/mfa.py` |
| Rate limit login | ✅ Implementato | 5/min per IP via flask-limiter | `app/__init__.py:18` |
| Risposta uniforme errori | ✅ Implementato | Stesso messaggio email/password sbagliata | `app/auth.py:67` |
| Session ID | ✅ Implementato | itsdangerous + CSPRNG, 128 bit | Flask default |
| Logout invalidazione lato server | ✅ Implementato | `session.clear()` + DB session record removal | `app/auth.py:120` |
| Password policy | ⚠️ Parziale | Min 12 char, no check HaveIBeenPwned | `app/validators.py:55` |

### 3.2 Autorizzazione

| Controllo | Stato | Dettaglio | Riferimento codice |
|-----------|-------|-----------|---------------------|
| Decorator `@login_required` | ✅ | Su tutti gli endpoint protetti | `app/decorators.py` |
| Ownership check su risorse | ✅ | Pattern `filter_by(owner_id=current_user.id)` | `app/views/*.py` |
| Role-based access (admin) | ✅ | Decorator `@require_role("admin")` | `app/decorators.py:31` |
| Status code corretti (401 vs 403) | ✅ | Test automatici in `tests/test_authz.py` | |
| Mass Assignment protection | ✅ | Pydantic schemas per input | `app/schemas.py` |

### 3.3 Input validation

| Controllo | Stato | Dettaglio | Riferimento codice |
|-----------|-------|-----------|---------------------|
| Schema validation | ✅ | Pydantic per ogni endpoint | `app/schemas/*.py` |
| Whitelist caratteri username | ✅ | Regex `^[a-zA-Z0-9_]{3,20}$` | `app/schemas/user.py:12` |
| Email validation | ✅ | `EmailStr` Pydantic | |
| File upload validation | ✅ | magic + Pillow + max size 5MB | `app/upload.py:23` |
| Lunghezza max stringhe | ✅ | Field constraints Pydantic | |

### 3.4 Output / rendering

| Controllo | Stato | Dettaglio |
|-----------|-------|-----------|
| Template engine con escape automatico | ✅ | Jinja2 default escape |
| Uso di `\|safe` | ⚠️ | Solo in `app/templates/about.html` per testo statico — revisionato |
| Sanitizzazione input HTML | ✅ | `bleach` per i commenti utente | `app/sanitize.py` |

### 3.5 Header HTTP di sicurezza

| Header | Valore configurato |
|--------|---------------------|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains; preload` |
| `Content-Security-Policy` | `default-src 'self'; script-src 'self' 'nonce-...'` |
| `X-Frame-Options` | `DENY` |
| `X-Content-Type-Options` | `nosniff` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=()` |
| `Server` | rimosso (nginx `server_tokens off`) |

Configurazione: vedi `nginx/security-headers.conf` + middleware Flask `app/security.py`.

### 3.6 Cifratura

| Cosa | Algoritmo / configurazione | Riferimento |
|------|-----------------------------|-------------|
| TLS in transito | TLS 1.3 (1.2 minimum), cipher suite forward secrecy | `nginx/ssl.conf` |
| Password storage | bcrypt cost=12 | `app/auth.py` |
| Database at rest | AES-256 (cloud-provider managed) | AWS RDS configuration |
| Backup at rest | AES-256, KMS managed key | S3 + AWS KMS |
| Token CSRF | itsdangerous + secret key | Flask-WTF |
| Session cookie | Flask SECRET_KEY ≥256 bit, ruotata ogni 12 mesi | env `SECRET_KEY` |

### 3.7 Gestione segreti

- ✅ Tutti i segreti in **variabili d'ambiente** (`os.environ[...]`).
- ✅ File `.env` in `.gitignore` (verificato).
- ✅ Pre-commit hook **gitleaks** attivo.
- ✅ Rotazione chiavi: ogni 12 mesi o on-demand dopo incidenti.
- ✅ Provisioning segreti via **AWS Secrets Manager** in produzione.

### 3.8 Database

- ✅ Utente applicativo con permessi `SELECT, INSERT, UPDATE, DELETE` solo sul proprio schema.
- ❌ Nessun `GRANT`, `DROP`, `CREATE ROLE` per l'utente applicativo.
- ✅ Connessione TLS-only (`sslmode=require`).
- ✅ Query parametrizzate ovunque (verificato con `bandit -i`).
- ✅ Backup automatici (daily, retention 30gg + monthly retention 12 mesi).
- ✅ Backup testati con restore mensile.

### 3.9 Logging e audit

| Tipo log | Cosa logghiamo | Retention | Storage |
|----------|----------------|-----------|---------|
| Application log | Errori, info richieste | 30gg | CloudWatch / ELK |
| Audit log | Login, logout, modifiche dati sensibili, modifica permessi | 7 anni | S3 Object Lock immutabile |
| Access log | Tutti gli accessi HTTP | 90gg | CloudWatch |
| Security alert | Brute force, anomalie | 1 anno | SIEM (Wazuh) |

**Formato**: JSON strutturato (Elastic Common Schema).
**PII redacted**: email mascherate, mai password/token completi.
**Correlation ID**: per ogni richiesta, propagato tra microservizi.

### 3.10 Gestione dipendenze (supply chain)

- ✅ **pip-audit** (Python) + **npm audit** (frontend) in CI.
- ✅ **Dependabot** per PR automatiche su CVE.
- ✅ **SBOM** generato a ogni release (formato CycloneDX).
- ✅ Versioni dipendenze **pinned** (no `>=`).
- ✅ Verifica firme pacchetti dove disponibile.
- ⚠️ Aggiornamento Critical CVE entro **7 giorni** (SLA documentato).

### 3.11 Pipeline CI/CD

| Check in CI | Stato |
|-------------|-------|
| Bandit (SAST Python) | ✅ |
| Semgrep (multi-lang SAST) | ✅ |
| pip-audit (SCA) | ✅ |
| gitleaks (secrets) | ✅ |
| pytest + coverage ≥80% | ✅ |
| Trivy (container scan) | ✅ |
| OWASP ZAP baseline (staging) | ✅ |
| Branch protection main | ✅ — richiede review + CI green |
| Signed commits | ⚠️ raccomandato, non obbligatorio |

Pipeline file: `.github/workflows/security.yml`.

### 3.12 Network

- ✅ Application server **non** esposto direttamente — dietro reverse proxy nginx.
- ✅ Database accessibile **solo** dalla subnet privata (Security Group AWS).
- ✅ Bastion host per accesso amministrativo (SSH).
- ✅ WAF (AWS WAF) con managed rules OWASP Top 10.
- ✅ DDoS protection (AWS Shield Standard).

---

## 4. Vulnerabilità note e debiti tecnici

Trasparenza è meglio che fingere di essere perfetti.

| ID | Descrizione | Severity | Workaround attivo? | Data scoperta | Piano fix |
|----|-------------|----------|---------------------|----------------|------------|
| DT-01 | MFA non obbligatoria per utenti normali | Media | No | 2025-09-15 | Q2 2026 (rollout graduale) |
| DT-02 | Dipendenza `lib-x v1.2` con CVE-2025-XXXX (CVSS 6.5) — patch non disponibile | Bassa | WAF rule custom | 2025-11-03 | Sostituzione libreria entro Q1 2026 |

---

## 5. Test di sicurezza

### 5.1 Test automatici

- ✅ Test SQLi: `tests/security/test_sqli.py` (10 test)
- ✅ Test IDOR: `tests/security/test_idor.py` (8 test)
- ✅ Test XSS: `tests/security/test_xss.py` (6 test)
- ✅ Test authz: `tests/security/test_authz.py` (15 test)

Coverage test security: **85%**.

### 5.2 Pentest

| Tipo | Data | Eseguito da | Findings | Status |
|------|------|--------------|----------|--------|
| Internal pentest | 2025-03-15 | Team interno | 3 Medium, 5 Low | Tutti chiusi entro 30gg |
| External pentest | 2025-09-01 | Acme Security | 1 High, 4 Medium | High chiuso entro 7gg |

Report disponibili in `docs/pentest/` (accesso ristretto).

### 5.3 Vulnerability disclosure

Email per disclosure responsabile: `security@example.com`
Policy: vedi `SECURITY.md` (timeline 90gg per fix, riconoscimento ricercatore).

---

## 6. Incident response

### 6.1 Contatti emergenza

| Ruolo | Nome | Telefono | Email |
|-------|------|----------|-------|
| Security lead | [Nome] | [tel 24/7] | [email] |
| DPO | [Nome] | [tel] | [email] |
| CTO | [Nome] | [tel] | [email] |
| Provider hosting (escalation) | AWS Support | - | [Premium account ID] |

### 6.2 Playbook

In caso di sospetto incidente:

1. **T+0**: STOP. Documenta. Non chiudere log.
2. **T+0 a T+1h**: Contenimento (isola, blocca credenziali compromesse).
3. **T+1h a T+24h**: Investigazione + early warning autorità se NIS 2 soggetti.
4. **T+24h a T+72h**: Notifica Garante (GDPR Art. 33) + interessati (Art. 34 se rischio elevato).
5. **T+30gg**: Report finale alle autorità + post-mortem interno.

Vedi: `docs/incident-response-playbook.md`.

---

## 7. Compliance e adempimenti

### 7.1 GDPR

| Adempimento | Stato | Note |
|--------------|-------|------|
| Registro trattamenti (Art. 30) | ✅ | `docs/registro-trattamenti.xlsx` |
| Privacy policy pubblica | ✅ | `/privacy` |
| Cookie banner | ✅ | Conforme TTDSG/Garante |
| Diritti interessati (Art. 15-22) | ✅ | Endpoint `/account/data-export`, `/account/delete` |
| DPIA | ✅ | Eseguita, vedi `docs/dpia.pdf` |
| Procedura breach 72h | ✅ | Documentata + simulazione annuale |
| Pseudonimizzazione dati di test | ✅ | Script `scripts/anonymize.py` |

### 7.2 NIS 2 (se applicabile)

| Adempimento | Stato |
|--------------|-------|
| Registrazione come soggetto NIS 2 | [Sì/No] |
| Misure Art. 21 (10 categorie) | [stato per ognuna] |
| Procedura notifica 24h+72h+30gg | [Sì/No] |
| Formazione cyber annuale dipendenti | [Sì/No] |

### 7.3 CRA (dal dicembre 2027)

[Compilare quando ci si avvicina alla scadenza]

---

## 8. Approvazione e revisione

### 8.1 Storico revisioni

| Versione | Data | Autore | Modifiche |
|----------|------|--------|-----------|
| 1.0 | 2024-09-01 | M. Rossi | Prima stesura |
| 1.1 | 2024-12-10 | M. Rossi | Aggiunti MFA, fix DT-01 |
| 1.2 | 2025-03-20 | L. Bianchi | Post-pentest |
| 2.0 | 2025-09-15 | Team | Major release v2.0 applicativo |

### 8.2 Approvazione

| Ruolo | Nome | Data | Firma |
|-------|------|------|-------|
| Security Lead | [Nome] | [data] | [firma/email approvazione] |
| DPO | [Nome] | [data] | [firma] |
| CTO / Owner | [Nome] | [data] | [firma] |

### 8.3 Prossima revisione

**Data**: [+12 mesi]
**Trigger anticipato**:
- Modifica architetturale significativa
- Incidente di sicurezza
- Cambio normativa (es. CRA in vigore)
- Pentest annuale

---

## 9. Allegati

- [Allegato A] DPIA dettagliata
- [Allegato B] Report pentest [data]
- [Allegato C] Registro trattamenti
- [Allegato D] Pipeline diagram
- [Allegato E] Disaster Recovery Plan
- [Allegato F] SBOM (CycloneDX JSON)

---

# FINE TEMPLATE

---

## Note per chi compila

### Quando compilare ogni sezione

| Sezione | Quando |
|---------|--------|
| 1 Informazioni generali | Inizio progetto |
| 2 Threat Model | Inizio progetto, aggiornare a ogni feature grossa |
| 3 Controlli applicati | Progressivamente durante lo sviluppo |
| 4 Debiti tecnici | Continuo |
| 5 Test sicurezza | Dopo ogni pentest / aggiornamento test suite |
| 6 Incident response | All'inizio + dopo ogni incidente reale |
| 7 Compliance | All'inizio + audit annuali |
| 8 Approvazione | Ad ogni release maggiore |

### Strumenti consigliati per ogni sezione

| Sezione | Strumento |
|---------|-----------|
| DFD (cap. 2.1) | draw.io, Microsoft Threat Modeling Tool, OWASP Threat Dragon |
| Threat model STRIDE (2.2) | Excel/Sheets, Microsoft TMT |
| Schema validation (3.3) | Pydantic, JSON Schema |
| Header sicurezza (3.5) | securityheaders.com, Mozilla Observatory |
| TLS (3.6) | SSL Labs ssltest |
| Logging (3.9) | Elastic Common Schema spec |
| CI/CD (3.11) | GitHub Actions, GitLab CI |
| Pentest (5.2) | OWASP ZAP, Burp Suite, fornitori esterni |
| Compliance (7) | Linee guida Garante, ENISA |

### Errori comuni da evitare

- ❌ Compilare tutto alla fine "perché ora si chiude il progetto". Non leggibile, non utile.
- ❌ Scrivere "siamo sicuri" senza dettagli. Auditor: "dimostrami".
- ❌ Copia-incolla controlli che non sono **veri** nel tuo progetto. Mentire è peggio che ammettere debt.
- ❌ Documento separato dal codice. **Versionalo con Git** nella stessa repo.
- ❌ Non aggiornarlo dopo l'incidente. È quando serve di più.
- ❌ Tenerlo segreto. Almeno il team dev e il DPO devono averlo accessibile.

### Lunghezza tipica

Per un progetto medio:
- **5-10 pagine** PDF compilato.
- **2-4 ore** di scrittura iniziale.
- **30-60 minuti** di aggiornamento ad ogni feature.
- **2-4 ore** di revisione annuale.

---

## Esempio di sezione compilata (per riferimento)

Vedi `02_template_documentazione_sicurezza_ESEMPIO_COMPILATO.md` per un esempio concreto su un progetto fittizio "MiniBlog".

> *Documento per il corso STEM IFTS — Anno formativo 2024/2025*
> *Versione template: 1.0*
