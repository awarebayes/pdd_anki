import os
from pathlib import Path
import genanki
import json

base_id = 104465

A_B_images_path = "pdd_json/images/A_B"
C_D_images_path = "pdd_json/images/C_D"

images_ab = [os.path.join(A_B_images_path,  i) for i in os.listdir(A_B_images_path)]
images_cd = [os.path.join(C_D_images_path,  i) for i in os.listdir(C_D_images_path)]
images = images_ab + images_cd

deck_names = []
deck_dirs = ["A_B/tickets", "A_B/topics", "C_D/tickets", "C_D/topics"]
for i in deck_dirs:
    for billet in os.listdir("pdd_json/questions/" + i):
        deck_names.append(i+"/"+billet.replace(".json", ""))

decks = {
    name: genanki.Deck(base_id + (hash(name) % 10_000_000) + sum(map(ord, name)), "PDD::" + name.replace("/", "::"))
    for name in deck_names
}
my_package = genanki.Package(decks.values())
my_package.media_files = images

my_model = genanki.Model(
  1091735104,
  'Simple Model with Media',
  fields=[
    {'name': 'Name'},
    {'name': 'Question'},
    {'name': 'Answer'},
    {'name': 'MyMedia'},                                  # ADD THIS
  ],
  templates=[
    {
      'name': '{{Name}}',
      'qfmt': '{{Question}}<br>{{MyMedia}}',              # AND THIS
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
  ])


questions_dir = Path("pdd_json/questions")

notes = []
for deck_name in decks.keys():
    deck_items_path = questions_dir / (deck_name + ".json")
    deck_item_json = json.load(open(deck_items_path, encoding="utf8"))
    for question in deck_item_json:
        if "no_image" in question['image']:
            image = ""
        else:
            image = Path(question['image']).name
            image = f'<img src="{image}">'
        question_text = question['question'] + "<br> <ol>"
        correct_answer = ""
        for index, answer in enumerate(question["answers"]):
            question_text += f"<li> {answer['answer_text']} </li>"
            if answer["is_correct"]:
                correct_answer = answer["answer_text"]
        question_text += "</ol>"
        answer_text = f"{question['correct_answer']} - {correct_answer} <br> {question['answer_tip']}"
        my_note = genanki.Note(
            model=my_model,
            fields=[
                f"{question['title']} - {question['question']}",
                question_text,
                answer_text,
                image,
            ])
        decks[deck_name].add_note(my_note)

my_package.write_to_file("pdd.apkg")
print("Generated")
