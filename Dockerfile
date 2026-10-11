FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DISPLAY=:0 \
    QT_QPA_PLATFORM=xcb \
    REPORT_DIR=/app/reports \
    LANG=C.UTF-8

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pyqt6 qt6-qpa-plugins \
        xvfb x11vnc fluxbox novnc websockify procps \
        libxkbcommon-x11-0 libxcb-cursor0 libxcb-icccm4 libxcb-image0 \
        libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0 \
        libxcb-xinerama0 libxcb-xfixes0 libgl1 libegl1 \
        fonts-dejavu-core \
    && ln -sf /usr/share/novnc/vnc.html /usr/share/novnc/index.html \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/src
COPY src /app/src
RUN mkdir -p /app/reports

EXPOSE 6080 5900

CMD ["sh", "-c", "Xvfb :0 -screen 0 1280x800x24 -nolisten tcp & sleep 1; fluxbox >/dev/null 2>&1 & x11vnc -display :0 -forever -shared -nopw -quiet -rfbport 5900 >/dev/null 2>&1 & websockify --web /usr/share/novnc 6080 localhost:5900 >/dev/null 2>&1 & echo 'Open http://localhost:6080/vnc.html?autoconnect=1&resize=scale'; while true; do python3 main.py; sleep 1; done"]