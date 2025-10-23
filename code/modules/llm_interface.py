"""
Modulo di interfaccia con Ollama LLM locale per AEON
Permette di generare testi, policy, report e dialoghi AI.
"""
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.1:latest"

def ollama_generate(prompt: str, model: str = OLLAMA_MODEL) -> str:
    """Invia un prompt a Ollama e restituisce la risposta generata."""
    response = requests.post(
        OLLAMA_URL,
        json={"model": model, "prompt": prompt},
        stream=True
    )
    if response.ok:
        result = ""
        for line in response.iter_lines():
            if line:
                try:
                    import json
                    obj = json.loads(line)
                    result += obj.get("response", "")
                except Exception:
                    continue
        return result
    return "[Errore LLM]"

# Esempio di funzione per generare una policy

def generate_policy(data: dict) -> dict:
    prompt = (
        "Sei l'AI di una colonia marziana. "
        "Analizza questi dati e genera una policy descrittiva in una sola riga:\n"
        f"{data}\n"
        "Rispondi solo con la frase della policy, senza spiegazioni."
    )
    text = ollama_generate(prompt)
    return {"descrizione": text.strip()}

# Puoi aggiungere altre funzioni per report, dialoghi, ecc.
