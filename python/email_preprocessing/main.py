from process_email import process
import os

raw_dataset_dir = "/home/mathias/Projects/spam_classifier/dataset/raw_dataset"
processed_dataset_spam_dir = "/home/mathias/Projects/spam_classifier/dataset/processed_dataset/spam"
processed_dataset_not_spam_dir = "/home/mathias/Projects/spam_classifier/dataset/processed_dataset/not_spam"

for sub_dir, dirs, files in os.walk(raw_dataset_dir):
    save_dir = processed_dataset_spam_dir
    if sub_dir.lower().find("spam", len(raw_dataset_dir)) == -1:
        save_dir = processed_dataset_not_spam_dir
    for file in files:
        if not file == "cmds":
            f_load = open("{}/{}".format(sub_dir, file), encoding="utf8", errors='ignore')
            file_content = f_load.read()
            f_load.close()
            processed_file_content = process(file_content)

            f_save = open("{}/{}_processed".format(save_dir, file), "w+")
            f_save.write(processed_file_content)
            f_save.close()



