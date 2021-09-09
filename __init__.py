from aqt.qt import *
import json
from anki import hooks
from aqt import editor
from aqt.webview import AnkiWebView
from aqt.utils import showInfo
from aqt.theme import theme_manager
from aqt import addcards
from aqt import gui_hooks
from aqt import mw

class Editor_Preview(object):

    def addcards_hook(self, ac: addcards):
        layout = ac.form.fieldsArea.layout()
        ac.web_view = AnkiWebView(title="preview")
        layout.addWidget(ac.web_view)
        ac.web_view.stdHtml(
            ac.mw.reviewer.revHtml(),
            css=["css/reviewer.css"],
            js=[
                "js/mathjax.js",
                "js/vendor/mathjax/tex-chtml.js",
                "js/reviewer.js",
            ],
            context=ac,
        )
        note = ac.editor.note
        if ac.editor.card:
            ord = ac.editor.card.ord
        else:
            ord = 0
        c = note.ephemeral_card()
        a = ac.mw.prepare_card_text_for_display(c.answer())
        a = gui_hooks.card_will_show(a, c, "clayoutAnswer")
        bodyclass = theme_manager.body_classes_for_card_ord(c.ord, ac.mw.pm.night_mode())
        ac.web_view.eval(f"_showAnswer({json.dumps(a)},'{bodyclass}');")
        self.web_view = ac.web_view

    def onedit_hook(self, note):
        c = note.ephemeral_card()
        a = mw.prepare_card_text_for_display(c.answer())
        a = gui_hooks.card_will_show(a, c, "clayoutAnswer")
        bodyclass = theme_manager.body_classes_for_card_ord(c.ord, mw.pm.night_mode())
        self.web_view.eval(f"_showAnswer({json.dumps(a)},'{bodyclass}');")


eprev = Editor_Preview()
gui_hooks.add_cards_did_init.append(eprev.addcards_hook)
gui_hooks.editor_did_fire_typing_timer.append(eprev.onedit_hook)
