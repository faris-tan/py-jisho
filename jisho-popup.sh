#!/usr/bin/bash
to_lookup=$(xsel | head -n 1)
text=$(py-jisho.py $to_lookup)
gxmessage -borderless -title "jisho" -center "$text"
