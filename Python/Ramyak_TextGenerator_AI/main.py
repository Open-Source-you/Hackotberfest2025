cat > main.py << 'EOF'
from transformers import pipeline

def generate_text(prompt):
    # uses GPT-2 (small) — downloads model on first run
    generator = pipeline("text-generation", model="gpt2")
    result = generator(prompt, max_length=80, num_return_sequences=1)
    return result[0]['generated_text']

if __name__ == "__main__":
    print("=== Ramyak Text Generator ===")
    prompt = input("Enter a prompt: ")
    print("\nGenerated Text:\n")
    print(generate_text(prompt))
EOF
