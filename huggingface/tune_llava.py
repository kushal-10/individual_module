# flake8: noqa
# Copyright 2024 The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
from contextlib import nullcontext

TRL_USE_RICH = os.environ.get("TRL_USE_RICH", False)

from trl.commands.cli_utils import init_zero_verbose, SFTScriptArguments, TrlParser

if TRL_USE_RICH:
    init_zero_verbose()
    FORMAT = "%(message)s"

    from rich.console import Console
    from rich.logging import RichHandler

import torch
from accelerate import Accelerator
from datasets import load_dataset

from tqdm.rich import tqdm
from transformers import AutoTokenizer, AutoProcessor, LlavaForConditionalGeneration

from trl import (
    ModelConfig,
    RichProgressCallback,
    SFTConfig,
    SFTTrainer,
    get_peft_config,
    get_quantization_config,
    get_kbit_device_map,
)

from PIL import Image
import io
from huggingface.template import apply_llava_template

tqdm.pandas()

if TRL_USE_RICH:
    logging.basicConfig(format=FORMAT, datefmt="[%X]", handlers=[RichHandler()], level=logging.INFO)


if __name__ == "__main__":
    parser = TrlParser((SFTScriptArguments, SFTConfig, ModelConfig))
    sft_script_args, training_args, model_config = parser.parse_args_and_config()
    training_args.gradient_checkpointing_kwargs = dict(use_reentrant=False)
    # Force use our print callback
    if TRL_USE_RICH:
        training_args.disable_tqdm = True
        console = Console()

    ################
    # Model, Tokenizer & Processor
    ################

    torch_dtype = (
        model_config.torch_dtype
        if model_config.torch_dtype in ["auto", None]
        else getattr(torch, model_config.torch_dtype)
    )
    quantization_config = get_quantization_config(model_config)
    model_kwargs = dict(
        revision=model_config.model_revision,
        trust_remote_code=model_config.trust_remote_code,
        attn_implementation=model_config.attn_implementation,
        torch_dtype=torch_dtype,
        device_map="auto",
        quantization_config=quantization_config,
    )
    tokenizer = AutoTokenizer.from_pretrained(model_config.model_name_or_path, use_fast=False)
    processor = AutoProcessor.from_pretrained(model_config.model_name_or_path)
    processor.tokenizer = tokenizer

    model = LlavaForConditionalGeneration.from_pretrained(model_config.model_name_or_path, **model_kwargs)

    ################
    # Create a data collator to encode text and image pairs
    ################

    class LLavaDataCollator:
        def __init__(self, processor):
            self.processor = processor

        def __call__(self, examples):
            texts = []
            images = []
            for example in examples:
                if len(example["images"]) > 1:
                    raise ValueError("This collator only supports one image per example")
                messages = example["messages"]
                text = apply_llava_template(messages)
                texts.append(text)
                byte_image = example["images"][0]['bytes']
                image_data = io.BytesIO(byte_image)
                pil_image = Image.open(image_data)
                images.append(pil_image)

            batch = self.processor(texts, images, return_tensors="pt", padding=True)

            labels = batch["input_ids"].clone()
            if self.processor.tokenizer.pad_token_id is not None:
                labels[labels == self.processor.tokenizer.pad_token_id] = -100
            batch["labels"] = labels

            return batch

    data_collator = LLavaDataCollator(processor)

    ################
    # Dataset
    ################
    raw_datasets = load_dataset(sft_script_args.dataset_name)
    train_dataset = raw_datasets[sft_script_args.dataset_train_split]
    eval_dataset = raw_datasets[sft_script_args.dataset_test_split]
                        
    ################
    # Optional rich context managers
    ###############
    init_context = nullcontext() if not TRL_USE_RICH else console.status("[bold green]Initializing the SFTTrainer...")
    save_context = (
        nullcontext()
        if not TRL_USE_RICH
        else console.status(f"[bold green]Training completed! Saving the model to {training_args.output_dir}")
    )

    ################
    # Training
    ################
    with init_context:
        trainer = SFTTrainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            dataset_text_field="text",  # need a dummy field
            tokenizer=tokenizer,
            peft_config=get_peft_config(model_config),
            callbacks=[RichProgressCallback] if TRL_USE_RICH else None,
            data_collator=data_collator,
            dataset_kwargs={"skip_prepare_dataset": True},
        )

    trainer.train()

    with save_context:
        trainer.save_model(training_args.output_dir)
        # trainer.push_to_hub()
        # if Accelerator().is_main_process:
        #     processor.push_to_hub(training_args.hub_model_id)