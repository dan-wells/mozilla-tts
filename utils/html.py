import os
import sys
import textwrap
from glob import glob

def make_audio_page(audios, transcripts=None, html_out='audios.html'):
    html_head = textwrap.dedent("""\
    <!DOCTYPE HTML>
    <html>
    <head>
    <meta charset="utf-8"/>
    <style type="text/css">
      table {text-align:left;}
      th, td {padding:5px;}
    </style>
    </head>
    <body>
    """)
    table_head = textwrap.dedent("""\
    <table>
      <tr><th>Audio</th><th>Transcript</th></tr>
    """)
    audio_col = "  <tr><td><audio controls><source src='{}' type='audio/wav'></audio></td>"
    transcript_col = "<td>{}</td></tr>\n"
    html_tail = textwrap.dedent("""\
    </table>
    </body>
    </html>""")

    with open(html_out, 'w', encoding='utf-8') as html:
        html.write(html_head)
        html.write(table_head)
        if (type(audios) != list) and (os.path.isdir(audios)):
            audios = glob("{}/**/*.wav".format(audios), recursive=True)
        if transcripts is None:
            # assume audios are named for text content
            transcripts = [os.path.basename(i) for i in audios]
        for audio, transcript in zip(audios, transcripts):
            audio_rel = os.path.relpath(audio, start=os.path.dirname(html_out))
            html.write(audio_col.format(audio_rel))
            html.write(transcript_col.format(transcript))
        html.write(html_tail)

