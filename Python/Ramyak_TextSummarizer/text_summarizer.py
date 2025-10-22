from transformers import pipeline

def main():
    summarizer = pipeline("summarization")
    text = input("Enter text to summarize: ")
    summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
    print("\nSummary:\n", summary[0]['summary_text'])

if __name__ == "__main__":
    main()

