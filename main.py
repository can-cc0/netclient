"""Basit sohbet istemcisi (Kivy) — kendi LLM sunucuna (OpenAI-uyumlu) baglanir.
Metin girisi + 'Gonder' butonu + ScrollView icinde yanit.
"""
import json
import ssl
import threading
import urllib.request

from kivy.app import App
from kivy.clock import mainthread
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

try:
    import certifi
    _SSL = ssl.create_default_context(cafile=certifi.where())
except Exception:
    _SSL = ssl.create_default_context()

# Kendi bulut sunucun (Colab + ngrok). Adres degisirse sadece burayi guncelle.
API_URL = "https://encounter-shortcake-uncorrupt.ngrok-free.dev/v1/chat/completions"


class ClientUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=dp(10), spacing=dp(10), **kwargs)

        self.inp = TextInput(hint_text="Mesaj yaz...", multiline=False,
                             size_hint_y=None, height=dp(50))
        self.add_widget(self.inp)

        self.btn = Button(text="Gonder", size_hint_y=None, height=dp(50))
        self.btn.bind(on_release=self.on_send)
        self.add_widget(self.btn)

        sv = ScrollView()
        self.out = Label(text="Yanit burada gorunecek.", size_hint_y=None,
                         halign="left", valign="top")
        self.out.bind(width=lambda *_: setattr(
            self.out, "text_size", (self.out.width - dp(16), None)))
        self.out.bind(texture_size=lambda *_: setattr(
            self.out, "height", self.out.texture_size[1]))
        sv.add_widget(self.out)
        self.add_widget(sv)

    def on_send(self, *_):
        self.out.text = "Dusunuyor..."
        threading.Thread(target=self._worker, args=(self.inp.text,), daemon=True).start()

    def _worker(self, msg):
        try:
            payload = json.dumps({
                "messages": [{"role": "user", "content": msg}],
                "temperature": 0.7,
                "max_tokens": 256,
            }).encode("utf-8")
            req = urllib.request.Request(
                API_URL, data=payload, method="POST",
                headers={
                    "Content-Type": "application/json",
                    "ngrok-skip-browser-warning": "true",
                },
            )
            with urllib.request.urlopen(req, timeout=240, context=_SSL) as resp:
                data = json.loads(resp.read().decode("utf-8", "replace"))
            try:
                text = data["choices"][0]["message"]["content"]
            except (KeyError, IndexError, TypeError):
                text = json.dumps(data, indent=2, ensure_ascii=False)
            self._show(text.strip())
        except Exception as e:
            self._show("Baglanti hatasi: " + str(e))

    @mainthread
    def _show(self, text):
        self.out.text = text


class NetClientApp(App):
    def build(self):
        return ClientUI()


if __name__ == "__main__":
    NetClientApp().run()
