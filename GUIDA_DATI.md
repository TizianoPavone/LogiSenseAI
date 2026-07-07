# 📊 Guida alla Preparazione dei Dati

Per garantire che **LogiSense AI** analizzi correttamente il tuo magazzino, il file caricato (in formato `.csv` o `.xlsx`) deve contenere le seguenti colonne.

### Struttura del File
Assicurati che le intestazioni delle colonne corrispondano esattamente a queste (il sistema è sensibile alle maiuscole/minuscole):

| Nome Colonna | Descrizione |
| :--- | :--- |
| `SKU` | Codice univoco identificativo dell'articolo. |
| `Prodotto` | Nome o descrizione dell'articolo. |
| `Giacenza Attuale` | Numero di unità attualmente in magazzino. |
| `Domanda Annuale` | Stima delle unità vendute in un anno. |
| `Costo Unitario` | Prezzo di acquisto per singola unità. |
| `Costo Ordine` | Costo fisso per ogni ordine effettuato. |
| `Lead Time (gg)` | Giorni necessari al fornitore per consegnare. |
| `Scorta Sicurezza` | Numero minimo di unità da tenere sempre in stock. |

### Suggerimenti per l'importazione
* **Formato CSV**: Se usi un file CSV, assicurati che sia separato da virgole.
* **Excel**: Puoi caricare direttamente file `.xlsx`, il sistema estrarrà automaticamente la prima scheda (foglio) disponibile.
* **Pulizia**: Assicurati che non ci siano righe vuote o formule complesse nelle celle.
