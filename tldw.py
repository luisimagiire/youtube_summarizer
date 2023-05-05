import warnings

# Suppress all warnings just for the CLI
warnings.filterwarnings("ignore")

from pathlib import Path

import fire

from yt_summarizer.base import YTSum


class YTSummarizerCLI(object):
    def summarize(self, yt_url: str, config_path: str = 'config.yaml'):
        """
        Summarize the audio file from a YouTube video and print the summary
        :param yt_url: The YouTube URL
        :param config_path: config.yaml path
        """
        (YTSum(config_path=Path(config_path))
         .download_yt_audio(yt_url)
         .transcribe()
         .summarize()
         .print())

    def transcribe(self, yt_url: str, config_path: str = 'config.yaml'):
        """
        Transcribe the audio file from a YouTube video and print the transcription
        :param yt_url: YouTube URL
        :param config_path: config.yaml path
        """
        (YTSum(config_path=Path(config_path))
         .download_yt_audio(yt_url)
         .transcribe()
         .print())


if __name__ == '__main__':
    fire.Fire(YTSummarizerCLI)
