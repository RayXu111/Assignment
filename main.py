def count_and_replace_terrible(input_text):
    word_count = 0
    new_text = ""

    words = input_text.split()
    replace_terrible = False

    for word in words:
        cleaned_word = word.strip(".,?!")
        if cleaned_word == "terrible":
            word_count += 1
            if replace_terrible:
                new_text += "pathetic "
            else:
                new_text += "marvellous "
            replace_terrible = not replace_terrible
        else:
            new_text += word + " "

    return word_count, new_text.strip()

def main():
    with open("file_to_read.txt", "r") as file:
        input_text = file.read()

    word_count, new_text = count_and_replace_terrible(input_text)

    with open("result.txt", "w") as file:
        file.write(new_text)

    print("Total occurrences of 'terrible':", word_count)
    print("Modified text written to 'result.txt'.")

if __name__ == "__main__":
    main()