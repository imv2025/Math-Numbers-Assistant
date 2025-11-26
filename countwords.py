# count_words.py
def count_words(filename="readme.md"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()
        words = text.split()
        print(f"Word count in {filename}: {len(words)}")
    except FileNotFoundError:
        print(f"File {filename} not found.")

if __name__ == "__main__":
    count_words("readme.md")
