# YT Summarizer

> No time to watch your favorite youtuber? No problem! Get the top 10 highlights in the video!

Youtube video summarizer using OpenAI's API, Whisper and Pytube.


⚡ Lean implementation - call it with 5 lines of code!

![image](https://user-images.githubusercontent.com/29677585/236568275-21eb224d-b8a1-4837-af68-bdb3a6f2819f.png)

or use it as a CLI tool

![image](https://user-images.githubusercontent.com/29677585/236568314-9eb8f1aa-bd35-4eb2-bece-0a2af56f1e1d.png)

Made by [@mewtzu](https://twitter.com/mewtzu)

## How to use it

- Install the requirements w/ [poetry](https://github.com/python-poetry/poetry)

```bash
poetry install
```

- Add your OpenAI API key to the `config.yaml` file (or set it as an environment variable)

```bash
export OPENAI_API_KEY="YOUR_API_KEY"
```

- To summarize the video, run:

```bash
python tldw.py summarize "[VIDEO_URL]"
```

- To get the video transcription, run:

```bash
python tldw.py transcribe "[VIDEO_URL]"
```

## Caveats

- You will need to authenticate with your google account in the first run so `pytube` can download the video
- We use the [whisper](https://github.com/openai/whisper) library to transcribe the audio, which uses `ffmpeg`. Refer to
  the [installation instructions](https://github.com/openai/whisper#setup) to install it.
- The transcription is not perfect, but it's a good start. If things are not good enough, try picking a different
  whisper model in `config.yaml`.
- The summarization is not perfect either. If things are not good enough, try picking a different temperature - or tweak
  the prompt at `yt_summarizer/base.py`.
- This is just a demo made in 2 hours, fork it and make it better! :)

-----------------
Feel free to reach out [on Twitter](https://twitter.com/mewtzu) if you have any questions or feedback!
 
