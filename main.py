from classes.openai_generation import OpenAI_Generation

openAI = OpenAI_Generation()

script = openAI.generate_script_promt()

openAI.generate_images()

openAI.generate_audio()
