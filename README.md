# Corso STEM IFTS — Secure Coding (materiali complementari)

**Corso di riferimento**: IFTS **STEM — Specialista nelle Tecniche di Evoluzione e Manutenzione del Software**
**Codice progetto**: 321386 — Matricola 2025IS0766
**Partenariato**: Assoservizi S.r.l. · Polo Tecnologico Manetti Porciatti · Università di Siena · Fondazione ITS Prodigi · Opus Automazione S.p.A.
**Durata corso completo**: 990 ore (564 aula + 30 accompagnamento + 396 stage)
**Autore materiali**: Ing. Alessandro Manneschi
**Anno formativo**: 2024/2025

---

## Cosa contiene questo repository

Materiali **complementari** al modulo Secure Coding (~16h) del corso IFTS, da fornire agli allievi a integrazione delle UF principali (UF 9, 10, 11, 12).

> Questi documenti **non sostituiscono** le UF del corso — le **integrano** con strumenti operativi pratici (checklist da consultare durante lo sviluppo, template documentali, linee guida per l'uso responsabile dell'AI).

### Cartella `materiali_complementari/`

| # | File | Tipologia | Pagine ~ | Collegamento UF |
|---|------|-----------|----------|------------------|
| 1 | `01_checklist_secure_coding.md` | Guida rapida di consultazione | 20+ | UF 10, 11, 12 |
| 2 | `02_template_documentazione_sicurezza.md` | Template documentale | 15+ | **UF 7** |
| 2-bis | `02_template_documentazione_sicurezza_ESEMPIO_COMPILATO.md` | Esempio compilato (MiniBlog) | 12+ | UF 7 + 9 |
| 3 | `03_guida_validazione_codice_IA.md` | Linee guida uso AI | 25+ | UF 6 + 10 |

Tutti i documenti sono disponibili sia in **markdown** (per modifica/versioning) sia in **`.docx`** (per distribuzione agli allievi e stampa).

---

## Sintesi dei tre documenti

### 1. Checklist "Secure Coding"

Guida rapida **da tenere a portata di mano mentre si scrive codice**. Coperti:

- Validazione input, output, accesso a database
- Autenticazione, autorizzazione, gestione segreti
- Errori e logging
- Checklist pre-commit e pre-deploy

**Multi-linguaggio**: Python, Java, JavaScript/TypeScript, PHP, CSS (tutti i linguaggi previsti dal corso STEM nell'UF 10).

Esempi `✅ corretto` / `❌ anti-pattern` per ogni controllo.
Inclusa versione "tasca" stampabile su una pagina.

### 2. Template di Documentazione

Template `SECURITY.md` da copiare in ogni progetto e compilare **progressivamente** durante lo sviluppo (non alla fine).

Struttura in 9 sezioni:

1. Informazioni generali
2. Threat Model (DFD + STRIDE)
3. Controlli applicati (auth, authz, validation, output, header, cifratura, ecc.)
4. Vulnerabilità note e debiti tecnici
5. Test di sicurezza
6. Incident response
7. Compliance (GDPR, NIS 2, CRA)
8. Approvazione e revisione
9. Allegati

Affiancato da un **esempio compilato su un progetto fittizio "MiniBlog"** come riferimento pratico per gli allievi.

Collegamento esplicito con **UF 7 — Tecniche di redazione documentazione tecnica**.

### 3. Guida all'uso dell'IA

Linee guida per validare il codice suggerito da strumenti di AI generativa (GitHub Copilot, Claude, ChatGPT, Gemini, Cursor).

Argomenti:

- I 7 errori tipici del codice AI (SQLi con f-string, hash deboli, IDOR, ecc.)
- Workflow di validazione in 4 step
- Checklist per ogni suggerimento
- Tecniche di prompting per la sicurezza
- 4 casi pratici corretti (login, modifica profilo, esecuzione comandi, upload file)
- Uso etico e legale (IP, segreti nei prompt, GDPR, EU AI Act)
- Quando **NON** usare l'AI (crittografia, sicurezza critica)

Collegamento con **UF 6 — Applicativi informatici** (parte "Opportunità e rischi dell'intelligenza artificiale") e con UF 10/12.

---

## Come usare i materiali (per il docente)

1. **Distribuire la Checklist** all'inizio del modulo di programmazione (UF 10). Stamparla. Tenerla appesa.
2. **Spiegare il Template documentale** durante UF 7. Far iniziare ai discenti la compilazione del proprio `SECURITY.md` sul progetto di stage.
3. **Discutere la Guida AI** all'inizio del corso (UF 6 tocca AI). Aggiornarla quando emergono nuovi tool / vulnerabilità.

### Suggerimenti per gli esercizi

- Far revisionare codice generato da AI usando la **Guida AI** (4 casi pratici come template)
- Far compilare il **Template documentale** sul progetto di stage (parte dell'output finale UF 7)
- Verificare aderenza alla **Checklist Secure Coding** nelle code review

---

## Conversione e manutenzione

### Conversione markdown → docx

I `.docx` sono generati con [pandoc](https://pandoc.org) usando come reference template `dispensa_code_security_v8.docx` per stile uniforme:

```bash
for f in materiali_complementari/*.md; do
  pandoc "$f" --reference-doc=template.docx -o "${f%.md}.docx" \
    --toc --toc-depth=2 -V geometry:margin=2cm
done
```

### Manutenzione

I documenti sono **vivi**: vanno aggiornati periodicamente.

| Frequenza | Cosa rivedere |
|-----------|----------------|
| Annuale | OWASP Top 10, riferimenti normativi |
| Annuale | OWASP LLM Top 10 (per la guida AI) |
| Quando esce nuovo strumento | Tool list nella guida AI |
| Trimestrale | Linguaggi/framework nella Checklist (versioni) |
| Quando arrivano nuovi casi Garante | Esempi nel Template |

---

## Crediti

- **Autore**: Ing. Alessandro Manneschi (alessandro.manneschi@gmail.com)
- **Per**: SS4I S.r.l. · ITS Prodigi · Polo Tecnologico Manetti Porciatti · Assoservizi
- **Licenza**: materiale ad uso didattico interno corso IFTS STEM

---

## Riferimenti

- Abstract del corso completo: `Abstract_STEM.pdf`
- OWASP: https://owasp.org
- Garante Privacy: https://www.garanteprivacy.it
- ENISA: https://www.enisa.europa.eu
- NIST: https://csrc.nist.gov

---

> **Versione**: 1.0
> **Data**: maggio 2026
