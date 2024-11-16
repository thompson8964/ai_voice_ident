

download_list = ["https://youtu.be/t1bmPvwe30o", "https://youtu.be/WzEyveqnf78", "https://youtu.be/p75Rue-NKko", "https://youtu.be/yZ8__UVsJ0I", "https://youtu.be/UKijcqIdEaw", "https://youtu.be/BapkTGn1zZk", "https://youtu.be/VYInOyYnD4c", "https://youtu.be/466aCWJSW28", "https://youtu.be/bnnzGKLpuFk", "https://youtu.be/tSctwhjqVuk", "https://youtu.be/XvPAoaO9uZ8", "https://youtu.be/bOykbgW8uwE", "https://youtu.be/WyOEviy3OsY"]
from pytubefix import YouTube
from pytubefix.cli import on_progress

for url in download_list:

    yt = YouTube(url, on_progress_callback=on_progress)
    print(yt.title)

    ys = yt.streams.get_audio_only()
    ys.download(mp3=True)