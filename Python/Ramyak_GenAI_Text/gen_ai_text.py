from transformers import pipeline

def main():
    generator = pipeline('text-generation', model='gpt2')
    prompt = input("Enter a prompt: ")
    results = generator(prompt, max_length=50, num_return_sequences=1)
    print("\nGenerated Text:\n")
    for r in results:
        print(r['generated_text'])

if __name__ == "__main__":
    main()

