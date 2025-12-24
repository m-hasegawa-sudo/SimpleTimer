import streamlit as st
from datetime import datetime, time
import json

st.set_page_config(page_title="タイムログ", layout="centered")

# 現在の日付を取得
today = datetime.now().date()

# セッションストレージの初期化
if 'is_tracking' not in st.session_state:
    st.session_state.is_tracking = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'sessions' not in st.session_state:
    st.session_state.sessions = []
if 'last_date' not in st.session_state:
    st.session_state.last_date = today

# 日付が変わったらリセット
if st.session_state.last_date != today:
    st.session_state.sessions = []
    st.session_state.is_tracking = False
    st.session_state.start_time = None
    st.session_state.last_date = today

st.title("⏱️ タイムログ")

# スタート/ストップボタン
if st.session_state.is_tracking:
    if st.button("⏸️ 停止", use_container_width=True, type="primary"):
        end_time = datetime.now()
        duration = (end_time - st.session_state.start_time).total_seconds()
        st.session_state.sessions.append({
            'start': st.session_state.start_time.isoformat(),
            'end': end_time.isoformat(),
            'duration': duration
        })
        st.session_state.is_tracking = False
        st.session_state.start_time = None
        st.rerun()
else:
    if st.button("▶️ 開始", use_container_width=True, type="primary"):
        st.session_state.start_time = datetime.now()
        st.session_state.is_tracking = True
        st.rerun()

# 現在計測中の時間を表示
if st.session_state.is_tracking:
    current_duration = (datetime.now() - st.session_state.start_time).total_seconds()
    st.info(f"計測中: {int(current_duration // 3600):02d}:{int((current_duration % 3600) // 60):02d}:{int(current_duration % 60):02d}")

# 合計時間の計算
total_seconds = sum(session['duration'] for session in st.session_state.sessions)
if st.session_state.is_tracking:
    total_seconds += (datetime.now() - st.session_state.start_time).total_seconds()

hours = int(total_seconds // 3600)
minutes = int((total_seconds % 3600) // 60)
seconds = int(total_seconds % 60)

# 合計時間を表示
st.markdown("---")
st.markdown(f"### 合計時間")
st.markdown(f"# {hours:02d}:{minutes:02d}:{seconds:02d}")

# セッション一覧を表示
if st.session_state.sessions:
    st.markdown("---")
    st.markdown("### セッション履歴")
    for i, session in enumerate(reversed(st.session_state.sessions), 1):
        start = datetime.fromisoformat(session['start'])
        end = datetime.fromisoformat(session['end'])
        dur = session['duration']
        st.text(f"{len(st.session_state.sessions) - i + 1}. {start.strftime('%H:%M:%S')} - {end.strftime('%H:%M:%S')} ({int(dur // 3600):02d}:{int((dur % 3600) // 60):02d}:{int(dur % 60):02d})")

# 自動更新（計測中のみ）
if st.session_state.is_tracking:
    st.rerun()
