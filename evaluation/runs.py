## Backend for running the models
from transformers import AutoModelForVision2Seq, AutoProcessor
from peft import PeftModel
from PIL import Image
import torch

class ModelRuns():
    def __init__(self, model_id: str, adapter_path: str = ""):
        """
        Args:
            model_id :  Huggingface ID for the model
            adapter_path: If using the fine tuned version, specify the path to the adapter directory
            image_path : Path to the image
            prompt : Prompt value (string)
        """

        self.model_id = model_id
        self.adapter_path = adapter_path

        # Load Model and Processor
        self.model = AutoModelForVision2Seq.from_pretrained(self.model_id, device_map="auto", torch_dtype=torch.float16)
        if self.adapter_path:
            self.model = PeftModel.from_pretrained(self.model, self.adapter_path, device_map="auto", torch_dtype=torch.float16)

        self.processor = AutoProcessor.from_pretrained(self.model_id, device_map="auto")

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def generate_response(self, image_path: str, prompt: str):
        """
        Args:
            image_path: Path to the image
            prompt: Prompt value (string)
        Returns:
            response: Model Response (After Processing it to a single word)
        """

        image = Image.open(image_path).convert("RGB")
        inputs = self.processor(prompt, image, return_tensors="pt").to(self.device)
        outputs = self.model.generate(**inputs, max_new_tokens=10, do_sample=False)
        response = self.processor.decode(output[0][2:], skip_special_tokens=True)

        return response
