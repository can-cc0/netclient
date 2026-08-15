"""Basit ag istemcisi (Kivy) — bir API'ye JSON POST atar, yaniti ekranda gosterir.
Odev: metin girisi + 'Gonder' butonu + ScrollView icinde Label.
"""
import json
import threading

from kivy.app import App
from kivy.clock import mainthread
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

import requests

# Simdilik gecici test adresi. Daha sonra kendi sunucunla degistir.
API_URL = "https://httpbin.org/post"


class ClientUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=dp(10), spacing=dp(10), **kwargs)

        # 1) Metin giris alani
        self.inp = TextInput(
            hint_text="Mesaj yaz...", multiline=False,
            size_hint_y=None, height=dp(50),
        )
        self.add_widget(self.inp)

        # 2) Gonder butonu
        self.btn = Button(text="Gonder", size_hint_y=None, height=dp(50))
        self.btn.bind(on_release=self.on_send)
        self.add_widget(self.btn)

        # 3) ScrollView icinde Label
        sv = ScrollView()
        self.out = Label(
            text="Yanit burada gorunecek.",
            size_hint_y=None, halign="left", valign="top",
        )
        # Label'in metne gore sarilmasi ve yuksekligi
        self.out.bind(width=lambda *_: setattr(
            self.out, "text_size", (self.out.width - dp(16), None)))
        self.out.bind(texture_size=lambda *_: setattr(
            self.out, "height", self.out.texture_size[1]))
        sv.add_widget(self.out)
        self.add_widget(sv)

    def on_send(self, *_):
        self.out.text = "Gonderiliyor..."
        msg = self.inp.text
        # Agi arka planda calistir ki arayuz donmasin
        threading.Thread(target=self._worker, args=(msg,), daemon=True).start()

    def _worker(self, msg):
        try:
            r = requests.post(API_URL, json={"message": msg}, timeout=30)
            try:
                body = json.dumps(r.json(), indent=2, ensure_ascii=False)
            except ValueError:
                body = r.text
            self._show(f"[HTTP {r.status_code}]\n{body}")
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
