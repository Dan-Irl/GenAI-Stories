import os, random
import json
from openai import OpenAI
from pathlib import Path
from classes.support_functions import (
    change_pitch_without_affecting_speed,
    download_images,
)


class OpenAI_Generation:

    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

        self.script = None

        self.script_model = os.environ.get("SCRIPT_MODEL")
        self.image_model = os.environ.get("IMAGE_MODEL")

        self.characters = {}

        self.images_url = []

    def generate_script_promt(self):

        # Reads the script_promt file that gets passed to the system role
        script_promt_path = os.environ.get("OPEN_AI_SCRIPT_PROMT")
        with open(script_promt_path, "r", encoding="utf-8") as file:
            script_promt = file.read()

        # pick random text file from data\writing_promts
        # TODO: Instead of random choice, we pass a path to the method
        writing_promt_path = random.choice(os.listdir("data/writing_promts"))
        with open(
            f"data/writing_promts/{writing_promt_path}", "r", encoding="utf-8"
        ) as file:
            writing_promt = file.read()

        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": script_promt},
                {"role": "user", "content": writing_promt},
            ],
            model="gpt-4-turbo-preview",
            response_format={"type": "json_object"},
        )

        # get the script from the chat completion and convert it to a json object
        script = chat_completion.choices[0].message.content
        script = json.loads(script)

        # move the used writing promt text file to the used_promts folder
        # os.rename(
        #     f"data/writing_promts/{writing_promt_path}",
        #     f"data/used_writing_promts/{writing_promt_path}",
        # )

        # TODO: remove this temporary save of the script
        # save script as a json file
        with open("data/stories/generated_script.json", "w", encoding="utf-8") as file:
            json.dump(
                script,
                file,
            )

        for character in script["characters"].keys():
            self.characters[character] = script["characters"][character]

        print("Finished generating script")

        self.script = script
        # returns the system response from the chat completion
        return script

    def generate_images(self):

        with open("D:\Repos\GenAI-Stories\promts\image_promt.txt", "r") as f:
            image_promt_prefix = f.read()

        for scene in self.script["scenes"]:
            prommt = {
                "character_descriptions": [
                    self.characters[character] for character in scene["characters"]
                ],
                "scene_description": scene["scene_description"],
            }

            image_promt = image_promt_prefix + json.dumps(prommt)

            response = self.client.images.generate(
                model="dall-e-3",
                prompt=image_promt,
                size="1024x1024",
                quality="standard",
                n=1,
            )

            print("image done")

            self.images_url.append(response.data[0].url)

        # save the image urls to a image files
        download_images(self.images_url, "data/stories")

    def generate_audio(self):
        i = 0

        for scene in self.script["scenes"]:
            for dialogue in scene["dialogue"]:

                character = dialogue["character"]
                dialogue = dialogue["dialogue"]

                try:

                    if character == list(self.characters.keys())[0]:
                        voice = "fable"

                    if character == list(self.characters.keys())[1]:
                        voice = "onyx"

                except:
                    voice = "fable"

                response = self.client.audio.speech.create(
                    model="tts-1", voice=voice, input=dialogue
                )
                speech_file_path = f"data/stories/dialogue_{i}.mp3"
                response.stream_to_file(speech_file_path)

                if character == list(self.characters.keys())[1]:
                    change_pitch_without_affecting_speed(speech_file_path, -4)

                i += 1
