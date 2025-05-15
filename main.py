from flask import Flask, request, jsonify
import torch
from transformers import AutoTokenizer
from parler_tts import ParlerTTSForConditionalGeneration
import soundfile as sf
import os
import sys
import time

# Add the root of the project to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dbmodule.dbmodule import GoogleDriveAudioManager

# Initialize Flask app
app = Flask(__name__)

# Load the model once on app startup
class TextToSpeech:
    def __init__(self, model_name="ai4bharat/indic-parler-tts"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")

        dtype = torch.float16 if self.device == "cuda" else torch.float32
        self.model = ParlerTTSForConditionalGeneration.from_pretrained(model_name, torch_dtype=dtype).to(self.device)

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.description_tokenizer = AutoTokenizer.from_pretrained(self.model.config.text_encoder._name_or_path)

        # Warm-up run (optional)
        dummy_desc = self.description_tokenizer("test", return_tensors="pt").to(self.device)
        dummy_prompt = self.tokenizer("test", return_tensors="pt").to(self.device)
        with torch.inference_mode():
            _ = self.model.generate(
                input_ids=dummy_desc.input_ids,
                attention_mask=dummy_desc.attention_mask,
                prompt_input_ids=dummy_prompt.input_ids,
                prompt_attention_mask=dummy_prompt.attention_mask
            )

    def generate_audio(self, text, description, local_output="output.wav"):
        description_input_ids = self.description_tokenizer(description, return_tensors="pt").to(self.device)
        prompt_input_ids = self.tokenizer(text, return_tensors="pt").to(self.device)

        with torch.inference_mode():
            generation = self.model.generate(
                input_ids=description_input_ids.input_ids,
                attention_mask=description_input_ids.attention_mask,
                prompt_input_ids=prompt_input_ids.input_ids,
                prompt_attention_mask=prompt_input_ids.attention_mask
            )

        audio_arr = generation.cpu().numpy().squeeze()
        sf.write(local_output, audio_arr, self.model.config.sampling_rate)

        manager = GoogleDriveAudioManager()
        file_id = manager.upload_audio(local_output)

        return file_id

# Instantiate the class (done only once to avoid reloading on every request)
tts = TextToSpeech()

# API Endpoint
@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    data = request.json

    # Validation
    if not data or 'text' not in data or 'description' not in data:
        return jsonify({"error": "Please provide 'text' and 'description'"}), 400

    text = data['text']
    description = data['description']

    try:
        start = time.time()
        file_id = tts.generate_audio(text, description)
        end = time.time()
        return jsonify({
            "file_id": file_id,
            "time_taken": f"{end - start:.2f} seconds"
        }), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    app.run(host='0.0.0.0', port=1000, debug=True)

