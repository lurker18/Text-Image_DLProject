from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def summarize_and_save(input_file, output_file, tokenizer, model):
    # Read data from file
    with open(input_file, "r", encoding="utf-8") as f:
        data = f.read()

    inputs = tokenizer.encode("summarize: " + data, return_tensors="pt", max_length=8196, truncation=True)
    summary_ids = model.generate(inputs,
                                 max_length=500,
                                 min_length=50,
                                 length_penalty=2.0,
                                 num_beams=4,
                                 repetition_penalty = 10.1,
                                 early_stopping=True)

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    print(f"Original Text ({input_file}):\n", data)
    print(f"\nSummarized Text ({input_file}):\n", summary)

    with open(output_file, 'w', encoding='utf-8') as output_file:
        output_file.write(summary)

data_types = ['상의_가격', '상의_디자인', '상의_배송', '상의_색감', '상의_재질', '상의_핏']

tokenizer = AutoTokenizer.from_pretrained("lcw99/t5-base-korean-text-summary")
model = AutoModelForSeq2SeqLM.from_pretrained("lcw99/t5-base-korean-text-summary")

for data_type in data_types:
    input_file_path = f"Text_data/test_data_{data_type}.txt"
    output_file_path = f"Text_Summarization/Results/sum_test_data_{data_type}.txt"
    summarize_and_save(input_file_path, output_file_path, tokenizer, model)