import genanki
import os
import random
import shutil
import tempfile

def create_temp_directory_with_images(question_image_dir, answer_image_dir, deck_type):
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    print(f"Temporary directory created at: {temp_dir}")

    # Copy question images with "question_" prefix
    for img in os.listdir(question_image_dir):
        src = os.path.join(question_image_dir, img)
        dst = os.path.join(temp_dir, f"question_{deck_type}_{img}")
        shutil.copy(src, dst)

    # Copy answer images with "answer_" prefix
    for img in os.listdir(answer_image_dir):
        src = os.path.join(answer_image_dir, img)
        dst = os.path.join(temp_dir, f"answer_{deck_type}_{img}")
        shutil.copy(src, dst)

    return temp_dir

# gen random ID:
# python3 -c "import random; print(random.randrange(1 << 30, 1 << 31))"

MODEL_ID = random.randrange(1 << 30, 1 << 31)

my_model = genanki.Model(
    MODEL_ID,
    'Image Flashcard',
    fields=[
        {'name': 'QuestionImage'},
        {'name': 'AnswerImage'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '<div class="image-container">{{QuestionImage}}</div>',
            'afmt': '<div class="image-container">{{QuestionImage}}</div><hr id="answer"><div class="image-container">{{AnswerImage}}</div>',
        },
    ],
    css="""
    .card {
        font-family: arial;
        font-size: 20px;
        text-align: center;
        color: black;
        background-color: white;
    }
    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
    }
    img {
        max-width: 100%;
        max-height: 100%;
    }
    """
)

def create_anki_image_deck(question_image_dir, answer_image_dir, deck_name):
    deck_type = question_image_dir.split("/")[-1]
    # should be very low chance of collision
    deck_id = random.randrange(1 << 30, 1 << 31)

    # Create the Anki deck
    my_deck = genanki.Deck(
        deck_id,
        deck_name
    )

    question_images = sorted([f for f in os.listdir(question_image_dir) if f.endswith('png')])
    answer_images = sorted([f for f in os.listdir(answer_image_dir) if f.endswith('png')])

    # Create a temporary directory and populate it with images
    temp_dir = create_temp_directory_with_images(question_image_dir, answer_image_dir, deck_type)

    try:
        # Collect images
        question_images = sorted([f for f in os.listdir(temp_dir) if f.startswith('question_')])
        answer_images = sorted([f for f in os.listdir(temp_dir) if f.startswith('answer_')])

        # Ensure the question and answer images are properly paired
        if len(question_images) != len(answer_images):
            raise ValueError("Number of question and answer images do not match.")

        # Add notes (cards) to the deck
        for question_image, answer_image in zip(question_images, answer_images):
            print(f"Adding Note: Question = {question_image}, Answer = {answer_image}")
            note = genanki.Note(
                model=my_model,
                fields=[f'<img src="{question_image}">', f'<img src="{answer_image}">']
            )
            my_deck.add_note(note)

        # Create a package and add media files
        my_package = genanki.Package(my_deck)

        # Add all images to the media files
        my_package.media_files = [
            os.path.join(temp_dir, img) for img in question_images + answer_images
        ]

        # Write the .apkg file
        output_dir = "ankidecks/Corners"
        os.makedirs(output_dir, exist_ok=True)
        output_file = f'{output_dir}/{deck_name}.apkg'
        my_package.write_to_file(output_file)

    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir)
        print(f"Temporary directory at {temp_dir} deleted.")


    print(f"Anki deck created: {output_file}")

create_anki_image_deck("images/top_U", "images/answer_U", "Top U")
create_anki_image_deck("images/left_U", "images/answer_U", "Left U")
create_anki_image_deck("images/right_U", "images/answer_U", "Right U")

create_anki_image_deck("images/bottom_D", "images/answer_D", "Bottom D")
create_anki_image_deck("images/left_D", "images/answer_D", "Left D")
create_anki_image_deck("images/right_D", "images/answer_D", "Right D")

create_anki_image_deck("images/letter_D", "images/answer_D", "Letter D")
create_anki_image_deck("images/letter_U", "images/answer_U", "Letter U")