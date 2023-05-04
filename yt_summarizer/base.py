import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from pprint import pprint

import whisper
import yaml
from colorama import Fore
from colorama import Style
from colorama import init as colorama_init
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from pytube import YouTube

colorama_init()

_fc = lambda color, text: f"{color}{text}{Style.RESET_ALL}"


class WhisperVersion(Enum):
    TINY = 'tiny'
    BASE = 'base'
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'


@dataclass
class YTSumConfig:
    OPENAI_API_KEY: str
    cache_folder: Path
    whisper_model: WhisperVersion

    @classmethod
    def from_yaml(cls, filename):
        with open(filename, 'r') as file:
            yaml_data = yaml.safe_load(file)
        # Check types and coerce if necessary
        for field in cls.__dataclass_fields__.values():
            field_name = field.name
            field_type = field.type

            if field_name in yaml_data and not isinstance(yaml_data[field_name], field_type):
                yaml_data[field_name] = field_type(yaml_data[field_name])

        if "OPENAI_API_KEY" in os.environ:
            yaml_data["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"]

        return cls(**yaml_data)


class YTSum:

    def __init__(self, config_path: Path = Path('config.yaml')):
        self.config = YTSumConfig.from_yaml(str(config_path))
        self.config.cache_folder.mkdir(exist_ok=True)

        self.file_path = None
        self.summary = None
        self.transcription = None

    def download_yt_audio(self, url: str, output_folder: Path = None, filename: str = None):
        """
        Download audio from a YouTube video
        :param url: YouTube URL
        :param output_folder: Folder to save the audio file
        :param filename: Filename to save the audio file
        :return:
        """
        output_path = output_folder if output_folder is not None else self.config.cache_folder
        yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
        f_name = filename if filename is not None else yt.video_id
        f_path = (output_path / filename) if filename is not None else output_path / f"{f_name}.mp4"
        if f_path.exists():
            print(
                f"{_fc(Fore.LIGHTGREEN_EX, 'Found')} {_fc(Fore.LIGHTYELLOW_EX, f_path)}, {_fc(Fore.LIGHTGREEN_EX, 'skipping download')}...")
        else:
            print(f"Downloading audio from {url} to {output_path}/{f_name}.mp4")
            (yt.streams
             .filter(only_audio=True, file_extension="mp4")
             .order_by('abr')
             .last()
             .download(output_path=str(output_path), filename=f"{f_name}.mp4"))
            print(f"Downloaded audio to {output_path}/{f_name}.mp4")
        self.file_path = f_path
        return self

    def transcribe(self, audio_file: Path = None, use_cache: bool = True, verbose: bool = False):
        """
        Summarize an audio file
        :param use_cache: Flag to use cache
        :param audio_file: Path to audio file
        :return:
        """
        cache_path = self.config.cache_folder / f"{self.file_path.stem}_{self.config.whisper_model.value}.txt"
        if use_cache:
            # Find audio transcription in cache
            if cache_path.exists():
                print(
                    f"{_fc(Fore.LIGHTGREEN_EX, 'Found')} {_fc(Fore.LIGHTYELLOW_EX, cache_path)}, {_fc(Fore.LIGHTGREEN_EX, 'skipping transcription')}...")
                self.transcription = cache_path.read_text()
                if verbose:
                    pprint(
                        f"{_fc(Fore.YELLOW, 'Transcription')}: {self.transcription} \n {_fc(Fore.YELLOW, '---------------------')} \n ")
                return self

        model = whisper.load_model(self.config.whisper_model.value)
        audio_path = audio_file if audio_file is not None else self.file_path
        transcription = model.transcribe(str(audio_path))
        if verbose:
            pprint(
                f"{_fc(Fore.YELLOW, 'Transcription')}: {transcription} \n {_fc(Fore.YELLOW, '---------------------')} \n ")
        self.transcription = transcription['text']

        # Save transcription to cache
        with cache_path.open('w') as file:
            file.write(self.transcription)

        return self

    def summarize(self):
        llm = OpenAI(openai_api_key=self.config.OPENAI_API_KEY, temperature=0)
        prompt = PromptTemplate(
            input_variables=["summary"],
            template="""You are a helpful A.I. that summarizes texts.
Given the following text, list the main points. 
The more points the better, but do not list more than 10 points. Do not use information that is outside of the text.

Text: {summary}
""",
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        self.summary = chain.run(self.transcription)
        return self

    def print(self):
        """
        Print the summary
        :return:
        """
        for txt in [self.summary, self.transcription]:
            if txt is not None:
                print('---------------------')
                print(f"{Fore.LIGHTBLUE_EX}{txt}{Style.RESET_ALL}")
                return self
        print("No summary or transcription found")
        return self
